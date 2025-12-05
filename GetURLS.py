import sqlite3

# připojení k databázi (souboru)
conn = sqlite3.connect("urls.db")
cursor = conn.cursor()

# vytvoření tabulky pokud ještě neexistuje
cursor.execute("""
CREATE TABLE IF NOT EXISTS urls (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    medimat_url TEXT NOT NULL,
    heureka_url TEXT NOT NULL,
    produkt TEXT,
    cena_medimat INTEGER,
    cena_heureka INTEGER
)
""")
conn.commit()
