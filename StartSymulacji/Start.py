from ObslugaDanych.OdczytajDane import OdczytDanych
from StartSymulacji import SymulacjaDlaPowielania
from StartSymulacji import SymulacjaDlaBCH
#from StartSymulacji import SymulacjaDlaHamminga

sciezka = "dane.txt"

odczyt = OdczytDanych(sciezka)
ilosc_bledow_dla_Powielania = 0
ilosc_bledow_dla_BCH = 0
ilosc_bledow_dla_LDPC = 0
ilosc_danych = 0

dane_bin = odczyt.odczytaj_dane()

for dane_wejsciowe in dane_bin:
    ilosc_danych+=1
    print(f"Symulacja dla danych: {dane_wejsciowe}")

    #powielanie
    bledy_powielanie = SymulacjaDlaPowielania.SymulujPowielanie(dane_wejsciowe)
    ilosc_bledow_dla_Powielania += bledy_powielanie
    print(f"Liczba błędów dla powielania: {bledy_powielanie}")

    #bch
    bledy_BCH = SymulacjaDlaBCH.SymulujBCH(dane_wejsciowe)
    ilosc_bledow_dla_BCH+=bledy_BCH
    print(f"Liczba błędów dla BCH: {bledy_BCH}")






print(f"Podsumowanie:")
print(f"Liczba błędów dla powielania: {ilosc_bledow_dla_Powielania}")
print(f"Liczba błędów dla BCH: {ilosc_bledow_dla_BCH}")
#print(f"Liczba błędów dla LDPC: {ilosc_bledow_dla_LDPC}")
print(f"Liczba danych wyslanych: {ilosc_danych}")


