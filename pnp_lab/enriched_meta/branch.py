"""Strada #3: policy di branching pluggabili per il CDCL (Modulo 11 ↔ CDCL).

Il CDCL del Modulo 1 (enriched_meta) decide su quale variabile ramificare con
l'euristica VSIDS. La domanda di ricerca aperta (stile AlphaProof / Modulo 11):
una policy più intelligente — appresa, o un LLM — guida meglio la ricerca di
refutazioni sulle istanze UNSAT dure?

Qui forniamo l'AGGANCIO: una policy è una funzione
``(unassigned, activity, nvars) → literale``. Diamo alcune policy concrete e una
``LLMBranchPolicy`` OPZIONALE e pluggable (stile `proof_search.LLMPolicy`): mai nel
percorso di correttezza (il CDCL resta sound qualunque sia la scelta), nessuna
dipendenza da reti o chiavi, fallback all'euristica se il modello non risponde.

PREDIZIONE TEORICA (onesta). Nessuna policy può rendere FACILE un'istanza UNSAT la
cui refutazione resolution è esponenzialmente lunga: il numero di conflitti del
CDCL è limitato INFERIORMENTE dalla dimensione della refutazione (general
resolution), che è una proprietà del *sistema di prova*, non del branching. Quindi
un LLM-oracolo può cambiare le costanti, non la barriera. Lo misuriamo.
"""

from __future__ import annotations

import random
from dataclasses import dataclass
from typing import Callable, Dict, List, Optional

from pnp_lab.proof_complexity import CNF
from .cdcl import CdclResult, solve

#: una policy di branching: (variabili libere, attività, n) → literale con segno
BranchPolicy = Callable[[List[int], Dict[int, float], int], int]


def vsids_policy(unassigned: List[int], activity: Dict[int, float], nvars: int) -> int:
    """VSIDS esplicito: la variabile libera di attività massima, polarità positiva."""
    best, best_act = unassigned[0], -1.0
    for v in unassigned:
        if activity[v] > best_act:
            best, best_act = v, activity[v]
    return best


def static_policy(unassigned: List[int], activity: Dict[int, float], nvars: int) -> int:
    """Ordine statico: la variabile libera di indice minimo."""
    return min(unassigned)


def random_policy(seed: int = 0) -> BranchPolicy:
    """Policy casuale (seedata): variabile e polarità a caso. Baseline 'cieca'."""
    rng = random.Random(seed)

    def pol(unassigned: List[int], activity: Dict[int, float], nvars: int) -> int:
        v = rng.choice(unassigned)
        return v if rng.random() < 0.5 else -v
    return pol


@dataclass
class LLMBranchPolicy:
    """Policy di branching guidata da un modello, OPZIONALE e pluggable.

    `call_fn` è fornita dall'utente (es. una chiamata a un LLM) e prende il prompt,
    restituendo testo; `parse` ne estrae una variabile. Se `call_fn` è None o il
    parsing fallisce, si ricade su VSIDS. Il core del CDCL NON dipende da questa
    classe: la correttezza è garantita comunque (proprio come `proof_search.LLMPolicy`).
    """
    call_fn: Optional[Callable[[str], str]] = None

    def build_prompt(self, unassigned: List[int], activity: Dict[int, float]) -> str:
        top = sorted(unassigned, key=lambda v: -activity[v])[:20]
        items = ", ".join(f"x{v}(act={activity[v]:.2f})" for v in top)
        return ("Sei una policy di branching per un solver SAT. Variabili libere "
                f"(prime per attività): {items}. Rispondi col solo numero della "
                "variabile su cui ramificare.")

    def parse(self, response: str, unassigned: List[int]) -> Optional[int]:
        digits = "".join(c if c.isdigit() else " " for c in response).split()
        for tok in digits:
            v = int(tok)
            if v in unassigned:
                return v
        return None

    def __call__(self, unassigned: List[int], activity: Dict[int, float], nvars: int) -> int:
        if self.call_fn is not None:
            try:
                v = self.parse(self.call_fn(self.build_prompt(unassigned, activity)), unassigned)
                if v is not None:
                    return v
            except Exception:
                pass
        return vsids_policy(unassigned, activity, nvars)   # fallback


@dataclass
class PolicyResult:
    name: str
    satisfiable: bool
    conflicts: int
    decisions: int
    aborted: bool


def compare_policies(cnf: CNF, policies: Dict[str, Optional[BranchPolicy]],
                     conflict_budget: int = 200_000) -> List[PolicyResult]:
    """Esegue il CDCL con ogni policy sulla STESSA CNF e confronta i conflitti.

    `None` come policy = VSIDS di default. ``aborted`` = budget di conflitti
    superato (l'istanza è troppo dura per quella policy entro il budget)."""
    out: List[PolicyResult] = []
    for name, pol in policies.items():
        r: CdclResult = solve(cnf, conflict_budget=conflict_budget, decide=pol)
        aborted = (not r.satisfiable) and r.conflicts > conflict_budget
        out.append(PolicyResult(name=name, satisfiable=r.satisfiable,
                                conflicts=r.conflicts, decisions=r.decisions,
                                aborted=aborted))
    return out


@dataclass
class BranchFinding:
    headline: str
    measured: str
    theory: str
    honest_limit: str


def branch_summary() -> BranchFinding:
    return BranchFinding(
        headline="Una policy di branching (anche un LLM-oracolo) cambia le costanti, "
                 "non la barriera: sulle istanze UNSAT dure tutte esplodono.",
        measured="confronto VSIDS / statica / casuale / LLM-pluggable sui conflitti, "
                 "sulla STESSA istanza di sintesi.",
        theory="il numero di conflitti del CDCL è ≥ la dimensione della refutazione "
               "(general resolution), proprietà del SISTEMA DI PROVA, indipendente dal "
               "branching: nessuna policy rende facile un'istanza con refutazione "
               "esponenziale (proof complexity ≠ euristica di ricerca).",
        honest_limit="l'LLM è uno stub pluggable (nessun modello reale chiamato nei test); "
                     "il core CDCL resta sound con qualunque policy. Conferma una barriera "
                     "nota, nessun risultato nuovo.",
    )
