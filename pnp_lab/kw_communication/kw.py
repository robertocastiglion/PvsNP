"""Gioco di Karchmer-Wigderson MONOTONO (KW+) e misure di comunicazione esatte.

Arena (Razborov-Pudlak / Karchmer-Wigderson). Sia ``f`` una funzione booleana
MONOTONA su ``n`` variabili. Definiamo:

  * un **minterm** = un 1-input MINIMALE (insieme di coordinate poste a 1, tale
    che f=1, ma azzerando una qualunque coordinata f diventa 0);
  * un **maxterm** = un 0-input MASSIMALE (insieme di coordinate poste a 0 nel
    complemento; cioe' f=0, ma porre a 1 una qualunque coordinata fa diventare f=1).

Il gioco KW+ : Alice riceve un minterm ``m`` (un 1-input), Bob un maxterm ``M``
(un 0-input); devono concordare una coordinata ``i`` tale che ``m_i = 1`` e
``M_i = 0``. Per f monotona tale ``i`` esiste SEMPRE (altrimenti M >= m e f(M)=1).

La **matrice KW+** ha righe = minterm, colonne = maxterm; l'entrata (m, M) e'
l'INSIEME delle coordinate ``i`` con ``m_i = 1`` e ``M_i = 0`` (le mosse legali).
Un **rettangolo monocromatico** R x C e' valido se ESISTE UNA coordinata ``i``
comune a TUTTE le entrate (m, M) del sotto-rettangolo (cioe' una mossa che vince
su tutto il rettangolo). Questo e' il colore "i" del rettangolo.

Teorema (Karchmer-Wigderson, versione monotona): la profondita' del miglior
circuito monotono per f = costo di comunicazione deterministico del gioco KW+.

Tutto e' calcolato in aritmetica esatta su INTERI (bitmask), forza bruta sulle
istanze minuscole. Niente float.
"""
from __future__ import annotations

from functools import lru_cache
from itertools import product
from typing import Callable, Dict, FrozenSet, List, Tuple

# Una funzione booleana monotona e' data come callable f(x) dove x e' una tupla
# di n bit (0/1). Minterm e maxterm sono rappresentati come tuple di n bit.
BitVec = Tuple[int, ...]


# --------------------------------------------------------------------------- #
#  Minterm / maxterm per forza bruta su 2^n                                   #
# --------------------------------------------------------------------------- #
def _all_inputs(n: int) -> List[BitVec]:
    return [tuple(bits) for bits in product((0, 1), repeat=n)]


def minterms(f: Callable[[BitVec], int], n: int) -> List[BitVec]:
    """1-input MINIMALI di f (forza bruta su 2^n).

    Un input x con f(x)=1 e' minimale se azzerando una qualunque coordinata=1
    si ottiene f=0.
    """
    out: List[BitVec] = []
    for x in _all_inputs(n):
        if f(x) != 1:
            continue
        minimal = True
        for i in range(n):
            if x[i] == 1:
                y = list(x)
                y[i] = 0
                if f(tuple(y)) == 1:
                    minimal = False
                    break
        if minimal:
            out.append(x)
    return out


def maxterms(f: Callable[[BitVec], int], n: int) -> List[BitVec]:
    """0-input MASSIMALI di f (forza bruta su 2^n).

    Un input x con f(x)=0 e' massimale se ponendo a 1 una qualunque coordinata=0
    si ottiene f=1.
    """
    out: List[BitVec] = []
    for x in _all_inputs(n):
        if f(x) != 0:
            continue
        maximal = True
        for i in range(n):
            if x[i] == 0:
                y = list(x)
                y[i] = 1
                if f(tuple(y)) == 0:
                    maximal = False
                    break
        if maximal:
            out.append(x)
    return out


# --------------------------------------------------------------------------- #
#  Matrice KW+                                                                 #
# --------------------------------------------------------------------------- #
# La matrice e' una struttura: per ogni (riga r, colonna c) l'insieme di coord.
# (frozenset di interi 0..n-1). La rappresentiamo come matrice di frozenset.
KWMatrix = Tuple[Tuple[FrozenSet[int], ...], ...]


