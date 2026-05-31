/-
  Classes.lean: le classi P e NP, e il teorema P ⊆ NP.
-/
import PvsNP.Basic

namespace PvsNP

/-- `P M L` : il linguaggio `L` è deciso da un decisore poly-time. -/
def P (M : Model) (L : Language) : Prop :=
  ∃ d : BitString → Bool, M.PolyDec d ∧ ∀ x, L x ↔ d x = true

/-- `NP M L` : caratterizzazione tramite verificatore. Esiste un limite
    polinomiale `p` e un verificatore poly-time `V` tali che `x ∈ L` se e solo
    se esiste un testimone `w` di lunghezza ≤ `p (|x|)` accettato da `V`. -/
def NP (M : Model) (L : Language) : Prop :=
  ∃ (p : Nat → Nat) (V : BitString → BitString → Bool),
    IsPoly p ∧ M.PolyVer V ∧
      ∀ x, L x ↔ ∃ w : BitString, w.length ≤ p x.length ∧ V x w = true

/-- P ⊆ NP. Un decisore diventa un verificatore che ignora il testimone:
    il testimone vuoto basta, con limite polinomiale nullo. -/
theorem P_subset_NP (M : Model) (L : Language) (h : P M L) : NP M L := by
  cases h with
  | intro d hrest =>
    cases hrest with
    | intro hd hiff =>
      refine ⟨fun _ => 0, (fun x _ => d x), ⟨0, 0, ?_⟩, M.ignoreWitness hd, ?_⟩
      · intro n
        exact Nat.zero_le _
      · intro x
        apply Iff.intro
        · intro hx
          exact ⟨[], Nat.zero_le _, (hiff x).mp hx⟩
        · intro hw
          cases hw with
          | intro w hwp =>
            exact (hiff x).mpr hwp.2

/-- "P = NP" nel modello `M`: le due classi coincidono. -/
def PEqNP (M : Model) : Prop := ∀ L, P M L ↔ NP M L

/-- La congettura P ≠ NP nel modello `M`. -/
def PNeqNP (M : Model) : Prop := ¬ PEqNP M

end PvsNP
