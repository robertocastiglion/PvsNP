"""Demo del Modulo 18 -- EXACTNESS COMPOSES (killer search).

Risolve la congettura post-audit: la classe delle relazioni a copertura INTEGRALE
(gap pinnato sul LP  G* = Cov - LP = 0) e' chiusa per gadget composition?
Esito: VERA per il tensore (ma corollario della moltiplicativita' LP), FALSA per il
lift -- controesempio = matrice di disuguaglianza J - I_4 su 4 bit, G* = 1.

Uso:
    py examples/run_exactness_composes.py
"""

import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
except (AttributeError, ValueError):
    pass

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from pnp_lab.exactness_composes import gap_table, report, witness_note  # noqa: E402


def main() -> None:
    print()
    print("  P/NP RESEARCH LAB -- Modulo 18: EXACTNESS COMPOSES (killer search)")
    print()
    print("=" * 72)
    print(report())
    print()
    print("=" * 72)
    print("  Controesempi-lift (gadget INTEGRALE, gap aperto):")
    print(gap_table())
    print()
    print("=" * 72)
    print(witness_note())
    print()


if __name__ == "__main__":
    main()
