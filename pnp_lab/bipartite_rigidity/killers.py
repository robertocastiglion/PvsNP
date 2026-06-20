"""I KILLER dell'arena Bipartite Rigidity: l'analisi adversariale in codice.

Tre domande, tutte ESATTE su istanze tiny (k<=2 esaustivo; k=3 campione/famiglie):

  killer-1  reducible_from_rank : la rigidita' R_M(r) e' ricostruibile dai SOLI ranghi
            (rank_gf2, rank_q) della matrice?  (riduzione a log-rank).
  killer-2  dict_table / splits : R_M(r) e' ricostruibile dal DIZIONARIO CONGIUNTO del
            lab (cost, gf2_degree, sensitivity, block_sensitivity) come adeg nel Modulo
            29?  Se ogni firma del dizionario mappa a un solo valore di rigidita',
            collasso (RESTATEMENT).
  controllo perm-non-invarianza : la rigidita' DEVE variare sotto permutazioni che
            MESCOLANO i due lati della bipartizione (X<->Y, variabili tra lati), mentre
            una statistica perm-invariant di f (es. la sensitivity) resta PIATTA.

Piu' la metrica di LEVA leverage(ks) = rho(k+1)/rho(k): monotona crescente (>1) =
leverage; bounded/non-monotona = survival-no-leverage.

Esatto e deterministico (interi/Fraction).  Nessun claim su P vs NP.
"""

from __future__ import annotations

import pickle
from collections import defaultdict
from dataclasses import dataclass
from fractions import Fraction
from itertools import combinations, permutations, product
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from pnp_lab.circuits import min_formula_sizes
from pnp_lab.meta_complexity import strata_graph as sg

from .rigidity import (
    comm_matrix_gf2,
    comm_matrix_pm,
    rank_gf2,
    rank_q,
    rigidity_q_pm_exact,
    tt_to_fn,
)


# --------------------------------------------------------------------------- #
#  Costruzione delle matrici a bipartizione FISSA per ogni f su 2k bit        #
# --------------------------------------------------------------------------- #

def _matrices_for(tt: int, k: int):
    """(M_gf2, M_pm) per la funzione ``tt`` su 2k bit, bipartizione alice=primi k bit."""
    f = tt_to_fn(tt, 2 * k)
    return comm_matrix_gf2(f, k), comm_matrix_pm(f, k)


# --------------------------------------------------------------------------- #
#  Tabella per-funzione (rank/rigidity) + confronto col dizionario congiunto   #
# --------------------------------------------------------------------------- #

@dataclass
class RigRow:
    tt: int
    rank_gf2: int
    rank_q: int
    rigidity: int            # R su Q (negazione segno) a target r


def _rigidity_q(M_pm, r: int, max_flips: int) -> int:
    return rigidity_q_pm_exact(M_pm, r, max_flips=max_flips)


def rig_rows(k: int, r: int, *, sample: List[int] | None = None,
             max_flips: int = 8) -> List[RigRow]:
    """Per ogni f su 2k bit (esaustivo se ``sample`` None, altrimenti sul campione):
    (rank_gf2, rank_q, rigidity_q a target r) della matrice di comunicazione.

    ESAUSTIVO solo per k<=2 (2k<=4 -> 16 funzioni).  Per k=3 (2k=6 -> 2^64) NON
    enumerabile: passare un ``sample`` di truth-table esplicite."""
    if sample is None:
        if 2 * k > 4:
            raise ValueError(
                f"k={k}: 2k={2*k} bit -> 2^{1 << (2*k)} funzioni NON enumerabile; "
                "passa un 'sample' esplicito."
            )
        sample = list(range(1 << (1 << (2 * k))))
    rows: List[RigRow] = []
    for tt in sample:
        Mg, Mp = _matrices_for(tt, k)
        rows.append(RigRow(tt, rank_gf2(Mg), rank_q(Mp), _rigidity_q(Mp, r, max_flips)))
    return rows


