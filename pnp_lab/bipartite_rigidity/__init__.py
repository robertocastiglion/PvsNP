"""Bipartite Rigidity — nuova arena del PvsNP-lab (lever A: non-perm-invariant ∧
non-statistica-globale ∧ non-enumerabile).

Oggetto: la RIGIDITA' di matrice R_M(r) della matrice di comunicazione a bipartizione
FISSA della famiglia esplicita inner-product / Hadamard (IP_k, H_k).  E' una proprieta'
della MATRICE (quindi del lato/bipartizione, non solo di f), notoriamente intrattabile.

  rigidity.py : costruttori delle matrici di comunicazione (±1 su Q, 0/1 su GF(2)),
                rank_gf2 / rank_q ESATTI, rigidita' ESATTA su tiny (k<=2 piena, k=3 a
                budget), lower bound CERTIFICATO di Hadamard per k>=4 (CITED), rho.
  killers.py  : i killer adversariali (reducible_from_rank = killer-1; dict_table =
                killer-2; side_mixing_spread = controllo perm-non-invarianza; leverage).

Honesty boundary in inglese in ``rigidity.honesty_note()``.  Esatto, deterministico,
nessun claim su P vs NP.
"""

from .rigidity import (
    comm_matrix_gf2,
    comm_matrix_pm,
    hadamard_matrix,
    honesty_note,
    ip_matrix_gf2,
    rank_gf2,
    rank_q,
    rho,
    rigidity_certified_lb,
    rigidity_gf2_exact,
    rigidity_q_pm_exact,
    tt_to_fn,
)
from .killers import (
    dict_table,
    dict_table_rows,
    leverage,
    leverage_verdict,
    reducible_from_rank,
    reducible_from_rank_rows,
    rig_rows,
    side_mixing_spread,
)

__all__ = [
    "comm_matrix_gf2",
    "comm_matrix_pm",
    "hadamard_matrix",
    "honesty_note",
    "ip_matrix_gf2",
    "rank_gf2",
    "rank_q",
    "rho",
    "rigidity_certified_lb",
    "rigidity_gf2_exact",
    "rigidity_q_pm_exact",
    "tt_to_fn",
    "dict_table",
    "dict_table_rows",
    "leverage",
    "leverage_verdict",
    "reducible_from_rank",
    "reducible_from_rank_rows",
    "rig_rows",
    "side_mixing_spread",
]
