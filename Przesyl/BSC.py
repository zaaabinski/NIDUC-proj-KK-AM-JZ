import random

class KanalBSC:
    """
    Model kanału BSC (Binary Symmetric Channel), który symuluje przypadkowe błędy w przesyłanych bitach.
    Parametry:
    - prawd_bledu: Prawdopodobieństwo wystąpienia błędu dla każdego bitu (wartość od 0 do 1).
    """
    def __init__(self, prawd_bledu):
        self.prawd_bledu = prawd_bledu

    def transmituj(self, dane):
        """
        Przesyła dane przez kanał BSC, wprowadzając błędy zgodnie z prawdopodobieństwem prawd_bledu.
        Argumenty:
        - dane: Lista bitów (0 lub 1), które mają być przesłane przez kanał.
        Zwraca:
        - Lista bitów po przesłaniu przez kanał (może zawierać błędy).
        """
        dane_po_transmisji = []
        for bit in dane:
            # Losowo zmienia bit, jeśli wygenerowana liczba jest mniejsza niż prawd_bledu
            if random.random() < self.prawd_bledu:
                dane_po_transmisji.append(1 - bit)  # Inwersja bitu (0->1 lub 1->0)
            else:
                dane_po_transmisji.append(bit)  # Bez zmiany
        return dane_po_transmisji


