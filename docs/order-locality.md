# Module 22 — Order-Locality (Magnification Frontier): the barrier made non-invariant

*Crystallized 2026-06-15. This **reopens and then honestly closes** the executable
Magnification Frontier program (`RESEARCH_LOG.md`, Entries 16–17; `prompts/
magnification-frontier.md`). It does **not** prove a lower bound and makes **no claim
about P vs NP**. Unlike the two collapsing cycles of [Module 21](locality-barrier.md),
this is the program's **first non-collapsing outcome**: it supplies the exact object the
prior sub-branch's stop-rule asked for, and validates it on two independent measures — but
it also locates the program's true tiny-instance ceiling.*

## Why this module exists (the reopening criterion)

Module 21 closed the locality sub-branch with a *structural* reason, not a parameter
choice: the meta-function it used, `MCSP[s]` (`HARD = no small **formula**`), is
**invariant under permutation of its `N` coordinates** (formula size ignores the order /
naming of the input variables). So every "best `k`-local" leverage quantity collapsed to a
**symmetric statistic of the hard set** — a global average already in the `μ_R` dictionary.
Two cycles fell for that one reason.

The stop-rule named the exact price of reopening:

> *Reopening the program requires a meta-level object that is **not** permutation-invariant,
> or a measure that is **not** a global statistic of the hard set — otherwise it re-enters
> the dictionary.*

This module supplies one, with the **smallest possible change** to the existing machinery:
keep the meta framing, change only the complexity measure.

## The object (faithful, exact) — `MBPSP[s]`

> `MBPSP[s] : {0,1}^N → {0,1}`, `N = 2^n`, input = the **whole truth table** of an `n`-bit
> function read as `N` coordinates; the measure is the **reduced-OBDD size at a FIXED
> variable order** `π = (x_{n-1}, …, x_0)`; `HARD = (min_obdd_size(t ; π) > s)`.

The reduced OBDD is **canonical for a fixed order**, so `min_obdd_size` is an exact integer
computed directly (node count = # distinct non-constant subfunctions, redundant tests
removed) in `poly(N)` — no DP table; n=4 (all `2^16` tables) runs in well under a second
(`pnp_lab/meta_complexity/order_locality.py`).

