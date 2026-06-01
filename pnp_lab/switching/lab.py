"""Lo switching lemma in azione: la DNF collassa, la parità no.

Esperimento. Si prende una DNF di larghezza w su n variabili, si applicano molte
restrizioni casuali (con '*' di probabilità p) e si misura la profondità
dell'albero di decisione della funzione ristretta. Lo switching lemma di Håstad
prevede

        Pr[ D(DNF|ρ) ≥ s ]  ≤  (5 p w)^s .

Per p < 1/(5w) il fattore 5pw < 1: la profondità crolla esponenzialmente in s —
la DNF "switcha" a un albero poco profondo. La parità, invece, ristretta resta
parità delle variabili libere: D(parità|ρ) = (numero di variabili libere),
SEMPRE. Non si semplifica: ecco perché parità ∉ AC0.
"""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass, field
from typing import Dict, List

from .decision_tree import optimal_dt_depth
from .restriction import (
    DNF,
    eval_dnf,
    free_vars,
    parity_value,
    random_restriction,
    tabulate,
)

# ── Palette "System Ignition" ────────────────────────────────────────────
_BG = "#0A0502"
_FG = "#FCF2E6"
_ORANGE = "#FF8012"
_GREEN = "#4AF626"
_RED = "#D73434"
_ASH = "#876244"


@dataclass
class SwitchingStats:
    n: int
    width: int
    p: float
    trials: int
    dnf_depth_hist: Dict[int, int] = field(default_factory=dict)        # D(DNF|ρ) → conteggio
    dnf_depth_by_free: Dict[int, List[int]] = field(default_factory=dict)  # #liberi → [D(DNF|ρ)]
    empirical_ge: Dict[int, float] = field(default_factory=dict)        # s → Pr[D ≥ s]
    bound: Dict[int, float] = field(default_factory=dict)               # s → (5pw)^s

    def avg_dnf_depth_by_free(self) -> Dict[int, float]:
        return {k: sum(v) / len(v) for k, v in sorted(self.dnf_depth_by_free.items())}


def run_switching(dnf: DNF, n: int, p: float, trials: int, rng, *, width: int, max_s: int = 4) -> SwitchingStats:
    """Applica `trials` restrizioni casuali e misura il collasso della DNF."""
    hist: Dict[int, int] = defaultdict(int)
    by_free: Dict[int, List[int]] = defaultdict(list)
    depths: List[int] = []
    for _ in range(trials):
        rho = random_restriction(n, p, rng)
        table, free = tabulate(lambda a: eval_dnf(dnf, a), rho)
        d = optimal_dt_depth(table)
        hist[d] += 1
        by_free[len(free)].append(d)
        depths.append(d)

    empirical_ge = {
        s: sum(1 for d in depths if d >= s) / trials for s in range(1, max_s + 1)
    }
    bound = {s: (5.0 * p * width) ** s for s in range(1, max_s + 1)}
    return SwitchingStats(
        n=n, width=width, p=p, trials=trials,
        dnf_depth_hist=dict(sorted(hist.items())),
        dnf_depth_by_free={k: by_free[k] for k in sorted(by_free)},
        empirical_ge=empirical_ge, bound=bound,
    )


def parity_depth_under_restriction(n: int, p: float, trials: int, rng) -> Dict[int, int]:
    """Per la parità: profondità DT = numero di variabili libere, sempre.

    Restituisce {numero_di_liberi: profondità_DT}. Verifica eseguendo l'albero
    ottimo (non si fida del teorema: lo controlla).
    """
    out: Dict[int, int] = {}
    for _ in range(trials):
        rho = random_restriction(n, p, rng)
        free = free_vars(rho)
        k = len(free)
        if k not in out:
            table, _ = tabulate(parity_value, rho)
            out[k] = optimal_dt_depth(table)   # risulterà == k
    return dict(sorted(out.items()))


def ascii_report(stats: SwitchingStats, parity_depth: Dict[int, int]) -> str:
    lines = [
        f"  Switching lemma — DNF larghezza w={stats.width}, n={stats.n} variabili, "
        f"p={stats.p}, {stats.trials} restrizioni",
        "  " + "─" * 66,
        f"  5·p·w = {5*stats.p*stats.width:.3f}  "
        f"({'< 1 → la DNF collassa' if 5*stats.p*stats.width < 1 else '≥ 1 → bound vacuo'})",
        "",
        f"  Bound di Håstad   Pr[D(DNF|ρ) ≥ s] ≤ (5pw)^s   vs   misura empirica:",
        f"  {'s':>3}  {'(5pw)^s':>12}  {'empirico':>10}  esito",
    ]
    for s in sorted(stats.bound):
        b = stats.bound[s]
        e = stats.empirical_ge[s]
        ok = "OK (empirico ≤ bound)" if e <= b + 1e-9 else "!! sopra il bound"
        lines.append(f"  {s:>3}  {b:>12.4f}  {e:>10.4f}  {ok}")
    lines += [
        "",
        "  Profondità DT media in funzione del numero di variabili libere:",
        f"  {'#liberi':>8}  {'DNF (media)':>12}  {'parità':>8}",
    ]
    avg = stats.avg_dnf_depth_by_free()
    for k in sorted(set(avg) | set(parity_depth)):
        a = f"{avg.get(k, float('nan')):.2f}" if k in avg else "—"
        pdep = str(parity_depth.get(k, "—"))
        lines.append(f"  {k:>8}  {a:>12}  {pdep:>8}")
    lines += [
        "  " + "─" * 66,
        "  La DNF resta piatta e bassa; la parità sale come la diagonale (=#liberi):",
        "  la parità NON si semplifica ⇒ parità ∉ AC0.",
    ]
    return "\n".join(lines)


