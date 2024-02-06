"""
projekt_3.py: třetí projekt do Engeto Online Python Akademie
author: Jan Tomáš
email: jenda.tomas@seznam.cz
discord: jendatomas
"""

from requests import get
from bs4 import BeautifulSoup as bs
import csv
import sys



def kod_obci(rozdelene_html):
    """
    vyscrapuje kódy jednotlivých obcí
    """
    cisla_obci= rozdelene_html.find_all("td", class_="cislo")
    kody=list()
    for i in cisla_obci:
        kody.append(i.string)
    return kody

def jmena_obci(rozdelene_html): 
    """
    vyscrapuje jmena obci, ale z hlavni stranky
    """
    jmena_obci= rozdelene_html.find_all("td", {"class":"overflow_name"}) 
    obce=list()                                              
    for i in jmena_obci:
        obce.append(i.string)
    return obce

def odkazy_vysledky(rozdelene_html):
    """
    vyscrapuje odkazy na stránky s výsledky voleb v obcích
    """
    vyber_odkazu= rozdelene_html.find_all("td", {"class":"cislo"})
    odkazy= list()
    for i in vyber_odkazu:
        odkaz = i.find_all("a")
        for i in odkaz:
            odkazy.append(i["href"])
    spojeni=list()
    for i in odkazy: 
        spojeni.append("https://volby.cz/pls/ps2017nss/" + i)
    return spojeni

def rozdelene_html_obci(html_odkazy_vysledky):
    """
    nacte a rozdeli html jednotlivych obci
    """
    html_rozdelene_obce= list()
    for odkaz in html_odkazy_vysledky:
        prehled_obec= get(odkaz)
        rozdelena_obec= bs(prehled_obec.text, features="html.parser")
        html_rozdelene_obce.append(rozdelena_obec)
    return html_rozdelene_obce


def volici_seznam(html_rozdelene_obce):
    """
    vyscrapuje z html jednolivých obcí počet voličů v seznamu
    """
    pocet_volicu=list()
    for i in html_rozdelene_obce:
        volici= i.find_all("td", {"class":"cislo", "headers":"sa2"})
        for i in volici:
            pocet_volicu.append(i.string)
    return pocet_volicu


def volici_obalky_hlasy(html_rozdelene_obce):
    """
    vyscrapuje z html jednotlivých obcí 
    počet voličů v seznamu, počet vydaných obálek, počet platných hlasů
    """
    pocet_volicu= list()
    pocet_obalek= list()
    pocet_hlasu_obec= list()
    for i in html_rozdelene_obce:
        volici= i.find_all("td", {"class":"cislo", "headers":"sa2"})
        obalky= i.find_all("td", {"class":"cislo", "headers":"sa3"})
        hlasy= i.find_all("td", {"class":"cislo", "headers":"sa6"})
        for i in volici:
            pocet_volicu.append(i.string)
        for i in obalky:
            pocet_obalek.append(i.string)
        for i in hlasy:
            pocet_hlasu_obec.append(i.string)
    return pocet_hlasu_obec,pocet_obalek,pocet_volicu


def strany_fce(html_strany):
    """
    vyscrapuje názvy stran na seznamu (z 1.obce v seznamu),
    ve všech obcích jsou stejné strany i jejich pořadí
    """
    strany=list()
    strana= html_strany.find_all("td", {"class":"overflow_name"})
    for i in strana:
        strany.append(i.string)
    return strany
        
def strany_hlasy(html_rozdelene_obce):
    """
    vyscrapuje počet hlasů všech stran ve všech obcích
    """
    pocty_hlasu_strany=list()
    for i in html_rozdelene_obce:
        hlasy_1= i.find_all("td",{"class":"cislo", "headers":["t1sa2 t1sb3","t2sa2 t2sb3"]})
        for i in hlasy_1:
            pocty_hlasu_strany.append(i.string)
    return pocty_hlasu_strany

def rozdeleni_vysledky_obci(obce, strany, pocty_hlasu_strany):
    """
    rozdeli hlasy jednotlivým stranám dle obcí
    """
    pocet_obci=len(obce)
    pocet_stran=len(strany)
    hlasy_strany=list(list()for _ in range(pocet_stran))
    index_obce=0
    index_strany=0
    for list_strany in range(pocet_stran):
        for _ in range(pocet_obci):
            hlasy_strany[list_strany].append(pocty_hlasu_strany[(index_strany*pocet_stran)+index_obce])
            index_strany +=1
        index_obce += 1
        index_strany = 0
    return hlasy_strany




adresa= sys.argv[1]
if "ps2017" in adresa:
    pass
else:
    print("URL adresa je zadána chybně")
    sys.exit("ukončuji program")

csv_nazev= sys.argv[2]
if not csv_nazev.endswith(".csv"):
    print("název csv souboru musí končit \".csv\"")
    sys.exit("ukončuji program")

try:
    prehled_okres=get(adresa)
except:
    print("URL adresa nebyla nalezena")
    sys.exit("ukončuji program")
if prehled_okres.status_code==200:
    print("Načítám")
else:
    print("Zadané URL nelze načíst")
    sys.exit("ukončuji program")


rozdelene_html= bs(prehled_okres.text, features="html.parser")
html_odkazy_vysledky= odkazy_vysledky(rozdelene_html)
if len(html_odkazy_vysledky)==0:
    print("Nebylo zadáno URL konkrétního okresu - výběr obce")
    sys.exit("ukončuji program")
else:
    print(f"Stahuji data z vybraneho URL: {adresa}")
kody= kod_obci(rozdelene_html)
obce= jmena_obci(rozdelene_html)
html_rozdelene_obce= rozdelene_html_obci(html_odkazy_vysledky)
volici_pocet_obce= volici_seznam(html_rozdelene_obce)
pocet_hlasu_obec, pocet_obalek, pocet_volicu = volici_obalky_hlasy(html_rozdelene_obce)
html_strany= html_rozdelene_obce[0]
strany= strany_fce(html_strany)
pocty_hlasu_strany = strany_hlasy(html_rozdelene_obce)
rozdelene_hlasy_obce= rozdeleni_vysledky_obci(obce, strany, pocty_hlasu_strany)

hlavicka= ["code", "location","registered","envelopes",
            "valid"]
hlavicka.extend(strany)

data= zip(kody, obce, pocet_volicu, pocet_obalek, pocet_hlasu_obec, *rozdelene_hlasy_obce)


with open(csv_nazev, mode="w", newline="") as nove_csv:
    zapisovac= csv.writer(nove_csv, delimiter=",")
    print(f"Ukladam data do souboru:{csv_nazev}")
    zapisovac.writerow(hlavicka)
    for radky in data:
        zapisovac.writerow(radky)
print("Ukončuji program")