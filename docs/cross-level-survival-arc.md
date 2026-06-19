# The Cross-Level Survival Arc (Modules 24–27) — capstone

*Crystallized 2026-06-19. This closes the executable **Magnification Frontier** program
(`prompts/magnification-frontier.md`, `RESEARCH_LOG.md` Entries 13–24) at its honest
positive ceiling. It proves **no** lower bound and makes **no claim about P vs NP**. It is
the companion to [Module 22](order-locality.md): where Module 22 found the order-anisotropy
of `MBPSP[s]` **exactly at a single level** (n=4), this arc establishes — under sampling and
multiple controls — that the anisotropy **survives every reachable level (n=4,5,6)** while
exhibiting **no cross-level leverage**. Leverage is the heart of magnification; it stays
asymptotic and CITED, escaping tiny executable sizes by construction.*

## What the arc is about

The Magnification Frontier program asked for the **leverage** — not a static wall at one
`n`, but how a quantity *grows across levels*, the slope of the amplification staircase
(`prompts/magnification-frontier.md`, "the leverage principle"). [Module 22](order-locality.md)
delivered the program's first non-collapsing object: `MBPSP[s]` = min-OBDD-size at a **fixed
variable order** (`HARD = no small OBDD`), the one meta-function that is **not** permutation-
invariant. Its order-anisotropy — the pre-registered gap between the top variable `x_{n-1}`
and `x0` in the pair-influence of `MBPSP[s]` — was exact at n=4 (`184/65536` for the
weight-1 class) but seen at a **single level**: n=5 means `2^32` truth tables, beyond the
exact sweep.

This arc is four cycles that turned that single point into a **multiply-controlled
cross-level measurement**, and read off what it does and does not show.

## The four modules

| # | Module | Move | Result |
|---|--------|------|--------|
| 24 | [Sampled Order-Anisotropy](sampled-order-n5.md) | **Spend exactness for reach**: both Module-22 statistics are sums of indicators over the uniform meta-space → estimate by **Monte Carlo** with a **Common-Random-Numbers** estimator (`min_obdd_size` is `O(N)`). | The anisotropy **survives to n=5** (pooled z≈4.9, exact n=4 anchor inside its CI, popcount null control flat, killer does not fire). The lab's **first cross-level PASS**. |
| 25 | [Cross-Level Median](cross-level-median.md) | The faithful `θ=0.5·max` threshold degenerates at n≥6 (random OBDD sizes concentrate near the max → constant-HARD). **Recalibrate** the threshold to the **median** OBDD size to keep the boundary open. | **Survives all three levels** (n=4 exact, n=5 z=73, n=6 z=43, control flat at each). On a *recalibrated* object. |
| 26 | [Iso-Hardness Control](iso-hardness.md) | The median policy let the hard-fraction `H` drift (0.17/0.25/0.44); maybe `rel` tracks `H`, not `n`. **Hold `H` ≈ fixed** (the `(1−H_target)` quantile) on two slices (H=0.5, 0.2). | **Survival is H-ROBUST** (killer does not fire at fixed H) and the **H-confound is FALSIFIED** (at fixed H, `rel` still peaks at n=5). |
| 27 | [Leverage Gauge-Invariance](leverage-gauge.md) | Module 24 called the trend *normalization-dependent* ("abs decays / rel grows"). Interpolate with `L_α(n)=diff/base^α`; since `log L_α` is linear in α, the abs+rel endpoints prove all `α∈[0,1]`. | The n=5 peak is **gauge-invariant** (α*₅→₆ = 2.00/2.61 > 1, `P(α*≤1)=0`). M24's divergence was an artifact *between policies*, not *between normalizations*. **"No leverage" is gauge-independent.** |

## The two-sided verdict

