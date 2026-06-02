"""Sintesi esatta di circuiti come SAT — il cardine della lente "dimostrare".

Per riparare il Modulo 14 verso (S) servono lenti su un'UNICA misura e una lente
"dimostrare" che non sia tautologica. Qui la misura è la **dimensione di circuito
in base De Morgan** (gate binari ∧/∨, negazione degli input gratuita, fan-out
libero = DAG), e la lente "dimostrare" è la **vera lunghezza di refutazione** di
un lower bound.

Idea (encoding standard di *exact synthesis*): "∃ circuito di ≤ s gate che calcola
f" è una CNF; è UNSAT esattamente quando $\text{size}(f) > s$. Allora:
  • calcolare  → il più piccolo s con CNF soddisfacibile  (SAT incrementale);
  • dimostrare → la lunghezza della refutazione della CNF a s = size−1  (UNSAT),
    misurata dal DPLL del Modulo 5 (= refutazione tree-resolution).

Niente più conteggio brute-force: questa è la proof complexity del lower bound in
un sistema di prova fissato (resolution tree-like).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Tuple

from pnp_lab.proof_complexity import CNF, dpll


# ── encoding "∃ circuito di s gate che calcola tt" ────────────────────────

def circuit_exists_cnf(tt: int, n: int, s: int) -> CNF:
    """CNF soddisfacibile sse esiste un circuito De Morgan di ≤ s gate per ``tt``.

    Sorgenti di valore (1-based): id 1..n = variabili d'ingresso; id n+k = uscita
    del gate k. Il gate i (1..s) sceglie due sorgenti in {1..n+i−1}, ciascuna con
    una negazione libera, e un operatore ∧/∨. L'uscita del gate s deve valere tt.
    """
    if s < 1:
        raise ValueError("s >= 1 (il caso s=0 = letterale è gestito a parte)")
    N = 1 << n
    cnt = [0]

    def new() -> int:
        cnt[0] += 1
        return cnt[0]

    clauses: List[frozenset] = []
    val: Dict[Tuple[int, int], int] = {}
    for i in range(1, s + 1):
        for t in range(N):
            val[(i, t)] = new()

    selL: Dict[Tuple[int, int], int] = {}
    selR: Dict[Tuple[int, int], int] = {}
    negL: Dict[int, int] = {}
    negR: Dict[int, int] = {}
    op: Dict[int, int] = {}
    Lval: Dict[Tuple[int, int], int] = {}
    Rval: Dict[Tuple[int, int], int] = {}
    for i in range(1, s + 1):
        pool = list(range(1, n + i))          # sorgenti disponibili al gate i
        for p in pool:
            selL[(i, p)] = new()
            selR[(i, p)] = new()
        negL[i] = new(); negR[i] = new(); op[i] = new()
        for t in range(N):
            Lval[(i, t)] = new(); Rval[(i, t)] = new()

    def srcval(p: int, t: int):
        if p <= n:
            return ("const", (t >> (p - 1)) & 1)
        return ("var", val[(p - n, t)])

    def exactly_one(vs: List[int]) -> None:
        clauses.append(frozenset(vs))
        for a in range(len(vs)):
            for b in range(a + 1, len(vs)):
                clauses.append(frozenset({-vs[a], -vs[b]}))

    def input_link(sel: int, lv: int, ng: int, sv) -> None:
        # sel → ( lv ↔ (srcval XOR ng) )
        if sv[0] == "const":
            if sv[1] == 0:                    # lv ↔ ng
                clauses.append(frozenset({-sel, -lv, ng}))
                clauses.append(frozenset({-sel, lv, -ng}))
            else:                              # lv ↔ ¬ng
                clauses.append(frozenset({-sel, -lv, -ng}))
                clauses.append(frozenset({-sel, lv, ng}))
        else:
            g = sv[1]                          # lv ⊕ g ⊕ ng = 0  (parità pari)
            clauses.append(frozenset({-sel, -lv, g, ng}))
            clauses.append(frozenset({-sel, lv, -g, ng}))
            clauses.append(frozenset({-sel, lv, g, -ng}))
            clauses.append(frozenset({-sel, -lv, -g, -ng}))

    # (op,L,R) → val :  op=0 AND, op=1 OR
    _combos = [
        (0, 0, 0, 0), (0, 0, 1, 0), (0, 1, 0, 0), (0, 1, 1, 1),
        (1, 0, 0, 0), (1, 0, 1, 1), (1, 1, 0, 1), (1, 1, 1, 1),
    ]

    def gate_op(o_var: int, L: int, R: int, v: int) -> None:
        for (o, l, r, vt) in _combos:
            lits = {
                (-o_var if o == 1 else o_var),
                (-L if l == 1 else L),
                (-R if r == 1 else R),
                (v if vt == 1 else -v),
            }
            clauses.append(frozenset(lits))

    for i in range(1, s + 1):
        pool = list(range(1, n + i))
        exactly_one([selL[(i, p)] for p in pool])
        exactly_one([selR[(i, p)] for p in pool])
        for t in range(N):
            for p in pool:
                sv = srcval(p, t)
                input_link(selL[(i, p)], Lval[(i, t)], negL[i], sv)
                input_link(selR[(i, p)], Rval[(i, t)], negR[i], sv)
            gate_op(op[i], Lval[(i, t)], Rval[(i, t)], val[(i, t)])

    for t in range(N):
        v = val[(s, t)]
        clauses.append(frozenset({v if (tt >> t) & 1 else -v}))

    return CNF(clauses=clauses, num_vars=cnt[0], name=f"circ-exists n={n} s={s}")


# ── la misura condivisa: dimensione di circuito esatta via SAT ────────────

def _is_literal(tt: int, n: int) -> bool:
    """tt è una variabile o la sua negazione (dimensione 0)."""
    for j in range(1, n + 1):
        proj = 0
        for t in range(1 << n):
            if (t >> (j - 1)) & 1:
                proj |= 1 << t
        if tt == proj or tt == (proj ^ ((1 << (1 << n)) - 1)):
            return True
    return False


@dataclass
class SizeResult:
    truth_table: int
    n: int
    size: int                 # dimensione di circuito esatta (gate)
    capped: bool              # True se ha toccato il cap senza trovare un circuito


def circuit_size(tt: int, n: int, cap: int = 6,
                 node_budget: int = 200_000) -> SizeResult:
    """Dimensione di circuito De Morgan esatta: il più piccolo s con CNF SAT.

    La ricerca sale da s=1: gli SAT (s ≥ size) si trovano in fretta (DPLL esibisce
    un modello), gli UNSAT (s < size) richiedono una refutazione completa che può
    esplodere — in quel caso il budget la interrompe e si sale comunque, perché per
    trovare il *minimo* basta il primo SAT.
    """
    if _is_literal(tt, n):
        return SizeResult(tt, n, 0, False)
    for s in range(1, cap + 1):
        if dpll(circuit_exists_cnf(tt, n, s), node_budget=node_budget).satisfiable:
            return SizeResult(tt, n, s, False)
    return SizeResult(tt, n, cap, True)


def circuit_size_cdcl(tt: int, n: int, cap: int = 12,
                      conflict_budget: int = 200_000) -> SizeResult:
    """Come ``circuit_size`` ma con il solver CDCL — abbastanza forte da arrivare
    a n=4 (il DPLL naïf del Modulo 5 esplode già su molte funzioni di n=3).

    Si usa CDCL come *oracolo di decisione* per la misura; la lente "dimostrare"
    (refutazione tree-resolution) resta affidata a ``refutation_length``.
    """
    from .cdcl import solve
    if _is_literal(tt, n):
        return SizeResult(tt, n, 0, False)
    for s in range(1, cap + 1):
        if solve(circuit_exists_cnf(tt, n, s), conflict_budget=conflict_budget).satisfiable:
            return SizeResult(tt, n, s, False)
    return SizeResult(tt, n, cap, True)


# ── la lente "dimostrare": lunghezza di refutazione del lower bound ───────

@dataclass
class ProofResult:
    truth_table: int
    n: int
    threshold: int            # s tale che il lower bound è "size > s"
    refutation_nodes: int     # lunghezza della refutazione tree-resolution
    aborted: bool             # budget superato (= prova troppo lunga)
    is_lower_bound: bool      # la CNF a s era davvero UNSAT (lower bound vero)


def refutation_length(tt: int, n: int, s: int,
                      node_budget: int = 200_000) -> ProofResult:
    """Lunghezza della refutazione di 'size(tt) > s' nel sistema resolution.

    Costruisce la CNF di esistenza a taglia s e la refuta con DPLL (Modulo 5). Se
    la CNF è soddisfacibile non c'è lower bound a quella soglia. Se è UNSAT, il
    numero di nodi è la dimensione (tree-like) della prova; ``aborted`` segnala
    che la prova eccede il budget — cioè il lower bound è duro da dimostrare.
    """
    res = dpll(circuit_exists_cnf(tt, n, s), node_budget=node_budget)
    return ProofResult(
        truth_table=tt,
        n=n,
        threshold=s,
        refutation_nodes=res.tree_nodes,
        aborted=res.aborted,
        is_lower_bound=(not res.satisfiable) and (not res.aborted),
    )
