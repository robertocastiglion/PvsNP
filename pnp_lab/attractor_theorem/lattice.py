"""Reticolo di ricostruibilita' dei 5 invarianti di orbita su n=3 booleane.

GRUPPO DI SIMMETRIA DICHIARATO: B_n (gruppo iperoctaedrale) = permutazioni delle n
variabili di input × negazioni di ciascun input.  |B_3| = 3! * 2^3 = 48.
Questo e' il gruppo usato in tutti i moduli esistenti del lab: orbit_B in
pnp_lab/meta_complexity/strata_graph.py; la funzione adeg_vs_dictionary in
pnp_lab/approx_degree/adeg.py usa come chiave esattamente il vettore degli invarianti
B_n (cost, gf2_degree, sensitivity, block_sensitivity).

I 5 INVARIANTI (tutti B_n-invarianti, esatti):
    cost            -- dimensione di formula minima  (pnp_lab.circuits.min_formula_sizes)
    gf2_degree      -- grado del polinomio GF(2) / ANF  (strata_graph.gf2_degree)
    sensitivity     -- sensitivity classica              (strata_graph.sensitivity)
    block_sensitivity -- block-sensitivity               (strata_graph.block_sensitivity)
    adeg            -- grado approssimato adeg_{1/3}    (approx_degree.approx_degree)

MISURE ESATTE (int/Fraction, NO float).  Deterministico.
"""

from __future__ import annotations

import itertools
from fractions import Fraction
from typing import Dict, FrozenSet, List, Optional, Set, Tuple

# ── riuso funzioni esistenti ──────────────────────────────────────────────────
from pnp_lab.circuits import min_formula_sizes
from pnp_lab.meta_complexity.strata_graph import (
    gf2_degree,
    sensitivity,
    block_sensitivity,
    orbit_B,
)
from pnp_lab.approx_degree.adeg import approx_degree

# nomi canonici degli invarianti (ordine fisso per tutto il modulo)
INV_NAMES: Tuple[str, ...] = (
    "cost",
    "gf2_degree",
    "sensitivity",
    "block_sensitivity",
    "adeg",
)


# ── 1. tabella orbita -> invarianti ──────────────────────────────────────────

def orbit_invariant_table(n: int = 3) -> Dict[int, Dict[str, int]]:
    """Per ogni orbita di B_n su {0,1}^n -> {0,1} restituisce il dict dei 5 invarianti.

    La chiave e' il rappresentante canonico dell'orbita = min dell'orbita.
    Complessita': O(2^(2^n)) con n piccolo (per n=3: 256 funzioni, ~20 orbite).
    """
    ct = min_formula_sizes(n)
    N_funcs = 1 << (1 << n)

    # prima passata: trova tutti i canonici senza ripetizioni
    visited: Set[int] = set()
    canons: Set[int] = set()

    for tt in range(N_funcs):
        if tt in visited:
            continue
        orb = orbit_B(tt, n)
        canon = min(orb)
        visited.update(orb)
        canons.add(canon)

    # seconda passata: calcola gli invarianti per ogni canonico
    table: Dict[int, Dict[str, int]] = {}
    for canon in sorted(canons):
        table[canon] = {
            "cost":              ct.cost[canon],
            "gf2_degree":        gf2_degree(canon, n),
            "sensitivity":       sensitivity(canon, n),
            "block_sensitivity": block_sensitivity(canon, n),
            "adeg":              approx_degree(canon, n),
        }

    return table


# ── 2. matrice di ricostruibilita' ───────────────────────────────────────────

