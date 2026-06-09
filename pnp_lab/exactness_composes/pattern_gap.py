"""Ciclo 2: il PRIMO gap di lift che NON sia J-I (o prova che a <=3 bit non esiste).

Contesto (RESEARCH_LOG Entry 1): ogni cella-gap del lift f∘g^k con gadget a 1 bit
trovata nel ciclo 1 e' la matrice di DISUGUAGLIANZA J - I_m (Cov=m, LP=m-1, G*=1),
il gap di dualita' LP elementare. La domanda del ciclo 2:

    esiste un gap su PATTERN-MATRIX da lift (G* > 0) che NON sia, a meno di
    permutazione di righe/colonne, la matrice J - I_m, raggiungibile a <= 3 bit?

Per un gadget di PERMUTAZIONE (XOR/EQ) il lift collassa nella pattern-matrix di un
gruppo abeliano:  M_f[x][y] = f(x XOR y)  su Z2^k  (8x8 a k=3).  Questo file:

  * `pattern_matrix(f, k)`             -- la matrice f(x XOR y) su Z2^k (esatta);
  * `is_J_minus_I_up_to_perm(M)`       -- M e' J - I_m a meno di perm righe/colonne?
  * `bool_funcs_3bit(...)`             -- enumeratori di outer a 3 bit (MAJ3, 1-in-3,
                                         threshold, tutte le 256 se serve);
  * `pattern_gap_table(...)`           -- (nome_f -> Cov, LP, G*, isJI) ESATTO;
  * `first_non_JI_gap(...)`            -- il primo gap non-J-I, o None.

Aritmetica ESATTA (Fraction): riusa gap.py (gstar/cover_number/frac_cover). Nessun
float, nessuna approssimazione. NON dimostra P vs NP: misura un gap su istanze minuscole.
"""

from __future__ import annotations

from fractions import Fraction
from itertools import permutations, product
from typing import Callable, Dict, List, Optional, Sequence, Tuple

from .gap import BoolMatrix, as_matrix, cover_number, frac_cover, gstar

BoolFn = Callable[[Tuple[int, ...]], int]


# --- costruzione della pattern-matrix su Z2^k ---------------------------------

def _xor(a: Tuple[int, ...], b: Tuple[int, ...]) -> Tuple[int, ...]:
    return tuple(ai ^ bi for ai, bi in zip(a, b))


def pattern_matrix(f: BoolFn, k: int) -> BoolMatrix:
    """M[x][y] = f(x XOR y) su Z2^k (2^k x 2^k).

    E' esattamente il lift f∘XOR^k (gadget di permutazione): vedi compose.lift con
    g=XOR. La produciamo direttamente per poter spazzare TUTTE le f a 3 bit senza
    passare da base_function (limitato a poche funzioni nominali).
    """
    pts = list(product([0, 1], repeat=k))
    return as_matrix([[f(_xor(x, y)) for y in pts] for x in pts])


def truth_table_fn(bits: Sequence[int], k: int) -> BoolFn:
    """Funzione f: {0,1}^k -> {0,1} da una tavola di verita' (lista di 2^k bit).

    L'indice nella tavola e' l'intero big-endian dell'input (b[0] bit piu' alto).
    """
    table = tuple(bits)

    def f(z: Tuple[int, ...]) -> int:
        idx = 0
        for b in z:
            idx = (idx << 1) | b
        return table[idx]

    return f


# --- detector: J - I_m a meno di permutazione di righe/colonne ----------------

def is_J_minus_I_up_to_perm(M: BoolMatrix) -> bool:
    """True sse M e' la matrice J - I_m (1 ovunque tranne una permutazione di 0)
    a meno di permutazione di righe e colonne.

    J - I_m (la "matrice di disuguaglianza") ha: quadrata m x m; ogni entrata 1
    tranne ESATTAMENTE m zeri che formano un PERFECT MATCHING (un solo 0 per riga e
    per colonna). Una permutazione di righe/colonne preserva questa proprieta', e
    qualunque matrice con esattamente m zeri in posizioni di matching e' J - I_m
    permutata.  Controllo O(m^2), nessuna enumerazione di permutazioni.
    """
    m = len(M)
    if m == 0 or any(len(row) != m for row in M):
        return False
    zeros = [(r, c) for r in range(m) for c in range(m) if M[r][c] == 0]
    if len(zeros) != m:
        return False
    # gli m zeri devono essere un matching perfetto: 1 per riga, 1 per colonna.
    rows = {r for r, _ in zeros}
    cols = {c for _, c in zeros}
    return len(rows) == m and len(cols) == m


