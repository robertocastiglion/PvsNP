"""Circuiti AC0 concreti a livelli alternati ∧/∨ (profondità d, fan-in qualunque).

Il Modulo 8 «base» lavora su una singola DNF (profondità 2). Per iterare lo
switching *livello dopo livello* serve un vero circuito a profondità d. Qui lo
rappresentiamo in modo esplicito ed eseguibile:

  - il livello più basso è fatto di TERMINI AND su letterali, ognuno di larghezza
    ≤ w  (``bottom_fanin`` = w, la "larghezza al fondo" che lo switching controlla);
  - sopra si alternano livelli di porte ∨ e ∧ a fan-in qualunque, fino a un'unica
    porta di uscita.

Tutto è calcolato in modo ESATTO sulla tabella di verità (n piccolo): nessuna
approssimazione. Questo circuito è la "cavia" che il motore di switching iterato
(`iterate.py`) fa collassare un livello alla volta.
"""

from __future__ import annotations

import random
from dataclasses import dataclass
from typing import Callable, List, Sequence, Tuple

from .restriction import Term  # tuple di (var, want)

#: una porta interna = lista di indici nel livello precedente
Gate = List[int]
#: un livello interno = (operatore, lista di porte)
Layer = Tuple[str, List[Gate]]


@dataclass
class AC0Circuit:
    """Circuito AC0 a livelli alternati.

    - ``bottom``: lista di termini AND su letterali (il livello 1, di porte ∧).
    - ``layers``: livelli successivi, ciascuno ``(op, gates)`` con ``op`` in
      ``{"OR", "AND"}`` e ogni porta una lista di indici nel livello precedente.
      Il primo livello in ``layers`` legge ``bottom``; l'ultimo deve avere una
      sola porta (l'uscita). Gli operatori si alternano: ``bottom`` è AND, quindi
      ``layers[0]`` è OR, ``layers[1]`` AND, e così via.
    """

    n: int
    bottom: List[Term]
    layers: List[Layer]

    @property
    def depth(self) -> int:
        """Profondità = livello dei termini ∧ (1) + numero di livelli interni."""
        return 1 + len(self.layers)

    @property
    def bottom_fanin(self) -> int:
        """La larghezza w al fondo: massimo numero di letterali in un termine."""
        return max((len(t) for t in self.bottom), default=0)

    @property
    def size(self) -> int:
        """Numero totale di porte (termini al fondo + porte interne)."""
        return len(self.bottom) + sum(len(g) for _, g in self.layers)

    def evaluate(self, assignment: Sequence[int]) -> int:
        """Valuta il circuito su un assegnamento completo 0/1 di tutte le n variabili."""
        # livello 1: termini AND
        level = [
            1 if all((assignment[v] == 1) == want for (v, want) in term) else 0
            for term in self.bottom
        ]
        # livelli interni
        for op, gates in self.layers:
            if op == "OR":
                level = [1 if any(level[i] for i in g) else 0 for g in gates]
            elif op == "AND":
                level = [1 if all(level[i] for i in g) else 0 for g in gates]
            else:  # pragma: no cover - guardia
                raise ValueError(f"operatore sconosciuto: {op}")
        if len(level) != 1:
            raise ValueError("il livello di uscita deve avere esattamente una porta")
        return level[0]

    def truth_table(self) -> Tuple[int, ...]:
        """Tabella di verità completa, lunghezza 2^n (big-endian sulle variabili)."""
        out: List[int] = []
        for a in range(1 << self.n):
            assign = [(a >> (self.n - 1 - i)) & 1 for i in range(self.n)]
            out.append(self.evaluate(assign))
        return tuple(out)

    def as_evaluator(self) -> Callable[[Sequence[int]], int]:
        """Restituisce un valutatore compatibile con ``tabulate`` del modulo base."""
        return lambda a: self.evaluate(a)


def random_ac0(
    n: int,
    depth: int,
    bottom_fanin: int,
    rng: random.Random,
    *,
    bottom_terms: int = 8,
    fanin: int = 3,
) -> AC0Circuit:
    """Circuito AC0 casuale: profondità ``depth``, fan-in al fondo ``bottom_fanin``.

    I livelli si alternano OR/AND partendo dai termini ∧ del fondo; l'uscita è
    un'unica porta. ``bottom_terms`` termini al fondo, fan-in interno ``fanin``.
    """
    if depth < 2:
        raise ValueError("la profondità deve essere ≥ 2")
    w = min(bottom_fanin, n)
    bottom: List[Term] = []
    for _ in range(bottom_terms):
        vs = rng.sample(range(n), w)
        bottom.append(tuple((v, bool(rng.getrandbits(1))) for v in vs))

    layers: List[Layer] = []
    prev_count = len(bottom)
    # bottom è AND ⇒ il primo livello interno è OR, poi si alterna
    ops = ["OR" if i % 2 == 0 else "AND" for i in range(depth - 1)]
    for li, op in enumerate(ops):
        last = li == len(ops) - 1
        n_gates = 1 if last else max(2, prev_count // 2)
        gates: List[Gate] = []
        for _ in range(n_gates):
            k = min(prev_count, max(2, fanin))
            gates.append(rng.sample(range(prev_count), k))
        layers.append((op, gates))
        prev_count = n_gates
    return AC0Circuit(n=n, bottom=bottom, layers=layers)


def parity_as_dnf(n: int) -> AC0Circuit:
    """La parità come circuito AC0 canonico: una DNF (profondità 2).

    OR su TUTTI i 2^(n-1) mintermini di parità dispari, ciascun termine di
    larghezza n. Fan-in al fondo = n, dimensione = 2^(n-1): è proprio il "muro"
    — l'unica rappresentazione AC0 a profondità 2 della parità è enorme e larga.
    """
    bottom: List[Term] = []
    for a in range(1 << n):
        bits = [(a >> (n - 1 - i)) & 1 for i in range(n)]
        if sum(bits) & 1:  # parità dispari ⇒ mintermine vero
            bottom.append(tuple((i, bool(bits[i])) for i in range(n)))
    # un'unica porta OR su tutti i mintermini
    out_gate: Gate = list(range(len(bottom)))
    return AC0Circuit(n=n, bottom=bottom, layers=[("OR", [out_gate])])