def reconstructibility_matrix(
    table: Dict[int, Dict[str, int]]
) -> Dict[str, Dict[str, bool]]:
    """M[I][J] = True sse I e' ricostruibile da J (splits(I|J) = 0).

    'I ricostruibile da J' significa: per ogni coppia di orbite o1, o2,
    J(o1) == J(o2) implica I(o1) == I(o2).
    Equivalente: la partizione indotta da J e' piu' fine di quella di I.

    La matrice e' un dict-of-dict su INV_NAMES x INV_NAMES.
    La diagonale e' sempre True (riflessivita').
    """
    orbits = list(table.keys())
    M: Dict[str, Dict[str, bool]] = {I: {} for I in INV_NAMES}

    for I in INV_NAMES:
        for J in INV_NAMES:
            # controlla se J(o1)==J(o2) => I(o1)==I(o2) per tutte le coppie
            ok = True
            j_to_i: Dict[int, int] = {}
            for orb in orbits:
                jval = table[orb][J]
                ival = table[orb][I]
                if jval in j_to_i:
                    if j_to_i[jval] != ival:
                        ok = False
                        break
                else:
                    j_to_i[jval] = ival
            M[I][J] = ok

    return M


def reconstructible_from(
    inv: str,
    S: List[str],
    table: Dict[int, Dict[str, int]],
) -> bool:
    """True sse `inv` e' ricostruibile dal sottoinsieme S di invarianti.

    Ovvero: per ogni coppia di orbite o1, o2,
    (tutti i J in S: J(o1)==J(o2)) implica inv(o1)==inv(o2).
    """
    orbits = list(table.keys())
    joint_to_inv: Dict[tuple, int] = {}
    for orb in orbits:
        key = tuple(table[orb][J] for J in S)
        ival = table[orb][inv]
        if key in joint_to_inv:
            if joint_to_inv[key] != ival:
                return False
        else:
            joint_to_inv[key] = ival
    return True


# ── 3. separatori minimi ─────────────────────────────────────────────────────

def _separates_all(
    S: Tuple[str, ...],
    table: Dict[int, Dict[str, int]],
) -> bool:
    """True sse il sottoinsieme S separa tutte le orbite (joint invariant iniettivo)."""
    orbits = list(table.keys())
    seen: Set[tuple] = set()
    for orb in orbits:
        key = tuple(table[orb][inv] for inv in S)
        if key in seen:
            return False
        seen.add(key)
    return True


def minimum_separators(
    table: Dict[int, Dict[str, int]]
) -> List[List[str]]:
    """Tutti i G ⊆ INV_NAMES di cardinalita' minima che separano TUTTE le orbite.

    Esaustivo su 2^5 = 32 sottoinsiemi non vuoti.  Restituisce la lista dei
    separatori minimi (liste di nomi), ordinati lessicograficamente.
    """
    min_size: Optional[int] = None
    result: List[List[str]] = []

    for size in range(1, len(INV_NAMES) + 1):
        for S in itertools.combinations(INV_NAMES, size):
            if _separates_all(S, table):
                if min_size is None:
                    min_size = size
                if size == min_size:
                    result.append(list(S))
        if min_size is not None:
            break

    return result


# ── 4. diagramma di Hasse ────────────────────────────────────────────────────

