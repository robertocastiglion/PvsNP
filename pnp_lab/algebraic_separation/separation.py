"""Il cuore di query complexity della separazione P^Ã ≠ NP^Ã.

Modello (onesto, e dichiarato). Un oracolo è una funzione booleana A : {0,1}^m →
{0,1} (quindi N = 2^m valori sul cubo). L'accesso ALGEBRICO permette di valutare
l'estensione multilineare Ã in un qualunque punto r ∈ GF(p)^m; sul cubo Ã = A.

Problema OR: «esiste un 1 in A?» — il prototipo di problema NP.

  • Lato NP (nondeterministico).  Si indovina un testimone z ∈ {0,1}^m e con UNA
    query si verifica Ã(z) = A(z) = 1. Complessità a query nondeterministica = 1.

  • Lato P (deterministico).  Un algoritmo deterministico interroga Ã in punti
    r_1, r_2, … L'AVVERSARIO risponde sempre 0 (coerente con A ≡ 0). Perché
    l'algoritmo sia corretto, NESSUN oracolo booleano non nullo deve dare le stesse
    risposte 0 su quei punti — altrimenti seguirebbe lo stesso cammino e otterrebbe
    la risposta sbagliata. Cioè i funzionali di valutazione  χ_·(r_i)  non devono
    avere alcun vettore-nucleo booleano non nullo. Finché ne hanno uno, due
    posizioni segrete si "cancellano" e l'algoritmo è cieco.

Risultato: la complessità deterministica è ≥ κ(m,p) := minimo numero di punti di
valutazione che eliminano ogni nucleo booleano. Con N = 2^m > p−1 una sola query
non basta (κ ≥ 2): un insieme di N valori in GF(p) non può essere "zero-sum-free".
Quindi NP a query = 1, ma P a query cresce — la separazione, nel suo cuore.

Onestà sul confine: ESEGUIAMO questa separazione a query. Il sollevamento a un
oracolo per macchine di Turing (P^Ã ≠ NP^Ã) è la diagonalizzazione standard, e la
versione asintotica/forte è il teorema di Aaronson–Wigderson: li CITIAMO.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations, product
from typing import List, Optional, Tuple

from pnp_lab.algebrization import Field, MultilinearExtension, bits

Point = Tuple[int, ...]
BoolVec = Tuple[int, ...]


def all_field_points(p: int, m: int) -> List[Point]:
    """Tutti i punti di GF(p)^m (le possibili query algebriche)."""
    return [tuple(x) for x in product(range(p), repeat=m)]


def all_boolean_oracles(m: int, *, nonzero: bool = True):
    """Tutti gli oracoli booleani A : {0,1}^m → {0,1}, come tuple di lunghezza 2^m."""
    N = 1 << m
    start = 1 if nonzero else 0
    for code in range(start, 1 << N):
        yield tuple((code >> i) & 1 for i in range(N))


def chi_vector(point: Point, m: int, field: Field) -> List[int]:
    """[χ_z(point) per z ∈ {0,1}^m]: il funzionale lineare di una query algebrica.

    χ_z(r) = ∏_i (r_i se z_i=1, altrimenti 1−r_i). L'evaluazione Ã(r) è la
    combinazione lineare Σ_z A(z)·χ_z(r) dei valori dell'oracolo sul cubo.
    """
    out: List[int] = []
    for a in range(1 << m):
        zb = bits(a, m)
        v = 1
        for ri, zi in zip(point, zb):
            v = field.mul(v, field.reduce(ri) if zi == 1 else field.sub(1, ri))
        out.append(v)
    return out


def evaluate(values: BoolVec, point: Point, field: Field) -> int:
    """Ã(point) per l'oracolo booleano `values` (estensione multilineare su GF(p))."""
    m = len(point)
    chi = chi_vector(point, m, field)
    total = 0
    for z, vz in enumerate(values):
        if vz:
            total = field.add(total, chi[z])
    return total


def boolean_kernel_witness(query_points: List[Point], m: int, field: Field) -> Optional[BoolVec]:
    """Un oracolo booleano NON nullo che dà 0 su tutte le query (se esiste).

    È l'avversario: A ≠ 0 ma indistinguibile dall'oracolo tutto-zero con quelle
    query. La sua esistenza significa che le query NON bastano a decidere OR.
    """
    chis = [chi_vector(r, m, field) for r in query_points]
    N = 1 << m
    for code in range(1, 1 << N):
        ones = [z for z in range(N) if (code >> z) & 1]
        if all(field.reduce(sum(chi[z] for z in ones)) == 0 for chi in chis):
            return tuple((code >> z) & 1 for z in range(N))
    return None


