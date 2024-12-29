def zlicz_bledyPowielanie(dane_poczatkowe, dane_koncowe):

    # Dopasowanie długości do krótszej listy
    dlugosc = min(len(dane_poczatkowe), len(dane_koncowe))

    # Zliczanie różnic w bitach
    liczba_roznic = sum(1 for i in range(dlugosc) if dane_poczatkowe[i] != dane_koncowe[i])

    # Dodanie różnic wynikających z nadmiarowych bitów (jeśli długości się różnią)
    liczba_roznic += abs(len(dane_poczatkowe) - len(dane_koncowe))
    return liczba_roznic


def zlicz_bledy_bch(dane_wejsciowe, dane_odebrane):
    """
    Liczy błędy między oryginalnymi danymi a danymi odebranymi po dekodowaniu.
    :param dane_wejsciowe: Lista bitów lub ciąg zer i jedynek (np. [1, 0, 1, 0] lub "1010")
    :param dane_odebrane: Lista bitów lub ciąg zer i jedynek (np. [1, 0, 1, 0] lub "1010")
    :return: Liczba błędów
    """
    # Konwersja danych wejściowych i odebranych na listę bitów
    if isinstance(dane_wejsciowe, str):
        dane_wejsciowe = [int(bit) for bit in dane_wejsciowe]
    if isinstance(dane_odebrane, str):
        dane_odebrane = [int(bit) for bit in dane_odebrane]

    # Upewnienie się, że długości danych są zgodne
    if len(dane_wejsciowe) != len(dane_odebrane):
        raise ValueError("Długość danych wejściowych i odebranych musi być taka sama.")

    # Zliczanie błędów
    return sum(1 for a, b in zip(dane_wejsciowe, dane_odebrane) if a != b)

def zlicz_bledy_LDPC(dane_wejsciowe, dane_odebrane):
    """
    Liczy liczbę błędów między danymi wejściowymi i odebranymi.
    :param dane_wejsciowe: Oryginalne dane wejściowe.
    :param dane_odebrane: Odkodowane dane wyjściowe.
    :return: Liczba błędów.
    """
    return sum(1 for a, b in zip(dane_wejsciowe, dane_odebrane) if a != b)