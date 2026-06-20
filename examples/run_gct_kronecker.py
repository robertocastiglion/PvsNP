"""GCT / Kronecker (7th arena) — exact vanishing pattern vs known necessary conditions.

Per d=3,4,5 stampa #partizioni, #terne, #vanishing (g==0), #mismatches e — soprattutto —
l'ELENCO ESPLICITO di sporadic_vanishing (g=0 con TUTTE le NC soddisfatte = il KILLER
dell'ipotesi-lab) e di nc_false_positive (g>0 con una NC violata = bug nella NC).

Run:  py examples/run_gct_kronecker.py
"""

import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")  # evita crash cp1252 su Unicode (λ, μ, ν)
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from pnp_lab.gct_kronecker import (
    partitions,
    kronecker,
    vanishing_table,
    mismatches,
    sporadic_vanishing,
    nc_false_positive,
    covered,
    uncovered,
    coverage_summary,
    honesty_note,
)


def _fmt(p):
    return "(" + ",".join(str(x) for x in p) + ")"


def _fmt_triple(t):
    return "  ".join(_fmt(p) for p in t)


def main() -> None:
    print("=" * 78)
    print("7a arena del PvsNP-lab — coefficienti di Kronecker g(λ,μ,ν) di S_d")
    print("Ipotesi-lab: il vanishing (g==0) COLLASSA nelle NC note (length + max-part).")
    print("Killer: sporadic_vanishing non vuoto = vanishing sporadico = fuori dizionario.")
    print("=" * 78)

    for d in [3, 4, 5, 6]:
        tab = vanishing_table(d)
        n_triples = len(tab)
        n_vanish = sum(1 for (g, v, vp) in tab.values() if v)
        mis = mismatches(d)
        sp = sporadic_vanishing(d)
        fp = nc_false_positive(d)
        n_sp, n_cov, n_unc = coverage_summary(d)

        print(f"\nd = {d}")
        print(f"  #partizioni di d         : {len(partitions(d))}")
        print(f"  #terne (λ≤μ≤ν)           : {n_triples}")
        print(f"  #vanishing (g==0)        : {n_vanish}")
        print(f"  #mismatch (V ≠ V_pred)   : {len(mis)}")
        print(f"  #sporadic_vanishing      : {len(sp)}   <-- IL KILLER (g=0, tutte le NC ok)")
        print(f"  #nc_false_positive       : {len(fp)}   <-- bug NC (g>0, una NC violata)")
        print(f"  #covered                 : {n_cov}   <-- coperti da formule chiuse note (COMPUTED)")
        print(f"  #uncovered               : {n_unc}   <-- fuori-dizionario genuino (obiettivo: 0)")

        if uncovered(d):
            print("  uncovered (SOPRAVVIVENZA GENUINA fuori-dizionario):")
            for t in uncovered(d):
                print(f"     {_fmt_triple(t)}   g=0, NC ok, nessuna copertura di forma")
        else:
            print("  uncovered: [] (ogni vanishing sporadico e' COPERTO — collasso COMPUTED)")

        if fp:
            print("  nc_false_positive (DA INVESTIGARE, NON e' il killer):")
            for t in fp:
                print(f"     {_fmt_triple(t)}   g={kronecker(*t)}")
        else:
            print("  nc_false_positive: [] (le NC sono solide su questo d)")

        if sp:
            print("  sporadic_vanishing (FALSIFICA l'ipotesi-lab su questo d):")
            for t in sp:
                print(f"     {_fmt_triple(t)}   g=0, NC tutte soddisfatte")
        else:
            print("  sporadic_vanishing: [] (il vanishing COLLASSA nelle NC — ipotesi confermata)")

    print("\n" + honesty_note())


if __name__ == "__main__":
    main()
