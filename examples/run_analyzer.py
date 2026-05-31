"""Demo: passa ogni proprietà di esempio nel Natural Proofs Analyzer.

Uso:
    py examples/run_analyzer.py
"""

import sys
from pathlib import Path

# la console Windows usa spesso cp1252: forziamo UTF-8 per emoji e simboli (µ, ⚠️)
try:
    sys.stdout.reconfigure(encoding="utf-8")
except (AttributeError, ValueError):
    pass

# rende importabile il pacchetto pnp_lab quando si lancia lo script direttamente
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from pnp_lab.natural_proofs import analyze  # noqa: E402
from pnp_lab.natural_proofs.properties import ALL_PROPERTIES  # noqa: E402


def main() -> None:
    print()
    print("  P/NP RESEARCH LAB — Modulo 1: Natural Proofs Analyzer")
    print("  Razborov–Rudich (1994): costruttiva + larga => non separa P/NP")
    print()

    for prop in ALL_PROPERTIES:
        print("-" * 68)
        print(f"  Proprietà: {prop.name}")
        for line in prop.description.splitlines():
            print(f"    {line}" if line else "")
        print("-" * 68)
        # high_circuit_complexity è costosa: limitiamo il range di n
        if prop.name == "high_circuit_complexity":
            report = analyze(
                prop,
                largeness_ns=(2, 3),
                constructiveness_ns=(2, 3, 4),
            )
        else:
            report = analyze(prop)
        print(report)
        print()


if __name__ == "__main__":
    main()
