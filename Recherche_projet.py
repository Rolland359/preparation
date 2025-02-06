# coding: "utf-8"
import os

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

def recherche_projet(projet, bc, espace="3D", date="2024"):
    """
    Recherche un projet dans le disque Q: en utilisant le nom du projet,
    le numéro de BC et l'espace (2D ou 3D).
    """
    dossier_source = f"Q:/GP/{date}/"
    liste_projet = []

    try:
        for item in os.listdir(dossier_source):
            if projet.upper() in item.upper() and bc.upper() in item.upper():
                if espace.upper() == "3D":
                    if "_2D" not in item.upper():
                        liste_projet.append(os.path.join(dossier_source, item)) # Stocker le chemin complet
                elif espace.upper() == "2D":  # Simplification de la condition
                    if "_2D" in item.upper():
                        liste_projet.append(os.path.join(dossier_source, item)) # Stocker le chemin complet
    except FileNotFoundError:
        print(f"Dossier source non trouvé : {dossier_source}")
        return None, None # Gérer l'erreur et retourner None

    if len(liste_projet) > 1:
        print("Plusieurs projets correspondent à votre critère :")
        for elm in liste_projet:
            print("    -", elm)
        return liste_projet, None # Retourner la liste des chemins et None pour projet
    elif not liste_projet:  # Vérification plus pythonique pour une liste vide
        print("AUCUN RÉSULTAT TROUVÉ \n--------------------\nFin de recherche projet ...")
        return None, None # Retourner None pour les deux
    else:
        return liste_projet[0], os.path.basename(liste_projet[0]) # Retourner le chemin complet et le nom du projet


def get_user_input():
    date = input("Entrer la date [2024-2025]: ")
    saisie = input("Entrez le PROJET BC DOSSIER : ").split(" ")
    return date, saisie

if __name__ == "__main__":
    os.system("color a")
    os.system("title R_DbFinder V02.5BT")
    os.system("cls")

    mots_cles = input("Entrer les mots clés (projet BC espace[3D ou 2D]) séparés par un espace : ").split()

    if len(mots_cles) < 2:
        print("Veuillez entrer au moins le projet et le BC.")
        input()
        exit()
    
    try:
        projet_nom = mots_cles[0]
        bc_num = mots_cles[1]
        espace_val = mots_cles[2] if len(mots_cles) > 2 else "3D" # Valeur par défaut pour l'espace
        chemin_projet, nom_projet = recherche_projet(projet_nom, bc_num, espace_val)
        if chemin_projet:
          if isinstance(chemin_projet, list): # Gérer le cas de plusieurs résultats
            print("Veuillez affiner votre recherche.")
          else:
            os.chdir(os.path.dirname(chemin_projet)) # Changer le répertoire au parent du fichier
            os.system(f"start explorer \"{chemin_projet}\"") # Ouvrir directement le fichier/dossier
        
    except IndexError:
        print("Erreur : Nombre d'arguments incorrect.")
    except Exception as e: # Capturer les autres exceptions
        print(f"Une erreur s'est produite : {e}")

    input()