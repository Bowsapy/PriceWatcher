import os
import sqlite3

from SendMail import send_price_alert

conn = sqlite3.connect("prices.db")
cursor = conn.cursor()

# DŮLEŽITÉ: povolit foreign keys v SQLite
cursor.execute("PRAGMA foreign_keys = ON;")

# tabulka history s FOREIGN KEY
cursor.execute("SELECT * from urls")
print(cursor.fetchall())


conn = sqlite3.connect("prices.db")
cursor = conn.cursor()

print("Používaný soubor DB:")
print(os.path.abspath("prices.db"))

cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
print("Tabulky v DB:", cursor.fetchall())


conn.commit()
