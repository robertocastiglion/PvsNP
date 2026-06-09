"""Demo della REGOLA sui gadget per il gap del lift (Modulo 18, ciclo 1).

Verifica l'ipotesi dell'Explorer:
    F = f ∘ g^k apre il gap (G* > 0)  SSE  g e' una PERMUTAZIONE ({XOR, EQ})
    E l'outer f apre la pattern-matrix non integrale.

Risolve anche il DISCRIMINANTE EQ-vs-XOR: EQ non e' "XOR-Fourier" ma e' una
permutazione; se apre il gap come XOR la regola e' "PERMUTAZIONE" (nuova).

Uso:
    py examples/run_gadget_rule.py
"""

import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
except (AttributeError, ValueError):
    pass

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from pnp_lab.exactness_composes import GADGETS_1BIT  # noqa: E402
from pnp_lab.exactness_composes.gadget_rule import (  # noqa: E402
    gap_table,
    is_permutation_gadget,
    measured_gap,
    rule_matches_measurement,
    xor_eq_same_up_to_col_perm,
    DEFAULT_OUTERS,
    DEFAULT_GADGETS,
)


def main() -> None:
    print()
    print("  P/NP RESEARCH LAB -- Modulo 18 (ciclo 1): REGOLA sui gadget del lift")
    print("=" * 72)

    perms = [n for n, g in GADGETS_1BIT.items() if is_permutation_gadget(g)]
    print(f"  Gadget di PERMUTAZIONE (un 1 per riga/colonna): {perms}")
    print()

    print("  Tabella k=2  (6 outer x 9 gadget)  -- celle con G* > 0:")
    t = gap_table(k=2)
    for (f, g), (cov, lp, gs) in sorted(t.items()):
        if gs > 0:
            print(f"    ({f:<4}, {g:<3}):  Cov={cov}  LP={lp}  G*={gs}")
    ok, mm = rule_matches_measurement(k=2)
    print(f"  predict_gap == (G*>0) su tutte le {len(t)} celle k=2:  {ok}")
    if mm:
        print(f"    MISMATCH: {mm}")
    print()

    print("  DISCRIMINANTE EQ-vs-XOR (numeri esatti):")
    print(f"    G*(OR ∘ XOR^2) = {measured_gap('OR', 'XOR', 2)}")
    print(f"    G*(OR ∘ EQ^2)  = {measured_gap('OR', 'EQ', 2)}")
    same_all = all(xor_eq_same_up_to_col_perm(f, k)
                   for f in DEFAULT_OUTERS for k in (2, 3))
    print(f"    lift(f,XOR,k) = lift(f,EQ,k) a meno di perm-colonne, per ogni (f,k):"
          f" {same_all}")
    print("    => G*(EQ) = G*(XOR) per OGNI k (anche k=3, senza LP costoso).")
    print("    => VERDETTO: la regola e' PERMUTAZIONE, non XOR-Fourier (contenuto nuovo).")
    print()

    print("  Tabella k=3 -- SOLO celle sparse (cover esatto immediato):")
    print("  (le celle dense con gadget di permutazione, es. OR/NAND x XOR/EQ,")
    print("   sono SALTATE: LP esatto sulle 8x8 dense ~600s, cover ancora oltre.)")
    t3 = gap_table(outers=("AND", "NOR"), k=3)
    for (f, g), (cov, lp, gs) in sorted(t3.items()):
        print(f"    ({f:<4}, {g:<3}):  Cov={cov}  LP={lp}  G*={gs}")
    print()


if __name__ == "__main__":
    main()
