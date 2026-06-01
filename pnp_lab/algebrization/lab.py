"""Narrazione + visualizzazione SVG del sum-check (colori del brand).

Un'immagine: la "scala dell'arithmetization". Il sum-check parte da una somma su
2^n vertici booleani e, round dopo round, fissa una variabile a un punto casuale
del campo, riducendo il problema fino a UNA sola valutazione del polinomio. Si
vede il crollo da 2^n termini a 1 query.
"""

from __future__ import annotations

import math

from .sumcheck import SumcheckResult

# ── Palette "System Ignition" ────────────────────────────────────────────
_BG = "#0A0502"
_FG = "#FCF2E6"
_ORANGE = "#FF8012"
_GREEN = "#4AF626"
_RED = "#D73434"
_ASH = "#876244"


def ascii_transcript(res: SumcheckResult, *, p: int, honest: bool = True) -> str:
    """Trascrizione ASCII di un'esecuzione del sum-check."""
    lines = [
        f"  Sum-check su GF({p}), n={res.n} variabili, grado/var ≤ {res.degree}",
        f"  Somma dichiarata H = {res.claimed_sum}   "
        f"({'PROVER ONESTO' if honest else 'PROVER DISONESTO'})",
        "  " + "─" * 64,
        f"  {'round':>5}  {'atteso':>8}  {'g_i(0)+g_i(1)':>14}  {'check':>6}  {'r_i':>5}",
    ]
    for rd in res.rounds:
        s01 = (rd.samples[0] + rd.samples[1]) % p
        lines.append(
            f"  {rd.var:>5}  {rd.expected:>8}  {s01:>14}  "
            f"{'OK' if rd.local_ok else 'NO':>6}  {rd.challenge:>5}"
        )
    lines += [
        "  " + "─" * 64,
        f"  Punto casuale finale r = {res.final_point}",
        f"  Valutazione finale di g(r) (UNA query) == atteso ?  "
        f"{'SÌ' if res.final_check else 'NO'}",
        f"  ESITO: {'ACCETTATO' if res.accepted else 'RIFIUTATO'}"
        f"   (query all'oracolo polinomiale: {res.oracle_queries})",
    ]
    return "\n".join(lines)


def to_svg_ladder(res: SumcheckResult, *, n_terms: int, width: int = 900, height: int = 480) -> str:
    """La scala dell'arithmetization: da 2^n termini a 1 query."""
    pad_l, pad_r, pad_t, pad_b = 70, 30, 96, 70
    plot_w = width - pad_l - pad_r
    plot_h = height - pad_t - pad_b
    n = res.n
    # numero di termini residui dopo k round: 2^(n-k) (concettuale), fino a 1.
    counts = [n_terms >> k for k in range(n + 1)]
    counts = [max(1, c) for c in counts]
    peak = counts[0]

    p: list[str] = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" '
        f'font-family="Inter, Segoe UI, system-ui, sans-serif">',
        f'<rect width="{width}" height="{height}" fill="{_BG}"/>',
        f'<text x="{pad_l}" y="40" fill="{_ORANGE}" font-size="13" '
        f'font-family="ui-monospace, Consolas, monospace" letter-spacing="2">'
        f'&gt; ALGEBRIZATION // la scala dell\'arithmetization</text>',
        f'<text x="{pad_l}" y="68" fill="{_FG}" font-size="22" font-weight="700">'
        f'Sum-check: da 2^{n} = {n_terms} termini a 1 sola query</text>',
    ]
    base_y = pad_t + plot_h
    p.append(f'<line x1="{pad_l}" y1="{base_y}" x2="{pad_l+plot_w}" y2="{base_y}" stroke="{_ASH}"/>')
    p.append(f'<line x1="{pad_l}" y1="{pad_t}" x2="{pad_l}" y2="{base_y}" stroke="{_ASH}"/>')

    slot = plot_w / len(counts)
    bw = slot * 0.6
    log_peak = math.log2(peak) if peak > 1 else 1
    for i, c in enumerate(counts):
        # altezza in scala logaritmica per far vedere il crollo
        h = plot_h * (math.log2(c) / log_peak) if peak > 1 else plot_h
        h = max(h, 4)
        x = pad_l + i * slot + (slot - bw) / 2
        y = base_y - h
        col = _GREEN if i == len(counts) - 1 else (_ORANGE if i > 0 else _RED)
        p.append(f'<rect x="{x:.0f}" y="{y:.0f}" width="{bw:.0f}" height="{h:.0f}" '
                 f'fill="{col}" opacity="0.9"/>')
        p.append(f'<text x="{x+bw/2:.0f}" y="{y-8:.0f}" fill="{_FG}" font-size="12" '
                 f'font-weight="600" text-anchor="middle">{c}</text>')
        label = "start" if i == 0 else (f"round {i}" if i < len(counts) - 1 else "1 query")
        p.append(f'<text x="{x+bw/2:.0f}" y="{base_y+22:.0f}" fill="{_ASH}" '
                 f'font-size="12" text-anchor="middle">{label}</text>')

    p.append(f'<text x="{pad_l+plot_w/2:.0f}" y="{height-22}" fill="{_ASH}" '
             f'font-size="12" text-anchor="middle">round del sum-check '
             f'(ogni round fissa una variabile a un punto casuale del campo)</text>')
    p.append(f'<text x="{pad_l-50}" y="{pad_t+plot_h/2:.0f}" fill="{_ASH}" font-size="12" '
             f'text-anchor="middle" transform="rotate(-90 {pad_l-50} {pad_t+plot_h/2:.0f})">'
             f'termini da sommare (scala log)</text>')
    p.append("</svg>")
    return "\n".join(p)


def write_svg(content: str, path: str) -> str:
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    return path
