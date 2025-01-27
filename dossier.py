# coding : "UTF-8"
from tkinter import *
from tkinter import ttk
import os



root = Tk()
root.title("RDB_Finder")
root.iconbitmap("logo.ico")

trv = ttk.Treeview(root)

# Definir les columns du treeview :
trv["columns"] = ("Dossier")
#configurer les columns :
trv.column("#0",width=35)
trv.column("Dossier", anchor=W, minwidth=25)
# création de l'êntete :
trv.heading("#0",text="Label")
trv.heading("Dossier",text="Dossier")

trv.pack()


dates = ['2024','2025']
list_projet = []
lien_projet = []
for date in dates:
    dossier_source = f"Q:/GP/{str(date)}/"
    liste = os.listdir(dossier_source)

print(liste)
i = 0
for elm in list_projet:
    trv.insert(parent="",index='end',iid=i,text="prnt",values=(elm))
    i += 1


root.mainloop()