def reducible_from_rank(k: int, r: int, *, sample: List[int] | None = None,
                        max_flips: int = 8) -> Tuple[bool, List[tuple]]:
    """killer-1: la rigidita' e' ricostruibile dai SOLI ranghi (rank_gf2, rank_q)?

    Ritorna (reducible, splits): reducible=True sse ogni coppia di ranghi (rank_gf2,
    rank_q) mappa a UN SOLO valore di rigidita' (cioe' la rigidita' NON separa nessuna
    coppia di funzioni con gli stessi ranghi).  splits = le firme-rango che portano a
    >=2 valori di rigidita' (la rigidita' aggiunge contenuto oltre i ranghi)."""
    rows = rig_rows(k, r, sample=sample, max_flips=max_flips)
    return reducible_from_rank_rows(rows)


def reducible_from_rank_rows(rows: List[RigRow]) -> Tuple[bool, List[tuple]]:
    """killer-1 da righe gia' calcolate (per riusare un'unica passata di rigidita')."""
    sig: Dict[Tuple[int, int], set] = defaultdict(set)
    for row in rows:
        sig[(row.rank_gf2, row.rank_q)].add(row.rigidity)
    splits = [(key, sorted(v)) for key, v in sig.items() if len(v) > 1]
    return len(splits) == 0, splits


def _load_cost_table(m: int):
    """Tabella formula-size per m variabili.  Per m=4 (~500-900 s a costruirla) usa la
    cache del lab .cache/ct4.pkl se presente; per m<=3 la calcola al volo (veloce); per
    m>4 ritorna None (non enumerabile / fuori dizionario su questo asse)."""
    if m <= 3:
        return min_formula_sizes(m, 60)
    if m == 4:
        cache = Path(__file__).resolve().parents[2] / ".cache" / "ct4.pkl"
        if cache.exists():
            with open(cache, "rb") as fh:
                return pickle.load(fh)
        return min_formula_sizes(4, 60)   # lento (~500-900 s) se la cache manca
    return None


def dict_table(k: int, r: int, *, sample: List[int] | None = None,
               max_flips: int = 8, ct=None) -> Tuple[bool, List[tuple]]:
    """killer-2: la rigidita' e' ricostruibile dal DIZIONARIO CONGIUNTO del lab
    (cost del Modulo 6, gf2_degree, sensitivity, block_sensitivity) — come adeg nel
    Modulo 29?  Ogni invariante e' calcolato su f come funzione di 2k variabili.

    Ritorna (reconstructible, splits): reconstructible=True sse ogni firma del
    dizionario congiunto mappa a UN SOLO valore di rigidita'.  splits = firme che si
    spezzano (la rigidita' separa funzioni su cui il dizionario concorda -> contenuto
    FUORI dizionario).  ``ct`` opzionale = tabella costo precaricata (per k=2/m=4 usa la
    cache .cache/ct4.pkl); se assente, cost = None e il dizionario usa solo gli
    invarianti di analisi booleana (gf2_degree, sensitivity, block_sensitivity)."""
    m = 2 * k
    if ct is None:
        ct = _load_cost_table(m)
    rows = rig_rows(k, r, sample=sample, max_flips=max_flips)
    return dict_table_rows(rows, m, ct)


def dict_table_rows(rows: List[RigRow], m: int, ct) -> Tuple[bool, List[tuple]]:
    """killer-2 da righe gia' calcolate (riusa un'unica passata di rigidita')."""
    sig: Dict[tuple, set] = defaultdict(set)
    for row in rows:
        tt = row.tt
        cost = ct.cost[tt] if ct is not None else None  # cost non enumerabile a m>4
        key = (cost, sg.gf2_degree(tt, m), sg.sensitivity(tt, m),
               sg.block_sensitivity(tt, m))
        sig[key].add(row.rigidity)
    splits = [(key, sorted(v)) for key, v in sig.items() if len(v) > 1]
    return len(splits) == 0, splits


