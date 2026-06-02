/-
  NaturalProofs.lean — the logical core of the Razborov–Rudich barrier.

  Honesty about scope. The FULL Razborov–Rudich theorem (a natural property that
  is useful against P/poly breaks every pseudorandom generator / every PRF)
  requires the cryptographic construction: out of reach for this mathlib-free core.
  What we DO formalize, kernel-verified, is the entire logical structure:

    • Boolean functions on n variables as truth tables (2^(2^n) of them in all,
      a count that is VERIFIED below);
    • `Useful`  — the property rejects ALL easy functions (a ∀, a WORST-CASE
      condition, exactly as in RR — not an average);
    • `Large`   — the property accepts at least k functions (a constructive count);
    • `Constructive` — an ABSTRACT predicate (like `Model.PolyDec` in Basic.lean):
      not internally expressible, so we expose it as a hypothesis of a model;
    • the RR CORE as a model hypothesis (`rrCore`), and from it the verified
      BARRIER: if cryptography is secure, NO natural proof exists — hence natural
      techniques cannot separate the classes.

  Same style as the abstract `Model` theorems: they hold for EVERY model that
  satisfies the core hypothesis (real cryptography certainly does). Zero `sorry`,
  no `Classical.choice`.
-/
import PvsNP.Concrete

namespace PvsNP.NaturalProofs

open PvsNP

/-- A Boolean function on n variables is given by its truth table: a string of
    2^n bits. -/
abbrev TruthTable := BitString

/-- All Boolean functions on n variables = all truth tables of length 2^n. -/
def allFns (n : Nat) : List TruthTable := stringsOfLen (2 ^ n)

/-- `f` is a function on n variables ⟺ its table has 2^n bits. -/
theorem mem_allFns (n : Nat) (f : TruthTable) :
    f ∈ allFns n ↔ f.length = 2 ^ n := mem_stringsOfLen (2 ^ n) f

/-- The number of truth tables of length m is 2^m. -/
theorem length_stringsOfLen (m : Nat) : (stringsOfLen m).length = 2 ^ m := by
  induction m with
  | zero => rfl
  | succ k ih =>
    rw [stringsOfLen, List.length_append, List.length_map, List.length_map, ih,
        Nat.pow_succ, Nat.mul_two]

/-- **How many Boolean functions there are on n variables: 2^(2^n).** (Verified.)
    This is the size of the space natural proofs must "fish" in. -/
theorem card_allFns (n : Nat) : (allFns n).length = 2 ^ (2 ^ n) :=
  length_stringsOfLen (2 ^ n)

/-- A combinatorial property of Boolean functions: a Bool-valued test on the
    truth table. -/
abbrev Property := TruthTable → Bool

/-- How many functions on n variables satisfy the property. -/
def count (P : Property) (n : Nat) : Nat := (allFns n).countP P

/-- The count never exceeds the total 2^(2^n). -/
theorem count_le_total (P : Property) (n : Nat) : count P n ≤ 2 ^ (2 ^ n) := by
  show (allFns n).countP P ≤ 2 ^ (2 ^ n)
  rw [← card_allFns]
  exact List.countP_le_length

/-- **USEFUL** against the class `easy` (the "easy", low-complexity functions):
    P rejects EVERY easy function. It is a ∀ — a WORST-CASE condition, not an
    average — exactly the "usefulness" condition of Razborov–Rudich. -/
def Useful (P easy : Property) (n : Nat) : Prop :=
  ∀ f ∈ allFns n, easy f = true → P f = false

/-- **LARGE**: P accepts at least `k` functions. (In RR: k ≥ 2^(2^n) · 2^{-O(n)},
    a non-negligible fraction; here parametrized by the threshold `k`.) -/
def Large (P : Property) (n k : Nat) : Prop := count P n ≥ k

/-- The canonical property "f is hard" = "f is not easy". -/
def hardnessProperty (easy : Property) : Property := fun f => !(easy f)

/-- **The hardness property is USEFUL by construction**: it rejects every easy
    function. (Verified — no hypotheses.) -/
theorem hardnessProperty_useful (easy : Property) (n : Nat) :
    Useful (hardnessProperty easy) easy n := by
  intro f _ hf
  show (!(easy f)) = false
  rw [hf]
  rfl

/-- If NO function is easy, the hardness property accepts them all: it is maximally
    large (k = 2^(2^n)). (Verified.) -/
theorem hardnessProperty_large (easy : Property) (n : Nat)
    (h : ∀ f ∈ allFns n, easy f = false) :
    Large (hardnessProperty easy) n (2 ^ (2 ^ n)) := by
  have hall : ∀ f ∈ allFns n, hardnessProperty easy f = true := by
    intro f hf
    show (!(easy f)) = true
    rw [h f hf]
    rfl
  have hcount : count (hardnessProperty easy) n = (allFns n).length :=
    List.countP_eq_length.mpr hall
  show count (hardnessProperty easy) n ≥ 2 ^ (2 ^ n)
  rw [hcount, card_allFns]
  exact Nat.le_refl _

/-- An abstract cryptographic model: it exposes "constructiveness", the existence
    of secure cryptography, and — as a HYPOTHESIS (the part we CITE) — the core of
    Razborov–Rudich: a constructive, useful and large property breaks security. -/
structure CryptoModel where
  /-- Abstract predicate "P is constructive" (efficiently computable). Like
      `Model.PolyDec`, it is not internally expressible: it is a model hypothesis. -/
  Constructive : Property → Prop
  /-- "Secure cryptography exists" (PRG/PRF). -/
  SecurePRG : Prop
  /-- **The core of Razborov–Rudich** (cited): if there exists a property that is
      constructive, useful (against the class `easy` of easy functions) and large
      enough, then cryptography is NOT secure. -/
  rrCore : ∀ {P easy : Property} {n : Nat},
    Constructive P → Useful P easy n → Large P n (2 ^ (2 ^ n) / 2) → ¬ SecurePRG

/-- A **natural proof** in the sense of Razborov–Rudich: a property that is
    constructive, useful against the easy functions, and large (≥ half of all
    functions). -/
def NaturalProperty (M : CryptoModel) (P easy : Property) (n : Nat) : Prop :=
  M.Constructive P ∧ Useful P easy n ∧ Large P n (2 ^ (2 ^ n) / 2)

/-- **The Razborov–Rudich barrier, verified.** If cryptography is secure, then NO
    natural proof exists — hence no "natural" technique (constructive + large) can
    separate the classes. This is the deep reason almost all known lower-bound
    techniques are blocked. -/
theorem rr_barrier (M : CryptoModel) (hsec : M.SecurePRG) :
    ¬ ∃ (P easy : Property) (n : Nat), NaturalProperty M P easy n := by
  rintro ⟨P, easy, n, hC, hU, hL⟩
  exact (M.rrCore hC hU hL) hsec

/-- Contrapositive form: the existence of a natural proof REFUTES cryptographic
    security. (This is the "offensive" use of the theorem: a natural property is
    an attack on every PRG.) -/
theorem natural_property_breaks_crypto (M : CryptoModel)
    {P easy : Property} {n : Nat} (h : NaturalProperty M P easy n) : ¬ M.SecurePRG := by
  obtain ⟨hC, hU, hL⟩ := h
  exact M.rrCore hC hU hL

end PvsNP.NaturalProofs
