"""Demo del Modulo 7 — Algebrization Sandbox.

Uso:
    py examples/run_algebrization.py
"""

import random
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
except (AttributeError, ValueError):
    pass

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from pnp_lab.algebrization import (  # noqa: E402
    Field,
    MultilinearExtension,
    algebrization_summary,
    ascii_transcript,
    count_true,
    run_sumcheck,
    to_svg_ladder,
    write_svg,
)


def main() -> None:
    print()
    print("  P/NP RESEARCH LAB — Modulo 7: Algebrization Sandbox")
    print()

    p = 97
    F = Field(p)
    # una funzione booleana su 3 variabili (5 assegnamenti veri)
    values = (0, 1, 1, 0, 1, 1, 0, 1)
    n = 3
    ext = MultilinearExtension(values, n, F)

    print("=" * 72)
    print("  ESTENSIONE MULTILINEARE  f~  (l'oggetto algebrico)")
    print("=" * 72)
    print(f"  f su {{0,1}}^{n} = {values}   (assegnamenti veri: {count_true(values)})")
    print(f"  f~ coincide con f sul cubo?           {ext.agrees_on_cube()}")
    print(f"  f~ è multilineare (grado ≤ 1 / var)?  {ext.is_multilinear()}")
    print(f"  Ma FUORI dal cubo f~ è un vero polinomio: f~(2,3,4) = {ext((2, 3, 4))}")
    print()

    print("=" * 72)
    print("  SUM-CHECK  —  verificare Σ_cube f~ con UNA sola query")
    print("=" * 72)
    honest = run_sumcheck(ext, n, F, degree=1, rng=random.Random(7))
    print(ascii_transcript(honest, p=p, honest=True))
    print()
    cheat = run_sumcheck(ext, n, F, degree=1, rng=random.Random(7), cheat=True)
    print(ascii_transcript(cheat, p=p, honest=False))
    print()

    # --- SVG nel brand ------------------------------------------------------
    assets = Path(__file__).resolve().parent.parent / "web" / "assets"
    assets.mkdir(parents=True, exist_ok=True)
    svg = to_svg_ladder(honest, n_terms=1 << n)
    out = write_svg(svg, str(assets / "algebrization_ladder.svg"))
    print(f"  SVG salvato: {out}")
    print()

    print(algebrization_summary())


if __name__ == "__main__":
    main()
