from Kody.PowielanieBitow import PowielanieBitow
from ObslugaDanych.LiczenieBledow import zlicz_bledyPowielanie
from Przesyl.GEliot import KanalGilbertaElliotta


def SymulujPowielanieGEliot(dane_wejsciowe):
    """
    Symulacja kodowania i dekodowania danych za pomocą BCH oraz transmisji przez kanał Gilberta-Elliotta.
    :param dane_wejsciowe: Oryginalne dane wejściowe (ciąg zer i jedynek)
    :return: Liczba błędów w danych odebranych
    """
    powielanie = PowielanieBitow(liczba_powtorzen=3)
    kanal_ge = KanalGilbertaElliotta(niskie_prawd_bledu=0.1, wysokie_prawd_bledu=0.3,
                                     przejscie_dobry_na_zly=0.05, przejscie_zly_na_dobry=0.1)

    # Kodowanie danych
    zakodowane = powielanie.koduj(dane_wejsciowe)

    # Przesłanie danych przez kanał Gilberta-Elliotta
    dane_po_kanale = kanal_ge.transmituj(zakodowane)

    # Dekodowanie danych
    odkodowane_dane = powielanie.dekoduj(dane_po_kanale)

    # Obliczenie liczby błędów
    bledy = zlicz_bledyPowielanie(dane_wejsciowe, odkodowane_dane)
    return bledy, odkodowane_dane, dane_po_kanale