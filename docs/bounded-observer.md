# Bounded Observer (Module 16) — can the four barriers be one inequality?

*Implemented on 2026-06-03. A minimal definition of "resource-bounded observer"
and a single distinguishing advantage `Δ(𝒞; D0, D1)`, then an exact measurement
of which barriers fit `Δ ≤ ε` — and the precise point where one does not.*

## The question

Module 15 measured that the barriers live on **two orthogonal axes** (information
× computation). This module asks the sharper question: is there **one** definition
of "bounded observer" that contains, as special cases,

- **relativization** — a *query* limit,
- **algebrization** — an *algebraic-query* limit,
- **natural proofs** — a *computation* limit,
- **proof complexity** — a *proof-length* limit,

and can all four be written as

```
Δ(𝒞; D0, D1) ≤ ε
```

for different observer classes `𝒞`? If not, **where exactly** does it break?

## The minimal definition

A **world** `w ∈ Ω` is the object the technique accesses (an oracle, a function, a
formula). A **bounded observer** is a triple `T = (𝒜, 𝒭, t)`:

| component | meaning | axis |
|---|---|---|
| `𝒜` access interface | allowed queries `q` and answer `ans(w,q)` | **information** (bits per probe) |
| `𝒭` resource | the class of functions combining answers into a bit | **computation** |
| `t` budget | #queries / transcript length / certificate size | quantity |

Decision: `T(w) = 𝒭( (q₁, ans(w,q₁)), …, (q_t, ans(w,q_t)) ) ∈ {0,1}`.

The **single distinguishing advantage**, over a class `𝒞` and two world
distributions:

```
Δ(𝒞; D0, D1) = sup_{T ∈ 𝒞} | Pr_{w~D1}[T(w)=1] − Pr_{w~D0}[T(w)=1] | .
```

A barrier is the statement: for the technique's class and for `D1` ("the theorem
holds") vs `D0` ("it is collapsed/forged"), `Δ(𝒞; D0, D1) ≤ ε` — the technique
cannot tell which world it is in, hence cannot prove the theorem.

## What it measures (exact, tiny instances)

`examples/run_bounded_observer.py` instantiates all four and computes `Δ`:

```
(1) RELATIVIZATION   𝒜 = Boolean queries,  𝒭 unbounded,  budget t
    needle on N=8 points:   Δ(t) = t/N
    t=0: 0.000   t=1: 0.125   t=2: 0.250          → ε = t/N → 0.   FITS.

(2) ALGEBRIZATION    𝒜 = low-degree-extension queries
    1 algebraic query: Δ=1.000   1 Boolean query: Δ=0.125
    → same template, 𝒜_alg ⊋ 𝒜_rel; bound rests on Schwartz–Zippel.  FITS.

(3) NATURAL PROOFS   𝒜 = saturated truth table, 𝒭 bounded (Module 15)
    Δ with saturated info (ℓ=n=3) and computation s=3:  Δ=0.324
    → bound from the ORTHOGONAL (computation) axis.  FITS.

(4) PROOF COMPLEXITY  attempt: D0=SAT, D1=UNSAT, t = resolution depth
    D0 side (satisfiable formulas):  Pr[decide=1] = 0.000
    t=0: 0.000  t=1: 0.333  t=2: 1.000  t=3: 1.000  t=4: 1.000
    min |Π| over UNSAT worlds (depth): [1, 2, 2]
    → D0 side is IDENTICALLY 0 (soundness): no two-sided ε.
      the real quantity is min|Π| ∈ ℕ∪{∞}, not sup|E1−E0| ∈ [0,1].  FAILS.
```

### Why 1–2–3 genuinely unify

- **Relativization** and **algebrization** are the *same* template — same needle
  worlds, same `Δ`, `𝒭` unbounded — differing **only in the interface `𝒜`**:
  Boolean point queries vs queries to the low-degree extension `Ã` (a field
  element per probe). The code shows `𝒜_alg ⊋ 𝒜_rel`: one algebraic query already
  beats `t` Boolean ones. The bound is a (algebraic) **query-complexity** bound —
  exactly how Aaronson–Wigderson prove the barrier — resting on **Schwartz–Zippel**
  (two distinct degree-`d` polynomials agree on `≤ d/|F|` of the points; verified
  on the tiny instance).
