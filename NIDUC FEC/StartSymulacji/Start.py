from Przesyl.BSC import KanalBSC
from WysylanieOdbieranie.Nadawca import Nadawca
from WysylanieOdbieranie.Odbiorca import Odbiorca

kanal_bsc = KanalBSC(prawd_bledu=0.1)

# Inicjalizacja nadawcy i odbiorcy
nadawca = Nadawca(kanal=kanal_bsc)
odbiorca = Odbiorca()

# Przykładowe dane do wysłania
dane = [1, 0, 1, 1, 0, 0, 1, 0]

# Nadawca wysyła dane przez kanał
dane_po_kanale = nadawca.wyslij(dane)

# Odbiorca odbiera dane po przejściu przez kanał
dane_odebrane = odbiorca.odbierz(dane_po_kanale)