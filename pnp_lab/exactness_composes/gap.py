"""Gap di integralita' del CERTIFICATE-COVERING IP di una matrice di comunicazione.

Definizione operativa (Modulo 18, congettura "EXACTNESS COMPOSES").
Per una matrice booleana M (matrice di comunicazione, righe = input di Alice,
colonne = input di Bob):

* un *1-rettangolo* e' un rettangolo combinatorio R x C i cui valori sono tutti 1;
* il programma intero di COPERTURA dei certificati e':
      Cov(M)  = min numero di 1-rettangoli che coprono TUTTE le entrate-1 di M;
* il suo rilassamento LP (canonico, sempre definito):
      LP(M)   = ottimo frazionario della stessa copertura (pesi reali >= 0);
* il GAP PINNATO sul LP:
      G*(M)   = Cov(M) - LP(M)  >= 0,   G*(M) = 0  <=>  l'IP e' integrale.

Tutto e' calcolato in aritmetica ESATTA (Fraction): Cov(M) per set-cover esatto,
LP(M) risolvendo il duale di packing con un simplesso razionale (origine ammissibile,
nessuna fase-1). Per duality forte LP-packing = LP-covering, quindi il valore e' esatto.

Questo modulo NON dimostra P vs NP: misura un gap di integralita' su istanze minuscole.
"""

from __future__ import annotations

from fractions import Fraction
from functools import lru_cache
from typing import Dict, FrozenSet, List, Sequence, Tuple

# Una matrice booleana = tupla di tuple di 0/1.
BoolMatrix = Tuple[Tuple[int, ...], ...]
Entry = Tuple[int, int]


def as_matrix(rows: Sequence[Sequence[int]]) -> BoolMatrix:
    """Normalizza in BoolMatrix (tuple di tuple, valori in {0,1})."""
    return tuple(tuple(1 if v else 0 for v in row) for row in rows)


def ones(M: BoolMatrix) -> List[Entry]:
    """Elenco delle entrate-1 (r, c)."""
    return [(r, c) for r, row in enumerate(M) for c, v in enumerate(row) if v]


def maximal_one_rectangles(M: BoolMatrix) -> List[FrozenSet[Entry]]:
    """Tutti i 1-rettangoli MASSIMALI, come insiemi di entrate (r, c) coperte.

    Enumerazione via "concetti formali": per ogni sottoinsieme di colonne C, le
    righe che sono 1 su tutte le C danno R; la chiusura per colonne rende il
    rettangolo massimale. Si itera sulla dimensione piu' piccola per restare leggeri.
    """
    nrows = len(M)
    ncols = len(M[0]) if M else 0
    if not ones(M):
        return []

    # Per tenere bassa l'enumerazione, itera sui sottoinsiemi della dimensione minore.
    transpose = ncols > nrows
    A = M if not transpose else as_matrix(list(zip(*M)))
    R, Cn = len(A), len(A[0])  # iteriamo sui sottoinsiemi di colonne di A (Cn <= R)

    seen: Dict[Tuple[FrozenSet[int], FrozenSet[int]], FrozenSet[Entry]] = {}
    # rows-bitmask per colonna: quali righe sono 1 in quella colonna
    col_rows = [frozenset(r for r in range(R) if A[r][c]) for c in range(Cn)]

    for mask in range(1, 1 << Cn):
        cols = [c for c in range(Cn) if mask & (1 << c)]
        # R(cols) = righe 1 su tutte le colonne selezionate
        rset = frozenset.intersection(*[col_rows[c] for c in cols]) if cols else frozenset()
        if not rset:
            continue
        # chiusura: tutte le colonne dove ogni riga di rset e' 1
        cclose = frozenset(c for c in range(Cn) if all(A[r][c] for r in rset))
        key = (rset, cclose)
        if key in seen:
            continue
        # entrate coperte (riportate nell'orientamento originale)
        if not transpose:
            ent = frozenset((r, c) for r in rset for c in cclose)
        else:
            ent = frozenset((c, r) for r in rset for c in cclose)  # de-traspone
        seen[key] = ent

    # tieni solo i massimali (per inclusione di entrate)
    rects = list(seen.values())
    maximal: List[FrozenSet[Entry]] = []
    for i, ri in enumerate(rects):
        if not any(i != j and ri < rj for j, rj in enumerate(rects)):
            maximal.append(ri)
    return maximal


