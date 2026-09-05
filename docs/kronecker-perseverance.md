# Kronecker Perseverance Run — Entries 62–70

*Crystallized 2026-09-05. This document records the second phase of the GCT / Kronecker
arc (Entries 62–70 of the RESEARCH_LOG), which follows Module 30 (`gct-kronecker.md`)
and constitutes the lab's deepest dive into representation-theoretic computation. No
lower bound is proved. No claim about P vs NP, Kronecker positivity, or GCT obstructions
is made. All conjectures are empirical on short series; no asymptotic claim is proved.*

---

## 1. Genericness ratio R = g · d! / f³ on self-conjugate shapes

### Setup

For a partition λ ⊢ d that is self-conjugate (λ = λ'), the **diagonal Kronecker
coefficient** is g(λ, λ, λ). The **genericness ratio**

```
R(λ) = g(λ, λ, λ) · d! / f(λ)³
```

(where f(λ) = dim V_λ = hook-length dimension) measures how much the diagonal
coefficient deviates from a Haar-random expectation (the Weingarten value f(λ)³ / d!).
R = 1 is "generic"; R → 0 is "degenerate"; R → ∞ is "super-concentrated".

Regenerate all R-values:

```
$env:PYTHONPATH=(pwd)
py -c "
from pnp_lab.gct_kronecker.fast import g_fast
from pnp_lab.gct_kronecker.kronecker import hook_length_dimension
from math import factorial
shapes = [
    (1,),(2,1),(3,2,1),(4,3,2,1),(5,4,3,2,1),(6,5,4,3,2,1),  # staircases
    (2,2),(3,3,3),(4,4,4,4),(5,5,5,5,5),                       # squares
    (4,1,1,1),(6,1,1,1,1,1),(7,1,1,1,1,1,1),                  # hooks
]
for lam in shapes:
    d = sum(lam); f = hook_length_dimension(lam)
    g = g_fast(lam,lam,lam)
    R = g * factorial(d) / f**3
    print(lam, d, g, f'{R:.4f}')
"
```

### Spectrum d = 10..21 (Entry 62–64)

**Staircase δ_k = (k, k−1, …, 1)** [Entry 62, regenerate: g_fast on δ_k, k=1..6]:

| k | d  | f          | g(δ_k³) | R_staircase |
|---|----|------------|---------|-------------|
| 1 | 1  | 1          | 1       | 1.0000      |
| 2 | 3  | 2          | 1       | 0.7500      |
| 3 | 6  | 16         | 5       | 0.8789      |
| 4 | 10 | 768        | 117     | 0.9373      |
| 5 | 15 | 292 864    | 18 269  | 0.9511      |
| 6 | 21 | 1 100 742 656 | 24 891 165 | 0.9535 |
| 7 | 28 | (wall)     | —       | —           |

**Square (k^k)** [Entry 62, same command with lam=(k,)*k]:

| k | d  | f          | g((k^k)³) | R_square |
|---|----|------------|-----------|----------|
| 2 | 4  | 2          | 1         | 3.0000   |
| 3 | 9  | 42         | 1         | 4.8980   |
| 4 | 16 | 24 024     | 5         | 7.5449   |
| 5 | 25 | 701 149 020 | 21       | 0.9450   |

**Full d = 21 self-conjugate spectrum** [Entry 64; regenerate:
`$env:PYTHONPATH=(pwd); py examples/run_crossing.py` prints R for d=21 shapes]:

| λ                     | f            | g          | R       | hooks   |
|-----------------------|--------------|------------|---------|---------|
| (11, 1^{10})          | 184 756      | 1          | 8101.18 | {21}    |
| (9,3,3,1,1,1,1,1,1)  | 59 643 584   | 8 013      | 1.9295  | {17,3,1}|
| (8,4,3,2,1,1,1,1)    | 570 341 772  | 3 759 213  | 1.0352  | {15,5,1}|
| (7,5,3,2,2,1,1)      | 1 118 939 184 | 27 329 601| 0.9967  | {13,7,1}|
| (7,4,4,3,1,1,1)      | 609 339 500  | 4 420 601  | 0.9983  | {13,5,3}|
| (6,6,3,2,2,2)        | 276 529 344  | 411 081    | 0.9932  | {11,9,1}|
| (6,5,4,3,2,1) = δ_6  | 1 100 742 656| 24 891 165 | 0.9535  | {11,7,3}|
| (5,5,5,3,3)           | 69 283 500   | 5 453      | 0.8377  | {9,7,5} |

### Trichotomy (Entries 62–64)

Three qualitatively distinct behaviours emerge, all empirical on d ≤ 28:

| Type            | g behaviour       | R behaviour | Structural cause (conjectured)        |
|-----------------|-------------------|-------------|---------------------------------------|
| Hook (a, 1^{a−1}) | g = 1 constant | R → ∞       | f exponentially small; g wins         |
| Square (k^k)   | g ~ φ^{3k} (C53)  | R → 0       | row-column symmetry suppresses g      |
| Staircase δ_k  | g ~ f³/d! (C57)   | R → 1       | maximally irregular, Weingarten-generic |

**L63 (Lemma, Entry 63):** R_hook(a) → ∞ as a → ∞.  
Proof sketch: hook (a, 1^{a−1}) has d = 2a−1, f = C(2a−2, a−1) ~ 4^a / √(πa),
g = 1. Stirling gives log R_hook ~ 2a log a − 4a log 2 → +∞. Verified: R = 7.89
at d = 13, R = 32.35 at d = 15, R = 8101 at d = 21.

**L62 (Lemma, conditional, Entry 62):** If C53 holds (g((k^k)³) = F(3k−7), Fibonacci),
then R_square(k) → 0 as k → ∞. Proof sketch: Fibonacci grows as φ^{3k} (exponent
3 log φ ≈ 1.44 per step in k); log f^{(k^k)} grows quadratically in k (Stirling on
hook-length), so the quadratic term dominates and R_square → 0. Conditional: C53 is
verified only for k = 2..5 (d = 4..25).

**C57 (Conjecture, Entry 62):** lim_{k→∞} g(δ_k³) · d! / f³ = 1.  
Basis: 5 data points with R = 0.75, 0.88, 0.94, 0.95, 0.95 (monotone; Δ at k=5→6
is only 0.0024). Not verified: k = 7 requires d = 28 > HOOK_MAX_D = 27 (wall).

### C60: hook-spread predicts R (Entry 64)

**Observation (Entry 64):** Among k-hook self-conjugate shapes at fixed d and fixed k,
R is monotone increasing in the normalized hook-spread (h_1 − h_r) / d.

Evidence (k = 3 only; k ≥ 4 not tested):

```
d=15: spread 0.667 → R=0.9924; spread 0.533 → R=0.9511; spread 0.267 → R=0.8488
d=13: spread 0.615 → R=1.0019; spread 0.462 → R=0.8380
d=21: spread 0.762 → R=1.9295; spread 0.667 → R=1.0352; ...; spread 0.190 → R=0.8377
```

Regenerate: `$env:PYTHONPATH=(pwd); py examples/run_crossing.py` (prints d=21 spectrum).

**C60 (Conjecture, Entry 64):** R is monotone in (h_1−h_r)/d among k-hook shapes at
fixed (d, k). Killer declared: a pair (λ, μ) with same d and k, spread(λ) > spread(μ),
but R(λ) < R(μ). Verified for k = 3 only (d = 13, 15, 21). k ≥ 4 lies beyond
computable instances in this corpus.

Note: {13,5,3} and {11,9,1} at d=21 share spread = 10/21 = 0.476 (tie); their R
values differ by 0.005, which C60 does not order — spread alone is insufficient for
tied pairs.

---

## 2. Crossing s*(d): H65 killed — ramo CHIUSO (Entry 65)

**Hypothesis H65 (Entry 65):** The R = 1 crossing point s*(d) (interpolated linearly
among 3-hook self-conjugate shapes ranked by hook-spread) converges inside a fixed band
[0.50, 0.65] with |Δs*| strictly decreasing as d grows.

**Measurement** [Entry 65; regenerate: `$env:PYTHONPATH=(pwd); py examples/run_crossing.py`]:

```
d=13:  s*=0.6136  R_min=0.8380  R_max=1.0019
d=15:  s*=none    (R_max<1)
d=21:  s*=0.5796
d=23:  s*=0.6043
d=25:  s*=0.5600
d=27:  s*=0.5185
|Δs*|: 13→21: 0.0340; 21→23: 0.0247; 23→25: 0.0443; 25→27: 0.0415
```

**Killer fired.** |Δs*| is not monotonically decreasing (0.0247 at 21→23 rises to
0.0443 at 23→25). s*(27) = 0.5185 falls below the declared band minimum of 0.50.

**Verdict: ARTEFATTO.** H65 falsified and withdrawn (F65). The adversary identified
five independent failure modes:

1. Grid under-resolution: the d-spacing (2–6 units) gives |Δs*| ~ 0.025, only 2–3×
   above the sampling noise.
2. Linear interpolation of R(spread) unjustified: R is a rational function (Fraction)
   of f and g, not linear in spread.
3. Band [0.50, 0.65] fixed post-hoc on d = 13/21 only; loses validity at d ≥ 23.
4. Killer derived from same data as hypothesis: confirmation bias loop.
5. The "crossing" is a reparametrization of C57/trichotomy, not an independent
   phenomenon; Entry 62–64 already implied it.

**Evaluator: 3/10.** Flags: off-tiny-instance, overfitting, circularity,
confirmation-bias, unfalsifiable-here. Ramo crossing CHIUSO. The infrastructure
(`crossing.py`, `tests/test_crossing.py`, `examples/run_crossing.py`) is retained as
QA scaffolding for R-value verification, not as a live conjecture.

---

## 3. F68: C52 falsified out-of-sample (Entry 68)

**C52 (Entry 52, now FALSIFIED):** g((c^2)³) = ((c−1)/2)² for odd c. Verified at
c = 1, 3, 5 (g = 0, 1, 4).

**F68 (Entry 68):** g((7, 7, 7, 7)³) = **21** (d = 28, exact, g_fast, 400 s; confirmed
independently twice). C52 predicts ((7−1)/2)² = 9. 21 ≠ 9: **C52 killed.**

Regenerate (slow, ~400 s):

```
$env:PYTHONPATH=(pwd)
py -c "from pnp_lab.gct_kronecker.fast import g_fast; print(g_fast((7,7,7,7),(7,7,7,7),(7,7,7,7)))"
```

**Odd series now open:** g((c^4)³) for odd c = 1, 3, 5, 7: **[0, 1, 4, 21]**.
Differences: 1, 3, 17. No degree-2 fit. This is an observation, not a finding.

**Coincidence noted, not claimed:** 21 = g((5^5)³) (C53, d = 25) = F(8) = C(7,2) = T(6).
Two equal g-values at different d and different shapes. Not asserted as a structural law:
21 is a common integer appearing in many combinatorial contexts. A connection would
require external theory (plethysm / Murnaghan / Rosas / Pak–Panova).

**What survives:** C53 (g((k^k)³) = F(3k−7) for k = 2..5), C49, C50, C51 are
unaffected; F68 kills only the c^4 odd formula. Ehrhart quasi-polynomial asymptotics
(Rosas / prior art) are untouched.

---

## 4. L60 — machine-certified Lean 4 proof (Entry 69)

**L60 (Lemma, Entry 60; ERRATUM E69; certified Entry 69):** The sequence s₃(k) does
NOT satisfy any linear recurrence of order 2 with integer coefficients.

Formal statement (certified in Lean 4, zero sorry):

```
¬ ∃ a b : Int,
    (158 : Int) = 14 * a + 2 * b ∧
    (1497 : Int) = 158 * a + 14 * b
```

Proof: eliminating b reduces to 60·a = 391; since 60 ∤ 391 (391 = 6·60 + 31), no
integer solution exists. The rational solution a = 391/60 exists — so the certificate
proves genuine non-integrality, not vacuity.

Source values used:

```
s₃(1) = 2    (corrected by E69; Entry 60 erroneously used 1 = pre-stable plateau)
s₃(2) = 14
s₃(3) = 158
s₃(4) = 1497
```

Regenerate s₃ values (fast):

```
$env:PYTHONPATH=(pwd)
py -c "from pnp_lab.gct_kronecker.fast import g_fast; print([g_fast((a,3),(a,3),(a,3)) for a in range(6,13)])"
```

Expected: [2, 2, 2, 2, 2, 2, 2] (s₃(1) = 2, stable for a ≥ 6).

**Build:** `cd formalization && lake build` — exit code 0 (13 jobs compiled).  
**Axiom check:** `lake env lean Check.lean` — axioms: `[propext, Quot.sound]`, zero
`sorry`, no `Classical.choice`.

**Source:** `formalization/PvsNP/Kronecker.lean` — theorems
`s3_no_order2_recurrence` and `s3_no_order2_recurrence_named`.

**ERRATUM E69:** Entry 60 originally used s₃(1) = 1 (the pre-stable plateau at a = 4, 5).
The stable limit is s₃(1) = 2, declared in Entry 49 and reconfirmed here. L60 holds
with both values (38·a = 715 with the old value; 60·a = 391 with the corrected value;
neither has an integer solution). The Lean file formalises the corrected system.

**Honest limits:** L60 excludes only order-2 integer linear recurrences on the four
empirical values. It says nothing about higher-order recurrences, non-linear structure,
or asymptotic behaviour of s₃.

---

## 5. ERRATUM-HUNT protocol (Entry 70)

### Protocol

`pnp_lab/gct_kronecker/audit.py` provides a **declarative corpus** of 68 entries:
all Kronecker g-values hardcoded in STATE.md (conjectures C49–C54, staircase series,
s₃ values). `audit_all()` runs g_fast on each entry with d ≤ 24 and compares.

Regenerate the full audit (~120 s):

```
$env:PYTHONPATH=(pwd)
py -m examples.run_audit
```

**Results (Entry 70):**

```
60 MATCH       (hardcoded = computed by g_fast)
 1 MISMATCH    (C51 k=5: stated=2, computed=1)  → ERRATUM E70
 6 NON-AUDITED (d > 24: C51 k=8,9; s₃(5,6); C54 speculative)
 1 AMBIGUOUS   (C54 s₃(5)=10826, wall-limited, correctly marked speculative)
───────────────
68 total
```

### ERRATUM E70 (Entry 70)

**C51 k=5 correction:** g((3^5)³) = **1**, not 2 (as stated in STATE.md).

Corrected g((3^k)³) for k = 1..8:

```
k=1: 1  k=2: 0  k=3: 1  k=4: 1  k=5: 1  k=6: 1  k=7: 0  k=8: 1
Series: [1, 0, 1, 1, 1, 1, 0, 1, ...]
```

Regenerate (fast):

```
$env:PYTHONPATH=(pwd)
py -c "from pnp_lab.gct_kronecker.fast import g_fast; print([g_fast((3,)*k,(3,)*k,(3,)*k) for k in range(1,9)])"
```

Expected: [1, 0, 1, 1, 1, 1, 0, 1].

**C51 survives:** "g((3^k)³) = 0 iff k ≡ 2 (mod 5)" — zeros at k = 2, 7 confirmed.
E70 corrects only the value at k = 5 (1, not 2); the pattern is unaffected and the
corrected series is in fact cleaner.

### Track record

Three ERRATUM-HUNT iterations, three errata:

| Hunt | Entry | Erratum |
|------|-------|---------|
| 1    | F64 (Entry 64) | 5 non-self-conjugate shapes in Entry 63 table; 3 shapes missing |
| 2    | E69 (Entry 69) | s₃(1) = 1 → 2 in Entry 60 (pre-stable plateau used as stable value) |
| 3    | E70 (Entry 70) | C51 k=5: g = 2 → 1 |

### Residual circularity (declared, Entry 70)

g_fast is cross-validated against `kronecker()` (the reference character-sum engine)
only for d ≤ 7. For d = 8..24, both engines share the same `character_table`
implementation; no independent third source (SageMath, Stembridge) was used. This
residual circularity is declared and mitigated — but not eliminated — by:

- Anchors at d ≤ 7 (two independent engines agree);
- Known-family shapes (hooks, rectangles, two-row) cross-checked against Rosas /
  Bessenrodt–Bowman formulas;
- The error found by E70 (a mismatch of 1 vs 2) is consistent with a transcription
  error, not a systematic engine bug.

---

## Honesty boundary (complete)

| Claim category | Status |
|----------------|--------|
| All g-values in this document | COMPUTED exactly (Murnaghan–Nakayama, integer arithmetic, `Fraction` assert) |
| L60 (no ord-2 recurrence) | CERTIFIED by Lean 4 kernel (axioms: propext, Quot.sound; zero sorry) |
| L62 (R_square → 0) | PROVED conditionally on C53; C53 is empirical (k=2..5 only) |
| L63 (R_hook → ∞) | PROVED by Stirling (leading term only; sub-leading terms not bounded) |
| C53 (g((k^k)³) = F(3k−7)) | CONJECTURE — verified k=2..5 (d=4..25); not verified k=6 (d=36, beyond wall) |
| C57 (R_staircase → 1) | CONJECTURE — 5 data points; not verified k=7 (d=28, at wall) |
| C60 (hook-spread monotone) | CONJECTURE — verified k=3 only; k≥4 not reached in this corpus |
| C49, C50, C51 | CONJECTURE — empirical on c ≤ 13 or k ≤ 9 respectively |
| Series [0,1,4,21] (odd c^4) | OBSERVATION — no formula claimed; 4 data points |
| Double-21 coincidence (C53 vs F68) | NOTED — not claimed as a structural law |
| s₃ series [2,14,158,1497] | COMPUTED (g_fast); upper terms speculative/non-audited |
| Asymptotic of g((c^4)³) (Ehrhart) | CITED (Rosas / prior art) — not computed here |
| Cross-validation d=8..24 | SINGLE ENGINE (residual circularity declared) |
| Claim about P vs NP | NONE |
| Claim about Kronecker positivity | NONE |
| Claim about GCT obstructions | NONE |
| Asymptotic claim (any) | NONE (all asymptotic statements are conjectures or conditional lemmas) |

All conjectures C49–C60 are **empirical observations on series of length ≤ 9**.
None is promoted to a theorem. The lab's wall is d ≤ 27 (HOOK_MAX_D) for fast
computation and d ≤ 24 for the full audit.

---

## Infrastructure produced (Entries 62–70)

| File | Function |
|------|----------|
| `pnp_lab/gct_kronecker/crossing.py` | Enumerate SC 3-hook shapes; compute R (exact Fraction); interpolate s*(d). H65 killed; kept as QA tool |
| `pnp_lab/gct_kronecker/audit.py` | 68-entry declarative corpus; `audit_all()` verifies g_fast vs stated values |
| `formalization/PvsNP/Kronecker.lean` | Lean 4 certificate for L60; axioms propext + Quot.sound; zero sorry |
| `tests/test_crossing.py` | 18 fast + 8 slow tests for crossing.py |
| `tests/test_audit.py` | 4 fast + 2 slow tests for audit.py |
| `examples/run_crossing.py` | Driver for H65 / R-spectrum |
| `examples/run_audit.py` | Driver for full audit (~120 s) |

Pre-existing infrastructure (Entries 40–61):

```
pnp_lab/gct_kronecker/fast.py           (g_fast, HOOK_MAX_D=27)
pnp_lab/gct_kronecker/coverage.py       (covered, sporadic_vanishing)
pnp_lab/gct_kronecker/hook_depth.py     (C42/C44/C45/C47 callable)
pnp_lab/gct_kronecker/diagonal_census.py (STRETCH_MAX_D=24)
tests/test_hook_depth.py                 (56 fast + 12 slow)
examples/run_hook_depth.py
```
