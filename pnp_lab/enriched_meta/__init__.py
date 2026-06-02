"""Modulo 14 — Enriched Meta-Category: le tre lenti come morfismi, non problemi.

Rende ESEGUIBILE la tesi forte di Roberto (2026-06-02): calcolare / dimostrare /
riconoscere la complessità non sono tre problemi diversi ma — forse — gli STESSI
morfismi di un'unica categoria C, visti tramite tre arricchimenti incompatibili
(categorie arricchite su quantali, Lawvere 1973). L'invariante cercato non è uno
scalare ma la struttura di equivalenza tra le trasformazioni.

Il test, esatto su n piccolo:
  • ``category``  : la categoria sottostante C (funzioni booleane + rinomine S_n);
                    verifica che la complessità è invariante sui morfismi (isometria).
  • ``lenses``    : le tre realizzazioni del predicato di durezza H_s(f) con i loro
                    modelli di costo (V_time esatto, V_sample costruttivo, V_proof).
  • ``defect``    : il difetto di composizione tra le lenti — l'esperimento. Isola
                    di equivalenza CIKK (difetto 0), curva del budget di prova,
                    gap irriducibile riconoscere↔calcolare.
  • ``barrier``   : il verdetto (A-condizionato) e le citazioni.
  • ``lab``       : ASCII + SVG (heatmap dei difetti).

Onestà: tutto ciò che riguarda C, i verdetti e i difetti è ESEGUITO esatto su n
piccolo; le equivalenze/barriere asintotiche e l'invariante OWF sono CITATE. Non
risolve P vs NP.
"""

from .category import (
    Category,
    IsometryReport,
    apply_perm,
    check_isometry,
    orbit,
)
from .lenses import (
    LensVerdicts,
    best_recognize_threshold,
    chi_compute,
    chi_prove,
    chi_recognize,
    evaluate_lenses,
    formulas_of_size,
    proof_length_for_threshold,
    total_influence,
)
from .defect import (
    BudgetPoint,
    CikkIsland,
    DefectMatrix,
    IrreducibleGap,
    cikk_island,
    defect,
    defect_matrix,
    irreducible_recognize_gap,
    learn_property,
    proof_budget_curve,
)
from .barrier import (
    Citation,
    Verdict,
    enriched_metacategory_summary,
    framework_citations,
)
from .lab import (
    ascii_cikk,
    ascii_gap,
    ascii_matrix,
    to_svg_matrix,
    write_svg,
)

__all__ = [
    # category
    "Category", "IsometryReport", "apply_perm", "check_isometry", "orbit",
    # lenses
    "LensVerdicts", "best_recognize_threshold", "chi_compute", "chi_prove",
    "chi_recognize", "evaluate_lenses", "formulas_of_size",
    "proof_length_for_threshold", "total_influence",
    # defect
    "BudgetPoint", "CikkIsland", "DefectMatrix", "IrreducibleGap",
    "cikk_island", "defect", "defect_matrix", "irreducible_recognize_gap",
    "learn_property", "proof_budget_curve",
    # barrier
    "Citation", "Verdict", "enriched_metacategory_summary", "framework_citations",
    # lab
    "ascii_cikk", "ascii_gap", "ascii_matrix", "to_svg_matrix", "write_svg",
]
