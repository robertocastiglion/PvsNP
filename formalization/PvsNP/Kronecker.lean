/-
  Kronecker.lean — Lemma L60 (corretto): la successione s₃ non soddisfa alcuna
  ricorrenza lineare di ordine 2 a coefficienti interi.

  Fonte: RESEARCH_LOG.md Entry 60 (righe 3711–3779), con ERRATUM (Entry 69):
  Entry 60 usava s₃(1) = 1, che è il plateau PRE-stabile (a = 4, 5).
  Il valore stabile corretto è s₃(1) = 2 (verificato: g((a,3)^3) = 2 per
  a = 6..12, onset dichiarato già in Entry 49). La conclusione di L60
  sopravvive con entrambi i valori (38·a = 715 col vecchio, 60·a = 391 col
  corretto: nessuno dei due ha soluzione intera); qui si formalizza il
  sistema CORRETTO.

  Contesto. La successione s₃(k) = lim_{a→∞} g((a, 3^k)^3) vale:
    s₃(1) = 2      (stabile per a ≥ 6; ERRATUM su Entry 60 che usava 1)
    s₃(2) = 14     (stabile per a ≥ 7)
    s₃(3) = 158    (stabile per a ≥ 9)
    s₃(4) = 1497   (stabile per a ≥ 10)

  Enunciato formalizzato (su `Int` — Lean core usa `Int` senza notazione `ℤ`):
    NON esistono a b : Int tali che valgano contemporaneamente
      • 158 = 14·a + 2·b     (equazione I:  s₃(3) = a·s₃(2) + b·s₃(1))
      • 1497 = 158·a + 14·b  (equazione II: s₃(4) = a·s₃(3) + b·s₃(2))

  Nota sul campo. Il sistema 2×2 ha determinante det = 14·14 − 158·2 = −120 ≠ 0,
  quindi ammette un'UNICA soluzione razionale: a = 391/60, b = (158 − 14a)/2.
  L'enunciato su ℚ (Rat) sarebbe FALSO — quella soluzione esiste.
  L60 è correttamente enunciato su Int: non esiste soluzione INTERA.

  Verifica dell'eliminazione (col valore corretto s₃(1) = 2):
    Da (I):  2b = 158 − 14a  →  b = 79 − 7a
    In (II): 1497 = 158a + 14(79 − 7a) = 60a + 1106
    Quindi:  60a = 391
    60 ∤ 391 (391 = 6·60 + 31) → nessuna soluzione in Int. QED.

  Assiomi. Strutturando la prova in due passi (intro + omega), `omega` su Int
  richiede solo `propext` e `Quot.sound` — senza `Classical.choice`.
-/

namespace PvsNP.Kronecker

-- ────────────────────────────────────────────────────────────────────────────
-- Le quattro costanti note di s₃  (tipo Int = interi di Lean core)
-- ────────────────────────────────────────────────────────────────────────────

/-- s₃(1) = 2 — primo valore della successione stabile Kronecker di ordine 3.
    ERRATUM rispetto a Entry 60 (che usava 1 = plateau pre-stabile a=4,5):
    il limite stabile è 2, verificato per a = 6..12 (onset in Entry 49). -/
def s3_1 : Int := 2

/-- s₃(2) = 14 (stabile per a ≥ 7; verificato a = 7..11) -/
def s3_2 : Int := 14

/-- s₃(3) = 158 -/
def s3_3 : Int := 158

/-- s₃(4) = 1497 -/
def s3_4 : Int := 1497

-- ────────────────────────────────────────────────────────────────────────────
-- Lemma ausiliario: 60·a = 391 non ha soluzioni intere.
-- (Il cuore dell'eliminazione algebrica, col valore corretto s₃(1) = 2.)
-- ────────────────────────────────────────────────────────────────────────────

/-- 60·a = 391 non ha soluzioni in Int.
    60 ∤ 391 perché 391 = 6·60 + 31 (resto 31 ≠ 0). -/
private theorem no_int_sol_60_391 (a : Int) (h : 60 * a = 391) : False := by
  omega

-- ────────────────────────────────────────────────────────────────────────────
-- Lemma L60 — nessuna ricorrenza lineare di ordine 2 a coefficienti interi
-- ────────────────────────────────────────────────────────────────────────────

/-- **LEMMA L60** (Entry 60 del RESEARCH_LOG, 2026-07-18; erratum Entry 69).

    La successione s₃ con valori s₃(1)=2, s₃(2)=14, s₃(3)=158, s₃(4)=1497
    NON soddisfa alcuna ricorrenza lineare di ordine 2 a coefficienti interi.

    Formalmente: non esistono a b : Int tali che valgano contemporaneamente
      • s₃(3) = a · s₃(2) + b · s₃(1)   (equazione I)
      • s₃(4) = a · s₃(3) + b · s₃(2)   (equazione II)

    Prova: l'eliminazione di b riduce il sistema a 60·a = 391;
    poiché 60 ∤ 391 (391 = 6·60 + 31), non esistono soluzioni intere.

    Assiomi: solo `propext` e `Quot.sound` (niente `Classical.choice`). -/
theorem s3_no_order2_recurrence :
    ¬ ∃ a b : Int,
        (158 : Int) = 14 * a + 2 * b ∧
        (1497 : Int) = 158 * a + 14 * b := by
  -- Assumiamo per assurdo l'esistenza di a, b interi
  intro ⟨a, b, h1, h2⟩
  -- L'eliminazione di b e la riduzione a 60·a = 391 sono gestite da omega
  exact no_int_sol_60_391 a (by omega)

/-- Versione con le costanti denominate — stessa proposizione,
    collega il teorema ai nomi s3_1 … s3_4. -/
theorem s3_no_order2_recurrence_named :
    ¬ ∃ a b : Int,
        s3_3 = a * s3_2 + b * s3_1 ∧
        s3_4 = a * s3_3 + b * s3_2 := by
  intro ⟨a, b, h1, h2⟩
  simp only [s3_1, s3_2, s3_3, s3_4] at h1 h2
  exact no_int_sol_60_391 a (by omega)

end PvsNP.Kronecker
