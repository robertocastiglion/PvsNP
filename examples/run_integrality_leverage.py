"""Demo door-C (Entry 32): leva cross-livello del lifting come crescita del gap di
integralita'  G_k = Cov(M_k) - LP(M_k).

Stampa la tabella ESATTA (f, g) -> (G_1, G_2, G_3, killed) dello sweep su tutte le
coppie, evidenziando le celle a gap e l'ancora nota OR ∘ XOR a k=2 (Cov=4, LP=3).

Esegui:  py examples/run_integrality_leverage.py
"""

import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
except (AttributeError, ValueError):
    pass

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from fractions import Fraction  # noqa: E402,F401

from pnp_lab.exactness_composes.integrality_leverage import (  # noqa: E402
    killer_table,
    doorC_candidates,
    leverage_row,
)


def main() -> None:
    print("Door-C: la leva cross-livello del lifting come gap di integralita'")
    print("G_k = Cov(M_k) - LP(M_k),  M_k = lift(f, g, k)  (2^k x 2^k)")
    print()

    # Ancora di sanita': OR ∘ XOR a k=2 -> matrice di disuguaglianza J - I_4.
    a = leverage_row("OR", "XOR")
    print("ANCORA (Modulo 18)  OR ∘ XOR, k=2:  "
          f"Cov_2={a['Cov2']}, LP_2={a['LP2']}, G_2={a['G2']}  (atteso 4, 3, 1)")
    print()

    rows = killer_table()
    print(f"Sweep su {len(rows)} coppie (f ∈ 6 outer) x (g ∈ 9 gadget), k=2,3.")
    print()
    header = f"{'f':>4} ∘ {'g':<7} {'G1':>4} {'G2':>4} {'G3':>5}  {'mult':>5} {'aff':>4} {'poly':>5}  killed  doorC"
    print(header)
    print("-" * len(header))
    for r in rows:
        # mostra solo le righe con qualche gap, + un riassunto delle costanti-zero
        if r["G2"] != 0 or r["G3"] != 0:
            print(f"{r['f']:>4} ∘ {r['g']:<7} "
                  f"{str(r['G1']):>4} {str(r['G2']):>4} {str(r['G3']):>5}  "
                  f"{str(r['law_mult']):>5} {str(r['law_affine']):>4} {str(r['law_poly']):>5}  "
                  f"{str(r['killed']):>6}  {r['doorC_candidate']}")
    n_zero = sum(1 for r in rows if r["G2"] == 0 and r["G3"] == 0)
    print(f"... + {n_zero} celle con sequenza costante (G_1=G_2=G_3=0): killed banalmente.")
    print()

    cands = doorC_candidates()
    print(f"CANDIDATI door-C NON falsificati: {len(cands)}")
    for r in cands:
        print(f"  {r['f']} ∘ {r['g']}:  (G_1, G_2, G_3) = "
              f"({r['G1']}, {r['G2']}, {r['G3']})  "
              f"-- nessuna legge ricostruisce G_3=3/2 "
              f"(mult={r['G2'] * r['G2']}, affine={2 * r['G2'] - r['G1']}, poly=2*1=2)")


if __name__ == "__main__":
    main()
