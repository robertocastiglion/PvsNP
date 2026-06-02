"""Demo del Modulo 10 — la separazione P^Ã ≠ NP^Ã (cuore di query complexity).

Uso:
    py examples/run_algebraic_separation.py
"""

import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
except (AttributeError, ValueError):
    pass

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from pnp_lab.algebraic_separation import (  # noqa: E402
    ascii_separation,
    ascii_lift,
    build_oracle,
    cancellation_example,
    deterministic_lower_bound,
    lift_summary,
    separation_summary,
    to_svg_separation,
    to_svg_lift,
    write_svg,
)


def main() -> None:
    print()
    print("  P/NP RESEARCH LAB — Modulo 10: separazione P^Ã ≠ NP^Ã")
    print()

    # campo piccolo (p=3) → separazione che cresce; p=5 con N=4 → niente gap
    results = [
        deterministic_lower_bound(2, 3, cap=4),
        deterministic_lower_bound(3, 3, cap=8),
        deterministic_lower_bound(2, 5, cap=4),
    ]
    adv = cancellation_example(2, 3)

    print("=" * 72)
    print(ascii_separation(results, adv))
    print()

    assets = Path(__file__).resolve().parent.parent / "web" / "assets"
    assets.mkdir(parents=True, exist_ok=True)
    out = write_svg(to_svg_separation(results), str(assets / "algebraic_separation.svg"))
    print(f"  SVG salvato: {out}")
    print()

    print(separation_summary())
    print()

    # ── Passo #1: sollevamento query → oracolo TM ────────────────────────
    print("=" * 72)
    print("  SOLLEVAMENTO  —  da cuore a query a una lingua in NP^Ã \\ P^Ã")
    print("=" * 72)
    lift = build_oracle(p=3, m=2, base_n=2)
    print(ascii_lift(lift))
    print()
    out2 = write_svg(to_svg_lift(lift), str(assets / "algebraic_lift.svg"))
    print(f"  SVG salvato: {out2}")
    print()
    print(lift_summary())


if __name__ == "__main__":
    main()