# --------------------------------------------------------------------------- #
#  Controllo perm-NON-invarianza: mescolare i due lati DEVE muovere la rigidita' #
# --------------------------------------------------------------------------- #

def _permute_vars(tt: int, m: int, perm: Tuple[int, ...]) -> int:
    """Applica la permutazione ``perm`` delle m variabili a una truth table (bit i ->
    bit perm[i]).  Restituisce la nuova truth table."""
    out = 0
    N = 1 << m
    for x in range(N):
        y = 0
        for i in range(m):
            if (x >> i) & 1:
                y |= 1 << perm[i]
        if (tt >> x) & 1:
            out |= 1 << y
    return out


def side_mixing_spread(tt: int, k: int, r: int, *, max_flips: int = 8) -> Tuple[List[int], List[int]]:
    """Sotto TUTTE le permutazioni S_{2k} delle 2k variabili (che MESCOLANO i due lati),
    raccoglie il multiset dei valori di rigidita' di M_{f∘perm} a bipartizione FISSA, e
    in parallelo il multiset di un CONTROLLO perm-invariant (la sensitivity di f∘perm).

    Predizione del lever-A: la rigidita' VARIA (spread>1) perche' la bipartizione e'
    fissata e mescolare i lati cambia la matrice; la sensitivity resta PIATTA (spread=1)
    perche' e' invariante per permutazione.  Ritorna (rig_values, sens_values) ordinati."""
    m = 2 * k
    rig_vals: List[int] = []
    sens_vals: List[int] = []
    for perm in permutations(range(m)):
        tt2 = _permute_vars(tt, m, perm)
        f2 = tt_to_fn(tt2, m)
        Mp = comm_matrix_pm(f2, k)
        rig_vals.append(rigidity_q_pm_exact(Mp, r, max_flips=max_flips))
        sens_vals.append(sg.sensitivity(tt2, m))
    return sorted(rig_vals), sorted(sens_vals)


# --------------------------------------------------------------------------- #
#  Leva cross-level                                                            #
# --------------------------------------------------------------------------- #

def leverage(ks: List[int], *, exact_up_to: int = 2,
             max_flips: int = 8) -> List[Tuple[int, Fraction, Fraction]]:
    """La metrica di leva lambda(k->k+1) = rho(k+1) / rho(k) sui livelli ``ks``.

    rho(k) usa la rigidita' ESATTA per k<=exact_up_to (Q ±1 Hadamard) e il bound
    CERTIFICATO oltre (lower bound).  Target r = 2^{k-1} a ogni livello.  Ritorna la
    lista di (k, rho(k), lambda(k->k+1)) — l'ultimo lambda e' None-equivalente (0/0
    evitato) se non c'e' livello successivo."""
    from .rigidity import rho
    rhos: Dict[int, Fraction] = {}
    for k in ks:
        target = 1 << (k - 1)
        rhos[k] = rho(k, target, exact_up_to=exact_up_to, max_flips=max_flips)
    out: List[Tuple[int, Fraction, Fraction]] = []
    for i, k in enumerate(ks):
        if i + 1 < len(ks) and rhos[k] != 0:
            lam = rhos[ks[i + 1]] / rhos[k]
        else:
            lam = Fraction(0)
        out.append((k, rhos[k], lam))
    return out


def leverage_verdict(lev: List[Tuple[int, Fraction, Fraction]]) -> str:
    """Classifica la sequenza dei lambda: 'monotone-increasing (>1)' (leverage),
    altrimenti 'bounded/non-monotone' (survival-no-leverage)."""
    lams = [lam for (_, _, lam) in lev[:-1]]  # ultimo lambda e' placeholder
    if not lams:
        return "n/a"
    increasing = all(lams[i] >= lams[i - 1] for i in range(1, len(lams)))
    all_gt1 = all(lam > 1 for lam in lams)
    if increasing and all_gt1:
        return "monotone-increasing (>1) => LEVERAGE"
    return "bounded/non-monotone => SURVIVAL-NO-LEVERAGE"
