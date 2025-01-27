# coding : "UTF-8"
import os

pivot = ["/1_Donnees_Brutes/","/2_Preparation/","/6_Livraison/1_Livraison_Production/"]

def recherche_donnee_brute(projet,bc, parametre, dossier="",date = "2024"):
    # le dossier source ou racine c'est Q:/GP/ et on met la date en suite elle peut varier donc prevoir un moyen de le changer
    dossier_source = f"Q:/GP/{str(date)}/"

    # On se met dans le dossier source, on change le dossier courant
    os.chdir(dossier_source)

    # iterer sur tous les éléments dans le dossier courand qui est le dossier source
    # on devrait obtenir la liste de tous les projet normalements
    for elm in os.listdir():
        # on va filtrer sur les projet 3D, qui contient le nom du projet saisi et le numéro du BC
        if projet.upper() in elm and bc.upper() in elm and "_2D" not in elm:
            # si le projet et le bc correspont on concatène avec le donnée brute
            dossier_source = dossier_source + str(elm) + parametre
    # on change le curret directory pour se mettre au niveau du donnée brute ou du dossier préparé
    os.chdir(dossier_source)

    # iterer sur les dossier du DB, les dossier sont classé par le numéro du semaine donc il faut parcourir tout ces semaines
    trouve = 0
    dans_elif = 0
    # tester si le paramètre dossier n'est pas vide
    if dossier =="":
        return os.getcwd()
    else:
        print("Le dossier a chercher c'est : ",dossier)
    
    for root, dirs, files in os.walk(dossier_source):
        for dir in dirs:
            if dossier == dir:
                trouve = 1
                dossier_source = os.path.join(root, dir)
                print(dossier_source)
                break
            elif dossier in dir or dossier.replace("0","") == dir:
                if dans_elif == 0: print("Ce pourrait-il que le dossier que vous chercher soit dans l'un des dossier en bas :")
                dans_elif = 1
                print(os.path.join(root, dir))

    if dans_elif : print("Fin de proposision ...")
    print("---------------------------------------")
    if not trouve:
        print(f"Aucun dossier portant exactement le nom : {dossier} n'a été trouvé ...")
    os.chdir(dossier_source)
    return dossier_source


def main(liste,dossier_autre_pour_main):
    initial_dir = os.getcwd()

    if len(liste) == 2 :
        # l'utilisateur n'a pas mis la date et le dossier
        recherche_donnee_brute(liste[0],liste[1],dossier_autre_pour_main)
    elif len(liste) == 3:
        # l'utilisateur a mis le dossier mais pas de date
        recherche_donnee_brute(liste[0],liste[1],dossier_autre_pour_main,liste[2])
    elif len(liste) == 4:
        # l'utilisateur a saisi la date et le dossier
        recherche_donnee_brute(liste[0],liste[1],dossier_autre_pour_main,liste[2],liste[3])
    else:
        main(dossier_autre_pour_main)
    
    os.system(f"start explorer {os.getcwd()}")
    os.chdir(initial_dir)


def Read_Me():
    print(
        """
        ##############################
        # FUTURMAP - DATA            #
        # Rolland M_0359 (c)         #
        # Le 09-01-2025              #
        ##############################

        Version de l'application : V01

        Cette application a été crée dans le but de faciliter
        la recherche de dossier ou de projet dans le serveur(Q:)
        Voici les quelque consigne de base qu'il faut connaitre 
        Pour que ce dernier fonctionne bien :
        1. L'application attend en paramètre 3 mots clé dont :
            PROJET BC DOSSIER
        2. Les mots clé doivent être séparer par des espaces :
            exemple : 13h bc04 1245
        3. Vous pouvez choisir entre donnée brure préparation ou livraison
            => pour cela saisissez 0 ou 1 ou 2 si non ca crache
        4. Evitez d'entrer des valeur bidon
        5. La date par défaut est 2024
        6. Le numéro du dossier est optionnel, tout comme la date
            => vous pouvez faire :
                - 13h bc04
                - 13h bc04 1212
                - 13h bc06 1250 2025
        7. si vous voulez changé la date il faut mettre un numéro de
        dossier aussie comme sur l'éxemple d'en haut.

        BONNE CHANCHE ....
        """
    )
    a = input("\tAppyez sur Entrée pour continuer ...")

if __name__=="__main__":
    os.system("color a")
    os.system("title R_DbFinder ")
    Read_Me()
    os.system("cls")
    parent = pivot[int(input("Choisir entre : \n\t0 - donnée brute \n\t1 - préparé ou \n\t2 - livraison production \n>>> "))]
    mot_clef = input("entrer les mots clé (projet  BC  dossier) séparer par une espace : ").split(" ")
    projet_dossier = list(mot_clef[:2])
    main(mot_clef,parent)
    while True:
        drapeau_continu = input("Voulez vous effectué un autre opération ? Oui/Non (o-n) :")
        if drapeau_continu == "o" or drapeau_continu =="O":
            os.system("cls")
            numero_dossier = str(input("Numéro du dossier : "))
            # créer une liste temporaire pour memoriser le projet et le bc courant 
            # et inserer le nouveau numéro de dossier
            list_temp = list(mot_clef[:2].copy())
            list_temp.append(numero_dossier)
            # fin de création de list temporaire ...........
            main(list_temp,parent)
        elif drapeau_continu=="n" or drapeau_continu =="N":
            print("Fin du programme ...")
            break
        else:
            print("Veuillez entrer une lettre entre 'O' ou 'N'")
    a = input()



