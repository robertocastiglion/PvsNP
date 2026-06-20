"""Bipartite Rigidity — la matrice di comunicazione a bipartizione FISSA e la sua rigidita'.

Arena (lever A pre-dichiarato): un discriminante che sia, in un colpo solo,
  (1) NON permutation-invariant     — dipende dalla bipartizione/lato, non solo da f;
  (2) NON una statistica globale di f — non si riduce a un conteggio simmetrico;
  (3) NON enumerabile a k>=4         — vive in un regime dove l'esatto e' fuori portata.
La RIGIDITA' di matrice R_M(r) della matrice di comunicazione M_f e' il candidato
naturale: e' una proprieta' della MATRICE (quindi della bipartizione, non solo di f) ed e'
notoriamente intrattabile.

Definizione operativa.  Per una matrice M su un campo K e un target di rango r,
    R_M(r) = min { #entrate di M da modificare per ottenere una matrice di rango <= r }.
Su GF(2) "modificare" = flippare un bit.  La rigidita' e' la distanza di Hamming dalla
varieta' delle matrici di rango <= r.

Oggetto esplicito a bipartizione FISSA: il prodotto interno IP_k(x,y) = <x,y> mod 2 su
k+k bit (alice = x in GF(2)^k, bob = y in GF(2)^k), che da' la matrice di Hadamard/Sylvester
  H_k[x][y] = (-1)^{<x,y>}    (forma ±1 su Q, rango pieno 2^k)
  A_k[x][y] = <x,y> mod 2     (forma 0/1 su GF(2), rango k).
E' la famiglia canonica per cui esistono lower bound di rigidita' CERTIFICATI.

Aritmetica ESATTA: GF(2) con interi, Q con Fraction (stile exactness_composes.gap).
Nessun float, nessun claim su P vs NP.  La honesty boundary (cosa e' COMPUTED-esatto vs
CITED-certified) e' enunciata in inglese in `honesty_note()` e marcata sui singoli simboli.
"""

from __future__ import annotations

from fractions import Fraction
from functools import lru_cache
from itertools import combinations, product
from typing import Callable, List, Sequence, Tuple

# Una matrice = tupla di tuple di valori (int per GF(2)/±1, Fraction per Q).
Matrix = Tuple[Tuple[int, ...], ...]
BoolFn = Callable[[Sequence[int]], int]


# --------------------------------------------------------------------------- #
#  Costruttori di matrici di comunicazione a bipartizione FISSA               #
# --------------------------------------------------------------------------- #

def _ip(x: int, y: int) -> int:
    """Prodotto interno mod 2 di due interi visti come vettori di bit."""
    return bin(x & y).count("1") & 1


def ip_matrix_gf2(k: int) -> Matrix:
    """A_k[x][y] = <x,y> mod 2 su GF(2) (2^k x 2^k).  rank_gf2(A_k) = k (anchor verde)."""
    N = 1 << k
    return tuple(tuple(_ip(x, y) for y in range(N)) for x in range(N))


def hadamard_matrix(k: int) -> Matrix:
    """H_k[x][y] = (-1)^{<x,y>} su Q (forma ±1).  E' Hadamard/Sylvester: rango pieno 2^k.

    Sui Fraction restituiamo interi ±1 (Fraction(±1)) per uniformita' col rank_q."""
    N = 1 << k
    return tuple(
        tuple(Fraction(1 - 2 * _ip(x, y)) for y in range(N)) for x in range(N)
    )


def comm_matrix_pm(f: BoolFn, k: int) -> Matrix:
    """Matrice di comunicazione GENERICA in forma ±1 su Q, bipartizione FISSA.

    Alice = primi k bit (x), Bob = ultimi k bit (y); M[x][y] = (-1)^{f(x,y)}.
    f riceve la tupla (x_0..x_{k-1}, y_0..y_{k-1}) di 2k bit (big-endian per lato)."""
    N = 1 << k
    rows = []
    for x in range(N):
        xb = [(x >> i) & 1 for i in range(k)]
        row = []
        for y in range(N):
            yb = [(y >> i) & 1 for i in range(k)]
            row.append(Fraction(1 - 2 * f(tuple(xb + yb))))
        rows.append(tuple(row))
    return tuple(rows)


