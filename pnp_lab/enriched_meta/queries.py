"""Strada #3: la complessità di CERTIFICATO della durezza (quante query a f servono).

Dualizza le collisioni di feature (strada #2). Invece di chiedere "quale proprietà
costruttiva separa il duro dal facile", chiediamo: **quante posizioni della tavola
di verità (query a f) bisogna leggere** per separare lo strato duro da quello
facile? = la dimensione del più piccolo insieme di coordinate S tale che le
proiezioni su S delle funzioni dure e facili siano disgiunte.

È una quantità di tipo certificate/query-complexity della durezza. La teoria predice
che la durezza non ha certificati piccoli (devi praticamente leggere tutta f). Qui
lo misuriamo ESATTAMENTE su n piccolo.

Onestà: il `greedy` dà un *upper bound* sul minimo; l'`exact` (enumerazione dei
sottoinsiemi di coordinate) dà il valore vero, fattibile solo per N=2^n piccolo.
NESSUN risultato nuovo: è il fenomeno noto "MCSP/durezza non ha certificati piccoli"
reso eseguibile ed esatto.
"""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from itertools import combinations
from typing import Dict, List, Sequence, Tuple

Item = Tuple[int, bool]   # (truth_table, is_hard)


def _items(size_map: Dict[int, int], s: int, stratum: Sequence[int]) -> List[Item]:
    return [(tt, size_map[tt] > s) for tt in stratum]


def separates(coords: Sequence[int], items: Sequence[Item]) -> bool:
    """Le proiezioni di dure e facili sulle coordinate ``coords`` sono disgiunte?"""
    easy, hard = set(), set()
    for tt, h in items:
        pat = tuple((tt >> c) & 1 for c in coords)
        (hard if h else easy).add(pat)
    return easy.isdisjoint(hard)


@dataclass
class SeparatingSet:
    n: int
    s: int
    N: int
    stratum_size: int
    size: int               # numero di query (coordinate)
    fraction: float         # size / N
    exact: bool             # True se è il minimo esatto, False se upper bound (greedy)
    separable: bool         # è stato raggiunto un insieme separante?


def greedy_separating_set(size_map: Dict[int, int], n: int, s: int,
                          stratum: Sequence[int]) -> SeparatingSet:
    """Upper bound sul minimo: aggiunge la coordinata che minimizza le collisioni
    (tie-break: massimizza il raffinamento della partizione)."""
    N = 1 << n
    items = _items(size_map, s, stratum)

    def stats(coords: List[int]) -> Tuple[int, int]:
        groups = defaultdict(lambda: [0, 0])
        for tt, h in items:
            pat = tuple((tt >> c) & 1 for c in coords)
            groups[pat][1 if h else 0] += 1
        coll = sum(e + hh for e, hh in groups.values() if e > 0 and hh > 0)
        return coll, len(groups)

    coords: List[int] = []
    remaining = list(range(N))
    coll, _ = stats(coords)
    while coll > 0 and remaining:
        best = None
        for c in remaining:
            cc, npat = stats(coords + [c])
            key = (cc, -npat)
            if best is None or key < best[0]:
                best = (key, c, cc)
        _, c, coll = best
        coords.append(c)
        remaining.remove(c)
    return SeparatingSet(n=n, s=s, N=N, stratum_size=len(items), size=len(coords),
                         fraction=len(coords) / N, exact=False, separable=(coll == 0))


def exact_min_separating_set(size_map: Dict[int, int], n: int, s: int,
                             stratum: Sequence[int],
                             mmax: int | None = None) -> SeparatingSet:
    """Minimo ESATTO di query, per enumerazione dei sottoinsiemi di coordinate.

    Fattibile solo per N=2^n piccolo. ``mmax`` limita la ricerca: se nessun
    sottoinsieme di taglia ≤ mmax separa, ritorna ``separable=False`` (lower bound:
    il minimo è > mmax)."""
    N = 1 << n
    items = _items(size_map, s, stratum)
    cap = N if mmax is None else mmax
    for m in range(0, cap + 1):
        for S in combinations(range(N), m):
            if separates(S, items):
                return SeparatingSet(n=n, s=s, N=N, stratum_size=len(items), size=m,
                                     fraction=m / N, exact=True, separable=True)
    return SeparatingSet(n=n, s=s, N=N, stratum_size=len(items), size=cap,
                         fraction=cap / N, exact=True, separable=False)


@dataclass
class CertificateFinding:
    headline: str
    measured: str
    relation_to_theory: str
    honest_limit: str


def certificate_summary() -> CertificateFinding:
    return CertificateFinding(
        headline="La durezza non ha certificati piccoli: per separarla dal facile sullo "
                 "strato critico serve leggere (quasi) tutta la tavola di verità.",
        measured="minimo ESATTO di query: n=3 → 8/8 (tutta f); n=4 → >5/16 (lower bound). "
                 "Nessuna proprietà a poche query decide la durezza sullo strato.",
        relation_to_theory="è la faccia query/certificate-complexity della barriera: "
                           "duale delle collisioni di feature (strada #2). Coerente col "
                           "fatto noto che MCSP/durezza non ha certificati piccoli.",
        honest_limit="NESSUN risultato nuovo: fenomeno noto reso eseguibile ed esatto su n "
                     "piccolo. Il greedy è solo upper bound; l'esatto è limitato a N "
                     "piccolo; due punti non sono un teorema.",
    )
