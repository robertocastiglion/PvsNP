"""Il cuore eseguibile del metodo algoritmico: speedup di #SAT via sparsità.

L'idea di Williams in miniatura, ma ESATTA. Per contare gli assegnamenti che
soddisfano una funzione booleana, la forza bruta enumera tutti i 2^n input. Ma se
la funzione ha una rappresentazione come polinomio MULTILINEARE *sparso* (pochi
monomi), si può calcolare la somma su tutto il cubo senza enumerarlo:

    Σ_{x ∈ {0,1}^n}  Π_{i∈S} x_i  =  2^{n-|S|}

(il monomio χ_S vale 1 esattamente sugli x che hanno tutti i bit di S a 1). Quindi

    Σ_{x} f(x)  =  Σ_S c_S · 2^{n-|S|}

si calcola in O(#monomi) operazioni invece di O(2^n). Per i circuiti la cui classe
ammette rappresentazioni succinte (come ACC⁰ via Beigel–Tarui/Yao) questo è
*davvero* più veloce della forza bruta: la precondizione del metodo algoritmico.

Onestà: qui lo speedup viene dalla sparsità del polinomio (esatto e verificabile);
l'algoritmo ACC⁰ di Williams è una versione sofisticata della stessa idea (somma su
tutti gli input tramite una rappresentazione polinomiale + moltiplicazione veloce
di matrici).
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations, product
from typing import Dict, FrozenSet, List, Tuple

#: un polinomio multilineare: monomio (insieme di variabili) -> coefficiente intero
Monomials = Dict[FrozenSet[int], int]


@dataclass
class SparsePoly:
    """Polinomio multilineare su n variabili, come mappa monomio→coefficiente."""
    n: int
    terms: Monomials

    def eval(self, x: Tuple[int, ...]) -> int:
        total = 0
        for S, c in self.terms.items():
            if all(x[i] for i in S):
                total += c
        return total

    @property
    def sparsity(self) -> int:
        return len(self.terms)


@dataclass
class SatCount:
    value: int          # Σ_{x} f(x)  (= numero di assegnamenti veri se f è 0/1)
    ops: int            # operazioni svolte
    method: str


def count_bruteforce(poly: SparsePoly) -> SatCount:
    """Forza bruta: enumera tutti i 2^n input. O(2^n) operazioni."""
    total = 0
    for x in product((0, 1), repeat=poly.n):
        total += poly.eval(x)
    return SatCount(total, 1 << poly.n, "forza bruta (2^n)")


def count_fast(poly: SparsePoly) -> SatCount:
    """Metodo polinomiale: Σ_S c_S · 2^{n-|S|}. O(#monomi) operazioni."""
    total = 0
    for S, c in poly.terms.items():
        total += c * (1 << (poly.n - len(S)))
    return SatCount(total, poly.sparsity, "metodo polinomiale (sparsità)")


def speedup_factor(poly: SparsePoly) -> float:
    """Quante volte il metodo veloce batte la forza bruta su questo circuito."""
    return (1 << poly.n) / max(poly.sparsity, 1)


# ── circuiti d'esempio: strutturati (sparsi) vs densi ─────────────────────

def conj_poly(k: int, n: int) -> SparsePoly:
    """AND delle prime k variabili: UN solo monomio. Massimamente sparso.
    #SAT = 2^{n-k}."""
    return SparsePoly(n, {frozenset(range(k)): 1})


def disjoint_dnf_poly(groups: List[List[int]], n: int) -> SparsePoly:
    """OR di AND su gruppi di variabili DISGIUNTI (una DNF con termini disgiunti).

    Via inclusione-esclusione il polinomio ha 2^(#gruppi) − 1 monomi: SPARSO se i
    gruppi sono pochi, indipendentemente da n. Lo speedup scala con la *struttura*
    (numero di termini), non con n — l'essenza del metodo.
    """
    terms: Monomials = {}
    g = len(groups)
    for r in range(1, g + 1):
        for combo in combinations(range(g), r):
            union: FrozenSet[int] = frozenset().union(*(groups[i] for i in combo))
            coeff = (-1) ** (r + 1)
            terms[union] = terms.get(union, 0) + coeff
    return SparsePoly(n, {S: c for S, c in terms.items() if c != 0})


def or_poly(n: int) -> SparsePoly:
    """OR di tutte le n variabili via inclusione-esclusione: 2^n − 1 monomi.
    DENSO → il metodo veloce non guadagna nulla (≈ forza bruta). #SAT = 2^n − 1."""
    terms: Monomials = {}
    for r in range(1, n + 1):
        for combo in combinations(range(n), r):
            terms[frozenset(combo)] = (-1) ** (r + 1)
    return SparsePoly(n, terms)
