# docind : "UTF-8"
def Read_Me():
    print(
        """
        ##############################
        # FUTURMAP - DATA            #
        # Rolland M_0359 (c)         #
        # Le 09-01-2025              #
        ##############################

        Version de l'application : V02.5 Beta

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