def hasse_diagram(
    M: Dict[str, Dict[str, bool]]
) -> Dict[str, object]:
    """Riduzione transitiva del preordine di ricostruibilita'.

    Preordine: I <= J (J e' almeno informativo quanto J) sse M[I][J] = True
    (I ricostruibile da J).

    Gestisce le classi di equivalenza mutuamente ricostruibili (I<=J e J<=I).
    Restituisce:
        classes      -- lista di frozenset (una per classe di equiv)
        class_labels -- dict: frozenset -> etichetta stringa (ordine alfabetico)
        order        -- dict: label_A -> set{label_B} = A <= B nel quoziente
        arcs         -- lista di coppie (label_A, label_B) nella riduzione transitiva
                        (A < B, A coperto da B)
        shape        -- 'chain' / 'antichain' / 'other'
    """
    names = list(INV_NAMES)

    # 1. classi di equivalenza (mutuamente ricostruibili)
    eq_classes: List[FrozenSet[str]] = []
    assigned: Set[str] = set()
    for name in names:
        if name in assigned:
            continue
        cls: Set[str] = {name}
        for other in names:
            if other != name and M[name][other] and M[other][name]:
                cls.add(other)
        fs = frozenset(cls)
        if fs not in eq_classes:
            eq_classes.append(fs)
        assigned.update(cls)

    # etichette: stringa ordinata dei nomi della classe
    def label_of(cls: FrozenSet[str]) -> str:
        return "/".join(sorted(cls))

    labels = [label_of(c) for c in eq_classes]
    # mappa nome -> indice classe
    name_to_cls: Dict[str, int] = {}
    for i, cls in enumerate(eq_classes):
        for nm in cls:
            name_to_cls[nm] = i

    n_cls = len(eq_classes)

    # 2. preordine sul quoziente: classe A <= classe B sse ogni I in A e' ricostruibile
    #    da ogni J in B (basta un J in B per verificarlo, dato che le classi sono
    #    interne — ma usiamo qualsiasi rappresentante)
    # A <= B sse (scegli rapp_A in A, rapp_B in B): M[rapp_A][rapp_B]
    def cls_leq(i: int, j: int) -> bool:
        """Classe i <= Classe j nel quoziente."""
        ra = next(iter(eq_classes[i]))
        rb = next(iter(eq_classes[j]))
        return bool(M[ra][rb])

    # matrice reach[i][j] = cls i <= cls j (nel quoziente, che e' un ordine parziale)
    reach = [[cls_leq(i, j) for j in range(n_cls)] for i in range(n_cls)]

    # 3. riduzione transitiva: arco i->j sse reach[i][j] e i!=j
    #    e NON esiste k (k!=i, k!=j) con reach[i][k] e reach[k][j]
    arcs: List[Tuple[str, str]] = []
    for i in range(n_cls):
        for j in range(n_cls):
            if i == j or not reach[i][j]:
                continue
            # verifica che non ci sia un intermedio
            has_intermediate = any(
                k != i and k != j and reach[i][k] and reach[k][j]
                for k in range(n_cls)
            )
            if not has_intermediate:
                arcs.append((labels[i], labels[j]))

    # 4. shape
    n_arcs = len(arcs)
    if n_arcs == n_cls - 1 and n_cls > 1:
        # possibile catena: verifica che sia totalmente ordinato
        is_chain = all(
            reach[i][j] or reach[j][i]
            for i in range(n_cls)
            for j in range(n_cls)
        )
        shape = "chain" if is_chain else "other"
    elif n_arcs == 0:
        shape = "antichain"
    else:
        shape = "other"

    return {
        "classes":      eq_classes,
        "class_labels": {label_of(c): c for c in eq_classes},
        "order":        {labels[i]: {labels[j] for j in range(n_cls) if reach[i][j] and i != j}
                         for i in range(n_cls)},
        "arcs":         arcs,
        "shape":        shape,
    }


# ── 5. sommario ──────────────────────────────────────────────────────────────

def summary(n: int = 3) -> Dict[str, object]:
    """Sommario completo del reticolo di ricostruibilita' su n variabili.

    Restituisce un dict con:
        n_orbits         -- numero di orbite B_n
        min_sep_size     -- cardinalita' minima di un separatore
        min_separators   -- lista dei separatori minimi
        recon_matrix     -- matrice 5x5 come dict[I][J] = bool
        hasse            -- output di hasse_diagram
        shape            -- 'chain'/'antichain'/'other'
        group            -- descrizione del gruppo usato
    """
    table = orbit_invariant_table(n)
    M = reconstructibility_matrix(table)
    seps = minimum_separators(table)
    hasse = hasse_diagram(M)

    return {
        "n_orbits":     len(table),
        "min_sep_size": len(seps[0]) if seps else None,
        "min_separators": seps,
        "recon_matrix": M,
        "hasse":        hasse,
        "shape":        hasse["shape"],
        "group":        f"B_{n} (permutazioni x negazioni input, |B_{n}|={6 * (1<<n) if n==3 else '?'})",
    }
