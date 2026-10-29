import os
import subprocess

# --- PARAMÈTRES À MODIFIER ---
INPUT_FILE = None  # Si None, cherche automatiquement l'unique .mp4 du dossier
OUTPUT_FILE = "timelapse.mp4"
TARGET_DURATION_SECONDS = 30  # Durée finale souhaitée
# -----------------------------


def get_input_file():
    """Détermine le fichier d'entrée si non spécifié."""
    if INPUT_FILE:
        return INPUT_FILE

    if not os.path.exists('input'):
        os.makedirs('input')

    mp4_files = [f for f in os.listdir('input') if f.endswith('.mp4')]
    assert len(mp4_files) == 1, f"Erreur : INPUT_FILE n'est pas défini et {len(mp4_files)} fichier(s) .mp4 trouvé(s). Il doit y en avoir exactement un seul."
    return 'input/' + mp4_files[0]


def get_duration(filename):
    """Récupère la durée de la vidéo en secondes."""
    result = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", filename], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    return float(result.stdout)


def create_timelapse(input_path, output_path, target_duration):
    if not os.path.exists(input_path):
        print(f"Erreur : Le fichier {input_path} n'existe pas.")
        return

    current_duration = get_duration(input_path)
    print(f"Durée actuelle : {current_duration:.2f}s")
    print(f"Durée cible : {target_duration}s")

    if target_duration >= current_duration:
        print("La durée cible est supérieure ou égale à la durée actuelle. Aucun traitement nécessaire (ou la vidéo sera ralentie).")
        # On peut quand même continuer si l'utilisateur veut ralentir, mais ici on vise le timelapse.

    # Calcul du facteur de vitesse (setpts)
    # Pour accélérer, setpts doit être < 1.
    # vitesse = current / target. pts_factor = 1 / vitesse = target / current.
    pts_factor = target_duration / current_duration

    # Pour l'audio (atempo), il faut l'inverse, mais souvent pour un timelapse on supprime l'audio
    # ou on l'accélère. FFmpeg limite atempo entre 0.5 et 2.0.
    # Pour simplifier un timelapse, on va souvent supprimer l'audio ou ne pas s'en occuper.
    # Ici, on accélère la vidéo.

    cmd = [
        "ffmpeg",
        "-y",
        "-i",
        input_path,
        "-filter:v",
        f"setpts={pts_factor}*PTS,fps=30",
        "-c:v",
        "h264_videotoolbox",  # Utilise la puce du Mac (très rapide)
        "-b:v",
        "6000k",  # Définit un débit binaire (à ajuster selon la qualité voulue)
        "-an",
        output_path
    ]

    print(f"Exécution de la commande : {' '.join(cmd)}")
    subprocess.run(cmd)
    print(f"Terminé ! Vidéo sauvegardée dans {output_path}")


if __name__ == "__main__":
    input_to_use = get_input_file()
    create_timelapse(input_to_use, OUTPUT_FILE, TARGET_DURATION_SECONDS)
