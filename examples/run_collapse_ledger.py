"""Demo: ledger dei 21 collassi del PvsNP-lab (Entry 37).

Misura C(21), la curva cumulativa, la stima Good-Turing e i killer.

Eseguire:
    py examples/run_collapse_ledger.py
"""

import sys
sys.stdout.reconfigure(encoding="utf-8")

from pnp_lab.attractor_theorem.collapse_ledger import summary

s = summary()

recs      = s["records"]
curve     = s["curve"]
gt        = s["good_turing"]
stab      = s["stability"]
tc        = s["type_counts"]
killers   = s["killers"]
hyp       = s["hypothesis_H"]

# ── intestazione ──────────────────────────────────────────────────────────────
print("=" * 60)
print("Collapse Ledger — Entry 37 PvsNP-lab")
print("=" * 60)

# ── onestà di estrazione ──────────────────────────────────────────────────────
print(f"\nRecord estratti : {s['n_records']} / 21")
print(f"  literal       : {s['n_literal']}  (RESTATEMENT #N esplicito nel log)")
print(f"  heuristic     : {s['n_heuristic']}  (conteggio collassi nel testo)")
print()
print("Note di estrazione:")
print("  #9  — 'RESTATEMENT #9' in Entry 12 (back-ref); record → Entry 11")
print("  #15 — 'RESTATEMENT #15' in Entry 29 (predizione); record → Entry 30")

# ── tabella tipo → conteggio ──────────────────────────────────────────────────
print("\nTipo → conteggio:")
all_types = ["CITED-THEOREM", "PERM-ABSORBED", "OMISSION",
             "SYMM-ARTIFACT", "CLOSED-FORM", "COND-IMPOSSIBLE"]
for t in all_types:
    n = tc.get(t, 0)
    bar = "#" * n
    print(f"  {t:<20s} {n:2d}  {bar}")

# ── curva cumulativa C(1..21) ─────────────────────────────────────────────────
print(f"\nC(1..21) = {curve}")
print(f"C(21) = {curve[-1]}")

# ── Good-Turing ───────────────────────────────────────────────────────────────
print(f"\nGood-Turing (n_boot=10000, seed=0):")
print(f"  n_singleton = {gt['n_singleton']}")
print(f"  P(tipo non visto) = {gt['unseen']:.4f}")
print(f"  CI 95%  = [{gt['ci_lo']:.4f}, {gt['ci_hi']:.4f}]")

# ── ambigui ───────────────────────────────────────────────────────────────────
print(f"\nRecord ambigui (≥2 regole co-applicabili): {s['n_ambiguous']}")
if s["ambiguous_list"]:
    print(f"  RESTATEMENT #{sorted(s['ambiguous_list'])} ")

# ── stability ─────────────────────────────────────────────────────────────────
print(f"\nStabilità:")
print(f"  C_coarse (2 super-tipi) = {stab['C_coarse']}")
print(f"  C_normal (6 regole)     = {stab['C_normal']}")
print(f"  C_fine   (21 unici)     = {stab['C_fine']}")
print(f"  range = [{stab['C_coarse']}, {stab['C_fine']}]")

# ── killer ────────────────────────────────────────────────────────────────────
print("\nKiller:")
for k, info in killers.items():
    fires = info["fires"]
    flag  = "FIRES" if fires else "ok"
    print(f"  {k:<20s} {flag}")
    if k == "K_narrativa":
        print(f"    ambigui = {info['value']} / soglia = {info['threshold']}")
    elif k == "K_small_sample":
        print(f"    C(21)={info['C_final']}, n_sing={info['n_singleton']}, "
              f"ci_lo={info['unseen_ci_lo']:.4f}")

# ── ipotesi H ─────────────────────────────────────────────────────────────────
print(f"\nIpotesi H: C(21) ≤ 6 AND GT upper ≤ 1")
print(f"  C(21) ≤ 6  → {'PASS' if hyp['C_passes'] else 'FAIL'}  (C={hyp['C_final']})")
print(f"  CI-hi ≤ 1  → {'PASS' if hyp['gt_passes'] else 'FAIL'}  "
      f"(CI-hi={hyp['gt_ci_hi']:.4f})")
print(f"  H: {hyp['note']}")
print("=" * 60)
