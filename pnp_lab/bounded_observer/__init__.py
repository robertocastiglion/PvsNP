"""Modulo 16 — Bounded Observer.

Una definizione minimale di "osservatore limitato" T = (𝒜, 𝒭, t) e un unico
vantaggio di distinzione Δ(𝒞; D0, D1) = sup_T |Pr_D1 − Pr_D0|. Istanzia le quattro
barriere su mondi minuscoli e MISURA quali rientrano nel template Δ ≤ ε:

  • relativizzazione / algebrizzazione → SÌ (stesso template, cambia solo 𝒜);
  • natural proofs → SÌ (asse ortogonale: informazione satura, calcolo limitato);
  • proof complexity → NO (la sanità annulla il lato D0; la quantità è min|Π|∈ℕ).

Onestà: misure ESATTE su istanze minuscole, non le barriere asintotiche; non
tocca P vs NP.
"""

from .observer import (
    World,
    Dist,
    advantage,
    class_advantage,
    relativization_worlds,
    relativization_advantage,
    algebrization_one_query_advantage,
    schwartz_zippel_agreement,
    natural_proofs_advantage,
    Clause,
    refutation_depth,
    is_satisfiable,
    proof_system_observer,
    proof_complexity_worlds,
    ProofComplexityProbe,
    proof_complexity_probe,
    unified_summary,
)
from .lab import unified_report, verdict_note

__all__ = [
    "World", "Dist", "advantage", "class_advantage",
    "relativization_worlds", "relativization_advantage",
    "algebrization_one_query_advantage", "schwartz_zippel_agreement",
    "natural_proofs_advantage",
    "Clause", "refutation_depth", "is_satisfiable",
    "proof_system_observer", "proof_complexity_worlds",
    "ProofComplexityProbe", "proof_complexity_probe",
    "unified_summary", "unified_report", "verdict_note",
]
