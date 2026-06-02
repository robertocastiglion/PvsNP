# A time-bounded machine model and the tableau skeleton of Cook–Levin (Lean)

*Lean formalization thread implemented on 2026-06-02. Adds the row level of the
Cook–Levin reduction on top of the existing cell level.*

## Goal

`CookLevin.lean` already verified the **cell** level of Cook–Levin: every local
window constraint is a CNF (`canonical_correct` — "every Boolean function is a
CNF"). What was missing, and only cited, were two things: a **time-bounded
machine model** and the **tableau wiring** that turns a computation into that CNF.
`Tableau.lean` adds the **row** level, kernel-verified.

This is a *piece* of the full theorem (every NP language ≤ SAT), not the whole
thing — stated honestly below.

## What is verified (`PvsNP.Tableau`)

- **`Machine`** — a deterministic computation model: a configuration type, a
  one-step transition `step`, and an acceptance test. Time is **explicit**:
  `Machine.run c0 T` runs `T` steps, `Machine.accepts c0 T` tests the `T`-th
  configuration. This is the time-bounded model that was previously only cited.
- **`ValidUpTo M c0 t T`** — a *tableau*: a candidate sequence `t 0, t 1, …` is
  valid up to time `T` when `t 0 = c0` **and** `∀ i < T, t (i+1) = step (t i)`.
  The second conjunct is a **conjunction of local constraints** (each relates only
  `t i` and `t (i+1)`) — exactly the structure Cook–Levin SAT-encodes.
- **`run_validUpTo`** — the real computation is a valid tableau.
- **`validUpTo_eq_run`** — *determinism pins the tableau down*: any valid tableau
  equals the real run on `[0, T]`. A tableau cannot cheat the local constraints.
- **`accepts_iff_validUpTo`** — **the headline**:

  > `M.accepts c0 T = true  ↔  ∃ t, ValidUpTo M c0 t T ∧ M.accept (t T) = true`

  i.e. *the machine accepts within `T` steps iff there is a valid accepting
  tableau of height `T`*. This is precisely the equivalence the SAT encoding
  realizes ("∃ valid accepting computation ⟺ ∃ satisfying assignment"), here the
  row-level half, proved with no axioms.
- **`window_constraint_is_cnf`** — the bridge: re-exposes the cell-level
  `canonical_correct`, so the row level and the cell level sit side by side.
- **`counter` / `counter_accepts_at_3` / `counter_has_accepting_tableau`** — a
  concrete machine (a counter accepting at 3) showing the model is non-vacuous and
  the equivalence fires on a real instance.

## Axiom hygiene

`lake env lean Check.lean` confirms all five new theorems
(`run_validUpTo`, `validUpTo_eq_run`, `accepts_iff_validUpTo`,
`counter_accepts_at_3`, `counter_has_accepting_tableau`) **depend on no axioms** —
fully constructive, never `Classical.choice`. The whole development builds with
`lake build` with **no warnings**; total **41 kernel-verified theorems**, zero
`sorry`.

## Honesty boundary

- **Verified**: the time-bounded machine model, the tableau equivalence, the
  locality decomposition (validity = conjunction of local step constraints), and
  the bridge to the cell-level CNF.
- **Cited / remaining**: the bit-level encoding of a *specific* NP verifier's
  transition function as forbidden windows, stacked across the tableau rows, that
  produces a single CNF whose satisfiability equals acceptance. That is the
  laborious wiring; the two endpoints (row-level equivalence and cell-level
  local→CNF) are now both formalized.
- This does **not** prove P vs NP. It hardens the framework: Cook–Levin's
  structural skeleton is now kernel-checked, not assumed.

## Files

```
formalization/PvsNP/Tableau.lean   # Machine, run, ValidUpTo, accepts_iff_validUpTo, counter
formalization/PvsNP/CookLevin.lean # cell level: local window → CNF (canonical_correct)
formalization/Check.lean           # #print axioms for the tableau theorems
```
