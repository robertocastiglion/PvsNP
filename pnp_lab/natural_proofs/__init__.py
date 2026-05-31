"""Natural Proofs Analyzer.

Verifica se una proprietà combinatoria delle funzioni booleane cade nella
barriera di Razborov–Rudich (1994): se è *costruttiva* e *larga*, allora non
può servire a separare P da NP.
"""

from .boolean import BooleanFunction, all_functions, random_function
from .analyzer import (
    Property,
    LargenessResult,
    ConstructivenessResult,
    AnalysisReport,
    measure_largeness,
    measure_constructiveness,
    analyze,
)

__all__ = [
    "BooleanFunction",
    "all_functions",
    "random_function",
    "Property",
    "LargenessResult",
    "ConstructivenessResult",
    "AnalysisReport",
    "measure_largeness",
    "measure_constructiveness",
    "analyze",
]
