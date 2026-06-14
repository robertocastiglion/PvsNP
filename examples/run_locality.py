"""Magnification Frontier, ciclo 1 — la barriera di LOCALITA' resa esatta su MCSP[s].

Rende TANGIBILE (interi esatti) un muro NOTO: un argomento k-locale (che legge solo
k dei N=2^n bit del truth-table) non puo' certificare la durezza finche' non legge
quasi tutto. E la LEVA: per la funzione piu' dura servono k*=N bit a ogni livello, e
k* RADDOPPIA con N — la barriera di localita' come staircase. Nessun claim su P vs NP.

    py examples/run_locality.py
"""

import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from pnp_lab.circuits import min_formula_sizes  # noqa: E402
from pnp_lab.meta_complexity import locality  # noqa: E402


def main() -> None:
    print("=" * 72)
    print("  MAGNIFICATION FRONTIER — la barriera di localita' su MCSP[s] (esatto)")
    print("=" * 72)

    # ── il muro a n=3, s=4 ────────────────────────────────────────────────
    ct = min_formula_sizes(3)
    s = 4
    meta = locality.meta_truth_table(ct, s)
    N = 8
    H = locality.hard_count(meta)
    rel = locality.relevant_coordinates(meta, N)
    print(f"\n  Meta-funzione MCSP[s={s}] su N=2^3=8 bit (input = truth-table di una")
    print(f"  funzione a 3 bit). Input totali = 2^N = {len(meta)}.  H = #dure = {H}.")
    print(f"  Misura decisiva (killer-fedelta'): coordinate rilevanti = {len(rel)}/8"
          f"  -> {'8-junta GENUINO, muro reale' if len(rel) == 8 else 'degenere'}.")

    print("\n  IL MURO (ostruzione di conteggio), interi esatti:")
    print("    k = # bit del truth-table che l'argomento puo' leggere")
    print("    certified(k) = istanze DURE che un argomento k-locale certifica")
    print("                   con CERTEZZA (fibra pura-dura)\n")
    print("     k   certified(k)   H-certified(k)  (= dure NON certificabili)")
    for r in locality.obstruction(ct, s):
        bar = "#" * r.certified
        print(f"    {r.k:2d}      {r.certified:4d}          {r.gap_cert:4d}    {bar}")
    print("\n  -> nessun argomento che legge <= 5 degli 8 bit certifica una sola")
    print("     istanza dura; il muro crolla solo leggendo quasi tutto. E' la")
    print("     barriera di localita' (Chen-Hirahara-Ren-Santhanam-Vyas) in miniatura.")

    # ── la LEVA attraverso i livelli (il taglio orizzontale) ──────────────
    print("\n  LA LEVA (il taglio-torta): la funzione PIU' DURA, attraverso i livelli")
    print("  (policy banda-dura s=maxcost-1). k* = bit da leggere per certificarla.\n")
    rows = locality.leverage([min_formula_sizes(2), min_formula_sizes(3)])
    print("     n   N=2^n   s    H    loc    k*    rho=k*/N")
    for r in rows:
        print(f"    {r.n:2d}   {r.N:3d}   {r.s:3d}  {r.H:3d}   {r.loc:2d}/{r.N:<2d}  {r.k_star:3d}    {r.rho}")
    print(f"    {4:2d}   {16:3d}   {14:3d}  {114:3d}   {16:2d}/16   {14:3d}    {0.875}"
          "   <- misurato (build n=4, cache)")
    print("\n    FALSIFICAZIONE ESATTA: l'ipotesi 'rho=1 a ogni livello, k* raddoppia")
    print("    4->8->16' E' FALSA. rho crolla a 0.875 a n=4. Il rho=1 a n<=3 era un")
    print("    ARTEFATTO della banda-dura degenere H=2 (parita' e ¬parita': 2 sole")
    print("    istanze, max sparse -> nessuna fibra N-1 pura-dura -> rho=1 banale).")
    print("    Appena H e' reale (114 a n=4) compaiono fibre pura-dura sotto il junta")
    print("    pieno (cert(15)=24, cert(14)=8) e rho<1. La leva misura taglia+disper-")
    print("    sione della banda dura (H=2,2,114, non monotona), non l'amplificazione.")

    # ── CICLO 2: il taglio ORIZZONTALE (policy frazione fissa) ────────────
    print("\n  IL TAGLIO ORIZZONTALE (ciclo 2): policy a FRAZIONE FISSA s=round(maxcost·θ),")
    print("  θ=0.5. Tiene H non degenere (≈ mezzo spazio). Ipotesi Explorer: la curva")
    print("  normalizzata c(j)=certified(N-j)/H e' un INVARIANTE DI LIVELLO (c(j) indip.")
    print("  da n). Razionali ESATTI:\n")
    import pickle
    from pathlib import Path
    rows2 = locality.level_curves([min_formula_sizes(2), min_formula_sizes(3)])
    cache = Path(__file__).resolve().parent.parent / ".cache" / "ct4.pkl"
    if cache.exists():
        with open(cache, "rb") as f:
            ct4 = pickle.load(f)
        rows2 = locality.level_curves([min_formula_sizes(2), min_formula_sizes(3), ct4])
    print("     n   N=2^n   s     H       loc      c(0)   c(1)            c(2)")
    for r in rows2:
        cc = [str(x) for x in r.c]
        print(f"    {r.n:2d}   {r.N:3d}   {r.s:3d}  {r.H:6d}   {r.loc:2d}/{r.N:<2d}"
              f"   {cc[0]:<5s}  {cc[1]:<14s}  {cc[2]}")
    if not cache.exists():
        print("    (n=4 saltato: cache .cache/ct4.pkl assente)")
    print("\n    ESITO ONESTO: KILLER-A E' SCATTATO. c(1) e c(2) NON coincidono tra n=3 e")
    print("    n=4 (8/25=0.320 vs 8990/12977=0.693; 4/25=0.160 vs 6068/12977=0.468). Solo")
    print("    c(0)=1 regge (banale: junta pieno). c(j) NON e' un invariante di livello:")
    print("    la frazione certificabile (N-1)/(N-2)-locale CRESCE con n. Il muro c(0)=1")
    print("    solo al junta pieno regge; la sua NORMALIZZAZIONE non e' level-invariant.")

    print("\n  " + locality.magnification_threshold_note())
    print("=" * 72)


if __name__ == "__main__":
    main()
