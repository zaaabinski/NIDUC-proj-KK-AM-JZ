from Przesyl.BSC import KanalBSC
from WysylanieOdbieranie.Nadawca import Nadawca


class Odbiorca:
    """
    Klasa Odbiorca symuluje odbiorcę, który odbiera dane po przesłaniu przez kanał transmisyjny.
    """

    def odbierz(self, dane_otrzymane):
        """
        Odbiera dane i próbuje zrekonstruować oryginalną wiadomość.

        Argumenty:
        - dane_otrzymane: Lista bitów (0 lub 1), które zostały odebrane po transmisji przez kanał.

        Zwraca:
        - Otrzymane dane (lista bitów), bez dalszej korekcji błędów.
        """
        print("Odbiorca: Odebrane dane:", dane_otrzymane)
        # Tu można dodać logikę dekodowania/korekcji błędów.
        # Obecnie zakładamy, że dane są odbierane tak, jak są.
        return dane_otrzymane
