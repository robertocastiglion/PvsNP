"""Famiglie di formule split tiny con interpolante noto, per misurare la costruzione.

Tutte INSODD. come A∧B, con split pulito (p ∩ q = ∅ per clausola).
Numerazione variabili: z_1..z_n = 1..n ; poi le private.
"""
from __future__ import annotations

from pnp_lab.proof_complexity.formula import Clause
from .interp import Split


def or_family(n: int) -> Split:
    """Interpolante atteso = OR(z_1..z_n).

    z = 1..n condivise; a = n+1 (A-privata); b = n+2 (B-privata).
    A:  (a ∨ z_1 ∨ … ∨ z_n) , (¬a ∨ z_1 ∨ … ∨ z_n)   → forza (z_1∨…∨z_n)
    B:  (b ∨ ¬z_i) , (¬b ∨ ¬z_i)  per ogni i          → forza ¬z_i per ogni i
    A∧B insodd: A vuole almeno uno z=1, B li vuole tutti 0.
    A|α insodd ⟺ tutti z=0 ;  B|α insodd ⟺ qualche z=1  → I = OR(z).
    """
    z = list(range(1, n + 1))
    a, b = n + 1, n + 2
    base = frozenset(z)
    a_clauses: list[Clause] = [base | {a}, base | {-a}]
    b_clauses: list[Clause] = []
    for zi in z:
        b_clauses.append(frozenset({b, -zi}))
        b_clauses.append(frozenset({-b, -zi}))
    return Split(tuple(a_clauses), tuple(b_clauses),
                 frozenset(z), frozenset({a}), frozenset({b}))


def and_family(n: int) -> Split:
    """Interpolante atteso = AND(z_1..z_n) (duale dell'or_family).

    A:  (a ∨ z_i) , (¬a ∨ z_i) per ogni i  → forza z_i per ogni i
    B:  (b ∨ ¬z_1 ∨ … ∨ ¬z_n) , (¬b ∨ ¬z_1 ∨ … ∨ ¬z_n) → forza (¬z_1∨…∨¬z_n)
    A|α insodd ⟺ qualche z=0 ; B|α insodd ⟺ tutti z=1 → I = AND(z).
    """
    z = list(range(1, n + 1))
    a, b = n + 1, n + 2
    a_clauses: list[Clause] = []
    for zi in z:
        a_clauses.append(frozenset({a, zi}))
        a_clauses.append(frozenset({-a, zi}))
    negbase = frozenset(-zi for zi in z)
    b_clauses: list[Clause] = [negbase | {b}, negbase | {-b}]
    return Split(tuple(a_clauses), tuple(b_clauses),
                 frozenset(z), frozenset({a}), frozenset({b}))


def clique_triangle_K4() -> Split:
    """Split che codifica f = "il grafo contiene un triangolo" su K4.

    6 variabili CONDIVISE = i 6 archi di K4 (numerazione 1-based):
        z1=12, z2=13, z3=14, z4=23, z5=24, z6=34.
    I 4 triangoli (3-clique) di K4, come terne di archi:
        T1={1,2,4}  (vertici 1,2,3)   archi 12,13,23
        T2={1,3,5}  (vertici 1,2,4)   archi 12,14,24
        T3={2,3,6}  (vertici 1,3,4)   archi 13,14,34
        T4={4,5,6}  (vertici 2,3,4)   archi 23,24,34

    A(p, z)  "il grafo CONTIENE un triangolo", con selettori privati a1..a4:
        (a1 v a2 v a3 v a4)                 -- almeno un triangolo scelto
        (¬ak v zi)  per ogni arco zi di Tk  -- ak => tutti gli archi di Tk accesi
      A|z e' SODD  <=>  z contiene qualche triangolo.  La risoluzione che elimina
      i selettori a_k combina i rami via OR (regola A-privata) con operandi NON
      costanti (i singoli archi del triangolo).

    B(q, z)  "il grafo e' triangle-free", con testimoni privati b1..b4:
        per ogni triangolo Tk = {x,y,w}:
            (¬x v ¬y v ¬w v ¬bk)            -- se bk, almeno un arco di Tk spento
            (bk)                            -- bk e' forzato vero (testimone attivo)
      B|z e' SODD  <=>  ogni triangolo ha un arco spento  <=>  z e' triangle-free.
      La risoluzione che elimina i b_k combina i rami via AND (regola B-privata).

    A ∧ B e' INSODD (nessun z e' contemporaneamente con-triangolo e triangle-free).
    Interpolante atteso  I(z) = f(z) = "z contiene un triangolo".
    """
    z = [1, 2, 3, 4, 5, 6]  # archi condivisi
    # archi di ciascun triangolo (sugli indici 1..6)
    triangles = [
        (1, 2, 4),  # T1
        (1, 3, 5),  # T2
        (2, 3, 6),  # T3
        (4, 5, 6),  # T4
    ]
    # selettori A-privati: a1..a4 = 7..10 ; testimoni B-privati: b1..b4 = 11..14
    a = [7, 8, 9, 10]
    b = [11, 12, 13, 14]

    a_clauses: list[Clause] = [frozenset(a)]  # almeno un triangolo
    for k, tri in enumerate(triangles):
        for edge in tri:
            a_clauses.append(frozenset({-a[k], edge}))  # a_k => arco acceso

    b_clauses: list[Clause] = []
    for k, tri in enumerate(triangles):
        x, y, w = tri
        b_clauses.append(frozenset({-x, -y, -w, -b[k]}))  # b_k => un arco spento
        b_clauses.append(frozenset({b[k]}))               # b_k forzato vero

    return Split(
        tuple(a_clauses), tuple(b_clauses),
        frozenset(z), frozenset(a), frozenset(b),
    )


def threshold2_family(n: int) -> Split:
    """Interpolante 'almeno 2 degli z sono 1' — funzione NON letterale-singola.

    Costruzione diretta senza private: per ogni α con <2 uni vogliamo A insodd,
    per ogni α con ≥2 uni vogliamo B insodd. Realizziamo A e B come insiemi di
    clausole sui soli z (private vuote) che diventano insodd. esattamente lì.

    A = { ¬(α) : peso(α) < 2 } cioè una clausola che esclude ciascun α leggero;
    una clausola che è falsa SOLO in α: (⋁_i ℓ_i) con ℓ_i = z_i se α_i=0 else ¬z_i,
    negata… più semplice: A insodd su α leggeri ⟺ A contiene la clausola-unità
    che α viola. Per avere A|α insodd ⟺ peso(α)<2, mettiamo in A la clausola
    'almeno 2 uni' spezzata? Non è una singola clausola. Allora usiamo private.

    Qui A codifica 'esistono due indici distinti i<j con z_i=z_j=1' tramite una
    private 'scelta' — troppo grande. Per il ciclo restiamo su or/and, e usiamo
    threshold solo come banco per `min_interpolant_dt_size` costruendo i forced a
    mano (vedi tests). Questa funzione resta non implementata di proposito.
    """
    raise NotImplementedError("threshold gestita via forced-table nei test")
