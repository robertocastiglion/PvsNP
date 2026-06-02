/-
  NaturalProofs.lean — il nucleo logico della barriera di Razborov–Rudich.

  Onestà sullo scopo. Il teorema PIENO di Razborov–Rudich (una proprietà naturale
  utile contro P/poly rompe ogni generatore pseudo-casuale / ogni PRF) richiede la
  costruzione crittografica: fuori dalla portata di questo nucleo senza mathlib.
  Formalizziamo però, verificato dal kernel, TUTTA la struttura logica:

    • le funzioni booleane su n variabili come tavole di verità (2^(2^n) in tutto,
      conteggio VERIFICATO);
    • `Useful`  — la proprietà rifiuta TUTTE le funzioni facili (un ∀, condizione
      di CASO PEGGIORE, esattamente come in RR — non una media);
    • `Large`   — la proprietà accetta almeno k funzioni (conteggio costruttivo);
    • `Constructive` — predicato ASTRATTO (come `Model.PolyDec` in Basic.lean):
      non esprimibile internamente, lo esponiamo come ipotesi di un modello;
    • il CUORE di RR come ipotesi del modello (`rrCore`), e da esso la BARRIERA
      verificata: se la crittografia è sicura, NON esiste una prova naturale —
      quindi le tecniche naturali non possono separare.

  Stesso stile dei teoremi astratti `Model`: valgono per OGNI modello che soddisfa
  l'ipotesi-cuore (di sicuro per la crittografia reale). Zero `sorry`, niente
  `Classical.choice`.
-/
import PvsNP.Concrete

namespace PvsNP.NaturalProofs

open PvsNP

/-- Una funzione booleana su n variabili è data dalla sua tavola di verità: una
    stringa di 2^n bit. -/
abbrev TruthTable := BitString

/-- Tutte le funzioni booleane su n variabili = tutte le tavole di verità di
    lunghezza 2^n. -/
def allFns (n : Nat) : List TruthTable := stringsOfLen (2 ^ n)

/-- `f` è una funzione su n variabili ⟺ la sua tavola ha 2^n bit. -/
theorem mem_allFns (n : Nat) (f : TruthTable) :
    f ∈ allFns n ↔ f.length = 2 ^ n := mem_stringsOfLen (2 ^ n) f

/-- Numero di tavole di verità di lunghezza m: sono 2^m. -/
theorem length_stringsOfLen (m : Nat) : (stringsOfLen m).length = 2 ^ m := by
  induction m with
  | zero => rfl
  | succ k ih =>
    rw [stringsOfLen, List.length_append, List.length_map, List.length_map, ih,
        Nat.pow_succ, Nat.mul_two]

/-- **Quante funzioni booleane ci sono su n variabili: 2^(2^n).** (Verificato.)
    È la dimensione dello spazio in cui le prove naturali devono "pescare". -/
theorem card_allFns (n : Nat) : (allFns n).length = 2 ^ (2 ^ n) :=
  length_stringsOfLen (2 ^ n)

/-- Una proprietà combinatoria delle funzioni booleane: un test (Bool-valued) sulla
    tavola di verità. -/
abbrev Property := TruthTable → Bool

/-- Quante funzioni su n variabili soddisfano la proprietà. -/
def count (P : Property) (n : Nat) : Nat := (allFns n).countP P

/-- Il conteggio non supera il totale 2^(2^n). -/
theorem count_le_total (P : Property) (n : Nat) : count P n ≤ 2 ^ (2 ^ n) := by
  show (allFns n).countP P ≤ 2 ^ (2 ^ n)
  rw [← card_allFns]
  exact List.countP_le_length

/-- **UTILE** contro la classe `easy` (le funzioni "facili", a bassa complessità):
    P rifiuta OGNI funzione facile. È un ∀ — condizione di CASO PEGGIORE, non una
    media — esattamente la condizione di "usefulness" di Razborov–Rudich. -/
def Useful (P easy : Property) (n : Nat) : Prop :=
  ∀ f ∈ allFns n, easy f = true → P f = false

/-- **LARGA**: P accetta almeno `k` funzioni. (In RR: k ≥ 2^(2^n) · 2^{-O(n)},
    una frazione non trascurabile; qui parametrizzata dalla soglia `k`.) -/
def Large (P : Property) (n k : Nat) : Prop := count P n ≥ k

/-- La proprietà canonica «f è dura» = «f non è facile». -/
def hardnessProperty (easy : Property) : Property := fun f => !(easy f)

/-- **La proprietà di durezza è UTILE per costruzione**: rifiuta ogni funzione
    facile. (Verificato — nessuna ipotesi.) -/
theorem hardnessProperty_useful (easy : Property) (n : Nat) :
    Useful (hardnessProperty easy) easy n := by
  intro f _ hf
  show (!(easy f)) = false
  rw [hf]
  rfl

/-- Se NESSUNA funzione è facile, la proprietà di durezza le accetta tutte: è
    larga al massimo (k = 2^(2^n)). (Verificato.) -/
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

/-- Un modello crittografico astratto: espone la "costruttività", l'esistenza di
    crittografia sicura, e — come IPOTESI (la parte che CITIAMO) — il cuore di
    Razborov–Rudich: una proprietà costruttiva, utile e larga rompe la sicurezza. -/
structure CryptoModel where
  /-- Predicato astratto "P è costruttiva" (calcolabile efficientemente). Come
      `Model.PolyDec`, non è esprimibile internamente: è un'ipotesi del modello. -/
  Constructive : Property → Prop
  /-- "Esiste crittografia sicura" (PRG/PRF). -/
  SecurePRG : Prop
  /-- **Il cuore di Razborov–Rudich** (citato): se esiste una proprietà costruttiva,
      utile (contro la classe `easy` delle funzioni facili) e larga abbastanza,
      allora la crittografia NON è sicura. -/
  rrCore : ∀ {P easy : Property} {n : Nat},
    Constructive P → Useful P easy n → Large P n (2 ^ (2 ^ n) / 2) → ¬ SecurePRG

/-- Una **prova naturale** nel senso di Razborov–Rudich: una proprietà costruttiva,
    utile contro le funzioni facili, e larga (≥ metà di tutte le funzioni). -/
def NaturalProperty (M : CryptoModel) (P easy : Property) (n : Nat) : Prop :=
  M.Constructive P ∧ Useful P easy n ∧ Large P n (2 ^ (2 ^ n) / 2)

/-- **La barriera di Razborov–Rudich, verificata.** Se la crittografia è sicura,
    allora NON esiste alcuna prova naturale — dunque nessuna tecnica "naturale"
    (costruttiva + larga) può separare le classi. È la ragione profonda per cui
    quasi tutte le tecniche note di lower bound sono bloccate. -/
theorem rr_barrier (M : CryptoModel) (hsec : M.SecurePRG) :
    ¬ ∃ (P easy : Property) (n : Nat), NaturalProperty M P easy n := by
  rintro ⟨P, easy, n, hC, hU, hL⟩
  exact (M.rrCore hC hU hL) hsec

/-- Forma contrapposta: l'esistenza di una prova naturale CONFUTA la sicurezza
    crittografica. (È l'uso "offensivo" del teorema: una proprietà naturale è un
    attacco a ogni PRG.) -/
theorem natural_property_breaks_crypto (M : CryptoModel)
    {P easy : Property} {n : Nat} (h : NaturalProperty M P easy n) : ¬ M.SecurePRG := by
  obtain ⟨hC, hU, hL⟩ := h
  exact M.rrCore hC hU hL

end PvsNP.NaturalProofs
