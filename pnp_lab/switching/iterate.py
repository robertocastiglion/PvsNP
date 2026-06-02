"""Switching ITERATO in profondità d — far collassare un AC0, livello dopo livello.

Il Modulo 8 base applica UNA restrizione e mostra che una DNF (profondità 2)
si appiattisce. Qui iteriamo: ad ogni round applichiamo una nuova restrizione
casuale alle variabili ancora libere e rimisuriamo la profondità dell'albero di
decisione della funzione superstite. È l'induzione di Håstad resa eseguibile:

    profondità d  ──ρ₁──▶  d-1  ──ρ₂──▶  d-2  ──▶ ... ──▶  costante.

Ogni round "consuma" un livello del circuito: il blocco di profondità 2 al fondo
(largo ≤ w) switcha a un albero di decisione poco profondo (Håstad: prob.
≥ 1-(5pw)^s di profondità ≤ s), che si riscrive con poca larghezza e si FONDE col
livello sopra, abbassando la profondità di 1. Dopo d-1 round l'intero AC0 dipende
da pochissime variabili: è quasi costante.

La PARITÀ no. Ristretta resta la parità delle variabili libere, e il suo albero
di decisione ha profondità ESATTAMENTE pari al numero di variabili libere — round
dopo round. Non collassa mai. Da qui la separazione quantitativa: un AC0 di
profondità d collassa sotto la soglia che la parità, invece, mantiene; quindi
nessun AC0 piccolo calcola la parità.

Misura esatta su n piccolo (tabella di verità + albero di decisione ottimo):
nessuna approssimazione, tutto verificabile.
"""

from __future__ import annotations

import math
import random
from dataclasses import dataclass, field
from typing import Callable, Dict, List, Optional, Sequence, Tuple

from .circuit import AC0Circuit, parity_as_dnf, random_ac0
from .decision_tree import optimal_dt_depth
from .restriction import parity_value, tabulate

Evaluator = Callable[[Sequence[int]], int]

# ── Palette "System Ignition" ────────────────────────────────────────────
_BG = "#0A0502"
_FG = "#FCF2E6"
_ORANGE = "#FF8012"
_GREEN = "#4AF626"
_RED = "#D73434"
_ASH = "#876244"


@dataclass
class RoundStat:
    """Statistiche aggregate su un round di restrizione (media su molti trial)."""

    round: int
    p: float
    avg_free: float          # numero medio di variabili ancora libere
    avg_dt_depth: float      # profondità DT media della funzione superstite
    max_dt_depth: int        # profondità DT massima osservata
    collapsed_frac: float    # frazione di trial con profondità ≤ soglia di collasso


@dataclass
class IterationResult:
    """Esito dello switching iterato per UNA funzione lungo uno schedule."""

    n: int
    schedule: Tuple[float, ...]
    collapse_threshold: int
    rounds: List[RoundStat] = field(default_factory=list)

    @property
    def final_collapsed_frac(self) -> float:
        return self.rounds[-1].collapsed_frac if self.rounds else 0.0


def _one_trial_joint(
    evaluators: Dict[str, Evaluator], n: int, schedule: Sequence[float], rng: random.Random
) -> List[Tuple[int, Dict[str, int]]]:
    """Un singolo trial condiviso: la STESSA restrizione cumulativa per tutti.

    Restituisce, round per round, ``(numero_liberi, {nome: profondità_DT})``
    misurando ogni valutatore sotto la MEDESIMA ρ — così il confronto è esatto
    (in particolare #liberi è identico per tutte le funzioni).
    """
    rho: List[Optional[int]] = [None] * n
    out: List[Tuple[int, Dict[str, int]]] = []
    for p in schedule:
        # ogni variabile ancora libera resta libera con prob. p, altrimenti 0/1
        for v in range(n):
            if rho[v] is None and rng.random() >= p:
                rho[v] = 1 if rng.random() < 0.5 else 0
        free = [v for v in range(n) if rho[v] is None]
        depths = {name: optimal_dt_depth(tabulate(ev, tuple(rho))[0]) for name, ev in evaluators.items()}
        out.append((len(free), depths))
    return out


