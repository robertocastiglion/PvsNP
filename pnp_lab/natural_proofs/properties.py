"""Libreria di proprietà booleane di esempio, con commento sul loro destino.

Ogni proprietà è etichettata con quello che ci aspettiamo dall'analyzer.
Servono sia come test sia come materiale didattico/divulgativo: mostrano
in concreto la differenza fra una proprietà 'naturale' (vicolo cieco) e una
che evita la barriera.
"""

from __future__ import annotations

import math

from .analyzer import Property
from .boolean import BooleanFunction


# ---------------------------------------------------------------------------
# Proprietà NATURALI (costruttive + larghe) -> NON possono separare P/NP
# ---------------------------------------------------------------------------

def _is_balanced(f: BooleanFunction) -> bool:
    """f vale 1 su esattamente metà degli input."""
    return f.weight() * 2 == f.N


is_balanced = Property(
    name="is_balanced",
    predicate=_is_balanced,
    description=(
        "f è bilanciata (tanti 1 quanti 0). Costruttiva (basta contare gli 1) "
        "e larga: la frazione ~ 1/sqrt(N) = 2^(-n/2), decadimento lineare in n "
        "-> NATURALE."
    ),
)


def _depends_on_all_variables(f: BooleanFunction) -> bool:
    """f dipende davvero da ogni variabile (nessuna variabile 'fittizia')."""
    tt = f.truth_table
    for var in range(f.n):
        bit = f.n - 1 - var  # posizione del bit di questa variabile nell'indice
        mask = 1 << bit
        sensitive = False
        for i in range(f.N):
            if i & mask:
                continue
            if tt[i] != tt[i | mask]:
                sensitive = True
                break
        if not sensitive:
            return False
    return True


depends_on_all_variables = Property(
    name="depends_on_all_variables",
    predicate=_depends_on_all_variables,
    description=(
        "f dipende da tutte le n variabili. Costruttiva e larghissima (quasi "
        "tutte le funzioni dipendono da tutto) -> NATURALE."
    ),
)


def _majority_of_truth_table(f: BooleanFunction) -> bool:
    """La maggioranza degli output di f è 1."""
    return f.weight() * 2 > f.N


has_majority_ones = Property(
    name="has_majority_ones",
    predicate=_majority_of_truth_table,
    description=(
        "Più 1 che 0 nella truth table. Costruttiva e larga (~1/2 delle "
        "funzioni) -> NATURALE."
    ),
)


# ---------------------------------------------------------------------------
# Proprietà COSTRUTTIVE ma NON larghe -> evitano la barriera (sul fronte largh.)
# ---------------------------------------------------------------------------

def _is_constant(f: BooleanFunction) -> bool:
    s = f.weight()
    return s == 0 or s == f.N


is_constant = Property(
    name="is_constant",
    predicate=_is_constant,
    description=(
        "f è costante (sempre 0 o sempre 1). Costruttiva ma RARISSIMA: solo 2 "
        "funzioni su 2^(2^n), frazione 2^(1-2^n) -> decadimento ESPONENZIALE "
        "in N (super-lineare in n) -> NON larga."
    ),
)


def _is_parity(f: BooleanFunction) -> bool:
    """f è esattamente la parità (XOR) di tutte le sue variabili, eventualmente negata."""
    parity = [bin(i).count("1") & 1 for i in range(f.N)]
    neg_parity = [1 - p for p in parity]
    return list(f.truth_table) == parity or list(f.truth_table) == neg_parity


is_parity = Property(
    name="is_parity",
    predicate=_is_parity,
    description=(
        "f è la funzione parità (o la sua negazione). Costruttiva ma con sole 2 "
        "funzioni su tutte -> NON larga. Storicamente, la parità è al centro dei "
        "lower bound per circuiti AC^0 (Furst–Saxe–Sipser, Håstad)."
    ),
)


# ---------------------------------------------------------------------------
# Proprietà LARGHE ma NON costruttive -> il tipo che servirebbe davvero
# ---------------------------------------------------------------------------

def _high_circuit_complexity_bruteforce(f: BooleanFunction) -> bool:
    """Vera se f NON è calcolabile da un circuito 'piccolo'.

    Approssimiamo 'piccolo' con una ricerca a forza bruta su formule costruite
    da AND/OR/NOT di profondità limitata sulle variabili: la valutazione costa
    in modo che cresce molto rapidamente con n. È intenzionalmente costosa per
    illustrare la NON costruttività: nessuno sa calcolare la complessità di
    circuito in tempo poly(N) — è proprio questo che la rende 'non naturale'.
    """
    # Genera funzioni "semplici" (calcolabili da piccoli circuiti) e verifica se
    # f coincide con una di esse. La generazione esplode con n -> non costruttiva.
    n = f.n
    simple = _enumerate_small_circuit_functions(n, max_gates=2)
    return f.truth_table not in simple


def _enumerate_small_circuit_functions(n: int, max_gates: int) -> set[tuple[int, ...]]:
    """Insieme delle truth table realizzabili con al più ``max_gates`` porte.

    Implementazione deliberatamente ingenua e costosa (cresce molto in fretta):
    serve a mostrare che decidere la complessità di circuito non è costruttivo.
    """
    N = 1 << n
    # funzioni base: variabili e loro negazioni, più costanti
    base: set[tuple[int, ...]] = set()
    for var in range(n):
        bit = n - 1 - var
        tt = tuple((i >> bit) & 1 for i in range(N))
        base.add(tt)
        base.add(tuple(1 - v for v in tt))
    base.add(tuple(0 for _ in range(N)))
    base.add(tuple(1 for _ in range(N)))

    reachable = set(base)
    frontier = set(base)
    for _ in range(max_gates):
        new_funcs: set[tuple[int, ...]] = set()
        cur = list(reachable)
        for a in cur:
            for b in frontier:
                new_funcs.add(tuple(x & y for x, y in zip(a, b)))   # AND
                new_funcs.add(tuple(x | y for x, y in zip(a, b)))   # OR
        frontier = new_funcs - reachable
        reachable |= new_funcs
    return reachable


high_circuit_complexity = Property(
    name="high_circuit_complexity",
    predicate=_high_circuit_complexity_bruteforce,
    description=(
        "f NON è calcolabile da un circuito piccolo. Asintoticamente è LARGA "
        "(Shannon 1949: quasi tutte le funzioni hanno alta complessità di "
        "circuito) ma NON costruttiva: deciderla richiede di esplorare i "
        "circuiti, con costo che esplode. È il tipo di proprietà 'non naturale' "
        "che servirebbe a una vera separazione di P e NP.\n\n"
        "LEZIONE: a n piccolo (gli unici calcolabili) la larghezza NON si vede — "
        "a n=2 TUTTE le funzioni sono semplici (frazione 0), a n=3 già ~50%. La "
        "proprietà che aggira la barriera è proprio quella che il tool non riesce "
        "a calcolare: non è una coincidenza, è il cuore della difficoltà."
    ),
)


# ---------------------------------------------------------------------------
# Indice
# ---------------------------------------------------------------------------

#: Tutte le proprietà di esempio, per iterare nei demo/test.
ALL_PROPERTIES = [
    is_balanced,
    depends_on_all_variables,
    has_majority_ones,
    is_constant,
    is_parity,
    high_circuit_complexity,
]
