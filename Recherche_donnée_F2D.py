# coding : "UTF-8"
import os
from Recherche_projet import recherche_db, recherche_projet, formatage_dossier, get_user_input

from readMe import *
pivot = ["/1_Donnees_Brutes/","/2_Preparation/","/6_Livraison/1_Livraison_Production/"]

def main():
    date, saisie = get_user_input()
    projet, bc, dossier = saisie[0], saisie[1], formatage_dossier(saisie[2])
    parent = pivot[int(input("Choisir entre : \n\t0 - donnée brute \n\t1 - préparé ou \n\t2 - livraison production \n>>> "))]

    # recupere le lien et le nom du projet :
    lien_projet = os.path.join(recherche_projet(projet,bc,espace="2D",date=date)[0],parent)

    if not lien_projet:
        print("Aucun résultat trouvé ...")
        print("Fin du programme ...")
        input()
        exit(1)
    
    # rechercher le dossier :




if __name__=="__main__":
    os.system("color a")
    os.system("title R_DbFinder V02.5BT")

    Read_Me()
    os.system("cls")
    main()
    a = input()



