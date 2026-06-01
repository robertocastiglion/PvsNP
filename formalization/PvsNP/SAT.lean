/-
  SAT.lean — sintassi e semantica CONCRETE di CNF-SAT.

  È il "bersaglio" del teorema di Cook–Levin reso tangibile. Onestà: NON
  dimostriamo qui Cook–Levin per intero (ogni linguaggio NP si riduce a SAT) —
  serve un modello di macchina e la costruzione a tableau, fuori dalla portata
  di questo nucleo senza mathlib. Costruiamo però l'oggetto SAT in modo esatto e
  ne dimostriamo, verificate dal kernel:

    • la FORMA-NP: il testimone è un assegnamento, il verificatore è il
      valutatore — una funzione totale e calcolabile (`sat_iff_witness`);
    • la semantica della congiunzione (`eval_append`) e la monotonìa
      (più clausole ⇒ più difficile, `sat_append_left`);
    • la clausola vuota è insoddisfacibile (`not_sat_of_nil_clause`) — il caso
      base della refutazione per risoluzione (cfr. Modulo 5);
    • una RIDUZIONE verificata che preserva la soddisfacibilità: il rinominare
      le variabili lungo una sostituzione (`eval_rename`, `sat_of_sat_rename`),
      il mattone elementare di ogni riduzione many-one fra istanze SAT.
-/

namespace PvsNP.SAT

/-- Un letterale: una variabile (per indice) con una polarità. -/
structure Lit where
  var : Nat
  pos : Bool
  deriving DecidableEq

/-- Una clausola è una disgiunzione di letterali. -/
abbrev Clause := List Lit
/-- Una formula CNF è una congiunzione di clausole. -/
abbrev CNF := List Clause
/-- Un assegnamento dà un valore di verità a ogni variabile. -/
abbrev Assign := Nat → Bool

/-- Valore di verità di un letterale sotto un assegnamento. -/
def Lit.eval (σ : Assign) (l : Lit) : Bool :=
  if l.pos then σ l.var else !σ l.var

/-- Una clausola è vera se almeno un letterale è vero (OR). -/
def Clause.eval (σ : Assign) (c : Clause) : Bool := c.any (Lit.eval σ)

/-- Una CNF è vera se ogni clausola è vera (AND). -/
def CNF.eval (σ : Assign) (φ : CNF) : Bool := φ.all (Clause.eval σ)

/-- Soddisfacibilità: esiste un assegnamento che rende vera la CNF. -/
def Sat (φ : CNF) : Prop := ∃ σ : Assign, CNF.eval σ φ = true

/-- **Forma-NP di SAT.** Il testimone è un assegnamento, il verificatore è il
    valutatore `CNF.eval` (totale e calcolabile). È esattamente lo schema di NP;
    manca solo il limite polinomiale sul testimone, che nel framework astratto è
    l'ipotesi `PolyVer`. -/
theorem sat_iff_witness (φ : CNF) :
    Sat φ ↔ ∃ σ : Assign, CNF.eval σ φ = true := Iff.rfl

/-- La CNF vuota (nessuna clausola) è soddisfatta da qualunque assegnamento. -/
theorem sat_nil : Sat ([] : CNF) := ⟨fun _ => false, rfl⟩

/-- Una clausola vuota rende la formula insoddisfacibile: nessun letterale può
    renderla vera. È il caso base della refutazione (la "clausola vuota" ⊥). -/
theorem not_sat_of_nil_clause (φ : CNF) (h : ([] : Clause) ∈ φ) : ¬ Sat φ := by
  rintro ⟨σ, hσ⟩
  have hall := (List.all_eq_true).mp hσ
  have hc : Clause.eval σ [] = true := hall [] h
  simp [Clause.eval] at hc

/-- Semantica della congiunzione: una CNF concatenata è vera se e solo se lo
    sono entrambe le parti. -/
theorem eval_append (σ : Assign) (φ ψ : CNF) :
    CNF.eval σ (φ ++ ψ) = (CNF.eval σ φ && CNF.eval σ ψ) := by
  simp [CNF.eval, List.all_append]

/-- Monotonìa: aggiungere clausole può solo restringere le soluzioni. Se
    `φ ++ ψ` è soddisfacibile, lo è anche `φ`. -/
theorem sat_append_left (φ ψ : CNF) (h : Sat (φ ++ ψ)) : Sat φ := by
  obtain ⟨σ, hσ⟩ := h
  rw [eval_append] at hσ
  refine ⟨σ, ?_⟩
  revert hσ
  cases CNF.eval σ φ <;> cases CNF.eval σ ψ <;> simp

-- Rinomina (sostituzione) delle variabili lungo `ρ : Nat → Nat`.

/-- Rinomina la variabile di un letterale. -/
def renameLit (ρ : Nat → Nat) (l : Lit) : Lit := ⟨ρ l.var, l.pos⟩
/-- Rinomina le variabili di una clausola. -/
def renameClause (ρ : Nat → Nat) (c : Clause) : Clause := c.map (renameLit ρ)
/-- Rinomina le variabili di una CNF. -/
def rename (ρ : Nat → Nat) (φ : CNF) : CNF := φ.map (renameClause ρ)

/-- Valutare un letterale rinominato sotto `σ` = valutarlo sotto `σ ∘ ρ`. -/
theorem lit_eval_rename (ρ : Nat → Nat) (σ : Assign) (l : Lit) :
    Lit.eval σ (renameLit ρ l) = Lit.eval (fun v => σ (ρ v)) l := rfl

/-- Stessa cosa a livello di clausola (per induzione sui letterali). -/
theorem clause_eval_rename (ρ : Nat → Nat) (σ : Assign) (c : Clause) :
    Clause.eval σ (renameClause ρ c) = Clause.eval (fun v => σ (ρ v)) c := by
  induction c with
  | nil => rfl
  | cons l cs ih =>
    simp only [renameClause, List.map_cons, Clause.eval, List.any_cons] at *
    rw [lit_eval_rename, ih]

/-- **Lemma di sostituzione.** Valutare `φ` con l'assegnamento composto `σ ∘ ρ`
    equivale a valutare la formula rinominata `rename ρ φ` con `σ`. È il cuore
    di ogni riduzione fra istanze SAT che agisce rinominando le variabili. -/
theorem eval_rename (ρ : Nat → Nat) (σ : Assign) (φ : CNF) :
    CNF.eval (fun v => σ (ρ v)) φ = CNF.eval σ (rename ρ φ) := by
  induction φ with
  | nil => rfl
  | cons c cs ih =>
    simp only [rename, List.map_cons, CNF.eval, List.all_cons] at *
    rw [clause_eval_rename, ih]

/-- **Riduzione verificata (una direzione).** Se la formula rinominata è
    soddisfacibile, lo è anche l'originale: l'assegnamento `σ ∘ ρ` testimonia.
    (Il converso vale quando `ρ` è iniettiva.) -/
theorem sat_of_sat_rename (ρ : Nat → Nat) (φ : CNF)
    (h : Sat (rename ρ φ)) : Sat φ := by
  obtain ⟨σ, hσ⟩ := h
  exact ⟨fun v => σ (ρ v), by rw [eval_rename]; exact hσ⟩

end PvsNP.SAT
