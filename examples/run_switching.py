"""Demo del Modulo 8 — Switching Lemma Lab.

Uso:
    py examples/run_switching.py
"""

import random
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
except (AttributeError, ValueError):
    pass

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from pnp_lab.switching import (  # noqa: E402
    ascii_report,
    parity_depth_under_restriction,
    random_dnf,
    run_switching,
    switching_summary,
    to_svg_contrast,
    write_svg,
)


def main() -> None:
    print()
    print("  P/NP RESEARCH LAB — Modulo 8: Switching Lemma Lab")
    print()

    n, w, p, trials = 16, 3, 0.06, 6000
    rng = random.Random(2026)
    dnf = random_dnf(n, w, 12, rng)

    print("=" * 72)
    print("  ESPERIMENTO  —  restrizioni casuali su una DNF di larghezza w")
    print("=" * 72)
    stats = run_switching(dnf, n, p, trials, rng, width=w, max_s=4)
    parity_depth = parity_depth_under_restriction(n, p, trials, rng)
    print(ascii_report(stats, parity_depth))
    print()

    assets = Path(__file__).resolve().parent.parent / "web" / "assets"
    assets.mkdir(parents=True, exist_ok=True)
    out = write_svg(to_svg_contrast(stats, parity_depth), str(assets / "switching_contrast.svg"))
    print(f"  SVG salvato: {out}")
    print()

    print(switching_summary())


if __name__ == "__main__":
    main()
