"""Order-locality — a NON-permutation-invariant meta-object that reopens the
Magnification Frontier (Cycle 3).

EN-first summary (Honesty boundary at the bottom).

WHY THIS MODULE EXISTS.  The locality sub-branch (Module 21, ``locality.py``)
closed because the meta-function it used, ``MCSP[s]`` (HARD = "no small *formula*"),
is **permutation-invariant** in the coordinates of the truth table: formula size
does not care about the order or the naming of the input variables.  Every
"best k-local" leverage quantity therefore collapsed to a *symmetric* statistic of
the hard set — a global average that the duality dictionary already contains.  Two
cycles collapsed for that one structural reason.

The program's reopening criterion (stated when the sub-branch closed) was exact:
*reopening needs a meta-level object that is not permutation-invariant.*  This
module supplies one, with the smallest possible change to the existing machinery.

THE OBJECT — ``MBPSP[s]`` (Minimum Branching-Program / OBDD Size Problem at a fixed
order).  Same meta framing as ``locality.py`` (input = the whole ``N = 2^n``-bit
truth table of an n-bit function, read as N coordinates), but the complexity
measure is the **size of the reduced OBDD under a FIXED variable order**
``pi = (x_{n-1}, x_{n-2}, ..., x_0)`` (the highest-indexed variable is read first),
instead of formula size:

    MBPSP[s] : {0,1}^N -> {0,1},   N = 2^n,
    MBPSP[s](t) := ( min_obdd_size(t ; pi) > s )    # HARD = "no small OBDD at pi"

``min_obdd_size`` is exactly and cheaply computable (the reduced OBDD is canonical
for a fixed order: its node count = number of distinct non-constant subfunctions,
with redundant tests removed).  No dynamic-programming table is needed, so MBPSP is
*cheaper* to build than MCSP — n=4 (all 2^16 truth tables) takes well under a second.

WHY IT IS NOT PERMUTATION-INVARIANT.  OBDD size at a fixed order is invariant under
*negating* an input variable (it just swaps a node's two children), but NOT under
*permuting* the variables: the order singles out which variable sits at the top.
The textbook witness lives at n=4: ``f = (x0 & x1) | (x2 & x3)`` has a 6-node OBDD,
while the same function with variables 1,2 swapped, ``(x0 & x2) | (x1 & x3)``, needs
8 — two truth tables related by a coordinate permutation, with different size
(``variable_swap`` + ``min_obdd_size`` exhibit it).  Formula size cannot tell them
apart.  The fixed order is the "horizontal cut" the symmetric MCSP lacked.

THE MEASURE THAT READS THE ASYMMETRY — ``pair_influence`` (``pairinf``).
Single-coordinate influence cannot distinguish anything: the meta-function is
invariant under *translations* of the input cube (relabel inputs x -> x+a = negate
variables), and translations already act transitively on coordinates, so every
single coordinate has identical influence for BOTH MCSP and MBPSP.  The asymmetry
can only show at the level of *pairs*.  For a non-zero difference vector
``d in {1,...,N-1}`` (d = x XOR x', the input-variables in which two coordinates
differ),

    pairinf(d) := #{ t : MBPSP[s] is non-constant on the 4 inputs
                          {t, t^e0, t^ed, t^(e0^ed)} } ,

a translation-invariant integer (the base coordinate is fixed to 0 w.l.o.g.).  The
diagnostic is the **spread within a Hamming-weight class**: group the d's by
``weight(d)`` and look at ``max pairinf - min pairinf`` over each class.

    * permutation-invariant meta-function  =>  pairinf(d) depends only on weight(d)
      => spread = 0 in every class  (MCSP, all n).
    * order-dependent meta-function        =>  pairinf(d) depends on supp(d) (which
      variables, hence their place in the order) => spread > 0  (MBPSP, at n=4).

MEASURED (exact integers; frozen in tests/test_order_locality.py), threshold
s = round(maxOBDD * 0.5) (fixed-fraction, theta=0.5, as in locality.py Cycle 2):

    n   N    s    H        weight-class spread (w=1, 2, 3, 4)        verdict
    2   4    2    14       0, 0                                       symmetric (order silent)
    3   8    4    224      0, 0, 0                                    symmetric (order silent)
    4  16    6    64282    184, 176, 16, 0                            ORDER SURVIVES
    --- control: MCSP[s] (formula) ---
    4  16    8    25954    0, 0, 0, 0                                 symmetric (washed out)

So MBPSP[s]'s pair-influence at n=4 distinguishes equal-weight differences by their
order-support (e.g. w=1: differing in x3, the top variable, gives pairinf 4056;
differing in x1 gives 3872), while the MCSP control is flat.  This is the exact,
reproducible sense in which MBPSP[s] is NOT permutation-invariant — the reopening
criterion, met.

THE LEVERAGE (the cake's third cut), read honestly.  The asymmetry SWITCHES ON at
n=4 and is silent at n<=4-1 — exactly the level where OBDD order-sensitivity first
appears for individual functions (the (x0 x1)|(x2 x3) phenomenon needs 4 variables).
Per the leverage principle, a wall invisible below n=4 is not a failure: it locates
*where the staircase starts*, read by climbing.  But n=4 is the FIRST non-zero
level and n=5 (2^32 truth tables) is infeasible by brute force, so this module
establishes the OBJECT (non-invariant, exact) and locates the onset; it does NOT
yet measure a cross-level invariant of the asymmetry.  That is the next cycle's job.

Honesty boundary.
  * COMPUTED here (exact integers, no floats): min_obdd_size at a fixed order; its
    non-invariance under variable permutation (n=4 witness); MBPSP[s] as a meta-
    function; pair_influence and its weight-class spread for n=2,3,4, with the MCSP
    formula-size control (spread 0).
  * CITED, never computed: the magnification / locality theorems for branching
    programs and OBDDs and the asymptotic amplification (small LB -> separation):
    Oliveira-Pich 2019; Chen-Jin-Williams 2019/2020; Chen-Hirahara-Ren-Santhanam-
    Vyas (locality barrier).  At finite n the threshold is a single integer, not a
    regime; the amplification escapes tiny size.  No separation, no P vs NP claim.
    The spread is real but modest (~4.5% of the base at n=4, w=1) and is observed at
    a single non-trivial level; this module reopens the door, it does not walk
    through it.
"""

