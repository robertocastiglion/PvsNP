"""Visualizzazione del Modulo 14: la matrice dei difetti e l'isola di equivalenza."""

from __future__ import annotations

from typing import List

from .defect import BudgetPoint, CikkIsland, DefectMatrix, IrreducibleGap

# ── Palette "System Ignition" ────────────────────────────────────────────
_BG = "#0A0502"
_FG = "#FCF2E6"
_ORANGE = "#FF8012"
_GREEN = "#4AF626"
_RED = "#D73434"
_ASH = "#876244"


def ascii_matrix(dm: DefectMatrix) -> str:
    short = {"calcolare": "calc", "dimostrare": "prove", "riconoscere": "recog"}
    head = "        " + "".join(f"{short[l]:>9}" for l in dm.labels)
    lines = [
        f"  Matrice dei difetti (s={dm.s}, θ={dm.theta}, budget={dm.proof_budget})",
        "  " + "─" * 44,
        head,
    ]
    for i, a in enumerate(dm.labels):
        row = f"  {short[a]:>5} " + "".join(f"{dm.matrix[i][j]:>9.3f}" for j in range(len(dm.labels)))
        lines.append(row)
    lines.append("  " + "─" * 44)
    lines.append("  0.000 = equivalenza stretta · >0 = relazione lassa")
    return "\n".join(lines)


def ascii_cikk(island: CikkIsland) -> str:
    return "\n".join([
        "  Isola di equivalenza — riconoscere ⟺ apprendere (CIKK 2016):",
        f"    soglia appresa θ={island.learned_theta} da {island.samples_used} campioni",
        f"    difetto round-trip = {island.round_trip_defect:.3f} "
        f"⇒ {'EQUIVALENZA stretta ✓' if island.equivalent else 'lasso'}",
    ])


def ascii_gap(gap: IrreducibleGap) -> str:
    return "\n".join([
        f"  Gap irriducibile — calcolare ↔ riconoscere (s={gap.s}, θ*={gap.best_theta}):",
        f"    difetto residuo = {gap.residual_defect:.3f} "
        f"({gap.misclassified} funzioni mal classificate)",
        f"    → {gap.interpretation}",
    ])


def to_svg_matrix(dm: DefectMatrix, island: CikkIsland,
                  width: int = 900, height: int = 520) -> str:
    """Heatmap 3×3 dei difetti + nota sull'isola di equivalenza."""
    short = {"calcolare": "calcolare", "dimostrare": "dimostrare", "riconoscere": "riconoscere"}
    n = len(dm.labels)
    cell = 110
    grid_x = 220
    grid_y = 150

    def color(v: float) -> str:
        if v == 0.0:
            return _GREEN
        # da arancio (poco) a rosso (molto), v in (0,1]
        return _RED if v >= 0.25 else _ORANGE

    p: List[str] = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" '
        f'font-family="Inter, Segoe UI, system-ui, sans-serif">',
        f'<rect width="{width}" height="{height}" fill="{_BG}"/>',
        f'<text x="40" y="44" fill="{_ORANGE}" font-size="13" '
        f'font-family="ui-monospace, Consolas, monospace" letter-spacing="2">'
        f'&gt; ENRICHED META-CATEGORY // difetto di composizione delle tre lenti</text>',
        f'<text x="40" y="74" fill="{_FG}" font-size="22" font-weight="700">'
        f'Le tre lenti sono la stessa freccia? (0 = sì, &gt;0 = no)</text>',
    ]
    # etichette colonne
    for j, lab in enumerate(dm.labels):
        cx = grid_x + j * cell + cell / 2
        p.append(f'<text x="{cx:.0f}" y="{grid_y-12}" fill="{_ASH}" font-size="13" '
                 f'text-anchor="middle">{short[lab]}</text>')
    # righe + celle
    for i, lab in enumerate(dm.labels):
        cy = grid_y + i * cell + cell / 2
        p.append(f'<text x="{grid_x-14}" y="{cy+4:.0f}" fill="{_ASH}" font-size="13" '
                 f'text-anchor="end">{short[lab]}</text>')
        for j in range(n):
            v = dm.matrix[i][j]
            x = grid_x + j * cell
            y = grid_y + i * cell
            fill = color(v)
            opa = 0.22 if i == j else (0.9 if v > 0 else 0.9)
            p.append(f'<rect x="{x}" y="{y}" width="{cell-6}" height="{cell-6}" '
                     f'rx="6" fill="{fill}" opacity="{opa}"/>')
            txt = "—" if i == j else f"{v:.3f}"
            tcol = _BG if v == 0.0 and i != j else _FG
            p.append(f'<text x="{x+(cell-6)/2:.0f}" y="{y+(cell-6)/2+5:.0f}" '
                     f'fill="{tcol}" font-size="18" font-weight="700" '
                     f'text-anchor="middle">{txt}</text>')
    # nota isola CIKK
    note_y = grid_y + n * cell + 50
    verdict = "EQUIVALENZA stretta" if island.equivalent else "relazione lassa"
    p.append(f'<text x="40" y="{note_y}" fill="{_GREEN}" font-size="14" '
             f'font-family="ui-monospace, Consolas, monospace">'
             f'riconoscere ⟺ apprendere (CIKK 2016): difetto round-trip = '
             f'{island.round_trip_defect:.3f} → {verdict}</text>')
    p.append(f'<text x="40" y="{note_y+26}" fill="{_ASH}" font-size="12">'
             f'verde = stessa freccia · arancio/rosso = lente lassa (relazione, non identità)</text>')
    p.append("</svg>")
    return "\n".join(p)


def write_svg(content: str, path: str) -> str:
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    return path
