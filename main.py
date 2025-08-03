import cv2
import pyautogui
import numpy as np
import os
import time
from datetime import datetime


class BotClickImage:
    def __init__(self):
        """Initialise le bot avec les paramètres du fichier de configuration"""
        self.seuil_confiance = 0.8
        self.delai_scan = 1.0
        self.mode_debug = True
        self.dossier_images = "image"
        self.images_templates = []
        
        # Charger les paramètres
        self.charger_parametres()
        
        # Charger les images templates
        self.charger_images_templates()
        
        # Désactiver la protection contre les mouvements de souris rapides
        pyautogui.FAILSAFE = False
        
    def charger_parametres(self):
        """Charge les paramètres depuis le fichier parametre.txt"""
        try:
            if os.path.exists("parametre.txt"):
                with open("parametre.txt", "r", encoding="utf-8") as f:
                    for ligne in f:
                        ligne = ligne.strip()
                        if ligne and not ligne.startswith("#"):
                            if "=" in ligne:
                                cle, valeur = ligne.split("=", 1)
                                cle = cle.strip()
                                valeur = valeur.strip()
                                
                                if cle == "SEUIL_CONFIANCE":
                                    self.seuil_confiance = float(valeur)
                                elif cle == "DELAI_SCAN":
                                    self.delai_scan = float(valeur)
                                elif cle == "MODE_DEBUG":
                                    self.mode_debug = valeur.lower() == "true"
                                    
            print(f"[CONFIG] Seuil de confiance: {self.seuil_confiance}")
            print(f"[CONFIG] Délai de scan: {self.delai_scan}s")
            print(f"[CONFIG] Mode debug: {self.mode_debug}")
            
        except Exception as e:
            print(f"[ERREUR] Impossible de charger les paramètres: {e}")
            print("[INFO] Utilisation des paramètres par défaut")
    
    def charger_images_templates(self):
        """Charge toutes les images du dossier image/ comme templates"""
        try:
            if not os.path.exists(self.dossier_images):
                print(f"[ERREUR] Le dossier '{self.dossier_images}' n'existe pas")
                return
                
            extensions_supportees = ['.png', '.jpg', '.jpeg', '.bmp', '.tiff']
            fichiers_images = []
            
            for fichier in os.listdir(self.dossier_images):
                if any(fichier.lower().endswith(ext) for ext in extensions_supportees):
                    fichiers_images.append(fichier)
            
            if not fichiers_images:
                print(f"[ATTENTION] Aucune image trouvée dans le dossier '{self.dossier_images}'")
                print("Formats supportés: PNG, JPG, JPEG, BMP, TIFF")
                return
            
            for fichier in fichiers_images:
                chemin_image = os.path.join(self.dossier_images, fichier)
                try:
                    template = cv2.imread(chemin_image)
                    if template is not None:
                        self.images_templates.append({
                            'nom': fichier,
                            'template': template,
                            'hauteur': template.shape[0],
                            'largeur': template.shape[1]
                        })
                        print(f"[TEMPLATE] Chargé: {fichier} ({template.shape[1]}x{template.shape[0]})")
                    else:
                        print(f"[ERREUR] Impossible de charger l'image: {fichier}")
                except Exception as e:
                    print(f"[ERREUR] Erreur lors du chargement de {fichier}: {e}")
            
            print(f"[INFO] {len(self.images_templates)} template(s) chargé(s)")
            
        except Exception as e:
            print(f"[ERREUR] Erreur lors du chargement des templates: {e}")
    
    def capturer_ecran(self):
        """Capture l'écran et le convertit en format OpenCV"""
        try:
            screenshot = pyautogui.screenshot()
            screenshot_np = np.array(screenshot)
            screenshot_cv = cv2.cvtColor(screenshot_np, cv2.COLOR_RGB2BGR)
            return screenshot_cv
        except Exception as e:
            print(f"[ERREUR] Impossible de capturer l'écran: {e}")
            return None
    
    def detecter_image(self, screenshot, template_info):
        """Détecte une image template dans la capture d'écran"""
        try:
            template = template_info['template']
            
            # Effectuer la correspondance de template
            resultat = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
            
            # Trouver la meilleure correspondance
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(resultat)
            
            if max_val >= self.seuil_confiance:
                # Calculer les coordonnées du centre de l'image détectée
                x_centre = max_loc[0] + template_info['largeur'] // 2
                y_centre = max_loc[1] + template_info['hauteur'] // 2
                
                return {
                    'detecte': True,
                    'confiance': max_val,
                    'position': (x_centre, y_centre),
                    'rectangle': (max_loc[0], max_loc[1], 
                                template_info['largeur'], template_info['hauteur']),
                    'nom_template': template_info['nom']
                }
            
            return {'detecte': False, 'confiance': max_val}
            
        except Exception as e:
            print(f"[ERREUR] Erreur lors de la détection: {e}")
            return {'detecte': False, 'confiance': 0.0}
    
    def cliquer_sur_position(self, x, y):
        """Clique sur les coordonnées spécifiées"""
        try:
            pyautogui.click(x, y)
            timestamp = datetime.now().strftime("%H:%M:%S")
            print(f"[{timestamp}] CLIC effectué à la position ({x}, {y})")
            return True
        except Exception as e:
            print(f"[ERREUR] Impossible de cliquer à la position ({x}, {y}): {e}")
            return False
    
    def executer_cycle_detection(self):
        """Exécute un cycle de détection et de clic"""
        if not self.images_templates:
            print("[ATTENTION] Aucun template d'image chargé")
            return False
        
        # Capturer l'écran
        screenshot = self.capturer_ecran()
        if screenshot is None:
            return False
        
        # Tester chaque template
        for template_info in self.images_templates:
            resultat = self.detecter_image(screenshot, template_info)
            
            if resultat['detecte']:
                timestamp = datetime.now().strftime("%H:%M:%S")
                x, y = resultat['position']
                confiance = resultat['confiance']
                nom_image = resultat['nom_template']
                
                print(f"[{timestamp}] IMAGE DÉTECTÉE: '{nom_image}'")
                print(f"[{timestamp}] Confiance: {confiance:.2%}")
                print(f"[{timestamp}] Position de clic: ({x}, {y})")
                
                # Effectuer le clic
                if self.cliquer_sur_position(x, y):
                    print(f"[{timestamp}] Action terminée avec succès")
                    return True
                else:
                    print(f"[{timestamp}] Échec du clic")
            
            elif self.mode_debug:
                print(f"[DEBUG] '{template_info['nom']}' non détecté (confiance: {resultat['confiance']:.2%})")
        
        return False
    
    def demarrer(self):
        """Démarre la boucle principale du bot"""
        print("="*60)
        print("🤖 BOT DE DÉTECTION ET CLIC D'IMAGES")
        print("="*60)
        print("Appuyez sur Ctrl+C pour arrêter le bot")
        print("="*60)
        
        if not self.images_templates:
            print("[ERREUR] Aucune image template disponible. Ajoutez des images dans le dossier 'image/'")
            return
        
        try:
            while True:
                self.executer_cycle_detection()
                time.sleep(self.delai_scan)
                
        except KeyboardInterrupt:
            print("\n[INFO] Bot arrêté par l'utilisateur")
        except Exception as e:
            print(f"[ERREUR] Erreur inattendue: {e}")

def main():
    """Point d'entrée principal du programme"""
    bot = BotClickImage()
    bot.demarrer()

if __name__ == "__main__":
    main()