/-
  Tableau.lean — the time-bounded machine model and the tableau skeleton of
  Cook–Levin (a verified PIECE of the full reduction).

  Scope, honestly. The full Cook–Levin theorem (every NP language reduces to SAT)
  needs (a) a concrete time-bounded machine model, (b) the tableau wiring that
  turns a computation into a CNF. `CookLevin.lean` already verified the *cell*
  level: every local window constraint is a CNF (`canonical_correct`). This file
  adds the missing *row* level, kernel-verified:

    • `Machine` — a deterministic computation model with an EXPLICIT time bound
      (run for `T` steps); this is "the time-bounded machine" that was previously
      only cited;
    • `ValidUpTo` — a *tableau*: a sequence of configurations whose validity is
      the conjunction of LOCAL constraints (`t (i+1) = step (t i)` for `i < T`),
      exactly the structure Cook–Levin SAT-encodes;
    • `accepts_iff_validUpTo` — the headline equivalence: the machine accepts
      within `T` steps **iff** there exists a valid tableau of height `T` ending
      in an accepting configuration. This is the row-level heart of the reduction.

  The bridge `window_constraint_is_cnf` re-exposes the cell-level result
  (`canonical_correct`) so the two layers sit side by side. What remains — the
  bit-level encoding of a *specific* NP verifier's step function as forbidden
  windows — is the laborious part we still CITE.

  Constructive throughout: induction only, no `Classical.choice`.
-/
import PvsNP.CookLevin

namespace PvsNP.Tableau

/-- A deterministic machine: a configuration type, a single-step transition, and
    an acceptance test on configurations. Time is made explicit by running for a
    fixed number of steps (`Machine.run` / `Machine.accepts`), so this is a
    genuinely TIME-BOUNDED model. -/
structure Machine where
  /-- The (opaque) type of configurations. -/
  Config : Type
  /-- One computation step. -/
  step : Config → Config
  /-- Whether a configuration is accepting. -/
  accept : Config → Bool

/-- The configuration after running `T` steps from `c0`. -/
def Machine.run (M : Machine) (c0 : M.Config) : Nat → M.Config
  | 0 => c0
  | n + 1 => M.step (M.run c0 n)

/-- The machine accepts `c0` within `T` steps if the `T`-th configuration is
    accepting. (Time bound `T` is explicit — the point of this model.) -/
def Machine.accepts (M : Machine) (c0 : M.Config) (T : Nat) : Bool :=
  M.accept (M.run c0 T)

/-- A **tableau**: a candidate sequence of configurations `t 0, t 1, …`. It is
    *valid up to time `T`* when it starts at `c0` and every adjacent pair is a
    legal step. The second conjunct is a conjunction of LOCAL constraints — each
    relates only `t i` and `t (i+1)` — which is precisely what Cook–Levin turns
    into clauses. -/
def ValidUpTo (M : Machine) (c0 : M.Config) (t : Nat → M.Config) (T : Nat) : Prop :=
  t 0 = c0 ∧ ∀ i, i < T → t (i + 1) = M.step (t i)

/-- The actual run is itself a valid tableau (the "honest" computation). -/
theorem run_validUpTo (M : Machine) (c0 : M.Config) (T : Nat) :
    ValidUpTo M c0 (M.run c0) T := by
  refine ⟨rfl, ?_⟩
  intro i _
  rfl

/-- **Determinism ⇒ uniqueness of the tableau.** Any valid tableau must coincide
    with the real run on `[0, T]`. So a tableau cannot "cheat": the local step
    constraints pin it down completely. -/
theorem validUpTo_eq_run (M : Machine) (c0 : M.Config) (t : Nat → M.Config) (T : Nat)
    (h : ValidUpTo M c0 t T) : ∀ i, i ≤ T → t i = M.run c0 i := by
  obtain ⟨h0, hstep⟩ := h
  intro i
  induction i with
  | zero =>
    intro _
    rw [h0]
    rfl
  | succ k ih =>
    intro hk
    have hk' : k < T := Nat.lt_of_succ_le hk
    have hkle : k ≤ T := Nat.le_of_lt hk'
    rw [hstep k hk', ih hkle]
    rfl

/-- **The tableau equivalence — the row-level heart of Cook–Levin.** The machine
    accepts `c0` within `T` steps **iff** there is a valid tableau of height `T`
    whose last configuration is accepting. This is exactly the statement the SAT
    encoding realizes: «∃ valid accepting computation» ⟺ «∃ satisfying assignment».
    Verified by the kernel. -/
theorem accepts_iff_validUpTo (M : Machine) (c0 : M.Config) (T : Nat) :
    M.accepts c0 T = true ↔
      ∃ t : Nat → M.Config, ValidUpTo M c0 t T ∧ M.accept (t T) = true := by
  constructor
  · intro h
    exact ⟨M.run c0, run_validUpTo M c0 T, h⟩
  · rintro ⟨t, hvalid, hacc⟩
    have hT : t T = M.run c0 T := validUpTo_eq_run M c0 t T hvalid T (Nat.le_refl T)
    show M.accept (M.run c0 T) = true
    rw [← hT]
    exact hacc

/-- **Bridge to the cell level** (from `CookLevin.lean`). A single local window
    constraint — "the assignment avoids these forbidden patterns" — is *exactly*
    a CNF. Stacking such windows across consecutive tableau rows (the wiring of a
    concrete bit-encoded machine) is the remaining, cited part. Re-exposed here so
    the row level (`accepts_iff_validUpTo`) and the cell level sit together. -/
theorem window_constraint_is_cnf (σ : PvsNP.SAT.Assign) (forbids : List (List Bool)) :
    PvsNP.SAT.CNF.eval σ (PvsNP.SAT.canonicalCNF forbids) = true
      ↔ ∀ a ∈ forbids, ¬ PvsNP.SAT.matchesFrom σ 0 a :=
  PvsNP.SAT.canonical_correct σ forbids

/- ─────────────────────────────────────────────────────────────────────────
   A concrete machine, to show the model is non-vacuous (zero axioms).
   ───────────────────────────────────────────────────────────────────────── -/

/-- A trivial counter machine: configuration = a number, step = successor,
    accepting at exactly 3. -/
def counter : Machine where
  Config := Nat
  step := Nat.succ
  accept := fun c => decide (c = 3)

/-- Running the counter from 0 for `n` steps lands on `n`. -/
theorem counter_run (n : Nat) : counter.run (0 : Nat) n = n := by
  induction n with
  | zero => rfl
  | succ k ih =>
    show Nat.succ (counter.run (0 : Nat) k) = k + 1
    rw [ih]

/-- The counter accepts (reaches 3) in exactly 3 steps — the model really runs.
    Everything is concrete computation, so the kernel checks it by `rfl`. -/
theorem counter_accepts_at_3 : counter.accepts (0 : Nat) 3 = true := rfl

/-- …and there is a valid accepting tableau for it (the equivalence, instantiated). -/
theorem counter_has_accepting_tableau :
    ∃ t : Nat → Nat, ValidUpTo counter (0 : Nat) t 3 ∧ counter.accept (t 3) = true :=
  (accepts_iff_validUpTo counter (0 : Nat) 3).mp counter_accepts_at_3

end PvsNP.Tableau
