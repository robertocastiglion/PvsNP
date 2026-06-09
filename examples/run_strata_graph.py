"""Demo: il grafo degli strati di MCSP-size e il down-degree locale (Ciclo 5).

Stampa, per ogni strato di costo (n=3 e, se gira in tempo, n=4):
  - #funzioni nello strato,
  - i valori distinti di d_flip (mossa GENUINA output-flip),
  - la relazione tra la partizione-per-d_flip e {sensitivity, block_sensitivity,
    gf2_degree, orbita-B_n}.

E conferma il killer-1: la mossa input-negation (automorfismo del costo) ha
down-degree ≡ 0 ovunque.
"""

import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from pnp_lab.meta_complexity.strata_graph import analyze, down_degree_negation


def render(n: int) -> None:
    print(f"\n=== n = {n} ===")
    ct, reps = analyze(n)
    neg_nonzero = sum(1 for tt in ct.cost if down_degree_negation(ct, tt, n) != 0)
    print(f"funzioni coperte: {len(ct.cost)} / {ct.num_functions}   max_cost: {ct.max_cost}")
    print(f"killer-1 (input-negation, mossa A): funzioni con d_negation>0 = {neg_nonzero} "
          f"→ {'CONFERMATO d≡0' if neg_nonzero == 0 else 'NON banale'}")
    print()
    head = f"{'cost':>4} {'#fun':>5} {'|{d_flip}|':>9} {'d_flip':>14}  " \
           f"{'sens':>12} {'bsens':>12} {'gf2deg':>13} {'orbitaB':>12}"
    print(head)
    print("-" * len(head))
    for r in reps:
        vals = ",".join(map(str, r.dflip_values))
        rs = r.rel_sensitivity or "-"
        rb = r.rel_block_sensitivity or "-"
        rd = r.rel_gf2_degree or "-"
        ro = r.rel_orbit or "-"
        print(f"{r.cost:>4} {r.num_funcs:>5} {r.num_dflip_values:>9} {vals:>14}  "
              f"{rs:>12} {rb:>12} {rd:>13} {ro:>12}")


if __name__ == "__main__":
    render(3)
    if "--n4" in sys.argv:
        render(4)
    else:
        print("\n(passa --n4 per la tabella n=4, esaustiva e più lenta)")
