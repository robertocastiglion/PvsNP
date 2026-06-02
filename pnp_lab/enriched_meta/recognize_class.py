"""La lente "riconoscere" riparata: non una statistica, ma una CLASSE.

Difetto della v1: usava una singola statistica arbitraria (l'influenza totale),
quindi il "difetto" era proprietà di quella scelta, non della lente. Qui la lente
"riconoscere" diventa il **minimo errore della miglior proprietà costruttiva di una
classe a risorse limitate** — quantificata sulla classe, non su un rappresentante.

Classe a risorse d: alberi di decisione di profondità ≤ d su un banco di feature
costruttive cheap (poly(N)). d è il budget: d=0 è la costante (errore = strato di
minoranza), d crescente è più potente. Il **prezzo della costruttività** è la curva
errore(d): quanto bene una proprietà efficiente può approssimare il costo esatto.

Il legame con Razborov–Rudich: una proprietà *larga e costruttiva* (piccola d) non
può azzerare l'errore sulle funzioni dure senza far esplodere d — altrimenti
risolverebbe MCSP e romperebbe i PRG. Qui lo misuriamo come errore residuo.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Dict, List, Sequence, Tuple

from .lenses import total_influence


# ── banco di feature costruttive (tutte O(N·n) o meno) ────────────────────

def _weight(tt: int, n: int) -> int:
    return bin(tt & ((1 << (1 << n)) - 1)).count("1")


def _bias(tt: int, n: int) -> int:
    N = 1 << n
    return abs(2 * _weight(tt, n) - N)


def _coord_influences(tt: int, n: int) -> List[int]:
    N = 1 << n
    infl = [0] * n
    for x in range(N):
        fx = (tt >> x) & 1
        for j in range(n):
            if fx != ((tt >> (x ^ (1 << j))) & 1):
                infl[j] += 1
    return infl


def feature_vector(tt: int, n: int) -> Tuple[int, ...]:
    """Le feature costruttive di una funzione: (influenza totale, bias, max/min
    influenza di coordinata). Tutte calcolabili in tempo polinomiale in N."""
    ci = _coord_influences(tt, n)
    return (total_influence(tt, n), _bias(tt, n), max(ci), min(ci))


FEATURE_NAMES = ("infl_tot", "bias", "infl_max", "infl_min")


# ── min-error decision tree di profondità ≤ d sulle feature ───────────────

def _min_error(items: Sequence[Tuple[Tuple[int, ...], bool]], depth: int,
               num_features: int) -> int:
    """Numero minimo di errori di un albero di decisione di profondità ≤ depth.

    items = lista di (feature_vector, label). Foglia = predice la maggioranza
    (errore = dimensione della minoranza). Split = una soglia su una feature.
    """
    if not items:
        return 0
    pos = sum(1 for _, lab in items if lab)
    baseline = min(pos, len(items) - pos)        # errore predicendo la maggioranza
    if depth == 0 or baseline == 0:
        return baseline
    best = baseline
    for f in range(num_features):
        values = sorted({fv[f] for fv, _ in items})
        for k in range(len(values) - 1):
            thr = (values[k] + values[k + 1]) / 2
            left = [(fv, lab) for fv, lab in items if fv[f] <= thr]
            right = [(fv, lab) for fv, lab in items if fv[f] > thr]
            err = _min_error(left, depth - 1, num_features) + \
                _min_error(right, depth - 1, num_features)
            if err < best:
                best = err
                if best == 0:
                    return 0
    return best


@dataclass
class RecognizeError:
    s: int
    depth: int                # budget di risorse della classe
    stratum_size: int         # quante funzioni nello strato misurato
    min_errors: int           # errori della miglior proprietà della classe
    error_rate: float         # = min_errors / stratum_size


def recognize_error(size_map: Dict[int, int], n: int, s: int, depth: int,
                    stratum: Sequence[int] | None = None) -> RecognizeError:
    """Errore della miglior proprietà costruttiva (alberi prof. ≤ depth) nel
    distinguere {size > s} da {size ≤ s} sullo strato dato.

    ``size_map``: funzione → dimensione esatta (la misura condivisa). ``stratum``:
    sottoinsieme di funzioni su cui misurare (default: tutte). Per la metrica
    stratificata, passare la finestra critica attorno a s.
    """
    keys = list(stratum) if stratum is not None else list(size_map.keys())
    items = [(feature_vector(t, n), size_map[t] > s) for t in keys]
    err = _min_error(items, depth, len(FEATURE_NAMES))
    total = len(items) or 1
    return RecognizeError(
        s=s, depth=depth, stratum_size=len(items),
        min_errors=err, error_rate=err / total,
    )


def price_of_constructivity(size_map: Dict[int, int], n: int, s: int,
                            max_depth: int = 3,
                            stratum: Sequence[int] | None = None
                            ) -> List[RecognizeError]:
    """La curva errore(d): quanto migliora la lente 'riconoscere' aumentando le
    risorse. L'errore residuo a d piccolo è il prezzo della costruttività."""
    return [recognize_error(size_map, n, s, d, stratum) for d in range(max_depth + 1)]


# ── la finestra critica (metrica stratificata, fix i) ─────────────────────

def critical_window(size_map: Dict[int, int], s: int, half_width: int = 1) -> List[int]:
    """Le funzioni con dimensione nella banda [s−w, s+w]: lo strato dove la
    decisione 'dura?' è non banale, fuori dal bulk che la concentrazione rende
    triviale. È qui che il difetto, se è strutturale, deve sopravvivere."""
    lo, hi = s - half_width, s + half_width
    return [t for t, c in size_map.items() if lo <= c <= hi]
