/-
  Barriers.lean: le barriere dimostrative, formalizzate al livello che il
  nostro quadro astratto permette.

  Idea chiave. Nel nostro quadro i diversi `Model` giocano il ruolo dei "mondi
  con oracolo" di Baker–Gill–Solovay: modelli diversi possono soddisfare P = NP
  oppure P ≠ NP. La barriera della relativizzazione dice esattamente che
  entrambi i mondi esistono. Da qui dimostriamo (in modo verificato dal kernel)
  che nessun argomento valido in OGNI modello può decidere P vs NP.
-/
import PvsNP.Basic
import PvsNP.Classes

namespace PvsNP

/-- Forma astratta della barriera di relativizzazione (Baker–Gill–Solovay 1975):
    esiste un modello in cui P = NP e un modello in cui P ≠ NP.

    (Reso eseguibile nel Modulo 2 del toolkit: oracolo TQBF per P^A = NP^A e
    diagonalizzazione per P^B ≠ NP^B.) -/
def RelativizationBarrier : Prop :=
  (∃ M : Model, PEqNP M) ∧ (∃ M : Model, PNeqNP M)

/-- Una dimostrazione "relativizzante" è un argomento valido in OGNI modello.
    Se la barriera vale, nessuna dimostrazione del genere può stabilire né
    P = NP né P ≠ NP: dovrebbe valere anche nel modello con l'esito opposto. -/
theorem relativizing_cannot_settle (h : RelativizationBarrier) :
    ¬ (∀ M : Model, PEqNP M) ∧ ¬ (∀ M : Model, PNeqNP M) := by
  cases h with
  | intro hEq hNeq =>
    apply And.intro
    · intro hAll
      cases hNeq with
      | intro M hM => exact hM (hAll M)
    · intro hAll
      cases hEq with
      | intro M hM => exact (hAll M) hM

/-
  Le altre due barriere — Natural Proofs (Razborov–Rudich, Modulo 1) e
  Algebrizzazione (Aaronson–Wigderson) — richiedono di formalizzare le proprietà
  delle funzioni booleane e l'aritmetizzazione, fuori dalla portata di questo
  primo nucleo. Sono lasciate come sviluppo futuro: vedi il Modulo 1 per la
  versione ESEGUIBILE della barriera Natural Proofs e il Modulo 3 (Knowledge
  Graph) per come le tre barriere si collegano fra loro.
-/

end PvsNP
