# EXACTNESS COMPOSES (Module 18) — the killer search that resolves the post-audit conjecture

*Implemented 2026-06-04. Closes the duality-gap research arc
(`docs/duality-gap-theory.md`). This module does **not** prove a lower bound and
**does not touch P vs NP**: it builds a falsifiable conjecture on tiny instances and
**kills it**, exactly, in rational arithmetic.*

## Where this comes from

The hostile audit (Module-17 era) reduced the whole `μ_R` / `G(R)` program to a
**dictionary** over known theorems and showed its non-canonical dual makes `G` predict
nothing. The minimal repair was to **pin the dual to the explicit LP**:

> For a communication matrix `M`, let the certificate-covering IP be
> `Cov(M)` = fewest monochromatic-1 rectangles covering all 1-entries, and let
> `LP(M)` be its LP relaxation (fractional cover). Define the **canonical, computable**
> gap `G★(M) = Cov(M) − LP(M) ≥ 0`. `G★(M) = 0` iff the cover IP is integral.

This pins down a single new, falsifiable prediction:

> **EXACTNESS COMPOSES.** If `G★(R)=0` and `G★(S)=0`, then `G★(R∘S)=0` — the class of
> relations with an **integral** certificate-covering LP is closed under **gadget
> composition**.

It is *not* implied by lifting (which speaks of the *value* `μ`, with loss, and is
silent on whether the integrality *gap* stays 0), nor by KRW, the corner dualities,
resource-bounded Kolmogorov, or MCSP. So it is a genuine, testable prediction. This
module is the search for the smallest instance that kills it.

## What the search measures (exact, tiny)

Everything is exact `Fraction`: `Cov` by exact set-cover, `LP` by a rational simplex on
the **packing dual** (`max Σ yₑ s.t. each rectangle's weight ≤ 1`), whose value equals
fractional cover by LP duality. Three questions, three answers.

### (1) Does a gap even exist on tiny instances? — yes, first at 4×4

Exhaustive sweep over **all** Boolean matrices: every matrix up to **3×5** is integral
(`G★=0`). The **first** gap appears at 4×4, `G★ = 1/2`:

```
0 0 1 1
0 1 1 1
1 1 0 1
1 1 1 0      Cov = 3, LP = 5/2, G★ = 1/2
```

So the gap object is real and minuscule — the conjecture is genuinely testable.

### (2) Matrix∘matrix (Kronecker tensor) — the conjecture is TRUE, but not new

The only **well-typed** reading of "compose two integral matrices" is the tensor
`A⊗B`. Exhaustive over all integral pairs (every small matrix is integral): the tensor
is **always integral**, and `LP(A⊗B) = LP(A)·LP(B)` **exactly** on every pair. So
EXACTNESS COMPOSES *holds* here — but only as a corollary of two known facts:

```
LP(A⊗B) = LP(A)·LP(B)          (fractional cover is multiplicative — Lovász-type)
Cov(A⊗B) ≤ Cov(A)·Cov(B)       (product of covering rectangles)
Cov ≥ LP                       (LP relaxation, always)
A,B integral ⟹ LP(A⊗B)=LP(A)LP(B)=Cov(A)Cov(B) ≥ Cov(A⊗B) ≥ LP(A⊗B) ⟹ equal.
```

This is exactly the audit's prediction: where `μ_R` makes a *true* composition claim,
it is a **restatement** of LP multiplicativity. No new content.

### (3) Gadget-substitution (lifting) — the conjecture is FALSE

The composition the conjecture actually *intended* is **gadget substitution** (the
lifting `R∘S`): an outer function `f` with a gadget `g`,
`F[x,y] = f(g(x₁,y₁),…,g(x_k,y_k))`. Here the gap **opens**. Smallest counterexample:

```
f = OR₂   (query-certificate gap 0 — exact, by Tal multiplicativity)
g = XOR    (a 1-bit gadget; G★(g)=0 — every 2×2 matrix is integral)

f ∘ g²  =  the 2-bit INEQUALITY matrix  J − I₄ :

    0 1 1 1
    1 0 1 1
    1 1 0 1
    1 1 1 0

    Cov = 4,  LP = 3,  G★ = 1 > 0.
```

**Both factors are integral** (the gadget exactly; the outer function exactly in its
native query domain), **yet the lift is not**. The conjecture is **killed** on 4 bits
(2 + 2), well under the predicted ≤ 6.

#### Exact certificates for the witness

- `LP = 3`: put weight `1/2` on each of the **six** balanced `2×2` rectangles
  (`R×C`, `|R|=|C|=2`, `R∩C=∅`). Every off-diagonal cell `(i,j)` lies in exactly two of
  them, so it is covered with weight exactly `1`; total weight `6·½ = 3`. A matching
  dual of value `3` certifies optimality, so `LP = 3` **exactly**.
- `Cov = 4`: no three rectangles suffice — the 12 off-diagonal cells cannot be
  partitioned into three disjoint-side `2×2` rectangles (verified by exact set-cover).

So `G★ = 4 − 3 = 1`, and the gap is **born in the query→communication lift** — precisely
where the research note predicted it ("the killer must be sought where composition is
lossy"). The cycle-3 `Dcc = DT(f)+1` "+1" was the warning sign; this is its mechanism.

## Verdict

| reading of `R∘S` | EXACTNESS COMPOSES | why |
|---|---|---|
| matrix ⊗ matrix (tensor) | **TRUE** | corollary of `LP` multiplicativity — **not new** |
| function ∘ gadget (lifting) | **FALSE** | `OR₂ ∘ XOR = J − I₄`, `G★ = 1`, both factors integral |

The single genuinely-new prediction the minimal modification of `μ_R` could produce is
therefore **false in its intended arena and a restatement in the arena where it holds**.
This is the clean collapse the arc had been circling (AGENT SPEC §9): not vacuous, not a
breakthrough — a **falsifiable conjecture, falsified on 4 bits**.

## Honesty boundary (binding for this repo)

- This is a **falsification on tiny instances**, not a lower bound and **not** a P-vs-NP
  result. The "TRUE for tensor" half is a corollary of known LP multiplicativity, cited
  not re-derived asymptotically.
- All numbers are **exact** rationals on **minuscule** matrices (≤ 4×4 for the verdict;
  the no-gap sweep is exhaustive through 3×5). `Cov` is exact set-cover; `LP` is an exact
  rational simplex on the packing dual.
- "Integral outer function in the query domain" uses the known exactness of decision-tree
  certificate complexity under composition (Tal); the gap is contributed **only** by the
  lift, which is the point.

## Files

```
pnp_lab/exactness_composes/gap.py       # G★ = Cov − LP, exact (set-cover + rational simplex)
pnp_lab/exactness_composes/compose.py   # tensor (Kronecker) and lift (gadget substitution)
pnp_lab/exactness_composes/search.py    # the killer search + resolution()
pnp_lab/exactness_composes/lab.py       # text render
tests/test_exactness_composes.py        # exact tests
examples/run_exactness_composes.py
```
