from Kody.PowielanieBitow import PowielanieBitow
from ObslugaDanych.LiczenieBledow import zlicz_bledyPowielanie
from Przesyl.GEliot import KanalGilbertaElliotta


def SymulujPowielanieGEliot(dane_wejsciowe, error_prob=0.1, repetitions=3):
    """
    Symulacja kodowania i dekodowania danych za pomocą powielania oraz transmisji przez kanał Gilberta-Elliotta.
    :param dane_wejsciowe: Oryginalne dane wejściowe (ciąg zer i jedynek)
    :param error_prob: Podstawowe prawdopodobieństwo błędu (dla stanu dobrego)
    :param repetitions: Liczba powtórzeń każdego bitu
    :return: Liczba błędów w danych odebranych
    """
    powielanie = PowielanieBitow(liczba_powtorzen=repetitions)
    # Używamy error_prob jako niskiego prawdopodobieństwa błędu, a 3x większe jako wysokie
    kanal_ge = KanalGilbertaElliotta(
        niskie_prawd_bledu=error_prob,
        wysokie_prawd_bledu=min(3 * error_prob, 1.0),
        przejscie_dobry_na_zly=0.05,
        przejscie_zly_na_dobry=0.1
    )

    # Kodowanie danych
    zakodowane = powielanie.koduj(dane_wejsciowe)

    # Przesłanie danych przez kanał Gilberta-Elliotta
    dane_po_kanale = kanal_ge.transmituj(zakodowane)

    # Dekodowanie danych
    odkodowane_dane = powielanie.dekoduj(dane_po_kanale)

    # Obliczenie liczby błędów
    bledy = zlicz_bledyPowielanie(dane_wejsciowe, odkodowane_dane)
    return bledy, odkodowane_dane, dane_po_kanale