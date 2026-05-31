"""
Studio della complessità di circuito + visualizzazioni SVG (colori del brand).

Due immagini:
  1. **Spettro di Shannon** — istogramma della complessità di formula di TUTTE le
     funzioni su n variabili (default n=3): si vede che quasi tutte si
     ammassano sui valori alti, poche sono facili.
  2. **Muro della parità** — la DNF minima della parità cresce come 2^(n-1):
     un lower bound esatto che esplode.
"""
from __future__ import annotations

from dataclasses import dataclass

from .parity import parity_dnf_lower_bound
from .synthesis import ComplexityTable, min_formula_sizes

# ── Palette "System Ignition" ────────────────────────────────────────────
_BG = "#0A0502"
_FG = "#FCF2E6"
_ORANGE = "#FF8012"
_GREEN = "#4AF626"
_RED = "#D73434"
_ASH = "#876244"


@dataclass
class ParityGrowthRow:
    n: int
    dnf_terms: int
    tight: bool


def parity_growth(max_n: int = 7) -> list[ParityGrowthRow]:
    """DNF minima della parità per n = 2..max_n (verificata fino a dove è esatta)."""
    rows: list[ParityGrowthRow] = []
    for n in range(2, max_n + 1):
        lb = parity_dnf_lower_bound(n)
        rows.append(ParityGrowthRow(n=n, dnf_terms=lb.num_prime_implicants, tight=lb.is_tight))
    return rows


def ascii_distribution(ct: ComplexityTable, width: int = 44) -> str:
    """Istogramma ASCII della distribuzione delle complessità di formula."""
    dist = ct.distribution()
    if not dist:
        return "(nessun dato)"
    peak = max(dist.values())
    lines = [
        f"  Funzioni su n={ct.n} variabili: {ct.num_functions} totali, "
        f"complessità max = {ct.max_cost} gate",
        "  " + "─" * (width + 22),
        f"  {'taglia':>6}  {'funzioni':>8}  distribuzione",
    ]
    for size, count in dist.items():
        bar = "█" * max(1, round(width * count / peak))
        lines.append(f"  {size:>6}  {count:>8}  {bar}")
    return "\n".join(lines)


def to_svg_distribution(ct: ComplexityTable, width: int = 900, height: int = 500) -> str:
    """Istogramma SVG: quante funzioni hanno ciascuna complessità di formula."""
    dist = ct.distribution()
    pad_l, pad_r, pad_t, pad_b = 70, 30, 96, 64
    plot_w = width - pad_l - pad_r
    plot_h = height - pad_t - pad_b
    sizes = sorted(dist)
    peak = max(dist.values()) if dist else 1

    p: list[str] = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" '
        f'font-family="Inter, Segoe UI, system-ui, sans-serif">',
        f'<rect width="{width}" height="{height}" fill="{_BG}"/>',
        f'<text x="{pad_l}" y="40" fill="{_ORANGE}" font-size="13" '
        f'font-family="ui-monospace, Consolas, monospace" letter-spacing="2">'
        f'&gt; CIRCUIT COMPLEXITY // spettro di Shannon (n={ct.n})</text>',
        f'<text x="{pad_l}" y="68" fill="{_FG}" font-size="22" font-weight="700">'
        f'Quante funzioni hanno ciascuna complessità di formula</text>',
    ]
    base_y = pad_t + plot_h
    p.append(f'<line x1="{pad_l}" y1="{base_y}" x2="{pad_l+plot_w}" y2="{base_y}" '
             f'stroke="{_ASH}"/>')
    p.append(f'<line x1="{pad_l}" y1="{pad_t}" x2="{pad_l}" y2="{base_y}" stroke="{_ASH}"/>')

    if sizes:
        slot = plot_w / len(sizes)
        bw = slot * 0.66
        # la complessità di formula massima è la regione "difficile" → rosso
        hardest = max(sizes)
        for i, s in enumerate(sizes):
            c = dist[s]
            h = plot_h * (c / peak)
            x = pad_l + i * slot + (slot - bw) / 2
            y = base_y - h
            col = _RED if s == hardest else (_GREEN if s <= 1 else _ORANGE)
            p.append(f'<rect x="{x:.0f}" y="{y:.0f}" width="{bw:.0f}" height="{h:.0f}" '
                     f'fill="{col}" opacity="0.88"/>')
            p.append(f'<text x="{x+bw/2:.0f}" y="{y-8:.0f}" fill="{_FG}" font-size="12" '
                     f'font-weight="600" text-anchor="middle">{c}</text>')
            p.append(f'<text x="{x+bw/2:.0f}" y="{base_y+22:.0f}" fill="{_ASH}" '
                     f'font-size="12" text-anchor="middle">{s}</text>')

    p.append(f'<text x="{pad_l+plot_w/2:.0f}" y="{height-22}" fill="{_ASH}" '
             f'font-size="12" text-anchor="middle">dimensione di formula (gate ∧/∨)</text>')
    p.append(f'<text x="{pad_l-50}" y="{pad_t+plot_h/2:.0f}" fill="{_ASH}" font-size="12" '
             f'text-anchor="middle" transform="rotate(-90 {pad_l-50} {pad_t+plot_h/2:.0f})">'
             f'numero di funzioni</text>')
    p.append("</svg>")
    return "\n".join(p)


