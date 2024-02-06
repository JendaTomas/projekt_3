# Engeto-3-projekt
Třetí projekt na Python Akademii od Engeta
## Popis projektu
Tento projekt slouží k extrahování výsledků parlamentních voleb v roce 2017 z přehledu obcí v jednotlivých okresech.
## Instalace knihoven
Knihovny, které jsou použity v kódu naleznete uložené v souboru *requirements.txt*. Pro instalaci doporučuji použít nové virtuální prostředí a s nainstalovaným manažerem spustit následovně:
```bash
pip3 --version                      # overim verzi manazeru
pip3 install -r requirements.txt    # maistalujeme knihovny
```
## Spuštění projektu
Spuštění souboru *projekt_3.py* v rámci příkazového řádku vyžaduje dva povinné argumenty.
```bash
python projekt_3.py <odkaz-uzemniho-celku> <vysledny-soubor>
```
Po zadání tohoto příkazu se následně stáhnou výsledky jako soubor s příponou *.csv*
## Ukázka projektu
Výsledky hlasování pro okres Jičín:
1. argument: *https://volby.cz/pls/ps2017/ps32?xjazyk=CZ&xkraj=8&xnumnuts=5202*
    - je nutné zadat přesnou URL adresu ze stránky konkrétního okresu - výběr obce
2. argument: *okres_jicin.csv*
    - je nutné zadat s koncovkou *.csv*

Spouštění programu:
```bash
python projekt_3.py "https://volby.cz/pls/ps2017/ps32?xjazyk=CZ&xkraj=8&xnumnuts=5202" "okres_jicin.csv"
```
Průběh stahování:
```bash
Načítám
Stahuji data z vybraneho URL: https://volby.cz/pls/ps2017/ps32?xjazyk=CZ&xkraj=8&xnumnuts=5202
Ukladam data do souboru:okres_jicin.csv
Ukončuji program
```
Částečný výstup
```bash
code,location,registered,envelopes,valid,Občanská demokratická strana,...
553701,Bačalky,133,98,97,12,...
572675,Běchary,230,98,96,4,...
...
```
