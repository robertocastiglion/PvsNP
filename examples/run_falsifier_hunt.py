"""Ciclo 6 — caccia al falsificatore: completezza del dizionario μ_R.

Mostra la narrazione in tre stadi su n=3 e (opzionale) il caso decisivo n=4.

    py examples/run_falsifier_hunt.py        # solo n=3 (veloce)
    py examples/run_falsifier_hunt.py --n4    # include n=4 (lento, esaustivo)
"""

import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from pnp_lab.circuits import min_formula_sizes
from pnp_lab.meta_complexity.falsifier_hunt import hunt, named_separators


def show(n: int) -> None:
    ct = min_formula_sizes(n, 60)
    print(f"\n=== n={n} ===")
    configs = [
        (False, False, False, "NAIVE   (gruppo B_n, dizionario base senza support)"),
        (True, False, False, "B_n±    (aggiunge la negazione-output al gruppo)"),
        (True, True, False, "CORRECT (B_n± + support: completo su n=3)"),
        (True, True, True, "STRONG  (+ cover_number, Fourier, cofactor-cost: chiude n=4)"),
    ]
    for on, sup, strong, tag in configs:
        r = hunt(n, output_negation=on, include_support=sup, strong=strong)
        print(f"  {tag}")
        print(f"     |P_orbit|={r.num_orbits:4d}  |P_Σ|={r.num_sigma_classes:4d}  "
              f"#split={len(r.splits):3d}  ->  {r.verdict}")
        for w in r.splits[:3]:
            f, g = w.example_pair
            sep = named_separators(f, g, n, ct, include_support=sup, strong=strong)
            print(f"       split: {w.num_orbits} orbite  coppia=({f},{g})  "
                  f"separatori-nominati={sep or 'NESSUNO'}")


def main() -> None:
    print("CICLO 6 — il dizionario μ_R determina la funzione a meno di simmetria?")
    print("Un falsificatore = una classe di P_Σ che si spezza in >=2 orbite del")
    print("gruppo di automorfismi del costo (due funzioni identiche su TUTTO μ_R).")
    show(3)
    if "--n4" in sys.argv:
        show(4)
    else:
        print("\n(passa --n4 per il caso decisivo esaustivo su 65536 funzioni)")
    print("\nHonesty boundary: è una constatazione sul METODO su istanze FINITE,")
    print("NON un claim su P vs NP. Tutto esatto (interi/Fraction).")


if __name__ == "__main__":
    main()
