from ObslugaDanych.OdczytajDane import OdczytDanych
from StartSymulacji import SymulacjaDlaPowielania
from StartSymulacji import SymulacjaDlaBCH
#from StartSymulacji import SymulacjaDlaHamminga

def print_separator():
    print("-" * 60)

sciezka = "dane2.txt"

odczyt = OdczytDanych(sciezka)
ilosc_bledow_dla_Powielania = 0
ilosc_bledow_dla_BCH = 0
ilosc_bledow_dla_LDPC = 0
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

print("\nPODSUMOWANIE SYMULACJI")
print_separator()
print(f"Liczba przesłanych pakietów danych: {ilosc_danych}")
print_separator()
print("Metoda    | Liczba błędów | Współczynnik błędów")
print("-" * 45)
print(f"Powielanie| {ilosc_bledow_dla_Powielania:^13} | {ilosc_bledow_dla_Powielania/ilosc_danych:.4f}")
print(f"BCH       | {ilosc_bledow_dla_BCH:^13} | {ilosc_bledow_dla_BCH/ilosc_danych:.4f}")
#print(f"LDPC      | {ilosc_bledow_dla_LDPC:^13} | {ilosc_bledow_dla_LDPC/ilosc_danych:.4f}")
print_separator()


