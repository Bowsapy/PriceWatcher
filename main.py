from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re




def GetOnlyPriceReg(text):
    number = re.search(r"\d+", text).group()
    return number

def GetChromeDriver():
    options = Options()
    options.headless = True
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.7444.163 Safari/537.36")
    return options

def GetPriceFromHeureka():
    price_index = 0
    driver = webdriver.Chrome(options=GetChromeDriver())

    urls = ["https://pripravky-na-inkontinenci.heureka.cz/tena-lady-normal-24-ks/#prehled/?sort-filter=lowest_price"]
    data = []  # sem budeme ukládat výsledky

    driver.get(urls[0])
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
            if price_index == 3:
                break
            price_index = price_index + 1
            price = price_elem.text.replace("\u00a0", " ")
            logo_url = logo_elem.get_attribute("src")
            data.append({"Produkt": name, "Cena": int(GetOnlyPriceReg(price)), "Logo": logo_url})

    except Exception as e:
        print("Nepodařilo se najít ceny nebo loga:", e)

    driver.quit()
    return data

def GetPriceFromEshopMedimat():
    driver = webdriver.Chrome(options=GetChromeDriver())

    url = "https://eshop.medimat.cz/vlozky-tena-lady-normal-24-ks/"
    data = []

    driver.get(url)
    try:
        # počkej, až se objeví element s názvem a cenou
        WebDriverWait(driver, 15).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "div.col-xs-5.h4"))
        )

        # název produktu
        name = driver.find_element(By.CSS_SELECTOR, ".mt0").text

        # první cena
        price_elem = driver.find_element(By.CSS_SELECTOR, "div.col-xs-5.h4")
        price = price_elem.text

        data.append({"Produkt": str(name), "Cena": int(GetOnlyPriceReg(price))})

    except Exception as e:
        print("Nepodařilo se najít cenu:", e)

    driver.quit()
    return data[0]



if(GetPriceFromEshopMedimat()["Cena"]) > (GetPriceFromHeureka()[0]["Cena"]):
    print("Kurva")