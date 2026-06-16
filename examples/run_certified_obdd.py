"""Certified-bounds regime, Cycle 1 — famiglia OBDD esplicita con order gap PROVATO
da una ricorrenza CERTIFICATA (niente enumerazione), e il SOFFITTO strutturale del regime.

Stampa: la ricorrenza di taglia certificata vs l'esatto (anchor di fedelta'), il gap
d'ordine g(n) = istanza finita esatta del bound CITATO di Bryant — RESTATEMENT #12; e il
finding reale del ciclo (perche' un invariante di MURO reintroduce lo sweep).  L'evidenza-
muro del primo draft (A(n), r(n), discriminatore) e' STRUCK: category error (vedi modulo).
Esatto, niente float.  Nessun claim su P vs NP.

    py examples/run_certified_obdd.py
"""

import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from pnp_lab.meta_complexity import certified_obdd as co  # noqa: E402
from pnp_lab.meta_complexity import order_locality as ol   # noqa: E402


def main() -> None:
    print("=" * 76)
    print("  CERTIFIED-BOUNDS REGIME — Cycle 1: famiglia OR-AND, order gap CERTIFICATO")
    print("=" * 76)

    # ── la famiglia e i due ordini ────────────────────────────────────────
    print("\n  OGGETTO  f_n(x) = OR_{k} ( x_{2k} AND x_{2k+1} )   (Module-22 founding)")
    print("    ordine BUONO  π  = identità            (coppie adiacenti)")
    print("    ordine CATTIVO π' = interlacciato [0,2,…,n-2, 1,3,…,n-1]")

    # ── ricorrenza certificata vs esatto (anchor di fedeltà) ──────────────
    print("\n  RICORRENZA CERTIFICATA vs min_obdd_size ESATTO (anchor di fedeltà):")
    print("     n   size_good (cert / esatto)   size_bad (cert / esatto)")
    for n in (2, 4, 6, 8):
        t = co.family_or_and(n)
        eg = ol.min_obdd_size(co.permute_vars(t, n, co.good_perm(n)), n)
        eb = ol.min_obdd_size(co.permute_vars(t, n, co.bad_perm(n)), n)
        ok = "OK" if (eg, eb) == (co.size_good(n), co.size_bad(n)) else "MISMATCH"
        print(f"    {n:2d}    {co.size_good(n):2d}  /  {eg:2d}                 "
              f"{co.size_bad(n):3d}  /  {eb:3d}        [{ok}]")
    print("    ricorrenza: size_good = n+2 = 4,6,8,10  ·  size_bad = 2^(n/2+1) = 4,8,16,32")
    print("    prova fondante: 6 ≠ 8 a n=4 (lo stesso testimone di Module 22).")

    # ── il gap certificato = Bryant ristretto ─────────────────────────────
    rows = co.measure([2, 4, 6, 8])
    print("\n  IL GAP CERTIFICATO  g(n) = size_bad − size_good  (l'UNICA evidenza valida):")
    print("     n   size_good  size_bad   g(n)")
    for r in rows:
        print(f"    {r.n:2d}     {r.size_good:3d}      {r.size_bad:3d}     {r.gap:3d}")
    print("\n    g(n) = 2^(n/2+1) − (n+2) = 0,2,8,22 — istanza FINITA ESATTA del bound")
    print("    asintotico CITATO (Bryant 1991 / Wegener, gap OBDD 2^Ω(n)).  Il regime")
    print("    certified-bounds RESTATES Bryant: RESTATEMENT #12 (collasso-su-noto).")

    # ── l'evidenza-muro STRUCK (category error) ───────────────────────────
    print("\n  EVIDENZA-MURO del primo draft: STRUCK (NON citare).")
    print("    Tentava A(n) = spread del muro FEDELE certified_drop_spread su tt_π', ma")
    print("    quel muro è una statistica della META-funzione MBPSP[s] sull'INSIEME di")
    print("    tutte le 2^N funzioni — gli era data UNA singola funzione (arg N-vs-n: la")
    print("    chiamata fedele solleva IndexError). Category error: Adversary+Evaluator KILL.")

    # ── il finding reale: il soffitto del regime ──────────────────────────
    print("\n  IL FINDING REALE — il soffitto proprio del regime certified-bounds:")
    print("  " + co.ceiling_note())
    print("=" * 76)


if __name__ == "__main__":
    main()