from __future__ import annotations

import sys
from collections import defaultdict
from dataclasses import dataclass
from typing import Dict, List, Sequence, Tuple

# Le truth-table a n=4 hanno 2^16 input; la ricorsione OBDD e' profonda al piu' n,
# ma alziamo il limite per sicurezza su build batch.
sys.setrecursionlimit(100000)


# ── min-OBDD-size a ordine FISSO (ROBDD canonico, intero esatto) ───────────

def min_obdd_size(t: int, n: int) -> int:
    """Numero di nodi dell'OBDD ridotto (ROBDD) della funzione n-bit con truth-table
    ``t``, all'ordine FISSO ``pi = (x_{n-1}, ..., x_0)`` (la variabile di indice piu'
    alto e' letta per prima / sta in cima).

    Il ROBDD e' canonico per un ordine fissato: il suo conteggio nodi = numero di
    sotto-funzioni distinte non-costanti (con i test ridondanti rimossi) + i terminali
    distinti.  Calcolo esatto in tempo poly(N): si scende ricorsivamente spezzando
    sulla variabile in cima rimasta, si fondono le sotto-funzioni uguali (memo) e si
    saltano i nodi ridondanti (entrambi i figli uguali).

    Convenzione di indici: l'input x in [0, 2^n) ha variabile j = bit j di x; la
    truth-table ``t`` ha bit x = valore della funzione su x.  Spezzare sulla variabile
    di indice piu' alto m-1 => meta' bassa = ``t & (2^(2^(m-1)) - 1)`` (var=0),
    meta' alta = ``t >> 2^(m-1)`` (var=1)."""
    nodes: set[Tuple[int, int]] = set()      # (m, table) = nodi interni distinti
    terminals: set[int] = set()              # sottoinsieme di {0, 1}

    def rec(m: int, table: int) -> None:
        if table == 0:
            terminals.add(0)
            return
        full = (1 << (1 << m)) - 1
        if table == full:
            terminals.add(1)
            return
        half = 1 << (m - 1)                  # lunghezza di ciascuna meta' = 2^(m-1)
        mask = (1 << half) - 1
        low = table & mask                   # variabile in cima = 0
        high = table >> half                 # variabile in cima = 1
        if low == high:                      # non dipende dalla var in cima: ridondante
            rec(m - 1, low)
            return
        key = (m, table)
        if key in nodes:
            return
        nodes.add(key)
        rec(m - 1, low)
        rec(m - 1, high)

    rec(n, t)
    return len(nodes) + len(terminals)


