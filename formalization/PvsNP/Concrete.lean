/-
  Concrete.lean — un MODELLO concreto che soddisfa gli assiomi astratti.

  Chiude una lacuna di rigore. Finora `Model` era solo una struttura: se nessun
  modello la soddisfacesse, i teoremi sarebbero vacui. Qui ne costruiamo uno
  esplicito — il modello "senza limiti di tempo" — e dimostriamo, in modo
  COSTRUTTIVO (zero assiomi, nemmeno `Classical.choice`), che in esso P = NP:
  la forza bruta enumera tutti i testimoni e decide ogni problema NP.

  Conseguenze:
    • il framework è NON vacuo: i teoremi parlano di qualcosa di reale;
    • realizziamo concretamente il "mondo P = NP" della barriera di
      relativizzazione (`collapse_world_exists`), prima solo postulato.

  La forza bruta è esponenziale, quindi questo modello NON rispetta limiti
  polinomiali — ed è esattamente il punto: senza il vincolo di tempo, NP ⊆ P.
-/
import PvsNP.Basic
import PvsNP.Classes
import PvsNP.Barriers

namespace PvsNP

/-- Tutte le stringhe di bit di lunghezza esattamente `n`. -/
def stringsOfLen : Nat → List BitString
  | 0 => [[]]
  | n + 1 => (stringsOfLen n).map (false :: ·) ++ (stringsOfLen n).map (true :: ·)

/-- `w` appartiene a `stringsOfLen n` se e solo se ha lunghezza `n`.
    Dimostrazione costruttiva (niente `simp` classico): zero assiomi. -/
theorem mem_stringsOfLen (n : Nat) (w : BitString) :
    w ∈ stringsOfLen n ↔ w.length = n := by
  induction n generalizing w with
  | zero =>
    constructor
    · intro h
      rw [stringsOfLen, List.mem_singleton] at h
      subst h; rfl
    · intro h
      rw [stringsOfLen, List.mem_singleton]
      exact List.length_eq_zero_iff.mp h
  | succ n ih =>
    rw [stringsOfLen, List.mem_append, List.mem_map, List.mem_map]
    constructor
    · intro h
      rcases h with ⟨v, hv, hvw⟩ | ⟨v, hv, hvw⟩
      · subst hvw; rw [List.length_cons, (ih v).mp hv]
      · subst hvw; rw [List.length_cons, (ih v).mp hv]
    · intro h
      cases w with
      | nil =>
        rw [List.length_nil] at h
        exact absurd h.symm (Nat.succ_ne_zero n)
      | cons b v =>
        rw [List.length_cons] at h
        have hv : v.length = n := by omega
        cases b with
        | false => exact Or.inl ⟨v, (ih v).mpr hv, rfl⟩
        | true => exact Or.inr ⟨v, (ih v).mpr hv, rfl⟩

/-- Tutte le stringhe di bit di lunghezza al più `n`. -/
def allUpTo : Nat → List BitString
  | 0 => stringsOfLen 0
  | n + 1 => allUpTo n ++ stringsOfLen (n + 1)

/-- `w` appartiene a `allUpTo n` se e solo se ha lunghezza ≤ `n`.
    Dimostrazione costruttiva (niente `omega` sugli `↔`, niente choice). -/
theorem mem_allUpTo (n : Nat) (w : BitString) :
    w ∈ allUpTo n ↔ w.length ≤ n := by
  induction n with
  | zero =>
    rw [allUpTo, mem_stringsOfLen]
    exact Nat.le_zero.symm
  | succ n ih =>
    rw [allUpTo, List.mem_append, ih, mem_stringsOfLen]
    constructor
    · rintro (h | h)
      · exact Nat.le_succ_of_le h
      · exact Nat.le_of_eq h
    · intro h
      rcases Nat.lt_or_ge w.length (n + 1) with hlt | hge
      · exact Or.inl (Nat.lt_succ_iff.mp hlt)
      · exact Or.inr (Nat.le_antisymm h hge)

/-- Il modello "senza limiti": ammette ogni funzione (i predicati sono `True`).
    Soddisfa banalmente tutte le chiusure, perché le conclusioni sono `True`. -/
def Model.unbounded : Model where
  PolyDec := fun _ => True
  PolyVer := fun _ => True
  PolyFn := fun _ => True
  ignoreWitness := fun _ => trivial
  compFn := fun _ _ => trivial
  applyFn := fun _ _ => trivial
  idFn := trivial

/-- Nel modello senza limiti, ogni problema NP è in P: il decisore enumera per
    forza bruta tutti i testimoni di lunghezza ≤ p(|x|) e controlla il
    verificatore. Tutto costruttivo. -/
theorem unbounded_NP_subset_P (L : Language)
    (h : NP Model.unbounded L) : P Model.unbounded L := by
  obtain ⟨p, V, _hp, _hV, hiff⟩ := h
  refine ⟨fun x => (allUpTo (p x.length)).any (fun w => V x w), trivial, ?_⟩
  intro x
  rw [hiff x, List.any_eq_true]
  constructor
  · rintro ⟨w, hw, hVw⟩
    exact ⟨w, (mem_allUpTo _ _).mpr hw, hVw⟩
  · rintro ⟨w, hwmem, hVw⟩
    exact ⟨w, (mem_allUpTo _ _).mp hwmem, hVw⟩

/-- Nel modello senza limiti vale P = NP. -/
theorem unbounded_PEqNP : PEqNP Model.unbounded := by
  intro L
  exact ⟨fun h => P_subset_NP Model.unbounded L h,
         fun h => unbounded_NP_subset_P L h⟩

/-- Il "mondo P = NP" della barriera di relativizzazione, ora CONCRETO: esiste
    davvero un modello in cui le due classi coincidono. (L'altro mondo, P ≠ NP,
    è il lato difficile: relativizzato è la costruzione BGS del Modulo 2.) -/
theorem collapse_world_exists : ∃ M : Model, PEqNP M :=
  ⟨Model.unbounded, unbounded_PEqNP⟩

end PvsNP