def kw_plus_matrix(f: Callable[[BitVec], int], n: int
                   ) -> Tuple[KWMatrix, List[BitVec], List[BitVec]]:
    """Costruisce la matrice KW+ di f.

    Ritorna (matrix, rows, cols) dove rows = minterm, cols = maxterm e
    matrix[r][c] = { i : minterm_r[i]=1 AND maxterm_c[i]=0 }.

    Per f monotona ogni entrata e' NON vuota (proprieta' del gioco KW+).
    """
    rows = minterms(f, n)
    cols = maxterms(f, n)
    mat: List[Tuple[FrozenSet[int], ...]] = []
    for m in rows:
        rowv: List[FrozenSet[int]] = []
        for M in cols:
            coords = frozenset(i for i in range(n) if m[i] == 1 and M[i] == 0)
            if not coords:
                raise ValueError(
                    f"entrata vuota: minterm {m} maxterm {M} -> f non monotona?"
                )
            rowv.append(coords)
        mat.append(tuple(rowv))
    return tuple(mat), rows, cols


# --------------------------------------------------------------------------- #
#  Partition number (rettangoli monocromatici che PARTIZIONANO)               #
# --------------------------------------------------------------------------- #
def _is_mono(mat: KWMatrix, rs: FrozenSet[int], cs: FrozenSet[int]) -> bool:
    """Il sotto-rettangolo rs x cs e' monocromatico? (intersezione non vuota)."""
    common: FrozenSet[int] | None = None
    for r in rs:
        for c in cs:
            common = mat[r][c] if common is None else (common & mat[r][c])
            if not common:
                return False
    return True


def _all_mono_rectangles(mat: KWMatrix) -> List[FrozenSet[Tuple[int, int]]]:
    """TUTTI i rettangoli monocromatici (combinatori, R x C) della matrice.

    Un rettangolo R x C (R sottoinsieme di righe, C di colonne) e' monocromatico
    se esiste un colore comune a tutte le entrate (intersezione non vuota). Per
    una PARTIZIONE ottimale i rettangoli non sono necessariamente massimali,
    quindi li enumeriamo TUTTI (forza bruta su 2^righe x 2^colonne; tiny).
    """
    nrows = len(mat)
    ncols = len(mat[0]) if mat else 0
    out: List[FrozenSet[Tuple[int, int]]] = []
    for rmask in range(1, 1 << nrows):
        rs = [r for r in range(nrows) if rmask & (1 << r)]
        for cmask in range(1, 1 << ncols):
            cs = [c for c in range(ncols) if cmask & (1 << c)]
            # intersezione dei colori su tutto il blocco
            common: FrozenSet[int] | None = None
            ok = True
            for r in rs:
                for c in cs:
                    common = mat[r][c] if common is None else (common & mat[r][c])
                    if not common:
                        ok = False
                        break
                if not ok:
                    break
            if ok:
                out.append(frozenset((r, c) for r in rs for c in cs))
    return out


def partition_number(mat: KWMatrix) -> int:
    """Minimo numero di rettangoli monocromatici che PARTIZIONANO la matrice.

    Calcolo ESATTO via copertura-esatta (exact cover): ogni cella e' coperta da
    ESATTAMENTE un rettangolo (rettangoli a due a due disgiunti). Enumeriamo
    TUTTI i rettangoli monocromatici (non solo i massimali: in una partizione
    ottimale possono comparire rettangoli non massimali) e poi branch-and-bound.

    Intero esatto.
    """
    nrows = len(mat)
    ncols = len(mat[0]) if mat else 0
    if nrows == 0 or ncols == 0:
        return 0
    all_cells = frozenset((r, c) for r in range(nrows) for c in range(ncols))
    rects = _all_mono_rectangles(mat)

    @lru_cache(maxsize=None)
    def solve(uncovered: FrozenSet[Tuple[int, int]]) -> int:
        if not uncovered:
            return 0
        # ramifica sulla cella coperta dal minor numero di rettangoli disponibili
        # (un rettangolo e' "disponibile" se sta interamente in uncovered).
        avail = [r for r in rects if r <= uncovered]
        cell = min(uncovered, key=lambda e: sum(1 for r in avail if e in r))
        candidates = [r for r in avail if cell in r]
        best = len(uncovered)  # upper bound banale (i singoletti sono mono)
        for r in candidates:
            best = min(best, 1 + solve(uncovered - r))
        return best

    return solve(all_cells)


