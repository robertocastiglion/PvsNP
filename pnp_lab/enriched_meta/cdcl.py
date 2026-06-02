"""Un solver CDCL da zero — per spingere la sintesi-SAT fino a n=4.

Il DPLL naïf del Modulo 5 misura la refutazione tree-resolution (è il suo scopo),
ma è troppo debole per *risolvere* le istanze di sintesi a n=4. Qui un CDCL
(Conflict-Driven Clause Learning) completo e zero-dipendenze:

  • literali interi con segno (come il Modulo 5);
  • BCP con literali sorvegliati (2-watched);
  • analisi del conflitto 1-UIP + backjump non cronologico;
  • euristica VSIDS + restart di Luby.

Uso previsto: ORACOLO di decisione veloce per calcolare la dimensione di circuito
a n=4 (lato SAT). NON ridefinisce la lente "dimostrare" (che resta la refutazione
tree-resolution del Modulo 5): il conteggio di conflitti del CDCL è un proxy di
refutazione *general resolution*, riportato a parte.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional

from pnp_lab.proof_complexity import CNF


@dataclass
class CdclResult:
    satisfiable: bool
    model: Optional[Dict[int, bool]]    # var -> bool, se SAT
    conflicts: int                       # # conflitti = proxy refutazione gen-resolution
    decisions: int
    learned: int
    restarts: int


def _luby(x: int) -> int:
    """Valore di Luby all'indice x (0-based): 1,1,2,1,1,2,4,1,1,2,1,1,2,4,8,…"""
    size, seq = 1, 0
    while size < x + 1:
        seq += 1
        size = 2 * size + 1
    while size - 1 != x:
        size = (size - 1) // 2
        seq -= 1
        x = x % size
    return 1 << seq


