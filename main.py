from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from makeExcel import *

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--window-size=1920,1080")
chrome_options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.7444.163 Safari/537.36")

driver = webdriver.Chrome(options=chrome_options)

urls = ["https://pripravky-na-inkontinenci.heureka.cz/tena-lady-slim-ultra-mini-plus-50-42-ks-211482/#prehled/?sort-filter=lowest_price"]
data = []  # sem budeme ukládat výsledky

for url in urls:
    driver.get(url)
    try:
        WebDriverWait(driver, 15).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".c-offer__price.u-bold.u-delta"))
        )
        name = driver.find_element(
            By.CSS_SELECTOR,
            ".e-heading.c-product-info__name.u-color-grey-700.u-bold.u-gamma"
        ).text

        price_elements = driver.find_elements(By.CSS_SELECTOR, ".c-offer__price.u-bold.u-delta")
        logo_elements = driver.find_elements(By.CSS_SELECTOR, "img.c-offer__shop-logo.e-image-with-fallback")

        for price_elem, logo_elem in zip(price_elements, logo_elements):
            price = price_elem.text.replace("\u00a0", " ")
            logo_url = logo_elem.get_attribute("src")
            data.append({"Produkt": name, "Cena": price, "Logo": logo_url})
            print(f"{name} | Cena: {price} | Logo URL: {logo_url}")

    except Exception as e:
        print("Nepodařilo se najít ceny nebo loga:", e)

driver.quit()
WriteToExcel(data, "s")
