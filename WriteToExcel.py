import sqlite3
from openpyxl import Workbook
from openpyxl.styles import PatternFill

def ExportToExcel():
    conn = sqlite3.connect("prices.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, produkt, heureka_url, cena_heureka, moje_cena FROM urls"
    )
    rows = cursor.fetchall()

    wb = Workbook()
    wb.remove(wb.active)  # smaže defaultní list

    sheet_number = 1

    for row in rows:
        id_, produkt, heureka_url, cena_heureka, moje_cena = row

        ws = wb.create_sheet(title=str(sheet_number))

        # Hlavička
        ws.append(["Pole", "Hodnota"])
        ws.append(["ID", id_])
        ws.append(["Produkt", produkt])
        ws.append(["Heureka URL", heureka_url])
        ws.append(["Cena Heureka (Kč)", cena_heureka])
        ws.append(["Moje cena", moje_cena])

        # Zvýraznění – moje cena > Heureka
        if moje_cena and cena_heureka and moje_cena > cena_heureka:
            ws["B6"].fill = PatternFill("solid", fgColor="FF9999")

        sheet_number += 1

    wb.save("produkty.xlsx")
    conn.close()

    print("Hotovo – listy jsou pojmenované 1, 2, 3, …")
