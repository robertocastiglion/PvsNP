"""
Complessità di **formula** esatta di tutte le funzioni booleane piccole.

Definizione usata. La *dimensione di formula* di f è il numero minimo di gate
binari (∧, ∨) in una formula (un albero, senza condivisione) che calcola f,
avendo come foglie i letterali x_i e ¬x_i (gratuiti). È una misura additiva:
una formula ottima di dimensione s si spezza in due sotto-formule di dimensioni
i e s−1−i unite da un gate. Questo rende il calcolo esatto via programmazione
dinamica per dimensione crescente — la prima volta che incontriamo una funzione,
quella è la sua complessità minima.

Perché è interessante per P vs NP. Il **teorema di Shannon (1949)** dice che
*quasi tutte* le funzioni booleane richiedono circuiti (e formule) di dimensione
esponenziale, ~2^n/n. Eppure non sappiamo esibire UNA funzione esplicita in NP
che sia dimostrabilmente difficile: è esattamente il muro dei lower bound sui
circuiti. Qui lo vediamo in piccolo: enumeriamo lo spettro completo delle
complessità per n piccolo e osserviamo che la stragrande maggioranza delle
funzioni si accumula sui valori alti.

Nota onesta: la dimensione di *formula* (albero) è un limite superiore della
dimensione di *circuito* (DAG, con riuso dei gate). Le usiamo perché la prima è
esattamente e rapidamente calcolabile; il messaggio di Shannon vale per entrambe.
"""
from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass

from .circuit import AND, NOT, OR, mask_for, projection


@dataclass
class ComplexityTable:
    """Complessità di formula esatta per tutte le funzioni su n variabili."""

    n: int
    cost: dict[int, int]          # truth table -> dimensione di formula minima
    expr: dict[int, str]          # truth table -> una formula ottima (stringa)
    complete: bool                # True se TUTTE le 2^(2^n) funzioni sono coperte

    @property
    def num_functions(self) -> int:
        return 1 << (1 << self.n)

    @property
    def max_cost(self) -> int:
        return max(self.cost.values())

    def distribution(self) -> dict[int, int]:
        """Mappa dimensione -> quante funzioni hanno quella dimensione minima."""
        dist: dict[int, int] = defaultdict(int)
        for c in self.cost.values():
            dist[c] += 1
        return dict(sorted(dist.items()))

    def hardest(self) -> list[int]:
        """Le truth table con complessità massima."""
        m = self.max_cost
        return [t for t, c in self.cost.items() if c == m]


def _literals(n: int) -> dict[int, str]:
    """Le foglie (costo 0): ogni variabile e la sua negazione."""
    seeds: dict[int, str] = {}
    for j in range(n):
        xj = projection(n, j)
        seeds.setdefault(xj, f"x{j+1}")
        seeds.setdefault(NOT(xj, n), f"¬x{j+1}")
    return seeds


def min_formula_sizes(n: int, cap: int = 60) -> ComplexityTable:
    """Calcola la dimensione di formula minima di OGNI funzione su n variabili.

    Programmazione dinamica per dimensione crescente: alla prima volta che una
    funzione compare, quella è la sua dimensione minima. La base {letterali, ∧,
    ∨} è completa (ogni funzione ha una DNF), quindi si raggiungono tutte le
    2^(2^n) funzioni. Pratico per n ≤ 3 (256 funzioni); eseguibile per n = 4.
    ``cap`` è il tetto di sicurezza sulla dimensione esplorata.

    Nota: NON ci si ferma al primo livello "vuoto" — con questa base una taglia
    può non produrre nuove funzioni mentre una taglia maggiore sì (le partizioni
    cambiano), quindi si continua finché tutte sono coperte o si tocca ``cap``.
    """
    total = 1 << (1 << n)
    cost: dict[int, int] = {}
    expr: dict[int, str] = {}
    by_cost: dict[int, list[int]] = defaultdict(list)

    # dimensione 0: i letterali
    for table, name in _literals(n).items():
        if table not in cost:
            cost[table] = 0
            expr[table] = name
            by_cost[0].append(table)

    size = 1
    while len(cost) < total and size <= cap:
        found: list[int] = []
        for i in range(size):  # partizione i + (size-1-i) + 1 gate
            left = by_cost[i]
            right = by_cost[size - 1 - i]
            for a in left:
                ea = expr[a]
                for b in right:
                    eb = expr[b]
                    for t, sym in ((AND(a, b), "∧"), (OR(a, b), "∨")):
                        if t not in cost:
                            cost[t] = size
                            expr[t] = f"({ea} {sym} {eb})"
                            found.append(t)
        by_cost[size].extend(found)
        size += 1

    return ComplexityTable(n=n, cost=cost, expr=expr, complete=(len(cost) == total))


def shannon_counting_bound(n: int) -> dict:
    """Stima quante funzioni POSSONO avere formule piccole vs il totale.

    Argomento di conteggio (Shannon/Lupanov). Le formule con s gate su n
    variabili sono al più ~ (numero di scelte)^s, un numero che cresce solo
    esponenzialmente in s, mentre le funzioni sono 2^(2^n): un doppio
    esponenziale. Quindi per coprirle quasi tutte serve s ≈ 2^n / n. In altre
    parole: la frazione di funzioni "facili" tende a zero.
    """
    num_funcs = 1 << (1 << n)
    leaves = 2 * n  # x_i e ¬x_i
    # numero (grossolanamente sovrastimato) di formule con esattamente s gate:
    # ogni gate sceglie operazione (2) e i due operandi tra gli oggetti esistenti.
    return {
        "n": n,
        "num_functions": num_funcs,
        "log2_num_functions": 1 << n,  # log2(2^(2^n)) = 2^n
        "num_leaves": leaves,
        "shannon_estimate_size": (1 << n) // max(n, 1),  # ~ 2^n / n
    }