def solve(cnf: CNF, conflict_budget: Optional[int] = None,
          decide=None) -> CdclResult:
    """Decide la CNF con CDCL. ``conflict_budget`` interrompe (→ UNSAT/abort).

    ``decide`` (opzionale) è la POLICY DI BRANCHING: una funzione
    ``(unassigned: list[int], activity: dict[int,float], nvars: int) → int`` che
    ritorna il literale (con segno) su cui ramificare. Se ``None`` si usa VSIDS.
    Questo è l'aggancio per la strada #3 (policy alternative: random, LLM, RL).
    """
    clauses: List[List[int]] = [list(c) for c in cnf.clauses]

    # clausola vuota = insoddisfacibile subito
    if any(len(c) == 0 for c in clauses):
        return CdclResult(False, None, 0, 0, 0, 0)

    value: Dict[int, Optional[bool]] = {}      # var -> True/False/None
    level: Dict[int, int] = {}
    antecedent: Dict[int, Optional[int]] = {}  # var -> indice clausola (None = decisione)
    trail: List[int] = []                       # literali assegnati, in ordine
    trail_lim: List[int] = []                   # confini dei livelli
    activity: Dict[int, float] = {}
    var_inc = [1.0]
    decay = 0.95

    nvars = cnf.num_vars
    for v in range(1, nvars + 1):
        value[v] = None
        activity[v] = 0.0

    # literali sorvegliati: per ogni clausola, i primi due elementi sono i watched
    watches: Dict[int, List[int]] = {}

    def watch(lit: int, ci: int) -> None:
        watches.setdefault(lit, []).append(ci)

    units: List[int] = []
    for ci, c in enumerate(clauses):
        if len(c) == 1:
            units.append(c[0])
        else:
            watch(c[0], ci)
            watch(c[1], ci)

    def lit_val(lit: int) -> Optional[bool]:
        v = value[abs(lit)]
        if v is None:
            return None
        return v if lit > 0 else (not v)

    def enqueue(lit: int, ante: Optional[int]) -> None:
        var = abs(lit)
        value[var] = (lit > 0)
        level[var] = len(trail_lim)
        antecedent[var] = ante
        trail.append(lit)

    def bump(var: int) -> None:
        activity[var] += var_inc[0]
        if activity[var] > 1e100:
            for u in activity:
                activity[u] *= 1e-100
            var_inc[0] *= 1e-100

    stats = {"conflicts": 0, "decisions": 0, "learned": 0, "restarts": 0}

    def propagate() -> Optional[int]:
        """Propagazione unitaria. Ritorna l'indice della clausola in conflitto o None."""
        head = len(trail)
        # processa tutta la coda corrente
        qi = _qi[0]
        while qi < len(trail):
            p = trail[qi]
            qi += 1
            neg = -p                       # literale diventato falso
            wl = watches.get(neg, [])
            i = 0
            new_wl: List[int] = []
            conflict = None
            while i < len(wl):
                ci = wl[i]
                i += 1
                c = clauses[ci]
                # assicura che c[1] sia il watched falso
                if c[0] == neg:
                    c[0], c[1] = c[1], c[0]
                # se c[0] è vero, la clausola è soddisfatta: resta a sorvegliare neg
                if lit_val(c[0]) is True:
                    new_wl.append(ci)
                    continue
                # cerca un nuovo literale da sorvegliare (non falso) tra c[2:]
                found = False
                for k in range(2, len(c)):
                    if lit_val(c[k]) is not False:
                        c[1], c[k] = c[k], c[1]
                        watch(c[1], ci)
                        found = True
                        break
                if found:
                    continue
                # nessun rimpiazzo: c[1]=neg falso, c[0] è l'unico
                new_wl.append(ci)
                v0 = lit_val(c[0])
                if v0 is False:
                    conflict = ci
                    # conserva i watcher restanti
                    new_wl.extend(wl[i:])
                    break
                else:                       # c[0] è None → unit
                    enqueue(c[0], ci)
            watches[neg] = new_wl
            if conflict is not None:
                _qi[0] = qi
                return conflict
        _qi[0] = qi
        return None

    _qi = [0]

    for lit in units:
        v = lit_val(lit)
        if v is False:
            return CdclResult(False, None, 0, 0, 0, 0)
        if v is None:
            enqueue(lit, None)

    def analyze(conflict_ci: int):
        """1-UIP (forma canonica): ritorna (clausola appresa, livello di backjump).

        learnt[0] = literale asserente (UIP negato); learnt[1] = literale di livello
        più alto tra i restanti (sorvegliato per la propagazione dopo il backjump).
        """
        learnt: List[int] = [0]            # segnaposto per l'asserente
        seen = set()
        counter = 0
        p: Optional[int] = None
        cur = conflict_ci
        idx = len(trail) - 1
        dl = len(trail_lim)
        while True:
            c = clauses[cur]
            for q in c:
                if p is not None and q == p:   # salta il literale appena risolto
                    continue
                var = abs(q)
                if var not in seen and level.get(var, 0) > 0:
                    seen.add(var)
                    bump(var)
                    if level[var] >= dl:
                        counter += 1
                    else:
                        learnt.append(q)
            while abs(trail[idx]) not in seen:
                idx -= 1
            p = trail[idx]
            idx -= 1
            seen.discard(abs(p))
            counter -= 1
            if counter <= 0:
                break
            cur = antecedent[abs(p)]       # qui p non è UIP né decisione ⇒ non None
        learnt[0] = -p
        if len(learnt) == 1:
            return learnt, 0
        # porta in posizione 1 il literale di livello più alto (oltre l'asserente)
        mi = max(range(1, len(learnt)), key=lambda k: level[abs(learnt[k])])
        learnt[1], learnt[mi] = learnt[mi], learnt[1]
        return learnt, level[abs(learnt[1])]

    def backjump(to_level: int) -> None:
        while len(trail_lim) > to_level:
            start = trail_lim.pop()
            while len(trail) > start:
                q = trail.pop()
                value[abs(q)] = None
        _qi[0] = len(trail)

    luby_i = 0
    restart_base = 100
    conflicts_since_restart = 0

    # propagazione iniziale (livello 0)
    if propagate() is not None:
        return CdclResult(False, None, stats["conflicts"], 0, 0, 0)

    while True:
        conflict = propagate()
        if conflict is not None:
            stats["conflicts"] += 1
            conflicts_since_restart += 1
            if len(trail_lim) == 0:
                return CdclResult(False, None, stats["conflicts"], stats["decisions"],
                                  stats["learned"], stats["restarts"])
            learnt, bj = analyze(conflict)
            backjump(bj)
            ci = len(clauses)
            clauses.append(learnt)
            stats["learned"] += 1
            if len(learnt) == 1:
                enqueue(learnt[0], None)
            else:
                watch(learnt[0], ci)
                watch(learnt[1], ci)
                enqueue(learnt[0], ci)
            var_inc[0] /= decay
            if conflict_budget is not None and stats["conflicts"] > conflict_budget:
                return CdclResult(False, None, stats["conflicts"], stats["decisions"],
                                  stats["learned"], stats["restarts"])
            if conflicts_since_restart >= restart_base * _luby(luby_i):
                luby_i += 1
                conflicts_since_restart = 0
                stats["restarts"] += 1
                backjump(0)
        else:
            if decide is None:
                # scelta della variabile (VSIDS), polarità positiva
                best, best_act = None, -1.0
                for v in range(1, nvars + 1):
                    if value[v] is None and activity[v] > best_act:
                        best, best_act = v, activity[v]
                if best is None:
                    model = {v: bool(value[v]) for v in range(1, nvars + 1)}
                    return CdclResult(True, model, stats["conflicts"], stats["decisions"],
                                      stats["learned"], stats["restarts"])
                lit = best
            else:
                # policy di branching pluggable (strada #3)
                unassigned = [v for v in range(1, nvars + 1) if value[v] is None]
                if not unassigned:
                    model = {v: bool(value[v]) for v in range(1, nvars + 1)}
                    return CdclResult(True, model, stats["conflicts"], stats["decisions"],
                                      stats["learned"], stats["restarts"])
                lit = decide(unassigned, activity, nvars)
            trail_lim.append(len(trail))
            stats["decisions"] += 1
            enqueue(lit, None)
