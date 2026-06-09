"""Grafo degli strati di MCSP-size e il "down-degree" locale (Ciclo 5).

⚠ DEPRECATO come METRICA (vedi ``collapse.py``, Module 19). Questo modulo è il
BANCO DI MISURA del Ciclo 5; il suo discriminante ``d_flip`` è stato DISSOLTO
dall'audit: (W1) d_flip(f) = #{k : cost[f XOR (1<<k)] < cost[f]} è il GRADIENTE
discreto di MCSP-size — ricostruibile da ``cost`` solo, è la derivata di un
oggetto-KT, non un invariante nuovo; (W2) NON è canonico (cambia su 154/256
funzioni se si sostituisce formula-size con profondità DT). Resta utile come
strumento di misura esatta su istanze minuscole, NON come discriminante
strutturale. La chiusura riproducibile è in ``pnp_lab/meta_complexity/collapse.py``.

Contesto (META-COMPLESSITA'). Il Modulo 6 dà la dimensione di formula ESATTA
``cost[f]`` di ogni funzione booleana su n variabili (n<=4). Raggruppando le
funzioni per ``cost`` si ottengono gli STRATI di MCSP-size. L'ipotesi H5 chiede
se un invariante LOCALE di "down-degree" — quante mosse singole ABBASSANO
strettamente il costo — stratifichi ulteriormente le funzioni, distinguendole
DENTRO uno strato di pari MCSP-size.

Raffinamento cruciale (PI). Esistono due tipi di mossa, profondamente diversi:

  (A) INPUT-NEGATION  x_i -> ¬x_i.  È un AUTOMORFISMO del costo: negare una
      variabile in una formula ottima dà una formula di pari taglia, quindi
      ``cost`` è invariante. Atteso: down-degree ≡ 0 OVUNQUE (killer-1 per A).
      La implementiamo come CONTROLLO, per confermare che è banale.

  (B) OUTPUT-FLIP (vicino di Hamming nella tavola di verità). Flippare UN bit
      di output sposta f in una funzione f' la cui taglia può scendere. NON è
      un automorfismo: ``d_flip`` può essere >0 e variare DENTRO uno strato. È
      qui che il discriminante è davvero aperto.

Tutto è ESATTO e deterministico (interi, niente float). Riusa
``pnp_lab.circuits.min_formula_sizes`` come unica sorgente di ``cost``.
"""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from itertools import permutations
from typing import Dict, List, Tuple

from pnp_lab.circuits import ComplexityTable, min_formula_sizes, mask_for


# --------------------------------------------------------------------------- #
#  Mosse sulla tavola di verità                                               #
# --------------------------------------------------------------------------- #

def negate_input(tt: int, n: int, i: int) -> int:
    """Negazione della i-esima variabile di input: x_i -> ¬x_i.

    Permuta le 2^n righe scambiando ogni input ``idx`` con ``idx`` a cui è
    flippato il bit i. È un AUTOMORFISMO del costo (killer-1, mossa A).
    """
    if not (0 <= i < n):
        raise ValueError(f"variabile {i} fuori range per n={n}")
    N = 1 << n
    out = 0
    for idx in range(N):
        if (tt >> idx) & 1:
            out |= 1 << (idx ^ (1 << i))
    return out


def flip_output(tt: int, k: int) -> int:
    """Flippa il valore di output sull'input ``k`` (vicino di Hamming, mossa B)."""
    return tt ^ (1 << k)


def permute_inputs(tt: int, n: int, perm: Tuple[int, ...]) -> int:
    """Permuta le variabili: la nuova variabile j prende il ruolo di ``perm[j]``.

    Rimappa ogni input ``idx`` all'input i cui bit sono permutati.
    """
    N = 1 << n
    out = 0
    for idx in range(N):
        if (tt >> idx) & 1:
            nidx = 0
            for j in range(n):
                if (idx >> perm[j]) & 1:
                    nidx |= 1 << j
            out |= 1 << nidx
    return out


# --------------------------------------------------------------------------- #
#  Down-degree per le due mosse                                               #
# --------------------------------------------------------------------------- #

def down_degree_negation(ct: ComplexityTable, tt: int, n: int) -> int:
    """#input-negation che ABBASSANO strettamente il costo (atteso 0, killer-1)."""
    c0 = ct.cost[tt]
    d = 0
    for i in range(n):
        nb = negate_input(tt, n, i)
        if ct.cost[nb] < c0:
            d += 1
    return d


def down_degree_flip(ct: ComplexityTable, tt: int, n: int) -> int:
    """#output-flip (sui 2^n input) che ABBASSANO strettamente il costo (mossa B)."""
    c0 = ct.cost[tt]
    N = 1 << n
    d = 0
    for k in range(N):
        nb = flip_output(tt, k)
        if ct.cost[nb] < c0:
            d += 1
    return d


