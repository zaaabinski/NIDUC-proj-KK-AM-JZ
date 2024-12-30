from Kody.BCH import BCH
from ObslugaDanych.LiczenieBledow import zlicz_bledy_bch
from Przesyl.BSC import KanalBSC


def SymulujBCH(dane_wejsciowe):
    """
    Symulacja kodowania i dekodowania danych za pomocą BCH oraz transmisji przez BSC.
    :param dane_wejsciowe: Oryginalne dane wejściowe (ciąg zer i jedynek)
    :return: Liczba błędów w danych odebranych
    """
    # Inicjalizacja klasy BCH i kanału BSC
    bch = BCH(n=15, k=8)
    kanal_bsc = KanalBSC(prawd_bledu=0.1)

    # Kodowanie danych
    zakodowane = bch.koduj(dane_wejsciowe)

    # Przesłanie danych przez kanał BSC
    dane_po_kanale = kanal_bsc.transmituj(zakodowane)

    # Dekodowanie danych
    odkodowane_dane = bch.dekoduj(dane_po_kanale)

    # Obliczenie liczby błędów
    bledy = zlicz_bledy_bch(dane_wejsciowe, odkodowane_dane)
    return bledy, odkodowane_dane, dane_po_kanale, zakodowane