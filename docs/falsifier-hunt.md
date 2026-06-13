# Falsifier Hunt — testing the μ_R dictionary for completeness (Cycle 6)

**Scope / honesty boundary first.** This is a statement about the *method* of the
research loop on *finite* instances (n ≤ 4 Boolean functions). It is **NOT** a claim
about P vs NP. Everything below is exact and deterministic (integers / `Fraction`, no
floats).

## Where this comes from

The autonomous research loop closed at Module 19 ("Tiny-Instance Collapse",
`RESEARCH_LOG.md` Entry 7) on a meta-conclusion: on n ≤ 4, every local discriminant
built so far reduces, via an exact code-verified identity, to an invariant already in
the dictionary μ_R (cover-LP / proof-complexity / KT). The single declared rule for
restarting was:

> restart only on an out-of-dictionary direction, with the **falsifier declared in
> advance** — a discriminant on n ≤ 4 that separates two functions of equal MCSP-size
> **and** equal cover-LP/G★ and is **not** reconstructible from `cost` nor from μ_R.

Until now `collapse.py::falsifier_status` only *assumed* (without searching) that the
rest of the toolbox was already dictionarized. This cycle closes that hole with a
**systematic, exact search**, and in doing so forces μ_R to be made explicit.

## The test (a finite, decidable question)

Make μ_R a finite **generator set** of invariants, all invariant under the group of
**cost automorphisms** B_n± = (input permutations) × (input negations) × {id, output
negation}. Let `P_Σ` be the partition of all functions by their joint dictionary
vector, and `P_orbit±` the partition by B_n± orbit. Because every generator is
B_n±-invariant, **`P_orbit±` always refines `P_Σ`**, i.e. `|P_Σ| ≤ |P_orbit±|`. Then:

> a structural falsifier EXISTS ⇔ some class of `P_Σ` splits into ≥ 2 orbits — two
> functions identical on the *entire* dictionary but in different orbits (separable
> only by an out-of-dictionary invariant).

- `P_Σ == P_orbit±` → the dictionary determines the function up to symmetry: **no
  falsifier possible**, collapse hardened to a quasi-theorem on this instance size.
- `P_Σ` strictly coarser → a concrete pair (f, g) = falsifier candidate.

**Legitimacy guard (this caught a real bug):** any candidate separating invariant we
add must keep `|P_Σ| ≤ |P_orbit±|`. If adding it makes `|P_Σ| > |P_orbit±|`, the
"invariant" is **not** B_n±-invariant — it splits *within* orbits, and the resulting
`#splits = 0` is **vacuous** (zeroed by over-refinement, not by collapse).

## Results

### n = 3 (256 functions) — the dictionary must be closed under two symmetries
- NAIVE (group B_n, base dictionary, no support) → 8 splits: looks like a falsifier.
- B_n± (add output negation to the group) → 1 residual split: the pair (24, 30).
- CORRECT (B_n± + folded support-size) → **0 splits**, `P_Σ == P_orbit±`: complete
  collapse. Both closures (output negation, support-size) are **necessary**.

### n = 4 (65536 functions) — the decisive case
With the **strong** 11-generator dictionary (formula-cost, DT-depth, G★ multiset, max
sensitivity, block sensitivity, gf2-degree, folded support, cover-number multiset,
fractional-cover multiset, average sensitivity, real/Fourier degree, Fourier
fingerprint) exactly **one** split survives:

```
|P_orbit±| = 222
STRONG (11 generators):  |P_Σ| = 221   #splits = 1   →  pair (2025, 5742), cost 11
```

The pair (2025, 5742) is **indistinguishable on all 11 generators** (`named_separators
= []`), both cost 11, popcount 8, DT-depth 4, sensitivity 4, block-sensitivity 4,
gf2-degree 3, real-degree 4, average-sensitivity 40, identical G★ / cover-number /
frac-cover multisets and Fourier fingerprint — yet they lie in **disjoint** B_n±
orbits (96 each), and g ≠ ¬f.

### The lone candidate is killed — inside σ(cost)

Adding a 12th generator, the **cofactor-cost profile** — the multiset over variables i
of `sorted(cost(f|xᵢ=0), cost(f|xᵢ=1))`, with `cost` the exact (n−1)-variable
formula-size — completes the collapse:

```
STRONG + cofactor (12 generators):  |P_Σ| = 222   #splits = 0   →  COLLAPSE_HARDENED
                                     |P_Σ| == |P_orbit±| == 222  (legitimate, ≤ 222)
   cofactor(2025) = {(2,7),(2,7),(5,5),(5,5)}   ≠   cofactor(5742) = {(4,5),(4,5),(4,7),(4,7)}
```

The cofactor-cost profile is **the recursion that defines formula-size itself**, so it
lives strictly inside σ(cost): the apparent escape dies to a refinement of `cost`. The
same split is killed, independently, by the **per-point sensitivity profile** (a
refinement of `sensitivity`/`average_sensitivity` already present).

### The bug the guard caught

A *naive* cofactor profile that reads cofactor costs off the **n-variable** cost table
(instead of the (n−1)-variable table) measures the cost of the embedding `g ∧ ¬xᵢ`,
which is **not** B_n±-invariant (it breaks the symmetry on xᵢ). It produced
`|P_Σ| = 243 > 222` with `#splits = 0` — a **vacuous** zero. The legitimacy guard
(`|P_Σ| ≤ |P_orbit±|`) flagged it immediately. The corrected version uses the
(n−1)-variable table and is B_n±-invariant (`|P_Σ| = 222`).

## Verdict

No genuine out-of-dictionary falsifier exists at n ≤ 4. The dictionary as originally
coded failed on exactly one pair only because it used **coarsened scalar/max/sum**
versions of its own invariants (scalar `cost`, max sensitivity, summed average
sensitivity); the natural multiset/profile refinements close the single gap, and the
decisive one is inside σ(cost). This **hardens** the Tiny-Instance Collapse
meta-conclusion (Module 19) rather than refuting it. It is the sixth consecutive
collapse-hardened / restatement-of-known outcome of the loop.

## Reproduce

```
py examples/run_falsifier_hunt.py          # n=3, the three-stage narrative (fast)
py examples/run_falsifier_hunt.py --n4      # decisive n=4 (exhaustive, slow ~40 min)
py -m pytest tests/test_falsifier_hunt.py   # fast tests incl. the (2025,5742) kill
py -m pytest tests/test_falsifier_hunt.py -m slow   # the exhaustive n=4 collapse
```