# --------------------------------------------------------------------------- #
#  Invarianti classici esatti (per i killer-2)                                #
# --------------------------------------------------------------------------- #

def gf2_degree(tt: int, n: int) -> int:
    """Grado del polinomio GF(2) (ANF) di f. Esatto via trasformata di Möbius."""
    N = 1 << n
    # coefficienti ANF tramite trasformata di Möbius binaria sul reticolo dei subset
    coeff = [(tt >> i) & 1 for i in range(N)]
    j = 1
    while j < N:
        for i in range(N):
            if i & j:
                coeff[i] ^= coeff[i ^ j]
        j <<= 1
    deg = 0
    for i in range(N):
        if coeff[i]:
            deg = max(deg, bin(i).count("1"))
    return deg


def sensitivity(tt: int, n: int) -> int:
    """Sensitivity di f = max sui input della #variabili sensibili in quell'input."""
    N = 1 << n
    best = 0
    for idx in range(N):
        bit = (tt >> idx) & 1
        s = 0
        for i in range(n):
            if ((tt >> (idx ^ (1 << i))) & 1) != bit:
                s += 1
        best = max(best, s)
    return best


def block_sensitivity(tt: int, n: int) -> int:
    """Block-sensitivity esatta di f = max su input del #blocchi disgiunti sensibili.

    Per ogni input x si cerca il massimo numero di blocchi DISGIUNTI B (sottoinsiemi
    di variabili) tali che flippando l'intero blocco l'output cambia. Calcolo esatto
    via ricerca del massimo numero di blocchi sensibili disgiunti (n piccolo: forza
    bruta sull'insieme dei blocchi minimali — qui basta enumerare i blocchi sensibili
    e impacchettarli, ma per n<=4 enumeriamo direttamente con un packing esatto).
    """
    N = 1 << n
    best = 0
    full = N  # 2^n input
    for idx in range(N):
        out0 = (tt >> idx) & 1
        # tutti i sottoinsiemi non vuoti di variabili che, flippati, cambiano l'output
        sens_blocks: List[int] = []
        for mask in range(1, 1 << n):
            if ((tt >> (idx ^ mask)) & 1) != out0:
                sens_blocks.append(mask)
        # massimo packing di blocchi a due a due disgiunti -> max #blocchi
        best = max(best, _max_disjoint_packing(sens_blocks))
    _ = full
    return best


def _max_disjoint_packing(blocks: List[int]) -> int:
    """Massimo numero di maschere a due a due disgiunte (esatto, backtracking).

    Tiene solo i blocchi MINIMALI (un blocco che contiene un altro blocco
    sensibile è inutile per massimizzare la cardinalità) e fa branch & bound.
    """
    # filtra i non-minimali
    minimal: List[int] = []
    for b in blocks:
        if not any(other != b and (other & b) == other for other in blocks):
            minimal.append(b)
    minimal = sorted(set(minimal), key=lambda m: bin(m).count("1"))

    best = 0

    def rec(idx: int, used: int, count: int) -> None:
        nonlocal best
        if count > best:
            best = count
        # bound: ogni blocco rimanente disgiunto da used può aggiungere al più 1
        remaining = sum(1 for m in minimal[idx:] if (m & used) == 0)
        if count + remaining <= best:
            return
        for j in range(idx, len(minimal)):
            m = minimal[j]
            if (m & used) == 0:
                rec(j + 1, used | m, count + 1)

    rec(0, 0, 0)
    return best


# --------------------------------------------------------------------------- #
#  Orbita sotto il gruppo iperottaedrale B_n (per i killer-3)                  #
# --------------------------------------------------------------------------- #

def orbit_B(tt: int, n: int) -> frozenset[int]:
    """Orbita di f sotto B_n: negazioni di input × permutazioni di variabili.

    |B_n| = 2^n · n!  (per n=3: 8·6 = 48). ``cost`` è invariante su tutta l'orbita.
    """
    orbit: set[int] = set()
    for perm in permutations(range(n)):
        base = permute_inputs(tt, n, perm)
        # tutte le 2^n combinazioni di negazioni delle variabili
        for negmask in range(1 << n):
            t = base
            for i in range(n):
                if (negmask >> i) & 1:
                    t = negate_input(t, n, i)
            orbit.add(t)
    return frozenset(orbit)


# --------------------------------------------------------------------------- #
#  Strati e raffinamento di partizioni                                        #
# --------------------------------------------------------------------------- #

