# Module 23 — Certified-Bounds Regime (method note, RESTATEMENT #12)

**Verdict: RESTATEMENT #12 — collapse-onto-known (Bryant/Wegener), plus one honest
structural finding (the regime's own ceiling).** Not a result about P vs NP; a statement
about the *method* and about why the last out-of-the-box door does not open.

## Why this module exists

Both closed branches of the lab — the CSP/algebraic **Collapse Theorem** and the
**Magnification Frontier** ([Module 22](order-locality.md)) — hit the **same** wall, and
it is **computational, not conceptual**: the lab's whole method is *exact integers by
brute-force enumeration over tiny instances*, and on such instances a total classification
theorem "answers first" (the collapse). Module 22 located the order-anisotropy of the
faithful wall `certified_drop` at n=4, but a *cross-level* invariant needs n≥5, where
`N = 2^5 = 32` makes the `2^32`-truth-table SWEEP explode.

The pivot ([`prompts/certified-bounds-regime.md`](../prompts/certified-bounds-regime.md)):
**stop sweeping the function space**; CERTIFY an exact bound on an EXPLICIT family whose
per-instance measure stays cheap (`O(N)` for a single function), in a regime where the
controlling theorem is **not total**.

## The object

`family_or_and(n)` (n even), the Module-22 founding family:

```
f_n(x) = OR_{k=0}^{n/2-1} ( x_{2k} AND x_{2k+1} )
```

read at two explicit variable orders (realised by RELABELLING the variables, then measuring
with the fixed-frame `min_obdd_size` of `order_locality.py`):

* **good order** π (pairs adjacent, natural) ⇒ CERTIFIED `size_good(n) = n+2`.
* **bad order** π' (interleaved `[0,2,…,n−2, 1,3,…,n−1]`) ⇒ CERTIFIED `size_bad(n) = 2^(n/2+1)`.

Both are certified by a **checked recurrence** and cross-checked against the exact
`min_obdd_size` at n = 2,4,6,8 (the fidelity anchor). Founding witness: **6 ≠ 8 at n=4** —
the same witness as Module 22.

## The certified gap (the only valid measured quantity)

| n | size_good = n+2 | size_bad = 2^(n/2+1) | g(n) = gap |
|---|---|---|---|
| 2 | 4  | 4  | 0  |
| 4 | 6  | 8  | 2  |
| 6 | 8  | 16 | 8  |
| 8 | 10 | 32 | 22 |

`g(n) = 2^(n/2+1) − (n+2)`. A **finite, exact** instance of the CITED asymptotic
order-sensitivity (Bryant 1991 / Wegener, `2^Ω(n)` OBDD order gap), with **no enumeration**
of any function space. The certified-bounds regime **RESTATES Bryant** — the brief's
pre-declared, acceptable outcome: **RESTATEMENT #12**.

## What was STRUCK (category error)

The first draft also attempted a "wall-anisotropy" measure `A(n)` on the bad-order truth
table, reusing the faithful wall `certified_drop_spread`. This was **struck**: that wall is a
statistic of the **meta-function** `MBPSP[s]` over the **set of all `2^N` functions** — it
was handed a **single** function. The faithful call raises on the N-vs-n mismatch; the
Adversary + Evaluator KILL it as a category error. Only the certified size recurrence and the
gap `g(n)` survive as valid evidence.

## The real finding — the regime's own ceiling

The certified-bounds regime makes the OBDD size of a **single** function cheap (`O(N)`),
evading the sweep — **and only there**. A WALL invariant (Module 21/22) is irreducibly a
property of the meta-function `MBPSP[s]` over the **set** of all functions: it needs a *hard
set to certify*. Reintroducing the set at n≥5 reintroduces exactly the `2^(2^n)` enumeration
the regime tried to avoid. **Certification buys per-instance cheapness, not the cross-level
invariant**: the moment the quantity is a property of the wall, the sweep returns. That is the
regime's own ceiling — and it is, once more, the same computational wall, restated.

## Honesty boundary

COMPUTED (exact integers, no floats): the certified size recurrence `size_good = n+2`,
`size_bad = 2^(n/2+1)`, cross-checked against the exact `min_obdd_size` at n=2,4,6,8; the
gap `g(n) = 2^(n/2+1) − (n+2)`. The order gap is a **finite exact instance of Bryant/Wegener**
(CITED, never re-proved asymptotically) ⇒ RESTATEMENT #12. The wall-anisotropy attempt is
STRUCK (category error). No separation, no cross-level invariant, **no P vs NP claim**.

Files: `pnp_lab/meta_complexity/certified_obdd.py`, `tests/test_certified_obdd.py`,
`examples/run_certified_obdd.py`.
