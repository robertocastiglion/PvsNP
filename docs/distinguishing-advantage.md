# Distinguishing Advantage Sandbox (Module 15) — barriers as bounded-observer indistinguishability

*Implemented on 2026-06-03. Turns a theory conclusion into an exact finite-size
measurement.*

## Why this module exists

A long analysis of the five barriers (relativization, algebrization, natural
proofs, proof complexity, meta-complexity) led to a precise conclusion:

> A purely **informational** quantity `I(T,f)` ("how many bits a proof technique
> extracts") **cannot** unify the barriers, because Natural Proofs sees the whole
> `2^n`-bit truth table (information is *saturated*) yet is still blocked. The
> obstruction there is on **computation**, not information.

The correct common template is **indistinguishability against a resource-bounded
observer**, where the resource lives on two *orthogonal* axes:

- **Information** — how many bits the observer reads per local probe;
- **Computation** — how it is allowed to combine those probes.

This module makes that template **executable** on a tiny instance and *measures*
whether the two axes are genuinely both needed.

## The experiment

The observer (a **distinguisher**) receives the truth table of a function on
`n = 3` variables — `2^3 = 8` bits — and tries to decide whether the function is
**hard** (high formula complexity, an MCSP "yes-it's-hard" instance) or **easy**
(low complexity). We measure its distinguishing advantage

```
ε(ℓ, s) = max_D | Pr_{f hard}[D(f)=1] − Pr_{f easy}[D(f)=1] |
```

over two orthogonal budgets of the distinguisher:

| axis | knob | meaning |
|---|---|---|
| **information** | `ℓ` | fan-in of the *oracle gates* — bits read per local probe |
| **computation** | `s` | number of binary gates (∧, ∨; ¬ free) combining the probes |

- **Oracle gates** are the *symmetric* (counting) functions of any window of width
  `≤ ℓ` of the 8 truth-table bits: ∧, ∨, ⊕ (parity), majority, thresholds. Using
  `≤ ℓ` makes the basis cumulative, so the class is **monotone in `ℓ`**.
- The **hard / easy split** reuses Module 6 (`min_formula_sizes(3)`, exact formula
  complexity of all 256 functions) and the MCSP notion of Module 13. Default
  threshold τ = median complexity, so the two classes are balanced.

## What it measured (exact, n=3)

```
            s=1      s=2      s=3      ← computation (gates)
  ℓ=1     0.102    0.121    0.236
  ℓ=2     0.258    0.324   ≥0.324
  ℓ=3     0.264   ≥0.324   ≥0.324      (≥ = certified lower bound)
  ↑ information (oracle-gate fan-in)
```

Reading the corner against the edges:

```
  floor      (ℓ=1, s=1) = 0.102
  info only  (ℓ=3, s=1) = 0.264     much info, little computation
  comp only  (ℓ=1, s=3) = 0.236     little info, much computation
  both       (ℓ=3, s=3) = 0.324
```

**Both axes contribute.** The corner strictly beats *both* edges: adding
computation to wide probes raises 0.264 → ≥0.324, and adding information to a
deep combiner raises 0.236 → ≥0.324. Neither information nor computation **alone**
saturates the advantage on this instance — exactly the bounded-observer trade-off
the theory predicts, now visible as a number.

## Honesty boundary (binding for this repo)

- This is an **exact** measurement on **finite size** (`n=3`, 8 bits, 256
  functions), **not** the asymptotic proof of a barrier. At `n=3` the "wall"
  *cannot* be visible — that needs `n → ∞`. We only see the *geometry* of the
  trade-off on a toy instance.
- The oracle gates use a **canonical** repertoire (symmetric functions of
  contiguous windows), not all `2^(2^ℓ)` local lookups. With arbitrary lookups
  the closure under `≤ s` gates explodes (millions of 256-bit functions,
  out-of-memory already at `ℓ=2`). The restriction is deliberate and documented.
- High-resource cells (large `ℓ` and `s`) are too large to enumerate exhaustively;
  they are reported as **certified lower bounds** (`≥`, `exact=False`), then
  monotonically tightened using `C(ℓ',s') ⊆ C(ℓ,s)`. The conclusion "both axes
  contribute" is robust because the two edges are *exact* and below the corner.
  The very explosion of the computation-rich corner is the finite-size shadow of
  why exhaustive lower-bound certification is hard.
- Reuses the Module 6 evaluation engine; it does **not** rewrite the circuit
  evaluator. It does **not** prove (or touch) P vs NP.

## Files

```
pnp_lab/distinguishing/advantage.py     # split, oracle-gate basis, ε(ℓ,s) DP
pnp_lab/distinguishing/lab.py           # ASCII matrix + SVG heatmap
tests/test_distinguishing_advantage.py  # 10 exact tests
examples/run_distinguishing_advantage.py
web/assets/distinguishing_advantage.svg # the ε(ℓ,s) heatmap
```
