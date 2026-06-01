"""Narrazione + SVG della separazione a query algebriche (colori del brand)."""

from __future__ import annotations

from typing import List

from .separation import CancellationAdversary, SeparationResult

# ── Palette "System Ignition" ────────────────────────────────────────────
_BG = "#0A0502"
_FG = "#FCF2E6"
_ORANGE = "#FF8012"
_GREEN = "#4AF626"
_RED = "#D73434"
_ASH = "#876244"


def ascii_separation(results: List[SeparationResult], adv: CancellationAdversary | None) -> str:
    lines = [
        "  Separazione a query algebriche per OR (∃ un 1 nell'oracolo)",
        "  " + "─" * 62,
        f"  {'m':>2}  {'N=2^m':>6}  {'GF(p)':>6}  {'NP (query)':>10}  {'P  (query ≥ κ)':>14}",
    ]
    for r in results:
        kappa = f"{r.det_lower_bound}" + ("" if r.det_exact else "+")
        lines.append(f"  {r.m:>2}  {r.n_oracle_values:>6}  GF({r.p:>2})  {r.nondet_queries:>10}  {kappa:>14}")
    if adv is not None:
        secrets = ", ".join(str(z) for z in adv.ones_positions)
        lines += [
            "  " + "─" * 62,
            f"  Avversario di cancellazione (m={adv.m}, GF({adv.p})):",
            f"    una query r = {adv.query_point}; i segreti {secrets}",
            f"    hanno χ_z(r) = {adv.chi_values} → somma ≡ 0: Ã(r)=0, come il tutto-zero.",
            "    Quella query è cieca: NP indovina, P deve spezzare ogni cancellazione.",
        ]
    return "\n".join(lines)


def to_svg_separation(results: List[SeparationResult], width: int = 900, height: int = 470) -> str:
    """NP (=1) vs P (≥ κ) al crescere di N = 2^m: il divario della separazione."""
    pad_l, pad_r, pad_t, pad_b = 70, 30, 100, 70
    plot_w = width - pad_l - pad_r
    plot_h = height - pad_t - pad_b
    base_y = pad_t + plot_h
    peak = max((r.det_lower_bound for r in results), default=1)

    p: List[str] = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" '
        f'font-family="Inter, Segoe UI, system-ui, sans-serif">',
        f'<rect width="{width}" height="{height}" fill="{_BG}"/>',
        f'<text x="{pad_l}" y="40" fill="{_ORANGE}" font-size="13" '
        f'font-family="ui-monospace, Consolas, monospace" letter-spacing="2">'
        f'&gt; ALGEBRAIC SEPARATION // P^Ã ≠ NP^Ã (cuore di query complexity)</text>',
        f'<text x="{pad_l}" y="68" fill="{_FG}" font-size="22" font-weight="700">'
        f'OR: NP basta 1 query, P ne richiede κ (e κ cresce con N)</text>',
    ]
    p.append(f'<line x1="{pad_l}" y1="{base_y}" x2="{pad_l+plot_w}" y2="{base_y}" stroke="{_ASH}"/>')
    p.append(f'<line x1="{pad_l}" y1="{pad_t}" x2="{pad_l}" y2="{base_y}" stroke="{_ASH}"/>')

    slot = plot_w / max(len(results), 1)
    bw = slot * 0.30
    for i, r in enumerate(results):
        cx = pad_l + i * slot + slot / 2
        # barra NP (= 1)
        h_np = plot_h * (r.nondet_queries / peak)
        x_np = cx - bw - 4
        p.append(f'<rect x="{x_np:.0f}" y="{base_y-h_np:.0f}" width="{bw:.0f}" height="{h_np:.0f}" '
                 f'fill="{_GREEN}" opacity="0.9"/>')
        p.append(f'<text x="{x_np+bw/2:.0f}" y="{base_y-h_np-8:.0f}" fill="{_FG}" font-size="12" '
                 f'font-weight="600" text-anchor="middle">{r.nondet_queries}</text>')
        # barra P (≥ κ)
        h_p = plot_h * (r.det_lower_bound / peak)
        x_p = cx + 4
        p.append(f'<rect x="{x_p:.0f}" y="{base_y-h_p:.0f}" width="{bw:.0f}" height="{h_p:.0f}" '
                 f'fill="{_RED}" opacity="0.9"/>')
        kappa = f"{r.det_lower_bound}" + ("" if r.det_exact else "+")
        p.append(f'<text x="{x_p+bw/2:.0f}" y="{base_y-h_p-8:.0f}" fill="{_FG}" font-size="12" '
                 f'font-weight="600" text-anchor="middle">{kappa}</text>')
        p.append(f'<text x="{cx:.0f}" y="{base_y+22:.0f}" fill="{_ASH}" font-size="12" '
                 f'text-anchor="middle">N={r.n_oracle_values} · GF({r.p})</text>')

    # legenda
    lx = pad_l + plot_w - 200
    p.append(f'<rect x="{lx}" y="{pad_t}" width="12" height="12" fill="{_GREEN}"/>')
    p.append(f'<text x="{lx+18}" y="{pad_t+11}" fill="{_FG}" font-size="13">NP (nondeterministico)</text>')
    p.append(f'<rect x="{lx}" y="{pad_t+22}" width="12" height="12" fill="{_RED}"/>')
    p.append(f'<text x="{lx+18}" y="{pad_t+33}" fill="{_FG}" font-size="13">P (deterministico ≥ κ)</text>')
    p.append(f'<text x="{pad_l+plot_w/2:.0f}" y="{height-20}" fill="{_ASH}" font-size="12" '
             f'text-anchor="middle">dimensione dell\'oracolo N = 2^m (campo piccolo: regime di AW)</text>')
    p.append("</svg>")
    return "\n".join(p)


def write_svg(content: str, path: str) -> str:
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    return path
