"""Driver per la verifica dell'ortogonalita' di colonna E di riga dei caratteri di S_d.
Stampa anche i conteggi del gruppo spurio (Entry 76).

Esegue column_orthogonality_check e row_orthogonality_check per d=2..6,
poi spurious_group_size per d=2..6.

Uso:
    py examples/run_orthogonality.py
"""

from __future__ import annotations

import sys
import time

# Riconfigura stdout a utf-8 (evita crash su cp1252 su Windows)
sys.stdout.reconfigure(encoding="utf-8")

from pnp_lab.gct_kronecker.orthogonality import (
    column_orthogonality_check,
    row_orthogonality_check,
    dim_degeneracy_blocks,
    spurious_group_size,
)

SEPARATOR = "-" * 60


def main() -> None:
    # --- Ortogonalita' di colonna ---
    print("ORTOGONALITA' DI COLONNA: sum_lam chi^lam(a)*chi^lam(b) = z_a * delta_{ab}")
    print(SEPARATOR)
    print(f"{'d':>3}  {'classi':>7}  {'coppie':>7}  {'tempo':>7}  {'esito'}")
    print(SEPARATOR)

    col_overall = True
    for d in range(2, 9):
        t0 = time.perf_counter()
        result = column_orthogonality_check(d)
        elapsed = time.perf_counter() - t0
        esito = "PASS" if result.all_pass else f"FAIL ({len(result.violations)} viol.)"
        print(f"{d:>3}  {result.num_classes:>7}  {result.num_pairs_checked:>7}"
              f"  {elapsed:>6.3f}s  {esito}")
        if not result.all_pass:
            col_overall = False
            for v in result.violations[:3]:
                print(f"      VIOLAZIONE: alpha={v.alpha}, beta={v.beta},"
                      f" atteso={v.expected}, ottenuto={v.obtained}")

    print(SEPARATOR)
    if col_overall:
        print("  COL-ORTO: PASS -- chi3 soddisfa l'ortogonalita' di colonna.")
    else:
        print("  COL-ORTO: FAIL CRITICO -- engine3 errato!")

    # --- Ortogonalita' di riga ---
    print()
    print("ORTOGONALITA' DI RIGA: sum_alpha |C_a| chi^lam(a)*chi^rho(a) = d! * delta_{lr}")
    print(SEPARATOR)
    print(f"{'d':>3}  {'irreps':>7}  {'coppie':>7}  {'tempo':>7}  {'esito'}")
    print(SEPARATOR)

    row_overall = True
    for d in range(2, 7):
        t0 = time.perf_counter()
        result = row_orthogonality_check(d)
        elapsed = time.perf_counter() - t0
        esito = "PASS" if result.all_pass else f"FAIL ({len(result.violations)} viol.)"
        print(f"{d:>3}  {result.num_irreps:>7}  {result.num_pairs_checked:>7}"
              f"  {elapsed:>6.3f}s  {esito}")
        if not result.all_pass:
            row_overall = False
            for v in result.violations[:3]:
                print(f"      VIOLAZIONE: lam={v.lam}, rho={v.rho},"
                      f" atteso={v.expected}, ottenuto={v.obtained}")

    print(SEPARATOR)
    if row_overall:
        print("  RIGA-ORTO: PASS -- chi3 soddisfa l'ortogonalita' di riga.")
    else:
        print("  RIGA-ORTO: FAIL CRITICO -- engine3 errato!")

    # --- Blocchi degeneri e gruppo spurio (Entry 76) ---
    print()
    print("GRUPPO SPURIO (Entry 76): permutazioni di righe interne ai blocchi dim-degeneri")
    print("Il sistema [col-orto + riga-orto + ancoraggio dim] NON e' caratterizzante.")
    print(SEPARATOR)
    print(f"{'d':>3}  {'|blocchi|':>10}  {'|gruppo spurio|':>16}  blocchi degeneri")
    print(SEPARATOR)

    attesi = {3: 2, 4: 4, 5: 8, 6: 192}
    for d in range(2, 7):
        blocks = dim_degeneracy_blocks(d)
        size = spurious_group_size(d)
        atteso = attesi.get(d, "?")
        match = "OK" if size == atteso else f"MISMATCH (atteso {atteso})"
        block_str = ", ".join(str(b) for b in blocks) if blocks else "(nessuno)"
        print(f"{d:>3}  {len(blocks):>10}  {size:>16}  {match}  {block_str}")

    print(SEPARATOR)
    print("Valori attesi dall'explorer: d=3->2, d=4->4, d=5->8, d=6->192")
    print("Conclusione: gruppo spurio non banale per d>=3 => circolarita' NON chiusa.")


if __name__ == "__main__":
    main()
