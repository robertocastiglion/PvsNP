"""
Renderer SVG del knowledge graph — **zero dipendenze** (solo libreria standard).

Perché un SVG fatto a mano invece di Graphviz? Tre motivi:
  1. Su questa macchina `dot` non è installato (proxy aziendale), e così il
     modulo gira comunque, ovunque.
  2. L'SVG è nei colori del brand "System Ignition" (nero/arancione/verde):
     si incolla direttamente nella pagina web divulgativa.
  3. È vettoriale: nitido a ogni zoom, perfetto per slide e video YouTube.

Layout a colonne per *tipo* di nodo, con un piccolo flusso narrativo da sinistra
a destra (tecniche → approcci → barriere → risultati → concetti → problemi). Gli
archi sono colorati per *tipo di relazione* — in particolare rosso = "blocca",
verde = "aggira", che è il cuore del perché P vs NP resiste.
"""
from __future__ import annotations

import html

from .graph import Kind, KnowledgeGraph, Relation

# ── Palette "System Ignition" (brand La Logica dei Sistemi) ──────────────
BG = "#0A0502"
FG = "#FCF2E6"
ORANGE = "#FF8012"
GREEN = "#4AF626"
ASH = "#876244"

# Colore di accento per categoria di nodo (tinte sobrie su fondo scuro).
KIND_COLOR = {
    Kind.BARRIER: "#D73434",    # rosso: ciò che blocca
    Kind.APPROACH: ORANGE,      # arancione fuoco: i tentativi vivi
    Kind.TECHNIQUE: "#C77DFF",  # viola tenue: strumenti
    Kind.RESULT: GREEN,         # verde vita: risultati acquisiti
    Kind.CONCEPT: "#5BC0EB",    # azzurro: classi/concetti
    Kind.OPEN: FG,              # bianco caldo: le domande aperte
}

# Colore degli archi per tipo di relazione.
REL_COLOR = {
    Relation.BLOCKS: "#D73434",
    Relation.EVADES: GREEN,
    Relation.USES: ORANGE,
    Relation.GENERALIZES: "#C77DFF",
    Relation.IMPLIES: "#5BC0EB",
    Relation.INSTANCE_OF: ASH,
    Relation.RELATED: "#5A5040",
    Relation.TARGETS: "#FFAF4B",
}

REL_LABEL_IT = {
    Relation.BLOCKS: "blocca",
    Relation.EVADES: "aggira",
    Relation.USES: "usa",
    Relation.GENERALIZES: "generalizza",
    Relation.IMPLIES: "implica",
    Relation.INSTANCE_OF: "caso di",
    Relation.RELATED: "collega",
    Relation.TARGETS: "mira a",
}

# Ordine (e quindi colonna) delle categorie, da sinistra a destra.
COLUMNS = [
    Kind.TECHNIQUE,
    Kind.APPROACH,
    Kind.BARRIER,
    Kind.RESULT,
    Kind.CONCEPT,
    Kind.OPEN,
]

KIND_LABEL_IT = {
    Kind.TECHNIQUE: "tecnica",
    Kind.APPROACH: "approccio",
    Kind.BARRIER: "barriera",
    Kind.RESULT: "risultato",
    Kind.CONCEPT: "concetto / classe",
    Kind.OPEN: "problema aperto",
}

# Geometria
W, H = 1600, 860
MARGIN_X, MARGIN_TOP = 70, 120
NODE_W, NODE_H = 210, 58
RADIUS = 12


def _positions(g: KnowledgeGraph) -> dict[str, tuple[float, float]]:
    """Assegna a ogni nodo un centro (x, y): colonna per tipo, righe distribuite."""
    span = (W - 2 * MARGIN_X - NODE_W) / (len(COLUMNS) - 1)
    col_x = {kind: MARGIN_X + NODE_W / 2 + i * span for i, kind in enumerate(COLUMNS)}
    pos: dict[str, tuple[float, float]] = {}
    area_h = H - MARGIN_TOP - 70
    for kind in COLUMNS:
        nodes = sorted(g.nodes_of_kind(kind), key=lambda n: (n.year or 9999, n.title))
        x = col_x[kind]
        n = len(nodes)
        for j, node in enumerate(nodes):
            y = MARGIN_TOP + area_h * (j + 1) / (n + 1)
            pos[node.id] = (x, y)
    return pos


def _wrap(text: str, max_chars: int = 25, max_lines: int = 3) -> list[str]:
    """Spezza l'etichetta su più righe; tronca con ellissi se troppo lunga."""
    words, lines, cur = text.split(), [], ""
    for w in words:
        if len(cur) + len(w) + 1 <= max_chars:
            cur = (cur + " " + w).strip()
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    if len(lines) > max_lines:
        lines = lines[:max_lines]
        lines[-1] = lines[-1].rstrip()[: max_chars - 1] + "…"
    return lines


