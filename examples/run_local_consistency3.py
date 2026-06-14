"""Module 21 (Local-Consistency Width) — demo di w*(Gamma) su D={0,1,2}.

    py examples/run_local_consistency3.py

Stampa la TABELLA esatta (nome, g, profilo simmetrico, ha_majority, |Pol-slice|, w*) per
ogni Gamma trattabile del campione, l'esito dei 4 predicati-killer e il gap esibito.
Regime esatto-PER-ISTANZA: ogni is_sat e` enumerazione completa <=729, ogni w* e` un MIN
esatto sulla batteria CONGELATA. Tutto rigenerabile da codice.
"""

import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from pnp_lab.csp.local_consistency3 import (
    CSP,
    analyze_consistency,
    is_sat,
    kk1_consistent,
    T,
)
from pnp_lab.csp.polymorphism3 import CATALOG


def main() -> None:
    print("=== Local-Consistency Width w*(Γ) su D={0,1,2} ===\n")
    print("Regime: esatto-PER-ISTANZA su campione. is_sat = enumerazione completa ≤729;")
    print("w* = min{k≤4 : ∀Φ∈T(Γ) (k,k+1)-consistenza == is_sat}.\n")

    rep = analyze_consistency()
    print("Γ            g   σ-profilo  ha_maj  |Pol-slice|  w*")
    print("-" * 56)
    for r in rep.rows:
        print(f"{r.name:11s} {r.g_value:>2}  {str(r.sym_profile):9s} "
              f"{str(r.has_majority):5s}   {r.n_pol_slice:>6}      {r.w}")

    print("\n--- 4 predicati-killer (numeri esatti, NESSUNA interpretazione) ---")
    print(f"  K-bw23 (max w* ≤ 2)        : {rep.k_bw23_holds}   "
          f"[range w* = {rep.w_star_range}]")
    print(f"  w1_tracks_majority         : {rep.w1_tracks_majority}")
    print(f"  K-Pol-slice collassa       : {rep.k_polslice_collapses}")
    sep, wit = rep.h_separates
    print(f"  h_separates (g,σ uguali)   : {sep}  testimoni={wit}")

    print("\n--- GAP esibito: ciclo di lunghezza 4 sulla relazione C3 ---")
    C3 = CATALOG["cycle3"]
    phi = CSP(4, (((0, 1), C3), ((1, 2), C3), ((2, 3), C3), ((3, 0), C3)))
    print(f"  C3 = {sorted(C3)}  (grafo +1 mod 3)")
    print(f"  ciclo a 4 var: SAT={is_sat(phi)}  "
          f"k=1 consistente={kk1_consistent(phi, 1)}  "
          f"k=2 consistente={kk1_consistent(phi, 2)}")
    print("  -> UNSAT ma 1-consistente, scoperto solo da k=2 ⇒ w*(C3) > 1.")


if __name__ == "__main__":
    main()
