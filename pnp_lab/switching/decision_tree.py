"""Profondità dell'albero di decisione OTTIMO di una funzione booleana.

D(f) = la profondità minima di un albero di decisione (query deterministiche
alle variabili) che calcola f. È la misura di "complessità" che lo switching
lemma controlla: Håstad dimostra che, sotto una restrizione casuale, una DNF di
larghezza w diventa un albero di decisione poco profondo con alta probabilità.

Fatti chiave usati nel modulo:
  - una funzione costante ha D = 0;
  - D(parità su k variabili) = k  (bisogna leggerle TUTTE): la parità non si
    semplifica mai — è ciò che la rende fuori da AC0.

Calcolo esatto per ricorsione con memoizzazione sulla tabella di verità (adatto
a poche variabili libere, il caso tipico dopo una restrizione con p piccolo).
"""

from __future__ import annotations

from functools import lru_cache
from typing import Sequence, Tuple


def _cofactors(table: Tuple[int, ...], k: int, j: int) -> Tuple[Tuple[int, ...], Tuple[int, ...]]:
    """Restringe la variabile j a 0 e a 1, restituendo le due sotto-tabelle."""
    shift = k - 1 - j
    t0, t1 = [], []
    for a in range(len(table)):
        (t1 if (a >> shift) & 1 else t0).append(table[a])
    return tuple(t0), tuple(t1)


@lru_cache(maxsize=None)
def _depth(table: Tuple[int, ...], k: int) -> int:
    first = table[0]
    if all(v == first for v in table):
        return 0
    best = k  # non serve mai più di k query
    for j in range(k):
        t0, t1 = _cofactors(table, k, j)
        d = 1 + max(_depth(t0, k - 1), _depth(t1, k - 1))
        if d < best:
            best = d
    return best


def optimal_dt_depth(table: Sequence[int]) -> int:
    """Profondità dell'albero di decisione ottimo data la tabella di verità.

    ``table`` ha lunghezza 2^k (k variabili). Per k = 0 (funzione già costante)
    la profondità è 0.
    """
    t = tuple(table)
    if len(t) == 1:
        return 0
    k = (len(t) - 1).bit_length()
    if (1 << k) != len(t):
        raise ValueError("la tabella deve avere lunghezza una potenza di 2")
    return _depth(t, k)
