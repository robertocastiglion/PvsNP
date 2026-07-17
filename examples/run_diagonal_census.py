"""Demo: censimento dei vanishing DIAGONALI g(lam,lam,lam)=0 per d=1..12 (Entry 40).

Esegui:
    py examples/run_diagonal_census.py
"""

import sys

sys.stdout.reconfigure(encoding="utf-8")

from pnp_lab.gct_kronecker.diagonal_census import summary


if __name__ == "__main__":
    result = summary(d_max=12)
    print(f"\nRisultato summary:")
    print(f"  total_zeros  = {result['total_zeros']}")
    print(f"  by_category  = {result['by_category']}")
    print(f"  #uncovered   = {len(result['uncovered'])}")
