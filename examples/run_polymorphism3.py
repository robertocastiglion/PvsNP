"""Direzione B, ciclo TERNARIO — demo della quantita` g su D={0,1,2}.

    py examples/run_polymorphism3.py

Stampa la TABELLA esatta (g, profilo simmetrico, |Aut_unari|, marker WNU) per ogni
relazione del catalogo, le coppie testimoni di H (marker-identiche ma g-diverse) e
l'esito dei 3 killer. Tutto rigenerabile da codice, interi esatti.
"""

import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from pnp_lab.csp.polymorphism3 import (
    analyze3,
    commutative_idempotent_binary_ops,
    count_wnu_witnesses,
    symmetric_idempotent_ops,
)


def main() -> None:
    print("=== Politomorfismi su D={0,1,2} — la quantita` g ===\n")
    print(f"WNU binari idempotenti commutativi (candidati)  : "
          f"{len(commutative_idempotent_binary_ops())}  (atteso 27)")
    print("operazioni simmetriche idempotenti per arieta`  : "
          + ", ".join(f"k={k}:{len(symmetric_idempotent_ops(k))}" for k in (2, 3)))

    rep = analyze3()
    print("\nrelazione    g   #testimoni  σ-profilo   |Aut|  wnu2   wnu3")
    print("-" * 62)
    for r in rep.rows:
        w = count_wnu_witnesses(r.R)
        print(f"{r.name:11s} {r.g_value:>2}   {w:>5}      "
              f"{str(r.sym_profile):10s}  {r.n_aut:>4}  {str(r.wnu2):5s}  {str(r.wnu3):5s}")

    print("\ncoppie marker-identiche ma g-diverse (testimoni di H):")
    if rep.witness_pairs:
        for a, b in rep.witness_pairs:
            print(f"    {a}  vs  {b}")
    else:
        print("    (nessuna)")

    print("\nesito killer:")
    print(f"    K-marker collassa : {rep.k_marker_collapses}")
    print(f"    K-σ      collassa : {rep.k_sigma_collapses}")
    print(f"    K-aut    collassa : {rep.k_aut_collapses}")
    print(f"\nVERDETTO (numeri, non interpretazione): {rep.verdict}")


if __name__ == "__main__":
    main()
