"""Test del Modulo 3 — Knowledge Graph.

Eseguibili con: py tests/test_knowledge.py   (oppure py -m pytest)
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from pnp_lab.knowledge import (  # noqa: E402
    build_knowledge_graph,
    to_markdown,
    to_json,
    to_dot,
    Kind,
)


def test_graph_validates():
    g = build_knowledge_graph()
    assert g.validate() == [], "tutti gli archi devono puntare a nodi esistenti"


def test_three_barriers_present():
    g = build_knowledge_graph()
    titles = {b.id for b in g.barriers()}
    assert titles == {"relativization", "natural_proofs", "algebrization"}


def test_relativization_blocks_diagonalization():
    g = build_knowledge_graph()
    blockers = {b.id for b in g.barriers_blocking("diagonalization")}
    assert "relativization" in blockers


def test_natural_proofs_blocks_circuit_lb():
    g = build_knowledge_graph()
    blockers = {b.id for b in g.barriers_blocking("circuit_lb")}
    assert "natural_proofs" in blockers


def test_gct_evades_all_three_barriers():
    g = build_knowledge_graph()
    evaded = {b.id for b in g.evaded_by("gct")}
    assert evaded == {"relativization", "natural_proofs", "algebrization"}


def test_most_promising_ranks_gct_first():
    g = build_knowledge_graph()
    ranking = g.most_promising()
    assert ranking, "ci deve essere almeno un approccio che aggira qualche barriera"
    top_node, top_barriers = ranking[0]
    assert top_node.id == "gct"
    assert len(top_barriers) == 3


def test_modules_linked_to_barriers():
    # Le barriere che abbiamo reso eseguibili devono puntare ai moduli giusti.
    g = build_knowledge_graph()
    assert g.node("natural_proofs").module == "Modulo 1"
    assert g.node("relativization").module == "Modulo 2"


def test_find_path_symmetric():
    g = build_knowledge_graph()
    path = g.find_path("diagonalization", "p_vs_np")
    assert path is not None
    assert path[0] == "diagonalization" and path[-1] == "p_vs_np"


def test_find_path_unknown_node_raises():
    g = build_knowledge_graph()
    try:
        g.find_path("nope", "p_vs_np")
        assert False, "doveva sollevare KeyError"
    except KeyError:
        pass


def test_export_markdown_nonempty():
    g = build_knowledge_graph()
    md = to_markdown(g)
    assert "# P vs NP" in md
    assert "Natural Proofs" in md


def test_export_json_roundtrips():
    g = build_knowledge_graph()
    data = json.loads(to_json(g))
    assert len(data["nodes"]) == len(g.nodes)
    assert len(data["edges"]) == len(g.edges)


def test_export_dot_wellformed():
    g = build_knowledge_graph()
    dot = to_dot(g)
    assert dot.startswith("digraph PvsNP {")
    assert dot.rstrip().endswith("}")
    assert '"relativization" -> "diagonalization"' in dot


if __name__ == "__main__":
    fns = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    failed = 0
    for fn in fns:
        try:
            fn()
            print(f"  PASS  {fn.__name__}")
        except AssertionError as e:
            failed += 1
            print(f"  FAIL  {fn.__name__}: {e}")
        except Exception as e:  # noqa: BLE001
            failed += 1
            print(f"  ERROR {fn.__name__}: {type(e).__name__}: {e}")
    print()
    print(f"  {len(fns) - failed}/{len(fns)} test superati")
    sys.exit(1 if failed else 0)