def cover_number(M: BoolMatrix) -> int:
    """Cov(M): minimo numero di 1-rettangoli che coprono tutte le entrate-1 (esatto)."""
    universe = frozenset(ones(M))
    if not universe:
        return 0
    rects = [r & universe for r in maximal_one_rectangles(M)]
    rects = [r for r in rects if r]

    @lru_cache(maxsize=None)
    def solve(uncovered: FrozenSet[Entry]) -> int:
        if not uncovered:
            return 0
        # ramifica sull'elemento coperto dal minor numero di rettangoli
        elem = min(uncovered, key=lambda e: sum(1 for r in rects if e in r))
        candidates = [r for r in rects if elem in r]
        best = len(uncovered)  # singoletti: limite superiore banale
        for r in candidates:
            best = min(best, 1 + solve(uncovered - r))
        return best

    return solve(universe)


def _simplex_max(
    A: List[List[Fraction]], b: List[Fraction], c: List[Fraction]
) -> Fraction:
    """max c.x  s.t.  A x <= b, x >= 0, con b >= 0 (origine ammissibile).

    Simplesso primale esatto su Fraction con regola di Bland (anti-ciclo).
    Ritorna il valore ottimo (Fraction). Usato per il LP duale di packing.
    """
    m = len(A)
    n = len(c)
    total = n + m
    # tableau: m righe vincolo + 1 riga obiettivo; colonne: n strutturali + m slack + RHS
    T: List[List[Fraction]] = []
    for i in range(m):
        row = list(A[i]) + [Fraction(1) if j == i else Fraction(0) for j in range(m)]
        row.append(b[i])
        T.append(row)
    obj = [-ci for ci in c] + [Fraction(0)] * m + [Fraction(0)]
    T.append(obj)
    basis = list(range(n, n + m))

    while True:
        # entrante: primo indice con costo ridotto negativo (Bland)
        col = -1
        for j in range(total):
            if T[m][j] < 0:
                col = j
                break
        if col == -1:
            break
        # rapporto minimo, tie-break sul minor indice di base (Bland)
        row = -1
        best: Fraction | None = None
        for i in range(m):
            if T[i][col] > 0:
                ratio = T[i][total] / T[i][col]
                if best is None or ratio < best or (ratio == best and basis[i] < basis[row]):
                    best = ratio
                    row = i
        if row == -1:
            raise ValueError("LP illimitato (inatteso per un packing).")
        piv = T[row][col]
        T[row] = [v / piv for v in T[row]]
        for i in range(m + 1):
            if i != row and T[i][col] != 0:
                f = T[i][col]
                T[i] = [a - f * bb for a, bb in zip(T[i], T[row])]
        basis[row] = col

    return T[m][total]


def frac_cover(M: BoolMatrix) -> Fraction:
    """LP(M): copertura frazionaria esatta = valore del packing duale (Fraction)."""
    universe = ones(M)
    if not universe:
        return Fraction(0)
    rects = [r & frozenset(universe) for r in maximal_one_rectangles(M)]
    rects = [r for r in rects if r]
    idx = {e: i for i, e in enumerate(universe)}
    # Duale di packing: max sum_e y_e  s.t.  per ogni rettangolo r: sum_{e in r} y_e <= 1.
    A: List[List[Fraction]] = []
    for r in rects:
        rowv = [Fraction(0)] * len(universe)
        for e in r:
            rowv[idx[e]] = Fraction(1)
        A.append(rowv)
    b = [Fraction(1)] * len(rects)
    c = [Fraction(1)] * len(universe)
    return _simplex_max(A, b, c)


def gstar(M: BoolMatrix) -> Fraction:
    """G*(M) = Cov(M) - LP(M)  (>= 0; = 0 sse l'IP di copertura e' integrale)."""
    return Fraction(cover_number(M)) - frac_cover(M)


def is_integral(M: BoolMatrix) -> bool:
    """True sse G*(M) = 0 (copertura integrale)."""
    return gstar(M) == 0
