"""
Analisi della **crescita** della dimensione delle prove + visualizzazioni.

Mette in fila il costo della refutazione DPLL della piccionaia PHP^(n+1)_n al
crescere di n, stima il tasso di crescita (è esponenziale) e produce sia una
mini-tabella ASCII per il terminale sia un grafico SVG nei colori del brand per
la pagina divulgativa. Zero dipendenze.
"""
from __future__ import annotations

import math
from dataclasses import dataclass

from .dpll import DpllResult, dpll
from .formula import pigeonhole_cnf


@dataclass(frozen=True)
class GrowthRow:
    holes: int
    pigeons: int
    num_vars: int
    num_clauses: int
    tree_nodes: int
    seconds: float
    aborted: bool


@dataclass
class GrowthStudy:
    rows: list[GrowthRow]

    @property
    def growth_factor(self) -> float | None:
        """Fattore moltiplicativo medio dei nodi tra n e n+1 (media geometrica).

        Se i nodi crescono di un fattore ~costante > 1 a ogni passo, la crescita
        è esponenziale. Usa solo le righe non interrotte.
        """
        good = [r for r in self.rows if not r.aborted and r.tree_nodes > 0]
        if len(good) < 2:
            return None
        ratios = [
            good[i + 1].tree_nodes / good[i].tree_nodes
            for i in range(len(good) - 1)
        ]
        prod = 1.0
        for r in ratios:
            prod *= r
        return prod ** (1.0 / len(ratios))

    def verdict(self) -> str:
        gf = self.growth_factor
        if gf is None:
            return "dati insufficienti per stimare la crescita"
        if gf > 1.6:
            return (
                f"crescita ESPONENZIALE: ~×{gf:.1f} nodi a ogni piccione in più. "
                "È il teorema di Haken (1985) reso tangibile: la refutazione per "
                "resolution della piccionaia esplode."
            )
        return f"crescita moderata (fattore ~×{gf:.1f})"


def run_growth_study(max_holes: int = 6, node_budget: int = 2_000_000,
                     time_budget: float = 4.0) -> GrowthStudy:
    """Refuta PHP^(h+1)_h (insoddisfacibile) per h = 1..max_holes.

    Si ferma in modo pulito quando una singola istanza supera il budget: quel
    punto stesso *è* il risultato — la prova è diventata troppo grande.
    """
    rows: list[GrowthRow] = []
    for holes in range(1, max_holes + 1):
        pigeons = holes + 1  # un piccione di troppo => INSODDISFACIBILE
        cnf = pigeonhole_cnf(pigeons, holes)
        res: DpllResult = dpll(cnf, node_budget=node_budget, time_budget=time_budget)
        rows.append(GrowthRow(
            holes=holes, pigeons=pigeons,
            num_vars=cnf.num_vars, num_clauses=cnf.num_clauses,
            tree_nodes=res.tree_nodes, seconds=res.seconds, aborted=res.aborted,
        ))
        if res.aborted:
            break  # oltre questo punto è solo peggio
    return GrowthStudy(rows)


def ascii_chart(study: GrowthStudy, width: int = 40) -> str:
    """Tabella + barre in scala logaritmica per il terminale."""
    if not study.rows:
        return "(nessun dato)"
    max_log = max(math.log10(max(r.tree_nodes, 1)) for r in study.rows) or 1.0
    lines = [
        f"  {'PHP':>10}  {'vars':>5}  {'clausole':>8}  {'nodi':>10}  crescita",
        "  " + "─" * (38 + width),
    ]
    for r in study.rows:
        bar_len = int(round(width * math.log10(max(r.tree_nodes, 1)) / max_log))
        bar = "█" * bar_len
        php = f"{r.pigeons}/{r.holes}"
        flag = " *" if r.aborted else ""
        lines.append(
            f"  {php:>10}  {r.num_vars:>5}  {r.num_clauses:>8}  "
            f"{r.tree_nodes:>10}  {bar}{flag}"
        )
    return "\n".join(lines)


# ── Grafico SVG nei colori del brand "System Ignition" ───────────────────
_BG = "#0A0502"
_FG = "#FCF2E6"
_ORANGE = "#FF8012"
_RED = "#D73434"
_ASH = "#876244"


def to_svg(study: GrowthStudy, width: int = 900, height: int = 520) -> str:
    """Istogramma (scala log) dei nodi DPLL vs taglia della piccionaia."""
    rows = study.rows
    pad_l, pad_r, pad_t, pad_b = 70, 30, 90, 70
    plot_w = width - pad_l - pad_r
    plot_h = height - pad_t - pad_b
    n = len(rows)
    max_log = max((math.log10(max(r.tree_nodes, 1)) for r in rows), default=1.0) or 1.0

    p: list[str] = []
    p.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" '
        f'font-family="Inter, Segoe UI, system-ui, sans-serif">'
    )
    p.append(f'<rect width="{width}" height="{height}" fill="{_BG}"/>')
    p.append(
        f'<text x="{pad_l}" y="40" fill="{_ORANGE}" font-size="13" '
        f'font-family="ui-monospace, Consolas, monospace" letter-spacing="2">'
        f'&gt; PROOF COMPLEXITY // piccionaia</text>'
    )
    p.append(
        f'<text x="{pad_l}" y="68" fill="{_FG}" font-size="22" font-weight="700">'
        f'Dimensione della prova (resolution) — scala logaritmica</text>'
    )

    # assi
    base_y = pad_t + plot_h
    p.append(f'<line x1="{pad_l}" y1="{base_y}" x2="{pad_l+plot_w}" y2="{base_y}" '
             f'stroke="{_ASH}" stroke-width="1"/>')
    p.append(f'<line x1="{pad_l}" y1="{pad_t}" x2="{pad_l}" y2="{base_y}" '
             f'stroke="{_ASH}" stroke-width="1"/>')

    # barre
    if n:
        slot = plot_w / n
        bw = slot * 0.6
        for i, r in enumerate(rows):
            h = plot_h * (math.log10(max(r.tree_nodes, 1)) / max_log)
            x = pad_l + i * slot + (slot - bw) / 2
            y = base_y - h
            col = _RED if r.aborted else _ORANGE
            p.append(f'<rect x="{x:.0f}" y="{y:.0f}" width="{bw:.0f}" height="{h:.0f}" '
                     f'fill="{col}" opacity="0.88"/>')
            # valore sopra la barra
            p.append(f'<text x="{x + bw/2:.0f}" y="{y - 8:.0f}" fill="{_FG}" '
                     f'font-size="12" font-weight="600" text-anchor="middle">'
                     f'{r.tree_nodes}</text>')
            # etichetta asse x
            p.append(f'<text x="{x + bw/2:.0f}" y="{base_y + 22:.0f}" fill="{_ASH}" '
                     f'font-size="12" text-anchor="middle">{r.pigeons}/{r.holes}</text>')

    p.append(f'<text x="{pad_l + plot_w/2:.0f}" y="{height - 24}" fill="{_ASH}" '
             f'font-size="12" text-anchor="middle">piccioni / buche</text>')
    p.append(f'<text x="{pad_l - 50}" y="{pad_t + plot_h/2:.0f}" fill="{_ASH}" '
             f'font-size="12" text-anchor="middle" '
             f'transform="rotate(-90 {pad_l - 50} {pad_t + plot_h/2:.0f})">'
             f'nodi DPLL (log)</text>')
    p.append("</svg>")
    return "\n".join(p)


def write_svg(study: GrowthStudy, path: str) -> str:
    with open(path, "w", encoding="utf-8") as f:
        f.write(to_svg(study))
    return path
