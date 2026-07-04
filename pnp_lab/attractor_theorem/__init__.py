"""Teorema dell'Attrattore — Entry 36 del PvsNP-lab.

Misura la struttura del dizionario di ricostruibilita' sul reticolo dei 5 invarianti
di orbita (cost, gf2_degree, sensitivity, block_sensitivity, adeg) su n=3 booleane,
sotto l'azione del gruppo IPEROCTAEDRALE B_n (permutazioni × negazioni di input).

Funzioni esportate:
    orbit_invariant_table  -- tabella orbite -> 5 invarianti
    reconstructibility_matrix  -- matrice 5x5 di ricostruibilita'
    reconstructible_from   -- I ricostruibile da sottoinsieme S?
    minimum_separators     -- separatori minimi (cardinalita' min che separano tutte le orbite)
    hasse_diagram          -- riduzione transitiva del preordine
    summary                -- sommario completo (n=3)
"""

from .lattice import (
    orbit_invariant_table,
    reconstructibility_matrix,
    reconstructible_from,
    minimum_separators,
    hasse_diagram,
    summary,
)

__all__ = [
    "orbit_invariant_table",
    "reconstructibility_matrix",
    "reconstructible_from",
    "minimum_separators",
    "hasse_diagram",
    "summary",
]
