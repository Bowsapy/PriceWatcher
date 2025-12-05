import GetURLS
from GetURLS import cursor
from main import *

urls = cursor.fetchall()
for medi, heu in urls:
    if 1 == 1:
        print(GetPriceFromEshopMedimat(medi)["Produkt"])
        print(GetPriceFromEshopMedimat(medi)["Cena"])
        print (GetPriceFromHeureka(heu)[0]["Cena"])
