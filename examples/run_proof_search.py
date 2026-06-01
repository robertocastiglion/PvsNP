"""Demo del Modulo 11 — Proof-Search Lab.

Uso:
    py examples/run_proof_search.py

Nota: usa solo policy deterministiche (esaustiva, euristica). L'integrazione con
un modello esterno (LLMPolicy) è opzionale e richiede una `call_fn` fornita
dall'utente — non è inclusa qui e il toolkit non ne dipende.
"""

import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
except (AttributeError, ValueError):
    pass

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from pnp_lab.proof_search import (  # noqa: E402
    ascii_report,
    benchmark_goals,
    group_rules,
    heuristic_policy,
    replay,
    run_benchmark,
    search,
    to_svg_benchmark,
    write_svg,
)
from pnp_lab.proof_search.engine import show  # noqa: E402


def main() -> None:
    print()
    print("  P/NP RESEARCH LAB — Modulo 11: Proof-Search Lab")
    print()

    # una prova trovata, mostrata passo passo (e riverificata)
    rules = group_rules()
    g = next(x for x in benchmark_goals() if x.name == "nested_id")
    res = search(g, rules, heuristic_policy(top_k=4))
    print("=" * 72)
    print(f"  Obiettivo: {show(g.start)}  =  {show(g.target)}")
    term = g.start
    for tac in res.proof:
        from pnp_lab.proof_search.engine import apply_tactic
        nxt = apply_tactic(rules, term, tac)
        print(f"    {tac.show():<28} ⊢ {show(nxt)}")
        term = nxt
    print(f"  Prova trovata ({res.proof_length} passi, {res.nodes_expanded} nodi) — "
          f"riverificata: {replay(g, rules, res.proof)}")
    print()

    # benchmark onesto: baseline vs euristica
    print("=" * 72)
    reports = run_benchmark(max_nodes=4000)
    print(ascii_report(reports))
    print()

    assets = Path(__file__).resolve().parent.parent / "web" / "assets"
    assets.mkdir(parents=True, exist_ok=True)
    out = write_svg(to_svg_benchmark(reports), str(assets / "proof_search.svg"))
    print(f"  SVG salvato: {out}")
    print()
    print("  Onestà: l'LLM è una POLICY opzionale e pluggable (LLMPolicy), mai nel")
    print("  percorso verificato. Qui nessun modello è stato usato: solo euristiche")
    print("  deterministiche e un verificatore sound. Niente hype.")


if __name__ == "__main__":
    main()
