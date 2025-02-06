# coding : "utf-8"
import os
lien_principale = "Q:/GP/2024/"

for root, dirs, _ in os.walk(lien_principale):
    for dir in dirs:
        if "0073" in dir.zfill(4):
            lien = os.path.join(root, dir)
            if "Donnees_Brutes" in lien:
                print(lien)

