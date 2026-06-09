"""Demo del Modulo 16 — Bounded Observer.

Un'unica definizione di osservatore limitato T = (𝒜, 𝒭, t) e un unico vantaggio di
distinzione Δ(𝒞; D0, D1). Misura ESATTA su istanze minuscole di quali barriere si
scrivono come Δ ≤ ε e dove (esattamente) la proof complexity esce dal template.

Uso:
    py examples/run_bounded_observer.py
"""

import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
except (AttributeError, ValueError):
    pass

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from pnp_lab.bounded_observer import (  # noqa: E402
    unified_report,
    unified_summary,
    verdict_note,
)


def main() -> None:
    print()
    print("  P/NP RESEARCH LAB — Modulo 16: Bounded Observer")
    print()
    print(unified_summary())
    print()
    print("=" * 72)
    print(unified_report())
    print()
    print("=" * 72)
    print(verdict_note())
    print()


if __name__ == "__main__":
    main()
