"""Knowledge Graph — mappa navigabile delle barriere e degli approcci a P vs NP.

Il grafo collega barriere, approcci, tecniche, risultati e problemi aperti, con
i riferimenti ai paper. Rende esplicito CHI blocca CHI e CHI aggira CHI — cioè
perché il problema resiste e dove sta la 'frontiera' promettente.
"""

from .graph import (
    Kind,
    Relation,
    Reference,
    Node,
    Edge,
    KnowledgeGraph,
)
from .data import build_knowledge_graph
from .export import to_markdown, to_json, to_dot

__all__ = [
    "Kind",
    "Relation",
    "Reference",
    "Node",
    "Edge",
    "KnowledgeGraph",
    "build_knowledge_graph",
    "to_markdown",
    "to_json",
    "to_dot",
]