**Survival — established, and defended from every side at n≤6.** The order-anisotropy of
`MBPSP[s]` is real and persistent: significant at every reachable level (z from ≈5 to ≈73),
all seeds positive, with the permutation-invariant popcount null control flat throughout.
It is **not** an n=4 artifact (Module 24), **not** an artifact of the hard-fraction drifting
(Module 26), and **not** an artifact of the chosen normalization (Module 27). Three distinct
confounds were pre-registered as killers; none fired. This is a faithful, reproducible,
multiply-controlled executable model of cross-level **survival**.

**Leverage — genuinely absent across the reachable levels.** The effect does **not** grow:
the relative anisotropy `rel` is **bounded and non-monotone**, peaking at n=5 (e.g.
`5.5 → 10.7 → 7.6 %` at H≈0.5), and that peak is now known to be **gauge-invariant** — it
holds for every natural normalization, so it is a property of the *level*, not of the
denominator. Magnification needs a *growing* leverage; this is a curve that rises then falls.

## The ceiling (why the program closes here)

The amplification operator that magnification is *about* is asymptotic. The arc renders the
**survival** of its non-invariant ingredient exactly executable; it **cannot** render the
**leverage**, for a structural reason the program named from the start:

* **Only three levels exist.** n=4 is the last exact level; n=5 (`2^32`) and n=6 (`2^64`)
  are reachable only by sampling; **n=7 is `2^128` truth tables** — out of reach by
  construction. Three points cannot exhibit an asymptotic slope; they can only show that
  *across these three* the trend does not grow.
* **What the controls buy.** Modules 26–27 do not lift the ceiling — they remove the two
  ways one could have *argued around* it ("maybe it's the hardness drift", "maybe it's your
  normalization"). After them, the absence of leverage at n≤6 is a clean fact, not a
  confound. That is the honest positive close: a well-defended *negative* about leverage
  plus a well-defended *positive* about survival.
* **Leverage stays CITED.** The asymptotic amplification (a weak lower bound for gap-MCSP/
  MKtP blowing up into a separation) remains cited, never computed: Oliveira–Pich 2019;
  Chen–Jin–Williams 2019/20; McKay–Murray–Williams 2019; Chen–Hirahara–Ren–Santhanam–Vyas.

## Place in the lab

This is the **Magnification Frontier**'s honest terminus, mirroring how [Module 22](order-locality.md)
closed the locality sub-branch and [the Collapse Theorem](collapse-theorem.md) closed the
CSP/algebraic branch. The lab tally across both branches: **12 restatements + 1 falsification
+ 1 non-collapse (Module 22) + survival-PASS@1 (Module 24) + survival-PASS@3 (Module 25) +
2 control-PASS that harden the ceiling by falsifying a confound (Module 26 = H-confound,
Module 27 = gauge-confound).** The lab is a *methodology* — make a deep asymptotic
phenomenon run, exactly, on tiny instances, and report precisely where the asymptotic content
escapes — not an attack on P vs NP.

## Honesty boundary

ESTIMATED, not computed: every n=5 and n=6 number (Monte Carlo, CRN, pooled over seeds),
with 99% confidence intervals validated by the exact n=4 anchor. COMPUTED exactly: all n=4
rows (full sweep), `min_obdd_size` (`O(N)` per table, also at n=6 on 64-bit tables), the
popcount control's exact-0 by symmetry, and the gauge post-analysis (`Δ_abs`, `Δ_rel`, `α*`
as exact functions of the rows). RECALIBRATED (stated): the median (Module 25) and
iso-hardness (Module 26) thresholds differ from Module 22's faithful `θ=0.5·max` policy.
NOT shown: any *growing* cross-level leverage, and any *asymptotic* statement — the results
hold across the three reachable levels only; the n=5 peak could itself be a finite-size shape
whose asymptote lies beyond n=6. CITED, never computed: the magnification / locality
theorems. **No separation, no P vs NP claim — this arc measures whether one order-anisotropy
survives, and whether it amplifies. It survives; it does not amplify.**