def obdd_costs(n: int) -> List[int]:
    """Il vettore dei costi OBDD: ``min_obdd_size(t)`` per ogni truth-table
    ``t in [0, 2^N)``, ``N = 2^n``.  Analogo a ``ComplexityTable.cost`` ma per la
    dimensione OBDD a ordine fisso (e calcolabile direttamente, senza DP)."""
    N = 1 << n
    return [min_obdd_size(t, n) for t in range(1 << N)]


def variable_swap(t: int, n: int, i: int, j: int) -> int:
    """La truth-table ottenuta permutando le variabili i,j (scambiando i bit i,j di
    OGNI input).  Usata per ESIBIRE la non-invarianza per permutazione: la stessa
    funzione, con due variabili scambiate, e' una truth-table diversa con (in
    generale) dimensione OBDD diversa allo stesso ordine."""
    if i == j:
        return t
    N = 1 << n
    out = 0
    for x in range(N):
        bi = (x >> i) & 1
        bj = (x >> j) & 1
        y = x & ~((1 << i) | (1 << j))
        y |= (bj << i) | (bi << j)
        if (t >> x) & 1:
            out |= 1 << y
    return out


# ── la meta-funzione MBPSP[s] e la soglia ──────────────────────────────────

def meta_truth_table_obdd(costs: Sequence[int], s: int) -> List[bool]:
    """MBPSP[s] come vettore indicizzato dalle truth-table di n-bit, dato il vettore
    ``costs`` (= ``obdd_costs(n)``).  Convenzione: HARD = (dimensione OBDD > s),
    parallela a ``locality.meta_truth_table``."""
    return [c > s for c in costs]


def hard_count(meta: Sequence[bool]) -> int:
    """H = #{istanze dure}."""
    return sum(1 for v in meta if v)


def fixed_fraction_threshold(costs: Sequence[int], theta: float = 0.5) -> int:
    """Policy a frazione fissa ``s = round(maxOBDD * theta)`` (stessa policy del ciclo 2
    di ``locality.py``; banker's rounding di Python, vedi quel modulo)."""
    return round(max(costs) * theta)


# ── pair-influence: la misura che LEGGE l'asimmetria d'ordine ──────────────

def pair_influence(meta: Sequence[bool], d: int) -> int:
    """pairinf(d) = # di meta-input ``t`` per cui MBPSP[s] NON e' costante sui 4 input
    ``{t, t^e0, t^ed, t^(e0^ed)}`` (il 4-cubo generato dalle coordinate 0 e d).

    L'influenza di singola coordinata e' inutile: la meta-funzione e' invariante per
    traslazioni del cubo degli input (rietichettare x -> x+a = negare variabili) e le
    traslazioni sono gia' transitive sulle coordinate, quindi ogni coordinata ha la
    stessa influenza.  L'asimmetria appare solo sulle COPPIE.  Per traslazione la
    coordinata base e' fissata a 0 senza perdita: pairinf dipende solo dal vettore
    differenza ``d = x XOR x'``."""
    e0 = 1
    ed = 1 << d
    cnt = 0
    for t in range(len(meta)):
        a = meta[t]
        if not (a == meta[t ^ e0] == meta[t ^ ed] == meta[t ^ e0 ^ ed]):
            cnt += 1
    return cnt


@dataclass
class WeightClass:
    weight: int                       # peso di Hamming del vettore differenza d
    pairinf: List[Tuple[int, int]]    # [(d, pairinf(d)), ...] per i d di questo peso
    lo: int                           # min pairinf nella classe
    hi: int                           # max pairinf nella classe
    spread: int                       # hi - lo: l'INVARIANTE diagnostico


def weight_class_spread(meta: Sequence[bool], N: int) -> List[WeightClass]:
    """Per ogni peso di Hamming ``w`` di ``d in {1,...,N-1}``, raccoglie ``pairinf(d)``
    e ne misura lo SPREAD = max - min sulla classe.

    spread = 0 in ogni classe  <=>  pairinf dipende solo dal peso  <=>  meta-funzione
    PERMUTAZIONE-INVARIANTE (MCSP, ogni n).  spread > 0 in qualche classe  <=>
    pairinf dipende dal SUPPORTO di d (quali variabili, dunque la loro posizione
    nell'ordine)  <=>  asimmetria d'ordine sopravvissuta nella meta-funzione (MBPSP,
    a n=4)."""
    byw: Dict[int, List[Tuple[int, int]]] = defaultdict(list)
    for d in range(1, N):
        byw[bin(d).count("1")].append((d, pair_influence(meta, d)))
    out: List[WeightClass] = []
    for w in sorted(byw):
        lst = byw[w]
        vals = [v for _, v in lst]
        out.append(WeightClass(weight=w, pairinf=lst, lo=min(vals), hi=max(vals),
                               spread=max(vals) - min(vals)))
    return out


