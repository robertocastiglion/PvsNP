# TINY-INSTANCE COLLAPSE (Module 19) — the closing meta-conclusion of the research loop

*Crystallized 2026-06-09. This module does **not** prove a lower bound and **does
not touch P vs NP**. It is a statement about the **method** of the autonomous
research loop on **finite** instances (`n ≤ 4`), backed by exact, reproducible
witnesses. It closes the exploratory loop after **five consecutive
RESTATEMENT-OF-KNOWN** cycles.*

## Where this comes from

An autonomous multi-agent loop (Explorer → Builder → Adversary → Evaluator →
Archivist, see `RESEARCH_LOG.md`) ran five cycles, each trying to build a
**local discriminant** that carries genuinely new content — a measurable quantity
that separates structurally-similar objects and is **not** a restatement of a
theorem already in the `μ_R` "dictionary" (cover-LP / proof-complexity / KT).

Every cycle landed on the same verdict. The pattern is robust enough to state as
a falsifiable meta-conclusion.

> **TINY-INSTANCE COLLAPSE.** In the regime `n ≤ 4`, every local discriminant the
> loop has built reduces — via an **exact identity verified in code** — to an
> invariant already in the `μ_R` dictionary. The pattern **transcends three
> arenas**.

| arena | cycle | the discriminant | what it collapsed to |
|---|---|---|---|
| duality / cover-LP | 1–2 | lift gap `G★ = Cov − LP` | rectangle/biclique-cover LP integrality gap (Lovász) — see `docs/duality-gap-theory.md` |
| proof-complexity | 4 | interpolant size `S` vs `P`,`C` | `S` not canonical; `P`,`C` read off the KW⁺ matrix = Razborov–Pudlák, bound by the forced theorem `P ≤ 2^C` — see `docs/bounded-observer.md` |
| meta-complexity | 5 | down-degree `d_flip` on the truth-table cube | the **discrete gradient of MCSP-size** — the derivative of a KT object |

The recurring mechanism is *"the gradient/derivative of a known object is still
that object"*. That is why each cycle is a restatement, not a discovery.

## What this module makes reproducible

The meta-conclusion is only worth crystallizing if its load-bearing claims are
**exact and re-runnable**. This module deprecates the cycle-5 discriminant
`d_flip` (`strata_graph.py`) with three witnesses, computed exactly over **all**
`2^(2^n)` Boolean functions.

### Killer-1 — input-negation is a cost automorphism (`d_negation ≡ 0`)

Negating an input variable `xᵢ → ¬xᵢ` maps an optimal formula to one of equal
size, so `cost` is invariant: the down-degree of that move is identically zero.
Measured exact: **256/256** functions on `n=3`, **65536/65536** on `n=4`. The
"control" move is trivial by construction — as predicted in advance.

### W1 — `d_flip` is the exact gradient of MCSP-size

The "genuine" move flips one output bit (a Hamming neighbour on the truth-table
cube). Its down-degree is, **by the identity**

```
d_flip(f) = #{ k : cost[f XOR (1<<k)] < cost[f] },
```

the count of neighbours of strictly smaller MCSP-size — i.e. the **discrete
gradient** of `cost`. We recompute `d_flip` from the `cost` dictionary **alone**
(no extra oracle) and check it matches on every function: **0 mismatches** on
`n=3` (256/256) and `n=4` (65536/65536). So `d_flip ∈ σ(cost)`: it is the
derivative of a KT object, not a new invariant.

### W2 — `d_flip` is not canonical

A structural discriminant must not depend on an arbitrary choice of "cost". It
does. Replacing one exact complexity measure (minimal **formula size**, Module 6)
with another (optimal **decision-tree depth**) changes the value of `d_flip` on

```
154 / 256  ≈ 60%   of functions at n=3      (and a non-trivial fraction at n=4)
```

A metric that flips on a majority of inputs under a benign change of the
underlying cost is not measuring structure — it is measuring the cost oracle.

### The explicit falsifier (not found)

The meta-conclusion is **falsifiable**:

> **FALSIFIER.** A discriminant measurable on `n ≤ 4` that (a) separates two
> functions of **equal** MCSP-size and equal cover-LP/`G★`, and (b) is **not**
> reconstructible from `cost` (nor from `μ_R`) by an exact identity.

`falsifier_status` checks the loop's toolbox: `d_flip` violates (b) by W1 (it is
cost-reconstructible); the remaining tools (sensitivity, block-sensitivity,
GF(2)-degree) satisfy (b) but are **themselves** classical dictionary
invariants, so they are not new content. **No falsifier in the toolbox →
collapse confirmed.** Producing one would be the first genuine new content; the
loop stops here precisely because it could not.

## Verdict

Five consecutive cycles, three independent arenas, one outcome: on tiny
instances the loop's discriminants are exactly reconstructible from invariants
already in the dictionary. This is **strong negative evidence** that the
`μ_R` "everything-is-a-known-duality" reading is robust on finite instances — and
an honest stopping point for the exploration on this repo.

## Honesty boundary (binding for this repo)

- This is a statement about the **method** of the loop on **finite** instances
  (`n ≤ 4`), **not** a claim about P vs NP and **not** a lower bound. The collapse
  could in principle break at larger `n`; we make no asymptotic claim.
- All numbers are **exact** (integer arithmetic, full enumeration of the
  `2^(2^n)` functions). `cost` is exact minimal formula size (Module 6); the
  second oracle is exact optimal decision-tree depth.
- `d_flip` is **deprecated as a metric**, not deleted: `strata_graph.py` remains a
  valid exact **measurement bench** for tiny instances. The deprecation is W1+W2.
- The three-arena reduction is verified **in code for the meta-complexity arena**
  (this module). The cover-LP and proof-complexity arenas were verified in their
  own cycles (Modules 16/18 + `RESEARCH_LOG.md` Entry 1–2, 4–5); here they are
  cited, not re-derived.

## Files

```
pnp_lab/meta_complexity/collapse.py      # the closing witnesses (W1, W2, killer-1, falsifier) — exact
pnp_lab/meta_complexity/strata_graph.py  # the cycle-5 measurement bench (d_flip DEPRECATED as a metric)
tests/test_collapse.py                   # exact tests (n=3 fast; n=4 exhaustive, slow)
examples/run_collapse.py
```
