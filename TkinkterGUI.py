import tkinter as tk
from tkinter import messagebox
import sqlite3

# Připojení k SQLite databázi
conn = sqlite3.connect("urls.db")
cursor = conn.cursor()

# Vytvoření tabulky pokud neexistuje
cursor.execute("""
CREATE TABLE IF NOT EXISTS urls (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    medimat_url TEXT NOT NULL,
    heureka_url TEXT NOT NULL
)
""")
conn.commit()

# Funkce pro načtení všech URL z DB
def load_urls():
    cursor.execute("SELECT medimat_url, heureka_url FROM urls")
    return cursor.fetchall()

# Funkce pro přidání nové URL do DB
def add_url_to_db(medimat_url, heureka_url):
    cursor.execute("INSERT INTO urls (medimat_url, heureka_url) VALUES (?, ?)",
                   (medimat_url, heureka_url))
    conn.commit()

# Funkce pro tlačítko "Přidat URL"
def add_url():
    medimat = medimat_entry.get().strip()
    heureka = heureka_entry.get().strip()
    if medimat and heureka:
        add_url_to_db(medimat, heureka)
        messagebox.showinfo("Uloženo", "URL byly uloženy do databáze!")
        medimat_entry.delete(0, tk.END)
        heureka_entry.delete(0, tk.END)
        update_list()
    else:
        messagebox.showwarning("Chyba", "Vyplňte obě pole!")

# Funkce pro aktualizaci Listboxu
def update_list():
    listbox.delete(0, tk.END)
    for med, heu in load_urls():
        listbox.insert(tk.END, f"{med} → {heu}")

# --- GUI ---
root = tk.Tk()
root.title("URL Manager")

tk.Label(root, text="Medimat URL").grid(row=0, column=0)
tk.Label(root, text="Heureka URL").grid(row=1, column=0)

medimat_entry = tk.Entry(root, width=80)
medimat_entry.grid(row=0, column=1)

heureka_entry = tk.Entry(root, width=80)
heureka_entry.grid(row=1, column=1)

tk.Button(root, text="Přidat URL", command=add_url).grid(row=2, column=1, pady=5)

listbox = tk.Listbox(root, width=120)
listbox.grid(row=3, column=0, columnspan=2)

update_list()
root.mainloop()
