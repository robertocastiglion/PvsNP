"""Meta-Complexity Lab — MCSP & hardness magnification, dove il cerchio si chiude.

La meta-complessità studia la complessità di *calcolare la complessità* (MCSP). È
la frontiera più viva (2018+) e il punto in cui i fili del progetto si annodano:
Shannon (M6), Natural Proofs (M1) e il metodo algoritmico (M12).

  - ``mcsp``     : MCSP calcolato ESATTO (riuso del Modulo 6), MCSP ∈ NP, la
                   soglia facili/difficili.
  - ``frontier`` : il legame esatto MCSP ↔ Natural Proofs (la proprietà 'f è dura'
                   è utile+larga, ma costruttiva ⇒ risolvere MCSP), e l'hardness
                   magnification (citata).
  - ``barrier``  : la morale e la chiusura del cerchio.
  - ``lab``      : ASCII + SVG (la soglia di MCSP).

Onestà: MCSP e il legame con Natural Proofs sono ESEGUITI; lo status di MCSP e i
teoremi di amplificazione sono CITATI. Non risolve P vs NP.
"""

from .mcsp import (
    ComplexityTable,
    NPCertificate,
    ThresholdRow,
    complexity_map,
    mcsp_decide,
    mcsp_witness,
    np_certificate,
    mcsp_threshold,
)
from .frontier import (
    NaturalProofsLink,
    MagnificationFact,
    MagnificationGap,
    hard_property,
    is_useful,
    largeness,
    analyze_link,
    magnification_results,
    threshold_gap,
)
from .barrier import meta_complexity_summary
from .lab import ascii_threshold, ascii_link, to_svg_threshold, write_svg

__all__ = [
    "ComplexityTable", "NPCertificate", "ThresholdRow",
    "complexity_map", "mcsp_decide", "mcsp_witness", "np_certificate", "mcsp_threshold",
    "NaturalProofsLink", "MagnificationFact", "MagnificationGap",
    "hard_property", "is_useful", "largeness", "analyze_link",
    "magnification_results", "threshold_gap",
    "meta_complexity_summary",
    "ascii_threshold", "ascii_link", "to_svg_threshold", "write_svg",
]
