"""M14 riparato verso (S): tre lenti non-tautologiche su una misura condivisa.

Risponde alla critica (V) del Modulo 14 con i tre interventi identificati:

  (iii) "dimostrare" = vera lunghezza di refutazione del lower bound in un sistema
        fissato (resolution tree-like), via SAT di sintesi — non più conteggio
        brute-force. Vedi ``synthesis_sat``.
  (ii)  "riconoscere" = minimo errore della miglior proprietà di una CLASSE a
        risorse limitate (alberi di decisione prof. ≤ d su feature costruttive) —
        non più una statistica arbitraria. Vedi ``recognize_class``.
  (i)   metrica STRATIFICATA sulla finestra critica attorno alla soglia — non la
        media uniforme che la concentrazione rende triviale.

Regimi di calcolabilità (onesti):
  • n=2: tutte e tre le lenti esatte sulla stessa misura (dimensione di circuito
    via SAT). 16 funzioni.
  • n=3: "riconoscere" esatta (su dimensione di formula M6, proxy); "dimostrare"
    esatta solo sullo strato a bassa complessità — sulle funzioni dure la
    refutazione ESPLODE (il muro reale della proof complexity), che registriamo.

Ri-verdetto: i due artefatti della v1 (tautologia; media che svanisce) sono
rimossi. Resta un errore RESIDUO non banale sulla metrica stratificata. Con n ≤ 3
calcolabile, però, l'invarianza asintotica NON è verificata: (S)-candidato, non (S).
"""

from __future__ import annotations

import random
from collections import Counter
from dataclasses import dataclass, field
from statistics import median
from typing import Dict, List, Optional

from .recognize_class import RecognizeError, critical_window, price_of_constructivity
from .synthesis_sat import circuit_size, refutation_length


# ── misura condivisa esatta via SAT (pratica per n=2) ─────────────────────

def shared_measure(n: int, cap: int = 6, node_budget: int = 50_000) -> Dict[int, int]:
    """Dimensione di circuito esatta di ogni funzione su n variabili, via SAT.

    Pratico per n=2 (16 funzioni). Per n=3 le funzioni dure esplodono: usare la
    dimensione di formula del Modulo 6 come proxy per la lente 'riconoscere'.
    """
    return {t: circuit_size(t, n, cap=cap, node_budget=node_budget).size
            for t in range(1 << (1 << n))}


# ── asse "dimostrare": lunghezze di refutazione reali ─────────────────────

@dataclass
class ProofAxisPoint:
    name: str
    n: int
    size: int
    threshold: int
    refutation_nodes: int
    is_lower_bound: bool
    aborted: bool


def proof_axis(samples: List[tuple], node_budget: int = 300_000) -> List[ProofAxisPoint]:
    """Per ogni (nome, tt, n): calcola la dimensione e la lunghezza di refutazione
    del lower bound a soglia size−1. Le funzioni con size ≥ 2 danno un lower bound
    vero; ``aborted`` segnala il muro (prova troppo lunga)."""
    out: List[ProofAxisPoint] = []
    for name, tt, n in samples:
        sz = circuit_size(tt, n, cap=6, node_budget=node_budget)
        if sz.size >= 1 and not sz.capped:
            pr = refutation_length(tt, n, sz.size - 1, node_budget=node_budget) \
                if sz.size >= 2 else None
            if pr is None:                        # size 1: lower bound banale (>0)
                out.append(ProofAxisPoint(name, n, sz.size, 0, 0, True, False))
            else:
                out.append(ProofAxisPoint(name, n, sz.size, sz.size - 1,
                                          pr.refutation_nodes, pr.is_lower_bound, pr.aborted))
        else:
            out.append(ProofAxisPoint(name, n, sz.size, sz.size, 0, False, True))
    return out


# ── asse "riconoscere": prezzo della costruttività sullo strato critico ───

@dataclass
class RecognizeAxis:
    n: int
    s: int
    window_size: int
    curve: List[RecognizeError]               # errore al variare della profondità d
    residual: float                            # errore alla massima profondità
    vanishes: bool                             # l'errore arriva a 0?


