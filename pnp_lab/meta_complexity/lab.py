"""Visualizzazione: la soglia di MCSP (facili vs difficili) al variare di s."""

from __future__ import annotations

from typing import List

from .frontier import NaturalProofsLink, MagnificationFact
from .mcsp import ThresholdRow

# ── Palette "System Ignition" ────────────────────────────────────────────
_BG = "#0A0502"
_FG = "#FCF2E6"
_ORANGE = "#FF8012"
_GREEN = "#4AF626"
_RED = "#D73434"
_ASH = "#876244"


def ascii_threshold(rows: List[ThresholdRow], width: int = 40) -> str:
    total = rows[0].total if rows else 1
    lines = [
        f"  MCSP: funzioni 'facili' (dim ≤ s) vs 'difficili' (dim > s) — totale {total}",
        "  " + "─" * (width + 26),
        f"  {'s':>3}  {'facili':>7}  {'difficili':>9}  distribuzione (■ dure)",
    ]
    for r in rows:
        bar = "■" * max(0, round(width * r.hard / total))
        lines.append(f"  {r.s:>3}  {r.easy:>7}  {r.hard:>9}  {bar}")
    lines.append("  " + "─" * (width + 26))
    lines.append("  → per s piccolo le funzioni DURE dominano (Shannon); con n piccolo il")
    lines.append("    dominio è mite, a n grande la frazione dura → 1. Esibirne UNA esplicita")
    lines.append("    e dimostrabilmente dura resta il muro: il cuore di MCSP.")
    return "\n".join(lines)


def ascii_link(link: NaturalProofsLink) -> str:
    return "\n".join([
        f"  Legame MCSP ↔ Natural Proofs (soglia s = {link.s}):",
        f"    proprietà 'f è dura' — UTILE: {'sì' if link.useful else 'no'} · "
        f"LARGA: {link.large_fraction:.1%} delle funzioni",
        f"    costruttiva? {link.constructive_cost}",
        f"    ⇒ {link.conclusion}",
    ])


def to_svg_threshold(rows: List[ThresholdRow], width: int = 900, height: int = 480) -> str:
    """Curva: quante funzioni restano 'dure' (dim > s) al crescere di s."""
    pad_l, pad_r, pad_t, pad_b = 70, 30, 100, 64
    plot_w = width - pad_l - pad_r
    plot_h = height - pad_t - pad_b
    base_y = pad_t + plot_h
    total = rows[0].total if rows else 1

    def X(i): return pad_l + plot_w * (i / max(len(rows) - 1, 1))
    def Y(v): return base_y - plot_h * (v / total)

    p: List[str] = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" '
        f'font-family="Inter, Segoe UI, system-ui, sans-serif">',
        f'<rect width="{width}" height="{height}" fill="{_BG}"/>',
        f'<text x="{pad_l}" y="40" fill="{_ORANGE}" font-size="13" '
        f'font-family="ui-monospace, Consolas, monospace" letter-spacing="2">'
        f'&gt; META-COMPLEXITY // MCSP: la soglia facile/difficile</text>',
        f'<text x="{pad_l}" y="68" fill="{_FG}" font-size="22" font-weight="700">'
        f'Quante funzioni restano DURE (dim &gt; s) al crescere di s</text>',
    ]
    p.append(f'<line x1="{pad_l}" y1="{base_y}" x2="{pad_l+plot_w}" y2="{base_y}" stroke="{_ASH}"/>')
    p.append(f'<line x1="{pad_l}" y1="{pad_t}" x2="{pad_l}" y2="{base_y}" stroke="{_ASH}"/>')

    # area "dure" (rossa) e curva
    pts = [(X(i), Y(r.hard)) for i, r in enumerate(rows)]
    poly_pts = f"{pad_l},{base_y} " + " ".join(f"{x:.0f},{y:.0f}" for x, y in pts) + f" {X(len(rows)-1):.0f},{base_y}"
    p.append(f'<polygon points="{poly_pts}" fill="{_RED}" opacity="0.18"/>')
    p.append(f'<polyline points="{" ".join(f"{x:.0f},{y:.0f}" for x,y in pts)}" '
             f'fill="none" stroke="{_RED}" stroke-width="3"/>')
    for i, r in enumerate(rows):
        p.append(f'<circle cx="{X(i):.0f}" cy="{Y(r.hard):.0f}" r="4" fill="{_RED}"/>')
        p.append(f'<text x="{X(i):.0f}" y="{base_y+20:.0f}" fill="{_ASH}" font-size="11" '
                 f'text-anchor="middle">s={r.s}</text>')
    p.append(f'<text x="{pad_l+plot_w/2:.0f}" y="{height-16}" fill="{_ASH}" font-size="12" '
             f'text-anchor="middle">soglia di dimensione s · area rossa = funzioni dure</text>')
    p.append("</svg>")
    return "\n".join(p)


def write_svg(content: str, path: str) -> str:
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    return path
