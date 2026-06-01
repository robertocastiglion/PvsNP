"""MCSP — il Minimum Circuit Size Problem, calcolato in modo ESATTO.

MCSP: dato la tabella di verità di una funzione booleana (lunghezza N = 2^n) e un
parametro s, decidere se f ha un circuito (qui: una formula) di dimensione ≤ s.
È il problema centrale della META-COMPLESSITÀ: la complessità di *calcolare la
complessità*. Riusiamo il Modulo 6, che dà la dimensione di formula MINIMA esatta
di ogni funzione (e una formula ottima come testimone).

  • MCSP ∈ NP: il testimone è il circuito piccolo; la verifica è valutarlo su
    tutti gli N = 2^n input e confrontarlo con la tabella — poly in N.
  • La sua durezza è ignota e centrale: se MCSP fosse facile crollerebbero i
    generatori pseudo-casuali (e con essi la barriera Natural Proofs, Modulo 1).

Onestà: qui calcoliamo MCSP ESATTAMENTE su n piccolo (riuso del Modulo 6). La
questione "MCSP è NP-hard? / in P?" è aperta e la CITIAMO.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Tuple

from pnp_lab.circuits import ComplexityTable, min_formula_sizes


def complexity_map(n: int, cap: int = 60) -> ComplexityTable:
    """La complessità di formula esatta di ogni funzione su n variabili (Modulo 6)."""
    return min_formula_sizes(n, cap)


def mcsp_decide(ct: ComplexityTable, truth_table: int, s: int) -> bool:
    """MCSP[s](f): la funzione `truth_table` ha una formula di dimensione ≤ s?"""
    return ct.cost[truth_table] <= s


def mcsp_witness(ct: ComplexityTable, truth_table: int) -> Tuple[int, str]:
    """Per un'istanza YES: (dimensione minima, formula ottima) — il testimone NP."""
    return ct.cost[truth_table], ct.expr[truth_table]


@dataclass
class NPCertificate:
    input_length_N: int       # N = 2^n  (lunghezza della tabella = input di MCSP)
    witness_size: int         # dimensione del circuito-testimone
    verify_evaluations: int   # quante valutazioni servono = N
    poly_in_N: bool           # la verifica è polinomiale in N?


def np_certificate(n: int, s: int) -> NPCertificate:
    """Mostra che MCSP ∈ NP: testimone = circuito ≤ s, verifica = N valutazioni."""
    N = 1 << n
    return NPCertificate(input_length_N=N, witness_size=s, verify_evaluations=N, poly_in_N=True)


@dataclass
class ThresholdRow:
    s: int
    easy: int        # funzioni con dimensione ≤ s  (istanze YES)
    hard: int        # funzioni con dimensione > s   (istanze NO)
    total: int

    @property
    def hard_fraction(self) -> float:
        return self.hard / self.total


def mcsp_threshold(ct: ComplexityTable) -> List[ThresholdRow]:
    """Per ogni soglia s: quante funzioni sono 'facili' (≤ s) vs 'difficili' (> s).

    Si vede il messaggio di Shannon (Modulo 6): per s sotto il massimo, la
    stragrande maggioranza delle funzioni è DURA — eppure non sappiamo esibirne
    una esplicita e dimostrabilmente dura. È il cuore di MCSP.
    """
    total = ct.num_functions
    costs = list(ct.cost.values())
    rows: List[ThresholdRow] = []
    for s in range(0, ct.max_cost + 1):
        easy = sum(1 for c in costs if c <= s)
        rows.append(ThresholdRow(s=s, easy=easy, hard=total - easy, total=total))
    return rows
