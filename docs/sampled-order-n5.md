# Module 24 — Sampled Order-Anisotropy at n=5 (the lab's first cross-level PASS)

**Verdict: PASS, qualified — the lab's FIRST non-collapsing outcome that also
survives a level.** The order-anisotropy of `MBPSP[s]` found *exactly* at n=4 in
[Module 22](order-locality.md) is shown, by Monte-Carlo estimation, to survive one
level up to **n=5** (`N = 2^5 = 32`, `2^32` truth tables — infeasible to enumerate).
The pre-declared killer does **not** fire. The ceiling is stated as sharply as the
result: **survival, not leverage** — no monotone cross-level amplification is
established, and the asymptotic magnification theorems stay CITED. No P vs NP claim.

## Why this module exists

Module 22 produced the lab's only non-collapsing outcome but at a **single** level
(n=4); [Module 23](certified-bounds.md) then proved a wall invariant cannot be made
cheap per-instance (it is irreducibly a statistic over the *set* of all functions,
so reintroducing the set brings the `2^(2^n)` sweep back). Both closures shared the
same computational wall: *exact* enumeration on tiny instances.

This module makes the lab's own thesis — **"exactness is the trap"** — into a method:
it **spends** exactness to gain reach. Both Module-22 statistics are *sums of
indicators over the uniform meta-input space* `t ∈ {0,…,2^N−1}`:

```
pair_influence(d) = Σ_t [ MBPSP[s] non-constant on {t, t^e0, t^ed, t^(e0^ed)} ].
```

A sum of indicators over a uniform space is exactly what Monte Carlo estimates, and
`min_obdd_size` is `O(N)` per truth table — the same cheapness Module 23 noted for a
*single* function, now harnessed to estimate the *set* statistic. We recover the wall
invariant Module 23 could not, paying in a confidence interval instead of an exact
integer.

## The estimator — Common Random Numbers (CRN)

Resolving a ~0.3–4% difference between two counts of size ~`2^32` by differencing two
*independent* estimates is hopeless. Instead the **same** random base points `t` are
used for `d_hi` and `d_lo`, averaging the per-sample difference
`D(t) = I_{d_hi}(t) − I_{d_lo}(t) ∈ {−1,0,1}`. The two indicators share two of the
four cube corners (`t`, `t^e0`), so `Var(D)` is small and the standard error of the
difference shrinks far faster than that of either count. This is what makes the small
signal resolvable.

## Three guards against self-deception

1. **Fidelity anchor at n=4.** The sampler must reproduce the *exact* known
   `pair_influence` difference (`4056 − 3872 = 184`) inside its 99% CI. **Validated**
   (`anchor_n4`, deterministic at seed 0).
2. **Pre-registered pair, not max-min.** The max-min "spread" is an extreme-value
   statistic biased *positive* by sampling noise (the artifact that killed Cycle 1's
   `ρ=1` band). We test ONE pair fixed by the n=4 order structure: weight-1 **top
   variable vs bottom** (n=5: `d_hi = 16 = x4`, `d_lo = 1 = x0`).
3. **Null control.** A permutation-invariant, equally-cheap meta-function
   (`popcount(t) > s`) under the SAME CRN estimator must return a difference
   consistent with 0 (it is provably 0 by symmetry — tested exactly at n=4). The MCSP
   formula-size control of Module 21/22 is **not** samplable (min formula size of one
   32-bit function is not cheap); popcount is the cheap stand-in.

**Pre-declared killer.** At n=5: if the pooled CRN difference's 99% CI *includes* 0,
the killer FIRES (anisotropy not resolvable across levels; Module 22's n=4 effect not
shown to persist). PASS only if the pre-registered pair differs significantly **and**
the null control stays consistent with 0.

## Measured

A single 400k-sample run is unstable (`z` bounced from −0.65 at 80k to +3.3 at 1.2M,
same seed), so the robust statement **pools independent seeds** by inverse variance
and checks sign consistency.

| stage | result |
|---|---|
| **Anchor** (n=4, exact in CI) | **PASS** (exact 184 ∈ 99% CI) |
| **Signal** (n=5, s=10, pair x4 vs x0, 8 seeds × 300k) | diff prob ≈ **+1.7e-4**, pooled **z ≈ +4.9**, 99% CI excludes 0, **7/8 seeds positive** |
| **Null control** (popcount, same pair) | pooled ≈ 0, not significant |
| **Killer** | does **not** fire → **PASS** |

The order-anisotropy of `MBPSP[s]` **survives** from n=4 to n=5 — the first time a
measured quantity in this lab clears a level instead of collapsing onto a known
object. Replicated three times independently.

## The ceiling — survival, not leverage

Two facts, both measured, bound the claim:

**1. The cross-level trend is normalization-dependent.** The *absolute* pair-influence
difference DECAYS (n=4 `4.9e-4` → n=5 `1.4e-4`, same pre-registered pair), while the
difference *relative to the boundary base rate* GROWS (`0.8%` → `3.7%`). No canonical
"leverage" emerges — the sign of the trend depends on the (arbitrary) normalization.

**2. The faithful threshold regime degenerates at n≥6.** Under Module 22's policy
`s = round(0.5·max)`, random OBDD sizes concentrate near the maximum, so the boundary
the estimator reads vanishes:

| n | OBDD size min/median/max | s | base_prob (boundary) |
|---|---|---|---|
| 4 | 3 / 10 / 11 | 6 | 6.1e-2 (alive) |
| 5 | 11 / 16 / 19 | 10 | 3.7e-3 (thin) |
| 6 | 20 / 26 / 31 | 16 | **0** (sample min > s → constant-HARD) |
| 7 | 36 / 44 / 47 | 24 | **0** |

So the sampling pivot buys **exactly one level** over Module 22's exact n=4. No
monotone leverage is established; the asymptotic amplification (small LB → separation)
remains CITED. Same "regime degenerates / wall returns" pattern as the rest of the
lab — but reached one level deeper than exact methods, with the first PASS at that
level.

## Honesty boundary

ESTIMATED, not computed: the n=5 pair-influence difference (Monte Carlo, 99% CI, CRN),
validated by the exact n=4 anchor. COMPUTED exactly: `min_obdd_size` (O(N) per table),
the full n=4 ground truth, the popcount control's exact-0 difference, the threshold-
regime table. NOT measured: the faithful certified wall (~0.23% at n=4) is beyond this
sampling budget; any n≥6 point under the faithful policy (degenerate). CITED, never
computed: the magnification / locality theorems (Oliveira–Pich 2019; Chen–Jin–Williams
2019/2020; Chen–Hirahara–Ren–Santhanam–Vyas). No separation, no P vs NP claim — this
measures whether one order-anisotropy survives one level up, and it does, while no
cross-level leverage is shown.

Files: `pnp_lab/meta_complexity/sampled_order_n5.py`, `tests/test_sampled_order_n5.py`,
`examples/run_sampled_order_n5.py`.
