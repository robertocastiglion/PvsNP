# The `𝒭=∞` Survival Test (Module 17) — one measurable criterion that sorts the barriers

*Implemented on 2026-06-03. Companion to Modules 15–16 and to `docs/duality-gap-theory.md`.
A single scalar test — computed exactly on tiny instances — that, given a barrier,
decides which of the two known families it belongs to. It is a **classification
criterion, not a new lower bound**; the honesty boundary below is therefore strict.*

## The question

Module 15 established that the barriers live on **two orthogonal axes** — information
(`𝒜`) and computation (`𝒭`). Module 16 asked whether one inequality `Δ ≤ ε` covers
them all. This module asks the sharper, *operational* question:

> Given a barrier, is there **one measurable test** that tells you whether its
> indistinguishability is **information-theoretic** (unconditional) or
> **computational** (a pseudorandomness hypothesis in disguise)?

There is. It is a single number.

## The test

Take the barrier's distinguishing advantage `Δ` and hand the distinguisher
**unbounded computation** `𝒭 = ∞`, leaving only its **interface** limit `𝒜`. Then:

```
Δ(𝒭=∞) < 1   ⟹   INFORMATION-THEORETIC   (unconditional; the bound lives on 𝒜)
Δ(𝒭=∞) = 1   ⟹   COMPUTATIONAL           (= a pseudorandomness assumption; lives on 𝒭)
```

The intuition is exact. A barrier **survives** unbounded computation iff its bound
remains even when the observer can compute anything — which means the limit was never
about computation: you *missed the needle*, and no amount of computation recovers
information you never saw. That is an unconditional theorem. If instead the bound
**evaporates** (`Δ→1`) the moment computation is unbounded, then it existed *only*
because `𝒭` was restricted — i.e. the statement "hard looks easy to bounded
computation", which is precisely **pseudorandomness**.

## What it measures (exact, tiny instances)

`examples/run_survival_test.py` measures the two clean poles.

```
(1) RELATIVIZATION   axis 𝒜 (information)
    needle on N=8, budget t=2 Boolean queries, 𝒭 = ∞ (arbitrary g)
    Δ(𝒭=∞) = 0.250 = t/N      → computation is INERT
    margin = 1 − Δ = 0.750 > 0 ⟹ SURVIVES
    VERDICT: information-theoretic (unconditional, interface-bound)

(2) NATURAL PROOFS   axis 𝒭 (computation)
    saturated information ℓ=3; Δ(ℓ=3, s) as compute s grows:
      s=1: Δ=0.264   s=2: Δ=0.324   s=3: Δ=0.324
      s=∞: Δ = 1.000   (the indicator of the 'hard' predicate)
    margin = 1 − Δ = 0.000     ⟹ does NOT survive
    VERDICT: computational (= pseudorandomness)
```

### Why relativization survives

The Module-16 class of `≤ t` Boolean-query observers *already* combines its answers
with an **arbitrary** `g` — that is `𝒭 = ∞`. Yet `Δ = t/N`. So the bounded- and
unbounded-computation values coincide: **computation is inert**, the whole bound is on
the interface (you queried `t` of `N` cells). Restricting `g` can only *lower* `Δ`, so
`Δ(𝒭=∞) = t/N < 1` is the maximum, and it is `< 1`. The barrier survives — it is a
genuine information bound, holding with no assumption.

### Why natural proofs does not

The observer reads the **entire** truth table (`ℓ = n = 3`, saturated information). With
`s` gates of computation, `Δ(ℓ=3, s)` is small (Module 15). But the "hard" predicate
(formula complexity `≥ τ`) **is a function of the truth table**: with `𝒭 = ∞` the
optimal observer is simply its indicator, which separates hard from easy **perfectly**,
so `Δ = 1`. The module computes this directly (not hard-coded): `D1` uniform on the
hard functions, `D0` uniform on the easy ones, `decide(f)=1 ⟺ f hard` gives
`Pr_{D1}=1`, `Pr_{D0}=0`, `Δ=1`. The bound existed **only** because `𝒭` was bounded —
that restriction is the pseudorandomness assumption.

## What this settles (and what it does not)

The two "genericities" that earlier looked identical are **not** the same object:

| family | barriers | indistinguishability | conditional on | survives `𝒭=∞`? |
|---|---|---|---|---|
| information-theoretic | relativization, algebrization | `t/N`, Schwartz–Zippel | **nothing** (a theorem) | **yes** (`Δ<1`) |
| computational | natural proofs, proof complexity | pseudorandom (PRF) | **pseudorandomness** | **no** (`Δ→1`) |

So the four barriers do **not** collapse onto a single pseudorandomness hypothesis:
relativization and algebrization escape it, unconditionally and measurably. The
survival test is the operational form of Module 15's two axes — a single number that
recovers the split.

## Honesty boundary (binding for this repo)

- **This is a classification criterion, not a new lower bound.** It re-derives the
  information × computation split of Module 15 as one measurable scalar `Δ(𝒭=∞)`. It
  proves no new separation and **does not prove (or touch) P vs NP**.
- All numbers are **exact** on **minuscule** instances: an `N=8` needle and `n=3`
  truth tables — **not** the asymptotic barriers. The high-`s` cells of Module 15 are
  certified **lower bounds** (`≥`), which only strengthens the `𝒭=∞` verdict (the true
  `Δ` is at least as large).
- We **measure two clean poles** (relativization, natural proofs). Algebrization groups
  with the first (interface `𝒜` enriched — Module 16) and proof complexity with the
  second (same pseudorandomness debt — `docs/duality-gap-theory.md`); those groupings
  are cited, not re-measured here.
- The criterion is binary by design (`Δ<1` vs `Δ=1`). At the convex corners this is
  sharp; the claim is about the **limit** `lim_{𝒭→∞} Δ`, which for these instances is
  attained exactly.

## Files

```
pnp_lab/survival_test/survival.py   # the test, the classifier, the two poles
pnp_lab/survival_test/lab.py        # table + verdict (text)
tests/test_survival_test.py         # 13 exact tests
examples/run_survival_test.py
```
