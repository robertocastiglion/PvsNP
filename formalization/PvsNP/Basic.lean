/-
  Modulo 4 — Formalizzazione in Lean 4 (solo core, niente mathlib).

  Basic.lean: i mattoni di base.

  Scelta di progetto (onesta). Una formalizzazione PIENA di P e NP richiede un
  modello di calcolo concreto (macchine di Turing con limite di tempo). Qui
  lavoriamo a un livello ASTRATTO: parametrizziamo tutto su un `Model` che
  espone i predicati "calcolabile in tempo polinomiale" con le loro proprietà
  di chiusura, date come assiomi. È legittimo e rigoroso: i teoremi che proviamo
  valgono per OGNI modello che soddisfa quegli assiomi (di sicuro per le TM).
-/

namespace PvsNP

/-- Un input è una stringa di bit. -/
abbrev BitString := List Bool

/-- Un linguaggio è un predicato sulle stringhe. -/
abbrev Language := BitString → Prop

/-- `IsPoly f` : la funzione `f` è limitata da un polinomio. -/
def IsPoly (f : Nat → Nat) : Prop :=
  ∃ c k : Nat, ∀ n, f n ≤ c * (n + 1) ^ k

/-- Un modello di calcolo astratto.

    Espone tre predicati di "tempo polinomiale" (per decisori, verificatori e
    funzioni stringa→stringa) e le minime proprietà di chiusura che servono. -/
structure Model where
  /-- Decisori poly-time: `BitString → Bool`. -/
  PolyDec : (BitString → Bool) → Prop
  /-- Verificatori poly-time: input e testimone. -/
  PolyVer : (BitString → BitString → Bool) → Prop
  /-- Funzioni poly-time `BitString → BitString` (per le riduzioni). -/
  PolyFn  : (BitString → BitString) → Prop
  /-- Ignorare il testimone preserva la poly-time: da un decisore `d`
      otteniamo il verificatore `(x, _) ↦ d x`. -/
  ignoreWitness : ∀ {d : BitString → Bool}, PolyDec d → PolyVer (fun x _ => d x)
  /-- Composizione di funzioni poly-time. -/
  compFn : ∀ {f g : BitString → BitString}, PolyFn f → PolyFn g → PolyFn (g ∘ f)
  /-- Comporre un decisore con una funzione poly-time resta poly-time. -/
  applyFn : ∀ {f : BitString → BitString} {d : BitString → Bool},
    PolyFn f → PolyDec d → PolyDec (fun x => d (f x))

end PvsNP
