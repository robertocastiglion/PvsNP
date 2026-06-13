"""Direzione A, ciclo 1 — geometria dello spazio delle soluzioni (OGP minuscolo).

    py examples/run_solution_geometry.py        # n=3 (veloce, sotto-soglia)
    py examples/run_solution_geometry.py --n4    # n=4 decisivo (lento, costruisce la
                                                 #   tabella dei costi a 4 var)
"""

import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from pnp_lab.meta_complexity.solution_geometry import analyze


def show(n: int) -> None:
    r = analyze(n)
    print(f"\n=== n={n}  ({r.num_funcs} funzioni) ===")
    print(f"  classi-scalare (cost,|orbita B_n±|,N_min) : {r.num_scalar_classes}")
    print(f"  + geometria dello spazio soluzioni        : {r.num_geo_classes}")
    print(f"  coppie separate dalla sola geometria      : {len(r.separated)}")
    print(f"  K2 canonico (ordinato<->non-ordinato)     : {r.k2_canonical}")
    print(f"  VERDETTO                                  : {r.verdict}")
    for s in r.separated[:6]:
        print(f"    key={s.scalar_key}  pair={s.pair}")
        print(f"       A: dag={s.geom_a[0]} branch={s.geom_a[1]} front={s.geom_a[2]}")
        print(f"       B: dag={s.geom_b[0]} branch={s.geom_b[1]} front={s.geom_b[2]}")


def main() -> None:
    print("DIREZIONE A — la GEOMETRIA dell'insieme delle formule ottime separa funzioni")
    print("di pari (cost, |orbita|, N_min)?  Rompe scalare(1) + unario(3) + covering(2).")
    show(3)
    print("\nNota: a n=3 le 14 classi-scalare == |P_orbit±|=14 → test VACUO (sotto-soglia).")
    if "--n4" in sys.argv:
        show(4)
    else:
        print("Passa --n4 per il caso decisivo (lento).")
    print("\nRisultato n=4 (atteso): la geometria raffina 209->222==|P_orbit±| e separa 12+")
    print("coppie, MA ognuna è già in σ(cost) (cofactor_cost_profile del Ciclo 6) →")
    print("RESTATEMENT. La direzione A non esce da σ(cost) (serve la direzione B).")
    print("\nHonesty boundary: METODO su istanze FINITE, NON un claim su P vs NP.")


if __name__ == "__main__":
    main()
