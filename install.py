"""
==================================================
SCOOBA

Installer

Purpose:
Checks project structure and prepares the
environment for future model installation.

Author: Sachin
==================================================
"""

from pathlib import Path


PROJECT_FOLDERS = [
    "models",
    "models/speech",
    "models/tts",
    "models/vision",
    "models/wakeword",
    "data",
    "data/cache",
    "data/memory",
    "data/temp",
    "data/voices",
    "logs"
]


def create_folders():

    print("\n📁 Checking project folders...\n")

    for folder in PROJECT_FOLDERS:

        path = Path(folder)

        if not path.exists():

            path.mkdir(parents=True)

            print(f"✅ Created : {folder}")

        else:

            print(f"✔ Exists   : {folder}")


def main():

    print("=" * 50)
    print("SCOOBA INSTALLER")
    print("=" * 50)

    create_folders()

    print("\n✅ Installation completed successfully.")

    print("\nFuture installers will automatically download:")

    print(" • Aurora Voice")

    print(" • Vosk Models")

    print(" • Wake Word Models")

    print(" • Vision Models")


if __name__ == "__main__":

    main()