"""Il difetto di composizione: le tre lenti sono la STESSA freccia o no?

Misura, su tutti gli oggetti di C (n piccolo, esatto), quanto due lenti
dis-accordano. È l'esperimento che discrimina la tesi forte:

  difetto(A,B) = frazione di funzioni su cui il verdetto di A ≠ verdetto di B.

  • difetto = 0  ⇒  le due lenti coincidono = EQUIVALENZA stretta (stessa freccia).
  • difetto > 0  ⇒  relazione LASSA (profuntore/span, non isomorfismo).

Risultati attesi (e poi misurati):
  - RICONOSCERE ⟺ APPRENDERE: difetto 0 — l'isola di equivalenza (CIKK 2016).
  - CALCOLARE ↔ DIMOSTRARE: difetto chiudibile pagando budget di prova (→0).
  - CALCOLARE ↔ RICONOSCERE: difetto residuo irriducibile > 0 (barriera di
    località / Razborov–Rudich): nessuna proprietà costruttiva di questa famiglia
    riproduce il costo esatto, per quanto ben scelta la soglia.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Tuple

from pnp_lab.circuits import ComplexityTable
from .lenses import (
    LensVerdicts,
    evaluate_lenses,
    proof_length_for_threshold,
    total_influence,
)


def defect(a: Dict[int, bool], b: Dict[int, bool]) -> float:
    """Frazione di oggetti su cui due verdetti differiscono (distanza di Hamming)."""
    keys = a.keys()
    diff = sum(1 for k in keys if a[k] != b[k])
    return diff / len(keys)


@dataclass
class DefectMatrix:
    """Matrice 3×3 dei difetti tra le lenti, più i parametri usati."""

    s: int
    labels: Tuple[str, str, str]
    matrix: List[List[float]]
    theta: int
    proof_budget: int
    proof_length_needed: int

    def cell(self, a: str, b: str) -> float:
        i, j = self.labels.index(a), self.labels.index(b)
        return self.matrix[i][j]


def defect_matrix(verdicts: LensVerdicts) -> DefectMatrix:
    """Calcola tutti i difetti a coppie tra calcolare/dimostrare/riconoscere."""
    labels = ("calcolare", "dimostrare", "riconoscere")
    cols = {
        "calcolare": verdicts.compute,
        "dimostrare": verdicts.prove,
        "riconoscere": verdicts.recognize,
    }
    matrix = [[defect(cols[a], cols[b]) for b in labels] for a in labels]
    return DefectMatrix(
        s=verdicts.s,
        labels=labels,
        matrix=matrix,
        theta=verdicts.theta,
        proof_budget=verdicts.proof_budget,
        proof_length_needed=verdicts.proof_length_needed,
    )


# ── L'isola di equivalenza: RICONOSCERE ⟺ APPRENDERE (CIKK 2016) ──────────

@dataclass
class CikkIsland:
    """Round-trip riconoscere → apprendere → riconoscere."""

    learned_theta: int
    samples_used: int
    round_trip_defect: float    # atteso: 0.0 (equivalenza stretta)
    equivalent: bool


def learn_property(ct: ComplexityTable, recognize: Dict[int, bool]) -> int:
    """Apprende la soglia della proprietà 'riconoscere' dai campioni etichettati.

    La proprietà è un concetto-soglia su una feature costruttiva (l'influenza
    totale). Un learner che osserva (feature(f), etichetta(f)) recupera la soglia:
    è la direzione 'proprietà naturale ⇒ algoritmo di apprendimento' di
    Carmosino–Impagliazzo–Kabanets–Kolokolova 2016, resa eseguibile.
    """
    n = ct.n
    pos = [total_influence(t, n) for t, lab in recognize.items() if lab]
    neg = [total_influence(t, n) for t, lab in recognize.items() if not lab]
    if not pos:
        return (max(neg) if neg else 0) + 1     # nessun positivo: soglia oltre tutto
    if not neg:
        return min(pos) - 1                      # tutti positivi
    # soglia coerente: sotto il minimo dei positivi, dal massimo dei negativi
    return max(neg) if max(neg) < min(pos) else min(pos) - 1


def cikk_island(ct: ComplexityTable, verdicts: LensVerdicts) -> CikkIsland:
    """Verifica eseguibile dell'equivalenza riconoscere ⟺ apprendere."""
    n = ct.n
    learned = learn_property(ct, verdicts.recognize)
    hypothesis = {t: (total_influence(t, n) > learned) for t in ct.cost}
    d = defect(verdicts.recognize, hypothesis)
    return CikkIsland(
        learned_theta=learned,
        samples_used=len(ct.cost),
        round_trip_defect=d,
        equivalent=(d == 0.0),
    )


