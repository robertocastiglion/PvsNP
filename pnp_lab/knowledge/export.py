"""Esportazione del Knowledge Graph: Markdown, JSON, Graphviz DOT."""

from __future__ import annotations

import json

from .graph import Kind, KnowledgeGraph, Relation


_KIND_LABELS = {
    Kind.BARRIER: "Barriere",
    Kind.APPROACH: "Approcci",
    Kind.TECHNIQUE: "Tecniche",
    Kind.RESULT: "Risultati acquisiti",
    Kind.CONCEPT: "Concetti e classi",
    Kind.OPEN: "Problemi aperti",
}

# stile Graphviz per tipo di nodo: (forma, colore di riempimento)
_KIND_STYLE = {
    Kind.BARRIER: ("box", "#ffcccc"),
    Kind.APPROACH: ("ellipse", "#cce5ff"),
    Kind.TECHNIQUE: ("ellipse", "#d9ecff"),
    Kind.RESULT: ("note", "#ccffcc"),
    Kind.CONCEPT: ("component", "#eeeeee"),
    Kind.OPEN: ("diamond", "#ffe5b4"),
}

# stile Graphviz per tipo di arco: (colore, stile linea)
_REL_STYLE = {
    Relation.BLOCKS: ("#cc0000", "solid"),
    Relation.EVADES: ("#008800", "dashed"),
    Relation.USES: ("#333333", "solid"),
    Relation.GENERALIZES: ("#666666", "solid"),
    Relation.IMPLIES: ("#0000cc", "solid"),
    Relation.INSTANCE_OF: ("#996600", "dotted"),
    Relation.RELATED: ("#999999", "dotted"),
    Relation.TARGETS: ("#7700aa", "bold"),
}


def to_markdown(g: KnowledgeGraph) -> str:
    """Documento Markdown leggibile, organizzato per tipo di nodo."""
    lines = ["# P vs NP — Knowledge Graph", ""]
    for kind, label in _KIND_LABELS.items():
        nodes = sorted(g.nodes_of_kind(kind), key=lambda n: (n.year or 9999, n.title))
        if not nodes:
            continue
        lines.append(f"## {label}")
        lines.append("")
        for n in nodes:
            year = f" ({n.year})" if n.year else ""
            mod = f"  ·  ⚙️ {n.module}" if n.module else ""
            lines.append(f"### {n.title}{year}{mod}")
            lines.append("")
            lines.append(n.summary)
            lines.append("")
            outgoing = g.edges_from(n.id)
            if outgoing:
                for e in outgoing:
                    tgt = g.node(e.target).title
                    note = f" — {e.note}" if e.note else ""
                    lines.append(f"- *{e.relation.value}* → **{tgt}**{note}")
                lines.append("")
            if n.references:
                lines.append("Riferimenti:")
                for ref in n.references:
                    lines.append(f"- {ref}")
                lines.append("")
    return "\n".join(lines)


def to_json(g: KnowledgeGraph) -> str:
    """Serializzazione JSON di nodi e archi."""
    data = {
        "nodes": [
            {
                "id": n.id,
                "kind": n.kind.value,
                "title": n.title,
                "summary": n.summary,
                "year": n.year,
                "module": n.module,
                "tags": n.tags,
                "references": [
                    {
                        "authors": r.authors,
                        "title": r.title,
                        "year": r.year,
                        "venue": r.venue,
                        "url": r.url,
                    }
                    for r in n.references
                ],
            }
            for n in g.nodes
        ],
        "edges": [
            {"source": e.source, "target": e.target,
             "relation": e.relation.value, "note": e.note}
            for e in g.edges
        ],
    }
    return json.dumps(data, ensure_ascii=False, indent=2)


def to_dot(g: KnowledgeGraph) -> str:
    """Graphviz DOT. Renderizza con:  dot -Tpng grafo.dot -o grafo.png"""
    lines = [
        "digraph PvsNP {",
        "  rankdir=LR;",
        "  node [style=filled, fontname=\"Helvetica\", fontsize=10];",
        "  edge [fontname=\"Helvetica\", fontsize=8];",
        "",
    ]
    for n in g.nodes:
        shape, fill = _KIND_STYLE.get(n.kind, ("ellipse", "#ffffff"))
        label = n.title.replace('"', "'")
        if n.module:
            label += f"\\n[{n.module}]"
        lines.append(
            f'  "{n.id}" [label="{label}", shape={shape}, fillcolor="{fill}"];'
        )
    lines.append("")
    for e in g.edges:
        color, style = _REL_STYLE.get(e.relation, ("#000000", "solid"))
        lines.append(
            f'  "{e.source}" -> "{e.target}" '
            f'[label="{e.relation.value}", color="{color}", style={style}];'
        )
    lines.append("}")
    return "\n".join(lines)
