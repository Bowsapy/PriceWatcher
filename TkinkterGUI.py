import tkinter as tk
from tkinter import messagebox
import sqlite3
from RunProgram import *

# ---- Připojení k databázi ----
conn = sqlite3.connect("urls.db")
cursor = conn.cursor()

# ---- Načtení všech URL z databáze ----
def load_urls():
    cursor.execute("SELECT id, medimat_url, heureka_url FROM urls")
    rows = cursor.fetchall()

    # vrací slovník: {id: (medimat, heureka)}
    return {row[0]: (row[1], row[2]) for row in rows}


urls = load_urls()

# ---- Uložení jedné dvojice URL do databáze ----
def save_url(medimat, heureka):
    cursor.execute(
        "INSERT INTO urls (medimat_url, heureka_url) VALUES (?, ?)",
        (medimat, heureka)
    )
    conn.commit()


# ---- Přidání URL z GUI ----
def add_url():
    medimat = medimat_entry.get().strip()
    heureka = heureka_entry.get().strip()

    if medimat and heureka:
        save_url(medimat, heureka)

        # znovu načíst data
        global urls
        urls = load_urls()

        messagebox.showinfo("Uloženo", "URL byly uloženy!")

        medimat_entry.delete(0, tk.END)
        heureka_entry.delete(0, tk.END)
        update_list()
    else:
        messagebox.showwarning("Chyba", "Vyplňte obě pole!")


# ---- Aktualizace ListBoxu ----
def update_list():
    listbox.delete(0, tk.END)
    for _id, (med, heu) in urls.items():
        listbox.insert(tk.END, f"{med}  →  {heu}")


# ---- GUI ----
root = tk.Tk()
root.title("URL Manager")

tk.Label(root, text="Medimat URL").grid(row=0, column=0)
tk.Label(root, text="Heureka URL").grid(row=1, column=0)

medimat_entry = tk.Entry(root, width=80)
medimat_entry.grid(row=0, column=1)

heureka_entry = tk.Entry(root, width=80)
heureka_entry.grid(row=1, column=1)

tk.Button(root, text="Přidat URL", command=add_url).grid(row=2, column=1, pady=5)
tk.Button(root, text="Spustit srovnání", command=UpdateAll).grid(row=2, column=2, pady=1)
tk.Button(root, text="Smazat produkt podle ID", command=UpdateAll).grid(row=2, column=3, pady=1)

listbox = tk.Listbox(root, width=120)
listbox.grid(row=3, column=0, columnspan=2)

update_list()
root.mainloop()

# ukončení spojení
conn.close()
