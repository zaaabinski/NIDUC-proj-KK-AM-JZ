class Nadawca:
    """
    Klasa Nadawca symuluje nadawcę, który wysyła dane przez kanał transmisyjny.
    """

    def __init__(self, kanal):
        """
        Inicjalizuje nadawcę z wybranym kanałem transmisyjnym.

        Parametry:
        - kanal: Obiekt kanału (np. KanalBSC lub KanalGilbertaElliotta), przez który dane będą transmitowane.
        """
        self.kanal = kanal

    def wyslij(self, dane):
        """
        Wysyła dane przez kanał, wprowadzając ewentualne błędy.

        Argumenty:
        - dane: Lista bitów (0 lub 1), które mają być przesłane.

        Zwraca:
        - Lista bitów po przesłaniu przez kanał.
        """
        #print("Nadawca: Wysyłam dane:", dane)
        dane_po_kanale = self.kanal.transmituj(dane)
       # print("Nadawca: Dane po przejściu przez kanał:", dane_po_kanale)
        return dane_po_kanale



