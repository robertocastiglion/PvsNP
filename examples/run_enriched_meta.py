"""Demo del Modulo 14 — Enriched Meta-Category (difetto di composizione).

Uso:
    py examples/run_enriched_meta.py
"""

import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
except (AttributeError, ValueError):
    pass

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from pnp_lab.meta_complexity import complexity_map  # noqa: E402
from pnp_lab.enriched_meta import (  # noqa: E402
    Category,
    ascii_cikk,
    ascii_gap,
    ascii_matrix,
    check_isometry,
    cikk_island,
    defect_matrix,
    enriched_metacategory_summary,
    evaluate_lenses,
    framework_citations,
    irreducible_recognize_gap,
    proof_length_for_threshold,
    to_svg_matrix,
    write_svg,
)


def main() -> None:
    print()
    print("  P/NP RESEARCH LAB — Modulo 14: Enriched Meta-Category")
    print("  Le tre lenti (calcolare/dimostrare/riconoscere) sono la stessa freccia?")
    print()

    ct = complexity_map(3)
    s = 3

    print("=" * 72)
    rep = check_isometry(Category(n=3), ct.cost, measure="MCSP")
    print(f"  Categoria C: {rep.num_orbits} orbite (classi di iso sotto rinomina).")
    print(f"  Il costo MCSP è invariante sui morfismi? {'sì ✓' if rep.invariant else 'no'} "
          f"({rep.violations} violazioni) ⇒ le lenti sono funtori su C.")
    print()

    needed = proof_length_for_threshold(s, 3)
    v = evaluate_lenses(ct, s=s, proof_budget=needed)
    dm = defect_matrix(v)

    print("=" * 72)
    print(ascii_matrix(dm))
    print()

    print("=" * 72)
    print(ascii_cikk(cikk_island(ct, v)))
    print()
    print(ascii_gap(irreducible_recognize_gap(ct, s)))
    print()

    print("=" * 72)
    print("  Citazioni (eseguito vs citato):")
    for c in framework_citations():
        print(f"    • {c.claim}")
        print(f"        [{c.reference}]")
    print()

    assets = Path(__file__).resolve().parent.parent / "web" / "assets"
    assets.mkdir(parents=True, exist_ok=True)
    out = write_svg(to_svg_matrix(dm, cikk_island(ct, v)),
                    str(assets / "enriched_metacategory.svg"))
    print(f"  SVG salvato: {out}")
    print()

    verdict = enriched_metacategory_summary()
    print("=" * 72)
    print(f"  VERDETTO: {verdict.headline}")
    print(f"    • {verdict.cikk_island}")
    print(f"    • {verdict.prove_axis}")
    print(f"    • {verdict.recognize_axis}")
    print(f"  {verdict.conclusion}")
    print()
    print(f"  Onestà: {verdict.honesty}")
    print()


if __name__ == "__main__":
    main()
