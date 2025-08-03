# Bot de Détection et Clic d'Images

Ce bot détecte automatiquement des images à l'écran et clique dessus quand elles sont trouvées.

## 📁 Structure du projet

```
Bot_click_image/
├── main.py           # Script principal du bot
├── parametre.txt     # Fichier de configuration
├── image/           # Dossier contenant les images à détecter
└── README.md        # Ce fichier
```

## 🚀 Installation

1. Les dépendances ont été installées automatiquement :
   - opencv-python (pour la détection d'images)
   - pyautogui (pour capturer l'écran et cliquer)
   - numpy (pour le traitement des images)
   - pillow (support d'images)

## ⚙️ Configuration

Modifiez le fichier `parametre.txt` pour ajuster les paramètres :

- **SEUIL_CONFIANCE** (0.0 à 1.0) : Précision de la détection (0.8 = 80%)
- **DELAI_SCAN** : Temps en secondes entre chaque scan
- **MODE_DEBUG** : Affiche plus d'informations (True/False)

## 📸 Ajout d'images

1. Placez vos images de référence dans le dossier `image/`
2. Formats supportés : PNG, JPG, JPEG, BMP, TIFF
3. Plus l'image est précise, meilleure sera la détection

## 🎮 Utilisation

1. **Ajoutez vos images** dans le dossier `image/`
2. **Configurez les paramètres** dans `parametre.txt`
3. **Lancez le bot** :
   ```
   python main.py
   ```
4. **Arrêtez le bot** avec `Ctrl+C`

## 📊 Informations affichées

Le bot affiche dans la console :
- ✅ Images détectées avec le pourcentage de confiance
- 📍 Coordonnées exactes du clic
- ⏰ Horodatage de chaque action
- 🔍 Informations de debug (si activé)

## ⚠️ Notes importantes

- Le bot clique sur la **première image** détectée à chaque cycle
- Plus le seuil de confiance est élevé, plus la détection est stricte
- Testez d'abord avec des images simples et distinctes
- Le bot continue à tourner jusqu'à ce que vous l'arrêtiez

## 🛠️ Dépannage

- **"Aucune image trouvée"** : Vérifiez que le dossier `image/` contient des fichiers
- **"Image non détectée"** : Réduisez le seuil de confiance ou utilisez une image plus précise
- **Clic imprécis** : L'image de référence doit être exactement celle affichée à l'écran
