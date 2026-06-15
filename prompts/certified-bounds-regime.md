# Scoping brief — the certified-bounds, non-enumerable regime

Status: **scoped, not launched** (2026-06-15). This is the one genuinely
out-of-the-box door left open after the CSP/algebraic branch closed
(`docs/collapse-theorem.md`, falsifier **door 2**) and the Magnification Frontier
closed (`docs/order-locality.md`, Module 22, ceiling at n=5 = 2^32). Both closures
hit the **same** wall, and it is **computational, not conceptual**: the lab's entire
method is *exact integers by brute-force enumeration over tiny instances* (all
`2^(2^n)` functions, all `n≤4` instances), and on such instances a **total
classification theorem answers first** — the collapse. This brief specifies the
methodological pivot that would leave that regime, why it is hard, and the smallest
honest first experiment. No P vs NP claim, ever.

## The pivot in one line

Stop sweeping the whole function space; instead certify an **exact bound** on an
**explicit family** whose per-instance measure stays cheap, in a regime where the
controlling theorem is **not total** — and measure whether a quantity carries content
the theorem does not fix.

## Why this is the same door from two arenas

- **Magnification (Module 22).** The order-anisotropy of the faithful wall
  `certified_drop` was located at **n=4** (spread `144,144,16,0`) but a *cross-level
  invariant* needs n=5+, and `N = 2^5 = 32` means `2^32` truth tables — the **sweep**
  explodes. Yet a **single** function's min-OBDD-size at a fixed order is `O(N)` exact.
  The explosion is the enumeration over *all* functions, not the per-instance measure.
- **CSP (Collapse Theorem).** Same shape: a single instance's width / polymorphism
  check is cheap; enumerating *all* high-arity / large-domain relations is what lets
  Bulatov–Zhuk "answer first." Door 2 is: certify a bound on an **explicit** hard
  instance where the dichotomy theorem is not a total classifier of the measured
  quantity.

So the pivot is one object — **certify, don't enumerate** — usable in either arena.

## What "certified bound, exact, not brute force" must mean (discipline)

To stay inside the lab's honesty contract without enumeration:

1. **Exact** — the per-instance quantity is an exact integer/rational (a single OBDD
   size, a single polymorphism test), never a float, never a statistical estimate.
2. **Certified** — the cross-level claim is a **proved bound on a family**, verified in
   code *on the family's structure* (e.g. a checked recurrence for the family's OBDD
   size at every n), **not** a measured sweep. The certificate is re-checkable.
3. **Falsifiable** — pre-declare the **parent-killer**: the known asymptotic theorem
   the measured quantity would merely restate. "Restatement of the cited bound in the
   new regime" is the expected, acceptable outcome — report it as RESTATEMENT #12 and
   move on. The collapse can fire here too; the point is to find out.
4. **Reproducible** — the family is explicit and named; the certificate runs in the
   test suite at several n (not just the largest feasible one).

The honest tension to name up front: enumeration is what made the lab *falsifiable*
("every function, no exceptions"). Leaving it trades total coverage for reach. The
discipline above is how we keep falsifiability without the sweep — if a direction
cannot meet all four, it is not admissible.

## Primary candidate (continuation of Module 22, most concrete)

**Explicit OBDD families with a PROVABLE order gap.** The classical exponential
order-sensitivity functions are exactly the certified-bound objects Module 22 lacked:

- **HWB** (hidden weighted bit) — the textbook function with provable
  `2^Ω(n)` OBDD-size gap between good and bad variable orders (Bryant 1991; Wegener).
- **ISA / storage-access (multiplexer)** families — provable order-dependent size.
- The Module-22 founding family `(x0∧x1) ∨ … ∨ (x_{2k}∧x_{2k+1})` — order gap visible
  already at n=4 (6 vs 8), extends by a checked recurrence.

These give a **certified order gap at every n** without enumerating any function space.
The cross-level invariant Module 22 could not reach — *how the order-anisotropy of the
wall grows from level to level* — becomes a **proved recurrence** on the family,
checkable in code at n = 4,5,6,… (single-function OBDD size is `O(N)`).

**Pre-declared parent-killer (fidelity).** The certified gap must NOT be merely
Bryant/Wegener's exponential OBDD lower bound re-derived: if the measured cross-level
quantity is an exact restatement of the cited asymptotic bound, it is RESTATEMENT #12
in the new regime (informative collapse, not a new leverage). PASS requires a quantity
that is **a property of the magnification wall** (`certified_drop` / leverage operator),
not of raw OBDD size — i.e. the order-anisotropy of *certification*, shown to grow,
and shown **not** reconstructible from the family's OBDD-size recurrence alone (the
analogue of the Module-19 falsifier, now on a family instead of a sweep).

## Reserve candidate (CSP arena)

**Certified width / polymorphism obstruction on an explicit high-arity instance.** Take
a named large-domain relation that Bulatov–Zhuk classify as NP-hard; certify a
local-consistency width or a missing-polymorphism bound on it *without* enumerating
`Pol`. Killer: the bound reduces to the dichotomy criterion (a Taylor / WNU
polymorphism test) restated — RESTATEMENT in the algebraic regime. Less aligned with
the lab's current OBDD machinery; lower priority than the primary.

## First minimal experiment (the smallest honest step)

1. Implement `hwb(n)` and `family_or_and(k)` truth tables, and a **proved recurrence**
   for their reduced-OBDD size at the canonical order π and at one provably-bad order π'
   (`pnp_lab/meta_complexity/certified_obdd.py`). Verify the recurrence against the
   *exact* `min_obdd_size` from `order_locality.py` at n = 3,4,5 (where direct
   computation on a single function is still cheap) — this is the fidelity anchor.
2. Extend the certified size to n = 6,7,8 **by the recurrence only** (no per-function
   sweep), and read the **order-gap curve** `g(n) = size_π' − size_π` (or its ratio).
3. **Decision test (pre-declared):** is the gap curve a *new* cross-level quantity, or
   is it `2^Ω(n)` — Bryant's bound restated? If the latter, RESTATEMENT #12: the
   non-enumerable regime collapses onto the cited asymptotic theorem, exactly as the
   enumerable regime collapsed onto its total classifiers — a sharp, honest result
   about the *method* extending to the new regime. If a wall-specific anisotropy grows
   and is **not** reconstructible from the OBDD-size recurrence, the door is genuinely
   open and the program continues.

## Run

This is a **separate program**, launched only by a human PI decision (like Module 21 /
Module 22 crystallization). Cycle shape unchanged: Explorer (hypothesis + parent-killer
+ the **four-point admissibility** above) → Builder (exact recurrence + fidelity anchor
+ tests) → measure → Adversary (is it Bryant restated? is the certificate sound?) →
Evaluator (fidelity + tangibility + honesty boundary) → Archivist. Repo conventions:
doc EN-first, code/tests/example, `py -m pytest`, exact integers, no floats; cite the
asymptotic theorems, never claim a separation, mark every artifact. No P vs NP claim.
