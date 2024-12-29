class BCH:
    def __init__(self, n=15, k=8):
        """
        Klasa obsługująca kodowanie i dekodowanie za pomocą kodu BCH.
        :param n: Długość zakodowanych danych (np. BCH(15, 8) -> n=15)
        :param k: Długość oryginalnych danych (np. BCH(15, 8) -> k=8)
        """
        self.n = n
        self.k = k
        self.m = n - k  # Liczba bitów nadmiarowych
        self.generator = [1, 0, 1, 1]  # Przykładowy wielomian generujący (dla uproszczenia)

    def koduj(self, dane):
        """
        Kodowanie danych za pomocą BCH.
        :param dane: Oryginalne dane wejściowe w formie listy bitów (np. [1, 0, 1, 0, 1, 0, 1, 0])
        :return: Zakodowane dane w formie listy bitów
        """
        if len(dane) != self.k:
            raise ValueError(f"Długość danych wejściowych musi wynosić {self.k} bitów.")

        # Dodajemy bity nadmiarowe (na początku jako zera)
        dane_rozszerzone = dane + [0] * self.m

        # Obliczamy resztę z dzielenia wielomianowego
        for i in range(len(dane)):
            if dane_rozszerzone[i] == 1:  # Dzielimy, tylko jeśli bit jest równy 1
                for j in range(len(self.generator)):
                    dane_rozszerzone[i + j] ^= self.generator[j]

        # Dodajemy resztę jako bity nadmiarowe
        bity_nadmiarowe = dane_rozszerzone[-self.m:]
        return dane + bity_nadmiarowe

    def dekoduj(self, dane):
        """
        Dekodowanie danych BCH. W tym przypadku poprawiamy 1 błąd.
        :param dane: Zakodowane dane (np. 15 bitów w BCH(15, 8))
        :return: Oryginalne dane (8 bitów) w formie listy
        """
        if len(dane) != self.n:
            raise ValueError(f"Długość danych wejściowych musi wynosić {self.n} bitów.")

        # Obliczamy syndrom błędu
        syndrom = dane[:]
        for i in range(len(dane) - self.m):
            if syndrom[i] == 1:  # Dzielimy, tylko jeśli bit jest równy 1
                for j in range(len(self.generator)):
                    syndrom[i + j] ^= self.generator[j]

        # Jeśli syndrom jest zerowy, dane są poprawne
        if max(syndrom[-self.m:]) == 0:
            return dane[:self.k]  # Pierwsze k bitów to oryginalne dane

        # Korekcja błędu (przeszukiwanie)
        for i in range(len(dane)):
            dane_testowe = dane[:]
            dane_testowe[i] ^= 1  # Inwersja jednego bitu
            syndrom_testowe = dane_testowe[:]
            for j in range(len(dane_testowe) - self.m):
                if syndrom_testowe[j] == 1:
                    for k in range(len(self.generator)):
                        syndrom_testowe[j + k] ^= self.generator[k]
            if max(syndrom_testowe[-self.m:]) == 0:
                return dane_testowe[:self.k]  # Znaleziono poprawne dane

        # Jeśli nie można naprawić, zwracamy pierwsze k bitów, ale odnotowujemy błędy
        print("Nie udało się naprawić danych. Zwracam dane z możliwymi błędami.")
        return dane[:self.k]
