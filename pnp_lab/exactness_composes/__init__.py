"""Modulo 18 -- EXACTNESS COMPOSES: la killer search della congettura post-audit.

Definisce il gap pinnato sul LP  G*(M) = Cov(M) - LP(M)  della copertura dei
certificati di una matrice di comunicazione, e risolve su istanze minuscole se la
classe a copertura integrale e' chiusa per gadget composition. Esito: VERA per il
tensore (ma corollario della moltiplicativita' LP), FALSA per il lift (controesempio
J - I_4 a 4 bit, G* = 1).
"""

from .gap import (
    BoolMatrix,
    as_matrix,
    cover_number,
    frac_cover,
    gstar,
    is_integral,
    maximal_one_rectangles,
    ones,
)
from .compose import (
    GADGETS_1BIT,
    base_function,
    lift,
    lift_named,
    tensor,
    tensor_or,
)
from .search import (
    lift_counterexamples,
    resolution,
    smallest_gap_matrix,
    smallest_lift_counterexample,
    tensor_closure_holds,
)
from .lab import gap_table, report, witness_note
from .integrality_leverage import (
    DEFAULT_GADGETS,
    DEFAULT_OUTERS,
    doorC_candidates,
    gap_at,
    gap_sequence,
    ji_cover_number,
    ji_frac_cover,
    killer_table,
    law_affine,
    law_multiplicative,
    law_poly_gadget,
    leverage_row,
    sweep,
)

__all__ = [
    "BoolMatrix",
    "as_matrix",
    "cover_number",
    "frac_cover",
    "gstar",
    "is_integral",
    "maximal_one_rectangles",
    "ones",
    "GADGETS_1BIT",
    "base_function",
    "lift",
    "lift_named",
    "tensor",
    "tensor_or",
    "lift_counterexamples",
    "resolution",
    "smallest_gap_matrix",
    "smallest_lift_counterexample",
    "tensor_closure_holds",
    "gap_table",
    "report",
    "witness_note",
    "DEFAULT_GADGETS",
    "DEFAULT_OUTERS",
    "doorC_candidates",
    "gap_at",
    "gap_sequence",
    "ji_cover_number",
    "ji_frac_cover",
    "killer_table",
    "law_affine",
    "law_multiplicative",
    "law_poly_gadget",
    "leverage_row",
    "sweep",
]
