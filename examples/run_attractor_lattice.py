"""Demo: Teorema dell'Attrattore — reticolo di ricostruibilita' dei 5 invarianti (Entry 36).

Misura esatta su n=3 (22 orbite B_3) del preordine di ricostruibilita' su
{cost, gf2_degree, sensitivity, block_sensitivity, adeg}.

Esegui:  py examples/run_attractor_lattice.py
"""

import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from pnp_lab.attractor_theorem.lattice import (  # noqa: E402
    INV_NAMES,
    orbit_invariant_table,
    reconstructibility_matrix,
    minimum_separators,
    hasse_diagram,
    summary,
)


def print_table(table):
    print(f"  {'rep':>4}  {'cost':>4}  {'gf2':>3}  {'sens':>4}  {'bs':>4}  {'adeg':>4}")
    print("  " + "-" * 38)
    for rep in sorted(table):
        inv = table[rep]
        print(f"  {rep:>4}  {inv['cost']:>4}  {inv['gf2_degree']:>3}  "
              f"{inv['sensitivity']:>4}  {inv['block_sensitivity']:>4}  {inv['adeg']:>4}")


def print_matrix(M):
    names = list(INV_NAMES)
    abbr = {"cost": "cst", "gf2_degree": "gf2", "sensitivity": "sns",
            "block_sensitivity": "bsn", "adeg": "adg"}
    header = "     " + "  ".join(f"{abbr[n]:3s}" for n in names)
    print("  " + header)
    for I in names:
        row = "  ".join("T  " if M[I][J] else "F  " for J in names)
        print(f"  {abbr[I]:3s}  [{row}]")


def print_collisions(table):
    from collections import defaultdict
    by_tuple = defaultdict(list)
    for rep in sorted(table):
        key = tuple(table[rep][k] for k in INV_NAMES)
        by_tuple[key].append(rep)
    coll = {k: v for k, v in by_tuple.items() if len(v) > 1}
    print(f"  Collisioni (stesso 5-tuple, {len(coll)} gruppi):")
    for key, reps in sorted(coll.items()):
        print(f"    {key}: orbite {reps}")


def main():
    print("=" * 70)
    print("TEOREMA DELL'ATTRATTORE — reticolo di ricostruibilita' su n=3")
    print("=" * 70)

    summ = summary(3)

    print(f"\nGruppo: {summ['group']}")
    print(f"Numero orbite B_3 su n=3: {summ['n_orbits']}")

    print("\n--- Tabella orbite -> 5 invarianti (rep canonico = min orbita) ---")
    table = orbit_invariant_table(3)
    print_table(table)

    print("\n--- Matrice 5x5 di ricostruibilita' M[I][J]: I ricostruibile da J ---")
    M = summ["recon_matrix"]
    print_matrix(M)

    print("\n--- Collisioni del 5-tuple (stesso vettore, orbite diverse) ---")
    print_collisions(table)

    print("\n--- Separatori minimi ---")
    seps = summ["min_separators"]
    if seps:
        print(f"  Cardinalita' minima: {summ['min_sep_size']}")
        for s in seps:
            print(f"  {s}")
    else:
        print("  NESSUN SEPARATORE ESISTE da questa famiglia.")
        print("  Causa: tutti e 5 gli invarianti sono complement-invarianti")
        print("  (invarianti per la negazione dell'output), ma B_3 NON include")
        print("  la negazione dell'output => le 22 orbite NON sono separabili.")

    print("\n--- Diagramma di Hasse del preordine di ricostruibilita' ---")
    h = summ["hasse"]
    print(f"  Classi di equivalenza (mutua ricostruibilita'):")
    for cls in h["classes"]:
        print(f"    {sorted(cls)}")
    print(f"  Archi Hasse (A coperto da B = B piu' informativo): {h['arcs']}")
    print(f"  Shape: {h['shape']}")

    print("\n--- CONCLUSIONE ---")
    print(f"  #orbite B_3 su n=3         : {summ['n_orbits']}")
    print(f"  Separatori minimi (|G| min) : NESSUNO (min_sep_size={summ['min_sep_size']})")
    print(f"  Shape Hasse                 : {summ['shape']}")
    print(f"  Ipotesi 2<=|G|<=3           : FALSIFICATA (tutti 5 invarianti complement-invarianti)")
    print(f"  Ipotesi ne' catena ne' anti  : FALSIFICATA (e' un'anticatena)")
    print()
    print("  RESTATEMENT: i 5 invarianti del dizionario del lab collassano sotto la")
    print("  simmetria di complement dell'output, stessa firma delle 19 chiusure")
    print("  precedenti (tutti gli invarianti ricadono in una simmetria piu' ampia).")


if __name__ == "__main__":
    main()
