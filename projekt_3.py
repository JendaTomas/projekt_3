"""
projekt_3.py: třetí projekt do Engeto Online Python Akademie
author: Jan Tomáš
email: jenda.tomas@seznam.cz
discord: jendatomas
"""

import requests
from bs4 import BeautifulSoup as bs
import csv
import sys


def find_code(parsered_html):
    """
    find the codes of individual municipalities
    """
    number_municipalities = parsered_html.find_all("td", class_="cislo")
    codes = list()
    for number in number_municipalities:
        codes.append(number.string)
    return codes


def find_names(parsered_html):
    """
    find the name of the village, but from the main page
    """
    names_village = parsered_html.find_all("td", {"class": "overflow_name"})
    municipalite = list()
    for name in names_village:
        municipalite.append(name.string)
    return municipalite


def find_link_results(parsered_html):
    """
    find links to pages with municipal election results
    """
    td_with_link = parsered_html.find_all("td", {"class": "cislo"})
    incomplete_links = list()
    for td_tag in td_with_link:
        a_tags = td_tag.find_all("a")
        for a_tag in a_tags:
            incomplete_links.append(a_tag["href"])
    links = list()
    for link in incomplete_links: 
        links.append("https://volby.cz/pls/ps2017nss/" + link)
    return links


def parsering_html_municipalites(html_links_resultes):
    """
    load and parser html of municipalites
    """
    html_parser_municipalites = list()
    for link in html_links_resultes:
        html_municipalites = requests.get(link)
        parser_municipalites = bs(html_municipalites.text, features="html.parser")
        html_parser_municipalites.append(parser_municipalites)
    return html_parser_municipalites


def find_electorates_envelopes_votes(html_parser_municipalites):
    """
    from html of municipalites find number of electorates, envelopes and votes 
    """
    number_electorates = list()
    number_envelopes = list()
    number_votes_municipalite = list()
    for tag in html_parser_municipalites:
        electorates = tag.find_all("td", {"class": "cislo", "headers": "sa2"})
        envelopes = tag.find_all("td", {"class": "cislo", "headers": "sa3"})
        votes = tag.find_all("td", {"class": "cislo", "headers": "sa6"})
        for character in electorates:
            number_electorates.append(character.string)
        for character in envelopes:
            number_envelopes.append(character.string)
        for character in votes:
            number_votes_municipalite.append(character.string)
    return number_votes_municipalite, number_envelopes, number_electorates


def find_political_party(html_parties):
    """
    find names of political parties (from 1st municipalite in the list),
    (in the all municipalites are some politicat parties and their order)
    """
    political_parties = list()
    polit_party = html_parties.find_all("td", {"class": "overflow_name"})
    for character in polit_party:
        political_parties.append(character.string)
    return political_parties
        

def find_numbers_political_parties(html_parser_municipalites):
    """ 
    finds the number of votes of all parties in all municipalities
    """
    numbers_votes_parties = list()
    for tag in html_parser_municipalites:
        td_tags = tag.find_all("td", {"class": "cislo", "headers": ["t1sa2 t1sb3", "t2sa2 t2sb3"]})
        for character in td_tags:
            numbers_votes_parties.append(character.string)
    return numbers_votes_parties


def parsering_html_results(municipalite, political_parties, numbers_votes_parties):
    """
    adds votes to parties by municipality 
    """
    number_municipalities = len(municipalite)
    number_parties = len(political_parties)
    votes_party = list(list()for _ in range(number_parties))
    index_municipality = 0
    index_party = 0
    for list_party in range(number_parties):
        for _ in range(number_municipalities):
            votes_party[list_party].append(numbers_votes_parties[(index_party*number_parties)+index_municipality])
            index_party += 1
        index_municipality += 1
        index_party = 0
    return votes_party
    

def check_url(url_address):
    """
    checks that the URL entered is correct
    """
    if "ps2017" in url_address:
        pass
    else:
        sys.exit("URL adresa je zadána chybně \nukončuji program")
    try:
        url_district = requests.get(url_address)
    except:
        sys.exit("URL adresa nebyla nalezena\nukončuji program")
    if url_district.status_code == 200:
        print("Načítám")
    else:
        sys.exit("Zadané URL nelze načíst\nukončuji program")
    return url_district


def check_csv_suffix(csv_name):
    """
    checks if the csv_name has a .csv suffix
    """
    if not csv_name.endswith(".csv"):
        sys.exit("název csv souboru musí končit \".csv\"\nukončuji program")


def check_url_district(html_links_resultes):
    """
    checks if the link is link of district
    """
    if len(html_links_resultes) == 0:
        sys.exit("Nebylo zadáno URL konkrétního okresu - výběr obce\nukončuji program")
    else:
        print(f"Stahuji data z vybraneho URL: {url_address}")


def create_csv_file(political_parties):
    """
    creats csv file with head and results
    """
    head = ["code", "location", "registered", "envelopes",
            "valid"]
    head.extend(political_parties)
    with open(csv_name, mode="w", newline="") as new_csv:
        write_down = csv.writer(new_csv, delimiter=",")
        print(f"Ukladam data do souboru:{csv_name}")
        write_down.writerow(head)
        for lines in data:
            write_down.writerow(lines)
    return new_csv


url_address = sys.argv[1]
url_district = check_url(url_address)

csv_name = sys.argv[2]
check_csv_suffix(csv_name)

parsered_html = bs(url_district.text, features="html.parser")
html_links_resultes = find_link_results(parsered_html)
check_url_district(html_links_resultes)

codes = find_code(parsered_html)
municipalite = find_names(parsered_html)
html_parser_municipalites = parsering_html_municipalites(html_links_resultes)
number_votes_municipalite, number_envelopes, number_electorates = find_electorates_envelopes_votes(
    html_parser_municipalites)
html_parties = html_parser_municipalites[0]
political_parties = find_political_party(html_parties)
numbers_votes_parties = find_numbers_political_parties(html_parser_municipalites)
parsered_votes_municipalites = parsering_html_results(municipalite, political_parties, numbers_votes_parties)


data = zip(codes, municipalite, number_electorates, number_envelopes, number_votes_municipalite,
           *parsered_votes_municipalites)

create_csv_file(political_parties)
