import sqlite3
import re
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

def GetOnlyPriceReg(text):
    number = re.search(r"\d+", text).group()
    return number


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

def GetPriceFromHeureka(url, row_id):

    driver = webdriver.Chrome(options=GetChromeDriver())
    cena_heureka = None
    produkt = None

    try:
        driver.get(url)

        WebDriverWait(driver, 15).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".c-offer__price.u-bold.u-delta"))
        )

        # Název produktu
        produkt = driver.find_element(
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

    # Uložení do DB
    cursor.execute(
        "UPDATE urls SET produkt = ?, cena_heureka = ? WHERE id = ?",
        (produkt, cena_heureka, row_id)
    )
    conn.commit()

    return produkt, cena_heureka






# =============================
#   Hlavní funkce pro celý záznam
# =============================

def UpdatePrices(row_id, medimat_url, heureka_url):
    print("➡ Zpracovávám produkt ID:", row_id)

    produkt2, cena_h = GetPriceFromHeureka(heureka_url, row_id)

    print("OK – hotovo")