def strata(ct: ComplexityTable) -> Dict[int, List[int]]:
    """{cost: [tt, ...]} — gli strati di MCSP-size."""
    out: Dict[int, List[int]] = defaultdict(list)
    for tt, c in ct.cost.items():
        out[c].append(tt)
    return {c: sorted(v) for c, v in sorted(out.items())}


def _classes(items: List[int], key) -> Dict[object, frozenset[int]]:
    """Partizione di ``items`` indotta dalla funzione ``key`` (etichetta -> classe)."""
    groups: Dict[object, set[int]] = defaultdict(set)
    for it in items:
        groups[key(it)].add(it)
    return {lab: frozenset(s) for lab, s in groups.items()}


def _blocks(items: List[int], key) -> set[frozenset[int]]:
    """L'insieme dei BLOCCHI (ignorando le etichette) della partizione indotta."""
    return set(_classes(items, key).values())


def partition_refinement(part_a: set[frozenset[int]],
                         part_b: set[frozenset[int]]) -> str:
    """Relazione tra due partizioni dello STESSO insieme.

    Ritorna: "COINCIDE", "RAFFINA" (a più fine di b), "RAFFINATA" (a più grossa
    di b), oppure "INCOMPARABILE".
    """
    if part_a == part_b:
        return "COINCIDE"
    a_refines_b = all(any(A <= B for B in part_b) for A in part_a)
    b_refines_a = all(any(B <= A for A in part_a) for B in part_b)
    if a_refines_b and not b_refines_a:
        return "RAFFINA"
    if b_refines_a and not a_refines_b:
        return "RAFFINATA"
    return "INCOMPARABILE"


# --------------------------------------------------------------------------- #
#  Analisi per-strato                                                         #
# --------------------------------------------------------------------------- #

@dataclass
class StratumReport:
    cost: int
    num_funcs: int
    dflip_values: List[int]          # i valori distinti di d_flip nello strato
    rel_sensitivity: str | None      # relazione partizione-d_flip vs sensitivity
    rel_block_sensitivity: str | None
    rel_gf2_degree: str | None
    rel_orbit: str | None

    @property
    def num_dflip_values(self) -> int:
        return len(self.dflip_values)


def analyze(n: int, cap: int = 60) -> Tuple[ComplexityTable, List[StratumReport]]:
    """Analisi completa: per ogni strato di costo, |{d_flip}| e i confronti.

    Per gli strati con |{d_flip}| >= 2 confronta la partizione-per-d_flip con
    quelle indotte da sensitivity, block_sensitivity, gf2_degree e orbita-B_n.
    """
    ct = min_formula_sizes(n, cap)
    st = strata(ct)

    # cache invarianti
    dflip = {tt: down_degree_flip(ct, tt, n) for tt in ct.cost}
    sens = {tt: sensitivity(tt, n) for tt in ct.cost}
    bsens = {tt: block_sensitivity(tt, n) for tt in ct.cost}
    deg = {tt: gf2_degree(tt, n) for tt in ct.cost}

    reports: List[StratumReport] = []
    for c, items in st.items():
        vals = sorted(set(dflip[tt] for tt in items))
        rep = StratumReport(
            cost=c, num_funcs=len(items), dflip_values=vals,
            rel_sensitivity=None, rel_block_sensitivity=None,
            rel_gf2_degree=None, rel_orbit=None,
        )
        if len(vals) >= 2:
            P = _blocks(items, lambda tt: dflip[tt])
            rep.rel_sensitivity = partition_refinement(
                P, _blocks(items, lambda tt: sens[tt]))
            rep.rel_block_sensitivity = partition_refinement(
                P, _blocks(items, lambda tt: bsens[tt]))
            rep.rel_gf2_degree = partition_refinement(
                P, _blocks(items, lambda tt: deg[tt]))
            # partizione per orbita-B_n: l'etichetta è l'orbita stessa (ristretta
            # allo strato), ma le orbite sono già contenute negli strati (cost è
            # invariante), quindi usiamo l'orbita completa come chiave canonica.
            orbit_of = _orbit_labels(items, n)
            rep.rel_orbit = partition_refinement(
                P, _blocks(items, lambda tt: orbit_of[tt]))
        reports.append(rep)
    return ct, reports


def _orbit_labels(items: List[int], n: int) -> Dict[int, int]:
    """Etichetta canonica dell'orbita-B_n per ogni elemento (min dell'orbita)."""
    label: Dict[int, int] = {}
    itemset = set(items)
    for tt in items:
        if tt in label:
            continue
        orb = orbit_B(tt, n)
        canon = min(orb)
        for o in orb:
            if o in itemset:
                label[o] = canon
    return label
