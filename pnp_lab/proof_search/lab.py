"""Benchmark onesto delle policy + visualizzazione (colori del brand).

Esegue gli stessi obiettivi con policy diverse e riporta numeri nudi: quanti
obiettivi chiusi, quanti nodi espansi, e — soprattutto — RIVERIFICA ogni prova
trovata (soundness). Nessuna cifra è "fidati di me": tutto è ricontrollato.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List

from .engine import Goal, Rule, benchmark_goals, group_rules
from .policies import exhaustive_policy, heuristic_policy
from .search import Policy, SearchResult, replay, search

# ── Palette "System Ignition" ────────────────────────────────────────────
_BG = "#0A0502"
_FG = "#FCF2E6"
_ORANGE = "#FF8012"
_GREEN = "#4AF626"
_RED = "#D73434"
_ASH = "#876244"


@dataclass
class PolicyReport:
    name: str
    results: List[SearchResult]

    @property
    def solved(self) -> int:
        return sum(1 for r in self.results if r.success)

    @property
    def total(self) -> int:
        return len(self.results)

    @property
    def total_nodes(self) -> int:
        return sum(r.nodes_expanded for r in self.results if r.success)

    @property
    def total_generated(self) -> int:
        """Stati generati totali = ramificazione impegnata (meno = policy migliore)."""
        return sum(r.generated for r in self.results if r.success)

    @property
    def all_proofs_valid(self) -> bool:
        return all(getattr(r, "_verified", True) for r in self.results)


def run_policy(name: str, policy: Policy, goals: List[Goal], rules: Dict[str, Rule],
               *, max_nodes: int = 4000) -> PolicyReport:
    """Esegue la policy su tutti gli obiettivi e RIVERIFICA ogni prova trovata."""
    results: List[SearchResult] = []
    for g in goals:
        res = search(g, rules, policy, max_nodes=max_nodes)
        # soundness: una prova "riuscita" deve davvero ricostruire il target
        res._verified = (not res.success) or replay(g, rules, res.proof)  # type: ignore[attr-defined]
        results.append(res)
    return PolicyReport(name, results)


def run_benchmark(max_nodes: int = 4000) -> List[PolicyReport]:
    rules = group_rules()
    goals = benchmark_goals()
    return [
        run_policy("esaustiva (baseline)", exhaustive_policy(), goals, rules, max_nodes=max_nodes),
        run_policy("euristica (top-4)", heuristic_policy(top_k=4), goals, rules, max_nodes=max_nodes),
    ]


def ascii_report(reports: List[PolicyReport]) -> str:
    goals = [r.goal for r in reports[0].results]
    lines = [
        "  Proof-search: stessi obiettivi, policy diverse (STATI GENERATI per chiuderli)",
        "  " + "─" * 64,
        f"  {'obiettivo':<18}" + "".join(f"{rp.name.split()[0]:>16}" for rp in reports),
    ]
    for i, gname in enumerate(goals):
        row = f"  {gname:<18}"
        for rp in reports:
            r = rp.results[i]
            cell = f"{r.generated}" if r.success else "—"
            row += f"{cell:>16}"
        lines.append(row)
    lines.append("  " + "─" * 64)
    for rp in reports:
        lines.append(
            f"  {rp.name}: risolti {rp.solved}/{rp.total}, "
            f"stati generati {rp.total_generated}, prove verificate: "
            f"{'sì' if rp.all_proofs_valid else 'NO'}"
        )
    lines.append("  → meno stati generati a parità di obiettivi = policy migliore (tutto qui, niente hype).")
    return "\n".join(lines)


def to_svg_benchmark(reports: List[PolicyReport], width: int = 900, height: int = 500) -> str:
    """Nodi espansi per obiettivo: baseline vs euristica (meno è meglio)."""
    pad_l, pad_r, pad_t, pad_b = 70, 30, 100, 96
    plot_w = width - pad_l - pad_r
    plot_h = height - pad_t - pad_b
    base_y = pad_t + plot_h
    goals = [r.goal for r in reports[0].results]
    peak = max((r.generated for rp in reports for r in rp.results if r.success), default=1)
    colors = [_ASH, _GREEN]

    p: List[str] = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" '
        f'font-family="Inter, Segoe UI, system-ui, sans-serif">',
        f'<rect width="{width}" height="{height}" fill="{_BG}"/>',
        f'<text x="{pad_l}" y="40" fill="{_ORANGE}" font-size="13" '
        f'font-family="ui-monospace, Consolas, monospace" letter-spacing="2">'
        f'&gt; PROOF-SEARCH // una policy migliore espande meno nodi</text>',
        f'<text x="{pad_l}" y="68" fill="{_FG}" font-size="22" font-weight="700">'
        f'Nodi espansi per chiudere ogni lemma (meno è meglio)</text>',
    ]
    p.append(f'<line x1="{pad_l}" y1="{base_y}" x2="{pad_l+plot_w}" y2="{base_y}" stroke="{_ASH}"/>')
    p.append(f'<line x1="{pad_l}" y1="{pad_t}" x2="{pad_l}" y2="{base_y}" stroke="{_ASH}"/>')

    n = len(goals)
    slot = plot_w / max(n, 1)
    bw = slot * 0.32
    for i, gname in enumerate(goals):
        cx = pad_l + i * slot + slot / 2
        for j, rp in enumerate(reports):
            r = rp.results[i]
            val = r.generated if r.success else 0
            h = plot_h * (val / peak) if r.success else 0
            x = cx + (j - 0.5) * (bw + 3) - bw / 2
            col = colors[j % len(colors)] if r.success else _RED
            hh = max(h, 3) if r.success else 6
            p.append(f'<rect x="{x:.0f}" y="{base_y-hh:.0f}" width="{bw:.0f}" height="{hh:.0f}" '
                     f'fill="{col}" opacity="0.9"/>')
        p.append(f'<text x="{cx:.0f}" y="{base_y+18:.0f}" fill="{_ASH}" font-size="10" '
                 f'text-anchor="end" transform="rotate(-40 {cx:.0f} {base_y+18:.0f})">{gname}</text>')

    lx = pad_l + plot_w - 220
    for j, rp in enumerate(reports):
        p.append(f'<rect x="{lx}" y="{pad_t + j*20}" width="12" height="12" fill="{colors[j % len(colors)]}"/>')
        p.append(f'<text x="{lx+18}" y="{pad_t + j*20 + 11}" fill="{_FG}" font-size="13">{rp.name}</text>')
    p.append("</svg>")
    return "\n".join(p)


def write_svg(content: str, path: str) -> str:
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    return path