def recognize_axis(size_map: Dict[int, int], n: int, s: int,
                   max_depth: int = 3, half_width: int = 1,
                   sample: Optional[int] = None, seed: int = 0) -> RecognizeAxis:
    win = critical_window(size_map, s, half_width=half_width)
    used = win
    if sample is not None and len(win) > sample:
        used = random.Random(seed).sample(win, sample)
    curve = price_of_constructivity(size_map, n, s, max_depth=max_depth, stratum=used)
    residual = curve[-1].error_rate if curve else 0.0
    return RecognizeAxis(n=n, s=s, window_size=len(used), curve=curve,
                         residual=residual, vanishes=(residual == 0.0))


def relative_threshold(size_map: Dict[int, int], frac: float = 0.5) -> int:
    """Soglia RELATIVA: il quantile ``frac`` della distribuzione delle dimensioni.

    Una soglia assoluta fissa (es. s=3) non è comparabile tra n diversi: a n=3 è
    medio-bassa, a n=4 è banale. Per confrontare il residuo al variare di n serve
    ancorare s a un quantile della complessità (default: la mediana)."""
    vals = sorted(size_map.values())
    idx = min(len(vals) - 1, int(frac * len(vals)))
    return vals[idx]


@dataclass
class ScalingPoint:
    n: int
    threshold: int
    window_size: int
    residual: float


def residual_scaling(size_maps: Dict[int, Dict[int, int]], frac: float = 0.5,
                     max_depth: int = 3, half_width: int = 1,
                     sample: int = 300, seed: int = 0) -> List[ScalingPoint]:
    """Il residuo della lente 'riconoscere' a soglia RELATIVA (quantile ``frac``)
    al variare di n: il dato che discrimina (S) da (V). Finestre grandi campionate.

    ⚠ Con n piccolo calcolabile (≤4) restano pochi punti: tendenza, non prova di
    invarianza asintotica.
    """
    out: List[ScalingPoint] = []
    for n in sorted(size_maps):
        sm = size_maps[n]
        s = relative_threshold(sm, frac)
        ax = recognize_axis(sm, n, s, max_depth=max_depth, half_width=half_width,
                            sample=sample, seed=seed)
        out.append(ScalingPoint(n=n, threshold=s, window_size=ax.window_size,
                                residual=ax.residual))
    return out


# ── ri-verdetto ───────────────────────────────────────────────────────────

@dataclass
class Reverdict:
    classification: str
    tautology_removed: str
    vanishing_removed: str
    new_failure_mode: str
    open_point: str
    conclusion: str


def reverdict() -> Reverdict:
    return Reverdict(
        classification="(S)-candidato — non più (V), ma (S) non confermato.",
        tautology_removed="'dimostrare' ora è la lunghezza di refutazione reale in "
                          "resolution tree-like (es. XOR2: size>2 in 2055 nodi; AND3: "
                          "size>1 in 71 nodi) — non il conteggio brute-force.",
        vanishing_removed="'riconoscere' è il minimo errore di una CLASSE a risorse d "
                          "sulla finestra critica: a n=3 resta un residuo ~0.05 che NON "
                          "svanisce aumentando d — non la media uniforme che →0 per "
                          "concentrazione.",
        new_failure_mode="la lente 'dimostrare' sulle funzioni dure ESPLODE "
                         "(refutazione oltre budget, anche con CDCL): è il muro reale "
                         "della proof complexity, non un artefatto.",
        open_point="terzo punto (strada #1, solver CDCL + DP capped n=4): su finestre "
                   "interne il residuo CRESCE con n — n=2:0, n=3:~0.05, n=4:~0.17 — e a "
                   "n=4 è robusto su più soglie (non svanisce con le risorse). Caveat: "
                   "finestre n=4 sotto la mediana vera (size>8 fuori portata) e "
                   "campionate; residuo relativo alla classe di feature; 3 punti, non "
                   "invarianza asintotica.",
        conclusion="I due artefatti della v1 sono rimossi, il difetto non collassa più "
                   "trivialmente, e il terzo punto mostra un residuo CRESCENTE con n — "
                   "coerente con un prezzo strutturale della costruttività (natural "
                   "proofs). Ma per (S) confermato serve l'andamento al regime mediano e "
                   "per n→∞, fuori dalla portata del calcolo. Onesto: (S)-candidato "
                   "rafforzato, non (S).",
    )


@dataclass
class RepairedReport:
    measure_distribution: Dict[int, int]
    proof: List[ProofAxisPoint]
    recognize: List[RecognizeAxis]
    verdict: Reverdict = field(default_factory=reverdict)


def size_distribution(size_map: Dict[int, int]) -> Dict[int, int]:
    return dict(sorted(Counter(size_map.values()).items()))
