"""Driver per la verifica dell'ortogonalita' di colonna dei caratteri di S_d.

Esegue column_orthogonality_check per d=2..8 e stampa PASS/FAIL con dettagli.

Uso:
    py examples/run_orthogonality.py
"""

from __future__ import annotations

import sys
import time

# Riconfigura stdout a utf-8 (evita crash su cp1252 su Windows)
sys.stdout.reconfigure(encoding="utf-8")

from pnp_lab.gct_kronecker.orthogonality import column_orthogonality_check

SEPARATOR = "-" * 50


def main() -> None:
    print("Ortogonalita' di colonna: sum_lam chi^lam(a)*chi^lam(b) = z_a * delta_{ab}")
    print(SEPARATOR)
    print(f"{'d':>3}  {'classi':>7}  {'coppie':>7}  {'tempo':>7}  {'esito'}")
    print(SEPARATOR)

    overall_pass = True
    for d in range(2, 9):
        t0 = time.perf_counter()
        result = column_orthogonality_check(d)
        elapsed = time.perf_counter() - t0

        esito = "PASS" if result.all_pass else f"FAIL ({len(result.violations)} violazioni)"
        print(
            f"{d:>3}  {result.num_classes:>7}  {result.num_pairs_checked:>7}"
            f"  {elapsed:>6.3f}s  {esito}"
        )
        if not result.all_pass:
            overall_pass = False
            for v in result.violations[:3]:
                print(f"      VIOLAZIONE: alpha={v.alpha}, beta={v.beta},"
                      f" atteso={v.expected}, ottenuto={v.obtained}")

    print(SEPARATOR)
    print("KILLER CHECK (bidirezionale):")
    if overall_pass:
        print("  PASS — chi3 soddisfa l'ortogonalita' di colonna su ogni (alpha,beta).")
        print("  => Circolarita' concettuale su chi per alpha != 1^d RISOLTA.")
    else:
        print("  FAIL CRITICO — chi3 NON soddisfa l'ortogonalita' di colonna!")
        print("  => engine3 non calcola caratteri corretti su classi non banali.")


if __name__ == "__main__":
    main()
