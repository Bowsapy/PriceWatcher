import tkinter as tk
from tkinter import messagebox
import sqlite3
from RunProgram import *
from WriteToExcel import ExportToExcel

# ---- Připojení k databázi ----
conn = sqlite3.connect("prices.db")
cursor = conn.cursor()
ExportToExcel()
# ---- Načtení všech URL z databáze ----
def load_urls():
    cursor.execute("SELECT id, moje_cena, heureka_url, cena_heureka FROM urls")
    rows = cursor.fetchall()

    # vrací slovník: {id: (medimat, heureka)}
    return {row[0]: (row[1], row[2]) for row in rows}


urls = load_urls()

# ---- Uložení jedné dvojice URL do databáze ----
def save_url(price, heureka):
    cursor.execute(
        "INSERT INTO urls (moje_cena, heureka_url) VALUES (?, ?)",
        (price, heureka)
    )
    conn.commit()


# ---- Přidání URL z GUI ----
def add_url():
    price = price_entry.get().strip()
    heureka = heureka_entry.get().strip()

    if price and heureka:
        save_url(price, heureka)

        # znovu načíst data
        global urls
        urls = load_urls()

        messagebox.showinfo("Uloženo", "URL byly uloženy!")

        price_entry.delete(0, tk.END)
        heureka_entry.delete(0, tk.END)
        update_list()
    else:
        messagebox.showwarning("Chyba", "Vyplňte obě pole!")


# ---- Aktualizace ListBoxu ----
def update_list():
    listbox.delete(0, tk.END)
    for _id, (med, heu) in urls.items():
        listbox.insert(tk.END, f"{med}  →  {heu}")

def delete_product():
    row_id = 4
    cursor.execute("DELETE FROM urls WHERE id = ?", (row_id,))
    conn.commit()
    conn.commit()  # potvrzení změn


# ---- GUI ----
root = tk.Tk()
root.title("URL Manager")

tk.Label(root, text="Moje cena").grid(row=0, column=0)
tk.Label(root, text="Heureka URL").grid(row=1, column=0)

price_entry = tk.Entry(root, width=80)
price_entry.grid(row=0, column=1)

heureka_entry = tk.Entry(root, width=80)
heureka_entry.grid(row=1, column=1)

tk.Button(root, text="Přidat URL", command=add_url).grid(row=2, column=1, pady=5)
tk.Button(root, text="Spustit srovnání", command=UpdateAll).grid(row=2, column=2, pady=1)
tk.Button(root, text="Smazat produkt podle ID", command=delete_product).grid(row=2, column=3, pady=1)

listbox = tk.Listbox(root, width=120)
listbox.grid(row=3, column=0, columnspan=2)

update_list()
root.mainloop()

# ukončení spojení
conn.close()