- **Natural proofs** maxes the information axis (reads all `2^n` bits) and puts the
  bound entirely on `𝒭` (computation). This is Module 15, reused verbatim.

So the bounded-observer template *is* the common generalization of the first three
barriers, on the two orthogonal axes `(𝒜, 𝒭)`.

## The first point of failure (proof complexity)

The break is **the construction of `Δ` itself** — the `advantage` step. Writing
`Δ = | E_{D1}[T] − E_{D0}[T] |` requires two things proof complexity lacks:

1. **Two-sidedness ⇒ there is no `D0`.** A proof system is **sound**: on a "false"
   world (a satisfiable formula) the probability of producing a refutation is
   **identically 0** — not `ε`. The code confirms it: `refutation_depth` returns
   `None` for every satisfiable formula at every depth (`D0` acceptance `= 0.000`,
   `test_d0_acceptance_is_zero_at_every_budget`). So `Δ` collapses to the single
   `D1` side, `Pr[short refutation exists]` — not a difference, not a correlation.

2. **Existential certificate ⇒ wrong type.** The decision rule is **not** a
   function of the world `τ` alone: it takes an extra input `Π` (the candidate
   proof) under an existential, `∃Π (|Π| ≤ t): Verify(τ, Π) = 1`. The hard
   quantity is therefore `min |Π| ∈ ℕ ∪ {∞}` — a **witness length** — whereas `Δ`
   has type `sup of a difference of means ∈ [0,1]`. The signatures do not match:

   ```
   Δ : (decision rule) × (D0, D1) → [0,1]      (sup of difference of means)
   proof complexity : τ ↦ min{|Π| : Verify(τ,Π)=1} ∈ ℕ ∪ {∞}   (min over ∃-witnesses)
   ```

The module prints these `min |Π|` values (`[1, 2, 2]`) precisely to exhibit the
type that `Δ` cannot represent.

### The only way to "save" it — and its cost

Proof complexity can be made statistical by putting a distribution over hard
formulas via a **proof-complexity generator** (Razborov, Krajíček), turning
"no short refutation of `g(x)`" into a pseudorandomness statement — a
natural-proofs-style `Δ ≤ ε`. Likewise **feasible interpolation** converts
proof size into circuit size (the computation axis), but **fails** for strong
systems under cryptographic assumptions. Both bridges **require an extra
pseudorandomness hypothesis** that is not part of the proof-complexity barrier:
they **reduce barrier 4 to barrier 3 at the cost of an unproven assumption** —
a reduction with a debt, not a common generalization.

## Verdict

- Barriers **1, 2, 3** are a single template `Δ(𝒞; D0, D1) ≤ ε`, with `𝒞`
  varying over two orthogonal axes `(𝒜, 𝒭)`. Relativization/algebrization differ
  only in `𝒜`; natural proofs saturates `𝒜` and bounds `𝒭`.
- Barrier **4 does not fit**. The break is at the advantage step: soundness kills
  the `D0` side (no `ε`), and the governing quantity is a witness length
  `min|Π| ∈ ℕ`, a different type than `sup|E1−E0| ∈ [0,1]`.

## Honesty boundary (binding for this repo)

- All numbers are **exact** measurements on **minuscule** instances, **not** the
  asymptotic barriers. `N=8` needle, `n=3` truth tables, 2–3 variable CNFs.
- For **algebrization** we demonstrate the **interface enrichment** and the
  **Schwartz–Zippel** lemma the bound rests on; we do **not** reproduce an
  asymptotic algebraic lower bound (that needs the Aaronson–Wigderson class
  separation). This is deliberate and documented.
- Resolution is the proof system used for the proof-complexity probe; the
  conclusion (soundness ⇒ `D0 ≡ 0`; quantity is a length) is **system-independent**
  — it holds for any sound system.
- Reuses Module 15 for the natural-proofs axis. Does **not** prove (or touch) P vs NP.

## Files

```
pnp_lab/bounded_observer/observer.py   # T=(𝒜,𝒭,t), Δ, the four instances, the probe
pnp_lab/bounded_observer/lab.py        # unified table + verdict (text)
tests/test_bounded_observer.py         # 17 exact tests
examples/run_bounded_observer.py
```
