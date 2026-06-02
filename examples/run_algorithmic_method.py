"""Demo del Modulo 12 — Algorithmic Method Lab (Ryan Williams).

Uso:
    py examples/run_algorithmic_method.py
"""

import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
except (AttributeError, ValueError):
    pass

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from pnp_lab.algorithmic_method import (  # noqa: E402
    algorithmic_method_summary,
    analyze_all,
    ascii_speedup,
    ascii_winwin,
    benchmark,
    conj_poly,
    disjoint_dnf_poly,
    evasion_report,
    or_poly,
    to_svg_speedup,
    write_svg,
)


def main() -> None:
    print()
    print("  P/NP RESEARCH LAB — Modulo 12: Algorithmic Method Lab")
    print()

    # 1) lo speedup, esatto e verificato
    print("=" * 72)
    examples = [
        ("AND 3 letterali (n=14)", conj_poly(3, 14)),
        ("DNF 3 gruppi disgiunti (n=14)", disjoint_dnf_poly([[0, 1], [2, 3], [4, 5]], 14)),
        ("OR di 14 var (denso)", or_poly(14)),
    ]
    print(ascii_speedup(examples))
    print()

    # 1b) #SAT esplicito per profondità-2 (DNF), con TEMPI REALI
    print("=" * 72)
    print("  #SAT esplicito profondità-2 (DNF) — forza bruta vs inclusione-esclusione:")
    print(f"  {'n':>3} {'m':>3} {'brute (ms)':>12} {'IE (ms)':>10} {'speedup':>10} {'ok':>4}")
    for r in benchmark(num_terms=4, term_width=3, ns=[10, 14, 18]):
        print(f"  {r.n:>3} {r.m:>3} {r.brute_seconds*1000:>12.1f} {r.ie_seconds*1000:>10.3f} "
              f"{r.speedup_measured:>9.0f}x {'sì' if r.agree else 'NO':>4}")
    print("  → m fisso, n cresce: la forza bruta esplode (2^n), l'IE resta piatta (2^m).")
    print()

    # 2) la soglia win-win
    print("=" * 72)
    print(ascii_winwin(analyze_all()))
    print()

    # 3) aggira le tre barriere
    print("=" * 72)
    print("  Aggira le tre barriere note:")
    for b in evasion_report():
        print(f"    [{'✓' if b.evaded else '✗'}] {b.barrier}")
    print()

    assets = Path(__file__).resolve().parent.parent / "web" / "assets"
    assets.mkdir(parents=True, exist_ok=True)
    out = write_svg(to_svg_speedup(k=3, max_n=22), str(assets / "algorithmic_method.svg"))
    print(f"  SVG salvato: {out}")
    print()

    print(algorithmic_method_summary())


if __name__ == "__main__":
    main()
