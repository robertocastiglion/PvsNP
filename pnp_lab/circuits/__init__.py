"""Modulo 6 — Circuit Complexity Sandbox.

Due risultati esatti e calcolabili sui lower bound che *funzionano*:

  * **Spettro di Shannon** — la complessità di formula esatta di tutte le
    funzioni booleane piccole. Quasi tutte sono difficili, ma non sappiamo
    esibire UNA funzione esplicita difficile: è il muro dei lower bound.
  * **Muro della parità** — la DNF (profondità 2) minima della parità ha
    esattamente 2^(n-1) termini. È il caso base, esatto, del teorema
    'parità ∉ AC0' (Furst–Saxe–Sipser, Håstad), uno dei rari lower bound che
    aggira la barriera Natural Proofs.
"""

from .circuit import (
    AND,
    NOT,
    OR,
    mask_for,
    parity_table,
    popcount_table,
    projection,
    truth_rows,
)
from .synthesis import (
    ComplexityTable,
    min_formula_sizes,
    shannon_counting_bound,
)
from .parity import (
    ParityLowerBound,
    dnf_size,
    parity_dnf_lower_bound,
    prime_implicants,
)
from .lab import (
    ParityGrowthRow,
    ascii_distribution,
    parity_growth,
    to_svg_distribution,
    to_svg_parity,
    write_svg,
)

__all__ = [
    "AND", "OR", "NOT", "mask_for", "projection", "parity_table",
    "popcount_table", "truth_rows",
    "ComplexityTable", "min_formula_sizes", "shannon_counting_bound",
    "ParityLowerBound", "parity_dnf_lower_bound", "prime_implicants", "dnf_size",
    "ParityGrowthRow", "parity_growth", "ascii_distribution",
    "to_svg_distribution", "to_svg_parity", "write_svg",
]
