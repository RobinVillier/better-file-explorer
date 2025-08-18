import os
import subprocess


def compile_qrc():
    # Chemin vers pyside2-rcc dans Maya
    rcc_path = r"F:\Autodesk\Maya2023\bin\pyside2-rcc.exe"

    # Fichiers QRC à compiler
    qrc_file = os.path.join("resources", "resources.qrc")
    output_py = os.path.join("ui", "resources_rc.py")

    if not os.path.exists(qrc_file):
        print(f"[Erreur] Fichier QRC introuvable : {qrc_file}")
        return

    command = [rcc_path, qrc_file, "-o", output_py]
    try:
        subprocess.run(command, check=True)
        print(f"[OK] Compilation réussie : {output_py}")
    except subprocess.CalledProcessError as e:
        print(f"[Erreur] Erreur pendant la compilation : {e}")


if __name__ == "__main__":
    compile_qrc()
