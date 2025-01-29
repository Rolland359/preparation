# coding : "UTF-8"
import os
import sys
import shutil
import getpass
import threading
import subprocess
from Recherche_projet import recherche_projet
from preparation_3D_ import recherche_db, formatage_dossier

# Constantes pour les chemins de fichiers
REVIT_PATH = "C:/Program Files/Autodesk/Revit 2022/Revit.exe"
GABARIT_PATH = "O:/TECHNIQUE/SYNCHRO/Gabarit/RTE/Revit-2022/Gabarit ABYREF_LOGT_GP3D.rte"
ONLYOFFICE_PATH = "C:/Program Files/ONLYOFFICE/DesktopEditors/DesktopEditors.exe"
# GOOGLE_EARTH_PATH = "C:/Program Files/Google/Google Earth Pro/client/googleearth.exe"

# Ouvrir le fichier gabarit dans Revit
def open_with_apk(apk, file):
    command = ['start', '', apk, file]
    try:
        subprocess.run(command, check=True, shell=True)
        print(f"Le fichier \"{os.path.basename(file)}\" a été ouvert avec succès.")
    except subprocess.CalledProcessError as e:
        print(f"Erreur rencontrée lors de l'ouverture de {file} avec {apk}: {e}")

def get_user_input():
    date = input("Entrer la date [2024-2025]: ")
    saisie = input("Entrez le PROJET BC DOSSIER : ").split(" ")
    return date, saisie

def copy_prepared_files(source, destination):
    print("Début du copie des fichier préparé ...")
    shutil.copytree(source, os.path.join(destination, "2_Preparation"))
    os.mkdir(os.path.join(destination, "REVIT"))
    print("Fin du copie des fichire préparé ...")

def find_file_with_extension(directory, extensions):
    for root, _, files in os.walk(directory):
        for file in files:
            if extensions[0] in file:
                return os.path.join(root, file)
            elif any(file.endswith(ext) for ext in extensions):
                return os.path.join(root, file)
    return None

def main():
    date, saisie = get_user_input()
    projet, bc, dossier = saisie[0], saisie[1], formatage_dossier(saisie[2])
    # recupere le lien et le nom du projet :
    lien_projet, nom_projet = recherche_projet(projet, bc, espace="3D", date=date)
   
    if not nom_projet:
        print("Aucun dossier trouvé, \nveuillez vérifier votre saisie ou le BC ....")
        return

    # recherche du dossier préparé :
    source_initial_prepa = recherche_db(dossier, f"{lien_projet}/2_Preparation/")
    if not source_initial_prepa:
        print("Fin du programme ...")
        input("Tapez sur Entré ....")
        sys.exit()
    else :
        print(source_initial_prepa)
    
    # Recuperer le nom de l'utilisateur et le mettre dans un variable nom :
    nom = "M" + getpass.getuser()
    print(nom)

    destination_local = f"D:/{nom}/BuildingMap-2025/{nom_projet}/{dossier}/PROD/"
    
    # copier les fichier préparé dans la destination de préparation :
    copy_prepared_files(source_initial_prepa, destination_local)

    # Rehcerche de la fp et dy fichier kmz :
    FP = find_file_with_extension(os.path.join(destination_local, "2_Preparation"), ["FP"])
    kmz = find_file_with_extension(os.path.join(destination_local, "2_Preparation"), [".kml", ".kmz"])

    if not kmz:
        print("Pas de kmz trouvé ...")
    else :
        print("\n", "-"*50, "\nLe lien vers le fichier kmz :")
        print(kmz)
        print("-"*50, "\n")
    #. ........

    # ouvrir les ficher avec leurs apk respectifs :
    threads = [
        threading.Thread(target=open_with_apk, args=(ONLYOFFICE_PATH, FP)),
        threading.Thread(target=open_with_apk, args=(REVIT_PATH, GABARIT_PATH)),
        # threading.Thread(target=open_with_apk, args=(GOOGLE_EARTH_PATH, kmz))
    ]

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    for root,dirs,_ in os.walk(destination_local):
        for folder in dirs:
            if "Plans à utiliser" in folder:
                plan_a_utiliser = os.path.join(root,folder)
                break
    
    # Ouvrir le DB sur le plan de Niveau, préparé sur le Plan à utiliser 
    try:
        os.startfile(destination_local)
        os.startfile(plan_a_utiliser)
        os.startfile(kmz)
    except (Exception, OSError) as e:
        print(f"Erreur renncontré : {e}")


if __name__== "__main__":
    # Mise en forme :
    os.system("title PROD_3D")
    os.system("color a")
    # lancement des procedures et fonctions :
    main()
    a = input("Appuyez sur entrée pour quitter")