"""Motore generico del Knowledge Graph: nodi, archi e interrogazioni.

Il grafo modella lo stato dell'arte attorno a P vs NP:
  - NODI: barriere, approcci/tecniche, risultati, concetti/classi, problemi aperti.
  - ARCHI: relazioni con verso e significato ('blocca', 'aggira', 'implica', …).

È volutamente senza dipendenze esterne (solo standard library) così gira
ovunque. La base di conoscenza vera è in ``data.py``; l'export in ``export.py``.
"""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass, field
from enum import Enum
from typing import Iterable, Iterator


class Kind(str, Enum):
    """Tipo di nodo."""

    BARRIER = "barrier"          # barriera dimostrativa (es. relativizzazione)
    APPROACH = "approach"        # programma/strategia di attacco (es. GCT)
    TECHNIQUE = "technique"      # tecnica concreta (es. diagonalizzazione)
    RESULT = "result"            # teorema/risultato acquisito (es. IP = PSPACE)
    CONCEPT = "concept"          # classe o concetto (es. PSPACE, P/poly)
    OPEN = "open_problem"        # problema aperto (es. P vs NP)


class Relation(str, Enum):
    """Tipo di arco (diretto: source -> target)."""

    BLOCKS = "blocks"            # una barriera blocca un approccio/tecnica
    EVADES = "evades"            # un approccio aggira una barriera
    USES = "uses"                # X usa Y
    GENERALIZES = "generalizes"  # X generalizza Y
    IMPLIES = "implies"          # X implica Y
    INSTANCE_OF = "instance_of"  # X è un caso particolare di Y
    RELATED = "related"          # collegamento generico
    TARGETS = "targets"          # un approccio mira a un problema aperto


@dataclass(frozen=True)
class Reference:
    """Riferimento bibliografico."""

    authors: str
    title: str
    year: int
    venue: str = ""
    url: str = ""

    def __str__(self) -> str:
        bits = [f"{self.authors} ({self.year}). {self.title}."]
        if self.venue:
            bits.append(f" {self.venue}.")
        if self.url:
            bits.append(f" {self.url}")
        return "".join(bits)


@dataclass
class Node:
    id: str
    kind: Kind
    title: str
    summary: str
    year: int | None = None
    references: list[Reference] = field(default_factory=list)
    module: str | None = None  # modulo eseguibile collegato (es. "Modulo 2")
    tags: list[str] = field(default_factory=list)


@dataclass
class Edge:
    source: str
    target: str
    relation: Relation
    note: str = ""


class KnowledgeGraph:
    """Grafo diretto di nodi ed archi, con interrogazioni di alto livello."""

    def __init__(self) -> None:
        self._nodes: dict[str, Node] = {}
        self._edges: list[Edge] = []

    # -- costruzione -------------------------------------------------------

    def add_node(self, node: Node) -> Node:
        if node.id in self._nodes:
            raise ValueError(f"nodo duplicato: {node.id!r}")
        self._nodes[node.id] = node
        return node

    def add_edge(self, edge: Edge) -> Edge:
        self._edges.append(edge)
        return edge

    # -- accesso -----------------------------------------------------------

    def node(self, node_id: str) -> Node:
        return self._nodes[node_id]

    @property
    def nodes(self) -> list[Node]:
        return list(self._nodes.values())

    @property
    def edges(self) -> list[Edge]:
        return list(self._edges)

    def nodes_of_kind(self, kind: Kind) -> list[Node]:
        return [n for n in self._nodes.values() if n.kind == kind]

    def edges_from(self, node_id: str) -> list[Edge]:
        return [e for e in self._edges if e.source == node_id]

    def edges_to(self, node_id: str) -> list[Edge]:
        return [e for e in self._edges if e.target == node_id]

    # -- interrogazioni tematiche -----------------------------------------

    def barriers(self) -> list[Node]:
        return self.nodes_of_kind(Kind.BARRIER)

    def barriers_blocking(self, approach_id: str) -> list[Node]:
        """Barriere che bloccano l'approccio/tecnica dato."""
        return [
            self._nodes[e.source]
            for e in self.edges_to(approach_id)
            if e.relation == Relation.BLOCKS
            and self._nodes[e.source].kind == Kind.BARRIER
        ]

    def evaded_by(self, node_id: str) -> list[Node]:
        """Barriere che il nodo dato dichiara di aggirare."""
        return [
            self._nodes[e.target]
            for e in self.edges_from(node_id)
            if e.relation == Relation.EVADES
            and self._nodes[e.target].kind == Kind.BARRIER
        ]

    def evasion_matrix(self) -> dict[str, set[str]]:
        """Per ogni nodo con archi 'evades', l'insieme di barriere che aggira."""
        matrix: dict[str, set[str]] = {}
        for e in self._edges:
            if e.relation == Relation.EVADES and self._nodes[e.target].kind == Kind.BARRIER:
                matrix.setdefault(e.source, set()).add(e.target)
        return matrix

    def most_promising(self) -> list[tuple[Node, set[str]]]:
        """Approcci ordinati per numero di barriere aggirate (la 'frontiera')."""
        matrix = self.evasion_matrix()
        ranked = sorted(
            ((self._nodes[nid], barriers) for nid, barriers in matrix.items()),
            key=lambda pair: len(pair[1]),
            reverse=True,
        )
        return ranked

    def find_path(self, a: str, b: str) -> list[str] | None:
        """Cammino più breve fra due nodi, trattando gli archi come NON orientati."""
        if a not in self._nodes or b not in self._nodes:
            raise KeyError("nodo inesistente")
        adj: dict[str, set[str]] = {nid: set() for nid in self._nodes}
        for e in self._edges:
            adj[e.source].add(e.target)
            adj[e.target].add(e.source)
        queue: deque[list[str]] = deque([[a]])
        seen = {a}
        while queue:
            path = queue.popleft()
            if path[-1] == b:
                return path
            for nxt in adj[path[-1]]:
                if nxt not in seen:
                    seen.add(nxt)
                    queue.append(path + [nxt])
        return None

    # -- integrità ---------------------------------------------------------

    def validate(self) -> list[str]:
        """Restituisce la lista di problemi di integrità referenziale (vuota = ok)."""
        problems: list[str] = []
        for e in self._edges:
            if e.source not in self._nodes:
                problems.append(f"arco con sorgente inesistente: {e.source!r}")
            if e.target not in self._nodes:
                problems.append(f"arco con destinazione inesistente: {e.target!r}")
        return problems

    def __iter__(self) -> Iterator[Node]:
        return iter(self._nodes.values())

    def __len__(self) -> int:
        return len(self._nodes)
