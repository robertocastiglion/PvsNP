"""Demo del Modulo 3 — Knowledge Graph.

Stampa le interrogazioni principali ed esporta il grafo in Markdown, JSON e DOT.

Uso:
    py examples/run_knowledge.py
"""

import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
except (AttributeError, ValueError):
    pass

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from pnp_lab.knowledge import (  # noqa: E402
    build_knowledge_graph,
    to_markdown,
    to_json,
    to_dot,
)


def main() -> None:
    g = build_knowledge_graph()

    print()
    print("  P/NP RESEARCH LAB — Modulo 3: Knowledge Graph")
    print(f"  {len(g.nodes)} nodi, {len(g.edges)} archi")
    print()

    problems = g.validate()
    print(f"  Integrità referenziale: {'OK' if not problems else problems}")
    print()

    print("  ── Barriere e cosa bloccano ──────────────────────────────────")
    for barrier in g.barriers():
        blocked = [g.node(e.target).title for e in g.edges_from(barrier.id)
                   if e.relation.value == "blocks"]
        print(f"  • {barrier.title}: blocca {', '.join(blocked) or '(—)'}")
    print()

    print("  ── Frontiera: approcci che aggirano più barriere ─────────────")
    for node, barriers in g.most_promising():
        names = ", ".join(sorted(g.node(b).title for b in barriers))
        print(f"  • {node.title}  →  aggira {len(barriers)}: {names}")
    print()

    print("  ── Esempio di cammino nel grafo ──────────────────────────────")
    path = g.find_path("diagonalization", "p_vs_np")
    if path:
        print("  diagonalization → p_vs_np:")
        print("    " + " → ".join(g.node(nid).title for nid in path))
    print()

    # Export su file
    out = ROOT / "knowledge_export"
    out.mkdir(exist_ok=True)
    (out / "knowledge.md").write_text(to_markdown(g), encoding="utf-8")
    (out / "knowledge.json").write_text(to_json(g), encoding="utf-8")
    (out / "knowledge.dot").write_text(to_dot(g), encoding="utf-8")
    print(f"  Esportato in {out}\\:  knowledge.md, knowledge.json, knowledge.dot")
    print("  Per il grafico:  dot -Tpng knowledge_export/knowledge.dot -o grafo.png")
    print()


if __name__ == "__main__":
    main()
