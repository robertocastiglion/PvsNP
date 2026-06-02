"""#SAT esplicito per circuiti di PROFONDITÀ 2 (DNF), più veloce della forza bruta.

La precondizione del metodo di Williams è un algoritmo di #SAT per una classe di
circuiti *più veloce di 2^n*. Qui lo realizziamo per la classe debole esplicita
delle **DNF** (OR di AND = profondità 2), con tempi misurati.

Algoritmo (inclusione–esclusione sui termini). Sia la DNF un OR di m termini
T_1,…,T_m. Per il principio di inclusione–esclusione:

    |{x : DNF(x)=1}|  =  Σ_{∅≠S⊆[m]} (-1)^{|S|+1} · |{x : tutti i T_i (i∈S) veri}|

Un'intersezione "tutti i termini di S veri" fissa l'unione dei loro letterali: se
sono consistenti (nessuna variabile forzata 0 e 1) e fissano d variabili distinte,
i modelli sono 2^{n-d}; se sono contraddittori, 0. Costo: O(2^m · m) invece di
O(2^n · m). **Più veloce della forza bruta quando m < n** — il regime strutturato,
esattamente la precondizione del metodo algoritmico.

Onestà: è esatto (lo verifichiamo contro la forza bruta) ma guadagna solo quando i
termini sono pochi (DNF densa ⇒ nessun guadagno). L'algoritmo ACC⁰ di Williams
(2^{n-n^δ}) è una versione sofisticata della stessa idea — CITATO.
"""

from __future__ import annotations

import time
from dataclasses import dataclass
from itertools import combinations, product
from typing import Dict, List, Optional, Tuple

#: un letterale: (variabile, positivo?)
Literal = Tuple[int, bool]
#: un termine = AND di letterali; una DNF = OR di termini
Term = List[Literal]
DNF = List[Term]


def _term_true(term: Term, x: Tuple[int, ...]) -> bool:
    return all((x[v] == 1) == pos for v, pos in term)


def dnf_true(dnf: DNF, x: Tuple[int, ...]) -> bool:
    return any(_term_true(t, x) for t in dnf)


@dataclass
class CountResult:
    value: int
    seconds: float
    method: str


def count_sat_bruteforce(dnf: DNF, n: int) -> CountResult:
    """Forza bruta: enumera tutti i 2^n assegnamenti. O(2^n · m)."""
    t0 = time.perf_counter()
    total = sum(1 for x in product((0, 1), repeat=n) if dnf_true(dnf, x))
    return CountResult(total, time.perf_counter() - t0, "forza bruta (2^n)")


def _intersection_fixed(terms: List[Term]) -> Optional[int]:
    """Per un insieme di termini, i letterali della loro congiunzione: ritorna il
    numero di variabili fissate se consistenti, altrimenti None (contraddizione)."""
    forced: Dict[int, bool] = {}
    for t in terms:
        for v, pos in t:
            if v in forced and forced[v] != pos:
                return None
            forced[v] = pos
    return len(forced)


def count_sat_inclusion_exclusion(dnf: DNF, n: int) -> CountResult:
    """#SAT della DNF via inclusione–esclusione sui termini. O(2^m · m)."""
    t0 = time.perf_counter()
    m = len(dnf)
    total = 0
    for r in range(1, m + 1):
        sign = 1 if (r % 2 == 1) else -1
        for combo in combinations(range(m), r):
            d = _intersection_fixed([dnf[i] for i in combo])
            if d is not None:
                total += sign * (1 << (n - d))
    return CountResult(total, time.perf_counter() - t0, "inclusione-esclusione (2^m)")


def analytic_speedup(n: int, m: int) -> float:
    """Fattore analitico di speedup su una DNF con m termini: 2^n / 2^m."""
    return (1 << n) / (1 << m) if m <= n else (1 << n) / (1 << m)


# ── famiglie di DNF strutturate (per i benchmark) ─────────────────────────

def disjoint_terms_dnf(num_terms: int, term_width: int, n: int) -> DNF:
    """`num_terms` termini su gruppi di variabili DISGIUNTI (m fisso, piccolo).

    Classe debole strutturata: pochi termini, indipendenti da n. È il regime in cui
    l'inclusione–esclusione (2^m) stra-batte la forza bruta (2^n) al crescere di n.
    """
    dnf: DNF = []
    v = 0
    for _ in range(num_terms):
        term: Term = []
        for _ in range(term_width):
            term.append((v % n, True))
            v += 1
        dnf.append(term)
    return dnf


@dataclass
class BenchRow:
    n: int
    m: int
    brute_seconds: float
    ie_seconds: float
    speedup_measured: float       # tempo brute / tempo IE
    speedup_analytic: float       # 2^n / 2^m
    agree: bool                   # i due conteggi coincidono (correttezza)


def benchmark(num_terms: int, term_width: int, ns: List[int]) -> List[BenchRow]:
    """Confronta forza bruta vs inclusione–esclusione su una famiglia strutturata,
    misurando i TEMPI reali e verificando che i conteggi coincidano."""
    rows: List[BenchRow] = []
    for n in ns:
        dnf = disjoint_terms_dnf(num_terms, term_width, n)
        b = count_sat_bruteforce(dnf, n)
        ie = count_sat_inclusion_exclusion(dnf, n)
        rows.append(BenchRow(
            n=n, m=len(dnf),
            brute_seconds=b.seconds, ie_seconds=ie.seconds,
            speedup_measured=(b.seconds / ie.seconds if ie.seconds > 0 else float("inf")),
            speedup_analytic=analytic_speedup(n, len(dnf)),
            agree=(b.value == ie.value),
        ))
    return rows
