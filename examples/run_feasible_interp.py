"""Demo ciclo 3: feasible interpolation misurata su famiglie split tiny.

Esegui:  py examples/run_feasible_interp.py
"""
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
except (AttributeError, ValueError):
    pass

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from pnp_lab.feasible_interp.families import or_family, and_family  # noqa: E402
from pnp_lab.feasible_interp.interp import (  # noqa: E402
    dag_refute, build_interpolant, verify_interpolant, min_interpolant_dt_size,
)


def main() -> None:
    print("FEASIBLE INTERPOLATION sul piccolo — costruzione di Krajíček/Pudlák")
    print("=" * 70)
    for name, fam in [("OR(z)", or_family), ("AND(z)", and_family)]:
        print(f"\nFamiglia interpolante = {name}")
        print(f"{'n':>2} | {'sat.steps':>9} | {'interp':>6} {'mux':>4} {'bool':>4} "
              f"| {'verify':>6} | {'min_DT':>6}")
        for n in range(1, 6):
            s = fam(n)
            ref = dag_refute(s)
            interp = build_interpolant(s, ref)
            ver = verify_interpolant(s, interp)
            mn = min_interpolant_dt_size(s)["min_leaves"]
            print(f"{n:>2} | {ref.steps:>9} | {interp.gate_count:>6} "
                  f"{interp.mux_gates:>4} {interp.bool_gates:>4} | "
                  f"{'OK' if ver['ok'] else 'FAIL':>6} | {mn:>6}")
    print("\nLettura: #MUX = #variabili shared = passi-su-shared del DAG (Krajíček).")
    print("I passi di saturazione esplodono, l'interpolante resta lineare e ~minimo.")
    print("Honesty boundary: misure esatte ≤5 bit shared; il minimo è su albero di")
    print("decisione, non su circuito generale; i gate OR/AND privati hanno operandi")
    print("costanti/uguali su queste famiglie (regola a→OR/b→AND dal teorema).")


if __name__ == "__main__":
    main()
