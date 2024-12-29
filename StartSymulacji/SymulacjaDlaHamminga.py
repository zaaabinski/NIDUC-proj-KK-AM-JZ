from Przesyl.BSC import KanalBSC
from Przesyl.Hamming import Hamming


def SymulujHamminga(dane_wejsciowe):
    hamming = Hamming()

    # Zakodowanie danych
    zakodowane = hamming.koduj(dane_wejsciowe)
    print(f"Zakodowane dane: {zakodowane}")

    # Symulacja przesyłania z błędem
    dane_po_kanale = KanalBSC.transmituj(zakodowane)
    print(f"Dane po błędzie: {zakodowane}")

    # Odkodowanie danych
    odkodowane = hamming.dekoduj(dane_po_kanale)
    print(f"Odkodowane dane: {odkodowane}")
