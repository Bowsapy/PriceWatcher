import sqlite3
from openpyxl import Workbook
from openpyxl.formatting.rule import CellIsRule
from openpyxl.styles import PatternFill

def ExportToExcel():
    conn = sqlite3.connect("urls.db")
    cursor = conn.cursor()

    cursor.execute("SELECT id, medimat_url, heureka_url, produkt, cena_medimat, cena_heureka FROM urls")
    rows = cursor.fetchall()

    wb = Workbook()
    ws = wb.active
    ws.title = "Ceny"

    # záhlaví
    ws.append([
        "ID",
        "Medimat URL",
        "Heureka URL",
        "Produkt",
        "Cena Medimat (Kč)",
        "Cena Heureka (Kč)"
    ])

    # data
    for row in rows:
        ws.append(row)

    # ================================
    # 🔥 PODMÍNĚNÉ FORMÁTOVÁNÍ
    # ================================

    # Červené pozadí
    red_fill = PatternFill(start_color="FF9999", end_color="FF9999", fill_type="solid")

    # Svítí červeně, když Medimat > Heureka
    ws.conditional_formatting.add(
        "E2:E999",
        CellIsRule(operator="greaterThan", formula=["F2"], fill=red_fill)
    )

    # ================================

    wb.save("urls.xlsx")
    print("Hotovo: jen buňky Medimatu jsou červené, když jsou dražší než Heureka.")

    conn.close()


if __name__ == "__main__":
    ExportToExcel()
