"""Sampled order-anisotropy at n=5 — the lab's FIRST deliberate trade of exactness
for reach, to get the one cross-level data point Module 22 could not.

EN-first summary (Honesty boundary at the bottom).

WHY THIS MODULE EXISTS.  Module 22 (``order_locality.py``) found the lab's only
non-collapsing outcome: ``MBPSP[s]`` (min-OBDD-size at a FIXED variable order) is
NOT permutation-invariant, and at n=4 its ``pair_influence`` distinguishes
equal-weight difference vectors by their order-support (weight-1 spread 184: top
variable x3 -> 4056, x1 -> 3872).  But the asymmetry was seen at a SINGLE level
(n=4); n=5 means ``N = 2^5 = 32`` meta-coordinates and ``2^32`` truth tables, so
the EXACT sweep that built every prior number is infeasible.  Module 23 then proved
that a WALL invariant cannot be made cheap per-instance: it is irreducibly a
statistic over the SET of all functions, and reintroducing the set brings the sweep
back.

THE PIVOT (the lab's own thesis turned into a method).  "Exactness is the trap":
here we SPEND exactness to gain reach.  Both Module-22 statistics are SUMS OF
INDICATORS over the uniform meta-input space ``t in {0,...,2^N-1}``:

    pair_influence(d) = SUM_t [ MBPSP[s] non-constant on {t, t^e0, t^ed, t^(e0^ed)} ].

A sum of indicators over a uniform space is exactly what Monte Carlo estimates.  The
per-sample cost is ``min_obdd_size`` on a 32-bit table = O(N), microseconds — the
SAME cheapness Module 23 noted for a single function, now harnessed to estimate the
SET statistic instead of certifying one instance.  We recover the wall invariant
Module 23 could not, paying in a confidence interval instead of an exact integer.

WHICH STATISTIC.  ``pair_influence`` (relative spread ~4.5% at n=4).  The faithful
certified wall ``certified_drop`` (~0.23% at n=4) needs ~(4.5/0.23)^2 ~ 400x more
samples to resolve and is BEYOND sampling reach at this budget — an honest limit,
stated, not hidden.

THE ESTIMATOR — Common Random Numbers (CRN).  Resolving a ~0.3-4% difference between
two counts of size ~2^32 by differencing two independent estimates is hopeless (the
variance of each dwarfs the gap).  Instead we use the SAME random base points ``t``
for ``d_hi`` and ``d_lo`` and average the per-sample difference
``D(t) = I_{d_hi}(t) - I_{d_lo}(t) in {-1,0,1}``.  The two indicators are highly
correlated (they share two of the four cube corners, ``t`` and ``t^e0``), so
``Var(D)`` is small and the standard error of the difference shrinks far faster than
that of either count.  This is what makes the small signal resolvable.

THREE GUARDS AGAINST SELF-DECEPTION (the design the Adversary would demand):
  1. FIDELITY ANCHOR at n=4.  The sampler must reproduce the EXACT, known
     ``pair_influence`` difference (4056-3872 = 184, i.e. p = 184/65536) within its
     CI.  Validated before any n=5 number is trusted (see ``anchor_n4``).
  2. PRE-REGISTERED PAIR, not max-min.  The max-min "spread" is an extreme-value
     statistic biased POSITIVE by sampling noise (the very artifact that killed
     Cycle 1's rho=1 band).  We instead test ONE pre-declared pair fixed by the n=4
     order structure: weight-1 top variable vs bottom variable
     (n=5: d_hi = 16 = bit x4, d_lo = 1 = bit x0).
  3. NULL CONTROL.  A permutation-invariant, equally-cheap meta-function
     (``popcount(t) > s``) sampled by the SAME CRN estimator must return a difference
     consistent with 0 — proving the estimator does not FABRICATE signal from noise.
     (The MCSP formula-size control of Module 21/22 is NOT samplable: min formula
     size of a single 32-bit function is not cheap.  popcount is the cheap
     permutation-invariant stand-in; its difference is provably 0 by symmetry.)

PRE-DECLARED KILLER.  At n=5: if the CRN difference's 99% CI INCLUDES 0 (not
significant), the killer FIRES — the order-anisotropy is not resolvable across
levels and Module 22's n=4 anisotropy is NOT shown to persist (consistent with an
n=4 artifact).  PASS only if (a) the pre-registered pair differs significantly at
n=5 AND (b) the null control difference stays consistent with 0.

This module COMPUTES nothing exactly at n=5 (by construction it cannot); it reports
ESTIMATES with confidence intervals.  No separation, no P vs NP claim.  See the
Honesty boundary at the bottom for the full COMPUTED/CITED/ESTIMATED split.

MEASURED (final verdict — the lab's FIRST cross-level PASS, qualified):

  * ANCHOR (n=4, exact ground truth inside CI): PASS.
  * SIGNAL (n=5, s=10, pre-registered pair x4 vs x0, 8 seeds x 300k, pooled by
    inverse variance):  difference prob ~ +1.7e-4,  pooled z ~ +4.9,
    99% CI excludes 0,  7/8 seeds positive.   The popcount NULL CONTROL on the
    same pair pools to ~0 (not significant).  KILLER does NOT fire => the order-
    anisotropy of MBPSP[s] SURVIVES one level above Module 22's n=4.
  * CEILING (survival, NOT leverage): the cross-level TREND is normalization-
    dependent (absolute pair-influence difference DECAYS n=4 4.9e-4 -> n=5 1.4e-4,
    while the difference relative to the boundary GROWS 0.8% -> 3.7%), and under
    Module 22's faithful threshold policy (s = round(0.5*max)) the measurement
    DEGENERATES at n>=6: random OBDD sizes concentrate near the max (n=6 sample
    min 20 > s 16), the meta-function is constant-HARD, pair-influence -> 0
    (``threshold_regime``).  So sampling buys EXACTLY ONE level over the exact n=4;
    no monotone leverage is established, the asymptotic amplification stays CITED.
"""

