"""Demo del Modulo 5 — Proof Complexity Lab.

Esegue:  py examples/run_proof_complexity.py
"""

import os
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")  # console Windows in cp1252
except (AttributeError, ValueError):
    pass

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from pnp_lab.proof_complexity import (
    ascii_chart,
    dpll,
    horn_chain_cnf,
    pigeonhole_cnf,
    refute,
    run_growth_study,
    write_svg,
)


def main() -> None:
    print("=" * 66)
    print("  P/NP RESEARCH LAB — Modulo 5: Proof Complexity Lab")
    print("=" * 66)

    # --- una refutazione VERA, esibita ---------------------------------
    print("\n── Una refutazione per resolution (PHP 3 piccioni / 2 buche) ──")
    cnf = pigeonhole_cnf(3, 2)
    print(f"  {cnf.describe()}")
    res = refute(cnf, max_clauses=50000)
    print(f"  {res.detail}")
    print(f"  risolventi generati: {res.generated}")

    # --- contrasto: insoddisfacibile ma FACILE -------------------------
    print("\n── Contrasto: insoddisfacibile ma facile (catena di Horn) ────")
    horn = horn_chain_cnf(10)
    hres = dpll(horn)
    print(f"  {horn.describe()}")
    print(f"  {hres.pretty()}")
    print("  → propagazione unitaria pura: refutazione LINEARE, 0 decisioni.")

    # --- la crescita esponenziale (il cuore) ---------------------------
    print("\n── Il muro di Haken: dimensione della prova vs taglia ─────────")
    study = run_growth_study(max_holes=6, node_budget=2_000_000, time_budget=4.0)
    print(ascii_chart(study))
    print(f"\n  VERDETTO: {study.verdict()}")
    if any(r.aborted for r in study.rows):
        print("  (* = budget superato: la prova è semplicemente troppo grande)")

    # --- export SVG per la pagina/canale -------------------------------
    here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    out = os.path.join(here, "web", "assets", "proof_growth.svg")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    write_svg(study, out)
    print(f"\n  Grafico SVG esportato in: {out}")

    print("\n" + "=" * 66)
    print("  Cook–Reckhow: lower bound forti su OGNI sistema di prova")
    print("  ⇒ NP ≠ coNP ⇒ P ≠ NP. La proof complexity è una vera strada.")
    print("=" * 66)


if __name__ == "__main__":
    main()