def to_svg_parity(rows: list[ParityGrowthRow], width: int = 900, height: int = 480) -> str:
    """Istogramma SVG della crescita 2^(n-1) della DNF minima della parità."""
    pad_l, pad_r, pad_t, pad_b = 70, 30, 96, 64
    plot_w = width - pad_l - pad_r
    plot_h = height - pad_t - pad_b
    peak = max((r.dnf_terms for r in rows), default=1)

    p: list[str] = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" '
        f'font-family="Inter, Segoe UI, system-ui, sans-serif">',
        f'<rect width="{width}" height="{height}" fill="{_BG}"/>',
        f'<text x="{pad_l}" y="40" fill="{_ORANGE}" font-size="13" '
        f'font-family="ui-monospace, Consolas, monospace" letter-spacing="2">'
        f'&gt; CIRCUIT COMPLEXITY // il muro della parità</text>',
        f'<text x="{pad_l}" y="68" fill="{_FG}" font-size="22" font-weight="700">'
        f'DNF minima della parità = 2^(n−1) termini (esatto)</text>',
    ]
    base_y = pad_t + plot_h
    p.append(f'<line x1="{pad_l}" y1="{base_y}" x2="{pad_l+plot_w}" y2="{base_y}" stroke="{_ASH}"/>')
    p.append(f'<line x1="{pad_l}" y1="{pad_t}" x2="{pad_l}" y2="{base_y}" stroke="{_ASH}"/>')

    if rows:
        slot = plot_w / len(rows)
        bw = slot * 0.6
        for i, r in enumerate(rows):
            h = plot_h * (r.dnf_terms / peak)
            x = pad_l + i * slot + (slot - bw) / 2
            y = base_y - h
            p.append(f'<rect x="{x:.0f}" y="{y:.0f}" width="{bw:.0f}" height="{h:.0f}" '
                     f'fill="{_ORANGE}" opacity="0.9"/>')
            p.append(f'<text x="{x+bw/2:.0f}" y="{y-8:.0f}" fill="{_FG}" font-size="12" '
                     f'font-weight="600" text-anchor="middle">{r.dnf_terms}</text>')
            p.append(f'<text x="{x+bw/2:.0f}" y="{base_y+22:.0f}" fill="{_ASH}" '
                     f'font-size="12" text-anchor="middle">n={r.n}</text>')

    p.append(f'<text x="{pad_l+plot_w/2:.0f}" y="{height-22}" fill="{_ASH}" '
             f'font-size="12" text-anchor="middle">numero di variabili</text>')
    p.append(f'<text x="{pad_l-50}" y="{pad_t+plot_h/2:.0f}" fill="{_ASH}" font-size="12" '
             f'text-anchor="middle" transform="rotate(-90 {pad_l-50} {pad_t+plot_h/2:.0f})">'
             f'termini DNF minimi</text>')
    p.append("</svg>")
    return "\n".join(p)


def write_svg(content: str, path: str) -> str:
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    return path
