# Module 26 — Iso-Hardness Control: survival is H-robust, leverage is genuinely absent

**Verdict: PASS — cross-level SURVIVAL is H-ROBUST, and the Module-25 H-confound is
FALSIFIED; there is still NO growing leverage.** Holding the hard-fraction `H` ~ fixed
across n=4 (exact), n=5, n=6 (sampled), the order-anisotropy of `MBPSP[s]` stays
overwhelmingly significant at every level with the control flat — so [Module
25](cross-level-median.md)'s survival is not an artifact of `H` drifting. And at fixed
`H` the relative effect `rel` still **peaks at n=5**, so the "rel tracks H" objection is
itself disproven — but the peak is **bounded and non-monotone**, i.e. there is no
growing leverage hiding behind the H-drift. The "no leverage" ceiling is now *cleaner*,
not lifted. No P vs NP claim.

## Why this module exists

[Module 25](cross-level-median.md) pushed the order-anisotropy survival to n=6 by
recalibrating the threshold to the **median** OBDD size. Its own Adversary left one open
objection: the integer-median policy does **not** hold the hard-fraction fixed
(`H = 0.17 / 0.25 / 0.44` at n=4,5,6), and the relative anisotropy `rel` could be
tracking `H` rather than the level `n`. If so, *both* readings of Module 25 were at
risk:

* the **survival** could be an H-artifact (the signal might vanish at a common `H`), and
* the **"no leverage"** verdict could be hiding leverage that the H-drift happens to
  cancel.

This module runs the control that settles it.

## The control: hold H fixed instead of the median

Re-pick the threshold as the **(1−H_target) quantile** of the OBDD-size distribution
(`iso_hardness_threshold`: exact full sweep at n≤4, sampled at n≥5), so `H ≈ H_target`
at every level. Integer thresholds cannot hit `H_target` exactly — OBDD sizes are coarse
(at n=4 `frac>s` jumps `0.526 → 0.170` between s=9 and s=10) — but the achievable `H`
lands **far tighter** than the median policy: for `H_target=0.5` the rows are
`H ≈ 0.53 / 0.55 / 0.44` versus the median policy's `0.17 / 0.25 / 0.44`.

To regress out the residual H-drift we run **two matched-H slices** (`H_target` 0.5 and
0.2). The within-level H-sensitivity of `rel` is modest — at n=4 (exact) `rel` moves
`+2.9% → +7.3%` as `H` goes `0.93 → 0.17` — and is small compared to the cross-level
effect we test. Everything else is unchanged from Module 24/25: the CRN estimator, the
pre-registered pair (top variable `x_{n-1}` vs `x0`), the popcount null control,
multi-seed pooling.

**Pre-declared killer.** At fixed `H`, if the signal **loses** significance at n=5 or
n=6 (99% CI includes 0), the killer fires — Module 25's survival was an H-artifact. PASS
if the signal stays significant at every level with the control flat. Then, *separately*
and descriptively (not pass/fail): does `rel` **grow** with `n` at fixed `H` (the
magnification prize) or stay **non-monotone/bounded** (survival without leverage)?

## Measured (frozen; n=4 exact, n=5,6 sampled CRN, pooled over 6 seeds)

| H_target | n | s | H_ach | base_prob | diff_prob | z | rel = diff/base | control_z | signs |
|----------|---|---|-------|-----------|-----------|---|-----------------|-----------|-------|
| **0.5** | 4\* | 9 | 0.526 | 0.559 | +3.08e-2 | *exact* | **+5.5%** | 0 (exact) | — |
|         | 5 | 15 | 0.548 | 0.394 | +4.20e-2 | **+68.8** | **+10.7%** | flat (−0.51) | 6/6 |
|         | 6 | 26 | 0.435 | 0.282 | +2.15e-2 | **+40.5** | **+7.6%** | flat (+1.04) | 6/6 |
| **0.2** | 4\* | 10 | 0.170 | 0.321 | +2.34e-2 | *exact* | **+7.3%** | 0 (exact) | — |
|         | 5 | 16 | 0.246 | 0.299 | +3.41e-2 | **+63.0** | **+11.4%** | flat (−0.51) | 6/6 |
|         | 6 | 27 | 0.194 | 0.200 | +1.19e-2 | **+26.4** | **+6.0%** | flat (+1.04) | 6/6 |

\* n=4 is the exact full sweep (ground truth); the popcount control is exactly 0 by
permutation symmetry. The `H_target=0.2` n=4 row coincides with Module 25's n=4 (same
threshold s=10, diff 1536).

## What it shows

1. **Survival is H-robust (killer does not fire).** At *both* fixed-H slices the
   pre-registered pair is hugely significant at every level (`z` = 68.8/40.5 and
   63.0/26.4), all seeds positive, with the popcount null control flat throughout. So
   Module 25's survival is **not** a side effect of `H` drifting upward — it persists at
   a common `H`.

2. **The H-confound is falsified.** Holding `H` fixed, `rel` still **peaks at n=5**
   (`5.5 → 10.7 → 7.6 %` at H≈0.5; `7.3 → 11.4 → 6.0 %` at H≈0.2). The shape is the same
   one Module 25 saw under the drifting-H median policy (`7.3 → 11.8 → 7.3 %`). So the
   `n=5` peak is a property of the **level**, not of `H` — the "rel tracks H" reading is
   wrong.

3. **No leverage, now for a cleaner reason.** The peak is **bounded and non-monotone**
   at every fixed `H`. Magnification needs a *growing* leverage across levels; here it
   rises then falls. The H-confound could in principle have hidden a real growth — this
   control rules that out. The ceiling stands as a *genuine bounded curve*, not a
   confound.

## The ceiling

* **Still survival, not leverage.** The point of the cycle was to test whether the
  absence of leverage was a confound. It is not: leverage is genuinely absent at fixed
  `H`.
* **Three levels, n=4 exact vs n≥5 sampled.** As in Modules 24/25 the comparison mixes
  one exact level with two sampled ones, and rests on three points — too few to assert a
  true asymptotic shape (only that there is no monotone growth across these three).
* The asymptotic amplification (small LB → separation) remains **CITED**
  (Oliveira–Pich; Chen–Jin–Williams; Chen–Hirahara–Ren–Santhanam–Vyas), never computed.

## Honesty boundary

ESTIMATED, not computed: the n=5 and n=6 differences (Monte Carlo, CRN, pooled over
seeds). COMPUTED exactly: both n=4 rows (full sweep), the popcount control's exact-0
difference, `min_obdd_size` (O(N) per table, also at n=6 on 64-bit tables), the
iso-hardness thresholds at n=4. ITERATED, stated: integer thresholds cannot hit
`H_target` exactly (OBDD sizes are coarse), so `H` is held *near* the target, not
exactly; two slices plus the small within-level H-sensitivity bound the residual.
NOT shown: any *growing* cross-level leverage — it is bounded and non-monotone at fixed
`H`. CITED, never computed: the magnification / locality theorems. No separation, no P
vs NP claim — this is the control that hardens Module 25's survival and removes the
H-confound from its "no leverage" verdict.

Files: `pnp_lab/meta_complexity/sampled_order_n5.py` (the `iso_hardness_*` section),
`tests/test_sampled_order_n5.py`, `examples/run_iso_hardness.py`.
