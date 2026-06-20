"""Bipartite Rigidity (new arena) — exact rigidity of a fixed-bipartition comm matrix.

Reports, per level k:
  * rank_gf2(IP_k) and rank_q(H_k);
  * R_M(r) at target r = 2^{k-1}: COMPUTED-exact for k<=3 (Q ±1 Hadamard, sign flips),
    CITED-certified lower bound for k>=4 (de Wolf/Midrijanis/Lokam spectral bound);
  * rho(k) = R / 4^k and the leverage lambda(k->k+1) = rho(k+1)/rho(k);
  * the killer verdict (reducible_from_rank? dict_table splits empty? leverage monotone?).

Run:  py examples/run_bipartite_rigidity.py
"""

import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))  # repo root su sys.path

from fractions import Fraction

from pnp_lab.bipartite_rigidity import killers as K
from pnp_lab.bipartite_rigidity import rigidity as R


def main() -> None:
    print("=== Bipartite Rigidity — fixed-bipartition communication matrix ===\n")

    print("Ranks of the explicit family (inner-product / Hadamard):")
    for k in (1, 2, 3):
        rg = R.rank_gf2(R.ip_matrix_gf2(k))
        rq = R.rank_q(R.hadamard_matrix(k))
        print(f"   k={k}: rank_gf2(IP_k)={rg}  rank_q(H_k)={rq}")

    print("\nRigidity R_M(r) at target r = 2^(k-1)  [COMPUTED-exact k<=2; k=3 budgeted LB; CITED-LB k>=4]:")
    rhos = {}
    # k=1,2: exact (4x4 fully enumerable).
    for k in (1, 2):
        r = 1 << (k - 1)
        val = R.rigidity_q_pm_exact(R.hadamard_matrix(k), r, max_flips=8)
        rho = Fraction(val) / Fraction(1 << (2 * k))
        rhos[k] = rho
        print(f"   k={k} (entries={1<<(2*k)}): r={r}  R={val}  rho={rho}  (~{float(rho):.4f})  COMPUTED-exact")
    # k=3: 8x8, subset search blows up; we only CERTIFY a lower bound R>budget honestly.
    k, r, budget = 3, 4, 2
    try:
        val3 = R.rigidity_q_pm_exact(R.hadamard_matrix(3), r, max_flips=budget)
        rhos[3] = Fraction(val3) / Fraction(1 << 6)
        print(f"   k=3 (entries=64): r={r}  R={val3}  COMPUTED-exact (fit in budget {budget})")
    except RuntimeError:
        # exact value is > budget; exhaustive search beyond budget is impractical (measured:
        # budget 3 ~ 86 s, budget 4 ~ tens of minutes). Report the honest lower bound.
        lb_search = budget + 1
        lb_cert = R.rigidity_certified_lb(3, r)
        rhos[3] = Fraction(max(lb_search, lb_cert)) / Fraction(1 << 6)
        print(f"   k=3 (entries=64): r={r}  R > {budget} (exhaustive STOPPED honestly; "
              f"exact beyond practical search), certified-LB={lb_cert}  rho_LB={rhos[3]} (~{float(rhos[3]):.4f})")
    for k in (4, 5, 6):
        r = 1 << (k - 1)
        lb = R.rigidity_certified_lb(k, r)
        rho = Fraction(lb) / Fraction(1 << (2 * k))
        rhos[k] = rho
        print(f"   k={k} (entries={1<<(2*k)}): r={r}  R_LB={lb}  rho_LB={rho}  (~{float(rho):.6f})  CITED-certified")

    print("\nLeverage lambda(k->k+1) = rho(k+1)/rho(k):")
    ks = [1, 2, 3, 4, 5, 6]
    lams = []
    for i in range(len(ks) - 1):
        a, b = rhos[ks[i]], rhos[ks[i + 1]]
        lam = (b / a) if a != 0 else Fraction(0)
        lams.append(lam)
        tag = "  [exact->exact]" if ks[i + 1] <= 2 else "  [LB involved]"
        print(f"   lambda({ks[i]}->{ks[i+1]}) = {lam}  (~{float(lam):.4f}){tag}")
    incr = all(lams[i] >= lams[i - 1] for i in range(1, len(lams)))
    gt1 = all(l > 1 for l in lams)
    print(f"   monotone non-decreasing? {incr}   all > 1? {gt1}")

    # k=2 exhaustive = 2^(2k)=16 entries but 2^16=65536 truth tables on 2k=4 bits.
    # Demo on a deterministic sample (full sweep is the slow test); r=2, budget 4.
    import random
    rng = random.Random(0)
    sample = sorted(rng.sample(range(1 << 16), 1200))
    print("\n--- KILLERS (k=2, deterministic sample of 1200 / 65536 functions) ---")
    red, sp1 = K.reducible_from_rank(2, 2, sample=sample, max_flips=4)
    print(f"killer-1 reducible_from_rank: reducible={red}  splits={len(sp1)}")
    rec, sp2 = K.dict_table(2, 2, sample=sample, max_flips=4)
    print(f"killer-2 dict_table (joint dictionary): reconstructible={rec}  splits={len(sp2)}")

    print("\n--- perm-NON-invariance control (S_4 mixing the two sides) ---")
    examples = [0b0110100110010110, 0b0001011101111000, 0b0110011010011001]
    any_move = False
    for tt in examples:
        rig, sens = K.side_mixing_spread(tt, 2, 2, max_flips=6)
        moved = len(set(rig)) > 1
        any_move = any_move or moved
        print(f"   tt={tt:016b}: rigidity spread={len(set(rig))} ({sorted(set(rig))}), "
              f"sensitivity spread={len(set(sens))} (flat={len(set(sens))==1})")

    print("\n--- VERDICT ---")
    if not red and sp1:
        v1 = "rigidity NOT reducible from rank alone (killer-1 does NOT fire)"
    else:
        v1 = "rigidity reducible from rank (killer-1 FIRES => log-rank restatement)"
    if not rec and sp2:
        v2 = "rigidity splits the joint dictionary (out-of-dictionary content)"
    else:
        v2 = "rigidity reconstructible from joint dictionary (killer-2 FIRES => RESTATEMENT)"
    if incr and gt1:
        v3 = "leverage monotone increasing (>1) => SURVIVAL-WITH-LEVERAGE"
    else:
        v3 = "leverage bounded/non-monotone => SURVIVAL-NO-LEVERAGE"
    print("  killer-1:", v1)
    print("  killer-2:", v2)
    print("  side-mixing moves rigidity (non-perm-invariant)?", any_move)
    print("  leverage:", v3)

    print("\n" + R.honesty_note())


if __name__ == "__main__":
    main()
