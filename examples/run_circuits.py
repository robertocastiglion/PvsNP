"""Demo del Modulo 6 — Circuit Complexity Sandbox.

Uso:  py examples/run_circuits.py
"""

import os
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")  # console Windows in cp1252
except (AttributeError, ValueError):
    pass

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from pnp_lab.circuits import (  # noqa: E402
    ascii_distribution,
    min_formula_sizes,
    parity_dnf_lower_bound,
    parity_growth,
    to_svg_distribution,
    to_svg_parity,
    write_svg,
)


def main() -> None:
    print("=" * 66)
    print("  P/NP RESEARCH LAB — Modulo 6: Circuit Complexity Sandbox")
    print("=" * 66)

    # --- Spettro di Shannon -------------------------------------------------
    print("\n── Spettro di Shannon: complessità ESATTA delle funzioni piccole ──")
    ct = min_formula_sizes(3)
    print(ascii_distribution(ct))
    n_hard = ct.distribution().get(ct.max_cost, 0)
    print(f"\n  La fascia più difficile (taglia {ct.max_cost}) contiene {n_hard} funzioni.")
    print("  Lezione: quasi tutte le funzioni sono difficili (Shannon 1949)…")
    print("  …ma non sappiamo esibire UNA funzione esplicita in NP che lo sia.")
    print("  È esattamente il muro dei lower bound sui circuiti.")

    # --- Muro della parità --------------------------------------------------
    print("\n── Il muro della parità: DNF minima = 2^(n-1) (esatto) ────────────")
    print(f"  {'n':>3}  {'DNF minima':>11}  verificato")
    print("  " + "─" * 34)
    for row in parity_growth(max_n=7):
        flag = "esatto ✓" if row.tight else "—"
        print(f"  {row.n:>3}  {row.dnf_terms:>11}  {flag}")
    lb = parity_dnf_lower_bound(5)
    print(f"\n  {lb.pretty()}")
    print("  → la parità ∉ AC0 (Furst–Saxe–Sipser, Håstad): un lower bound che")
    print("    FUNZIONA, e che aggira la barriera Natural Proofs (Modulo 1).")

    # --- Export SVG ---------------------------------------------------------
    here = Path(__file__).resolve().parent.parent
    assets = here / "web" / "assets"
    assets.mkdir(parents=True, exist_ok=True)
    write_svg(to_svg_distribution(ct), str(assets / "circuit_spectrum.svg"))
    write_svg(to_svg_parity(parity_growth(max_n=7)), str(assets / "parity_wall.svg"))
    print(f"\n  Grafici SVG esportati in: {assets}")
    print("    - circuit_spectrum.svg  (spettro di Shannon)")
    print("    - parity_wall.svg       (muro della parità)")

    print("\n" + "=" * 66)
    print("  Shannon: quasi tutte le funzioni sono difficili (ma non esplicite).")
    print("  Parità: un lower bound esplicito ed esatto che davvero funziona.")
    print("=" * 66)


if __name__ == "__main__":
    main()