def comm_matrix_gf2(f: BoolFn, k: int) -> Matrix:
    """Matrice di comunicazione GENERICA su GF(2) (0/1), bipartizione FISSA.

    Alice = primi k bit, Bob = ultimi k bit; M[x][y] = f(x,y) in {0,1}."""
    N = 1 << k
    rows = []
    for x in range(N):
        xb = [(x >> i) & 1 for i in range(k)]
        row = []
        for y in range(N):
            yb = [(y >> i) & 1 for i in range(k)]
            row.append(f(tuple(xb + yb)) & 1)
        rows.append(tuple(row))
    return tuple(rows)


def tt_to_fn(tt: int, m: int) -> BoolFn:
    """Funzione f: {0,1}^m -> {0,1} dalla truth table intera ``tt`` (bit indicizzato
    dall'intero little-endian dei m bit: idx = sum b_i << i)."""
    def f(bits: Sequence[int]) -> int:
        idx = 0
        for i, b in enumerate(bits):
            idx |= (b & 1) << i
        return (tt >> idx) & 1
    return f


# --------------------------------------------------------------------------- #
#  Ranghi ESATTI                                                              #
# --------------------------------------------------------------------------- #

def rank_gf2(M: Matrix) -> int:
    """Rango esatto su GF(2) via eliminazione di Gauss (righe come bitmask).

    Ogni riga e' impacchettata in un intero (colonna j -> bit j).  Si mantiene una base
    in forma a scaletta: ogni nuova riga viene ridotta XOR-ando i vettori-base il cui
    leading-bit e' acceso; se resta non nulla entra in base.  Costo O(rows * rank)."""
    rows = []
    for row in M:
        v = 0
        for j, e in enumerate(row):
            if int(e) & 1:
                v |= 1 << j
        rows.append(v)
    basis: List[int] = []  # tenuta ordinata per leading-bit decrescente
    for v in rows:
        cur = v
        for b in basis:
            if cur ^ b < cur:  # il leading-bit di b e' acceso in cur -> eliminalo
                cur ^= b
        if cur:
            basis.append(cur)
            basis.sort(reverse=True)
    return len(basis)


def rank_q(M: Matrix) -> int:
    """Rango esatto su Q via eliminazione di Gauss su Fraction (stile gap.py).

    Accetta entrate int o Fraction; le promuove a Fraction.  Nessun float."""
    A = [[Fraction(e) for e in row] for row in M]
    nrows = len(A)
    ncols = len(A[0]) if A else 0
    rank = 0
    r = 0
    for c in range(ncols):
        if r >= nrows:
            break
        piv = None
        for i in range(r, nrows):
            if A[i][c] != 0:
                piv = i
                break
        if piv is None:
            continue
        A[r], A[piv] = A[piv], A[r]
        inv = A[r][c]
        A[r] = [v / inv for v in A[r]]
        for i in range(nrows):
            if i != r and A[i][c] != 0:
                f = A[i][c]
                A[i] = [a - f * b for a, b in zip(A[i], A[r])]
        r += 1
        rank += 1
    return rank


# --------------------------------------------------------------------------- #
#  Rigidita' ESATTA su GF(2)  (COMPUTED, tiny)                                 #
# --------------------------------------------------------------------------- #

def _flip(M: Matrix, flips: Sequence[Tuple[int, int]]) -> Matrix:
    """Restituisce M con le entrate in ``flips`` flippate (GF(2))."""
    rows = [list(int(e) & 1 for e in row) for row in M]
    for (i, j) in flips:
        rows[i][j] ^= 1
    return tuple(tuple(r) for r in rows)


