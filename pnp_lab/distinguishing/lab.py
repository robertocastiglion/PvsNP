"""Visualizzazione del Modulo 15: la matrice ε(ℓ, s) come heatmap del trade-off.

Asse X = CALCOLO (numero di gate s), asse Y = INFORMAZIONE (fan-in ℓ). Il colore
è il vantaggio di distinzione ε. Si cerca il "confine" in cui servono SIMULTANEA-
mente ℓ e s alti.
"""

from __future__ import annotations

from typing import List

from .advantage import AdvantageMatrix, CellResult, frontier_note

# ── Palette "System Ignition" ────────────────────────────────────────────────
_BG = "#0A0502"
_FG = "#FCF2E6"
_ORANGE = "#FF8012"
_GREEN = "#4AF626"
_ASH = "#876244"
_DIM = "#3A2A1C"


def _fmt(c: CellResult) -> str:
    return ("≥" if not c.exact else " ") + f"{c.epsilon:.3f}"


def ascii_matrix(m: AdvantageMatrix) -> str:
    """La matrice ε(ℓ, s) a terminale (≥ = cota inferiore, classe troppo grande)."""
    sp = m.split
    lines = [
        f"  Vantaggio di distinzione ε(ℓ, s)  —  DURE (≥{sp.tau}) vs FACILI, n=3",
        f"  funzioni: {sp.n_hard} dure · {sp.n_easy} facili · complessità max {sp.max_cost}",
        "  " + "─" * 46,
        "        " + "  ".join(f"s={s}".rjust(7) for s in m.ss) + "    ← CALCOLO (gate)",
    ]
    for ell in m.ells:
        row = "  ".join(_fmt(m.get(ell, s)).rjust(7) for s in m.ss)
        lines.append(f"  ℓ={ell}   {row}")
    lines.append("  " + "─" * 46)
    lines.append("  ↑ INFORMAZIONE (fan-in oracle gate)   ·   ≥ = cota inferiore esatta")
    lines.append("")
    lines.append(frontier_note(m))
    return "\n".join(lines)


def _heat(eps: float, eps_max: float) -> str:
    """Interpola ash → arancione → verde in funzione di ε/ε_max."""
    if eps_max <= 0:
        return _DIM
    t = max(0.0, min(1.0, eps / eps_max))

    def lerp(a, b, u):
        return tuple(round(a[i] + (b[i] - a[i]) * u) for i in range(3))

    ash = (0x3A, 0x2A, 0x1C)
    orange = (0xFF, 0x80, 0x12)
    green = (0x4A, 0xF6, 0x26)
    if t < 0.5:
        r, g, b = lerp(ash, orange, t / 0.5)
    else:
        r, g, b = lerp(orange, green, (t - 0.5) / 0.5)
    return f"#{r:02X}{g:02X}{b:02X}"


def to_svg_matrix(m: AdvantageMatrix, width: int = 820, height: int = 560) -> str:
    """Heatmap 3×3 di ε(ℓ, s): X = calcolo s, Y = informazione ℓ."""
    pad_l, pad_r, pad_t, pad_b = 110, 40, 120, 90
    plot_w = width - pad_l - pad_r
    plot_h = height - pad_t - pad_b
    nx, ny = len(m.ss), len(m.ells)
    cw, ch = plot_w / nx, plot_h / ny
    eps_max = max(c.epsilon for c in m.cells.values()) or 1.0

    p: List[str] = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" '
        f'font-family="Inter, Segoe UI, system-ui, sans-serif">',
        f'<rect width="{width}" height="{height}" fill="{_BG}"/>',
        f'<text x="{pad_l}" y="42" fill="{_ORANGE}" font-size="13" '
        f'font-family="ui-monospace, Consolas, monospace" letter-spacing="2">'
        f'&gt; MODULO 15 // DISTINGUISHING ADVANTAGE</text>',
        f'<text x="{pad_l}" y="72" fill="{_FG}" font-size="22" font-weight="700">'
        f'ε(ℓ, s): servono insieme informazione e calcolo?</text>',
        f'<text x="{pad_l}" y="98" fill="{_ASH}" font-size="13">'
        f'distinguere {m.split.n_hard} funzioni DURE da {m.split.n_easy} FACILI '
        f'(n=3) · misura esatta su finite size</text>',
    ]

    # celle
    for yi, ell in enumerate(m.ells):
        for xi, s in enumerate(m.ss):
            c = m.get(ell, s)
            x = pad_l + xi * cw
            y = pad_t + (ny - 1 - yi) * ch        # ℓ piccolo in basso
            fill = _heat(c.epsilon, eps_max)
            p.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{cw-6:.1f}" '
                     f'height="{ch-6:.1f}" rx="6" fill="{fill}" '
                     f'stroke="{_BG}" stroke-width="2"/>')
            label = ("≥ " if not c.exact else "") + f"{c.epsilon:.3f}"
            txt_color = _BG if c.epsilon > 0.55 * eps_max else _FG
            p.append(f'<text x="{x+cw/2-3:.1f}" y="{y+ch/2+2:.1f}" fill="{txt_color}" '
                     f'font-size="22" font-weight="700" text-anchor="middle" '
                     f'font-family="ui-monospace, Consolas, monospace">{label}</text>')
            if not c.exact:
                p.append(f'<text x="{x+cw/2-3:.1f}" y="{y+ch/2+24:.1f}" fill="{txt_color}" '
                         f'font-size="10" text-anchor="middle" opacity="0.8">cota inf.</text>')

    # assi
    for xi, s in enumerate(m.ss):
        p.append(f'<text x="{pad_l+xi*cw+cw/2-3:.1f}" y="{pad_t+plot_h+28:.0f}" '
                 f'fill="{_ASH}" font-size="14" text-anchor="middle">s={s}</text>')
    for yi, ell in enumerate(m.ells):
        y = pad_t + (ny - 1 - yi) * ch + ch / 2
        p.append(f'<text x="{pad_l-16:.0f}" y="{y+5:.1f}" fill="{_ASH}" '
                 f'font-size="14" text-anchor="end">ℓ={ell}</text>')
    p.append(f'<text x="{pad_l+plot_w/2:.0f}" y="{height-30}" fill="{_FG}" '
             f'font-size="13" text-anchor="middle">CALCOLO → numero di gate s</text>')
    p.append(f'<text x="34" y="{pad_t+plot_h/2:.0f}" fill="{_FG}" font-size="13" '
             f'text-anchor="middle" transform="rotate(-90 34 {pad_t+plot_h/2:.0f})">'
             f'INFORMAZIONE → fan-in ℓ</text>')
    p.append("</svg>")
    return "\n".join(p)


def write_svg(content: str, path: str) -> str:
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    return path
