import sqlite3
from openpyxl import Workbook
from openpyxl.styles import PatternFill, Font
from datetime import date


def ExportToExcel():
    conn = sqlite3.connect("prices.db")
    cursor = conn.cursor()

    today_date = date.today().strftime("%d.%m.%Y")

    wb = Workbook()
    wb.remove(wb.active)  # smažeme defaultní sheet

    header_fill = PatternFill("solid", fgColor="DDDDDD")
    header_font = Font(bold=True)

    headers = [
        "Datum",
        "Cena",
        "Moje cena"
    ]

    # 1️⃣ Načteme všechny produkty
    cursor.execute("""
        SELECT id, produkt, heureka_url, moje_cena
        FROM urls
    """)
    products = cursor.fetchall()
    for id, produkt, heureka_url, moje_cena in products:
        sheet_name = f"{id} - {produkt[:25] if produkt else 'Produkt'}"
        ws = wb.create_sheet(title=sheet_name)

        ws["A1"] = "Produkt:"
        ws["B1"] = produkt

        ws["A2"] = "Heureka URL:"
        ws["B2"] = heureka_url

        ws["A1"].font = Font(bold=True)
        ws["A2"].font = Font(bold=True)
        # hlavičky
        for col, header in enumerate(headers, start=1):
            cell = ws.cell(row=4, column=col, value=header)
            cell.fill = header_fill
            cell.font = header_font

        # 2️⃣ historie pro konkrétní produkt
        cursor.execute("""
            SELECT date, price
            FROM history
            WHERE product_id = ?
            ORDER BY date
        """, (id,))

        history_rows = cursor.fetchall()

        # data
        for row_idx, (hist_date, price) in enumerate(history_rows, start=4):
            ws.cell(row=row_idx, column=1, value=hist_date)
            ws.cell(row=row_idx, column=2, value=price)
            ws.cell(row=row_idx, column=3, value=moje_cena)

        # automatická šířka sloupců
        for column_cells in ws.columns:
            length = max(len(str(cell.value)) if cell.value else 0 for cell in column_cells)
            ws.column_dimensions[column_cells[0].column_letter].width = length + 2

    wb.save(f"produkty.xlsx")
    conn.close()
ExportToExcel()