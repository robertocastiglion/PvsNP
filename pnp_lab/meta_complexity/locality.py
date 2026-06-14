"""Locality barrier — the magnification wall, made measurable on tiny MCSP[s].

EN-first summary (Honesty boundary at the bottom).

Hardness magnification (Oliveira-Pich 2019; Chen-Jin-Williams 2019/2020;
McKay-Murray-Williams 2019) says: barely super-linear lower bounds for gap-MCSP /
MKtP would *amplify* into NP not in P/poly. They remain unproven because the known
lower-bound techniques appear to be **local** (they inspect few bits / are small
fan-in / streaming / small space), and a counting obstruction prevents any local
argument from crossing the magnification threshold (the *locality barrier*: Chen-
Hirahara-Ren-Santhanam-Vyas; Chen-Jin-Williams "sharp threshold"). This is to the
magnification wall what Module 1 is to Natural Proofs: we make the wall an exact
integer.

This module does NOT prove anything new. It makes one finite slice of the wall
TANGIBLE and EXACT, on the meta-function MCSP[s] itself.

The object.  Fix n and the threshold s.  The meta-function is

    MCSP[s] : {0,1}^N -> {0,1},   N = 2^n,

whose input is the *whole truth table* of an n-bit function, read as N coordinates.
We use the EXACT formula complexity of Module 6 (``min_formula_sizes``):

    meta(t) := ( cost[t] > s )        # convention: HARD = "no small formula"

i.e. coordinate t (an integer in [0, 2^N)) is HARD iff the n-bit function with that
truth table needs a formula of size > s.  ``H`` denotes #{hard}.

Locality, exactly.
  * ``relevant_coordinates`` : bit i is RELEVANT if some input pair differing only
    in coordinate i flips MCSP[s].  ``loc`` = number of relevant coordinates: if
    loc < N the meta-function is a genuine (loc)-junta and a local argument reading
    only those bits suffices; if loc = N no coordinate is ignorable.
  * ``best_k_local`` : the best k-local *classifier*.  A k-local argument may read
    only some fixed set S of k coordinates; on each fibre of S (the inputs sharing
    the same S-bits) it must answer one value.  Two readings of "best":
      - A(k)        = max over |S|=k of  sum_fibres max(#hard, #easy)   -- the best
                      junta-classifier; counts ALL inputs it labels correctly.
      - certified(k)= max over |S|=k of  sum over PURE-hard fibres of #hard  -- how
                      many hard instances a k-local argument can certify *with
                      certainty* (the fibre contains no easy instance, so reading
                      those k bits proves hardness).
    ``certified`` is the faithful obstruction: a k-local argument can only certify a
    hard instance when its fibre is pure-hard.  H - certified(k) is the count of
    hard instances NO k-local argument certifies.

The wall.  ``obstruction`` tabulates (k, A(k), certified(k), H, H-A(k),
H-certified(k)).  The honest signal is ``H - certified(k)``: it stays at H for all
small k and only collapses to 0 at the full junta k = N.  That gap is the counting
obstruction in miniature.

Honesty boundary.
  * COMPUTED here (exact integers, no floats): MCSP[s] as an N-junta, its relevant
    coordinates, A(k), certified(k), and the obstruction table, for one (n, s).
  * CITED, never computed: the asymptotic magnification theorems and the locality
    barrier proper.  At finite n the "threshold" is a single number, not a regime;
    the amplification (small LB -> big separation) is asymptotic and ESCAPES tiny
    size.  We exhibit the *mechanism* (local arguments cannot certify hard
    instances below the full junta), not the amplification.  No separation, no
    P vs NP claim.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations
from typing import Dict, List, Sequence, Set, Tuple

from pnp_lab.circuits import ComplexityTable


# ── la meta-funzione MCSP[s] ──────────────────────────────────────────────

def meta_truth_table(ct: ComplexityTable, s: int) -> List[bool]:
    """MCSP[s] come vettore indicizzato dalle truth-table di n-bit.

    L'input di MCSP è la truth-table di una funzione n-bit: una stringa di
    N = 2^n bit.  Quindi gli INPUT della meta-funzione sono 2^N = 2^(2^n) (una
    per funzione), NON 2^n.  L'indice t in [0, 2^N) È la truth-table letta come
    input N-locale; il valore è True se la funzione con quella truth-table è DURA.

    Convenzione: HARD = (dimensione di formula minima > s).
    """
    N = 1 << ct.n                      # N = 2^n = lunghezza della truth-table (input di MCSP)
    num_functions = 1 << N             # 2^N = 2^(2^n) = numero di meta-input
    return [ct.cost[t] > s for t in range(num_functions)]


def hard_count(meta: Sequence[bool]) -> int:
    """H = numero di istanze dure (#{cost > s})."""
    return sum(1 for v in meta if v)


# ── località: coordinate rilevanti ────────────────────────────────────────

def relevant_coordinates(meta: Sequence[bool], N: int) -> Set[int]:
    """Insieme dei bit RILEVANTI della meta-funzione.

    Il bit i è rilevante se esiste una coppia di input che differiscono SOLO nel
    bit i e che hanno output MCSP[s] diverso.  Se i non e' rilevante, nessun
    argomento ha bisogno di leggerlo.
    """
    rel: Set[int] = set()
    for i in range(N):
        bit = 1 << i
        for t in range(len(meta)):
            if t & bit:
                continue
            if meta[t] != meta[t | bit]:
                rel.add(i)
                break
    return rel


def loc(meta: Sequence[bool], N: int) -> int:
    """loc = |coordinate rilevanti|: il piu' piccolo junta che PUO' contenere
    MCSP[s].  Se loc = N la funzione non degenera (vero N-junta)."""
    return len(relevant_coordinates(meta, N))


# ── A(k): il miglior classificatore k-locale ──────────────────────────────

def _fibre_counts(meta: Sequence[bool], S: Tuple[int, ...]) -> Dict[Tuple[int, ...], Tuple[int, int]]:
    """Per il sottoinsieme di coordinate S, raggruppa gli input nelle fibre (stessi
    bit su S) e conta (#hard, #easy) in ciascuna fibra."""
    fibres: Dict[Tuple[int, ...], Tuple[int, int]] = {}
    for t in range(len(meta)):
        key = tuple((t >> i) & 1 for i in S)
        h, e = fibres.get(key, (0, 0))
        if meta[t]:
            h += 1
        else:
            e += 1
        fibres[key] = (h, e)
    return fibres


def best_k_local(meta: Sequence[bool], N: int, k: int) -> int:
    """A(k): il miglior classificatore k-locale.

    A(k) = max su |S| = k di  sum_fibre max(#hard, #easy).  Su ogni fibra il
    classificatore deve dare UN solo valore (rispetta le fibre di S); la scelta
    ottima e' la maggioranza.  A(N) = numero totale di input (junta pieno =
    classificazione perfetta); A(0) = max(H, totale - H) (classificatore costante).
    """
    best = 0
    for S in combinations(range(N), k):
        correct = sum(max(h, e) for h, e in _fibre_counts(meta, S).values())
        if correct > best:
            best = correct
    return best


def certified_k_local(meta: Sequence[bool], N: int, k: int) -> int:
    """certified(k): quante istanze DURE un argomento k-locale puo' certificare con
    CERTEZZA.

    Un argomento che legge solo le k coordinate di S certifica come dura un'istanza
    solo se la sua fibra e' PURA-dura (nessun easy): allora i k bit dimostrano la
    durezza.  certified(k) = max su |S| = k di  sum_{fibre pure-hard} #hard.

    E' l'ostruzione FEDELE: H - certified(k) = istanze dure che nessun argomento
    k-locale certifica.  Resta = H per k piccolo e crolla a 0 solo a k = N.
    """
    best = 0
    for S in combinations(range(N), k):
        cert = sum(h for h, e in _fibre_counts(meta, S).values() if e == 0 and h > 0)
        if cert > best:
            best = cert
    return best


# ── la tabella-ostruzione: il muro come interi ────────────────────────────

@dataclass
class ObstructionRow:
    k: int
    A: int            # miglior classificatore k-locale (tutti gli input)
    certified: int    # istanze dure certificate con certezza k-locale
    H: int            # numero totale di istanze dure
    gap_A: int        # H - A(k)
    gap_cert: int     # H - certified(k)  (l'ostruzione fedele)


def obstruction(ct: ComplexityTable, s: int, ks: Sequence[int] | None = None) -> List[ObstructionRow]:
    """Tabella (k, A(k), certified(k), H, H-A(k), H-certified(k)) per k in ks.

    Default: k = 0..N.  Tutti gli interi sono esatti (enumerazione completa degli
    S; a N = 8 sono sum_k C(8,k) = 256 sottoinsiemi totali)."""
    N = 1 << ct.n
    meta = meta_truth_table(ct, s)
    H = hard_count(meta)
    if ks is None:
        ks = range(N + 1)
    rows: List[ObstructionRow] = []
    for k in ks:
        A = best_k_local(meta, N, k)
        cert = certified_k_local(meta, N, k)
        rows.append(ObstructionRow(k=k, A=A, certified=cert, H=H, gap_A=H - A, gap_cert=H - cert))
    return rows


# ── la LEVA: il muro attraverso i livelli n (il taglio-torta) ─────────────
#
# Il principio: non misurare un muro statico a un solo n, ma l'OPERATORE di
# amplificazione attraverso i livelli n=2->3->4.  Per certificare la funzione
# PIU' DURA (banda alta, s=maxcost-1) servono k*(n) bit del truth-table;
# rho(n)=k*/N e' la frazione che un argomento deve leggere.
#
# RISULTATO MISURATO (il taglio orizzontale, falsificazione esatta).  L'ipotesi
# iniziale "rho=1 a ogni livello, k* raddoppia 4->8->16" e' FALSA.  Misura:
#
#     n   N    H     k*   rho      cert tail (cert(N-j)/H, j=0..3)
#     2   4    2      4   1.000    1.00, 0,    0,    0
#     3   8    2      8   1.000    1.00, 0,    0,    0
#     4  16  114     14   0.875    1.00, 0.21, 0.07, 0
#
# rho NON resta 1: crolla a 0.875 a n=4.  La diagnosi (esatta): rho=1 a n=2,3 e'
# un ARTEFATTO della banda-dura degenere H=2 (solo la parita' e la sua negazione
# sono massimamente dure; con 2 sole istanze, massimamente sparse, nessuna fibra
# di N-1 bit e' pura-dura, quindi cert(N-1)=0 e rho=1 banalmente).  Appena la
# popolazione dura e' reale (H=114 a n=4) compaiono fibre pura-dura sotto il junta
# pieno e rho<1.  Quel che la leva misura non e' l'operatore di magnification ma
# la TAGLIA-e-dispersione della banda piu' dura (H = 2,2,114: non monotona).
# Negativo ed esatto, nessun claim su P vs NP.  (Il MECCANISMO di localita'
# -- cert(k) basso finche' k<N -- regge; e' la storia "rho=1 staircase" a cadere.)

def hardest_band_threshold(ct: ComplexityTable) -> int:
    """Policy di soglia FEDELE alla magnification: isola la banda piu' dura,
    s = (costo massimo) - 1, cioe' le funzioni di complessita' massima (gli
    'explicit-hard' di cui parlano i lower bound)."""
    return max(ct.cost.values()) - 1


def k_star(meta: Sequence[bool], N: int) -> int | None:
    """Minimo k per cui un argomento k-locale certifica ALMENO un'istanza dura
    (``certified(k) > 0``).  None se nemmeno il junta pieno certifica (H=0).

    ``certified(k)`` e' MONOTONA non-decrescente in k (aggiungere una coordinata
    a S puo' solo raffinare le fibre -> una fibra pura-dura resta pura-dura),
    quindi k* e' ben definito e si DISCENDE dall'alto: il primo k (da N-1 in giu')
    con ``certified(k) = 0`` implica ``certified = 0`` per ogni k minore, dunque
    k* = k+1.  Nel regime banda-dura k* e' vicino a N, quindi si toccano solo i
    sottoinsiemi grandi (a N=16: C(16,15), C(16,14), ... — niente k centrali
    costosi come C(16,8)=12870)."""
    if hard_count(meta) == 0:
        return None
    for k in range(N - 1, -1, -1):
        if certified_k_local(meta, N, k) == 0:
            return k + 1          # monotonia: tutti i k minori sono pure 0
    return 0


@dataclass
class LeverageRow:
    n: int
    N: int                 # 2^n = lunghezza del truth-table (input di MCSP)
    s: int                 # soglia (policy banda dura)
    H: int                 # # istanze dure
    loc: int               # coordinate rilevanti (=N => junta non degenere)
    k_star: int | None     # min bit da leggere per certificare la piu' dura
    rho: float | None      # k*/N (frazione del truth-table da leggere)


def leverage(cts: Sequence[ComplexityTable]) -> List[LeverageRow]:
    """La scala della leva: per ogni livello (ComplexityTable di un dato n) misura
    (N, s, H, loc, k*, rho) con la policy banda-dura.  MISURATO: rho NON resta 1
    (n=2,3 -> rho=1 ma e' artefatto della banda degenere H=2; n=4 -> H=114, k*=14,
    rho=0.875).  La leva traccia la taglia/dispersione della banda piu' dura, non
    un operatore di magnification.  Vedi il blocco-commento sopra."""
    rows: List[LeverageRow] = []
    for ct in cts:
        N = 1 << ct.n
        s = hardest_band_threshold(ct)
        meta = meta_truth_table(ct, s)
        H = hard_count(meta)
        loc_v = loc(meta, N)
        ks = k_star(meta, N)
        rows.append(LeverageRow(n=ct.n, N=N, s=s, H=H, loc=loc_v,
                                k_star=ks, rho=(ks / N if ks is not None else None)))
    return rows


def magnification_threshold_note() -> str:
    """Lega i numeri tiny al teorema citato (stringa, nessun claim asintotico)."""
    return (
        "I numeri tiny mostrano il MECCANISMO della barriera di localita': un "
        "argomento k-locale puo' certificare un'istanza dura solo quando la sua "
        "fibra e' pura-dura, percio' certified(k) resta 0/parziale finche' k < N e "
        "raggiunge H solo al junta pieno k = N.  La SOGLIA di amplificazione "
        "(lower bound n^{1+eps} per gap-MCSP => NP not in P/poly) e' un fenomeno "
        "ASINTOTICO: si CITA (Oliveira-Pich 2019; Chen-Jin-Williams 2019/2020; "
        "barriera di localita' Chen-Hirahara-Ren-Santhanam-Vyas).  A n finito la "
        "soglia e' un singolo intero, non un regime; nessuna separazione.  E il "
        "tentativo di leggere l'amplificazione come 'rho=1 a ogni livello' e' "
        "FALSIFICATO esattamente a n=4 (rho=0.875): la frazione rho=1 a n<=3 era "
        "solo l'artefatto della banda-dura degenere H=2."
    )
