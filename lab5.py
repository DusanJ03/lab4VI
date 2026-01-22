import copy

N = 4

def inicijalizuj_domene():
    """
    Za svaku kolonu (0 do 3), domen su svi moguci redovi (0 do 3).
    Format: {kolona: {skup_mogucih_redova}}
    """
    domeni = {}
    for kolona in range(N):
        domeni[kolona] = set(range(N))
    return domeni


def degree_heuristics(dodeljeno, domeni):
    """
    Bira sledecu promenljivu (kolonu) koju cemo obradjivati.
    Kriterijum: Kolona koja je ukljucena u najvise ogranicenja sa
    drugim NEPOPUNJENIM promenljivama.
    """
    ne_dodeljene = [k for k in domeni.keys() if k not in dodeljeno]

    if not ne_dodeljene:
        return None

    najbolja_kolona = -1
    max_stepen = -1

    for kolona in ne_dodeljene:
        stepen = 0
        # Brojimo veze sa drugim nepopunjenim kolonama
        for druga_kolona in ne_dodeljene:
            if kolona != druga_kolona:
                # U problemu n-kraljica, svaka kolona ogranicava svaku drugu
                # (zbog redova i dijagonala), pa je ovo zapravo broj preostalih kolona.
                stepen += 1

        if stepen > max_stepen:
            max_stepen = stepen
            najbolja_kolona = kolona

    # Napomena: Kod N-Queens sve preostale kolone obicno imaju isti stepen,
    # pa se cesto svodi na izbor prve slobodne, ali ovo je formalna implementacija.
    return najbolja_kolona


def forward_checking(domeni, trenutna_kolona, odabrani_red):
    """
    Azurira domene ostalih kolona na osnovu poteza (trenutna_kolona, odabrani_red).
    Vraca nove domene ako je sve u redu, ili None ako neki domen postane prazan.
    """
    # Pravimo kopiju domena da ne bi unistili original ako budemo morali da radimo backtrack
    novi_domeni = copy.deepcopy(domeni)

    # Izbacujemo trenutnu kolonu iz domena jer je resena
    # (ili je mozemo ostaviti sa samo tom vrednoscu, ali lakse je ignorisati je kasnije)
    del novi_domeni[trenutna_kolona]

    for kolona in novi_domeni:
        # Promenljive koje treba izbaciti iz domena 'kolona'
        za_brisanje = set()

        for r in novi_domeni[kolona]:
            # 1. Provera istog reda
            if r == odabrani_red:
                za_brisanje.add(r)

            # 2. Provera dijagonala
            # Uslov napada dijagonalno: |r1 - r2| == |c1 - c2|
            if abs(r - odabrani_red) == abs(kolona - trenutna_kolona):
                za_brisanje.add(r)

        # Uklanjanje nevalidnih vrednosti
        novi_domeni[kolona] -= za_brisanje

        # Ako je domen neke kolone ostao prazan, ovaj potez nije dobar
        if len(novi_domeni[kolona]) == 0:
            return None

    return novi_domeni


def backtracking(dodeljeno, domeni):
    """
    Glavna rekurzivna funkcija.
    dodeljeno: dict {kolona: red} - trenutno resenje
    domeni: dict {kolona: {moguci_redovi}} - preostale opcije
    """
    # 1. Baza rekurzije: Ako su sve kolone dodeljene, nasli smo resenje
    if len(dodeljeno) == N:
        return dodeljeno

    # 2. Odabir sledece promenljive pomocu Degree Heuristike
    kolona = degree_heuristics(dodeljeno, domeni)

    # 3. Iteracija kroz vrednosti (redove) u domenu odabrane kolone
    # Mozemo sortirati vrednosti (LCV), ali ovde idemo redom
    moguci_redovi = list(domeni[kolona])

    for red in moguci_redovi:
        # Pokusavamo dodelu
        nova_dodela = dodeljeno.copy()
        nova_dodela[kolona] = red

        # 4. Forward Checking
        # Pokusavamo da smanjimo domene buducim promenljivama
        skraceni_domeni = forward_checking(domeni, kolona, red)

        # Ako FC nije vratio None, znaci da nismo unistili nijednu buducu promenljivu
        if skraceni_domeni is not None:
            rezultat = backtracking(nova_dodela, skraceni_domeni)
            if rezultat is not None:
                return rezultat

    # Ako smo probali sve redove i nista nije uspelo, vracamo se nazad (Backtrack)
    return None


def prikazi_tablu(resenje):
    if resenje is None:
        print("Nema resenja.")
        return

    tabla = [["." for _ in range(N)] for _ in range(N)]
    for kol, red in resenje.items():
        tabla[red][kol] = "Q"

    print("\nRešenje (Q predstavlja kraljicu):")
    for red in range(N):
        print(" ".join(tabla[red]))
    print(f"\nKoordinate (Kolona: Red): { dict(sorted(resenje.items())) }")


# --- Glavni program ---
if __name__ == "__main__":
    startni_domeni = inicijalizuj_domene()
    startna_dodela = {}

    konacno_resenje = backtracking(startna_dodela, startni_domeni)
    prikazi_tablu(konacno_resenje)