def to_svg_contrast(stats: SwitchingStats, parity_depth: Dict[int, int],
                    width: int = 900, height: int = 500, min_samples: int = 10) -> str:
    """DT-depth media vs numero di variabili libere: parità (diagonale) vs DNF (piatta).

    Per la curva DNF si usano solo i gruppi con almeno ``min_samples`` restrizioni,
    così la media è significativa (evita gli outlier da pochissimi campioni).
    """
    pad_l, pad_r, pad_t, pad_b = 70, 30, 100, 64
    plot_w = width - pad_l - pad_r
    plot_h = height - pad_t - pad_b
    avg = {k: v for k, v in stats.avg_dnf_depth_by_free().items()
           if len(stats.dnf_depth_by_free.get(k, [])) >= min_samples}
    ks = sorted(set(avg) | {k for k in parity_depth if k in avg})
    if not ks:
        ks = [0]
    kmax = max(ks) or 1
    dmax = max([parity_depth.get(k, 0) for k in ks] + [1])

    def X(k: int) -> float:
        return pad_l + plot_w * (k / kmax)

    def Y(d: float) -> float:
        return pad_t + plot_h * (1 - d / dmax)

    p: List[str] = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" '
        f'font-family="Inter, Segoe UI, system-ui, sans-serif">',
        f'<rect width="{width}" height="{height}" fill="{_BG}"/>',
        f'<text x="{pad_l}" y="40" fill="{_ORANGE}" font-size="13" '
        f'font-family="ui-monospace, Consolas, monospace" letter-spacing="2">'
        f'&gt; SWITCHING LEMMA // la DNF collassa, la parità no</text>',
        f'<text x="{pad_l}" y="68" fill="{_FG}" font-size="22" font-weight="700">'
        f'Profondità dell\'albero di decisione vs variabili libere</text>',
    ]
    base_y = pad_t + plot_h
    p.append(f'<line x1="{pad_l}" y1="{base_y}" x2="{pad_l+plot_w}" y2="{base_y}" stroke="{_ASH}"/>')
    p.append(f'<line x1="{pad_l}" y1="{pad_t}" x2="{pad_l}" y2="{base_y}" stroke="{_ASH}"/>')

    # parità: diagonale D = #liberi (rossa = "muro")
    pts_par = " ".join(f"{X(k):.0f},{Y(parity_depth.get(k, k)):.0f}" for k in ks)
    p.append(f'<polyline points="{pts_par}" fill="none" stroke="{_RED}" stroke-width="3"/>')
    for k in ks:
        p.append(f'<circle cx="{X(k):.0f}" cy="{Y(parity_depth.get(k, k)):.0f}" r="4" fill="{_RED}"/>')

    # DNF: media (verde = "si semplifica")
    pts_dnf = " ".join(f"{X(k):.0f},{Y(avg.get(k, 0)):.0f}" for k in ks)
    p.append(f'<polyline points="{pts_dnf}" fill="none" stroke="{_GREEN}" stroke-width="3"/>')
    for k in ks:
        p.append(f'<circle cx="{X(k):.0f}" cy="{Y(avg.get(k, 0)):.0f}" r="4" fill="{_GREEN}"/>')

    # etichette assi + legenda
    for k in ks:
        p.append(f'<text x="{X(k):.0f}" y="{base_y+22:.0f}" fill="{_ASH}" font-size="12" '
                 f'text-anchor="middle">{k}</text>')
    p.append(f'<text x="{pad_l+plot_w/2:.0f}" y="{height-20}" fill="{_ASH}" font-size="12" '
             f'text-anchor="middle">numero di variabili libere dopo la restrizione</text>')
    p.append(f'<text x="{pad_l-50}" y="{pad_t+plot_h/2:.0f}" fill="{_ASH}" font-size="12" '
             f'text-anchor="middle" transform="rotate(-90 {pad_l-50} {pad_t+plot_h/2:.0f})">'
             f'profondità albero di decisione</text>')
    p.append(f'<rect x="{pad_l+plot_w-220:.0f}" y="{pad_t}" width="12" height="12" fill="{_RED}"/>')
    p.append(f'<text x="{pad_l+plot_w-202:.0f}" y="{pad_t+11}" fill="{_FG}" font-size="13">parità (= #liberi)</text>')
    p.append(f'<rect x="{pad_l+plot_w-220:.0f}" y="{pad_t+22:.0f}" width="12" height="12" fill="{_GREEN}"/>')
    p.append(f'<text x="{pad_l+plot_w-202:.0f}" y="{pad_t+33:.0f}" fill="{_FG}" font-size="13">DNF w={stats.width} (media)</text>')
    p.append("</svg>")
    return "\n".join(p)


def write_svg(content: str, path: str) -> str:
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    return path
