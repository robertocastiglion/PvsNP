# Module 29 — Approximate Degree: the 6th-arena collapse (incomparable with cost, inside the joint dictionary)

*Crystallized 2026-06-20. Opened by the autonomous strategist after the three classic
barriers were exhausted (Module 28), as the arena most distant from the five already
collapsed. RESTATEMENT-of-known — but a richer one: approximate degree is **incomparable
with formula-size cost alone**, yet **reconstructible from the lab's joint orbit-invariant
dictionary** on n=3. It proves no lower bound and makes **no claim about P vs NP**. It is
the 14th collapse, in a 6th independent arena, and it sharpens the [Collapse
Theorem](collapse-theorem.md).*

## The object (exact, new arena)

`adeg_{1/3}(f)` = the minimum degree of a real polynomial approximating `f` to error `1/3`
on every Boolean input — a genuine complexity measure (the **polynomial method**, exact
lower bounds for quantum query complexity). The lab had never touched it. It is computed
here **exactly** via LP duality (the **dual polynomial**), reusing the rational simplex of
`pnp_lab/exactness_composes/gap.py`:

```
E_d(f) = max_ψ  Σ_x ψ(x) f(x)   s.t.  Σ_x |ψ(x)| ≤ 1,  ψ ⟂ every monomial of degree ≤ d
adeg_{1/3}(f) = min { d : E_d(f) ≤ 1/3 }
```

This form is origin-feasible (all `b ≥ 0`), so the existing primal simplex solves it.
Anchors verified exactly: parity has full degree `adeg = n`; constants `0`; a dictator `1`;
`E_d` is monotone non-increasing in `d` and `E_n = 0`.

## The decisive measurement (exhaustive n=3, 256 functions)

`adeg` distribution: `{0: 2, 1: 102, 2: 134, 3: 18}`.

**`adeg` is incomparable with formula-size `cost` (Module 6) — a genuine, non-trivial
fact.** Neither refines the other:

| cost | adeg values at that cost |
|------|--------------------------|
| 1 | {0, 1} |
| 4 | {1, 2} |
| 3 | {2} |
| 7, 9 | {3} |

So `adeg` separates functions of *equal* formula size — unlike every prior σ(cost)-arena
cycle, it does **not** reduce onto `cost`. This is the first exactly-computable invariant
the lab found that lives **outside** the σ(cost) dictionary.

**But it collapses into the JOINT dictionary.** Tested against the joint of the lab's
existing orbit-invariants — `(cost, gf2_degree, sensitivity, block_sensitivity)` — every
signature maps to a **single** `adeg` value (`adeg_vs_dictionary(3)` → `reconstructible =
True`, `splits = []`): `adeg` separates **no** pair on which those four agree. It adds zero
discriminating power over the dictionary the lab already had.

## Verdict — RESTATEMENT-of-known, the 6th-arena collapse

`adeg` is a **parent-known measure** (textbook approximate degree / quantum query lower
bounds), exactly computed, that is incomparable with `cost` alone yet reconstructible from
the joint orbit-invariant dictionary at n=3. It is therefore **not new content** toward a
separation. The honest refinement it adds to the [Collapse Theorem](collapse-theorem.md):
the "dictionary" that absorbs every tiny-instance measure is not merely σ(cost) — it is the
**joint** of a few orbit-invariants, and a measure from a fully orthogonal arena (the
polynomial method) still falls inside that joint. Six independent arenas, 14 collapses (plus
the one non-collapse of Module 22, broken only by abandoning permutation-invariance, not by
a new scalar).

## Honesty boundary

COMPUTED exactly (rational LP, `Fraction`): `adeg_{1/3}(f)` for every function on n ≤ 3 via
the dual-polynomial LP; the incomparability with `cost`; the reconstruction from
`(cost, gf2_degree, sensitivity, block_sensitivity)`. CITED, never re-proved: the polynomial
method / quantum-query lower bounds, Paturi's symmetric-function formula. NOT shown: any new
separating content — `adeg` is a known invariant inside the joint dictionary at this size.
Tiny-instance only (n ≤ 3 exhaustive; n = 4 is `2^16` LPs, out of this cycle's scope).
**No separation, no P vs NP claim.**
