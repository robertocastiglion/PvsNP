"""Narrazione + SVG dei due mondi algebrici (colori del brand).

Una figura: "potenza vs limite". A sinistra il numero di query per rilevare un
bit piantato (booleano = 2^m, algebrico = 1). A destra il lower bound di
interpolazione: finché le query restano < 2^m, l'oracolo resta indeterminato.
"""

from __future__ import annotations

import math
from typing import List

from .worlds import InterpolationBound, PlantedDetection

# ── Palette "System Ignition" ────────────────────────────────────────────
_BG = "#0A0502"
_FG = "#FCF2E6"
_ORANGE = "#FF8012"
_GREEN = "#4AF626"
_RED = "#D73434"
_ASH = "#876244"


def ascii_power(det: PlantedDetection) -> str:
    lines = [
        f"  MONDO 1 — potenza: rilevare 1 bit piantato (m={det.m} bit, GF({det.p}))",
        "  " + "─" * 60,
        f"  query BOOLEANE:  servono fino a 2^{det.m} = {1 << det.m} "
        f"(prob. per query = 1/2^{det.m} = {det.boolean_detect_prob_one_query:.4g})",
        f"  query ALGEBRICA: UNA sola, prob. rilevamento = "
        f"{det.algebraic_detect_prob:.4f}",
        f"                   ( = (1−1/p)^m esatto = {det.exact_prob_formula:.4f} )",
        f"  → l'estensione Ã è ≠ 0 su {det.algebraic_nonzero_points} punti su "
        f"{det.p ** det.m}: l'accesso algebrico è esponenzialmente più potente.",
    ]
    return "\n".join(lines)


def ascii_limit(bounds: List[InterpolationBound]) -> str:
    lines = [
        f"  MONDO 2 — limite: determinare l'oracolo (lower bound di interpolazione)",
        "  " + "─" * 60,
        f"  {'#query':>7}  {'rango':>6}  {'2^m':>5}  esito",
    ]
    for b in bounds:
        verdict = ("DETERMINATO" if b.determined
                   else f"INDETERMINATO (avversario differisce in {b.witness_cube_point})")
        lines.append(f"  {b.num_queries:>7}  {b.rank:>6}  {1 << b.m:>5}  {verdict}")
    lines.append("  → finché le query sono < 2^m esistono due oracoli indistinguibili.")
    return "\n".join(lines)


def to_svg_worlds(det: PlantedDetection, bounds: List[InterpolationBound],
                  width: int = 900, height: int = 480) -> str:
    """Due pannelli: potenza (query per rilevare) e limite (rango vs 2^m)."""
    pad_t = 96
    p: List[str] = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" '
        f'font-family="Inter, Segoe UI, system-ui, sans-serif">',
        f'<rect width="{width}" height="{height}" fill="{_BG}"/>',
        f'<text x="60" y="40" fill="{_ORANGE}" font-size="13" '
        f'font-family="ui-monospace, Consolas, monospace" letter-spacing="2">'
        f'&gt; ALGEBRAIC WORLDS // potenza e limite dell\'accesso algebrico</text>',
        f'<text x="60" y="68" fill="{_FG}" font-size="22" font-weight="700">'
        f'Una query algebrica vale 2^m booleane — ma servono 2^m per l\'oracolo</text>',
    ]

    # Pannello sinistro: query per rilevare il bit (scala log)
    lx, lw = 60, 360
    base_y = height - 60
    plot_h = base_y - pad_t
    boolean_q = 1 << det.m
    algebraic_q = 1
    peak = boolean_q
    p.append(f'<text x="{lx}" y="{pad_t-10}" fill="{_ASH}" font-size="12">query per rilevare il bit piantato</text>')
    p.append(f'<line x1="{lx}" y1="{base_y}" x2="{lx+lw}" y2="{base_y}" stroke="{_ASH}"/>')
    for i, (label, q, col) in enumerate([("booleano", boolean_q, _RED), ("algebrico", algebraic_q, _GREEN)]):
        h = plot_h * (math.log2(q + 1) / math.log2(peak + 1))
        h = max(h, 4)
        x = lx + 60 + i * 160
        p.append(f'<rect x="{x}" y="{base_y-h:.0f}" width="80" height="{h:.0f}" fill="{col}" opacity="0.9"/>')
        p.append(f'<text x="{x+40}" y="{base_y-h-8:.0f}" fill="{_FG}" font-size="13" font-weight="600" text-anchor="middle">{q}</text>')
        p.append(f'<text x="{x+40}" y="{base_y+20}" fill="{_ASH}" font-size="12" text-anchor="middle">{label}</text>')

    # Pannello destro: rango vs 2^m al crescere delle query
    rx, rw = 500, 360
    p.append(f'<text x="{rx}" y="{pad_t-10}" fill="{_ASH}" font-size="12">rango del sistema vs 2^m (soglia di determinazione)</text>')
    p.append(f'<line x1="{rx}" y1="{base_y}" x2="{rx+rw}" y2="{base_y}" stroke="{_ASH}"/>')
    target = 1 << det.m
    if bounds:
        slot = rw / len(bounds)
        bw = slot * 0.6
        for i, b in enumerate(bounds):
            h = plot_h * (b.rank / target)
            x = rx + i * slot + (slot - bw) / 2
            col = _GREEN if b.determined else _ORANGE
            p.append(f'<rect x="{x:.0f}" y="{base_y-h:.0f}" width="{bw:.0f}" height="{h:.0f}" fill="{col}" opacity="0.9"/>')
            p.append(f'<text x="{x+bw/2:.0f}" y="{base_y+20:.0f}" fill="{_ASH}" font-size="11" text-anchor="middle">{b.num_queries}</text>')
        # linea soglia 2^m
        y_thresh = base_y - plot_h
        p.append(f'<line x1="{rx}" y1="{y_thresh:.0f}" x2="{rx+rw}" y2="{y_thresh:.0f}" '
                 f'stroke="{_RED}" stroke-dasharray="6 4"/>')
        p.append(f'<text x="{rx+rw}" y="{y_thresh-6:.0f}" fill="{_RED}" font-size="11" '
                 f'text-anchor="end">2^m = {target} (determinato)</text>')
    p.append(f'<text x="{rx+rw/2:.0f}" y="{height-20}" fill="{_ASH}" font-size="12" '
             f'text-anchor="middle">numero di query algebriche</text>')
    p.append("</svg>")
    return "\n".join(p)


def write_svg(content: str, path: str) -> str:
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    return path