def _canonical(M: BoolMatrix) -> Tuple:
    """Forma canonica di M sotto permutazione di righe E colonne (per dedup).

    Brute force sulle permutazioni di righe; per ognuna ordina le colonne in modo
    canonico. Solo per matrici PICCOLE (<=4x4 -- usata per i gadget 2-bit/k piccolo).
    """
    m = len(M)
    best: Optional[Tuple] = None
    for rp in permutations(range(m)):
        rows = [M[r] for r in rp]
        # ordina le colonne per il loro vettore-colonna
        cols = list(zip(*rows))
        cols_sorted = sorted(range(len(cols)), key=lambda c: cols[c])
        cand = tuple(tuple(rows[r][c] for c in cols_sorted) for r in range(m))
        if best is None or cand < best:
            best = cand
    return best


# --- enumeratori di outer a 3 bit ---------------------------------------------

def named_3bit_outers() -> Dict[str, BoolFn]:
    """Outer a 3 bit notevoli, oltre OR/AND/XOR: MAJ3, 1-in-3, threshold-2, ecc."""
    def thr(t: int) -> BoolFn:
        return lambda z: int(sum(z) >= t)

    return {
        "OR3": lambda z: int(any(z)),
        "AND3": lambda z: int(all(z)),
        "XOR3": lambda z: sum(z) & 1,
        "MAJ3": lambda z: int(sum(z) >= 2),
        "ONE_IN_3": lambda z: int(sum(z) == 1),     # esattamente un 1
        "TWO_IN_3": lambda z: int(sum(z) == 2),     # esattamente due 1
        "THR1": thr(1),                             # = OR3
        "THR2": thr(2),                             # = MAJ3
        "THR3": thr(3),                             # = AND3
        "NAE": lambda z: int(0 < sum(z) < 3),       # not-all-equal
        "EQ3": lambda z: int(sum(z) in (0, 3)),     # tutti uguali
    }


def all_3bit_outers() -> List[Tuple[str, BoolFn]]:
    """Tutte le 256 funzioni booleane a 3 bit, come (nome=tavola-bit, f)."""
    out = []
    for bits in product([0, 1], repeat=8):
        name = "".join(map(str, bits))
        out.append((name, truth_table_fn(bits, 3)))
    return out


# --- tabella di gap e ricerca del primo non-J-I -------------------------------

# (nome_f) -> (Cov, LP, G*, is_JI)
PatternCell = Tuple[int, Fraction, Fraction, bool]


def _ones(M: BoolMatrix) -> int:
    return sum(sum(row) for row in M)


def pattern_gap_table(
    outers: Sequence[Tuple[str, BoolFn]],
    k: int,
    sparsity_skip: Optional[Tuple[int, int]] = None,
) -> Dict[str, PatternCell]:
    """Per ogni outer (nome, f) calcola (Cov, LP, G*, is_JI) della pattern-matrix.

    `sparsity_skip = (lo, hi)`: se valorizzato, le matrici con #uni < lo o > hi
    sono SALTATE (densita' estreme: integrali banalmente, e l'LP esatto su 8x8
    densa e' costoso). Con None nessuna cella e' saltata.
    """
    table: Dict[str, PatternCell] = {}
    n = 1 << k
    for name, f in outers:
        M = pattern_matrix(f, k)
        if sparsity_skip is not None:
            lo, hi = sparsity_skip
            no = _ones(M)
            if no < lo or no > hi:
                continue
        cov = cover_number(M)
        lp = frac_cover(M)
        gv = Fraction(cov) - lp
        table[name] = (cov, lp, gv, is_J_minus_I_up_to_perm(M))
    return table


def first_non_JI_gap(
    outers: Sequence[Tuple[str, BoolFn]],
    k: int,
    sparsity_skip: Optional[Tuple[int, int]] = None,
) -> Optional[Tuple[str, BoolMatrix, int, Fraction, Fraction]]:
    """Il PRIMO outer la cui pattern-matrix ha G* > 0 e NON e' J - I_m.

    Ritorna (nome, M, Cov, LP, G*) oppure None se ogni gap trovato e' J - I.
    """
    n = 1 << k
    for name, f in outers:
        M = pattern_matrix(f, k)
        if sparsity_skip is not None:
            lo, hi = sparsity_skip
            no = _ones(M)
            if no < lo or no > hi:
                continue
        gv = gstar(M)
        if gv > 0 and not is_J_minus_I_up_to_perm(M):
            return name, M, cover_number(M), frac_cover(M), gv
    return None
