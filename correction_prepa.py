# coding: "UTF-8"
import os
import shutil
import sys

def recherche_projet(projet, bc, espace="3D"):
    initial_dir = "D:/BuildingMap-2025/"
    for root, dirs, _ in os.walk(initial_dir):
        for dire in dirs :
            if projet.upper() in dire and bc.upper() in dire :
                if espace == "3D" and "_2D" not in dire:
                    return os.path.join(root, dire)
                    print("le dossier a ete trouvé 3d ...")
                elif espace == "2D" and "_2D" in dire:
                    return os.path.join(root, dire)
                    print("le dossier trouvé dans 2d ...")

def recherche_dossier(lien_projet, dossier):
    for root, dirs, _ in os.walk(lien_projet+"/2_Preparation/"):
        for dire in dirs:
            if formatage_dossier(dire) == formatage_dossier(dossier):
                return os.path.join(root, dire)
            else:
                print("Dossier non trouvé ...")

def formatage_dossier(dossier):
    return str(dossier).zfill(4)


if __name__=="__main__":
    #date = input("Entrez la date [2024-2025]: ")
    saisie = input("Entrer PROJET BC DOSSIER : ").split(" ")
    projet, bc, dossier = saisie[0], saisie[1], saisie[2]

    source_dossier_xxx = "C:/Futurmap/Outils/Preparation/Gestion de Patrimoine/XXXX"


    # Rechercher le projet dans le disque local D
    prj = recherche_projet(projet, bc)
    # Recherche du dossier dans le disque D
    destination_dossier = recherche_dossier(prj, dossier)

    #os.system(f'xcopy "{source_dossier_xxx}" "{destination_dossier}" /T /E /I /Y /Q')
    #shutil.copytree(source_dossier_xxx, destination_dossier, dirs_exist_ok=True)
    # copier tous les sous_dossier du dossier xxx vers destination :

