"""Il loop di proof-search: best-first guidato da una *policy* (proposer).

È lo scheletro di AlphaProof/LeanDojo, ridotto all'osso e onesto: una ricerca
best-first sullo spazio delle riscritture, dove una `policy` propone (e ordina)
le tattiche da provare. La "intelligenza" sta tutta nella policy: una policy
migliore trova la prova espandendo MENO nodi. Misuriamo esattamente questo —
nessuna promessa, solo nodi espansi e successo/fallimento entro un budget.

Il verificatore (engine) è SOUND: ogni prova restituita è una vera catena di
riscritture che porta `start` a `target`.
"""

from __future__ import annotations

import heapq
import time
from dataclasses import dataclass, field
from typing import Callable, Dict, List, Optional, Tuple

from .engine import Goal, Rule, Tactic, apply_tactic, distance, show

#: una policy: dato (termine corrente, target, regole) restituisce tattiche ordinate
Policy = Callable[["SearchState"], List[Tactic]]


@dataclass(frozen=True)
class SearchState:
    term: "object"          # il termine corrente (engine.Term)
    target: "object"        # il target (engine.Term)
    rules: Dict[str, Rule]


@dataclass
class SearchResult:
    goal: str
    success: bool
    proof: List[Tactic] = field(default_factory=list)   # la catena di tattiche
    nodes_expanded: int = 0
    generated: int = 0      # stati generati (= ramificazione impegnata dalla policy)
    max_frontier: int = 0
    seconds: float = 0.0

    @property
    def proof_length(self) -> int:
        return len(self.proof)


def search(goal: Goal, rules: Dict[str, Rule], policy: Policy, *,
           max_nodes: int = 4000) -> SearchResult:
    """Best-first search dello spazio delle riscritture, guidata da `policy`.

    Priorità = (passi fatti) + distanza(stato, target): A*-like con euristica.
    `policy` decide QUALI tattiche proporre da ogni stato e in che ordine — è il
    punto in cui si innesta un modello (LLM) o un'euristica.
    """
    t0 = time.perf_counter()
    start, target = goal.start, goal.target
    # frontiera: (priorità, contatore, termine, proof-path)
    counter = 0
    frontier: List[Tuple[int, int, object, List[Tactic]]] = [
        (distance(start, target), counter, start, [])
    ]
    visited = {show(start)}
    nodes = 0
    generated = 0
    max_frontier = 1

    while frontier:
        _, _, term, path = heapq.heappop(frontier)
        if term == target:
            return SearchResult(goal.name, True, path, nodes, generated, max_frontier,
                                time.perf_counter() - t0)
        if nodes >= max_nodes:
            break
        nodes += 1
        state = SearchState(term, target, rules)
        for tac in policy(state):
            nxt = apply_tactic(rules, term, tac)  # type: ignore[arg-type]
            if nxt is None:
                continue
            key = show(nxt)
            if key in visited:
                continue
            visited.add(key)
            counter += 1
            generated += 1
            g = len(path) + 1
            h = distance(nxt, target)
            heapq.heappush(frontier, (g + h, counter, nxt, path + [tac]))
        max_frontier = max(max_frontier, len(frontier))

    return SearchResult(goal.name, False, [], nodes, generated, max_frontier,
                        time.perf_counter() - t0)


def replay(goal: Goal, rules: Dict[str, Rule], proof: List[Tactic]) -> bool:
    """Riverifica una prova: applica la catena e controlla che porti a `target`.

    Indipendente dalla ricerca: è il controllo di SOUNDNESS della prova trovata.
    """
    term = goal.start
    for tac in proof:
        nxt = apply_tactic(rules, term, tac)  # type: ignore[arg-type]
        if nxt is None:
            return False
        term = nxt
    return term == goal.target
