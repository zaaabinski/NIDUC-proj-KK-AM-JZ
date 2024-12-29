from ObslugaDanych.OdczytajDane import OdczytDanych
from StartSymulacji import SymulacjaDlaPowielania
from StartSymulacji import SymulacjaDlaBCH
from StartSymulacji import SymulacjaBCHGEliot
from StartSymulacji import SymulacjaDlaPowielaniaGEliot

def print_separator():
    print("-" * 60)

sciezka = "dane2.txt"

odczyt = OdczytDanych(sciezka)
ilosc_bledow_dla_Powielania = 0
ilosc_bledow_dla_Powielania2 = 0
ilosc_bledow_dla_BCH = 0
ilosc_bledow_dla_BCH2 = 0
ilosc_danych = 0

dane_bin = odczyt.odczytaj_dane()

print_separator()
print("SYMULACJA TRANSMISJI DANYCH")
print_separator()

for dane_wejsciowe in dane_bin:
    ilosc_danych += 1
    print(f"\nPakiet danych #{ilosc_danych}: {dane_wejsciowe}")
    print_separator()

    # powielanie
    bledy_powielanie, dane_po_powielaniu, dane_po_bsc_powielanie = SymulacjaDlaPowielania.SymulujPowielanie(dane_wejsciowe)
    ilosc_bledow_dla_Powielania += bledy_powielanie
    print(f"Powielanie - błędy w pakiecie: {bledy_powielanie}")
    print(f"Powielanie - dane po transmisji BSC: {dane_po_bsc_powielanie}")
    print(f"Powielanie - dane po korekcji: {dane_po_powielaniu}")

    #bch
    bledy_BCH, dane_po_bch, dane_po_bsc_bch = SymulacjaDlaBCH.SymulujBCH(dane_wejsciowe)
    ilosc_bledow_dla_BCH += bledy_BCH
    print(f"BCH      - błędy w pakiecie: {bledy_BCH}")
    print(f"BCH      - dane po transmisji BSC: {dane_po_bsc_bch}")
    print(f"BCH      - dane po korekcji: {dane_po_bch}")
    print_separator()


    # powielanie g eliot
    bledy_powielanie2, dane_po_powielaniu2, dane_po_bsc_powielanie2 = SymulacjaDlaPowielaniaGEliot.SymulujPowielanieGEliot(dane_wejsciowe)
    ilosc_bledow_dla_Powielania2 += bledy_powielanie2
    print(f"Powielanie - błędy w pakiecie: {bledy_powielanie2}")
    print(f"Powielanie - dane po transmisji  g eliot : {dane_po_bsc_powielanie2}")
    print(f"Powielanie - dane po korekcji: {dane_po_powielaniu2}")

    #bch g eliot
    bledy_BCH2, dane_po_bch2, dane_po_bsc_bch2 = SymulacjaBCHGEliot.SymulujBCHEliot(dane_wejsciowe)
    ilosc_bledow_dla_BCH2 += bledy_BCH2
    print(f"BCH      - błędy w pakiecie: {bledy_BCH2}")
    print(f"BCH      - dane po transmisji g eliot: {dane_po_bsc_bch2}")
    print(f"BCH      - dane po korekcji: {dane_po_bch2}")
    print_separator()

print("\nPODSUMOWANIE SYMULACJI")
print_separator()
print(f"Liczba przesłanych pakietów danych: {ilosc_danych}")
print_separator()
print("Metoda    | Liczba błędów | Współczynnik błędów")
print("-" * 45)
print(f"Powielanie| {ilosc_bledow_dla_Powielania:^13} | {ilosc_bledow_dla_Powielania/ilosc_danych:.4f}")
print(f"BCH       | {ilosc_bledow_dla_BCH:^13} | {ilosc_bledow_dla_BCH/ilosc_danych:.4f}")

print("\nGilberta Eliota")

print("Metoda    | Liczba błędów | Współczynnik błędów")
print("-" * 45)
print(f"Powielanie| {ilosc_bledow_dla_Powielania2:^13} | {ilosc_bledow_dla_Powielania2/ilosc_danych:.4f}")
print(f"BCH       | {ilosc_bledow_dla_BCH2:^13} | {ilosc_bledow_dla_BCH2/ilosc_danych:.4f}")
print_separator()


