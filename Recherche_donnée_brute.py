# coding : "UTF-8"
import os

dir = os.getcwd()
def recherche_donnee_brute(projet,bc, dossier=""):
    date = "2024"
    entree = input("voulez-vous modifier la date ? (Y/N):")
    if entree =="Y" or entree =="y":
        date = input("enttrez la nouvelle date : ")
    elif entree =="N" or entree =="n":
        print("la date ne change pas ...")
    else:
        print("vous avez entrez une valeur fausse")

    dossier_source = f"Q:/GP/{str(date)}/"
    os.chdir(dossier_source)
    for elm in os.listdir():
        if projet.upper() in elm and bc.upper() in elm and "_2D" not in elm:
            dossier_source = dossier_source + str(elm) + "/1_Donnees_Brutes/"
    os.chdir(dossier_source)

    for elm in os.listdir():
        if "s" in elm:
            os.chdir(dossier_source+"/"+elm)
            for child_elm in os.listdir():
                if dossier in child_elm:
                    print(dossier)
            print(os.getcwd())

    print(dossier_source)


mot_clef = input("entrer les mots clé (projet-BC-dossier) séparer par une espace : ").split(" ")
recherche_donnee_brute(mot_clef[0],mot_clef[1],mot_clef[2])