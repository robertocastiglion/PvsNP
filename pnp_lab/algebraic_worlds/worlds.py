"""I due mondi algebrici: la POTENZA e il LIMITE dell'accesso algebrico.

Mondo 1 — POTENZA (perché l'arithmetization scavalca la relativizzazione).
  Un oracolo booleano A su m bit nasconde un bit "piantato". Con query BOOLEANE
  servono fino a 2^m tentativi per trovarlo (Modulo 2). Ma con UNA query
  all'estensione multilineare Ã in un punto casuale del campo lo si rileva con
  probabilità (1 − 1/p)^m: l'accesso algebrico è esponenzialmente più potente.
  È esattamente ciò che permette a IP = PSPACE di non relativizzare.

Mondo 2 — LIMITE (perché, da sola, non basta).
  Determinare l'oracolo richiede comunque ~2^m query algebriche. È un lower
  bound di INTERPOLAZIONE, esatto: l'estensione multilineare ha 2^m coefficienti
  incogniti; con k < 2^m valutazioni il sistema lineare su GF(p) è
  sotto-determinato, quindi esistono DUE estensioni distinte coerenti con tutte
  le risposte — un avversario tiene in vita due oracoli indistinguibili.

Insieme: l'accesso algebrico cambia il paesaggio ma non lo banalizza. È il
contenuto concettuale della barriera dell'algebrizzazione (Aaronson–Wigderson).
"""

from __future__ import annotations

import random
from dataclasses import dataclass, field as dc_field
from itertools import product
from typing import List, Optional, Tuple

from pnp_lab.algebrization import Field, MultilinearExtension, bits

from .polynomial import Poly


# ── Mondo 1: la potenza dell'accesso algebrico ────────────────────────────

@dataclass
class PlantedDetection:
    m: int
    p: int
    planted_index: int
    algebraic_nonzero_points: int          # punti del campo in cui Ã ≠ 0
    algebraic_detect_prob: float           # = nonzero / p^m  (una query)
    exact_prob_formula: float              # (1 − 1/p)^m
    boolean_detect_prob_one_query: float   # = 1 / 2^m


def planted_oracle_extension(m: int, planted_index: int, field: Field) -> MultilinearExtension:
    """Estensione multilineare dell'oracolo booleano con un solo bit a 1."""
    values = tuple(1 if a == planted_index else 0 for a in range(1 << m))
    return MultilinearExtension(values, m, field)


def planted_detection(m: int, p: int, planted_index: int) -> PlantedDetection:
    """Confronta il potere di rilevamento: 1 query algebrica vs 1 query booleana."""
    F = Field(p)
    ext = planted_oracle_extension(m, planted_index, F)
    nonzero = sum(1 for x in product(range(p), repeat=m) if ext(x) != 0)
    total = p ** m
    return PlantedDetection(
        m=m, p=p, planted_index=planted_index,
        algebraic_nonzero_points=nonzero,
        algebraic_detect_prob=nonzero / total,
        exact_prob_formula=(1 - 1 / p) ** m,
        boolean_detect_prob_one_query=1 / (1 << m),
    )


# ── Mondo 2: il limite — lower bound di interpolazione su GF(p) ────────────

def _monomial_eval(subset: int, point: Tuple[int, ...], F: Field) -> int:
    """Valuta il monomio multilineare ∏_{j∈subset} x_j nel punto dato."""
    val = 1
    for j in range(len(point)):
        if (subset >> j) & 1:
            val = F.mul(val, point[j])
    return val


def _rref(rows: List[List[int]], ncols: int, F: Field) -> Tuple[List[List[int]], List[int]]:
    """Riduzione di Gauss–Jordan su GF(p). Restituisce (matrice ridotta, colonne pivot)."""
    mat = [row[:] for row in rows]
    pivots: List[int] = []
    r = 0
    for c in range(ncols):
        piv = None
        for i in range(r, len(mat)):
            if mat[i][c] != 0:
                piv = i
                break
        if piv is None:
            continue
        mat[r], mat[piv] = mat[piv], mat[r]
        inv = F.inv(mat[r][c])
        mat[r] = [F.mul(inv, v) for v in mat[r]]
        for i in range(len(mat)):
            if i != r and mat[i][c] != 0:
                fct = mat[i][c]
                mat[i] = [F.sub(mat[i][j], F.mul(fct, mat[r][j])) for j in range(ncols)]
        pivots.append(c)
        r += 1
        if r == len(mat):
            break
    return mat, pivots


def _null_vector(rows: List[List[int]], ncols: int, F: Field) -> Optional[List[int]]:
    """Un vettore non nullo nel nucleo (se il rango è < ncols), altrimenti None."""
    mat, pivots = _rref(rows, ncols, F)
    if len(pivots) == ncols:
        return None
    pivot_set = set(pivots)
    free = next(c for c in range(ncols) if c not in pivot_set)
    x = [0] * ncols
    x[free] = 1
    for i, c in enumerate(pivots):
        x[c] = F.neg(mat[i][free])
    return x


@dataclass
class InterpolationBound:
    m: int
    p: int
    num_queries: int
    rank: int
    determined: bool                         # rango == 2^m ?
    adversary: Optional[Poly] = None         # estensione "fantasma" coerente con le query
    witness_cube_point: Optional[Tuple[int, ...]] = None  # dove differisce dall'oracolo zero


def interpolation_lower_bound(m: int, p: int, queries: List[Tuple[int, ...]]) -> InterpolationBound:
    """Lower bound esatto: con `queries` valutazioni di Ã, l'oracolo è determinato?

    Costruisce la matrice di valutazione (righe = query, colonne = 2^m monomi
    multilineari) e ne calcola il rango su GF(p). Se rango < 2^m esibisce un
    avversario: una estensione NON nulla che si annulla su tutte le query (stesse
    risposte dell'oracolo zero) ma differisce su almeno un punto del cubo.
    """
    F = Field(p)
    ncols = 1 << m
    rows = [[_monomial_eval(S, q, F) for S in range(ncols)] for q in queries]
    nv = _null_vector(rows, ncols, F) if rows else [1] + [0] * (ncols - 1)
    if nv is None:
        # rango pieno: determinato
        return InterpolationBound(m=m, p=p, num_queries=len(queries), rank=ncols, determined=True)

    # rango = ncols - dim(nucleo); qui basta il rango come #pivot
    _, pivots = _rref(rows, ncols, F) if rows else ([], [])
    rank = len(pivots)

    # avversario: poli multilineare con coeff = vettore nullo
    terms = {}
    for S in range(ncols):
        if nv[S] != 0:
            exp = tuple((S >> j) & 1 for j in range(m))
            terms[exp] = nv[S]
    adv = Poly(n=m, field=F, terms=terms)

    # testimone sul cubo dove l'avversario differisce dall'oracolo zero
    witness = None
    for a in range(1 << m):
        x = bits(a, m)
        if adv.eval(x) != 0:
            witness = x
            break

    return InterpolationBound(m=m, p=p, num_queries=len(queries), rank=rank,
                              determined=False, adversary=adv, witness_cube_point=witness)


def random_queries(m: int, p: int, k: int, rng: random.Random) -> List[Tuple[int, ...]]:
    """k punti casuali di GF(p)^m (le 'domande' di un algoritmo a query algebriche)."""
    return [tuple(rng.randrange(p) for _ in range(m)) for _ in range(k)]


def cube_queries(m: int) -> List[Tuple[int, ...]]:
    """I 2^m vertici booleani: bastano e avanzano a determinare l'oracolo."""
    return [bits(a, m) for a in range(1 << m)]
