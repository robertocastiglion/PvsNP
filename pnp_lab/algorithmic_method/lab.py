"""Visualizzazione: la curva dello speedup (forza bruta vs metodo polinomiale)."""

from __future__ import annotations

from typing import List

from .speedup import SparsePoly, conj_poly, count_bruteforce, count_fast, speedup_factor
from .winwin import WinWin

# ── Palette "System Ignition" ────────────────────────────────────────────
_BG = "#0A0502"
_FG = "#FCF2E6"
_ORANGE = "#FF8012"
_GREEN = "#4AF626"
_RED = "#D73434"
_ASH = "#876244"


def ascii_speedup(examples: List[tuple]) -> str:
    lines = [
        "  Metodo algoritmico: contare #SAT (forza bruta 2^n vs sparsità del polinomio)",
        "  " + "─" * 66,
        f"  {'circuito':<26}{'#SAT':>8}{'op. brute':>11}{'op. fast':>10}{'speedup':>10}",
    ]
    for name, poly in examples:
        b = count_bruteforce(poly)
        f = count_fast(poly)
        flag = "" if b.value == f.value else "  !!MISMATCH"
        lines.append(f"  {name:<26}{f.value:>8}{b.ops:>11}{f.ops:>10}"
                     f"{speedup_factor(poly):>9.0f}x{flag}")
    lines.append("  " + "─" * 66)
    lines.append("  → strutturato (polinomio sparso) = SAT veloce; denso = nessun guadagno.")
    return "\n".join(lines)


def ascii_winwin(results: List[WinWin]) -> str:
    lines = [
        "  Soglia win-win: quale speedup implica un lower bound (NEXP ⊄ C)?",
        "  " + "─" * 66,
        f"  {'speedup':<32}{'super-poly?':>12}{'lower bound?':>14}",
    ]
    for w in results:
        lines.append(f"  {w.speedup.label:<32}"
                     f"{('sì' if w.speedup.superpolynomial else 'no'):>12}"
                     f"{('SÌ' if w.lower_bound else 'no'):>14}")
    lines.append("  " + "─" * 66)
    lines.append("  → serve uno speedup SUPER-POLINOMIALE: il senso di «un po' più veloce».")
    return "\n".join(lines)


def to_svg_speedup(k: int = 3, max_n: int = 22, width: int = 900, height: int = 500) -> str:
    """Forza bruta (2^n) vs metodo polinomiale (sparsità costante) al crescere di n.
    Scala logaritmica: la forza bruta esplode, il metodo resta piatto."""
    import math
    pad_l, pad_r, pad_t, pad_b = 80, 30, 100, 64
    plot_w = width - pad_l - pad_r
    plot_h = height - pad_t - pad_b
    base_y = pad_t + plot_h
    ns = list(range(k + 1, max_n + 1))
    brute = [(1 << n) for n in ns]                       # 2^n
    fast = [count_fast(conj_poly(k, n)).ops for n in ns]  # = 1 (monomio singolo)
    peak = math.log2(max(brute)) if brute else 1

    def X(i): return pad_l + plot_w * (i / max(len(ns) - 1, 1))
    def Y(v): return base_y - plot_h * (math.log2(max(v, 1)) / peak)

    p: List[str] = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" '
        f'font-family="Inter, Segoe UI, system-ui, sans-serif">',
        f'<rect width="{width}" height="{height}" fill="{_BG}"/>',
        f'<text x="{pad_l}" y="40" fill="{_ORANGE}" font-size="13" '
        f'font-family="ui-monospace, Consolas, monospace" letter-spacing="2">'
        f'&gt; ALGORITHMIC METHOD // SAT più veloce della forza bruta (Williams)</text>',
        f'<text x="{pad_l}" y="68" fill="{_FG}" font-size="22" font-weight="700">'
        f'Operazioni per contare #SAT: 2^n vs polinomio sparso (scala log)</text>',
    ]
    p.append(f'<line x1="{pad_l}" y1="{base_y}" x2="{pad_l+plot_w}" y2="{base_y}" stroke="{_ASH}"/>')
    p.append(f'<line x1="{pad_l}" y1="{pad_t}" x2="{pad_l}" y2="{base_y}" stroke="{_ASH}"/>')

    pts_b = " ".join(f"{X(i):.0f},{Y(v):.0f}" for i, v in enumerate(brute))
    pts_f = " ".join(f"{X(i):.0f},{Y(v):.0f}" for i, v in enumerate(fast))
    p.append(f'<polyline points="{pts_b}" fill="none" stroke="{_RED}" stroke-width="3"/>')
    p.append(f'<polyline points="{pts_f}" fill="none" stroke="{_GREEN}" stroke-width="3"/>')

    for i, n in enumerate(ns):
        if i % 3 == 0 or i == len(ns) - 1:
            p.append(f'<text x="{X(i):.0f}" y="{base_y+20:.0f}" fill="{_ASH}" font-size="11" '
                     f'text-anchor="middle">n={n}</text>')
    lx = pad_l + plot_w - 230
    p.append(f'<rect x="{lx}" y="{pad_t}" width="12" height="12" fill="{_RED}"/>')
    p.append(f'<text x="{lx+18}" y="{pad_t+11}" fill="{_FG}" font-size="13">forza bruta = 2^n</text>')
    p.append(f'<rect x="{lx}" y="{pad_t+22}" width="12" height="12" fill="{_GREEN}"/>')
    p.append(f'<text x="{lx+18}" y="{pad_t+33}" fill="{_FG}" font-size="13">metodo polinomiale (sparso)</text>')
    p.append(f'<text x="{pad_l+plot_w/2:.0f}" y="{height-18}" fill="{_ASH}" font-size="12" '
             f'text-anchor="middle">numero di variabili n (circuito AND di {k} letterali)</text>')
    p.append("</svg>")
    return "\n".join(p)


def write_svg(content: str, path: str) -> str:
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    return path
