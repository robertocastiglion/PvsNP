"""Calcolo veloce dei coefficienti di Kronecker via tavola dei caratteri precalcolata.

Ottimizzazione chiave rispetto a kronecker.py:
  - character_table(d) calcola l'intera tavola dei caratteri di S_d UNA sola volta
    e memoizza il risultato in _CT_CACHE (dict a livello di modulo, persiste per
    l'intera durata del processo).
  - g_fast(lam, mu, nu) usa la tavola precalcolata per il prodotto triplo con
    PURA aritmetica intera (nessun Fraction per termine): evita il Fraction overhead
    di kronecker() e riusa ogni mn_character senza ricalcoli.
  - census(d) enumera tutte le C(p(d)+2,3) terne non ordinate in un unico ciclo
    e salva la lista degli zeri in .cache/kronecker_zeros_d{d}.pkl.

Garanzia di correttezza: g_fast == kronecker su tutte le terne d<=6 (test_gct_fast.py).

IPOTESI VERIFICATA (Ciclo 0b): il "muro brute-force d>=7" e' un ARTEFATTO
implementativo.  La formula g = (1/d!) sum |C_alpha| chi_lam chi_mu chi_nu
richiede solo la tavola dei caratteri di S_d, che ha p(d)^2 voci.
Per d=7: 15^2=225 voci, 680 terne — trivialmente enumerabili in pochi secondi.
"""

from __future__ import annotations

import pickle
from dataclasses import dataclass
from math import factorial
from pathlib import Path
from typing import Dict, List, Tuple

from .kronecker import mn_character, partitions, z_alpha, _triples

Partition = Tuple[int, ...]

# ---------------------------------------------------------------------------
# Cache a livello di modulo (d -> CharTable)
# ---------------------------------------------------------------------------
_CT_CACHE: Dict[int, "CharTable"] = {}

# Percorso .cache nella radice del repository (tre livelli sopra questo file)
# pnp_lab/gct_kronecker/fast.py -> parent(gct_kronecker) -> parent(pnp_lab) -> parent(root)
_CACHE_DIR = Path(__file__).resolve().parent.parent.parent / ".cache"


# ---------------------------------------------------------------------------
# Struttura dati della tavola
# ---------------------------------------------------------------------------
@dataclass
class CharTable:
    """Tavola dei caratteri completa di S_d.

    Attributi
    ---------
    d           : grado del gruppo simmetrico
    parts       : lista di tutte le partizioni di d (stesso ordine di partitions(d))
    chi         : chi[i][j] = mn_character(parts[i], parts[j])  (int esatto)
    class_sizes : class_sizes[j] = d! / z_{parts[j]}  (dimensione della classe j)
    part_index  : mappa partizione -> indice per lookup O(1)
    """
    d: int
    parts: List[Partition]
    chi: List[List[int]]
    class_sizes: List[int]
    part_index: Dict[Partition, int]


# ---------------------------------------------------------------------------
# API pubblica
# ---------------------------------------------------------------------------
def character_table(d: int) -> CharTable:
    """Tavola caratteri COMPLETA di S_d, calcolata una volta e memoizzata.

    Righe  = irriducibili S^lambda  (lambda = partizione di d);
    Colonne = classi di coniugio alpha  (alpha = partizione di d).
    Voce chi[i][j] = chi^{lambda_i}(alpha_j) via Murnaghan-Nakayama (int esatto).
    class_sizes[j] = d! / z_{alpha_j}  (numero di permutazioni nel tipo-ciclo j).
    """
    if d in _CT_CACHE:
        return _CT_CACHE[d]

    ps = partitions(d)
    n = len(ps)
    part_index: Dict[Partition, int] = {p: i for i, p in enumerate(ps)}
    d_fact = factorial(d)

    # Calcolo completo: n*n chiamate a mn_character (con lru_cache su mn_character,
    # ogni coppia unica e' calcolata una sola volta anche per le ricorsioni interne)
    chi: List[List[int]] = [
        [mn_character(ps[i], ps[j]) for j in range(n)]
        for i in range(n)
    ]

    # Dimensioni delle classi di coniugio (interi esatti)
    class_sizes: List[int] = [d_fact // z_alpha(ps[j]) for j in range(n)]

    ct = CharTable(
        d=d, parts=ps, chi=chi, class_sizes=class_sizes, part_index=part_index
    )
    _CT_CACHE[d] = ct
    return ct


def g_fast(lam: Partition, mu: Partition, nu: Partition) -> int:
    """Coefficiente di Kronecker g(lam, mu, nu) via tavola precalcolata.

    Formula esatta:
        g = (1/d!) * sum_alpha  |C_alpha| * chi^lam(alpha) * chi^mu(alpha) * chi^nu(alpha)

    dove |C_alpha| = d! / z_alpha.  Aritmetica INTERA pura (no Fraction per termine).
    Verifica che il numeratore sia divisibile per d! prima di ritornare.
    """
    d = sum(lam)
    if sum(mu) != d or sum(nu) != d:
        raise ValueError(
            f"lam, mu, nu devono partizionare lo stesso d; "
            f"ricevuto sum(lam)={d}, sum(mu)={sum(mu)}, sum(nu)={sum(nu)}"
        )

    ct = character_table(d)
    i = ct.part_index[lam]
    j = ct.part_index[mu]
    k = ct.part_index[nu]

    chi_i = ct.chi[i]
    chi_j = ct.chi[j]
    chi_k = ct.chi[k]
    cs = ct.class_sizes

    num = sum(cs[a] * chi_i[a] * chi_j[a] * chi_k[a] for a in range(len(ct.parts)))

    d_fact = factorial(d)
    assert num % d_fact == 0, (
        f"g_fast: numeratore non divisibile per d!={d_fact}: "
        f"num={num} per lam={lam}, mu={mu}, nu={nu}"
    )
    return num // d_fact


def census(
    d: int,
) -> Tuple[int, int, List[Tuple[Partition, Partition, Partition]]]:
    """Enumera tutte le terne non ordinate (lam<=mu<=nu) di partizioni di d.

    Pre-calcola la tavola dei caratteri UNA volta, poi scorre le C(p(d)+2,3) terne
    con pura aritmetica intera.

    Ritorna:
        (n_triples, n_zeros, zeros)

    dove zeros e' la lista delle terne canoniche con g=0.
    Salva zeros in .cache/kronecker_zeros_d{d}.pkl (crea .cache se mancante).
    """
    # Pre-calcola la tavola prima del ciclo (una sola volta per il processo)
    character_table(d)

    triples = _triples(d)
    zeros: List[Tuple[Partition, Partition, Partition]] = []

    for lam, mu, nu in triples:
        if g_fast(lam, mu, nu) == 0:
            zeros.append((lam, mu, nu))

    # Persistenza su disco
    _CACHE_DIR.mkdir(parents=True, exist_ok=True)
    pkl_path = _CACHE_DIR / f"kronecker_zeros_d{d}.pkl"
    with open(pkl_path, "wb") as fh:
        pickle.dump(zeros, fh)

    return len(triples), len(zeros), zeros