def rigidity_gf2_exact(M: Matrix, r: int, max_flips: int | None = None) -> int:
    """R_M(r) ESATTO su GF(2): minimo #flip per portare rank_gf2(M) <= r.

    METODO.  Ricerca per #flip crescente t = 0,1,2,...: se esiste un sottoinsieme di t
    entrate il cui flip porta il rango <= r, allora R = t.  Per t fissato si enumerano i
    C(N^2, t) sottoinsiemi di entrate (N = lato della matrice) e si testa il rango.
    POTATURA: si parte da t=0 (gia' a rango basso?) e ci si ferma al primo t che riesce,
    quindi si paga solo fino al minimo.  Limite superiore banale: R_M(r) <= (N - r) * 1
    NON vale in generale, ma R_M(N) = 0 e flippando un'intera riga si scende di <=1 nel
    rango, quindi R_M(r) <= (N - r) * N (azzerando N-r righe) — usato solo come guardia.

    COMPLESSITA' (onesta).  Il numero di sottoinsiemi e' C(N^2, t); per N=4 (k=2) N^2=16
    ed e' ESATTO e veloce per ogni t.  Per N=8 (k=3) N^2=64 e gia' t=3 da' C(64,3)=41664
    test di rango 8x8 — fattibile ma lento; t=4 da' ~635k.  Il target tipico r=2^{k-1}=4
    su k=3 (8x8) e' raggiungibile a t piccolo (vedi sotto), quindi rimane calcolabile;
    se l'utente passa ``max_flips`` la ricerca si arresta e SOLLEVA RuntimeError se il
    minimo non e' stato raggiunto entro quel budget (onesta': nessun valore inventato).
    Per matrici piu' grandi questo esatto NON e' praticabile — usare rigidity_certified_lb.
    """
    N = len(M)
    entries = [(i, j) for i in range(N) for j in range(N)]
    cap = max_flips if max_flips is not None else N * N
    for t in range(cap + 1):
        for subset in combinations(entries, t):
            if rank_gf2(_flip(M, subset)) <= r:
                return t
    raise RuntimeError(
        f"rigidity non raggiunta entro max_flips={cap}: R_M({r}) > {cap}. "
        "Aumenta il budget o usa rigidity_certified_lb (regime non-enumerabile)."
    )


def _negate(M: Matrix, flips: Sequence[Tuple[int, int]]) -> Matrix:
    """Restituisce M (entrate ±1 su Q) con i segni in ``flips`` invertiti."""
    rows = [[Fraction(e) for e in row] for row in M]
    for (i, j) in flips:
        rows[i][j] = -rows[i][j]
    return tuple(tuple(r) for r in rows)


def rigidity_q_pm_exact(M: Matrix, r: int, max_flips: int | None = None) -> int:
    """R_M(r) ESATTO su Q per una matrice ±1: minimo #entrate da NEGARE (±1 -> ∓1) per
    portare rank_q(M) <= r.  E' la rigidita' a cui si riferisce il bound spettrale di
    Hadamard (il regime CERTIFICATO a k>=4), quindi l'oggetto esatto coerente col bound.

    METODO e COMPLESSITA': identici a ``rigidity_gf2_exact`` (ricerca per t crescente,
    C(N^2, t) sottoinsiemi), ma il test e' rank_q (Gauss su Fraction).  Per N=4 (k=2) e'
    ESATTO e veloce; per N=8 (k=3) cresce in fretta (C(64,t)) e va dato un ``max_flips``;
    se il minimo non e' raggiunto entro il budget SOLLEVA RuntimeError (nessun valore
    inventato).  Oltre k=3 NON praticabile — usare rigidity_certified_lb."""
    N = len(M)
    entries = [(i, j) for i in range(N) for j in range(N)]
    cap = max_flips if max_flips is not None else N * N
    for t in range(cap + 1):
        for subset in combinations(entries, t):
            if rank_q(_negate(M, subset)) <= r:
                return t
    raise RuntimeError(
        f"rigidity_q non raggiunta entro max_flips={cap}: R_M({r}) > {cap}. "
        "Aumenta il budget o usa rigidity_certified_lb (regime non-enumerabile)."
    )


