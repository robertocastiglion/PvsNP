"""Demo del Modulo 13 — Meta-Complexity Lab (MCSP & hardness magnification).

Uso:
    py examples/run_meta_complexity.py
"""

import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
except (AttributeError, ValueError):
    pass

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from pnp_lab.meta_complexity import (  # noqa: E402
    analyze_link,
    ascii_link,
    ascii_threshold,
    complexity_map,
    magnification_results,
    meta_complexity_summary,
    mcsp_threshold,
    threshold_gap,
    to_svg_threshold,
    write_svg,
)


def main() -> None:
    print()
    print("  P/NP RESEARCH LAB — Modulo 13: Meta-Complexity Lab (MCSP)")
    print()

    ct = complexity_map(3)
    rows = mcsp_threshold(ct)

    print("=" * 72)
    print(ascii_threshold(rows))
    print()

    print("=" * 72)
    print(ascii_link(analyze_link(ct, 3)))
    print()

    print("=" * 72)
    print("  Hardness magnification (citata): piccolo LB ⇒ grande separazione")
    for f in magnification_results():
        print(f"    • {f.weak_lower_bound}")
        print(f"        ⇒ {f.implies}   [{f.reference}]")
    gap = threshold_gap()
    print(f"  {gap.known_lower_bound}")
    print(f"  {gap.magnifying_threshold}")
    print(f"  perché non basta: {gap.why_uncrossed}")
    print()

    assets = Path(__file__).resolve().parent.parent / "web" / "assets"
    assets.mkdir(parents=True, exist_ok=True)
    out = write_svg(to_svg_threshold(rows), str(assets / "meta_complexity.svg"))
    print(f"  SVG salvato: {out}")
    print()

    print(meta_complexity_summary())


if __name__ == "__main__":
    main()
