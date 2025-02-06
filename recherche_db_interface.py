# coding : "UTF-8"
import customtkinter as ctk
import os

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

root = ctk.CTk()
root.geometry("400x300")
root.title("RECHERCHE DONNEE BRUTE")

try:
    file_list = os.listdir()
except Exception as e:
    file_list = []
    print(f"Erreur lors de la lecture du répertoire: {e}")

file_list_str = "\n".join(file_list)

textbox = ctk.CTkTextbox(
    master=root,
    width=120,
    height=150,
)
textbox.insert("1.0", file_list_str)
textbox.pack()
root.mainloop()
