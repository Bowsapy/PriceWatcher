import sqlite3
import re
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# ---- Připojení k DB ----
conn = sqlite3.connect("prices.db")
cursor = conn.cursor()


# =============================
#   Utility funkce
# =============================

import re


def GetOnlyPriceReg(text):
    match = re.search(r"\d+(?:[ \u00A0]\d+)*", text)
    if not match:
        return None
    return int(match.group().replace(" ", "").replace("\u00A0", ""))


def GetChromeDriver():
    chrome_options = Options()
    chrome_options.headless = True
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.7444.163 Safari/537.36")
    return chrome_options



# =============================
#   Scraper: Heureka
# =============================
def GetNameFromHeureka(url):
    driver = webdriver.Chrome(options=GetChromeDriver())
    cena_heureka = None
    product = None

    try:
        driver.get(url)

        WebDriverWait(driver, 15).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".c-offer__price.u-bold.u-delta"))
        )

        # Název produktu
        product = driver.find_element(
            By.CSS_SELECTOR,
            ".e-heading.c-product-info__name.u-color-grey-700.u-bold.u-gamma"
        ).text


    except Exception as e:
        print("Chyba Heureky:", e)

    cursor.execute("SELECT id FROM urls WHERE heureka_url = ?", (url,))
    row = cursor.fetchone()

    if row:
        # URL existuje → aktualizujeme název produktu
        cursor.execute(
            "UPDATE urls SET produkt = ? WHERE id = ?",
            (product, row[0])
        )
    else:
        # URL neexistuje → vložíme nový řádek
        cursor.execute(
            "INSERT INTO urls (heureka_url, produkt) VALUES (?, ?)",
            (url, product)
        )

    conn.commit()

    return product, cena_heureka


def GetPriceFromHeureka(url):

    driver = webdriver.Chrome(options=GetChromeDriver())
    cena_heureka = None
    product = None

    try:
        driver.get(url)

        WebDriverWait(driver, 15).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".c-offer__price.u-bold.u-delta"))
        )

        # Název produktu
        product = driver.find_element(
            By.CSS_SELECTOR,
            ".e-heading.c-product-info__name.u-color-grey-700.u-bold.u-gamma"
        ).text

        # Nejnižší cena = první nabídka
        price_elem = driver.find_element(By.CSS_SELECTOR, ".c-offer__price.u-bold.u-delta")
        price = price_elem.text.replace("\u00a0", " ")

        cena_heureka = int(GetOnlyPriceReg(price))

    except Exception as e:
        print("Chyba Heureky:", e)

    driver.quit()

    cursor.execute(
        "SELECT id FROM urls WHERE heureka_url = ?", (url,))
    row = cursor.fetchone()
    product_id = row[0] if row else None
    # Uložení do DB
    cursor.execute("""
    INSERT INTO history (product_id, date, price)
    VALUES (?, ?, ?)
    """, (
        product_id,
        datetime.now().isoformat(timespec="seconds"),
        cena_heureka
    ))

    conn.commit()

    return product, cena_heureka






# =============================
#   Hlavní funkce pro celý záznam
# =============================

def UpdatePrices(row_id, medimat_url, heureka_url):
    print("➡ Zpracovávám produkt ID:", row_id)

    produkt2, cena_h = GetPriceFromHeureka(heureka_url, row_id)

    print("OK – hotovo")
