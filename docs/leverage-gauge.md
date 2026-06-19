# Module 27 — Gauge-Invariance of the Leverage Trend: "no leverage" is not a normalization choice

**Verdict: PASS (control) — the cross-level trend is NORMALIZATION-ROBUST.** On a
consistent fixed-policy series the order-anisotropy peaks at n=5 for *every* natural
normalization `L_α(n) = diff/base^α`, `α ∈ [0,1]` (α=0 absolute, α=1 relative-to-boundary).
The decisive flip exponent is `α*₅→₆ = 2.00` (H≈0.5) and `2.61` (H≈0.2) — both well above
1, robust to the n=5,6 sampling error (`P(α*₅→₆ ≤ 1) = 0`). So [Module
24](sampled-order-n5.md)'s "absolute decays / relative grows" divergence was an **artifact
of comparing two different threshold policies over two points**, not a real gauge freedom.
The "survival, not leverage" ceiling is now the cleanest it has been: gauge-independent.
No P vs NP claim.

## Why this module exists

[Module 24](sampled-order-n5.md) left the sharpest open flag of the entire survival arc.
Reporting the first cross-level data point it noted the trend was **normalization-
dependent**: the *absolute* pair-influence difference DECAYED (n=4 `4.9e-4` → n=5 `1.4e-4`)
while the difference *relative to the boundary* GREW (`0.8% → 3.7%`). If that divergence
were real, the central question — *is there cross-level LEVERAGE?* — would be **ill-posed**:
the answer would be whatever the chooser of the normalization wants it to be.

But that observation compared **two different threshold policies** (the faithful
`θ=0.5·max` wall, which degenerates at n≥6) over only **two levels**. [Module
26](iso-hardness.md) now provides a *consistent* iso-hardness series at **three** levels
for two `H` slices. With one fixed policy the gauge question can finally be settled.

## The gauge family

Interpolate the two named normalizations of Module 24 with a single exponent:

```
L_α(n) = diff_prob(n) / base_prob(n)^α ,    α ∈ [0, 1]
```

`α=0` is the absolute difference (Module 24's "abs"); `α=1` is the difference-relative-to-
boundary (its "rel"). The interval endpoints are *pinned by the prior flag*, not chosen to
win. Because

```
log L_α(n) = log diff(n) − α · log base(n)
```

is **linear in α**, the trend across a level pair,
`Δ(α) = log L_α(n+1) − log L_α(n) = A − α·B` with `A = log(diff_{n+1}/diff_n)`,
`B = log(base_{n+1}/base_n)`, keeps a **constant sign** over `α ∈ [0,1]` iff its two
endpoints `Δ(0)=A` (abs) and `Δ(1)=A−B` (rel) share a sign. Equivalently the trend flips
at the **critical exponent `α* = A/B`**; if `α*` lies *outside* `[0,1]` the whole interval
agrees. So checking the abs and rel endpoints **proves** the entire family.

## Pre-declared killer

Compute `α*₅→₆` on both `H` slices. If `α*₅→₆ ≤ 1` on *either* slice, then within the
natural gauge range some normalization turns the n=5 peak into monotone growth ⇒ the
leverage is **gauge-dependent** and Module 24's flag **stands**. PASS iff `α*₅→₆ > 1` on
*both* slices (the n=5 peak is gauge-invariant over `[0,1]`), **and** that conclusion
survives the sampling error of the n=5,6 estimates — a Monte-Carlo propagation of the CRN
standard error (and the binomial error of `base_prob`) onto `α*`, requiring
`P(α*₅→₆ ≤ 1)` small.

The killer can genuinely fire: `test_gauge_killer_fires_when_relative_grows` feeds a
synthetic series where `base` falls fast enough that `rel` grows monotonically, landing
`α*₅→₆ ∈ (0,1]` and firing the killer.

## Measured (sampled iso-hardness series; n=4 exact, n=5,6 CRN pooled over 6 seeds)

| H_target | pair | Δ_abs (α=0) | Δ_rel (α=1) | α\* | same sign over [0,1] |
|----------|------|-------------|-------------|-----|----------------------|
| **0.5** | 4→5 | **+0.312** | **+0.662** | −0.89 | yes (both rise) |
|         | 5→6 | **−0.671** | **−0.335** | **+2.00** | yes (both fall) |
| **0.2** | 4→5 | **+0.376** | **+0.444** | −5.47 | yes (both rise) |
|         | 5→6 | **−1.051** | **−0.649** | **+2.61** | yes (both fall) |

`peak level by α ∈ {0, .25, .5, .75, 1}` = **n=5 at every α**, on both slices.
`gauge_invariant_peak = True`; `α*₅→₆ = 2.00 / 2.61`; `P(α*₅→₆ ≤ 1) = 0.0000` (200k MC
draws); **killer does not fire; PASS on both slices.**

The gauge analysis introduces **no new sampling** of the meta-function — it is an exact
post-analysis of the frozen Module-26 rows. The n=4 endpoint of each slice is the exact
full sweep.

## What it shows

1. **The trend is gauge-invariant.** On both slices the absolute and relative trends
   *agree* — they rise together 4→5 and fall together 5→6 — so `L_α` peaks at n=5 for
   *every* `α ∈ [0,1]`. You would have to **over-normalize** (divide by `base^≈2–2.6`,
   outside the abs↔rel range) to manufacture monotone growth.

2. **Module 24's gauge flag is falsified.** Its "abs decays / rel grows" divergence was
   an artifact of comparing the faithful-θ policy at n=4 with a different policy at n=5
   over two points. Under one fixed policy across three levels the divergence vanishes:
   the divergence was *between policies*, not *between normalizations*.

3. **"No leverage" is now gauge-independent.** Removing the normalization escape, the
   non-monotone (peak-at-n=5) shape is a real property of these three levels, not a choice
   of denominator. The ceiling stands more firmly.

## The ceiling (unchanged, now cleaner)

* **Still survival, not leverage.** This cycle does not lift the ceiling; it closes one of
  the last ways to *argue around* it. The observed trend is bounded and non-monotone for
  every natural normalization.
* **Three levels, n=4 exact vs n≥5 sampled.** The gauge-invariance is established *across
  these three points only*. It does **not** assert the asymptotic leverage is zero: a true
  asymptotic shape could differ beyond n=6 (`N = 2^7 = 128`, out of reach). What this rules
  out is the specific alternative "the non-monotonicity is just your normalization".
* The asymptotic amplification (small LB → separation) remains **CITED** (Oliveira–Pich
  2019; Chen–Jin–Williams 2019/20; Chen–Hirahara–Ren–Santhanam–Vyas), never computed.

## Honesty boundary

ESTIMATED, not computed: the n=5 and n=6 `diff_prob` (Monte Carlo, CRN, pooled over 6
seeds) feeding the gauge analysis. COMPUTED exactly: both n=4 rows (full sweep); the gauge
post-analysis itself (`Δ_abs`, `Δ_rel`, `α*`) is an exact function of the rows. PROPAGATED:
`P(α*₅→₆ ≤ 1)` over 200k Monte-Carlo draws of the n=5,6 CRN error and the binomial `base`
error (= 0 on both slices). PINNED, not chosen: the gauge interval `[0,1]` is exactly
Module 24's two named normalizations. NOT shown: any asymptotic statement; the result is
about the gauge-robustness of the trend across the *three available levels*. CITED, never
computed: the magnification / locality theorems. No separation, no P vs NP claim.
