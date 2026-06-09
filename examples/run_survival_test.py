"""Demo del Modulo 17 — Survival Test (𝒭=∞).

Un unico test scalare classifica le barriere: si misura il vantaggio di distinzione
Δ concedendo CALCOLO ILLIMITATO. Se Δ(𝒭=∞) < 1 la barriera è information-theoretic
(incondizionata, asse 𝒜); se Δ(𝒭=∞) = 1 è computational (= pseudocasualità, asse 𝒭).

Uso:
    py examples/run_survival_test.py
"""

import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
except (AttributeError, ValueError):
    pass

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from pnp_lab.survival_test import (  # noqa: E402
    criterion_summary,
    survival_report,
    verdict_note,
)


def main() -> None:
    print()
    print("  P/NP RESEARCH LAB — Modulo 17: Survival Test (𝒭=∞)")
    print()
    print(criterion_summary())
    print()
    print("=" * 72)
    print(survival_report())
    print()
    print("=" * 72)
    print(verdict_note())
    print()


if __name__ == "__main__":
    main()