def iterate_collapse_joint(
    evaluators: Dict[str, Evaluator],
    n: int,
    schedule: Sequence[float],
    rng: random.Random,
    *,
    trials: int = 200,
    collapse_threshold: int = 1,
) -> Dict[str, IterationResult]:
    """Switching iterato su più funzioni sotto la STESSA sequenza di restrizioni.

    Garantisce che ``avg_free`` sia identico per tutte le funzioni (stessa ρ): è
    ciò che rende esatta l'osservazione «D(parità) = #liberi a ogni round».
    """
    sched = tuple(schedule)
    names = list(evaluators)
    per_round_free: List[List[int]] = [[] for _ in sched]
    per_round_depth: Dict[str, List[List[int]]] = {nm: [[] for _ in sched] for nm in names}
    for _ in range(trials):
        for ri, (free, depths) in enumerate(_one_trial_joint(evaluators, n, sched, rng)):
            per_round_free[ri].append(free)
            for nm in names:
                per_round_depth[nm][ri].append(depths[nm])

    results: Dict[str, IterationResult] = {}
    for nm in names:
        rounds: List[RoundStat] = []
        for ri, p in enumerate(sched):
            depths = per_round_depth[nm][ri]
            frees = per_round_free[ri]
            rounds.append(
                RoundStat(
                    round=ri + 1,
                    p=p,
                    avg_free=sum(frees) / len(frees),
                    avg_dt_depth=sum(depths) / len(depths),
                    max_dt_depth=max(depths),
                    collapsed_frac=sum(1 for d in depths if d <= collapse_threshold) / len(depths),
                )
            )
        results[nm] = IterationResult(
            n=n, schedule=sched, collapse_threshold=collapse_threshold, rounds=rounds
        )
    return results


def iterate_collapse(
    evaluator: Evaluator,
    n: int,
    schedule: Sequence[float],
    rng: random.Random,
    *,
    trials: int = 200,
    collapse_threshold: int = 1,
) -> IterationResult:
    """Switching iterato su una funzione qualunque, lungo uno schedule di p.

    Ad ogni round la restrizione è CUMULATIVA (le variabili già fissate restano
    fissate). Misura, per round, profondità DT media/massima e la frazione di
    trial in cui la funzione è "collassata" (profondità ≤ ``collapse_threshold``).
    """
    return iterate_collapse_joint(
        {"f": evaluator}, n, schedule, rng, trials=trials, collapse_threshold=collapse_threshold
    )["f"]


def default_schedule(depth: int, bottom_fanin: int) -> Tuple[float, ...]:
    """Schedule di Håstad: d-1 round con p = 1/(5w) (così 5·p·w = 1 al fondo)."""
    w = max(1, bottom_fanin)
    p = 1.0 / (5.0 * w)
    return tuple(p for _ in range(max(1, depth - 1)))


def depth_reduction_demo(
    circuit: AC0Circuit,
    rng: random.Random,
    *,
    trials: int = 200,
    schedule: Optional[Sequence[float]] = None,
    collapse_threshold: int = 1,
) -> Tuple[IterationResult, IterationResult]:
    """Fa passare circuito AC0 e parità per lo STESSO schedule.

    Restituisce ``(ac0_result, parity_result)``: l'AC0 collassa verso 0, la
    parità resta sulla diagonale (profondità = #liberi). Lo schedule predefinito
    è quello di Håstad per la profondità e il fan-in del circuito.
    """
    sched = tuple(schedule) if schedule is not None else default_schedule(
        circuit.depth, circuit.bottom_fanin
    )
    res = iterate_collapse_joint(
        {"AC0": circuit.as_evaluator(), "parità": parity_value},
        circuit.n, sched, rng,
        trials=trials, collapse_threshold=collapse_threshold,
    )
    return res["AC0"], res["parità"]


