"""Modulo 15 — Distinguishing Advantage Sandbox.

Rende ESEGUIBILE su n=3 la lente corretta sulle barriere: non "informazione
estratta" ma INDISTINGUIBILITÀ contro un osservatore a risorse limitate, su due
assi ortogonali — informazione (fan-in ℓ delle oracle gate) e calcolo (numero s
di gate). Misura il vantaggio ε(ℓ, s) nel separare funzioni DURE da FACILI
(istanze MCSP, riuso dei Moduli 6 e 13).

Onestà: misura ESATTA su finite size (n=3), non la barriera asintotica; non
tocca P vs NP.
"""

from .advantage import (
    N_VARS,
    TT_BITS,
    NUM_FUNCS,
    HardEasySplit,
    CellResult,
    AdvantageMatrix,
    default_split,
    build_local_basis,
    advantage_column,
    advantage_matrix,
    frontier_note,
    distinguishing_summary,
)
from .lab import ascii_matrix, to_svg_matrix, write_svg

__all__ = [
    "N_VARS", "TT_BITS", "NUM_FUNCS",
    "HardEasySplit", "CellResult", "AdvantageMatrix",
    "default_split", "build_local_basis",
    "advantage_column", "advantage_matrix",
    "frontier_note", "distinguishing_summary",
    "ascii_matrix", "to_svg_matrix", "write_svg",
]
