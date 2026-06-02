"""Demo del Modulo 14 riparato verso (S).

Mostra le tre lenti riparate: 'dimostrare' = refutazione reale (SAT di sintesi),
'riconoscere' = miglior proprietà di una classe a risorse, metrica stratificata.

Uso:
    py examples/run_enriched_meta_repaired.py
"""

import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
except (AttributeError, ValueError):
    pass

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from pnp_lab.circuits import parity_table  # noqa: E402
from pnp_lab.meta_complexity import complexity_map  # noqa: E402
from pnp_lab.enriched_meta import (  # noqa: E402
    proof_axis,
    recognize_axis,
    reverdict,
    shared_measure,
    size_distribution,
)


def _tt(bits):
    v = 0
    for t, b in enumerate(bits):
        if b:
            v |= 1 << t
    return v


def main() -> None:
    print()
    print("  P/NP RESEARCH LAB — Modulo 14 riparato verso (S)")
    print()

    print("=" * 72)
    print("  Misura condivisa (dimensione di circuito esatta via SAT), n=2:")
    size2 = shared_measure(2)
    print(f"    distribuzione size: {size_distribution(size2)}")
    print()

    print("=" * 72)
    print("  Lente 'dimostrare' — lunghezza di refutazione reale del lower bound:")
    AND3 = _tt([0, 0, 0, 0, 0, 0, 0, 1])
    XOR2 = _tt([0, 1, 1, 0])
    for p in proof_axis([("XOR2 (n=2)", XOR2, 2), ("AND3 (n=3)", AND3, 3)]):
        if p.is_lower_bound:
            print(f"    {p.name}: size={p.size} · refuta size>{p.threshold} "
                  f"in {p.refutation_nodes} nodi (resolution tree-like)")
        else:
            print(f"    {p.name}: size={p.size} · lower bound non confermato (muro/abort)")
    print("    [n=3, funzioni dure: la refutazione ESPLODE — il muro reale della")
    print("     proof complexity, non un artefatto.]")
    print()

    print("=" * 72)
    print("  Lente 'riconoscere' — prezzo della costruttività sulla finestra critica:")
    ct = complexity_map(3)
    for s in (2, 3, 4):
        ax = recognize_axis(ct.cost, 3, s=s, max_depth=3, half_width=1)
        curve = " → ".join(f"d{c.depth}:{c.error_rate:.2f}" for c in ax.curve)
        tail = "NON svanisce" if not ax.vanishes else "svanisce"
        print(f"    n=3 s={s} (finestra {ax.window_size}): {curve}   [{tail}]")
    print()

    print("=" * 72)
    rv = reverdict()
    print(f"  RI-VERDETTO: {rv.classification}")
    print(f"    • tautologia rimossa: {rv.tautology_removed}")
    print(f"    • collasso rimosso:   {rv.vanishing_removed}")
    print(f"    • nuovo muro:         {rv.new_failure_mode}")
    print(f"    • punto aperto:       {rv.open_point}")
    print(f"  {rv.conclusion}")
    print()


if __name__ == "__main__":
    main()
