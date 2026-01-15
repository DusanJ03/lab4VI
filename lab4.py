import math

N = 4
start = (1, 2)
cilj = (2, 1)

zabranjena = {
    (1, 1), 
    (3, 2)  
}

def h_heuristika(cvor, cilj):
    return abs(cvor[0] - cilj[0]) + abs(cvor[1] - cilj[1])

def je_ciljno_stanje(trenutni_cvor, cilj):
    return trenutni_cvor == cilj

def get_destination(cvor, n, zabranjena):
    i, j = cvor
    moguci_potezi = [
        (i - 1, j), 
        (i + 1, j), 
        (i, j - 1), 
        (i, j + 1)
    ]
    
    valid_destination = []
    for r, k in moguci_potezi:
        if 0 <= r < n and 0 <= k < n and (r, k) not in zabranjena:
            valid_destination.append((r, k))
                
    return valid_destination

def a_star_trazenje(start, cilj, n, zabranjena):
    za_obradu = [start]
    
    prethodnici = {}
    prethodnici[start] = None
    
    g = {start: 0}
    
    f = {start: h_heuristika(start, cilj)}
    
    print(f"Pretraga od {start} do {cilj}")

    while len(za_obradu) > 0:
        trenutni = None

        for sledeci in za_obradu:
            if trenutni is None or g[sledeci] + h_heuristika(sledeci, cilj) < g[trenutni] + h_heuristika(trenutni, cilj):
                trenutni = sledeci

        if je_ciljno_stanje(trenutni, cilj):
            print("Pronasli smo cilj!")
            return put(prethodnici, trenutni)
        
        za_obradu.remove(trenutni)
        
        destinations = get_destination(trenutni, n, zabranjena)
        
        for destination in destinations:
            privremeni_g = g[trenutni] + 1
            
            if destination not in g or privremeni_g < g[destination]:
                prethodnici[destination] = trenutni
                g[destination] = privremeni_g
                f[destination] = g[destination] + h_heuristika(destination, cilj)
                
                if destination not in za_obradu:
                    za_obradu.append(destination)
                    
    print("Nije pronađen put do cilja.")
    return None

def put(prethodnici, trenutni):
    put = [trenutni]
    while prethodnici[trenutni] is not None:
        trenutni = prethodnici[trenutni]
        put.append(trenutni)
    put.reverse()
    return put

rezultat = a_star_trazenje(start, cilj, N, zabranjena)

if rezultat:
    print(f"Najkraci put ima {len(rezultat)-1} koraka.")
    print("Putanja:")
    print(rezultat)
    
    print("\nVizuelni prikaz:")
    for r in range(N):
        linija = ""
        for k in range(N):
            if (r, k) == start:
                linija += " S " 
            elif (r, k) == cilj:
                linija += " C " 
            elif (r, k) in zabranjena:
                linija += " X " 
            elif (r, k) in rezultat:
                linija += " * " 
            else:
                linija += " . "
        print(linija)