# --------------------------------------------------------------------------- #
#  Dcc = costo deterministico esatto                                          #
# --------------------------------------------------------------------------- #
def dcc(mat: KWMatrix) -> int:
    """Costo deterministico esatto D^cc del gioco KW+ sulla matrice.

    Modello: un protocollo deterministico e' un albero binario. Ogni nodo
    interno e' una "domanda" che PARTIZIONA l'insieme di righe corrente in due
    (mossa di Alice) oppure l'insieme di colonne in due (mossa di Bob). Una
    foglia e' raggiunta quando il sotto-rettangolo (righe x colonne) e'
    monocromatico. Il costo e' la PROFONDITA' (numero di bit comunicati) nel
    caso peggiore, minimizzata su tutti i protocolli.

    Calcolo esatto via ricorsione con memoizzazione sullo stato
    (frozenset righe, frozenset colonne).
    """
    nrows = len(mat)
    ncols = len(mat[0]) if mat else 0
    all_rows = frozenset(range(nrows))
    all_cols = frozenset(range(ncols))

    @lru_cache(maxsize=None)
    def cost(rs: FrozenSet[int], cs: FrozenSet[int]) -> int:
        if _is_mono(mat, rs, cs):
            return 0
        best = None
        # Mossa di Alice: partiziona le righe in (S, rs\S), S proprio non vuoto.
        rlist = sorted(rs)
        if len(rlist) >= 2:
            # basta considerare le bipartizioni con il primo elemento in S
            first = rlist[0]
            others = rlist[1:]
            for mask in range(1 << len(others)):
                S = {first} | {others[i] for i in range(len(others))
                                if mask & (1 << i)}
                Sf = frozenset(S)
                comp = rs - Sf
                if not comp:
                    continue
                d = 1 + max(cost(Sf, cs), cost(comp, cs))
                if best is None or d < best:
                    best = d
        # Mossa di Bob: partiziona le colonne.
        clist = sorted(cs)
        if len(clist) >= 2:
            first = clist[0]
            others = clist[1:]
            for mask in range(1 << len(others)):
                S = {first} | {others[i] for i in range(len(others))
                                if mask & (1 << i)}
                Sf = frozenset(S)
                comp = cs - Sf
                if not comp:
                    continue
                d = 1 + max(cost(rs, Sf), cost(rs, comp))
                if best is None or d < best:
                    best = d
        assert best is not None
        return best

    return cost(all_rows, all_cols)


# --------------------------------------------------------------------------- #
#  Helper: funzione indicatrice del triangolo (3-clique) su K_m               #
# --------------------------------------------------------------------------- #
def clique_f(edges: List[Tuple[int, int]], m: int = 3
             ) -> Callable[[BitVec], int]:
    """Funzione indicatrice "il sottografo contiene una m-clique".

    ``edges`` e' l'elenco ordinato degli archi (coppie di vertici): la i-esima
    variabile booleana corrisponde a ``edges[i]``. La funzione vale 1 sse i lati
    accesi contengono una clique su ``m`` vertici (default m=3 = triangolo).
    Monotona (aggiungere archi non distrugge una clique).
    """
    from itertools import combinations
    edge_index: Dict[FrozenSet[int], int] = {
        frozenset(e): i for i, e in enumerate(edges)
    }
    vertices = sorted({v for e in edges for v in e})
    # tutte le possibili m-clique (insiemi di m vertici i cui m-scegli-2 archi
    # sono tutti presenti nell'elenco)
    cliques: List[List[int]] = []
    for verts in combinations(vertices, m):
        idxs: List[int] = []
        ok = True
        for a, b in combinations(verts, 2):
            key = frozenset((a, b))
            if key not in edge_index:
                ok = False
                break
            idxs.append(edge_index[key])
        if ok:
            cliques.append(idxs)

    def f(x: BitVec) -> int:
        for cl in cliques:
            if all(x[i] == 1 for i in cl):
                return 1
        return 0

    return f
