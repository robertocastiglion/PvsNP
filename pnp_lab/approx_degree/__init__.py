"""Approximate Degree — la 6a arena indipendente del PvsNP-lab (metodo dei polinomi).

``adeg_{1/3}(f)`` = grado minimo di un polinomio reale che approssima f a errore 1/3 su
ogni input booleano.  È una misura di complessita' REALE (limite inferiore esatto per la
quantum query complexity, il metodo dei polinomi), calcolata qui in modo ESATTO su istanze
minuscole via la DUALITA' LP (il dual polynomial), riusando il simplesso razionale del
Modulo "exactness_composes".

Apertura decisa dallo strategist-orchestratore dopo l'esaurimento delle tre barriere
classiche (Module 28): arena la piu' distante dalle cinque gia' collassate.  KILLER
pre-dichiarato: adeg e' permutation-invariant ⇒ collassa su una statistica simmetrica
globale (Paturi) / sul dizionario sigma(cost).  Nessun claim P vs NP.
"""

from .adeg import (
    chi,
    monomial_masks,
    error_degree_d,
    approx_degree,
    adeg_table,
    adeg_vs_cost,
    adeg_vs_dictionary,
)

__all__ = [
    "chi",
    "monomial_masks",
    "error_degree_d",
    "approx_degree",
    "adeg_table",
    "adeg_vs_cost",
    "adeg_vs_dictionary",
]
