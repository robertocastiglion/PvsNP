"""Demo: cono/politopo dei momenti di Kronecker ESATTO e caccia ai buchi (Module 30, Entry 35).

Costruisce P_D = conv{point_norm(lam,mu,nu): g>0, d<=D}, cerca i buchi (sporadic vanishing in
P_D) e li classifica superficiale/profondo/fuori-cono; poi stampa l'H-rep di P_3 con la conta
delle faccette fuori-dizionario (KILLER-2).

Esegui:  py examples/run_moment_cone.py
(d=6 e' lento, ~1 min; D=4 e' molto lento ~8 min: qui NON calcolato di default.)
"""

import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")  # evita crash su cp1252 con Δ μ ∘
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from pnp_lab.gct_kronecker.moment_cone import (  # noqa: E402
    max_parts,
    holes,
    summary,
    facet_report,
)


def show_holes(d: int, D: int) -> None:
    h = holes(d, D)
    print(f"d={d}  vs  P_{D}  (k={h['k']}, dim ambient={3*h['k']})")
    print(
        f"  (#sporadic, #in_cone, #superficiali, #profondi, #fuori_cono) = {summary(d, D)}"
    )
    if h["deep"]:
        print("  BUCHI PROFONDI (in-cono ma g(N·)=0 per N=2,3,4) — SOPRAVVIVENZA:")
        for t in h["deep"]:
            print(f"    {t}")
    else:
        print("  #profondi = 0  (nessun buco invisibile allo stretch)")
    if h["superficial"]:
        print("  buchi superficiali (in-cono, g(N·)>0 per qualche N≤4):")
        for t in h["superficial"]:
            print(f"    {t}")


def show_facets(D: int) -> None:
    rep = facet_report(D)
    k = rep["k"]
    print(f"\nFaccette di P_{D}  (k={k}, dim ambient={3*k}):")
    print(
        f"  #faccette = {rep['n_facets']}  |  in-dizionario = {rep['n_in_dictionary']}  |  "
        f"fuori-dizionario = {rep['n_out_of_dictionary']}"
    )
    ex_in = rep["examples"].get("in_dictionary")
    ex_out = rep["examples"].get("out_of_dictionary")
    if ex_in is not None:
        a, b = ex_in
        blocks = [a[i * k : (i + 1) * k] for i in range(3)]
        print(f"  esempio IN-dizionario:   {blocks} · x ≤ {b}")
    if ex_out is not None:
        a, b = ex_out
        blocks = [a[i * k : (i + 1) * k] for i in range(3)]
        print(f"  esempio FUORI-dizionario: {blocks} · x ≤ {b}")


def main() -> None:
    print("=" * 78)
    print("CONO DEI MOMENTI DI KRONECKER — inner approximation ESATTA P_D + caccia ai buchi")
    print("=" * 78)
    show_holes(5, 5)
    print()
    show_holes(6, 6)
    show_facets(3)
    print(
        "\nNB onestà: P_D è un'inner approximation a scala FISSA (non il cono).  Le faccette "
        "fuori-dizionario\nsono fuori dal dizionario ELEMENTARE {nonneg, ordering}; Klyachko/"
        "Horn per Kronecker non è\nnoto in forma chiusa e NON è codificato.  Nessun claim su "
        "saturation o P vs NP."
    )


if __name__ == "__main__":
    main()
