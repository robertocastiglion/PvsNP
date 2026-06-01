"""Demo del Modulo 9 — Algebraic Query Model (mondi algebrici).

Uso:
    py examples/run_algebraic_worlds.py
"""

import random
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
except (AttributeError, ValueError):
    pass

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from pnp_lab.algebraic_worlds import (  # noqa: E402
    algebraic_worlds_summary,
    ascii_limit,
    ascii_power,
    cube_queries,
    interpolation_lower_bound,
    planted_detection,
    random_queries,
    to_svg_worlds,
    write_svg,
)


def main() -> None:
    print()
    print("  P/NP RESEARCH LAB — Modulo 9: Algebraic Query Model")
    print()

    m, p = 4, 17

    # --- Mondo 1: potenza ---------------------------------------------------
    det = planted_detection(m=m, p=p, planted_index=5)
    print("=" * 72)
    print(ascii_power(det))
    print()

    # --- Mondo 2: limite ----------------------------------------------------
    print("=" * 72)
    rng = random.Random(2026)
    bounds = []
    for k in [1, 4, 8, 12, (1 << m) - 1]:
        bounds.append(interpolation_lower_bound(m, p, random_queries(m, p, k, rng)))
    bounds.append(interpolation_lower_bound(m, p, cube_queries(m)))  # 2^m = determinato
    print(ascii_limit(bounds))
    print()

    # --- SVG ----------------------------------------------------------------
    assets = Path(__file__).resolve().parent.parent / "web" / "assets"
    assets.mkdir(parents=True, exist_ok=True)
    out = write_svg(to_svg_worlds(det, bounds), str(assets / "algebraic_worlds.svg"))
    print(f"  SVG salvato: {out}")
    print()

    print(algebraic_worlds_summary())


if __name__ == "__main__":
    main()
