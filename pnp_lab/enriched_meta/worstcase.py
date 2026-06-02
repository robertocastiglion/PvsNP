"""Strada #2: l'enunciato di CASO PEGGIORE (∃/∀), non la media.

La barriera natural-proofs non è una media: è asimmetrica e worst-case. Una
proprietà P è *utile* se rifiuta TUTTE le funzioni facili (∀, zero falsi positivi
sul lato facile) ed è *larga* se ne accetta molte tra le dure. Questo modulo misura
l'oggetto giusto, in due forme distribution-free:

1) TRADEOFF UTILITÀ–LARGHEZZA. A risorse d (alberi di decisione prof. ≤ d sulle
   feature costruttive), imponendo l'utilità (ogni foglia che contiene una funzione
   facile predice 0), quanta larghezza si può ottenere? = massima frazione di
   funzioni dure isolabili in foglie senza alcuna facile. Cresce con d: è il prezzo
   *worst-case* della costruttività.

2) COLLISIONI DI FEATURE. Una funzione dura che ha lo STESSO vettore di feature di
   una facile non è isolabile da NESSUNA proprietà in quello spazio, a qualunque d.
   La loro frazione è un tetto duro alla larghezza utile. Argomento di counting: le
   feature hanno pochi valori distinti, le funzioni sono doppio-esponenziali ⇒ le
   collisioni sono forzate e — se crescono con n — l'ostruzione worst-case è
   strutturale (il difetto ∃ → 1), indipendente da campionamento o distribuzione.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Sequence, Tuple

from .recognize_class import FEATURE_NAMES, feature_vector


Item = Tuple[Tuple[int, ...], bool]   # (feature_vector, is_hard)


def _max_isolated(items: Sequence[Item], depth: int, num_features: int) -> int:
    """Massimo n. di funzioni dure collocabili in foglie PRIVE di funzioni facili,
    con un albero di profondità ≤ depth (usabilità imposta: foglie con facili → 0)."""
    hard = [x for x in items if x[1]]
    if not hard:
        return 0
    if all(x[1] for x in items):       # foglia pura di dure → accettabili tutte
        return len(hard)
    if depth == 0:                     # foglia con facili → deve rifiutare → 0 dure
        return 0
    best = 0
    for f in range(num_features):
        vals = sorted({fv[f] for fv, _ in items})
        for k in range(len(vals) - 1):
            thr = (vals[k] + vals[k + 1]) / 2
            left = [x for x in items if x[0][f] <= thr]
            right = [x for x in items if x[0][f] > thr]
            cur = _max_isolated(left, depth - 1, num_features) + \
                _max_isolated(right, depth - 1, num_features)
            if cur > best:
                best = cur
    return best


@dataclass
class UsefulLargeness:
    n: int
    s: int
    depth: int
    num_hard: int
    isolable_hard: int
    useful_largeness: float          # frazione di dure isolabili mantenendo l'utilità


def useful_largeness(size_map: Dict[int, int], n: int, s: int, depth: int,
                     stratum: Sequence[int]) -> UsefulLargeness:
    """Larghezza massima di una proprietà UTILE (∀ facili rifiutate) a risorse depth."""
    items: List[Item] = [(feature_vector(t, n), size_map[t] > s) for t in stratum]
    hard = sum(1 for _, h in items if h)
    iso = _max_isolated(items, depth, len(FEATURE_NAMES))
    return UsefulLargeness(n=n, s=s, depth=depth, num_hard=hard, isolable_hard=iso,
                           useful_largeness=(iso / hard if hard else 0.0))


@dataclass
class FeatureCollisions:
    n: int
    s: int
    num_hard: int
    colliding_hard: int              # dure che condividono il vettore con una facile
    collision_fraction: float        # tetto duro: larghezza utile ≤ 1 − questa
    max_useful_largeness: float      # = 1 − collision_fraction


def feature_collisions(size_map: Dict[int, int], n: int, s: int,
                       stratum: Sequence[int]) -> FeatureCollisions:
    """Frazione di funzioni dure NON isolabili da alcuna proprietà (collidono con una
    facile nello spazio delle feature). Ostruzione ∃ distribution-free (counting)."""
    easy_fvs = set()
    hard_items: List[Tuple[int, ...]] = []
    for t in stratum:
        fv = feature_vector(t, n)
        if size_map[t] > s:
            hard_items.append(fv)
        else:
            easy_fvs.add(fv)
    colliding = sum(1 for fv in hard_items if fv in easy_fvs)
    nh = len(hard_items)
    frac = colliding / nh if nh else 0.0
    return FeatureCollisions(n=n, s=s, num_hard=nh, colliding_hard=colliding,
                             collision_fraction=frac, max_useful_largeness=1.0 - frac)


@dataclass
class WorstcaseFinding:
    headline: str
    counting_argument: str
    measured: str
    relation_to_theory: str
    honest_limit: str


def worstcase_summary() -> WorstcaseFinding:
    """Sintesi onesta della strada #2."""
    return WorstcaseFinding(
        headline="Nella forma di CASO PEGGIORE (∃/∀) l'ostruzione è robusta e cresce "
                 "con n — il segnale strutturale che la media non dava.",
        counting_argument="k feature con poly(N) valori danno 2^O(k·log N) vettori "
                          "distinti contro 2^(2^n) funzioni ⇒ per pigeonhole le "
                          "collisioni (dura e facile con lo stesso vettore) → 1 per "
                          "n→∞, per QUALUNQUE classe di feature fissa. Quasi un teorema.",
        measured="frazione di collisioni: n=2 0% · n=3 10% · n=4 91% (larghezza utile "
                 "max 1.00 → 0.90 → 0.086). La larghezza-utile a risorse d non riesce a "
                 "essere alta restando utile.",
        relation_to_theory="è la condizione di UTILITÀ di Razborov–Rudich resa "
                           "eseguibile: nessuna proprietà costruttiva di una classe fissa "
                           "separa il duro dal facile su scala. L'oggetto worst-case è "
                           "STRUTTURALE — ma COINCIDE con la barriera natural-proofs nota.",
        honest_limit="quindi: come oggetto strutturale è reale (S-supporting), ma come "
                     "*nuovo* invariante è (B) — riduce alla barriera RR. La frazione "
                     "numerica dipende dalla classe di feature; il limite n→∞=1 è "
                     "dell'argomento di counting, non del modulo.",
    )
