"""Ciclo 4: misura la tripla (S, P, 2^C) su K4-triangolo.

S = taglia interpolante monotono estratto dalla refutazione dello split;
P = partition number della matrice KW+;
C = D^cc deterministico sulla stessa matrice.

Esegui:  py examples/run_kw_communication.py
"""
from __future__ import annotations

import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")  # evita crash cp1252 su unicode
except (AttributeError, ValueError):
    pass

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from pnp_lab.feasible_interp.families import clique_triangle_K4  # noqa: E402
from pnp_lab.feasible_interp.interp import (  # noqa: E402
    dag_refute, build_interpolant, build_interpolant_swapped, verify_interpolant,
)
from pnp_lab.kw_communication.kw import (  # noqa: E402
    clique_f, minterms, maxterms, kw_plus_matrix, partition_number, dcc,
)

K4_EDGES = [(1, 2), (1, 3), (1, 4), (2, 3), (2, 4), (3, 4)]
N = 6


def main() -> None:
    f = clique_f(K4_EDGES, 3)

    print("=== f = triangolo (3-clique) su K4, 6 archi ===")
    mts = minterms(f, N)
    Mts = maxterms(f, N)
    print(f"minterm (1-input minimali) : {len(mts)}  (i 4 triangoli)")
    print(f"maxterm (0-input massimali): {len(Mts)}")

    mat, rows, cols = kw_plus_matrix(f, N)
    print(f"matrice KW+ : {len(rows)} righe x {len(cols)} colonne")
    print("  entrate (coordinate-mossa legali):")
    for r in range(len(rows)):
        print("   ", [sorted(mat[r][c]) for c in range(len(cols))])

    # --- S : interpolante monotono dalla refutazione dello split ----------
    s = clique_triangle_K4()
    s.check_split()
    ref = dag_refute(s, max_clauses=200000)
    interp = build_interpolant(s, ref)
    ver = verify_interpolant(s, interp)
    S = interp.gate_count

    # --- buco-2 : lo scambio della regola privata rompe la semantica? -----
    interp_sw = build_interpolant_swapped(s, ref)
    ver_sw = verify_interpolant(s, interp_sw)
    swap_breaks = not ver_sw["ok"]

    # --- P, C : sulla matrice KW+ -----------------------------------------
    P = partition_number(mat)
    C = dcc(mat)

    print()
    print(f"refutazione: empty={ref.found_empty} capped={ref.capped} steps={ref.steps}")
    print(f"interpolante verificato OK su tutti i 64 α: {ver['ok']}")
    print(f"  S = gate distinti = {S}  (MUX={interp.mux_gates}, AND/OR={interp.bool_gates})")
    print(f"  BUCO-2: lo scambio a→AND/b→OR rompe verify_interpolant? "
          f"{'SI' if swap_breaks else 'NO (FALLIMENTO DI BANCO)'} "
          f"({len(ver_sw['violations'])} violazioni)")
    print()
    print("=== TRIPLA misurata su K4-triangolo ===")
    print(f"  S (interpolante)        = {S}")
    print(f"  P (partition number)    = {P}")
    print(f"  C (D^cc)                = {C}   ->  2^C = {2 ** C}")
    print(f"  S - P                   = {S - P}")
    print()
    disc = "RESTATEMENT" if abs(S - P) <= 1 else "S-P > 1: possibile segnale strutturale"
    print(f"  discriminante: {disc}")


if __name__ == "__main__":
    main()
