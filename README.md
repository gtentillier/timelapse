# Timelapse Vidéo

Ce script Python permet d'accélérer une vidéo pour qu'elle atteigne une durée cible précise, créant ainsi un effet de timelapse.

## Prérequis

- **Python 3**
- **FFmpeg** : Doit être installé et accessible dans votre PATH (`ffmpeg` et `ffprobe`).

## Performance

Le script prend deux foix moins de temps que la durée de la vidéo originale pour générer le timelapse (test réalisé sur une vidéo de 1h08, 30FPS, et pour un timelapse de 30s).

## Utilisation

1. Placez votre vidéo source dans le dossier `input`.
2. Si vous avez plusieurs fichiers `.mp4`, ouvrez [timelapse.py](/Users/gaston/Code/projets/timelapse/timelapse.py) et modifiez `INPUT_FILE`. Sinon, le script détectera automatiquement l'unique fichier présent.
3. Lancez la génération :
   - **Via VS Code** : `Cmd+Shift+B` (ou Terminal > Exécuter la tâche de build > Générer le Timelapse).
   - **Via le terminal** : `python3 timelapse.py`.

## Fonctionnement

Le script utilise `ffprobe` pour obtenir la durée originale, calcule le facteur d'accélération nécessaire, puis utilise `ffmpeg` avec le filtre `setpts` pour traiter la vidéo. L'audio est supprimé par défaut pour un rendu timelapse standard.