@dataclass
class AsymmetryRow:
    n: int
    N: int
    s: int
    H: int
    spreads: List[int]                # spread per peso w = 1, 2, ..., n
    order_survives: bool              # True se qualche spread > 0


def order_asymmetry(ns: Sequence[int], theta: float = 0.5) -> List[AsymmetryRow]:
    """La leva attraverso i livelli: per ogni n calcola MBPSP[s] (policy frazione
    fissa) e lo spread per classe di peso.  MISURATO: spread = 0 a n=2,3 (l'ordine
    e' silente, come la funzione testimone (x0 x1)|(x2 x3) richiede n=4) e spread > 0
    a n=4 (l'ordine sopravvive).  La leva LOCALIZZA l'accensione, non misura ancora un
    invariante di livello dell'asimmetria (n=5 = 2^32 truth-table, infattibile)."""
    rows: List[AsymmetryRow] = []
    for n in ns:
        N = 1 << n
        costs = obdd_costs(n)
        s = fixed_fraction_threshold(costs, theta)
        meta = meta_truth_table_obdd(costs, s)
        H = hard_count(meta)
        wcs = weight_class_spread(meta, N)
        spreads = [wc.spread for wc in wcs]
        rows.append(AsymmetryRow(n=n, N=N, s=s, H=H, spreads=spreads,
                                 order_survives=any(sp > 0 for sp in spreads)))
    return rows


# ── CICLO 4: l'asimmetria d'ordine RAGGIUNGE il muro FEDELE di Module 21 ───
#
# Il ciclo 3 mostra che l'OGGETTO MBPSP[s] e' non-permutazione-invariante via una
# misura d'influenza custom (pair_influence).  Il ciclo 4 chiede se l'ordine arriva
# fino al MURO che il programma cura davvero: l'ostruzione di certificazione di
# Module 21 (``locality.certified_k_local``), HARD certificabili leggendo solo le
# coordinate di un insieme S.  Si misura al livello j=2 (si RILASCIA una coppia di
# coordinate, k = N-2 lette) perche' a j=1 il gruppo di traslazione e' transitivo
# sulle singole coordinate => certified(N-1) e' isotropico per costruzione (sia MCSP
# sia MBPSP).  Per traslazione (negazione di variabile = permutazione delle posizioni
# x -> x^v, simmetria di MBPSP) ``certified_drop_pair(a,b) = certified_drop_pair(0,
# a^b)``, quindi il muro dipende solo dal vettore differenza ``d = a^b``.
#
# ESITO MISURATO (esatto; valori congelati in tests/test_order_locality.py). Lo SPREAD
# di certified_drop(d) entro una classe di ugual peso:
#
#     n   N    s    H        spread (w=1,2,3,4)         verdetto
#     3   8    4    224      0, 0, 0                    isotropico (ordine silente)
#     4  16    6    64282    144, 144, 16, 0            ANISOTROPICO (ordine al muro)
#     --- controllo MCSP (formula): n=4 s=8 H=25954 -> 0,0,0,0 (isotropico) ---
#
# Il muro VEDE l'ordine a n=4 (massimizzazione NON vacua: drop di ugual peso
# certificano numeri DIVERSI di istanze dure), mentre il controllo MCSP e' piatto in
# ogni classe (esattamente la trappola simmetrica che chiuse Module 21).  Robusto su
# tutta la banda non-degenere s in [5,10]; isotropico solo a s<=4 dove HARD satura
# (H~65534, meta quasi-costante).  CONFINE D'ONESTA': l'anisotropia e' REALE ma esile
# (~0.23% del valore base a n=4, w=1, piu' debole del 4.5% della pair-influence) e
# appare solo a n=4 (n=5 = 2^32, infattibile); il muro RAGGIUNGE l'ordine al livello
# piu' profondo misurabile, ma un invariante di livello resta fuori portata.  Nessun
# claim su P vs NP.

