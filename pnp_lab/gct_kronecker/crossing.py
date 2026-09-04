"""Crossing s*(d) per partizioni self-conjugate 3-hook — H65.

Una partizione self-conjugate di d con Durfee=3 e` determinata
univocamente dai suoi hook diagonali (h1, h2, h3): interi DISPARI
DISTINTI con h1 > h2 > h3 >= 1 e h1+h2+h3 = d.
Siccome gli hi sono dispari e distinti, d = somma di 3 dispari = dispari.
Quindi per d pari k=3 e` impossibile.

Spread: s = (h1 - h3) / d   in [0, 1).
Genericita`: R = g(lam, lam, lam) * d! / f(lam)^3
            dove f(lam) = d! / prod_{(i,j) in lam} hook(i,j)  (dim. irrappresentazione).

Crossing s*(d): valore di s in cui R attraversa 1 (interpolazione lineare
tra i due punti consecutivi con R < 1 e R >= 1).
"""

from __future__ import annotations

import sys
from fractions import Fraction
from math import factorial
from typing import List, Optional, Tuple

from .fast import g_fast

Partition = Tuple[int, ...]


# ---------------------------------------------------------------------------
# Costruzione partizione self-conjugate da hook diagonali
# ---------------------------------------------------------------------------

def sc_partition_from_hooks(h1: int, h2: int, h3: int) -> Partition:
    """Costruisce la partizione self-conjugate con hook diagonali (h1, h2, h3).

    Per Durfee=3: h1 > h2 > h3 dispari.  La riga i (1-indexed, i=1,2,3)
    del diagramma di Young vale:
        lam_i = i + (h_i - 1) // 2

    Questo perche` la cella diagonale (i,i) ha arm = lam_i - i, leg = lam_i - i
    (self-conjugate => arm = leg), e hook = 2*arm + 1 = h_i.

    Oltre le prime 3 righe esistono righe lam_4, lam_5, ... determinate
    dal fatto che lam e` self-conjugate: la colonna j ha altezza uguale a lam_j.
    Per j > 3: lam_j = #{i in {1,2,3} : lam_i >= j}.
    """
    hooks = sorted([h1, h2, h3], reverse=True)  # h[0] > h[1] > h[2]
    k = 3
    # Righe Durfee (1-indexed i=1,2,3)
    durfee_rows = [i + 1 + (hooks[i] - 1) // 2 for i in range(k)]
    # durfee_rows[i] = (i+1) + (h_{i+1}-1)//2  con i 0-indexed

    # Righe oltre il quadrato di Durfee
    # lam_j (j > k, 1-indexed) = #{i in 1..k : lam_i >= j}
    rows: List[int] = list(durfee_rows)
    max_j = durfee_rows[0]  # lam_1 e` la riga piu` lunga
    for j in range(k + 1, max_j + 1):  # j = 4, 5, ..., lam_1
        val = sum(1 for r in durfee_rows if r >= j)
        if val == 0:
            break
        rows.append(val)

    # Ordina decrescente (garantito dalla costruzione, ma per sicurezza)
    rows.sort(reverse=True)
    return tuple(rows)


def hook_length(lam: Partition, i: int, j: int) -> int:
    """Lunghezza dell'hook alla cella (i, j) (0-indexed)."""
    arm = lam[i] - j - 1
    leg = sum(1 for r in range(i + 1, len(lam)) if lam[r] > j)
    return arm + leg + 1


def frame_robinson_thrall(lam: Partition) -> int:
    """Dimensione dell'irriducibile S^lam via formula degli hook: d! / prod hook.

    Restituisce un intero esatto.
    """
    d = sum(lam)
    denom = 1
    for i, row_len in enumerate(lam):
        for j in range(row_len):
            denom *= hook_length(lam, i, j)
    return factorial(d) // denom


# ---------------------------------------------------------------------------
# Enumerazione shape 3-hook self-conjugate per d dato
# ---------------------------------------------------------------------------

def enum_sc3hook(d: int) -> List[Tuple[Tuple[int, int, int], Partition, Fraction, Fraction]]:
    """Enumera tutte le shape self-conjugate 3-hook di d.

    Ritorna lista di (hooks, lam, s, R) con:
      hooks = (h1, h2, h3) interi dispari con h1>h2>h3>=1, somma=d
      lam   = partizione self-conjugate corrispondente
      s     = Fraction((h1 - h3), d)  [spread]
      R     = Fraction(g * d!, f^3)   [genericita` esatta]

    Se d e` pari o d < 5 ritorna lista vuota (k=3 impossibile).
    """
    if d % 2 == 0 or d < 5:
        return []

    results = []
    # h3 dispari >= 1, h2 dispari > h3, h1 = d - h2 - h3 dispari > h2
    for h3 in range(1, d, 2):           # dispari, h3 < d/3
        for h2 in range(h3 + 2, d, 2):  # dispari, h2 > h3
            h1 = d - h2 - h3
            if h1 <= h2:
                continue
            if h1 % 2 == 0:
                continue  # h1 deve essere dispari
            # Tutti e tre dispari, h1 > h2 > h3 >= 1, somma = d
            lam = sc_partition_from_hooks(h1, h2, h3)
            assert sum(lam) == d, f"Errore costruzione: {lam} sum={sum(lam)} != {d}"
            f_lam = frame_robinson_thrall(lam)
            g = g_fast(lam, lam, lam)
            d_fact = factorial(d)
            # R = g * d! / f^3  (Fraction esatta)
            R = Fraction(g * d_fact, f_lam ** 3)
            s = Fraction(h1 - h3, d)
            results.append(((h1, h2, h3), lam, s, R))

    # Ordina per spread crescente
    results.sort(key=lambda x: x[2])
    return results


# ---------------------------------------------------------------------------
# Calcolo crossing s*(d)
# ---------------------------------------------------------------------------

def compute_crossing(d: int) -> Optional[Fraction]:
    """Calcola s*(d): il punto dove R(s) attraversa 1 (interpolazione lineare).

    Cerca la prima coppia consecutiva (per spread crescente) con R < 1 e R >= 1.
    Se non esiste crossing, ritorna None.
    """
    points = enum_sc3hook(d)
    if not points:
        return None

    for i in range(len(points) - 1):
        _, _, s0, R0 = points[i]
        _, _, s1, R1 = points[i + 1]
        if R0 < 1 and R1 >= 1:
            # Interpolazione lineare: s* = s0 + (1 - R0) / (R1 - R0) * (s1 - s0)
            return s0 + (Fraction(1) - R0) / (R1 - R0) * (s1 - s0)
        if R0 >= 1 and R1 < 1:
            # Crossing inverso (R decresce attraverso 1)
            return s0 + (Fraction(1) - R0) / (R1 - R0) * (s1 - s0)

    return None


def delta_s_star(d_list: List[int]) -> List[Optional[Fraction]]:
    """Calcola |s*(d_{i+1}) - s*(d_i)| per la lista d_list.

    Ritorna lista di len(d_list)-1 valori (o None se un crossing manca).
    """
    crossings = [compute_crossing(d) for d in d_list]
    deltas: List[Optional[Fraction]] = []
    for i in range(len(crossings) - 1):
        if crossings[i] is None or crossings[i + 1] is None:
            deltas.append(None)
        else:
            deltas.append(abs(crossings[i + 1] - crossings[i]))
    return deltas


# ---------------------------------------------------------------------------
# Utility stampa (riconfigura stdout per Unicode)
# ---------------------------------------------------------------------------

def print_table(d_list: List[int]) -> None:
    """Stampa tabella s*(d) e |Delta s*| per i valori d in d_list."""
    sys.stdout.reconfigure(encoding="utf-8")
    crossings = {}
    for d in d_list:
        c = compute_crossing(d)
        crossings[d] = c
        pts = enum_sc3hook(d)
        n = len(pts)
        c_str = f"{float(c):.4f}" if c is not None else "none"
        print(f"d={d:2d}  #shape={n}  s*={c_str}")

    print()
    print("|Delta s*| tra d consecutivi:")
    ds = [d for d in d_list if crossings.get(d) is not None]
    for i in range(len(ds) - 1):
        da, db = ds[i], ds[i + 1]
        delta = abs(crossings[db] - crossings[da])
        print(f"  d={da}->{db}:  |Delta s*| = {float(delta):.4f}  ({delta})")
