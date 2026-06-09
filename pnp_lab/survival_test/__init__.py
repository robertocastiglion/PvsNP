"""Modulo 17 — Survival Test (𝒭=∞).

Un criterio MISURABILE che, data una barriera, dice a quale famiglia appartiene:
si calcola il vantaggio di distinzione Δ concedendo CALCOLO ILLIMITATO (𝒭 = ∞).

  • Δ(𝒭=∞) < 1  ⟹  information-theoretic (relativizzazione: bound sull'interfaccia,
    incondizionato);
  • Δ(𝒭=∞) = 1  ⟹  computational (natural proofs: il bound evapora — pseudocasualità).

Onestà: criterio di CLASSIFICAZIONE (ri-deriva i due assi del Modulo 15), NON un
nuovo lower bound. Misure esatte su istanze minuscole. Non tocca P vs NP.
"""

from .survival import (
    SurvivalResult,
    TRIVIAL_TOL,
    classify,
    relativization_survival,
    natural_proofs_curve,
    natural_proofs_unbounded_advantage,
    natural_proofs_survival,
    survival_results,
    criterion_summary,
)
from .lab import survival_report, verdict_note

__all__ = [
    "SurvivalResult", "TRIVIAL_TOL", "classify",
    "relativization_survival",
    "natural_proofs_curve", "natural_proofs_unbounded_advantage",
    "natural_proofs_survival",
    "survival_results", "criterion_summary",
    "survival_report", "verdict_note",
]