def kills_all_kernels(query_points: List[Point], m: int, field: Field) -> bool:
    """True se nessun oracolo booleano non nullo si annulla su tutte le query."""
    return boolean_kernel_witness(query_points, m, field) is None


@dataclass
class CancellationAdversary:
    m: int
    p: int
    query_point: Point                # la query r dell'algoritmo
    ones_positions: List[Point]       # le posizioni segrete con un 1 (si cancellano)
    chi_values: List[int]             # χ_z(r) per quelle posizioni (somma ≡ 0)


def cancellation_example(m: int, p: int) -> Optional[CancellationAdversary]:
    """Una query r e un insieme MINIMALE di posizioni segrete i cui χ_z(r) sommano a 0.

    L'oracolo A con quei 1 ha Ã(r) = 0, identico al tutto-zero: quella query è
    cieca. È l'avversario di cancellazione, l'analogo algebrico della
    diagonalizzazione di Baker–Gill–Solovay (Modulo 2).
    """
    F = Field(p)
    best: Optional[CancellationAdversary] = None
    N = 1 << m
    for r in all_field_points(p, m):
        chi = chi_vector(r, m, F)
        # cerca il più piccolo sottoinsieme non vuoto con somma 0 (taglia crescente)
        from itertools import combinations as _comb
        nonzero_idx = [z for z in range(N) if chi[z] != 0]
        found = None
        for size in range(2, len(nonzero_idx) + 1):
            if best is not None and size >= len(best.ones_positions):
                break
            for subset in _comb(nonzero_idx, size):
                if F.reduce(sum(chi[z] for z in subset)) == 0:
                    found = subset
                    break
            if found:
                break
        if found and (best is None or len(found) < len(best.ones_positions)):
            best = CancellationAdversary(
                m=m, p=p, query_point=r,
                ones_positions=[bits(z, m) for z in found],
                chi_values=[chi[z] for z in found],
            )
            if len(found) == 2:
                break  # non si può fare meglio di una cancellazione a due
    return best


@dataclass
class SeparationResult:
    m: int
    p: int
    n_oracle_values: int             # N = 2^m
    nondet_queries: int              # = 1 (lato NP)
    det_lower_bound: int             # κ esatto, oppure il cap+1 se non raggiunto
    det_exact: bool                  # κ trovato esattamente entro il cap?
    one_query_enough: bool           # basta 1 query deterministica?


def deterministic_lower_bound(m: int, p: int, *, cap: Optional[int] = None) -> SeparationResult:
    """κ(m,p): minimo numero di punti di valutazione che eliminano ogni nucleo booleano.

    Ricerca per approfondimento iterativo sui sottoinsiemi di GF(p)^m. È il lower
    bound esatto sulla complessità deterministica a query algebriche di OR.
    """
    F = Field(p)
    pts = all_field_points(p, m)
    N = 1 << m
    if cap is None:
        cap = N
    kappa = None
    for t in range(1, cap + 1):
        found = False
        for subset in combinations(pts, t):
            if kills_all_kernels(list(subset), m, F):
                found = True
                break
        if found:
            kappa = t
            break
    exact = kappa is not None
    return SeparationResult(
        m=m, p=p, n_oracle_values=N,
        nondet_queries=1,
        det_lower_bound=kappa if exact else cap + 1,
        det_exact=exact,
        one_query_enough=(kappa == 1) if exact else False,
    )


def verify_nondet_one_query(m: int, p: int) -> bool:
    """Verifica il lato NP: su un'istanza YES, UNA query al testimone basta.

    Per ogni oracolo con almeno un 1, esiste z sul cubo con Ã(z)=1 (verifica in
    una query). Controllo esaustivo su tutti gli oracoli non nulli per m piccolo.
    """
    F = Field(p)
    for A in all_boolean_oracles(m, nonzero=True):
        witnessed = any(evaluate(A, bits(a, m), F) == 1 for a in range(1 << m) if A[a] == 1)
        if not witnessed:
            return False
    return True
