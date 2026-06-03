"""Demo del Modulo 15 — Distinguishing Advantage Sandbox.

Misura ESATTA su n=3 del vantaggio di distinzione ε(ℓ, s) di un osservatore che
prova a separare funzioni DURE (istanze MCSP) da FACILI, al variare di due assi
ortogonali: informazione (fan-in ℓ delle oracle gate) e calcolo (numero s di
gate). Si cerca il "punto di rottura": serve ℓ e s alti INSIEME per ε > 0?

Uso:
    py examples/run_distinguishing_advantage.py
"""

import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
except (AttributeError, ValueError):
    pass

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from pnp_lab.distinguishing import (  # noqa: E402
    advantage_matrix,
    ascii_matrix,
    default_split,
    distinguishing_summary,
    to_svg_matrix,
    write_svg,
)


def main() -> None:
    print()
    print("  P/NP RESEARCH LAB — Modulo 15: Distinguishing Advantage Sandbox")
    print()
    print(distinguishing_summary())
    print()
    print("=" * 72)
    split = default_split()
    m = advantage_matrix(split)
    print(ascii_matrix(m))
    print()

    assets = Path(__file__).resolve().parent.parent / "web" / "assets"
    assets.mkdir(parents=True, exist_ok=True)
    out = write_svg(to_svg_matrix(m), str(assets / "distinguishing_advantage.svg"))
    print(f"  SVG salvato: {out}")


if __name__ == "__main__":
    main()