# ─────────────────────────────────────────────────────────────────────────
#  Chiusura quantitativa di «parità ∉ AC0»
# ─────────────────────────────────────────────────────────────────────────
@dataclass
class ParityBound:
    """Il conto quantitativo dietro «parità ∉ AC0» a profondità d (forma di Håstad)."""

    n: int
    depth: int
    p: float                 # probabilità di sopravvivenza per round
    rounds: int              # = d - 1
    expected_survivors: float  # n · p^(d-1): variabili libere attese alla fine
    fanin_threshold: float   # larghezza w al fondo necessaria perché un AC0 collassi sotto i survivors
    size_lower_bound: float  # 2^(Ω(n^{1/(d-1)})): la dimensione minima (forma citata di Håstad)


def parity_lower_bound(n: int, depth: int) -> ParityBound:
    """Il conto che chiude quantitativamente «parità ∉ AC0».

    Argomento (eseguibile nelle parti finite, citato nella costante asintotica):

      • Con d-1 restrizioni che tengono ogni variabile con prob. p, sopravvivono
        in media  n·p^(d-1)  variabili libere.
      • Lo switching iterato fa collassare un AC0 di profondità d e fan-in w al
        fondo a un albero di decisione di profondità < (variabili libere) appena
        5·p·w < 1, cioè  w < 1/(5p).
      • La parità sulle k variabili libere ha invece profondità DT = k, SEMPRE.

    Perché la parità NON collassi serve che le superstiti k > soglia: imponendo
    p = 1/(5w) e n·p^(d-1) > w si ottiene la classica  w ≳ n^{1/d}/5  e quindi la
    dimensione  S ≥ 2^{Ω(n^{1/(d-1)})}  (teorema di Håstad, forma citata).
    """
    if depth < 2:
        raise ValueError("la profondità deve essere ≥ 2")
    rounds = depth - 1
    # soglia di fan-in che bilancia n·p^(d-1) = w con p = 1/(5w): w^d = n / 5^(d-1)
    fanin_threshold = (n / (5.0 ** rounds)) ** (1.0 / depth)
    p = 1.0 / (5.0 * max(fanin_threshold, 1e-12))
    expected_survivors = n * (p ** rounds)
    # forma citata di Håstad: S ≥ 2^( (1/10) · n^{1/(d-1)} )
    exponent = (1.0 / 10.0) * (n ** (1.0 / rounds)) if rounds >= 1 else 0.0
    size_lower_bound = 2.0 ** exponent
    return ParityBound(
        n=n, depth=depth, p=p, rounds=rounds,
        expected_survivors=expected_survivors,
        fanin_threshold=fanin_threshold,
        size_lower_bound=size_lower_bound,
    )


# ─────────────────────────────────────────────────────────────────────────
#  Report ASCII / SVG
# ─────────────────────────────────────────────────────────────────────────
def ascii_report(ac0: IterationResult, parity: IterationResult, *, label: str = "AC0") -> str:
    lines = [
        f"  Switching ITERATO in profondità — {label} vs parità  (n={ac0.n})",
        "  " + "─" * 66,
        f"  schedule p per round: {', '.join(f'{p:.3f}' for p in ac0.schedule)}",
        f"  soglia di collasso: profondità DT ≤ {ac0.collapse_threshold}",
        "",
        f"  {'round':>5}  {'p':>6}  {'#liberi':>8}  {'D('+label+')':>10}  {'D(parità)':>10}  {'collasso '+label:>14}",
    ]
    for ra, rp in zip(ac0.rounds, parity.rounds):
        lines.append(
            f"  {ra.round:>5}  {ra.p:>6.3f}  {ra.avg_free:>8.2f}  "
            f"{ra.avg_dt_depth:>10.2f}  {rp.avg_dt_depth:>10.2f}  {ra.collapsed_frac:>13.0%}"
        )
    lines += [
        "  " + "─" * 66,
        f"  {label}: la profondità crolla round dopo round → {ac0.final_collapsed_frac:.0%} collassato.",
        "  parità: la profondità resta = #variabili libere (segue la diagonale).",
        "  ⇒ l'AC0 si appiattisce, la parità no: parità ∉ AC0.",
    ]
    return "\n".join(lines)


