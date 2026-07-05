"""Demo: caccia agli zeri di Kronecker fuori dizionario a d=4..9 (Ciclo 1 "la caccia").

Calcola hunt(d) per d=4..9, stampa la tabella classificata e l'elenco degli uncovered
con il loro stretch-bit (HOLE/RAY) a N=2.  Per d>=7 marca i passi lenti.

Esegui:  py examples/run_beyond_wall.py
         (d=6 ~30 sec; d=7 ~30 sec; d=8 ~2 min; d=9 ~5 min)
"""

import sys
import time
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from pnp_lab.gct_kronecker.beyond_wall import (  # noqa: E402
    hunt,
    sanity_entry30,
    stretch_witnesses,
    honesty_note,
    HuntResult,
)


def _fmt_time(sec: float) -> str:
    if sec < 60:
        return f"{sec:.1f}s"
    return f"{sec/60:.1f}min"


def run_table(d_range=range(4, 10)) -> dict:
    """Calcola hunt(d) per tutti i gradi nel range e ritorna i risultati."""
    results = {}
    print("=" * 90)
    print("KRONECKER BEYOND THE WALL — classificazione vanishing g=0")
    print("NC estese: nc_length, nc_maxpart, nc_dvir_full (Dvir 1993), nc_triangle (Klyachko 2004)")
    print("=" * 90)
    print()
    print(
        f"{'d':>3}  {'#zero':>7}  {'#expl':>7}  {'#spor(new)':>10}  "
        f"{'#cov':>6}  {'#uncov':>7}  {'#spor(old)':>10}  "
        f"{'sanity':>8}  {'tempo':>7}"
    )
    print("-" * 90)

    for d in d_range:
        t0 = time.time()
        r = hunt(d)
        elapsed = time.time() - t0

        ok, expected = sanity_entry30(r)
        sanity_str = "OK" if ok else f"DIFF(exp={expected})"

        print(
            f"{d:>3}  {r.n_zeros:>7}  {r.n_explained:>7}  {r.n_sporadic:>10}  "
            f"{r.n_covered_ext:>6}  {r.n_uncovered:>7}  {r.n_sporadic_old:>10}  "
            f"{sanity_str:>8}  {_fmt_time(elapsed):>7}"
        )
        results[d] = r

    print("-" * 90)
    print("Legenda: #zero=totale g=0 | #expl=spiegati da NC | #spor(new)=sporadici NC estese")
    print("         #cov=covered_ext | #uncov=uncoperti (g-orbit dedup) | #spor(old)=Entry30")
    return results


def show_uncovered(results: dict, d_range=range(4, 10)) -> None:
    """Stampa i testimoni uncovered per ogni d."""
    print()
    print("=" * 90)
    print("TESTIMONI UNCOVERED (rappresentanti canonici per orbita g-simmetrica)")
    print("=" * 90)

    any_uncov = False
    for d in d_range:
        r = results.get(d)
        if r is None or r.n_uncovered == 0:
            print(f"\nd={d}: nessun uncovered (n_uncovered=0)")
            continue
        any_uncov = True
        print(f"\nd={d}: {r.n_uncovered} uncovered")
        for i, t in enumerate(r.uncovered_canon[:10]):
            lam, mu, nu = t
            print(f"  [{i+1}] lam={lam}, mu={mu}, nu={nu}")

    if not any_uncov:
        print("\nNessun uncovered in nessun d — RESTATEMENT (collasso del dizionario esteso).")


def show_stretch(results: dict, d_max_stretch: int = 8) -> None:
    """Calcola e stampa il bit HOLE/RAY per gli uncovered a d<=d_max_stretch."""
    print()
    print("=" * 90)
    print(f"STRETCH N=2 degli uncovered (d<={d_max_stretch}; 2d=16 => p(16)=231)")
    print("HOLE = g(2*triple) > 0 (buco interno); RAY = g(2*triple) = 0 (annullamento persistente)")
    print("=" * 90)

    for d in range(4, d_max_stretch + 1):
        r = results.get(d)
        if r is None or r.n_uncovered == 0:
            continue
        print(f"\nd={d}: calcolo stretch per {r.n_uncovered} testimoni...")
        t0 = time.time()
        try:
            ws = stretch_witnesses(r.uncovered_canon, n_max=2)
            elapsed = time.time() - t0
            print(f"  (completato in {_fmt_time(elapsed)})")
            for w in ws:
                t = w["triple"]
                g2 = w["stretch"][2]
                bit = "HOLE" if w["hole"] else "RAY"
                print(f"  {t} => g(2*)={g2} [{bit}]")
        except Exception as exc:
            print(f"  ERRORE/TIMEOUT: {exc}")


def main() -> None:
    # Tabella principale d=4..9
    results = run_table(range(4, 10))

    # Testimoni uncovered
    show_uncovered(results, range(4, 10))

    # Stretch per d<=8 (2d<=16; d=9 -> 2d=18 puo' essere > 10 min)
    # Mostriamo solo se ci sono uncovered
    has_uncov = any(r.n_uncovered > 0 for r in results.values() if r is not None)
    if has_uncov:
        show_stretch(results, d_max_stretch=8)
    else:
        print()
        print("Nessun uncovered trovato: stretch non necessario.")

    # Confine di onesta'
    print()
    print("=" * 90)
    print("CONFINE DI ONESTA'")
    print("=" * 90)
    print(honesty_note())
    print()
    print("Definizione ESATTA dell'orbita usata per canonicalizzare gli uncovered:")
    print("  G = S_3 (permutazioni) x V_4 (coniugio simultaneo di due qualsiasi)")
    print("  Canonico = minimo lessicografico su tuple(lam, mu, nu) nell'orbita.")
    print()
    print("Famiglie NOT implementate nel covered_ext (survival-by-omission dichiarato):")
    print("  B5: multiplicity-free (Bessenrodt-Bowman 2017, arXiv:1609.03596)")
    print("  B6: two-column/hook (Pak-Panova e coautori)")


if __name__ == "__main__":
    main()
