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


class KanalGilbertaElliotta:
    """
    Model kanału Gilberta-Elliotta, który symuluje błędy grupowe.
    Kanał ma dwa stany: "dobry" (niskie_prawd_bledu) i "zly" (wysokie_prawd_bledu).
    Parametry:
    - niskie_prawd_bledu: Prawdopodobieństwo błędu w stanie "dobrym".
    - wysokie_prawd_bledu: Prawdopodobieństwo błędu w stanie "złym".
    - przejscie_dobry_na_zly: Prawdopodobieństwo przejścia ze stanu "dobrego" do "złego".
    - przejscie_zly_na_dobry: Prawdopodobieństwo przejścia ze stanu "złego" do "dobrego".
    """
    def __init__(self, niskie_prawd_bledu, wysokie_prawd_bledu, przejscie_dobry_na_zly, przejscie_zly_na_dobry):
        self.niskie_prawd_bledu = niskie_prawd_bledu
        self.wysokie_prawd_bledu = wysokie_prawd_bledu
        self.przejscie_dobry_na_zly = przejscie_dobry_na_zly
        self.przejscie_zly_na_dobry = przejscie_zly_na_dobry
        self.czy_stan_zly = False  # Zaczynamy w stanie "dobrym"

    def transmituj(self, dane):
        """
        Przesyła dane przez kanał Gilberta-Elliotta, wprowadzając błędy grupowe.
        Argumenty:
        - dane: Lista bitów (0 lub 1), które mają być przesłane przez kanał.
        Zwraca:
        - Lista bitów po przesłaniu przez kanał (może zawierać błędy).
        """
        dane_po_transmisji = []
        for bit in dane:
            # Wybierz prawdopodobieństwo błędu na podstawie aktualnego stanu
            prawd_bledu = self.wysokie_prawd_bledu if self.czy_stan_zly else self.niskie_prawd_bledu

            # Losowo wprowadź błąd na podstawie aktualnego prawdopodobieństwa błędu
            if random.random() < prawd_bledu:
                dane_po_transmisji.append(1 - bit)  # Inwersja bitu
            else:
                dane_po_transmisji.append(bit)  # Bez zmiany

            # Aktualizacja stanu (przejścia między "dobrym" i "złym" stanem)
            if self.czy_stan_zly:
                # Przejście ze "złego" do "dobrego" stanu
                if random.random() < self.przejscie_zly_na_dobry:
                    self.czy_stan_zly = False
            else:
                # Przejście z "dobrego" do "złego" stanu
                if random.random() < self.przejscie_dobry_na_zly:
                    self.czy_stan_zly = True

        return dane_po_transmisji
