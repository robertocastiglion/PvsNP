"""Algebraic Separation — il cuore di query complexity di P^Ã ≠ NP^Ã.

Completa il Modulo 9: là si vedevano potenza e limite dell'accesso algebrico;
qui li si combina nella SEPARAZIONE vera e propria, nel modello a query.

  - ``separation`` : il modello (funzionali di valutazione χ_·(r)), il lato NP
                     (1 query), il lato P (lower bound κ via avversario di
                     cancellazione), tutto esatto.
  - ``barrier``    : la morale e il confine onesto (sollevamento a oracolo TM e
                     teorema di Aaronson–Wigderson: citati).
  - ``lab``        : ASCII + SVG del divario NP=1 vs P≥κ.

ESEGUIAMO il cuore combinatorio; la costruzione completa dell'oracolo per
macchine di Turing resta citata.
"""

from .separation import (
    CancellationAdversary,
    SeparationResult,
    all_field_points,
    all_boolean_oracles,
    chi_vector,
    evaluate,
    boolean_kernel_witness,
    kills_all_kernels,
    cancellation_example,
    deterministic_lower_bound,
    verify_nondet_one_query,
)
from .barrier import separation_summary
from .lab import ascii_separation, to_svg_separation, write_svg

__all__ = [
    "CancellationAdversary",
    "SeparationResult",
    "all_field_points",
    "all_boolean_oracles",
    "chi_vector",
    "evaluate",
    "boolean_kernel_witness",
    "kills_all_kernels",
    "cancellation_example",
    "deterministic_lower_bound",
    "verify_nondet_one_query",
    "separation_summary",
    "ascii_separation",
    "to_svg_separation",
    "write_svg",
]
