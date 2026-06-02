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
    ascii_report_iterated,
    bound_report,
    depth_reduction_demo,
    parity_depth_under_restriction,
    parity_lower_bound,
    random_ac0,
    random_dnf,
    run_switching,
    switching_summary,
    iterate_summary,
    to_svg_contrast,
    to_svg_trajectory,
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
    print()

    # ── Passo #2: switching ITERATO in profondità d ──────────────────────
    print("=" * 72)
    print("  SWITCHING ITERATO  —  collasso di un AC0 a profondità d, livello dopo livello")
    print("=" * 72)
    rng2 = random.Random(7)
    circuit = random_ac0(n=50, depth=3, bottom_fanin=2, rng=rng2, bottom_terms=14, fanin=3)
    print(f"  circuito AC0: profondità {circuit.depth}, fan-in al fondo {circuit.bottom_fanin}, "
          f"dimensione {circuit.size}")
    ac0, par = depth_reduction_demo(circuit, rng2, trials=400, schedule=[0.18, 0.18])
    print(ascii_report_iterated(ac0, par))
    print()
    out2 = write_svg(to_svg_trajectory(ac0, par), str(assets / "switching_iterated.svg"))
    print(f"  SVG salvato: {out2}")
    print()
    print(bound_report(parity_lower_bound(n=1000, depth=3)))
    print()
    print(iterate_summary())


if __name__ == "__main__":
    main()