def to_svg(g: KnowledgeGraph) -> str:
    """Restituisce il grafo come documento SVG completo (stringa)."""
    pos = _positions(g)
    p: list[str] = []
    p.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" '
        f'font-family="Inter, Segoe UI, system-ui, sans-serif">'
    )

    # marcatori freccia, uno per colore di relazione
    p.append("<defs>")
    for rel, col in REL_COLOR.items():
        p.append(
            f'<marker id="ar_{rel.name}" viewBox="0 0 10 10" refX="9" refY="5" '
            f'markerWidth="7" markerHeight="7" orient="auto-start-end">'
            f'<path d="M0,0 L10,5 L0,10 z" fill="{col}"/></marker>'
        )
    p.append("</defs>")

    # sfondo + titolo
    p.append(f'<rect width="{W}" height="{H}" fill="{BG}"/>')
    p.append(
        f'<text x="{MARGIN_X}" y="50" fill="{ORANGE}" font-size="13" '
        f'font-family="ui-monospace, Consolas, monospace" letter-spacing="3">'
        f'&gt; KNOWLEDGE GRAPH // P vs NP</text>'
    )
    p.append(
        f'<text x="{MARGIN_X}" y="82" fill="{FG}" font-size="24" font-weight="700">'
        f'Le barriere, gli approcci e perché il problema resiste</text>'
    )

    # archi (sotto i nodi)
    for e in g.edges:
        if e.source not in pos or e.target not in pos:
            continue
        x1, y1 = pos[e.source]
        x2, y2 = pos[e.target]
        col = REL_COLOR.get(e.relation, ASH)
        dx, dy = x2 - x1, y2 - y1
        dist = max((dx * dx + dy * dy) ** 0.5, 1.0)
        ux, uy = dx / dist, dy / dist
        sx, sy = x1 + ux * (NODE_W / 2 + 4), y1 + uy * (NODE_H / 2 + 2)
        ex, ey = x2 - ux * (NODE_W / 2 + 12), y2 - uy * (NODE_H / 2 + 10)
        dash = ' stroke-dasharray="5 5"' if e.relation in (Relation.RELATED, Relation.INSTANCE_OF) else ""
        mx, my = (sx + ex) / 2, (sy + ey) / 2 - 26
        p.append(
            f'<path d="M{sx:.0f},{sy:.0f} Q{mx:.0f},{my:.0f} {ex:.0f},{ey:.0f}" '
            f'fill="none" stroke="{col}" stroke-width="1.6" opacity="0.7"{dash} '
            f'marker-end="url(#ar_{e.relation.name})"/>'
        )

    # nodi
    for nid, (cx, cy) in pos.items():
        node = g.node(nid)
        col = KIND_COLOR.get(node.kind, ASH)
        x, y = cx - NODE_W / 2, cy - NODE_H / 2
        p.append(
            f'<rect x="{x:.0f}" y="{y:.0f}" width="{NODE_W}" height="{NODE_H}" '
            f'rx="{RADIUS}" fill="#140C06" stroke="{col}" stroke-width="2"/>'
        )
        p.append(f'<circle cx="{x + 14:.0f}" cy="{y + 14:.0f}" r="4" fill="{col}"/>')
        if node.module:
            p.append(
                f'<text x="{x + NODE_W - 10:.0f}" y="{y + 17:.0f}" fill="{ORANGE}" '
                f'font-size="9" font-family="ui-monospace, monospace" '
                f'text-anchor="end">⚙ {html.escape(node.module)}</text>'
            )
        lines = _wrap(node.title)
        n = len(lines)
        for k, r in enumerate(lines):
            ty = cy - (n - 1) * 8 + k * 16 + 4
            p.append(
                f'<text x="{cx:.0f}" y="{ty:.0f}" fill="{FG}" font-size="12.5" '
                f'font-weight="600" text-anchor="middle">{html.escape(r)}</text>'
            )

    # legenda categorie (in basso)
    lx, ly = MARGIN_X, H - 30
    for kind in COLUMNS:
        col = KIND_COLOR[kind]
        lab = KIND_LABEL_IT[kind]
        p.append(f'<circle cx="{lx + 6:.0f}" cy="{ly - 4:.0f}" r="5" fill="{col}"/>')
        p.append(f'<text x="{lx + 18:.0f}" y="{ly:.0f}" fill="{ASH}" font-size="12">{lab}</text>')
        lx += 30 + len(lab) * 7.0

    # legenda relazioni principali (a destra in basso)
    p.append(
        f'<text x="{W - MARGIN_X:.0f}" y="{ly:.0f}" fill="{ASH}" font-size="12" '
        f'text-anchor="end">'
        f'<tspan fill="{REL_COLOR[Relation.BLOCKS]}">━ blocca</tspan>   '
        f'<tspan fill="{REL_COLOR[Relation.EVADES]}">┄ aggira</tspan>   '
        f'<tspan fill="{REL_COLOR[Relation.TARGETS]}">━ mira a</tspan></text>'
    )

    p.append("</svg>")
    return "\n".join(p)


def write_svg(g: KnowledgeGraph, path: str) -> str:
    """Scrive l'SVG su `path` e restituisce il percorso."""
    with open(path, "w", encoding="utf-8") as f:
        f.write(to_svg(g))
    return path
