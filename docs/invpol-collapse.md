# INV-POL COLLAPSE (Module 20) — the collapse transcends `σ(cost)`

*Crystallized 2026-06-14. This module does **not** prove a lower bound and **does
not touch P vs NP**. Like Module 19 it is a statement about the **method** of the
autonomous research loop on **finite** instances — here on the constraint-domain
`D = {0,1,2}` — backed by exact, reproducible witnesses. It extends the
Tiny-Instance Collapse from the circuit/cost arena to the **algebraic CSP arena**,
after **nine consecutive RESTATEMENT-OF-KNOWN** cycles across **four** arenas.*

## Why a fourth arena was needed

Module 19 closed the loop with a sharp caveat: every discriminant that collapsed
there lived **inside `σ(cost)`** — it was reconstructible from minimal formula
size (a KT object). A sceptic could object that the collapse is an artefact of
staying in the covering / formula-size world. The *restart program*
(`prompts/restart-out-of-dictionary.md`) was built to answer exactly this: find a
direction whose objects are **not derived from cost**.

The **polymorphisms** of a relation `Γ` (its algebraic closure, the clone
`Pol(Γ)`) are such an object. They are the bridge where CSPs touch P vs NP
(Bulatov–Zhuk dichotomy: `CSP(Γ) ∈ P ⟺ Γ has a Taylor/WNU polymorphism). This is
the genuinely **out-of-`σ(cost)`** test — and it is the decisive one, because on
`|D| ≥ 3` the dichotomy is no longer the fully-classified Boolean lattice
(Post/Schaefer), where a parent-killer is almost tautological.

> **INV-POL COLLAPSE.** On the ternary domain `D = {0,1,2}`, the candidate
> discriminant built outside `σ(cost)` reduces — via an **exact identity verified
> in code** — to a **clone-slice cardinality**, an invariant already in the
> Inv–Pol dictionary. The collapse therefore **transcends `σ(cost)`**: the
> "everything-is-a-known-object" reading is not an artefact of the cost world.

## The full collapse table (four arenas, nine cycles)

| arena | cycle(s) | the discriminant | what it collapsed to |
|---|---|---|---|
| duality / cover-LP | 1–2 | lift gap `G★ = Cov − LP` | rectangle/biclique-cover LP integrality gap (Lovász) — `docs/duality-gap-theory.md` |
| proof-complexity | 4 | interpolant size `S` vs `P`,`C` | non-canonical; `P`,`C` = KW⁺ matrix (Razborov–Pudlák), forced `P ≤ 2^C` — `docs/bounded-observer.md` |
| meta-complexity (`σ(cost)`) | 5–6, 8–9(A) | `d_flip`; optimal-split DAG geometry | discrete gradient of MCSP-size; reconstructible from the cost table — `docs/tiny-instance-collapse.md` |
| **algebraic CSP (Inv–Pol)** | 10(B), **11** | symmetric-polymorphism profile; **`g(Γ)`** | BLP ⟺ symmetric polymorphisms (Barto–Kozik); **`g = \|Pol₂^{comm,idem}\|`** (this module) |

The recurring mechanism across the first three arenas was *"the
gradient/derivative of a known object is still that object."* The fourth arena
adds a second mechanism: *"the **cardinality of a slice** of a known structure
(the clone) is still dictionary content."*

## What this module makes reproducible

The cycle-11 discriminant is `g(Γ)`: on `D = {0,1,2}` there are exactly **27**
commutative-idempotent binary operations (fixed by the three off-diagonal values
`f(0,1), f(0,2), f(1,2) ∈ D`). The hypothesis was that

```
g(Γ) = #{ those 27 ops that preserve Γ },   quotiented by the unary automorphisms of Γ
```

carries content beyond the known markers (binary-WNU existence, the symmetric
profile, `|Aut|`). On the hand-built catalog of 8 ternary relations it does
separate marker-identical pairs — `between = 8`, `leq = 8`, `lt = 9`, all with
signature `(wnu2, wnu3, σ, |Aut|) = (T, T, (2,3), 1)`. The Adversary killed it
with reductions exact on every row.

### W1 — the Aut-quotient is structurally vacuous

`g` was *defined* as a count quotiented by the unary automorphism action, the one
place it could carry orbit-structure beyond a raw count. It does not: on **all
8/8** catalog rows `g == count_wnu_witnesses` (the raw count). The witness pairs
all have `|Aut| = 1`; and even the only row with non-trivial `Aut` **and** a
non-empty witness set (`cycle3`, `Aut ≅ C₃`) has every conjugation orbit of size
1. Where the hypothesis lives, the quotient reduces nothing → `g` is a **scalar
count**, violating the restart program's admissibility rule (1) (no bare scalars).

### W2 — `g` is a clone-slice cardinality (Inv–Pol)

Computed independently, the column

```
|{ f binary, commutative, idempotent : f ∈ Pol(Γ) }|
```

reproduces `g` **exactly** on all 8 rows `(0, 8, 3, 8, 9, 1, 0, 0)`. So
`g(Γ) = |Pol₂^{comm,idem}(Γ)|` — the size of a fixed slice of the polymorphism
clone, a standard object of the Inv–Pol Galois correspondence. It lives **inside**
the very algebraic language (WNU / symmetric profile) it was meant to transcend.

### W3 — the separation is not encoding-invariant

The only separation `g` claims (`8 / 8 / 9`) is between `between`, `leq`, `lt` —
three **encodings of the same linear order** `0 < 1 < 2`. The split tracks two
elementary markers, **arity** (`between` ternary vs `leq` binary) and
**reflexivity** (`leq` reflexive vs `lt` strict). Adding diagonal elements (a
pp-trivial `x = x` noise) makes `g` jump `9 → 10 → 12 → 6 → 8` non-monotonically:
`g` depends on the reflexive boundary, so it is **not** an invariant of the
underlying structure. This is exactly killer **K2** from Entry 9 (verdict flips
under a benign change of encoding).

## Verdict

Nine consecutive cycles, four independent arenas, one outcome. The fourth arena is
the important one: it was chosen **specifically to escape `σ(cost)`**, in the
`|D| = 3` regime where the CSP dichotomy is genuinely non-classical — and it
**still** collapsed, this time onto the Inv–Pol clone dictionary. This is strong
negative evidence that the "everything-is-a-known-object" reading is robust **not
only in the cost world but in the algebraic-CSP world too**, on finite instances.

## Honesty boundary (binding for this repo)

- This is a statement about the **method** of the loop on **finite** instances
  (`D = {0,1,2}`, relations of arity ≤ 3, binary witnesses among 27 candidates),
  **not** a claim about P vs NP and **not** a lower bound.
- All numbers are **exact** (integer arithmetic, full enumeration of the 27
  commutative-idempotent binary ops and of the symmetric idempotent ops up to
  arity 4). The `wnu3` marker was hardened by the Adversary by enumerating the
  **2187** real ternary symmetric-idempotent operations (not just majority/median),
  confirming the marker signature was not falsified by an under-estimate.
- The catalog is **minuscule** (8 relations) and **hand-built**, not randomly
  sampled. The Aut-quotient being vacuous *here* is **not** a theorem that no `Γ`
  has a non-trivial witness orbit; the Adversary killed `g`-as-measured, not
  `g`-in-general. On the full space of 511 binary relations the quotient is
  non-vacuous in 59 cases, none of which touches the claim.
- `|D| = 3` is the genuinely non-classical Bulatov–Zhuk regime, but the
  **decisive** content lives in **high-arity WNU operations and larger domains**,
  which are out of exact reach here (the `3^(3^3) ≈ 7.6·10¹²` ternary operations
  are never enumerated). What was tested is **below** that decisive threshold —
  this module does not, and cannot, settle the algebraic arena asymptotically.

## Files

```
pnp_lab/csp/polymorphism3.py     # ternary D={0,1,2}: the 27 binary ops, g(Γ), markers, analyze3 — exact
pnp_lab/csp/polymorphism.py      # Boolean precedent (Entry 10, cycle 1): symmetric profile == BLP
tests/test_polymorphism3.py      # exact tests (fast; symmetric profile arity-4 marked slow)
examples/run_polymorphism3.py    # regenerates the g table
```