**Why it is not permutation-invariant.** OBDD size at a fixed order is invariant under
*negating* a variable (it swaps a node's two children) but **not** under *permuting* them:
the order singles out which variable sits on top. The textbook witness lives at n=4 and is
checked in code:

> `(x0 ∧ x1) ∨ (x2 ∧ x3)` has a **6**-node OBDD; the same function with variables 1,2
> swapped, `(x0 ∧ x2) ∨ (x1 ∧ x3)`, needs **8** — two truth tables related by a coordinate
> permutation, with **different size**. Formula size cannot tell them apart.

The fixed order is the "horizontal cut" the symmetric `MCSP[s]` lacked.

## Two cycles, two independent confirmations (no collapse)

The diagnostic in both cycles is the **spread within a Hamming-weight class** of the
difference vector `d` (`max − min` over equal-weight `d`): spread `= 0` everywhere ⇔ the
quantity depends only on `weight(d)` ⇔ permutation-invariant; spread `> 0` ⇔ it depends on
`supp(d)` (which variables, hence their place in the order) ⇔ the order survives. Threshold
is fixed-fraction `s = round(maxOBDD·0.5)`, θ=0.5, the same policy as Module 21 Cycle 2.

| cycle (Entry) | measure | what it reads | weight-class spread (w = 1,2,3,4) | verdict |
|---|---|---|---|---|
| C3 (16) | `pair_influence(d)` — # meta-inputs on which `MBPSP[s]` is non-constant over the 4-cube `{t, t^e0, t^ed, t^(e0^ed)}` | local sensitivity on a 2-cube | n=3: `0,0,0` · **n=4: `184,176,16,0`** · *MCSP control n=4: `0,0,0,0`* | **ORDER SURVIVES** |
| C4 (17) | `certified_drop(d)` — **the faithful Module-21 wall** `= locality.certified_k_local(N−2)` (cross-checked), # hard instances an `(N−2)`-local argument certifies with certainty when the pair `{0,d}` is released | global pure-hard-fibre count | n=3: `0,0,0` · **n=4: `144,144,16,0`** · *MCSP control n=4: `0,0,0,0`* | **WALL SEES THE ORDER** |

Both rows show the asymmetry **switching on at n=4** with the **MCSP formula control flat**
on the *same* measure (the symmetric trap that closed Module 21). The two confirmations are
**independent**: `pair_influence` (a custom local sensitivity) and `certified_drop` (the
program's own faithful certification wall) are different quantities — anisotropy in one does
not force anisotropy in the other. Robust across the whole non-degenerate band `s ∈ [5,10]`;
isotropic only at `s ≤ 4` where `HARD` saturates (`H ≈ 65534`, meta near-constant).

**Why j=1 is isotropic by construction.** Single-coordinate influence reads nothing: the
meta-function is invariant under *translations* of the input cube (`x → x⊕v` = negating
variables, a symmetry of `MBPSP`), and translations act transitively on single coordinates.
So `certified(N−1)` is identical on every axis for both `MCSP` and `MBPSP`. The asymmetry can
only appear at pairs (`j ≥ 2`), and by translation `certified_drop(a,b)=certified_drop(0,a⊕b)`
— the wall depends only on the difference vector `d`. The cross-check
`max_{a<b} certified_drop_pair(a,b) == locality.certified_k_local(meta, N, N−2)` (== 152 at
n=3) is the proof that this **is** Module 21's wall, not a redefinition of it.

## Decision: the program is REOPENED, then closed at its honest ceiling

The reopening criterion is **met**, exactly and reproducibly, and **doubly validated** — on
both the custom influence measure and the program's own faithful wall. This is the lab's
first escape from the dictionary trap, achieved by **breaking the symmetry (the order)**,
not by a new exact discriminant.

But the same numbers locate the program's tiny-instance ceiling, so a third cycle at `n ≤ 4`
would not add a level invariant:

- The asymmetry is **real but faint** — `~4.5%` of the base for `pair_influence`, `~0.23%`
  for the faithful wall (n=4, w=1) — and **shrinks with weight** (vanishing at w=4, a
  singleton class).
- It appears at **n=4 only**, the last brute-forceable level (n=5 = `2^32` tables,
  infeasible). The onset is **located**; a **cross-level invariant of the asymmetry is not
  measured** — and the cross-level *leverage* (small LB → big separation, the heart of
  magnification) is **asymptotic and escapes tiny size by construction**, exactly like the
  cited theorems.

Per the human PI decision (2026-06-15) the program is **crystallized here** as an honest
positive close: the structural cause of the prior collapse (permutation-invariance) is
removed; the order reaches the program's own wall; the cross-level leverage stays out of
reach of brute force. The constraint is **computational, not conceptual**.

## Honesty boundary (binding for this repo)

- **COMPUTED here** (exact integers, no floats on the critical path): `min_obdd_size` at a
  fixed order; its non-invariance under variable permutation (n=4 witness 6≠8) and
  invariance under negation; `MBPSP[s]` as a meta-function; `pair_influence` and
  `certified_drop` and their weight-class spreads for n=2,3,4 (`0,0` / `0,0,0` /
  `184,176,16,0` and `0,0,0` / `144,144,16,0`), robust across `s ∈ [5,10]`, with the MCSP
  formula control **flat** on both. The cross-check `certified_drop_pair == certified_k_local
  (N−2)` ties the wall to Module 21. All numbers are reproduced independently and frozen in
  `tests/test_order_locality.py`.
- **CITED, never computed**: the asymptotic magnification / locality theorems for branching
  programs and OBDDs and the amplification proper (Oliveira–Pich 2019; Chen–Jin–Williams
  2019/2020; locality barrier Chen–Hirahara–Ren–Santhanam–Vyas). At finite `n` the threshold
  is a single integer, not a regime.
- The result establishes a **faithful positive**: the meta object is genuinely
  non-permutation-invariant and the program's own wall reads the order at the deepest
  measurable level. It does **not** show the certified obstruction carries new magnification
  content or amplifies, and **no `P ≠ NP` or `P = NP` claim is made or implied**. A
  measurement method, not a result.

## Files

```
pnp_lab/meta_complexity/order_locality.py  # MBPSP[s] meta-function, min_obdd_size (fixed
                                           #   order), variable_swap, pair_influence (C3),
                                           #   certified_drop / wall_anisotropy (C4)
tests/test_order_locality.py               # exact frozen numbers (fast + slow MCSP control)
examples/run_order_locality.py             # founding witness + both cycles, printed exact
docs/locality-barrier.md                   # Module 21 — the sub-branch this reopens
docs/collapse-theorem.md                   # the capstone whose trap this escapes
RESEARCH_LOG.md                            # Entries 16–17 — the full audited trail
.cache/ct4.pkl                             # n=4 MCSP ComplexityTable (gitignored, control)
```