from __future__ import annotations

import random
from dataclasses import dataclass
from typing import Callable, List, Optional, Sequence, Tuple

from pnp_lab.meta_complexity import order_locality as ol

# 99% two-sided normal critical value (the CI / significance level used throughout).
Z99 = 2.5758293035489004


# ── hardness predicates (one cheap call each) ──────────────────────────────

def mbpsp_predicate(n: int, s: int) -> Callable[[int], bool]:
    """HARD(t) = ( min_obdd_size(t ; fixed order) > s ) — the Module-22 meta-function,
    one O(N) call per truth table."""
    def hard(t: int) -> bool:
        return ol.min_obdd_size(t, n) > s
    return hard


def popcount_predicate(s: int) -> Callable[[int], bool]:
    """HARD(t) = ( popcount(t) > s ) — the NULL control: manifestly permutation-
    invariant (a variable permutation only permutes truth-table bit positions, leaving
    the popcount fixed), so its pair-influence depends on weight(d) ONLY and the CRN
    difference for two equal-weight d is exactly 0.  Equally cheap (one popcount)."""
    def hard(t: int) -> bool:
        return bin(t).count("1") > s
    return hard


# ── the CRN paired-difference estimator (the heart of the pivot) ───────────

@dataclass
class DiffEstimate:
    d_hi: int
    d_lo: int
    M: int                       # number of Monte Carlo samples
    mean_prob: float             # estimate of (pairinf(d_hi) - pairinf(d_lo)) / 2^N
    se_prob: float               # standard error of mean_prob (CRN, so small)
    N: int                       # 2^n meta-coordinates  (count = prob * 2^N)

    @property
    def mean_count(self) -> float:
        """The difference expressed back in pair-influence COUNT units (x 2^N)."""
        return self.mean_prob * (1 << self.N)

    @property
    def se_count(self) -> float:
        return self.se_prob * (1 << self.N)

    @property
    def z(self) -> float:
        return self.mean_prob / self.se_prob if self.se_prob > 0 else 0.0

    @property
    def ci99_prob(self) -> Tuple[float, float]:
        h = Z99 * self.se_prob
        return (self.mean_prob - h, self.mean_prob + h)

    @property
    def significant(self) -> bool:
        """True iff the 99% CI excludes 0 (the pre-declared PASS condition for the
        pre-registered pair / FIRE condition when this is the control)."""
        lo, hi = self.ci99_prob
        return lo > 0 or hi < 0


def crn_pair_diff(hard: Callable[[int], bool], N: int, d_hi: int, d_lo: int,
                  M: int, rng: random.Random) -> DiffEstimate:
    """CRN Monte Carlo estimate of ``(pairinf(d_hi) - pairinf(d_lo)) / 2^N`` for a
    hardness predicate ``hard`` on ``2^N``-entry truth tables.

    For each random base ``t`` we evaluate the four-cube indicator for BOTH d at the
    same ``t`` (sharing the corners ``t`` and ``t^e0``), and average the per-sample
    difference ``D(t) = I_hi(t) - I_lo(t)``.  Returns the mean and its standard error
    (sample-std / sqrt(M)); the shared corners make ``Var(D)`` small."""
    e0 = 1
    e_hi = 1 << d_hi
    e_lo = 1 << d_lo
    top = 1 << N                              # sample t uniformly in [0, 2^N)
    s1 = 0.0
    s2 = 0.0
    for _ in range(M):
        t = rng.randrange(top)
        a = hard(t)
        b0 = hard(t ^ e0)                     # shared corner, computed once (CRN)
        chi = hard(t ^ e_hi)
        dhi = hard(t ^ e0 ^ e_hi)
        clo = hard(t ^ e_lo)
        dlo = hard(t ^ e0 ^ e_lo)
        i_hi = 0 if (a == b0 == chi == dhi) else 1
        i_lo = 0 if (a == b0 == clo == dlo) else 1
        diff = i_hi - i_lo
        s1 += diff
        s2 += diff * diff
    mean = s1 / M
    var = max(s2 / M - mean * mean, 0.0)
    se = (var / M) ** 0.5
    return DiffEstimate(d_hi=d_hi, d_lo=d_lo, M=M, mean_prob=mean, se_prob=se, N=N)


# ── threshold at n=5 (no sweep): estimate the max OBDD size from a sample ───

def estimate_max_obdd(n: int, M: int, rng: random.Random) -> int:
    """Estimate ``max_t min_obdd_size(t)`` over n-bit functions from M random truth
    tables.  Random functions are near-maximal in OBDD size, so the sample max is a
    tight lower bound on the true max; the fixed-fraction threshold ``round(max*0.5)``
    sits in the middle of a robustness band (Module 22 verified s-invariance across
    s in [5,10]), so an exact max is not needed."""
    N = 1 << n
    top = 1 << N
    return max(ol.min_obdd_size(rng.randrange(top), n) for _ in range(M))


