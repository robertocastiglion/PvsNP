"""Algebrization Sandbox — la terza barriera, resa eseguibile.

Aaronson–Wigderson (2008) hanno mostrato che neppure le tecniche *algebrizzanti*
— quelle che funzionano rispetto a estensioni polinomiali a basso grado di un
oracolo — bastano a risolvere P vs NP. Questo modulo rende eseguibile il loro
nucleo positivo, l'arithmetization:

  - ``field``      : aritmetica esatta nel campo finito GF(p).
  - ``extension``  : estensione multilineare f~ di una funzione booleana (l'oggetto
                     algebrico su cui agiscono le tecniche e la barriera).
  - ``sumcheck``   : il protocollo sum-check (motore di IP = PSPACE), eseguito per
                     davvero con verifica di completezza e soundness.
  - ``barrier``    : la morale, la terza delle tre grandi barriere.
  - ``lab``        : trascrizione ASCII + SVG (la "scala dell'arithmetization").
"""

from .field import Field, is_prime
from .extension import MultilinearExtension, bits, count_true
from .sumcheck import (
    SumcheckResult,
    SumcheckRound,
    run_sumcheck,
    sum_over_cube,
    lagrange_eval,
)
from .barrier import algebrization_summary
from .lab import ascii_transcript, to_svg_ladder, write_svg

__all__ = [
    "Field",
    "is_prime",
    "MultilinearExtension",
    "bits",
    "count_true",
    "SumcheckResult",
    "SumcheckRound",
    "run_sumcheck",
    "sum_over_cube",
    "lagrange_eval",
    "algebrization_summary",
    "ascii_transcript",
    "to_svg_ladder",
    "write_svg",
]