def bound_report(bound: ParityBound) -> str:
    return "\n".join(
        [
            f"  Chiusura quantitativa — parità ∉ AC0  (n={bound.n}, profondità d={bound.depth})",
            "  " + "─" * 66,
            f"  round di restrizione (d-1) ........ {bound.rounds}",
            f"  p di sopravvivenza per round ...... {bound.p:.4f}",
            f"  variabili libere attese alla fine . {bound.expected_survivors:.2f}",
            f"  soglia di fan-in al fondo (w) ..... {bound.fanin_threshold:.2f}",
            f"  dimensione minima (Håstad) ........ 2^({math.log2(bound.size_lower_bound):.2f}) "
            f"≈ {bound.size_lower_bound:.3g}",
            "  " + "─" * 66,
            "  Un AC0 con w sotto la soglia collassa sotto le variabili superstiti;",
            "  la parità le mantiene tutte ⇒ nessun AC0 piccolo calcola la parità.",
        ]
    )


def _ratio(r: RoundStat) -> float:
    """Frazione di variabili libere che vanno ancora lette: D / #liberi (∈ [0,1])."""
    return (r.avg_dt_depth / r.avg_free) if r.avg_free > 1e-12 else 0.0


def to_svg_trajectory(
    ac0: IterationResult, parity: IterationResult, *,
    width: int = 900, height: int = 500, label: str = "AC0",
) -> str:
    """Traiettoria del rapporto D/#liberi round dopo round.

    Si plotta la FRAZIONE di variabili superstiti che la funzione deve ancora
    leggere (D diviso #liberi): così la parità è una retta piatta a 1.0 (deve
    leggerle tutte, sempre), mentre l'AC0 crolla verso 0. È la visualizzazione
    onesta: la parità non scende, l'AC0 sì — anche se in assoluto #liberi cala.
    """
    pad_l, pad_r, pad_t, pad_b = 70, 30, 100, 64
    plot_w = width - pad_l - pad_r
    plot_h = height - pad_t - pad_b
    rounds = list(range(len(ac0.rounds)))
    if not rounds:
        rounds = [0]
    rmax = max(rounds) or 1
    dmax = 1.0  # rapporto ∈ [0,1]

    def X(r: int) -> float:
        return pad_l + plot_w * (r / rmax)

    def Y(d: float) -> float:
        return pad_t + plot_h * (1 - d / dmax)

    base_y = pad_t + plot_h
    p: List[str] = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" '
        f'font-family="Inter, Segoe UI, system-ui, sans-serif">',
        f'<rect width="{width}" height="{height}" fill="{_BG}"/>',
        f'<text x="{pad_l}" y="40" fill="{_ORANGE}" font-size="13" '
        f'font-family="ui-monospace, Consolas, monospace" letter-spacing="2">'
        f'&gt; SWITCHING ITERATO // profondità d, livello dopo livello</text>',
        f'<text x="{pad_l}" y="68" fill="{_FG}" font-size="22" font-weight="700">'
        f'L\'AC0 si appiattisce round dopo round — la parità no</text>',
        f'<line x1="{pad_l}" y1="{base_y}" x2="{pad_l+plot_w}" y2="{base_y}" stroke="{_ASH}"/>',
        f'<line x1="{pad_l}" y1="{pad_t}" x2="{pad_l}" y2="{base_y}" stroke="{_ASH}"/>',
        # riferimenti orizzontali 0 e 1
        f'<line x1="{pad_l}" y1="{Y(1.0):.0f}" x2="{pad_l+plot_w}" y2="{Y(1.0):.0f}" '
        f'stroke="{_ASH}" stroke-dasharray="3 5" opacity="0.5"/>',
        f'<text x="{pad_l-8}" y="{Y(1.0)+4:.0f}" fill="{_ASH}" font-size="11" text-anchor="end">1.0</text>',
        f'<text x="{pad_l-8}" y="{Y(0.0)+4:.0f}" fill="{_ASH}" font-size="11" text-anchor="end">0.0</text>',
    ]
    pts_par = " ".join(f"{X(r):.0f},{Y(_ratio(parity.rounds[r])):.0f}" for r in rounds)
    p.append(f'<polyline points="{pts_par}" fill="none" stroke="{_RED}" stroke-width="3"/>')
    for r in rounds:
        p.append(f'<circle cx="{X(r):.0f}" cy="{Y(_ratio(parity.rounds[r])):.0f}" r="4" fill="{_RED}"/>')
    pts_ac0 = " ".join(f"{X(r):.0f},{Y(_ratio(ac0.rounds[r])):.0f}" for r in rounds)
    p.append(f'<polyline points="{pts_ac0}" fill="none" stroke="{_GREEN}" stroke-width="3"/>')
    for r in rounds:
        p.append(f'<circle cx="{X(r):.0f}" cy="{Y(_ratio(ac0.rounds[r])):.0f}" r="4" fill="{_GREEN}"/>')
    for r in rounds:
        p.append(f'<text x="{X(r):.0f}" y="{base_y+22:.0f}" fill="{_ASH}" font-size="12" '
                 f'text-anchor="middle">{r+1}</text>')
    p.append(f'<text x="{pad_l+plot_w/2:.0f}" y="{height-20}" fill="{_ASH}" font-size="12" '
             f'text-anchor="middle">round di restrizione (un livello consumato per round)</text>')
    p.append(f'<text x="{pad_l-50}" y="{pad_t+plot_h/2:.0f}" fill="{_ASH}" font-size="12" '
             f'text-anchor="middle" transform="rotate(-90 {pad_l-50} {pad_t+plot_h/2:.0f})">'
             f'variabili da leggere / variabili libere (D ÷ #liberi)</text>')
    p.append(f'<rect x="{pad_l+plot_w-200:.0f}" y="{pad_t}" width="12" height="12" fill="{_RED}"/>')
    p.append(f'<text x="{pad_l+plot_w-182:.0f}" y="{pad_t+11}" fill="{_FG}" font-size="13">parità (= 1.0, le legge tutte)</text>')
    p.append(f'<rect x="{pad_l+plot_w-200:.0f}" y="{pad_t+22:.0f}" width="12" height="12" fill="{_GREEN}"/>')
    p.append(f'<text x="{pad_l+plot_w-182:.0f}" y="{pad_t+33:.0f}" fill="{_FG}" font-size="13">{label} (→ 0, collassa)</text>')
    p.append("</svg>")
    return "\n".join(p)