def fixed_fraction_threshold_sampled(n: int, theta: float, M: int,
                                     rng: random.Random) -> int:
    return round(estimate_max_obdd(n, M, rng) * theta)


# ── the fidelity anchor at n=4 (exact ground truth vs sampler) ─────────────

@dataclass
class AnchorResult:
    d_hi: int
    d_lo: int
    exact_count: int             # exact pairinf(d_hi) - pairinf(d_lo) (Module 22 truth)
    est: DiffEstimate            # the sampler's estimate of the same quantity
    within_ci: bool              # exact value inside the sampler's 99% CI?


def anchor_n4(M: int = 60000, seed: int = 0, theta: float = 0.5,
              d_hi: int = 8, d_lo: int = 2) -> AnchorResult:
    """Run the CRN sampler at n=4 (where the EXACT answer is known and cheap) for the
    weight-1 top-vs-low pair (default d_hi=8 = x3, d_lo=2 = x1, the Module-22 spread)
    and check the exact count difference falls inside the sampler's 99% CI.  This
    validates the estimator before any n=5 number is reported."""
    n = 4
    N = 1 << n
    costs = ol.obdd_costs(n)
    s = ol.fixed_fraction_threshold(costs, theta)
    meta = ol.meta_truth_table_obdd(costs, s)
    exact = ol.pair_influence(meta, d_hi) - ol.pair_influence(meta, d_lo)
    hard = mbpsp_predicate(n, s)
    rng = random.Random(seed)
    est = crn_pair_diff(hard, N, d_hi, d_lo, M, rng)
    lo, hi = est.ci99_prob
    within = lo * (1 << N) <= exact <= hi * (1 << N)
    return AnchorResult(d_hi=d_hi, d_lo=d_lo, exact_count=exact, est=est,
                        within_ci=within)


# ── the n=5 measurement + null control + verdict ───────────────────────────

@dataclass
class Verdict:
    n: int
    N: int
    s: int
    M: int
    signal: DiffEstimate         # MBPSP[s] pre-registered pair (top var vs bottom var)
    control: DiffEstimate        # popcount null control, same pair, same M
    killer_fires: bool           # True => no resolvable cross-level anisotropy
    passes: bool                 # True => signal significant AND control consistent with 0


