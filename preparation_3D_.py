# coding: "UTF-8"
import os
import shutil
import sys
import openpyxl
import zipfile
import getpass
import threading
import concurrent.futures
from Recherche_projet import recherche_projet

def formatage_dossier(dossier):
    """Formate le dossier sur 4 caractères avec des zéros en préfixe."""
    return str(dossier).zfill(4)

def recherche_db(dossier, parent):
    """Recherche un dossier dans un répertoire parent."""
    dossier_formate = formatage_dossier(dossier)
    for root, dirs, _ in os.walk(parent):  # Ignorer les fichiers
        for dire in dirs:
            if dossier_formate == formatage_dossier(dire):
                return os.path.join(root, dire)
    print(f"Aucun dossier {dossier} trouvé dans les données brutes...")
    return None

def copie_donnees(source, destination, use_xcopy=False):
    """Copie un dossier source vers une destination (thread-safe)."""
    if not os.path.exists(source):
        print(f"Le dossier {source} n'existe pas. Veuillez faire une mise à jour des outils.")
        return

    if os.path.exists(destination):
        print(f"Le dossier {destination[-4:]} existe déjà.")
        return
    
    try:
        if use_xcopy:
            os.makedirs(os.path.dirname(destination), exist_ok=True) # Créer le répertoire parent si inexistant
            os.system(f"xcopy \"{source}\" \"{destination}\" /s /i /y /q")
        else:
            shutil.copytree(source, destination)
        print(f"Le dossier {destination} a été créé avec succès.")
    except OSError as e:
        print(f"Erreur lors de la copie : {e}")

def maj_grille_controle(destination_preparation, dossier):
    """Met à jour la grille de contrôle Excel."""
    for elm in os.listdir(destination_preparation):
        if "Grille contrôle Globale" in elm:
            src = os.path.join(destination_preparation, elm)
            dest = os.path.join(destination_preparation, elm.replace("XXXX", formatage_dossier(dossier)))
            os.rename(src, dest)

            try:
                wb = openpyxl.load_workbook(dest)
                wb["Contrôle PM"]["C2"] = formatage_dossier(dossier)
                wb["Contrôle Global"]["D2"] = formatage_dossier(dossier)
                wb.save(dest)
                wb.close()
            except Exception as e:
                print(f"Erreur lors de la mise à jour de la grille de contrôle : {e}")
            return # Sortir après avoir trouvé et mis à jour le fichier

def decompose_fichier_zip(destination_donnee_brute):
    """Décompresse les fichiers ZIP et les supprime."""
    for root, _, files in os.walk(destination_donnee_brute):
        for file in files:
            if file.endswith(".zip"):
                filepath = os.path.join(root, file)
                try:
                    with zipfile.ZipFile(filepath, "r") as zip_obj:
                        zip_obj.extractall(root)
                    os.remove(filepath)
                    print(f"Le fichier zip {file} a été extrait avec succès...")
                except zipfile.BadZipFile:
                    print(f"Fichier ZIP corrompu : {file}")
                except Exception as e:
                    print(f"Erreur lors de l'extraction de {file} : {e}")

def copier_photos_et_autres(source, destination, type_copie):
    """Copie les photos, façades/coupes ou plans de masse en utilisant le threading."""
    if os.path.exists(source):
        os.makedirs(destination, exist_ok=True) #Créer le dossier de destination si inexistant
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = [executor.submit(shutil.copy2, os.path.join(source, elm), destination)
                       for elm in os.listdir(source)]
            for future in concurrent.futures.as_completed(futures): # Attendre la fin de toutes les copies
                try:
                    future.result()  # Récupérer le résultat (ou l'exception)
                except Exception as e:
                    print(f"Erreur lors de la copie d'un fichier {type_copie}: {e}")
    else:
        print(f"Pas de {type_copie}")

nom = "M"+getpass.getuser()
espace = "3D"
winrar = "C:/Program Files/WinRAR/WinRAR.exe"
source_dossier_xxx = "C:/Futurmap/Outils/Preparation/Gestion de Patrimoine/XXXX"

