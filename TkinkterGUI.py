import datetime as dt
import email
import tkinter as tk
from tkinter import messagebox
import sqlite3
from RunProgram import UpdateAll
from SendMail import send_price_alert
from WriteToExcel import ExportToExcel
import os
from openpyxl.chart import LineChart, Reference
import re
from CalculateStats import *
from CalculateStats import FindOutIfPriceIsLower
def is_valid_heureka_url(url: str) -> bool:
    heureka_regex = re.compile(
        r"^https://[a-z0-9\-]+\.heureka\.cz/[a-z0-9\-]+/#prehled/(?:\?.*)?$",
        re.IGNORECASE)

    return bool(heureka_regex.match(url))
def is_valid_email(email: str) -> bool:
    EMAIL_REGEX = re.compile(
        r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
    )
    return bool(EMAIL_REGEX.match(email))

# ---- Připojení k databázi ----

conn = sqlite3.connect("prices.db")
cursor = conn.cursor()
# ---- Načtení všech URL z databáze ----
def change_send_bool_label():
    if (get_send_bool()==1):
        send_bool_label.config(text = "Zasílat")
    else:
        send_bool_label.config(text = "Nezasílat")


def save_user_email():
    cursor.execute("SELECT * FROM USER_WITH_EMAIL")
    users = cursor.fetchone()  # vezme první řádek, nebo None pokud nic není

    if users:  # pokud už je alespoň jeden řádek
        pass
    else:
            email = email_entry.get().strip()
            if is_valid_email(email):

                cursor.execute("INSERT INTO USER_WITH_EMAIL (email, send_bool) VALUES (?,?)", (email,0))
                conn.commit()  # nezapomeň uložit změny
                email_label.config(text=email)
            else:
                pass

def get_user_email():
    cursor.execute("SELECT email FROM USER_WITH_EMAIL")
    email = cursor.fetchone()
    if email:
        return email[0]
    else:
        return ""

def get_send_bool():
    cursor.execute("SELECT send_bool FROM USER_WITH_EMAIL")
    row = cursor.fetchone()

    if row is not None:
        return row[0]
    else:
        return False


def change_email_label():
    email_label.config(text=get_user_email())
    change_send_bool_label()

def load_urls():
    cursor.execute("SELECT id, moje_cena, heureka_url, cena_heureka FROM urls")
    rows = cursor.fetchall()

    # vrací slovník: {id: (medimat, heureka)}
    return {row[0]: (row[1], row[2]) for row in rows}

def update_and_write():
    UpdateAll()
    CalculateAvgPrice()
    CalculateMinPrice()
    CalculateMaxPrice()
    CalculateActPrice()
    FindOutIfPriceIsLower()


    check_()


urls = load_urls()

def deleteEmail():
    cursor.execute("DELETE FROM USER_WITH_EMAIL")
    email_label.config(text="")
    conn.commit()

def delete():
    cursor.execute("DELETE FROM urls")
    cursor.execute("DELETE FROM history")
    cursor.execute("DELETE FROM statistics")
    os.remove("produkty.xlsx")
    conn.commit()
# ---- Uložení jedné dvojice URL do databáze ----
#delete()
def save_url(price, heureka):
    price = int(price)

    cursor.execute(
        "INSERT INTO urls (heureka_url,moje_cena) VALUES (?, ?)",
        (heureka, price)
    )
    cursor.execute("""
        INSERT INTO STATISTICS (product_id)
        SELECT id
        FROM urls
    """)
    conn.commit()

    now = dt.datetime.now().isoformat(timespec="seconds")

    conn.commit()
def url_exists(heureka_url):
    cursor.execute(
        "SELECT 1 FROM urls WHERE heureka_url = ? LIMIT 1",
        (heureka_url,)
    )
    return cursor.fetchone() is not None


# ---- Přidání URL z GUI ----
def add_url():
    price = price_entry.get().strip()
    heureka = heureka_entry.get().strip()

    if not price or not heureka:
        messagebox.showwarning("Chyba", "Vyplňte obě pole!")
        return

    if is_valid_heureka_url(heureka):
        pass
    else:
        messagebox.showwarning("Neplatný odkaz")
        return
    if url_exists(heureka):
        messagebox.showwarning(
            "Duplicitní odkaz",
            "Tento Heureka odkaz už je v databázi!"
        )
        return

    save_url(price, heureka)


    global urls
    urls = load_urls()

    messagebox.showinfo("Uloženo", "URL byly uloženy!")

    price_entry.delete(0, tk.END)
    heureka_entry.delete(0, tk.END)
    update_list()


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

def notify_user(message):
    messagebox.showwarning(message)
def check_():
    if ExportToExcel():
        notify_user("OK")
    else:
        notify_user("Chyba")
    cursor.execute("SELECT send_bool FROM USER_WITH_EMAIL")
    send_bool = cursor.fetchone()[0]
    if send_bool == 1:
        prods = check_if_price_is_lower()
        email = get_user_email()
        if email:
            print("fsa")
            for prod in prods:
                send_price_alert(email,str(prod[0]),str(prod[3]),str(prod[1]),str(prod[2]))
def check_if_price_is_lower():
    cursor.execute("""
    SELECT produkt, moje_cena, heureka_url, act_price FROM STATISTICS
    join URLS ON URLS.id = statistics.product_id
    WHERE price_is_lower = 1
    """)
    prods = cursor.fetchall()
    return prods
def change_send_bool():
    cursor.execute("""SELECT send_bool from USER_WITH_EMAIL""")
    email = cursor.fetchone()
    if email is not None:
        send_bool = email[0]
        print(send_bool)

        if send_bool == 1:
            send_bool = 0
        else:
            send_bool = 1
        cursor.execute("""UPDATE USER_WITH_EMAIL set send_bool = ?""",(send_bool,))
        conn.commit()
        change_send_bool_label()

# ---- GUI ----
root = tk.Tk()
root.title("URL Manager")

tk.Label(root, text="Moje cena").grid(row=0, column=0)
tk.Label(root, text="Heureka URL").grid(row=1, column=0)

price_entry = tk.Entry(root, width=80)
price_entry.grid(row=0, column=1)

heureka_entry = tk.Entry(root, width=80)
heureka_entry.grid(row=1, column=1)

tk.Button(root, text="Přidat URL", command=add_url).grid(row=2, column=1, pady=1)
tk.Button(root, text="Spustit srovnání", command=update_and_write).grid(row=2, column=2, pady=1)
tk.Button(root, text="Smazat vše", command=delete).grid(row=2, column=3, pady=1)
tk.Button(root, text="Přidat Email", command=save_user_email).grid(row=3, column=3, pady=1)
tk.Button(root, text="Smazat Email", command=deleteEmail).grid(row=3, column=4, pady=1)
tk.Button(root, text = "Zasílat email", command=change_send_bool).grid(row=2, column=4, pady=1)
email_label = tk.Label(root, text="E-mail: ")
email_label.grid(row=4, column=1)
send_bool_label = tk.Label(root,text ="Nezasílat mail")
send_bool_label.grid(row=5, column=1)


email_entry = tk.Entry(root, width=20)
email_entry.grid(row=3, column=2)

listbox = tk.Listbox(root, width=120)
listbox.grid(row=3, column=0, columnspan=2)

change_email_label()
update_list()
root.mainloop()
# ukončení spojení
conn.close()
