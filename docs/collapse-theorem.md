# THE COLLAPSE THEOREM (capstone) — the closing meta-conclusion of the autonomous loop

*Crystallized 2026-06-14. This is the **capstone** of the autonomous research loop
(`RESEARCH_LOG.md`, Entries 1–12). It does **not** prove a lower bound and **does
not touch P vs NP**. It is a single, falsifiable statement about the **method** of
the loop on finite instances, backed by **ten consecutive RESTATEMENT-OF-KNOWN**
cycles across **four** independent arenas, all reproducible in code. It supersedes
the partial closings of Module 19 (circuit/cost arena) and Module 20 (CSP/Inv–Pol
arena) by stating what they have in common and why the loop stops on the
CSP/algebraic branch.*

## The statement

> **COLLAPSE THEOREM (empirical).** Every *local discriminant* the loop has built —
> a quantity intended to separate structurally-similar objects with genuinely new
> content — reduces, via an **exact identity verified in code**, to an invariant
> already named by a known theorem (a "dictionary" object). The reduction holds
> across **four arenas** and **ten cycles**. The common cause is not the choice of
> invariant: it is **the regime**. On **tiny, exactly-enumerable** instances the
> governing classification theorem is *total*, so it is mute on the *value* of any
> new quantity yet **absorbs** that quantity into its own verdict. **Exact
> enumerability is the trap, not the particular discriminant.**

## The four arenas, ten collapses

| arena | cycles (Entry) | discriminant | collapsed to (dictionary object) |
|---|---|---|---|
| duality / cover-LP | 1–2 | lift gap `G★ = Cov − LP` | rectangle/biclique-cover LP integrality gap (Lovász) — `docs/duality-gap-theory.md`, Module 18 |
| proof-complexity | 4 | interpolant size `S` vs `P`,`C` | `S` non-canonical; `P`,`C` = KW⁺ matrix (Razborov–Pudlák), forced `P ≤ 2^C` — `docs/bounded-observer.md` |
| meta-complexity (`σ(cost)`) | 5–6, 8, 9 | `d_flip`; falsifier hunt; optimal-split DAG | discrete gradient of MCSP-size; orbit-complete dictionary; all reconstructible from the cost table — Module 19, `docs/tiny-instance-collapse.md` |
| algebraic CSP (Inv–Pol) | 10, 11, **12** | symmetric profile; `g = \|Pol₂^{comm,idem}\|`; **`w*` local-consistency width** | BLP ⟺ symmetric polymorphisms (Barto–Kozik); clone-slice cardinality; **width-1 vs width-2 step** (Feder–Vardi/Dalmau–Pearson + Barto–Kozik (2,3)) — Module 20, `docs/invpol-collapse.md` |

Three mechanisms recur, one per layer of the dictionary:

1. *"the gradient/derivative of a known object is still that object"* (`d_flip` =
   gradient of MCSP-size; the optimal-split geometry is built from the cost table);
2. *"the cardinality of a slice of a known structure is still dictionary content"*
   (`g = |Pol-slice|`, a slice of the polymorphism clone);
3. *"a width/level index inside a total dichotomy is the dichotomy's own verdict
   relabeled"* (`w*` = the width-1/width-2 step).

## Why the regime pivot did not escape (the sharpest evidence)

After nine collapses the loop deliberately **pivoted out of the exact-finite
program** (Entry 12), aiming for the Bulatov–Zhuk-hard regime where the dichotomy
should be *deep*. The first pivot cycle collapsed **at once**, and the post-mortem
is the load-bearing insight of this capstone:

- The new "exact-per-instance on a sample" regime **never left the enumerable**.
  All 472 binary WNU relations on `D = {0,1,2}` are the *complete* `2⁹` universe,
  enumerated by brute force; symmetric operations up to arity 4 are `≤ 531441`,
  also brute-forced. There were **no certified bounds** and **no genuine
  infeasibility of enumeration**.
- Over that enumerable universe the confusion matrix of `w*` against the width-1
  marker is **perfect** (455 + 17, zero off-diagonal): `w*` is exactly the known
  width-1/width-2 step. The pivot **changed the arena, not the regime.**

So the collapse is **not** a property of CSPs, of cost, or of any one invariant.
It is a property of asking an **exactly-enumerable tiny** question of an arena that
possesses a **total classification theorem**: the theorem answers first.

## The falsifier (what would break this)

The Collapse Theorem is falsifiable. It is broken by **either**:

1. a discriminant, measurable exactly on tiny instances, that separates two objects
   a parent theorem declares equivalent **and** is provably *not* reconstructible
   from a dictionary invariant by an exact identity (the Module-19 falsifier — hunted
   exhaustively at `n ≤ 4`, **not found**); **or**
2. a measurement in the **genuinely non-enumerable** regime (high-arity / large
   domain, via *certified bounds* rather than brute force) where the controlling
   theorem is *not* total, and a measured quantity carries content the theorem does
   not fix. This regime was **declared but never reached** — it is the honest open
   door, and the reason this is a statement about the *method*, not a closed result.

## Decision: the CSP/algebraic branch is CLOSED

Per the loop's stop rule (two consecutive RESTATEMENTs with no plausible new
in-regime direction) and the human PI decision (2026-06-14), the autonomous loop
**stops on the CSP/algebraic branch**. Iterating an eleventh exactly-enumerable
cycle would yield RESTATEMENT #11 with probability ≈ 1: the arena is saturated with
attractor theorems that absorb every tiny measurement. Reopening requires **leaving
the enumerable regime** (falsifier door 2 above), which is a methodological change —
exact-on-certified-bounds, not brute force — that the current lab is not equipped
to carry out rigorously, and which the PI may choose to set up as a separate program.

## Honesty boundary (binding for this repo)

- This is an **empirical, falsifiable statement about the method** of the loop on
  **finite, exactly-enumerable** instances. It is **not** a theorem of complexity
  theory, **not** a lower bound, and makes **no claim about P vs NP** (neither
  `P ≠ NP` nor `P = NP`).
- "Ten collapses across four arenas" is exact and reproducible: each reduction is an
  identity checked in code (Modules 18, 19, 20 + `RESEARCH_LOG.md` Entries 1–12).
  Where an arena is cited rather than re-derived here, its cycle verified it in its
  own module.
- The decisive regime — non-enumerable high-arity / large-domain CSP with **certified
  bounds** — is **untested**. The Collapse Theorem therefore claims robustness *only*
  over the exactly-enumerable tiny regime, and explicitly leaves the asymptotic /
  certified-bound regime open. That open door is the whole content of falsifier
  door 2.

## Files

```
docs/tiny-instance-collapse.md   # Module 19 — circuit/cost arena (σ(cost)), n≤4
docs/invpol-collapse.md          # Module 20 — CSP/Inv–Pol arena, |D|=3
docs/duality-gap-theory.md       # cover-LP arena
docs/bounded-observer.md         # proof-complexity arena
pnp_lab/csp/local_consistency3.py  # Entry 12 — w* bench (RESTATEMENT, not a Module)
RESEARCH_LOG.md                  # Entries 1–12 — the full audited trail
```