# ── La curva del budget di prova: CALCOLARE ↔ DIMOSTRARE è chiudibile ──────

@dataclass
class BudgetPoint:
    budget: int
    defect_compute_prove: float
    certifies: bool             # il budget basta a dimostrare il lower bound?


def proof_budget_curve(ct: ComplexityTable, s: int,
                       budgets: List[int] | None = None) -> List[BudgetPoint]:
    """difetto(calcolare, dimostrare) al variare del budget di prova.

    Mostra la SOGLIA netta della proof complexity: sotto la lunghezza necessaria
    il lower bound è non dimostrato (difetto pieno), sopra crolla a 0. La lente
    'dimostrare' è quindi chiudibile su 'calcolare' pagando abbastanza — a
    differenza di 'riconoscere'.
    """
    n = ct.n
    needed = proof_length_for_threshold(s, n)
    if budgets is None:
        budgets = [needed // 1000, needed // 2, needed - 1, needed, needed * 2]
        budgets = sorted({max(0, b) for b in budgets})
    out: List[BudgetPoint] = []
    hard_fraction = sum(1 for t in ct.cost if ct.cost[t] > s) / len(ct.cost)
    for b in budgets:
        v = evaluate_lenses(ct, s, proof_budget=b, theta=verdicts_theta(ct, s))
        d = defect(v.compute, v.prove)
        out.append(BudgetPoint(budget=b, defect_compute_prove=d, certifies=(b >= needed)))
    return out


def verdicts_theta(ct: ComplexityTable, s: int) -> int:
    """Soglia θ ottimale riusata, per coerenza tra le chiamate."""
    from .lenses import best_recognize_threshold
    return best_recognize_threshold(ct, s)


# ── Il difetto irriducibile: CALCOLARE ↔ RICONOSCERE (la barriera) ────────

@dataclass
class IrreducibleGap:
    s: int
    best_theta: int
    residual_defect: float          # > 0 anche con la soglia migliore
    misclassified: int
    interpretation: str


def irreducible_recognize_gap(ct: ComplexityTable, s: int) -> IrreducibleGap:
    """Il difetto minimo tra 'calcolare' e la migliore proprietà costruttiva.

    Anche scegliendo la soglia ottimale, una proprietà naturale (influenza) NON
    riproduce il costo esatto: il residuo è la perdita strutturale. È la barriera
    natural-proofs / di località misurata in piccolo.
    """
    from .lenses import best_recognize_threshold, chi_recognize, chi_compute
    n = ct.n
    theta = best_recognize_threshold(ct, s)
    mis = sum(1 for t in ct.cost
              if chi_recognize(t, n, theta) != chi_compute(ct, t, s))
    d = mis / len(ct.cost)
    if d == 0.0:
        interp = ("a questo n/s la proprietà costruttiva combacia col costo esatto "
                  "(regime troppo piccolo perché la barriera si manifesti)")
    else:
        interp = ("difetto residuo > 0: nessuna soglia sull'influenza riproduce il "
                  "costo esatto ⇒ la lente 'riconoscere' NON arricchisce la stessa "
                  "freccia di 'calcolare' (barriera Razborov–Rudich / di località)")
    return IrreducibleGap(
        s=s, best_theta=theta, residual_defect=d, misclassified=mis, interpretation=interp,
    )