# --------------------------------------------------------------------------- #
#  Lower bound CERTIFICATO per IP/Hadamard a k>=4  (CITED, non enumerabile)    #
# --------------------------------------------------------------------------- #

def rigidity_certified_lb(k: int, r: int) -> int:
    """Lower bound CERTIFICATO sulla rigidita' R_{H_k}(r) della matrice di Hadamard 2^k x 2^k.

    PARENT THEOREM (CITED, NON ri-dimostrato qui).  Per una matrice n x n a entrate ±1 con
    valore singolare massimo sigma_max, ogni matrice di rango <= r differisce da essa in
    almeno
            R(r) >= (n - r) * n / (sigma_max^2 / n)  ... [forma generica spettrale]
    Per la matrice di Hadamard H_k (n = 2^k) TUTTI i valori singolari valgono sqrt(n)
    (H H^T = n I), quindi sigma_max^2 = n e il bound spettrale di Friedman / de Wolf
    (cfr. de Wolf, "Lower bounds on matrix rigidity via a quantum argument", 2006, e
    Midrijanis) da':
            R_{H_k}(r) >= n^2 / (4 (r+1))        per r < n,   n = 2^k.
    (Equivalentemente la classica Lokam: R_{H}(r) >= n^2/r per r piccolo; usiamo la
    forma conservativa n^2/(4(r+1)) sempre valida.)  Restituiamo l'intero
            floor( n^2 / (4 (r+1)) ).
    Questo e' un VALORE CERTIFICATO (CITED-certified): non e' la rigidita' esatta, e' una
    garanzia inferiore valida a ogni k, incluso il regime non-enumerabile k>=4."""
    n = 1 << k
    if r >= n:
        return 0
    return (n * n) // (4 * (r + 1))


# --------------------------------------------------------------------------- #
#  Densita' normalizzata rho                                                   #
# --------------------------------------------------------------------------- #

def rho(k: int, r: int, *, exact_up_to: int = 2, max_flips: int | None = None) -> Fraction:
    """rho(k,r) = R / 4^k, la rigidita' NORMALIZZATA dal numero totale di entrate (2^k)^2.

    Oggetto COERENTE col bound certificato: la rigidita' su Q (per NEGAZIONE di segno)
    della matrice di Hadamard ±1 H_k, con target r < 2^k.
    Per k <= ``exact_up_to`` usa la rigidita' ESATTA (COMPUTED, rigidity_q_pm_exact);
    per k oltre usa il lower bound CERTIFICATO di Hadamard (CITED, lower bound — quindi
    rho a k grande e' un rho_LB, una garanzia inferiore, NON il valore esatto).  Marca
    cosi' il cambio di regime esatto -> certificato.  Default chiamante: r = 2^{k-1}."""
    total = Fraction(1 << (2 * k))
    if k <= exact_up_to:
        R = rigidity_q_pm_exact(hadamard_matrix(k), r, max_flips=max_flips)
    else:
        R = rigidity_certified_lb(k, r)
    return Fraction(R) / total


def honesty_note() -> str:
    return (
        "COMPUTED exactly (integers over GF(2), Fraction over Q): the GF(2)-rank, the "
        "rational rank, and the matrix rigidity R_M(r) (min #flips to reach rank <= r) of "
        "the inner-product / Hadamard communication matrix at a FIXED bipartition, for the "
        "tiny instances that are truly enumerable (k<=2 fully; k=3 with an explicit per-t "
        "budget — beyond that subset search blows up and we stop honestly rather than "
        "fabricate a value).  CITED, never re-proved: the spectral rigidity lower bound for "
        "Hadamard matrices (de Wolf 2006 / Midrijanis / Lokam), used as the parent theorem "
        "for the certified bound R_{H_k}(r) >= n^2/(4(r+1)) at k>=4 (the non-enumerable "
        "regime).  This tests whether matrix rigidity at a fixed bipartition carries content "
        "outside the lab's joint orbit-invariant dictionary or shows cross-level leverage.  "
        "No separation, no P vs NP claim."
    )
