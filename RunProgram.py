import GetURLS
from GetURLS import cursor
from main import *
from WriteToExcel import *



def update_all():
    cursor.execute("SELECT id, moje_cena, heureka_url FROM urls")
    rows = cursor.fetchall()

    print(f"\nNalezeno {len(rows)} záznamů v databázi.")
    print("-------------------------------------")

    for row in rows:
        row_id, moje_cena, heureka_url = row

        print(f"\n➡ Zpracovávám ID {row_id}")
        print(f"   moje cena: {moje_cena}")
        print(f"   Heureka: {heureka_url}")

        try:
            get_price_from_heureka(heureka_url)
            get_name_from_heureka(heureka_url)

            print(f"   ✓ Hotovo — aktualizováno v DB")
        except Exception as e:
            print(f"   ✗ Chyba při zpracování: {e}")

    print("\nVšechny záznamy byly aktualizovány.")
conn.commit()