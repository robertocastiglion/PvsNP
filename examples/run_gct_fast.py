"""Benchmark: character_table(d) e census(d) per d=7,8,9.

Misura il tempo REALE (perf_counter) di:
  (i)  character_table(d)  — calcola la tavola dei caratteri completa
  (ii) census(d)           — enumera tutte le terne non ordinate e conta gli zeri

Stima aritmetica per d=10 basata sul profiling di d=9.
Dimostra che il "muro brute-force d>=7" e' un artefatto implementativo:
con la tavola precalcolata, d=7/8/9 sono trivialmente enumerabili.
"""

import sys
import time
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from math import factorial
from pnp_lab.gct_kronecker.fast import character_table, g_fast, census, _CT_CACHE
from pnp_lab.gct_kronecker.kronecker import partitions, _triples


def p_count(d: int) -> int:
    """Numero di partizioni di d."""
    return len(partitions(d))


def triple_count(d: int) -> int:
    """Numero di terne non ordinate (lam<=mu<=nu) di partizioni di d."""
    n = p_count(d)
    return n * (n + 1) * (n + 2) // 6


def fmt_time(seconds: float) -> str:
    if seconds < 0.001:
        return f"{seconds*1000:.2f} ms"
    if seconds < 1.0:
        return f"{seconds*1000:.1f} ms"
    if seconds < 60.0:
        return f"{seconds:.2f} s"
    return f"{seconds/60:.1f} min"


print("=" * 70)
print("BENCHMARK: Kronecker via tavola dei caratteri precalcolata")
print("Ipotesi: il muro d>=7 e' un artefatto implementativo")
print("=" * 70)
print()

header = f"{'d':>3}  {'p(d)':>5}  {'#terne':>8}  {'t_tavola':>12}  {'t_census':>12}  {'#zeri':>7}"
print(header)
print("-" * len(header))

CENSUS_TIMEOUT_SECS = 1800  # 30 minuti

results = {}

for d in [7, 8, 9]:
    n_parts = p_count(d)
    n_triples = triple_count(d)

    # (i) character_table(d)
    # Svuota la cache per misurare il tempo reale (primo calcolo)
    if d in _CT_CACHE:
        del _CT_CACHE[d]

    t0 = time.perf_counter()
    ct = character_table(d)
    t_table = time.perf_counter() - t0

    # (ii) census(d)
    t1 = time.perf_counter()
    n_tot, n_zeros, _ = census(d)
    t_census = time.perf_counter() - t1

    results[d] = {
        "n_parts": n_parts,
        "n_triples": n_triples,
        "t_table": t_table,
        "t_census": t_census,
        "n_zeros": n_zeros,
    }

    print(
        f"{d:>3}  {n_parts:>5}  {n_triples:>8}  "
        f"{fmt_time(t_table):>12}  {fmt_time(t_census):>12}  {n_zeros:>7}"
    )

print()
print("Legenda: t_tavola = character_table(d), t_census = census(d)")

# ---------------------------------------------------------------------------
# Stima aritmetica per d=10
# ---------------------------------------------------------------------------
print()
print("-" * 70)
print("Stima aritmetica per d=10 (NON eseguita)")
print("-" * 70)

d9 = results.get(9)
if d9 is not None:
    n9 = d9["n_parts"]
    n10 = p_count(10)
    nt9 = d9["n_triples"]
    nt10 = triple_count(10)
    tc9 = d9["t_census"]

    # La tavola d=10 ha n10^2 voci vs n9^2 di d=9
    t_table_est = (results[9]["t_table"] * (n10 ** 2) / (n9 ** 2))

    # census: tempo proporzionale a n_triples * n_classes
    # (ogni g_fast fa un dot product di lunghezza n_classes)
    # stima = t_census(9) * (nt10 * n10) / (nt9 * n9)
    t_census_est = tc9 * (nt10 * n10) / (nt9 * n9)

    print(f"  d=10: p(10)={n10}, #terne={nt10}, tavola={n10}x{n10}={n10**2} voci")
    print(f"  Stima t_tavola  : {fmt_time(t_table_est)}")
    print(f"  Stima t_census  : {fmt_time(t_census_est)}")
    print(f"  (proporzione da d=9: tavola*{(n10/n9)**2:.2f}x, census*{(nt10*n10)/(nt9*n9):.2f}x)")

# ---------------------------------------------------------------------------
# Sommario: dove si trova il VERO muro
# ---------------------------------------------------------------------------
print()
print("-" * 70)
print("Sommario: muro REALE vs muro ARTEFATTO")
print("-" * 70)
print("Muro artefatto (implementazione vecchia): d>=7 sembrava impraticabile")
print("Muro reale (con character_table precalcolata): vedi dove t_census esplode")
print()

# Stima dei punti di rottura su d=10..20
print(f"  {'d':>3}  {'p(d)':>5}  {'#terne':>10}  {'stima t_census':>16}")
print(f"  {'-'*3}  {'-'*5}  {'-'*10}  {'-'*16}")

if d9 is not None:
    for d_est in range(10, 21):
        nd = p_count(d_est)
        nt = triple_count(d_est)
        # Estrapolazione: t ~ nt * nd * (cost_per_term)
        cost_per_term = tc9 / (d9["n_triples"] * d9["n_parts"])
        t_est = nt * nd * cost_per_term
        marker = " <-- ~1 min" if 55 < t_est < 75 else (
                 " <-- ~1 ora" if 3500 < t_est < 4500 else (
                 " <-- MURO REALE (~1 giorno)" if t_est > 80000 else ""))
        print(f"  {d_est:>3}  {nd:>5}  {nt:>10}  {fmt_time(t_est):>16}{marker}")

print()
print("Rigenera con: py examples/run_gct_fast.py")
