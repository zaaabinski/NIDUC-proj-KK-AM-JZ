from Kody.PowielanieBitow import PowielanieBitow
from ObslugaDanych.LiczenieBledow import zlicz_bledyPowielanie
from Przesyl.BSC import KanalBSC

def SymulujPowielanie(dane_wejsciowe):
    kanal_bsc = KanalBSC(prawd_bledu=0.1)
    powielanie = PowielanieBitow(liczba_powtorzen=3)

    # Zakodowanie danych
    zakodowane = powielanie.koduj(dane_wejsciowe)

    # Przesłanie danych przez kanał BSC
    dane_po_kanale = kanal_bsc.transmituj(zakodowane)

    # Odkodowanie danych
    odkodowane_dane = powielanie.dekoduj(dane_po_kanale)

    # Obliczenie liczby błędów
    bledy = zlicz_bledyPowielanie(dane_wejsciowe, odkodowane_dane)
    return bledy
