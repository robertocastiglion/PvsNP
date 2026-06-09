"""Demo ciclo 2 -- il PRIMO gap di lift che NON e' J - I, a 3 bit.

Contesto: nel ciclo 1 ogni cella-gap del lift f∘g^k era la matrice di disuguaglianza
J - I (Cov=m, LP=m-1, G*=1), il gap di dualita' LP elementare. Qui mostriamo che con
un OUTER a 3 bit la pattern-matrix f(x XOR y) produce gap di TIPO DIVERSO:

  * ONE_IN_3 (esattamente un 1) -> adiacenza dell'ipercubo Q3: Cov=8, LP=6, G*=2;
  * NAE (not-all-equal)         -> Cov=4, LP=3, G*=1 ma struttura non-J-I.

Uso:
    py examples/run_pattern_gap.py
"""

import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
except (AttributeError, ValueError):
    pass

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from pnp_lab.exactness_composes.gap import cover_number, frac_cover  # noqa: E402
from pnp_lab.exactness_composes.pattern_gap import (  # noqa: E402
    is_J_minus_I_up_to_perm,
    named_3bit_outers,
    pattern_matrix,
    _ones,
)


def show(name: str) -> None:
    M = pattern_matrix(named_3bit_outers()[name], 3)
    cov, lp = cover_number(M), frac_cover(M)
    print(f"  {name}:  ones={_ones(M)}  Cov={cov}  LP={lp}  G*={cov - lp}  "
          f"J-I? {is_J_minus_I_up_to_perm(M)}")
    for row in M:
        print("      " + " ".join(map(str, row)))
    print()


def main() -> None:
    print()
    print("  P/NP RESEARCH LAB -- ciclo 2: il primo gap di lift NON-J-I (3 bit)")
    print("=" * 72)
    print("  Pattern-matrix M[x][y] = f(x XOR y) su Z2^3 (= lift f ∘ XOR^3).")
    print()
    for name in ("ONE_IN_3", "TWO_IN_3", "NAE"):
        show(name)
    print("=" * 72)
    print("  KILLER: ONE_IN_3 = adiacenza dell'ipercubo Q3, G*=2, NON J - I.")
    print("  La 'tutto-e'-J-I' del lift e' falsa gia' a 3 bit di input.")
    print()


if __name__ == "__main__":
    main()