def measure_n5(M: int = 400000, seed: int = 1, theta: float = 0.5,
               d_hi: int = 16, d_lo: int = 1, s: Optional[int] = None,
               max_sample: int = 4000) -> Verdict:
    """The decisive n=5 run.  Estimates the CRN pair-influence difference for the
    pre-registered weight-1 pair (d_hi = 16 = top variable x4, d_lo = 1 = x0) on
    MBPSP[s], and the SAME pair on the popcount null control.

    KILLER: fires iff the MBPSP signal's 99% CI includes 0.  PASS iff the signal is
    significant AND the control's CI includes 0."""
    n = 5
    N = 1 << n                                 # 32 meta-coordinates, 2^32 truth tables
    rng = random.Random(seed)
    if s is None:
        s = fixed_fraction_threshold_sampled(n, theta, max_sample, rng)
    signal = crn_pair_diff(mbpsp_predicate(n, s), N, d_hi, d_lo, M, rng)
    # control threshold: median popcount of a 2^N-bit table = N/2 (=16) -> HARD if above
    control = crn_pair_diff(popcount_predicate(N // 2), N, d_hi, d_lo, M,
                            random.Random(seed + 1))
    killer = not signal.significant
    passes = signal.significant and not control.significant
    return Verdict(n=n, N=N, s=s, M=M, signal=signal, control=control,
                   killer_fires=killer, passes=passes)


# ── replicated verdict (the ROBUST n=5 result: pool independent seeds) ──────
#
# A single 400k-sample run is unstable (z bounced from -0.65 at 80k to +3.3 at
# 1.2M, same seed).  The robust statement pools INDEPENDENT seeds by inverse-
# variance weighting and checks the SIGN consistency — the replication the
# Adversary would demand.  MEASURED (8 seeds x 300k, s=10, pre-registered pair
# d_hi=16 [x4] vs d_lo=1 [x0]): pooled z ~ +4.9, 99% CI excludes 0, 7/8 positive,
# popcount control consistent with 0.  PASS — the killer does NOT fire.

@dataclass
class PooledVerdict:
    n: int
    N: int
    s: int
    M_per_seed: int
    seeds: int
    mean_prob: float             # inverse-variance pooled difference estimate
    se_prob: float
    z: float
    ci99_prob: Tuple[float, float]
    frac_positive: float         # fraction of seeds with a positive estimate
    control_mean: float          # pooled popcount null-control difference
    control_z: float
    killer_fires: bool           # True => pooled signal CI includes 0
    passes: bool                 # signal significant AND control consistent with 0


def _pool(estimates: Sequence[DiffEstimate]) -> Tuple[float, float]:
    """Inverse-variance pool of independent CRN estimates -> (mean, se)."""
    ws = [1.0 / e.se_prob ** 2 for e in estimates if e.se_prob > 0]
    ms = [e.mean_prob for e in estimates if e.se_prob > 0]
    sw = sum(ws)
    mean = sum(m * w for m, w in zip(ms, ws)) / sw
    return mean, (1.0 / sw) ** 0.5


def replicate_n5(M_per_seed: int = 300000, seeds: int = 8, theta: float = 0.5,
                 d_hi: int = 16, d_lo: int = 1, s: Optional[int] = None,
                 base_seed: int = 1000) -> PooledVerdict:
    """The ROBUST n=5 verdict: pool ``seeds`` independent CRN runs of the pre-
    registered pair on MBPSP[s], plus the popcount null control on the same pair.
    PASS iff the pooled signal's 99% CI excludes 0 AND the pooled control's does not."""
    n = 5
    N = 1 << n
    if s is None:
        s = fixed_fraction_threshold_sampled(n, theta, 4000, random.Random(7))
    hard = mbpsp_predicate(n, s)
    ctrl = popcount_predicate(N // 2)
    sig = [crn_pair_diff(hard, N, d_hi, d_lo, M_per_seed, random.Random(base_seed + k))
           for k in range(seeds)]
    con = [crn_pair_diff(ctrl, N, d_hi, d_lo, M_per_seed,
                         random.Random(base_seed + 5000 + k)) for k in range(seeds)]
    mean, se = _pool(sig)
    cmean, cse = _pool(con)
    lo, hi = mean - Z99 * se, mean + Z99 * se
    clo, chi = cmean - Z99 * cse, cmean + Z99 * cse
    killer = lo <= 0 <= hi
    control_sig = clo > 0 or chi < 0
    return PooledVerdict(
        n=n, N=N, s=s, M_per_seed=M_per_seed, seeds=seeds,
        mean_prob=mean, se_prob=se, z=mean / se, ci99_prob=(lo, hi),
        frac_positive=sum(1 for e in sig if e.mean_prob > 0) / seeds,
        control_mean=cmean, control_z=cmean / cse if cse > 0 else 0.0,
        killer_fires=killer, passes=(not killer) and (not control_sig))


# ── the CEILING, measured: the faithful threshold regime degenerates at n>=6 ─

@dataclass
class RegimeRow:
    n: int
    N: int
    size_min: int
    size_median: int
    size_max: int
    s: int                       # round(theta * size_max)
    H_frac: float                # fraction of sampled functions that are HARD
    base_prob: float             # pairinf(d=1) rate = "boundary" the signal lives on


def threshold_regime(ns: Sequence[int] = (4, 5, 6, 7), sample: int = 3000,
                     base_M: int = 40000, theta: float = 0.5,
                     seed: int = 42) -> List[RegimeRow]:
    """Why the pivot reaches EXACTLY n=5 under Module 22's faithful policy
    (s = round(theta * max)).  MEASURED: random OBDD sizes concentrate near the max
    as n grows, so the fixed-fraction threshold leaves NO boundary at n>=6 (the
    sample min already exceeds s), the meta-function is constant-HARD, and the
    pair-influence the estimator reads -> 0 (base_prob = 0).  This is the honest
    ceiling: sampling buys exactly one level over the exact n=4 of Module 22."""
    import statistics
    rows: List[RegimeRow] = []
    for n in ns:
        N = 1 << n
        top = 1 << N
        rng = random.Random(seed)
        sizes = [ol.min_obdd_size(rng.randrange(top), n) for _ in range(sample)]
        smax = max(sizes)
        s = round(smax * theta)
        h = sum(1 for z in sizes if z > s) / len(sizes)
        hard = mbpsp_predicate(n, s)
        rng2 = random.Random(7)
        e0, el = 1, 1 << 1
        bc = 0
        for _ in range(base_M):
            t = rng2.randrange(top)
            a = hard(t)
            if not (a == hard(t ^ e0) == hard(t ^ el) == hard(t ^ e0 ^ el)):
                bc += 1
        rows.append(RegimeRow(n=n, N=N, size_min=min(sizes),
                              size_median=int(statistics.median(sizes)),
                              size_max=smax, s=s, H_frac=h, base_prob=bc / base_M))
    return rows


# ── CROSS-LEVEL (median-calibrated): push the survival to n=6 (Module 25) ───
#
# The faithful theta=0.5*max policy degenerates at n>=6 (random OBDD sizes
# concentrate near max -> constant-HARD -> pair-influence 0).  To keep the boundary
# OPEN at every level we RECALIBRATE the threshold to the MEDIAN OBDD size, so the
# meta-function stays non-trivial (H ~ 0.17-0.44) and the 4-cubes straddle s.  The
# PRICE: this is a DIFFERENT object from Module 22's faithful wall (recalibrated, not
# the same threshold).  With it the order-anisotropy is measurable on THREE levels.
#
# MEASURED (median policy, pre-registered pair top-var vs x0; n=4 exact, n=5,6
# sampled CRN, frozen):
#
#     n   s    H_frac   base_prob   diff_prob    z       rel=diff/base   control
#     4* 10   0.170    0.321       +2.34e-2     exact   +7.3%           0 (exact)
#     5  16   0.246    0.300       +3.53e-2     +73     +11.8%          flat (z=-0.95)
#     6  26   0.435    0.282       +2.05e-2     +43     +7.3%           flat (z=-0.24)
#
# SURVIVES all three levels (6/6 seeds positive at n=5,6; control flat at every
# level).  But the LEVERAGE does NOT grow: rel is non-monotone and bounded
# (7.3 -> 11.8 -> 7.3 %), and is confounded by H varying across levels (the integer-
# median policy does not hold the meta-function balance fixed).  Cross-level SURVIVAL,
# NOT cross-level leverage growth.  The asymptotic amplification stays CITED.

def median_threshold(n: int, sample: int = 4000, seed: int = 7) -> int:
    """s = median ``min_obdd_size`` over the n-bit functions: EXACT (full sweep) at
    n<=4, SAMPLED (random functions) at n>=5.  Recalibrates the meta-function so the
    boundary stays open at every level (unlike the faithful theta=0.5*max policy,
    which degenerates at n>=6)."""
    import statistics
    if n <= 4:
        return int(statistics.median(ol.obdd_costs(n)))
    N = 1 << n
    rng = random.Random(seed)
    return int(statistics.median(ol.min_obdd_size(rng.randrange(1 << N), n)
                                 for _ in range(sample)))


@dataclass
class CrossLevelRow:
    n: int
    N: int
    s: int                       # median-calibrated threshold
    H_frac: float
    base_prob: float             # pairinf(d=1) rate (the open boundary)
    diff_prob: float             # pooled (pairinf(top) - pairinf(x0)) / 2^N
    se_prob: float
    z: float                     # +inf at n=4 (exact)
    rel: float                   # diff_prob / base_prob (leverage relative to boundary)
    control_z: float
    frac_positive: float
    significant: bool
    exact: bool


def _anisotropy_row(n: int, s: int, seeds: int, M: int,
                    base_seed: int, sample: int = 4000) -> CrossLevelRow:
    """One row of the cross-level order-anisotropy measurement at a GIVEN threshold
    ``s`` for the pre-registered pair (top variable ``x_{n-1}`` vs ``x0``).  The
    threshold POLICY (median vs iso-hardness) is the caller's choice; the measurement
    is identical.  EXACT at n<=4 (full sweep, control is 0 by symmetry); SAMPLED +
    pooled CRN at n>=5 with the popcount null control."""
    N = 1 << n
    d_hi = 1 << (n - 1)                          # top-variable input index
    if n <= 4:
        meta = ol.meta_truth_table_obdd(ol.obdd_costs(n), s)
        base = ol.pair_influence(meta, 1)
        top = ol.pair_influence(meta, d_hi)
        diff = top - base
        return CrossLevelRow(
            n=n, N=N, s=s, H_frac=sum(meta) / (1 << N), base_prob=base / (1 << N),
            diff_prob=diff / (1 << N), se_prob=0.0, z=float("inf"),
            rel=diff / base if base else 0.0, control_z=0.0, frac_positive=1.0,
            significant=True, exact=True)
    hard = mbpsp_predicate(n, s)
    ctrl = popcount_predicate(N // 2)
    # H and base on one pass
    rng = random.Random(11)
    e0, el = 1, 1 << 1
    H = bc = 0
    M0 = 6000
    for _ in range(M0):
        t = rng.randrange(1 << N)
        a = hard(t)
        if a:
            H += 1
        if not (a == hard(t ^ e0) == hard(t ^ el) == hard(t ^ e0 ^ el)):
            bc += 1
    sig = [crn_pair_diff(hard, N, d_hi, 1, M, random.Random(base_seed + k))
           for k in range(seeds)]
    con = [crn_pair_diff(ctrl, N, d_hi, 1, M, random.Random(base_seed + 500 + k))
           for k in range(seeds)]
    mean, se = _pool(sig)
    cmean, cse = _pool(con)
    base_prob = bc / M0
    return CrossLevelRow(
        n=n, N=N, s=s, H_frac=H / M0, base_prob=base_prob, diff_prob=mean, se_prob=se,
        z=mean / se, rel=mean / base_prob if base_prob else 0.0,
        control_z=cmean / cse if cse > 0 else 0.0,
        frac_positive=sum(1 for e in sig if e.mean_prob > 0) / seeds,
        significant=(mean - Z99 * se > 0 or mean + Z99 * se < 0), exact=False)


def cross_level_row(n: int, seeds: int = 6, M: int = 150000,
                    base_seed: Optional[int] = None, sample: int = 4000) -> CrossLevelRow:
    """One row of the median-calibrated cross-level table for the pre-registered pair
    (top variable ``x_{n-1}`` vs ``x0``).  EXACT at n<=4 (full sweep, control is 0 by
    symmetry); SAMPLED + pooled CRN at n>=5 with the popcount null control."""
    if base_seed is None:
        base_seed = 300 + n * 10
    return _anisotropy_row(n, median_threshold(n, sample=sample), seeds, M,
                           base_seed, sample)


def cross_level_table(ns: Sequence[int] = (4, 5, 6), seeds: int = 6,
                      M: int = 150000) -> List[CrossLevelRow]:
    """The median-calibrated cross-level table (Module 25): order-anisotropy survival
    of MBPSP[s] across levels.  MEASURED: survives n=4,5,6; leverage non-monotone and
    bounded (no growth); control flat at every level."""
    return [cross_level_row(n, seeds=seeds, M=M) for n in ns]


# ── ISO-HARDNESS (Module 26): disentangle the leverage from the H-confound ──
#
# Module 25's Adversary left one open objection: the median-integer policy does NOT
# hold the hard-fraction H fixed across levels (H = 0.17 / 0.25 / 0.44 at n=4,5,6),
# and the relative anisotropy ``rel`` could be tracking H rather than the level n.  If
# so, BOTH readings of Module 25 are at risk: the "survival" could be an H-artifact,
# and the "no leverage" verdict could be hiding leverage that H-drift cancels.
#
# THE CONTROL.  Re-pick the threshold to HOLD H ~ constant across levels (the
# (1-H_target) quantile of the OBDD-size distribution) instead of the median, and
# re-measure.  Integer thresholds cannot hit H_target exactly (OBDD sizes are coarse:
# at n=4 frac>s jumps 0.526 -> 0.170 between s=9 and s=10), but the achievable H lands
# FAR tighter than the median policy: for H_target=0.5 the rows are H ~ 0.53/0.55/0.44
# vs the median policy's 0.17/0.25/0.44.  Run TWO matched-H slices (H_target 0.5 and
# 0.2) so the residual H-drift can be regressed out: the within-level H-sensitivity of
# rel is small (n=4 exact: rel 2.9% -> 7.3% as H 0.93 -> 0.17) compared to the
# cross-level effect we test.
#
# PRE-DECLARED KILLER.  At fixed H, if the signal LOSES significance at n=5 or n=6
# (99% CI includes 0), the killer FIRES: Module 25's survival was an H-artifact.  PASS
# if the signal stays significant at every level with the control flat.  Then,
# SEPARATELY (descriptive, not a pass/fail): does rel GROW with n at fixed H (the
# magnification prize, cross-level leverage) or stay non-monotone/bounded (survival
# without leverage)?
#
# MEASURED (frozen; n=4 exact, n=5,6 sampled CRN, base_seed 700+10n):
#
#   H_target=0.5  n   s    H_ach   base    diff_prob   z      rel%    control_z
#                 4* 9    0.526   0.559   +3.08e-2    exact  +5.5    0 (exact)
#                 5  15   0.548   0.394   +4.18e-2    +68    +10.6   +0.49
#                 6  26   0.435   0.282   +2.25e-2    +42    +8.0    -0.46
#   H_target=0.2  4* 10   0.170   0.321   +2.34e-2    exact  +7.3    0 (exact)
#                 5  16   0.246   0.299   +3.51e-2    +65    +11.7   +0.49
#                 6  27   0.194   0.200   +1.30e-2    +29    +6.5    -0.46
#
# VERDICT — survival is H-ROBUST, leverage is GENUINELY absent (not an H-confound).
# At BOTH fixed-H slices the signal is hugely significant at every level (control
# flat): the killer does NOT fire, so Module 25's survival is NOT an H-artifact.  AND
# at fixed H the rel curve still PEAKS at n=5 (5.5 -> 10.6 -> 8.0 ; 7.3 -> 11.7 ->
# 6.5): the n=5 peak is H-independent, so the Module-25 H-confound objection is itself
# FALSIFIED — but the peak is bounded and non-monotone, i.e. there is no growing
# leverage hiding behind the H-drift.  The "no leverage" ceiling is now CLEANER (a
# genuine bounded curve, not a confound).  Limit: still only 3 levels, n=4 exact vs
# n>=5 sampled.  The asymptotic amplification stays CITED.

def iso_hardness_threshold(n: int, H_target: float, sample: int = 4000,
                           seed: int = 7) -> int:
    """The integer threshold ``s`` whose hard-fraction ``frac( min_obdd_size > s )`` is
    closest to ``H_target`` — the iso-hardness calibration.  EXACT (full sweep) at
    n<=4, SAMPLED at n>=5.  Holds the meta-function's balance ~constant across levels
    so the cross-level ``rel`` can be read free of the median policy's H-drift."""
    if n <= 4:
        sizes: Sequence[int] = ol.obdd_costs(n)
    else:
        N = 1 << n
        rng = random.Random(seed)
        sizes = [ol.min_obdd_size(rng.randrange(1 << N), n) for _ in range(sample)]
    tot = len(sizes)
    best_s, best_gap = min(sizes) - 1, 2.0
    for s in range(min(sizes) - 1, max(sizes) + 1):
        h = sum(1 for z in sizes if z > s) / tot
        if abs(h - H_target) < best_gap:
            best_s, best_gap = s, abs(h - H_target)
    return best_s


def iso_hardness_row(n: int, H_target: float = 0.5, seeds: int = 6, M: int = 120000,
                     base_seed: Optional[int] = None, sample: int = 4000) -> CrossLevelRow:
    """One row of the iso-hardness cross-level table (Module 26): the pre-registered
    pair on MBPSP[s] with ``s`` chosen so H ~ ``H_target`` at this level.  Same
    estimator / null control / pooling as the median policy — only the threshold
    policy differs."""
    if base_seed is None:
        base_seed = 700 + n * 10
    return _anisotropy_row(n, iso_hardness_threshold(n, H_target, sample), seeds, M,
                           base_seed, sample)


def iso_hardness_table(ns: Sequence[int] = (4, 5, 6), H_target: float = 0.5,
                       seeds: int = 6, M: int = 120000) -> List[CrossLevelRow]:
    """The iso-hardness cross-level table (Module 26): order-anisotropy of MBPSP[s]
    with H held ~ ``H_target`` across levels.  MEASURED: survives n=4,5,6 at fixed H
    (survival is H-robust), and rel still peaks at n=5 (the Module-25 H-confound is
    falsified) but does not grow (no leverage)."""
    return [iso_hardness_row(n, H_target=H_target, seeds=seeds, M=M) for n in ns]


# ── GAUGE-INVARIANCE of the leverage trend (Module 27) ──────────────────────
#
# Module 24 left the sharpest open flag of the whole survival arc: it called the
# cross-level trend NORMALIZATION-DEPENDENT — "absolute pair-influence difference
# DECAYS (n=4 4.9e-4 -> n=5 1.4e-4) while the difference relative to the boundary
# GROWS (0.8% -> 3.7%)".  If that divergence were real, the question "is there
# cross-level LEVERAGE?" would be ILL-POSED (gauge-dependent): the answer would be
# whatever the chooser of the normalization wants.  But that observation compared
# TWO DIFFERENT threshold policies (the faithful theta=0.5*max wall) over only TWO
# levels.  Module 26 now gives a CONSISTENT iso-hardness series at THREE levels for
# two H slices, so the gauge question can be settled.
#
# THE GAUGE FAMILY.  Interpolate absolute and relative with one exponent:
#
#     L_alpha(n) = diff_prob(n) / base_prob(n) ** alpha ,   alpha in [0, 1]
#
# alpha=0 is the absolute difference (Module 24's "abs"); alpha=1 is the
# difference-relative-to-boundary (Module 24's "rel").  Because
#
#     log L_alpha(n) = log diff(n) - alpha * log base(n)
#
# is LINEAR in alpha, the trend across a level pair, Delta(alpha) = log L_alpha(n+1)
# - log L_alpha(n) = A - alpha*B with A = log(diff_{n+1}/diff_n), B =
# log(base_{n+1}/base_n), keeps a CONSTANT SIGN over alpha in [0,1] iff its two
# endpoints Delta(0)=A and Delta(1)=A-B share a sign.  Equivalently the trend FLIPS
# at the critical exponent alpha* = A/B; if alpha* is OUTSIDE [0,1] the level-pair
# trend is the same for every natural normalization.  So checking the abs and rel
# endpoints PROVES the whole interval.
#
# PRE-DECLARED KILLER.  Compute alpha*_{5->6} on both H slices.  If alpha*_{5->6} <=
# 1 on EITHER slice, then within the natural gauge range some normalization turns the
# n=5 peak into monotone growth => the leverage is GAUGE-DEPENDENT and Module 24's
# flag STANDS (we cannot claim a gauge-robust "no leverage").  PASS iff alpha*_{5->6}
# > 1 on BOTH slices (the n=5 peak is gauge-invariant over [0,1]), AND that conclusion
# survives the sampling error of the n=5,6 estimates (Monte-Carlo propagation:
# P(alpha*_{5->6} <= 1) small).
#
# MEASURED (sampled iso-hardness series, n=4 exact + n=5,6 CRN pooled over 6 seeds,
# M=120k; gauge post-analysis is exact, p_killer over 200k MC error-propagation draws):
#
#   H_target   pair   Delta_abs(a=0)  Delta_rel(a=1)  alpha*    same_sign over [0,1]
#   0.5        4->5      +0.31           +0.66         -0.89     yes (both rise)
#   0.5        5->6      -0.67           -0.33         +2.00     yes (both fall)
#   0.2        4->5      +0.38           +0.44         -5.47     yes (both rise)
#   0.2        5->6      -1.05           -0.65         +2.61     yes (both fall)
#
#   => peak level n=5 for every alpha in {0,.25,.5,.75,1}, p_killer = 0.0000 both slices.
#
# VERDICT — the n=5 peak is GAUGE-INVARIANT, the leverage is genuinely absent.  On
# BOTH slices abs and rel rise together 4->5 and fall together 5->6, so L_alpha peaks
# at n=5 for EVERY alpha in [0,1]; alpha*_{5->6} = 2.00 / 2.61 both exceed 1 (you would
# have to OVER-normalize by base^~2-2.6, outside the abs<->rel range, to manufacture
# monotone growth).  Module 24's "abs decays / rel grows" divergence was an artifact of
# comparing two DIFFERENT threshold policies over two points, NOT a real gauge freedom:
# under one fixed policy the trend is normalization-robust.  The "survival not leverage"
# ceiling is now the CLEANEST it has been — gauge-independent, not a normalization
# choice.  The asymptotic amplification stays CITED.

@dataclass
class GaugePair:
    n_lo: int
    n_hi: int
    delta_abs: float             # Delta(0) = log(diff_hi / diff_lo)  (absolute trend)
    delta_rel: float             # Delta(1) = log(rel_hi  / rel_lo)   (relative trend)
    alpha_star: float            # exponent where the trend flips (Delta(alpha*) = 0)

    @property
    def same_sign(self) -> bool:
        """True iff the absolute and relative trends agree => the level-pair trend is
        the same for every alpha in [0,1] (alpha* outside (0,1))."""
        return (self.delta_abs > 0) == (self.delta_rel > 0)


@dataclass
class GaugeVerdict:
    H_target: float
    pairs: List[GaugePair]
    peak_n_by_alpha: dict        # alpha (grid) -> argmax_n L_alpha(n)
    gauge_invariant_peak: bool   # same argmax for every alpha in the grid AND endpoints
    alpha_star_5_6: float        # the decisive flip exponent for the 5->6 pair
    p_killer: float              # P(alpha*_{5->6} <= 1) under sampling error (MC)
    killer_fires: bool           # alpha*_{5->6} <= 1 (gauge-dependent leverage)
    passes: bool                 # gauge-invariant peak AND alpha*_{5->6} > 1 robustly


def _alpha_star(diff_lo: float, base_lo: float, diff_hi: float, base_hi: float) -> float:
    """The exponent alpha at which L_alpha(hi) == L_alpha(lo); nan if base is unchanged."""
    import math
    B = math.log(base_hi / base_lo)
    if B == 0.0:
        return float("nan")
    return math.log(diff_hi / diff_lo) / B


def leverage_gauge(rows: Sequence[CrossLevelRow], H_target: float,
                   alpha_grid: Sequence[float] = (0.0, 0.25, 0.5, 0.75, 1.0),
                   mc: int = 200000, base_M: int = 6000,
                   seed: int = 0) -> GaugeVerdict:
    """Settle Module 24's gauge flag on a CONSISTENT iso-hardness series (Module 27).

    Given the three iso-hardness ``CrossLevelRow`` (n=4 exact, n=5,6 sampled CRN) for one
    H slice, decide whether the cross-level trend of ``L_alpha(n) = diff/base**alpha`` is
    the SAME for every natural normalization ``alpha in [0,1]``.  Returns the per-pair
    endpoint trends + flip exponent, the argmax level per alpha on a grid, the decisive
    ``alpha*_{5->6}`` with a Monte-Carlo propagation of the n=5,6 sampling error
    (``p_killer`` = P(alpha*_{5->6} <= 1)), and the PASS/killer verdict.  No new sampling
    of the meta-function: this is an exact post-analysis of the frozen rows."""
    import math
    by_n = {r.n: r for r in rows}
    ordered = sorted(by_n)
    pairs: List[GaugePair] = []
    for lo, hi in zip(ordered, ordered[1:]):
        rl, rh = by_n[lo], by_n[hi]
        pairs.append(GaugePair(
            n_lo=lo, n_hi=hi,
            delta_abs=math.log(rh.diff_prob / rl.diff_prob),
            delta_rel=math.log(rh.rel / rl.rel),
            alpha_star=_alpha_star(rl.diff_prob, rl.base_prob, rh.diff_prob, rh.base_prob)))
    # peak (argmax) level for each alpha on the grid
    peak: dict = {}
    for a in alpha_grid:
        vals = {n: by_n[n].diff_prob / by_n[n].base_prob ** a for n in ordered}
        peak[a] = max(vals, key=vals.get)
    invariant = (len(set(peak.values())) == 1) and all(p.same_sign for p in pairs)
    # the decisive pair: 5->6 (or the top pair if n=6 absent)
    top = pairs[-1]
    astar = top.alpha_star
    # Monte-Carlo propagation of the n=5,6 sampling error onto alpha*_{5->6}
    rl, rh = by_n[top.n_lo], by_n[top.n_hi]
    rng = random.Random(seed)
    def _bse(p: float) -> float:                       # binomial se of a base_prob count
        return (p * (1 - p) / base_M) ** 0.5
    fires = 0
    valid = 0
    for _ in range(mc):
        dl = rl.diff_prob if rl.exact else rng.gauss(rl.diff_prob, rl.se_prob)
        dh = rh.diff_prob if rh.exact else rng.gauss(rh.diff_prob, rh.se_prob)
        bl = rl.base_prob if rl.exact else rng.gauss(rl.base_prob, _bse(rl.base_prob))
        bh = rh.base_prob if rh.exact else rng.gauss(rh.base_prob, _bse(rh.base_prob))
        if dl <= 0 or dh <= 0 or bl <= 0 or bh <= 0:   # log undefined -> skip degenerate draw
            continue
        valid += 1
        a = _alpha_star(dl, bl, dh, bh)
        if a == a and a <= 1.0:                        # a==a excludes nan (base unchanged)
            fires += 1
    p_killer = fires / valid if valid else 1.0
    killer = (astar != astar) or astar <= 1.0
    return GaugeVerdict(
        H_target=H_target, pairs=pairs, peak_n_by_alpha=peak,
        gauge_invariant_peak=invariant, alpha_star_5_6=astar,
        p_killer=p_killer, killer_fires=killer,
        passes=invariant and (not killer) and p_killer < 0.01)


def leverage_gauge_table(H_target: float = 0.5, seeds: int = 6, M: int = 120000,
                         ns: Sequence[int] = (4, 5, 6)) -> GaugeVerdict:
    """Convenience: build the iso-hardness rows for one H slice and run ``leverage_gauge``
    (Module 27).  EXACT n=4 anchor + sampled CRN n=5,6, then the exact gauge post-analysis."""
    rows = [iso_hardness_row(n, H_target=H_target, seeds=seeds, M=M) for n in ns]
    return leverage_gauge(rows, H_target=H_target)


def honesty_note() -> str:
    """One-paragraph honesty boundary (string; no asymptotic claim)."""
    return (
        "ESTIMATED, not computed: at n=5 (N=32, 2^32 truth tables) the exact sweep is "
        "infeasible, so the n=5 pair-influence difference is a Monte Carlo estimate "
        "with a 99% CI (CRN estimator), validated by the exact n=4 anchor.  COMPUTED "
        "exactly: min_obdd_size (O(N) per table) and the full n=4 ground truth.  The "
        "faithful certified wall (~0.23% at n=4) is BEYOND this sampling budget and is "
        "NOT estimated.  CITED, never computed: the asymptotic magnification / locality "
        "theorems (Oliveira-Pich; Chen-Jin-Williams; CHRSV).  No separation, no P vs NP "
        "claim — this measures whether ONE order-anisotropy survives one level up."
    )
