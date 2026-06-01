/-
  CookLevin.lean — il cuore verificato della riduzione di Cook–Levin.

  Onestà sullo scopo. Cook–Levin PER INTERO (ogni linguaggio in NP si riduce a
  SAT) richiede un modello di macchina con limite di tempo e la costruzione a
  tableau: fuori dalla portata di questo nucleo senza mathlib (non c'è nemmeno in
  mathlib). Formalizziamo però il PASSO IRRIDUCIBILE della costruzione, quello
  che fa tutto il lavoro concettuale:

      la validità di una computazione è una CONGIUNZIONE di vincoli LOCALI
      (le "finestre" del tableau), e ogni vincolo locale booleano si scrive
      come una CNF.

  Qui lo dimostriamo, verificato dal kernel:
    • `forbidFrom i a`  — la clausola che vieta ESATTAMENTE il pattern `a` a
      partire dalla variabile `i` (la localitità: una finestra a posizione i);
    • `forbid_eval_false` — quella clausola è falsa esattamente sugli
      assegnamenti che combaciano col pattern vietato;
    • `canonicalCNF` + `canonical_correct` — congiungendo i divieti si ottiene
      una CNF soddisfatta esattamente dagli assegnamenti che evitano TUTTI i
      pattern vietati: cioè OGNI funzione booleana è una CNF. È la forma normale
      che trasforma «computazione valida» in «formula soddisfacibile».

  Mettendo i vincoli a offset diversi (`forbidFrom i`) si cablano le finestre del
  tableau: quel cablaggio (e il modello di macchina) è la parte che CITIAMO.
-/
import PvsNP.SAT

namespace PvsNP.SAT

/-- `matchesFrom σ i a` : l'assegnamento σ combacia col pattern `a` (lista di bit)
    a partire dalla variabile `i`. -/
def matchesFrom (σ : Assign) : Nat → List Bool → Prop
  | _, [] => True
  | i, b :: bs => σ i = b ∧ matchesFrom σ (i + 1) bs

/-- La clausola che VIETA il pattern `a` a partire dalla variabile `i`: è falsa
    esattamente quando σ combacia col pattern. Per ogni bit `b` mette il
    letterale che chiede l'opposto, così la disgiunzione è vera appena UN bit
    differisce. -/
def forbidFrom : Nat → List Bool → Clause
  | _, [] => []
  | i, b :: bs => (⟨i, !b⟩ : Lit) :: forbidFrom (i + 1) bs

/-- Un letterale `⟨i, !b⟩` è falso esattamente quando `σ i = b`. -/
theorem lit_forbid_false (σ : Assign) (i : Nat) (b : Bool) :
    Lit.eval σ ⟨i, !b⟩ = false ↔ σ i = b := by
  cases b <;> cases hσ : σ i <;> simp [Lit.eval, hσ]

/-- La clausola-divieto è falsa esattamente sugli assegnamenti che combaciano
    col pattern vietato. È il fatto-chiave della codifica locale. -/
theorem forbid_eval_false (σ : Assign) (i : Nat) (a : List Bool) :
    Clause.eval σ (forbidFrom i a) = false ↔ matchesFrom σ i a := by
  induction a generalizing i with
  | nil => simp [forbidFrom, Clause.eval, matchesFrom]
  | cons b bs ih =>
    have hstep : Clause.eval σ (forbidFrom i (b :: bs))
               = (Lit.eval σ ⟨i, !b⟩ || Clause.eval σ (forbidFrom (i + 1) bs)) := by
      simp [forbidFrom, Clause.eval, List.any_cons]
    rw [hstep, Bool.or_eq_false_iff, lit_forbid_false, ih, matchesFrom]

/-- La CNF canonica che vieta una lista di pattern (ognuno a partire dalla
    variabile 0). Soddisfatta esattamente dagli assegnamenti che evitano TUTTI i
    pattern. -/
def canonicalCNF (forbids : List (List Bool)) : CNF := forbids.map (forbidFrom 0)

/-- **Correttezza della codifica.** La CNF canonica è vera sotto σ se e solo se σ
    non combacia con NESSUN pattern vietato. Quindi ogni funzione booleana (data
    dal suo insieme di assegnamenti "vietati") è una CNF: è la forma normale che
    trasforma «vincolo locale» in «clausole». -/
theorem canonical_correct (σ : Assign) (forbids : List (List Bool)) :
    CNF.eval σ (canonicalCNF forbids) = true ↔ ∀ a ∈ forbids, ¬ matchesFrom σ 0 a := by
  induction forbids with
  | nil => simp [canonicalCNF, CNF.eval]
  | cons a rest ih =>
    have hstep : CNF.eval σ (canonicalCNF (a :: rest))
               = (Clause.eval σ (forbidFrom 0 a) && CNF.eval σ (canonicalCNF rest)) := by
      simp [canonicalCNF, CNF.eval, List.all_cons]
    rw [hstep]
    cases hc : Clause.eval σ (forbidFrom 0 a) with
    | false =>
      have hm : matchesFrom σ 0 a := (forbid_eval_false σ 0 a).mp hc
      simp only [Bool.false_and]
      constructor
      · intro h; exact Bool.noConfusion h
      · intro h; exact absurd hm (h a List.mem_cons_self)
    | true =>
      simp only [Bool.true_and, ih]
      have hnm : ¬ matchesFrom σ 0 a := by
        intro hm; rw [(forbid_eval_false σ 0 a).mpr hm] at hc; exact Bool.noConfusion hc
      constructor
      · intro h x hx
        rcases List.mem_cons.mp hx with rfl | hxr
        · exact hnm
        · exact h x hxr
      · intro h x hx; exact h x (List.mem_cons_of_mem a hx)

/-- Soddisfacibilità: la CNF canonica è soddisfacibile se e solo se esiste un
    assegnamento che evita tutti i pattern vietati. (Banale via
    `canonical_correct`, ma è la forma in cui si usa: «∃ computazione valida».) -/
theorem canonical_sat (forbids : List (List Bool)) :
    Sat (canonicalCNF forbids) ↔ ∃ σ : Assign, ∀ a ∈ forbids, ¬ matchesFrom σ 0 a := by
  constructor
  · rintro ⟨σ, hσ⟩; exact ⟨σ, (canonical_correct σ forbids).mp hσ⟩
  · rintro ⟨σ, hσ⟩; exact ⟨σ, (canonical_correct σ forbids).mpr hσ⟩

-- Esempio concreto: vietare il pattern (x0=1, x1=1) dà la clausola (¬x0 ∨ ¬x1).

/-- L'assegnamento tutto-falso soddisfa la CNF che vieta (1,1). -/
example : Sat (canonicalCNF [[true, true]]) := ⟨fun _ => false, rfl⟩

/-- L'assegnamento tutto-vero combacia col pattern vietato: la CNF è falsa. -/
example : CNF.eval (fun _ => true) (canonicalCNF [[true, true]]) = false := rfl

end PvsNP.SAT
