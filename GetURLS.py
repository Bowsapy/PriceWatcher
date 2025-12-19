import sqlite3

# připojení k databázi (souboru)
conn = sqlite3.connect("prices.db")
cursor = conn.cursor()

# vytvoření tabulky pokud ještě neexistuje
cursor.execute("""
CREATE TABLE IF NOT EXISTS urls (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    heureka_url TEXT NOT NULL,
    produkt TEXT,
    moje_cena INTEGER,
    cena_heureka INTEGER
)
""")
conn.commit()
