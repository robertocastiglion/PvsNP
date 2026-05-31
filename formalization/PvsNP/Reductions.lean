/-
  Reductions.lean: riduzioni poly-time, NP-hardness, NP-completezza,
  e il collasso "se un problema NP-completo è in P allora P = NP".
-/
import PvsNP.Basic
import PvsNP.Classes

namespace PvsNP

/-- Riduzione many-one poly-time da `A` a `B`: una funzione poly-time `f` con
    `x ∈ A ↔ f x ∈ B`. -/
def PolyReducible (M : Model) (A B : Language) : Prop :=
  ∃ f : BitString → BitString, M.PolyFn f ∧ ∀ x, A x ↔ B (f x)

/-- Le riduzioni poly-time sono transitive. -/
theorem reduces_trans (M : Model) (A B C : Language)
    (hAB : PolyReducible M A B) (hBC : PolyReducible M B C) :
    PolyReducible M A C := by
  cases hAB with
  | intro f hf =>
    cases hf with
    | intro hfp hfiff =>
      cases hBC with
      | intro g hg =>
        cases hg with
        | intro hgp hgiff =>
          exact ⟨g ∘ f, M.compFn hfp hgp,
                 fun x => Iff.trans (hfiff x) (hgiff (f x))⟩

/-- P è chiusa rispetto alle riduzioni: se `A ≤ B` e `B ∈ P` allora `A ∈ P`. -/
theorem P_closed_reduction (M : Model) (A B : Language)
    (hred : PolyReducible M A B) (hB : P M B) : P M A := by
  cases hred with
  | intro f hf =>
    cases hf with
    | intro hfp hfiff =>
      cases hB with
      | intro d hd =>
        cases hd with
        | intro hdp hdiff =>
          exact ⟨fun x => d (f x), M.applyFn hfp hdp,
                 fun x => Iff.trans (hfiff x) (hdiff (f x))⟩

/-- `L` è NP-hard: ogni linguaggio in NP si riduce a `L`. -/
def NPHard (M : Model) (L : Language) : Prop :=
  ∀ A : Language, NP M A → PolyReducible M A L

/-- `L` è NP-completo: è in NP ed è NP-hard. -/
def NPComplete (M : Model) (L : Language) : Prop :=
  NP M L ∧ NPHard M L

/-- Collasso di Cook: se un linguaggio NP-completo è in P, allora P = NP. -/
theorem complete_in_P_implies_PEqNP (M : Model) (L : Language)
    (hC : NPComplete M L) (hLP : P M L) : PEqNP M := by
  intro A
  apply Iff.intro
  · intro hPA
    exact P_subset_NP M A hPA
  · intro hNA
    exact P_closed_reduction M A L (hC.2 A hNA) hLP

end PvsNP
