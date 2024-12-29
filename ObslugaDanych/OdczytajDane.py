import os
class OdczytDanych:
    """
    Klasa do odczytu danych binarnych z pliku tekstowego.
    """
    def __init__(self, sciezka_do_pliku):
        self.sciezka_do_pliku = sciezka_do_pliku

    def odczytaj_dane(self):
        """
        Odczytuje linie z pliku i filtruje tylko te, które są w formacie binarnym.
        Zwraca listę binarnych ciągów bitów.
        """
        dane = []
        if not os.path.exists(self.sciezka_do_pliku):
            raise FileNotFoundError(f"Plik {self.sciezka_do_pliku} nie istnieje.")

        with open(self.sciezka_do_pliku, 'r') as plik:
            for linia in plik:
                linia = linia.strip()  # Usuń białe znaki
                if all(znak in {'0', '1'} for znak in linia):  # Sprawdź, czy linia jest binarna
                    dane.append([int(bit) for bit in linia])  # Przekształć ciąg na listę bitów
        return dane