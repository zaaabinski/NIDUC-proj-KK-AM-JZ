class PowielanieBitow:
    """
    Klasa implementująca metodę powielania bitów jako prostą technikę wykrywania i korekcji błędów.
    """
    def __init__(self, liczba_powtorzen=3):
        """
        Inicjalizuje system powielania bitów.
        Parametry:
        - liczba_powtorzen: Liczba razy, jaką każdy bit będzie powielany.
        """
        self.liczba_powtorzen = liczba_powtorzen

    def koduj(self, dane):
        """
        Koduje dane przez powielenie każdego bitu.
        Argumenty:
        - dane: Lista bitów do zakodowania.
        Zwraca:
        - Zakodowane dane jako lista bitów.
        """
        return [bit for bit in dane for _ in range(self.liczba_powtorzen)]

    def dekoduj(self, dane):
        """
        Dekoduje dane przez zliczanie większości w powtórzeniach bitów.
        Argumenty:
        - dane: Lista bitów odebranych.
        Zwraca:
        - Zdekodowane dane jako lista bitów.
        """
        odkodowane = []
        for i in range(0, len(dane), self.liczba_powtorzen):
            fragment = dane[i:i + self.liczba_powtorzen]
            odkodowane.append(1 if fragment.count(1) > fragment.count(0) else 0)
        return odkodowane
