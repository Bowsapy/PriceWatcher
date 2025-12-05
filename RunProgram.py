import GetURLS
from GetURLS import cursor
from main import *




def UpdateAll():
    cursor.execute("SELECT id, medimat_url, heureka_url FROM urls")
    rows = cursor.fetchall()

    print(f"\nNalezeno {len(rows)} záznamů v databázi.")
    print("-------------------------------------")

    for row in rows:
        row_id, medimat_url, heureka_url = row

        print(f"\n➡ Zpracovávám ID {row_id}")
        print(f"   Medimat: {medimat_url}")
        print(f"   Heureka: {heureka_url}")

        try:
            GetPriceFromEshopMedimat(medimat_url, row_id)
            GetPriceFromHeureka(heureka_url, row_id)

            print(f"   ✓ Hotovo — aktualizováno v DB")
        except Exception as e:
            print(f"   ✗ Chyba při zpracování: {e}")

    print("\nVšechny záznamy byly aktualizovány.")