def iterate_summary() -> str:
    """La morale dello switching iterato, con il confine di onestà."""
    return "\n".join(
        [
            "=" * 72,
            "  SWITCHING ITERATO IN PROFONDITÀ d  →  parità ∉ AC0, quantitativo",
            "=" * 72,
            "  Un round di switching abbassa la profondità di 1: il blocco di",
            "  profondità 2 al fondo (largo ≤ w) switcha a un albero poco profondo e si",
            "  fonde col livello sopra. Iterando d-1 volte, un AC0 di profondità d",
            "  collassa a qualcosa che dipende da pochissime variabili.",
            "",
            "  La parità non collassa MAI: ristretta resta parità delle variabili",
            "  libere, profondità DT = #liberi, round dopo round. Lo VEDIAMO nella",
            "  traiettoria: la curva AC0 scende a zero, quella della parità resta alta.",
            "",
            "  Confine di onestà. Eseguiamo in modo ESATTO (tabella di verità + albero",
            "  ottimo) il collasso iterato e la sopravvivenza della parità, e la parte",
            "  finita del conto quantitativo. La costante asintotica della forma",
            "  S ≥ 2^{Ω(n^{1/(d-1)})} è il teorema di Håstad: quella la CITIAMO.",
            "  E, come sempre: questo non risolve P vs NP — è un lower bound che",
            "  funziona davvero, contro una classe ristretta (AC0).",
            "=" * 72,
        ]
    )
