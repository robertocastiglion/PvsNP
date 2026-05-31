"""
DPLL con misura della dimensione della prova (refutazione tree-like).

DPLL (Davis–Putnam–Logemann–Loveland) decide la soddisfacibilità di una CNF per
ramificazione + propagazione unitaria. Il fatto chiave per la *proof
complexity*: quando DPLL conclude INSODD., **l'albero di ricerca che ha
percorso È una refutazione per resolution di tipo tree-like**. Quindi il numero
di nodi dell'albero è una misura concreta — e dimostrabile — della dimensione di
una prova resolution della formula.

Misuriamo esattamente quel numero. Sulla piccionaia PHP^(n+1)_n cresce in modo
**esponenziale**: non è un difetto del nostro codice, è il teorema di Haken
(1985) che si manifesta sotto gli occhi.
"""
from __future__ import annotations

import time
from dataclasses import dataclass

from .formula import CNF, Clause


@dataclass(frozen=True)
class DpllResult:
    """Esito di una decisione DPLL, con le metriche di costo."""

    satisfiable: bool
    tree_nodes: int        # nodi dell'albero di ricerca = dimensione prova tree-like
    decisions: int         # quante variabili sono state "indovinate" (branch)
    seconds: float
    aborted: bool = False  # interrotto per budget di nodi/tempo

    def pretty(self) -> str:
        sat = "SODDISFACIBILE" if self.satisfiable else "INSODDISFACIBILE"
        flag = "  [INTERROTTO: budget superato]" if self.aborted else ""
        return (
            f"{sat} — nodi albero: {self.tree_nodes}, "
            f"decisioni: {self.decisions}, {self.seconds*1000:.1f} ms{flag}"
        )


def _simplify(clauses: list[Clause], lit: int) -> list[Clause]:
    """Semplifica `clauses` assumendo `lit` vero.

    Le clausole che contengono `lit` sono soddisfatte (si tolgono); da quelle
    che contengono `-lit` si toglie quel letterale (diventa falso).
    """
    out: list[Clause] = []
    neg = -lit
    for c in clauses:
        if lit in c:
            continue
        if neg in c:
            out.append(c - {neg})
        else:
            out.append(c)
    return out


class _Budget(Exception):
    """Segnala il superamento del budget di nodi/tempo."""


def dpll(cnf: CNF, node_budget: int | None = None,
         time_budget: float | None = None) -> DpllResult:
    """Decide la CNF con DPLL, contando i nodi dell'albero di ricerca.

    `node_budget` / `time_budget` (secondi) interrompono la ricerca: utile per
    mostrare che oltre una certa taglia la prova è semplicemente troppo grande.
    """
    state = {"nodes": 0, "decisions": 0}
    start = time.perf_counter()
    empty: Clause = frozenset()

    def rec(clauses: list[Clause]) -> bool:
        state["nodes"] += 1
        if node_budget is not None and state["nodes"] > node_budget:
            raise _Budget
        if time_budget is not None and time.perf_counter() - start > time_budget:
            raise _Budget

        # propagazione unitaria (BCP)
        while True:
            if empty in clauses:
                return False
            if not clauses:
                return True
            unit = next((next(iter(c)) for c in clauses if len(c) == 1), None)
            if unit is None:
                break
            clauses = _simplify(clauses, unit)

        # scelta della variabile di branch: prima della prima clausola
        lit = next(iter(clauses[0]))
        var = abs(lit)
        state["decisions"] += 1
        if rec(_simplify(clauses, var)):
            return True
        return rec(_simplify(clauses, -var))

    aborted = False
    try:
        sat = rec(list(cnf.clauses))
    except _Budget:
        sat = False
        aborted = True

    return DpllResult(
        satisfiable=sat,
        tree_nodes=state["nodes"],
        decisions=state["decisions"],
        seconds=time.perf_counter() - start,
        aborted=aborted,
    )
