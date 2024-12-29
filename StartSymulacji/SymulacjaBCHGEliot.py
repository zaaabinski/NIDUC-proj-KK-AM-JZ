from Kody.BCH import BCH
from ObslugaDanych.LiczenieBledow import zlicz_bledy_bch
from Przesyl.GEliot import KanalGilbertaElliotta


def SymulujBCHEliot(dane_wejsciowe):
    """
    Symulacja kodowania i dekodowania danych za pomocą BCH oraz transmisji przez kanał Gilberta-Elliotta.
    :param dane_wejsciowe: Oryginalne dane wejściowe (ciąg zer i jedynek)
    :return: Liczba błędów w danych odebranych
    """
    # Inicjalizacja klasy BCH i kanału Gilberta-Elliotta
    bch = BCH(n=15, k=8)
    kanal_ge = KanalGilbertaElliotta(niskie_prawd_bledu=0.1, wysokie_prawd_bledu=0.3,
                                     przejscie_dobry_na_zly=0.05, przejscie_zly_na_dobry=0.1)

    # Kodowanie danych
    zakodowane = bch.koduj(dane_wejsciowe)

    # Przesłanie danych przez kanał Gilberta-Elliotta
    dane_po_kanale = kanal_ge.transmituj(zakodowane)

    # Dekodowanie danych
    odkodowane_dane = bch.dekoduj(dane_po_kanale)

    # Obliczenie liczby błędów
    bledy = zlicz_bledy_bch(dane_wejsciowe, odkodowane_dane)
    return bledy, odkodowane_dane, dane_po_kanale