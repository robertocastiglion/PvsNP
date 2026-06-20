"""Approximate degree (6th arena) — exact via the dual-polynomial LP.

Computes adeg_{1/3}(f) for canonical tiny functions and runs the decisive reduce-to-known:
does adeg add separating power over the lab's joint orbit-invariant dictionary?

Run:  py examples/run_approx_degree.py
"""

from collections import Counter

from pnp_lab.approx_degree import adeg as A


def main() -> None:
    print("Exact approximate degree adeg_{1/3} of canonical functions:")
    print("  n=3 parity :", A.approx_degree(sum((bin(x).count("1") % 2) << x for x in range(8)), 3))
    print("  n=3 OR     :", A.approx_degree(sum((1 if x else 0) << x for x in range(8)), 3))
    print("  n=3 MAJ    :", A.approx_degree(sum((1 if bin(x).count("1") >= 2 else 0) << x for x in range(8)), 3))

    print("\nExhaustive n=3 distribution (256 functions):",
          dict(sorted(Counter(A.adeg_table(3).values()).items())))

    c2a, refines, crefines = A.adeg_vs_cost(3)
    print("\nadeg vs formula-size cost (Module 6):")
    for cst in sorted(c2a):
        print(f"   cost {cst} -> adeg {sorted(c2a[cst])}")
    print("  adeg refines cost? ", refines, " cost refines adeg? ", crefines,
          " => adeg is INCOMPARABLE with cost alone" if not refines and not crefines else "")

    reconstructible, splits = A.adeg_vs_dictionary(3)
    print("\nDecisive reduce-to-known — adeg vs the JOINT dictionary "
          "(cost, gf2_degree, sensitivity, block_sensitivity):")
    print("  reconstructible:", reconstructible, " | separating splits:", len(splits))
    print("  => RESTATEMENT: adeg collapses into the joint orbit-invariant dictionary."
          if reconstructible else "  => adeg separates beyond the dictionary (investigate).")

    print("\n" + A.honesty_note())


if __name__ == "__main__":
    main()
