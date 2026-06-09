"""Demo: TINY-INSTANCE COLLAPSE — la cristallizzazione di chiusura (Module 19).

Stampa i witness riproducibili della meta-conclusione del loop di ricerca:
  - killer-1: input-negation è un automorfismo del costo (d_negation ≡ 0);
  - W1: d_flip è il GRADIENTE esatto di MCSP-size (ricostruibile da cost solo);
  - W2: d_flip NON è canonico (cambia tra formula-size e profondità DT);
  - falsificatore: NON trovato nella toolbox -> collasso confermato.

NON è un risultato su P vs NP: è una constatazione sul METODO del loop su
istanze finite (n<=4).
"""

import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from pnp_lab.meta_complexity.collapse import collapse_summary, falsifier_status


def render(n: int) -> None:
    s = collapse_summary(n)
    print(f"\n=== n = {n}  ({s.num_funcs} funzioni) ===")
    print(f"  killer-1  d_negation>0 : {s.negation_nonzero:>6}  "
          f"→ {'CONFERMATO (automorfismo del costo)' if s.negation_nonzero == 0 else 'NON banale'}")
    print(f"  W1  d_flip ≠ gradiente : {s.gradient_mismatch:>6}  "
          f"→ {'d_flip = gradiente ESATTO di cost (derivata di un oggetto-KT)' if s.gradient_mismatch == 0 else 'NON ricostruibile da cost'}")
    print(f"  W2  d_flip non-canonico: {s.canonicity_mismatch:>4}/{s.canonicity_total}  "
          f"({s.canonicity_fraction:.1%})  → cambia tra formula-size e DT-depth")
    fs = falsifier_status(n)
    print(f"  falsificatore trovato  : {str(fs.found):>6}  → {fs.note}")


if __name__ == "__main__":
    print("TINY-INSTANCE COLLAPSE — chiusura del loop di ricerca (5 RESTATEMENT).")
    print("Meta-conclusione: su n<=4 ogni discriminante locale costruito si riduce,")
    print("via identità ESATTA, a un invariante già nel dizionario μ_R. NON è P vs NP.")
    render(3)
    if "--n4" in sys.argv:
        render(4)
    else:
        print("\n(passa --n4 per i witness su n=4, esaustivi e più lenti)")
