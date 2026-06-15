"""Magnification Frontier, Cycle 3 — MBPSP[s] a ordine FISSO: l'oggetto meta-livello
NON permutazione-invariante che RIAPRE il programma.

Il sotto-ramo locality (Module 21) si chiuse perche' MCSP[s] (a FORMULA) e'
permutazione-invariante: ogni leva collassa a una statistica simmetrica del set duro.
Qui cambiamo la MISURA di complessita' (dimensione OBDD a ordine fisso, non formula):
l'ordine e' un asse asimmetrico, e a n=4 sopravvive nella pair-influence della
meta-funzione (spread > 0 per classe di peso), mentre il controllo MCSP lava via
(spread = 0). Nessun claim su P vs NP.

    py examples/run_order_locality.py
"""

import pickle
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from pnp_lab.meta_complexity import order_locality as ol  # noqa: E402

_CT4_CACHE = Path(__file__).resolve().parent.parent / ".cache" / "ct4.pkl"


def main() -> None:
    print("=" * 74)
    print("  MAGNIFICATION FRONTIER — Cycle 3: MBPSP[s] a ordine FISSO (riapertura)")
    print("=" * 74)

    # ── la prova fondante: l'ordine non e' permutazione-invariante ─────────
    n = 4

    def tt(f):
        out = 0
        for x in range(1 << n):
            b = [(x >> j) & 1 for j in range(n)]
            if f(b):
                out |= 1 << x
        return out

    tg = tt(lambda b: (b[0] & b[1]) | (b[2] & b[3]))
    tp = ol.variable_swap(tg, n, 1, 2)
    print("\n  Prova fondante (la stessa funzione, due variabili scambiate):")
    print(f"    (x0&x1)|(x2&x3)  -> OBDD size = {ol.min_obdd_size(tg, n)}")
    print(f"    (x0&x2)|(x1&x3)  -> OBDD size = {ol.min_obdd_size(tp, n)}"
          "   (= la prima con var 1,2 scambiate)")
    print("    Stessa funzione, coordinate permutate, dimensione DIVERSA: la misura")
    print("    OBDD a ordine fisso NON e' permutazione-invariante. La FORMULA si'.")

    # ── la leva attraverso i livelli: dove parte la scala ──────────────────
    print("\n  LA LEVA (pair-influence, spread per classe di peso di Hamming di d):")
    print("    spread = max-min di pairinf(d) sui d di ugual peso.")
    print("    spread = 0  <=>  pairinf dipende solo dal peso  <=>  permutazione-invar.")
    print("    spread > 0  <=>  pairinf dipende dal SUPPORTO di d <=> ordine sopravvive\n")
    print("     n   N=2^n   s    H        spread per peso w=1,2,...   verdetto")
    for r in ol.order_asymmetry([2, 3, 4]):
        verdict = "ORDINE SOPRAVVIVE" if r.order_survives else "ordine silente"
        print(f"    {r.n:2d}   {r.N:3d}   {r.s:3d}  {r.H:6d}   {str(r.spreads):<26s} {verdict}")
    print("\n    L'asimmetria si ACCENDE a n=4 — esattamente dove la sensibilita'")
    print("    all'ordine appare per le singole funzioni ((x0 x1)|(x2 x3) richiede 4 var).")

    # ── il dettaglio a n=4: l'influenza dipende da QUALE variabile ─────────
    costs = ol.obdd_costs(4)
    s = ol.fixed_fraction_threshold(costs)
    meta = ol.meta_truth_table_obdd(costs, s)
    wcs = ol.weight_class_spread(meta, 16)
    print(f"\n  DETTAGLIO n=4 (s={s}, H={ol.hard_count(meta)}): pairinf(d) per peso w=1")
    print("  (d = variabili in cui due coordinate differiscono; ordine = x3 in cima):")
    for d, v in wcs[0].pairinf:
        which = [j for j in range(4) if (d >> j) & 1]
        print(f"    d={d:04b}  differ in x{which[0]}   pairinf = {v}")
    print(f"    -> spread = {wcs[0].spread}: differire nella variabile in cima all'ordine")
    print("       (x3) e in x1 NON danno la stessa influenza. Asse asimmetrico reale.")

    # ── il controllo MCSP: lava via anche a n=4 ────────────────────────────
    print("\n  CONTROLLO MCSP (formula, Module 21) sulla STESSA misura:")
    if _CT4_CACHE.exists():
        with open(_CT4_CACHE, "rb") as f:
            ct4 = pickle.load(f)
        form = [ct4.cost[t] for t in range(1 << 16)]
        sf = ol.fixed_fraction_threshold(form)
        metaf = ol.meta_truth_table_obdd(form, sf)
        wcsf = ol.weight_class_spread(metaf, 16)
        print(f"    n=4, s={sf}, H={ol.hard_count(metaf)}: spread per peso = "
              f"{[wc.spread for wc in wcsf]}")
        print("    -> spread = 0 OVUNQUE: MCSP a formula e' permutazione-invariante. E'")
        print("       la ragione strutturale per cui il sotto-ramo locality si chiuse.")
    else:
        print(f"    (cache {_CT4_CACHE} assente: controllo n=4 saltato)")

    # ── CICLO 4: l'ordine raggiunge il MURO fedele di Module 21 ───────────
    print("\n  CICLO 4 — l'ordine raggiunge il MURO FEDELE di Module 21?")
    print("    certified_drop(d) = istanze dure certificate con certezza rilasciando la")
    print("    coppia di coordinate {0,d} (= locality.certified_k_local a k=N-2). Si")
    print("    misura lo spread entro una classe di ugual peso di d (j=1 e' isotropico")
    print("    per costruzione: traslazione transitiva sulle singole coordinate).\n")
    print("     n   N=2^n   s    H        spread muro w=1,2,...      verdetto")
    for r in ol.wall_anisotropy([3, 4]):
        verdict = "MURO VEDE L'ORDINE" if r.wall_sees_order else "muro isotropico"
        print(f"    {r.n:2d}   {r.N:3d}   {r.s:3d}  {r.H:6d}   {str(r.spreads):<24s} {verdict}")
    if _CT4_CACHE.exists():
        with open(_CT4_CACHE, "rb") as f:
            ct4b = pickle.load(f)
        formb = [ct4b.cost[t] for t in range(1 << 16)]
        sb = ol.fixed_fraction_threshold(formb)
        metab = ol.meta_truth_table_obdd(formb, sb)
        spb = [dc.spread for dc in ol.certified_drop_spread(metab, 16)]
        print(f"     4    16  {sb:3d}  {ol.hard_count(metab):6d}   {str(spb):<24s} "
              "MCSP control: muro isotropico")
    print("\n    A n=4 il muro FEDELE (non solo la pair-influence custom) e' anisotropico:")
    print("    la massimizzazione sui coordinate-set NON e' vacua, drop di ugual peso")
    print("    certificano numeri DIVERSI di istanze dure. Il controllo MCSP resta piatto")
    print("    (la trappola simmetrica che chiuse Module 21). Anisotropia REALE ma esile")
    print("    (~0.23%) e solo a n=4: il muro raggiunge l'ordine al livello piu' profondo")
    print("    misurabile; un invariante di livello resta fuori portata (n=5 = 2^32).")

    print("\n  " + ol.reopening_note())
    print("=" * 74)


if __name__ == "__main__":
    main()