if __name__=="__main__":
    os.system("color a")
    os.system("title R_Prepa3D ")

    date = str(input("Entrer la date [2024-2025]: "))
    
    # Recupérer les information de base via l'utilisateur :
    saisie = input("Entrez le PROJET BC DOSSIER : ").split(" ")
    projet, bc, dossier = saisie[0],saisie[1],saisie[2]

    # recupere le lien et le nom du projet :
    lien_projet, nom_projet = recherche_projet(projet,bc,espace=espace,date=date)

    # si la rehcherche a trouvé un projet :
    if nom_projet:

        print(f"Le nom du projet : {nom_projet}")

        source_initial_db = lien_projet+"/1_Donnees_Brutes/"

        destination_preparation = f"D:/{nom}/BuildingMap-2025/"+nom_projet+"/2_Preparation/"+formatage_dossier(dossier)
        destination_donnée_brute = f"D:/{nom}/BuildingMap-2025/"+nom_projet+"/1_Donnees_Brutes/"+formatage_dossier(dossier)

        # Copie du dossier xxx du disque C:/ vers le disque D:/
        copie_donnees(source_dossier_xxx,destination_preparation,use_xcopy=False)

        # recherche du donnée brute :
        source_initial_db = recherche_db(dossier,source_initial_db)
        if not source_initial_db:
            print("Fin du programme ...")
            input("Tapez sur Entré ....")
            sys.exit()

        else :
            print(source_initial_db)
        
        # Copie du donnée brute vers le disque D:/ - Utilisation de xcopy pour les données brutes
        copie_donnees(source_initial_db, destination_donnée_brute, use_xcopy=True)
        
        # copie du DB vers preparé :
        #       decopréssé tout les fichier rar dans chaque sous dossier:
        decompose_fichier_zip(destination_donnée_brute)

        # Définition des lien source et destination :
        # PHOTOS
        source_photos = destination_donnée_brute+"/1. Pièces Générales/1.1. Documents généraux/1.1.2 Photos/"
        destination_photos = destination_preparation+"/BATIMENT 01/Photos/Photos client/"
        # FACADE ET COUPE
        source_facade_coupe = destination_donnée_brute+"/1. Pièces Générales/1.2. Sites et architecture/1.2.3. Plans coupes-façades"
        destination_facade_coupe = destination_preparation+"/BATIMENT 01/Plans/Plans complémentaires/Façade et coupes/"
        # CET
        source_cet = destination_donnée_brute+"/1. Pièces Générales/1.3. Corps d'états techniques/"
        destination_cet = destination_preparation+"/BATIMENT 01/Plans/1.3. Corps d'états techniques/"
        # PLAN DE MASSE
        source_pm = destination_donnée_brute+"/1. Pièces Générales/1.2. Sites et architecture/1.2.1. Masse-Topo-VRD/"
        destination_pm = destination_preparation+"/BATIMENT 01/Plans/Plans complémentaires/Plans de masse SITE/"
        # FICHE PATRIMOINE
        source_FP = destination_donnée_brute+"/1. Pièces Générales/1.1. Documents généraux/1.1.1. Fiches patrimoniales/"
        destination_FP = destination_preparation+"/"
        # LANCEMENTS DES COPIES AVEC THREAD :
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = []
            #       copie des photos:
            futures.append(executor.submit(copier_photos_et_autres, source_photos, destination_photos, "Photos Clients"))
            #       copie des façades et coupes:
            futures.append(executor.submit(copier_photos_et_autres, source_facade_coupe, destination_facade_coupe, "façades et coupes"))
            #       copie du CET
            futures.append(executor.submit(copie_donnees, source_cet, destination_cet))
            #       copie du plan de Masse:
            futures.append(executor.submit(copier_photos_et_autres, source_pm, destination_pm, "Plans de masse"))
            #       copie du FP:
            futures.append(executor.submit(copier_photos_et_autres, source_FP, destination_FP, "FICHE PATRIMOINE"))

            for future in concurrent.futures.as_completed(futures):
                try:
                    future.result()
                except Exception as e:
                    print(f"Une erreur s'est produite lors d'une copie threadée: {e}")

        # Mise à jour du Grille de contrôle:
        maj_grille_controle(destination_preparation,dossier)

        # Gestion de la copie du FP qui est spéciale
        try:
            for elm in os.listdir(destination_donnée_brute):
                if "FP" in elm.upper():
                    shutil.copy2(os.path.join(destination_donnée_brute, elm), destination_preparation)
            print("Fiche patrimoniale copiée")
        except Exception as e:
            print(f"Erreur lors de la copie du FP : {e}")

        # Ouvrir le DB sur le plan de Niveau, préparé sur le Plan à utiliser
        try:
            os.startfile(destination_donnée_brute)
            os.startfile(destination_preparation)
        except AttributeError: # Pour les systèmes non-Windows
            import subprocess
            subprocess.Popen(['xdg-open', destination_donnée_brute]) # Exemple Linux
            subprocess.Popen(['xdg-open', destination_preparation]) # Exemple Linux
        except OSError as e:
            print(f"Erreur lors de l'ouverture des dossiers : {e}")
            
        print("La préparation est terminé, le programme va quiter")

    # il n'y a pas de projet correspondante à la saisie de l'utilisateur:
    else:
        print("Vérifiez  votre saisie ...\nFin du programme")
        sys.exit()

    a = input("Tapez sur Entré ....")
