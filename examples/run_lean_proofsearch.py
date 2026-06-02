"""Demo del passo #4 — proof-search su Lean VERO (Modulo 11, stile LeanDojo).

Una policy propone blocchi di tattiche; a verificarli è Lean 4 reale (`lake env
lean`). Metrica onesta: una policy migliore chiude i lemmi con MENO verifiche.

Uso (richiede Lean/lake installati):
    py examples/run_lean_proofsearch.py

Se Lean non è disponibile, stampa solo il riassunto e salta l'esecuzione reale.
"""

import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
except (AttributeError, ValueError):
    pass

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from pnp_lab.proof_search import (  # noqa: E402
    LeanChecker,
    ascii_comparison,
    benchmark_lean_goals,
    compare_lean_policies,
    exhaustive_lean_policy,
    heuristic_lean_policy,
    lean_bridge_summary,
    to_svg_comparison,
    write_svg,
)


def main() -> None:
    print()
    print("  P/NP RESEARCH LAB — Modulo 11 (passo #4): proof-search su Lean VERO")
    print()
    print(lean_bridge_summary())
    print()

    if not LeanChecker.available():
        print("  Lean/lake non disponibile: salto l'esecuzione reale.")
        print("  (Installa elan/Lean e riprova per vedere la policy guidare Lean.)")
        return

    checker = LeanChecker()
    policies = {
        "esaustiva": exhaustive_lean_policy(),
        "euristica": heuristic_lean_policy(),
    }
    print("=" * 72)
    print("  CONFRONTO  —  esaustiva vs euristica, verificatore = Lean 4 reale")
    print("=" * 72)
    comp = compare_lean_policies(benchmark_lean_goals(), policies, checker)
    print(ascii_comparison(comp, ["esaustiva", "euristica"]))
    print()

    assets = Path(__file__).resolve().parent.parent / "web" / "assets"
    assets.mkdir(parents=True, exist_ok=True)
    out = write_svg(to_svg_comparison(comp, ["esaustiva", "euristica"]),
                    str(assets / "lean_proofsearch.svg"))
    print(f"  SVG salvato: {out}")


if __name__ == "__main__":
    main()
