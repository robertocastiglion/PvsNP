# Module 25 — Cross-Level Survival under Median Calibration (push to n=6)

**Verdict: PASS — cross-level SURVIVAL on three levels, NOT cross-level leverage
growth.** The order-anisotropy of `MBPSP[s]` survives across n=4 (exact), n=5 and
**n=6** (sampled, `N = 64`, `2^64` truth tables — only samplable), overwhelmingly and
control-validated at every level. This is the strongest cross-level result in the lab
— but the *leverage* (what magnification needs) does **not** grow, the object is
**recalibrated** from [Module 24](sampled-order-n5.md)'s faithful one, and the trend
is confounded by a varying hard-fraction. No P vs NP claim.

## Why this module exists

[Module 24](sampled-order-n5.md) established that the sampling pivot reaches **exactly
n=5** under Module 22's *faithful* threshold policy (`s = round(0.5·max)`), because at
n≥6 random OBDD sizes concentrate near the maximum, the meta-function becomes
constant-HARD, and the pair-influence the estimator reads → 0. To push deeper we must
**reopen the boundary**.

## The recalibration (and its honest price)

Set the threshold to the **median** OBDD size (`median_threshold`: exact full sweep at
n≤4, sampled at n≥5). This keeps the meta-function non-trivial at every level
(`H ≈ 0.17–0.44`), so the 4-cubes straddle `s` and the pair-influence is large. **The
price is named explicitly: this is a DIFFERENT object** from Module 22's faithful wall
— a recalibrated threshold, not the same one. The cross-level comparison is therefore
between *median-calibrated* meta-functions, not the faithful magnification object.

Everything else is unchanged from Module 24: the CRN estimator, the pre-registered
pair (top variable `x_{n-1}` vs `x0`), the popcount null control, multi-seed pooling.

## Measured (median policy; n=4 exact, n=5/6 sampled CRN, frozen)

| n | s | H_frac | base_prob | diff_prob | z | rel = diff/base | control | signs |
|---|---|--------|-----------|-----------|---|-----------------|---------|-------|
| 4\* | 10 | 0.170 | 0.321 | +2.34e-2 | *exact* | **+7.3%** | 0 (exact) | — |
| 5 | 16 | 0.246 | 0.300 | +3.53e-2 | **+73** | **+11.8%** | flat (z=−0.95) | 6/6 |
| 6 | 26 | 0.435 | 0.282 | +2.05e-2 | **+43** | **+7.3%** | flat (z=−0.24) | 6/6 |

\* n=4 is the exact full sweep (ground truth); the popcount control is exactly 0 by
permutation symmetry.

The order-anisotropy **survives all three levels**: at n=5 and n=6 the pre-registered
pair is significant by a wide margin (z = 73, 43), **all seeds positive**, and the
popcount null control is flat at *every* level — so the signal is order-specific, not
an artifact of the calibration.

## The ceiling — survival, not leverage

Three honest limits bound the claim:

1. **Recalibrated object.** Reaching n=6 required changing the threshold from Module
   22's faithful `0.5·max` to the median. The result is about a *related but
   recalibrated* meta-function, not the faithful magnification wall.
2. **Leverage does not grow.** The relative effect is `7.3% → 11.8% → 7.3%` —
   **non-monotone and bounded**, not increasing. Magnification needs a *growing*
   leverage across levels; a bounded, oscillating one is neutral.
3. **H confound.** The integer-median policy does **not** hold the hard-fraction fixed
   (`H = 0.17, 0.25, 0.44`), and the relative effect tracks `H` (peaking at n=5 where
   `H ≈ 0.25`). So the apparent rel-stability must not be over-read as a clean
   level-invariant. The flat control at every `H` defends the *survival* claim, not a
   leverage-trend claim.

So this module **strengthens cross-level SURVIVAL** (one level in Module 24 → three
levels here) but does **not** demonstrate cross-level **leverage growth**. The
asymptotic amplification (small LB → separation) remains CITED (Oliveira–Pich;
Chen–Jin–Williams; Chen–Hirahara–Ren–Santhanam–Vyas), never computed. Same "the lab
reaches deeper than exact methods but the amplification escapes" pattern — now three
levels deep.

## Honesty boundary

ESTIMATED, not computed: the n=5 and n=6 differences (Monte Carlo, CRN, pooled over
seeds). COMPUTED exactly: the full n=4 row (sweep), the popcount control's exact-0
difference, `min_obdd_size` (O(N) per table, also at n=6 on 64-bit tables). RECALIBRATED
(stated): the median threshold differs from Module 22's faithful policy. NOT shown: any
*growing* cross-level leverage; the trend is bounded and H-confounded. CITED, never
computed: the magnification / locality theorems. No separation, no P vs NP claim — this
shows one order-anisotropy survives three levels under a recalibrated object, with no
amplification.

Files: `pnp_lab/meta_complexity/sampled_order_n5.py` (the `cross_level_*` section),
`tests/test_sampled_order_n5.py`, `examples/run_cross_level_median.py`.
