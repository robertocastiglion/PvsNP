"""Algebraic Query Model — i "mondi algebrici" della barriera dell'algebrizzazione.

Estende il Modulo 7: là eseguivamo l'arithmetization (estensione multilineare +
sum-check), qui rendiamo eseguibili i due effetti opposti dell'accesso algebrico
che definiscono la barriera di Aaronson–Wigderson:

  - ``polynomial`` : polinomi su GF(p) e il teorema di Schwartz–Zippel (il motore
                     di tutti i lower bound algebrici), verificato in modo esatto.
  - ``worlds``     : MONDO 1 (potenza) — rilevare un bit piantato con 1 query
                     algebrica invece di 2^m booleane; MONDO 2 (limite) — il lower
                     bound di interpolazione su GF(p) con avversario.
  - ``barrier``    : la morale, e il confine onesto fra ciò che eseguiamo e ciò
                     che citiamo (la separazione P^Ã vs NP^Ã completa).
  - ``lab``        : ASCII + SVG dei due mondi.
"""

from .polynomial import (
    Poly,
    SZCheck,
    count_zeros,
    count_agreements,
    schwartz_zippel_zero_bound,
    verify_schwartz_zippel,
    all_points,
)
from .worlds import (
    PlantedDetection,
    InterpolationBound,
    planted_oracle_extension,
    planted_detection,
    interpolation_lower_bound,
    random_queries,
    cube_queries,
)
from .barrier import algebraic_worlds_summary
from .lab import ascii_power, ascii_limit, to_svg_worlds, write_svg

__all__ = [
    "Poly",
    "SZCheck",
    "count_zeros",
    "count_agreements",
    "schwartz_zippel_zero_bound",
    "verify_schwartz_zippel",
    "all_points",
    "PlantedDetection",
    "InterpolationBound",
    "planted_oracle_extension",
    "planted_detection",
    "interpolation_lower_bound",
    "random_queries",
    "cube_queries",
    "algebraic_worlds_summary",
    "ascii_power",
    "ascii_limit",
    "to_svg_worlds",
    "write_svg",
]
