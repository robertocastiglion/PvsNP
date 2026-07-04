"""Teorema dell'Attrattore — Entry 36 del PvsNP-lab.

Misura la struttura del dizionario di ricostruibilita' sul reticolo dei 5 invarianti
di orbita (cost, gf2_degree, sensitivity, block_sensitivity, adeg) su n=3 booleane,
sotto l'azione del gruppo IPEROCTAEDRALE B_n (permutazioni x negazioni di input).

Funzioni esportate da lattice:
    orbit_invariant_table  -- tabella orbite -> 5 invarianti
    reconstructibility_matrix  -- matrice 5x5 di ricostruibilita'
    reconstructible_from   -- I ricostruibile da sottoinsieme S?
    minimum_separators     -- separatori minimi (cardinalita' min che separano tutte le orbite)
    hasse_diagram          -- riduzione transitiva del preordine
    lattice_summary        -- sommario completo del reticolo (n=3)

Funzioni esportate da collapse_ledger:
    load_collapses         -- 21 record di collasso da RESEARCH_LOG.md
    assign_type            -- classificazione di un testo in 6 tipi
    cumulative_curve       -- curva C(1..21) tipi distinti cumulati
    good_turing            -- stima Good-Turing + CI bootstrap (seed=0)
    stability              -- C sotto 3 livelli di granularita'
    ledger_summary         -- sommario completo del ledger
"""

from .lattice import (
    orbit_invariant_table,
    reconstructibility_matrix,
    reconstructible_from,
    minimum_separators,
    hasse_diagram,
    summary as lattice_summary,
)

from .collapse_ledger import (
    load_collapses,
    assign_type,
    cumulative_curve,
    good_turing,
    stability,
    summary as ledger_summary,
)

__all__ = [
    # lattice
    "orbit_invariant_table",
    "reconstructibility_matrix",
    "reconstructible_from",
    "minimum_separators",
    "hasse_diagram",
    "lattice_summary",
    # collapse_ledger
    "load_collapses",
    "assign_type",
    "cumulative_curve",
    "good_turing",
    "stability",
    "ledger_summary",
]
