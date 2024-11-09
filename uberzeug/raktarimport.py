import csv
import sqlite3

from collections import namedtuple
from time import strftime


ADATBAZIS = 'adatok.db'


def adatbazisInicializalasa(adatbazis):
    kapcsolat = sqlite3.connect(adatbazis)
    kapcsolat.execute("""
    CREATE TABLE IF NOT EXISTS raktar(
        cikkszam INTEGER PRIMARY KEY ASC,
        keszlet, 
        megnevezes, 
        gyarto, 
        leiras, 
        megjegyzes, 
        egyseg, 
        egysegar, 
        kiszereles, 
        hely, 
        lejarat, 
        gyartasido,
        szin,
        letrehozas, 
        utolso_modositas
        )""")
    kapcsolat.execute("""
    CREATE TABLE IF NOT EXISTS raktar_naplo(
        azonosito INTEGER PRIMARY KEY ASC, 
        cikkszam INTEGER, 
        megnevezes, 
        egyseg, 
        egysegar, 
        valtozas, 
        datum, 
        projektszam
        )""")
    return kapcsolat


TermekRekord = namedtuple("TermekRekord",
                          ["csoport", "cikkszam", "nev", "egyseg",
                           "nyitomennyiseg", "nyitoertek", "keszlet",
                           "egysegar", "osszesen"])
kapcsolat = adatbazisInicializalasa(ADATBAZIS)
datumbelyeg = strftime("%Y-%m-%d")

with open("keszletkivonat.csv") as keszlet:
    for termek in map(TermekRekord._make, csv.reader(keszlet, delimiter=",")):
        if termek.cikkszam:  # üres sorokat kihagyjuk
            if termek.keszlet:
                keszlet = float(termek.keszlet.replace(",", "."))
            else:
                keszlet = 0
            if termek.egysegar:
                egysegar = int(float(termek.egysegar.replace(",", ".")))
            else:
                egysegar = 0
            kapcsolat.execute("""INSERT INTO raktar(
                keszlet, 
                megnevezes, 
                gyarto, 
                leiras, 
                megjegyzes,
                egyseg, 
                egysegar, 
                kiszereles,
                hely,
                lejarat,
                gyartasido, 
                letrehozas,
                utolso_modositas)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", 
                (keszlet, 
                termek.nev, 
                "", 
                "",
                "", 
                termek.egyseg,
                egysegar,
                "", 
                "", 
                "", 
                "", 
                datumbelyeg,
                datumbelyeg))
            kapcsolat.commit()
            print(termek.nev + " beírva")
