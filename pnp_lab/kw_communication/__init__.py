"""Modulo KW (Karchmer-Wigderson) monotono + comunicazione deterministica esatta.

Vedi ``kw.py`` per la matrice KW+, il partition number e D^cc esatti.
"""
from .kw import (
    minterms,
    maxterms,
    kw_plus_matrix,
    partition_number,
    dcc,
    clique_f,
)

__all__ = [
    "minterms",
    "maxterms",
    "kw_plus_matrix",
    "partition_number",
    "dcc",
    "clique_f",
]
