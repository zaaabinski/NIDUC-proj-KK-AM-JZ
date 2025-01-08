from Kody.PowielanieBitow import PowielanieBitow
from ObslugaDanych.LiczenieBledow import zlicz_bledyPowielanie
from Przesyl.BSC import KanalBSC

def SymulujPowielanie(dane_wejsciowe, error_prob=0.1, repetitions=3):
    kanal_bsc = KanalBSC(prawd_bledu=error_prob)
    powielanie = PowielanieBitow(liczba_powtorzen=repetitions)

    # Zakodowanie danych
    zakodowane = powielanie.koduj(dane_wejsciowe)

    # Przesłanie danych przez kanał BSC
    dane_po_kanale = kanal_bsc.transmituj(zakodowane)

    # Odkodowanie danych
    odkodowane_dane = powielanie.dekoduj(dane_po_kanale)

    # Obliczenie liczby błędów
    bledy = zlicz_bledyPowielanie(dane_wejsciowe, odkodowane_dane)
    return bledy, odkodowane_dane, dane_po_kanale, zakodowane