def certified_drop_pair(meta: Sequence[bool], a: int, b: int) -> int:
    """Il muro FEDELE di Module 21 (``locality.certified_k_local``) quando si
    RILASCIANO le coordinate {a,b} (si leggono le altre N-2): # di istanze dure che
    un argomento (N-2)-locale certifica con CERTEZZA.

    Ogni fibra sulle N-2 coordinate lette ha esattamente 4 elementi (le 4 combinazioni
    dei bit a,b); e' pura-dura sse tutti e 4 sono duri, e allora contribuisce 4 istanze
    dure.  Quindi ``certified_drop_pair = 4 * #{base (bit a,b = 0) : tutti e 4 di
    {base, base^ea, base^eb, base^ea^eb} duri}``.  Il massimo su tutte le coppie {a,b}
    eguaglia ``locality.certified_k_local(meta, N, N-2)`` (verificato in test)."""
    ea = 1 << a
    eb = 1 << b
    cnt = 0
    for base in range(len(meta)):
        if base & ea or base & eb:
            continue
        if meta[base] and meta[base ^ ea] and meta[base ^ eb] and meta[base ^ ea ^ eb]:
            cnt += 1
    return 4 * cnt


@dataclass
class DropClass:
    weight: int                        # peso di Hamming del vettore differenza d
    certified: List[Tuple[int, int]]   # [(d, certified_drop(0,d)), ...] per i d di peso w
    lo: int
    hi: int
    spread: int                        # hi - lo: anisotropia del MURO entro la classe


def certified_drop_spread(meta: Sequence[bool], N: int) -> List[DropClass]:
    """Per ogni peso ``w`` di ``d in {1,...,N-1}``, ``certified_drop_pair(0,d)`` (muro
    di Module 21 rilasciando la coppia {0,d}) e il suo SPREAD nella classe.

    spread = 0 in ogni classe  <=>  il muro dipende solo dal peso  <=>  ISOTROPICO
    (MCSP, ogni n; MBPSP a n<=3).  spread > 0  <=>  il muro dipende dal SUPPORTO di d
    <=>  l'ordine RAGGIUNGE il muro fedele (MBPSP a n=4)."""
    byw: Dict[int, List[Tuple[int, int]]] = defaultdict(list)
    for d in range(1, N):
        byw[bin(d).count("1")].append((d, certified_drop_pair(meta, 0, d)))
    out: List[DropClass] = []
    for w in sorted(byw):
        lst = byw[w]
        vals = [v for _, v in lst]
        out.append(DropClass(weight=w, certified=lst, lo=min(vals), hi=max(vals),
                             spread=max(vals) - min(vals)))
    return out


@dataclass
class WallAnisotropyRow:
    n: int
    N: int
    s: int
    H: int
    spreads: List[int]                # spread del muro per peso w = 1, 2, ..., n
    wall_sees_order: bool             # True se qualche spread > 0


def wall_anisotropy(ns: Sequence[int], theta: float = 0.5) -> List[WallAnisotropyRow]:
    """La leva del ciclo 4: per ogni n, l'anisotropia del MURO fedele di Module 21 su
    MBPSP[s] (policy frazione fissa).  MISURATO: isotropico a n<=3, anisotropico a n=4
    (spread 144,144,16,0).  Il muro raggiunge l'ordine al livello piu' profondo
    misurabile; nessun invariante di livello (n=5 infattibile)."""
    rows: List[WallAnisotropyRow] = []
    for n in ns:
        N = 1 << n
        costs = obdd_costs(n)
        s = fixed_fraction_threshold(costs, theta)
        meta = meta_truth_table_obdd(costs, s)
        H = hard_count(meta)
        dcs = certified_drop_spread(meta, N)
        spreads = [dc.spread for dc in dcs]
        rows.append(WallAnisotropyRow(n=n, N=N, s=s, H=H, spreads=spreads,
                                      wall_sees_order=any(sp > 0 for sp in spreads)))
    return rows


def reopening_note() -> str:
    """Lega i numeri tiny al criterio del programma (stringa, nessun claim asintotico)."""
    return (
        "MBPSP[s] (dimensione OBDD a ordine FISSO, HARD = nessun OBDD piccolo) e' "
        "l'oggetto meta-livello NON permutazione-invariante richiesto per riaprire la "
        "Magnification Frontier: a n=4 la sua pair-influence distingue differenze di "
        "ugual peso per il loro supporto nell'ordine (spread > 0), mentre il controllo "
        "MCSP a formula lava tutto via (spread = 0).  L'ordine e' il taglio orizzontale "
        "che a MCSP mancava.  L'amplificazione asintotica (lower bound debole su "
        "gap-MCSP/MKtP/BP => separazione) resta CITATA (Oliveira-Pich 2019; "
        "Chen-Jin-Williams 2019/2020; barriera di localita' Chen-Hirahara-Ren-"
        "Santhanam-Vyas); a n finito nessuna separazione, nessun claim su P vs NP."
    )
