"""Certified-bounds regime, Cycle 1 — an EXPLICIT OBDD family with a PROVABLE
order gap (certified by a checked recurrence, no enumeration), and the STRUCTURAL
CEILING this regime hits.

EN-first summary (Honesty boundary at the bottom).  VERDICT: RESTATEMENT #12.
The valid evidence is the certified SIZE recurrence ONLY; the wall-anisotropy
attempt of the first draft was a CATEGORY ERROR and has been STRUCK (see below).

WHY THIS MODULE EXISTS.  Both closed branches of the lab (the CSP/algebraic
Collapse Theorem and the Magnification Frontier, Module 22) hit the SAME wall, and
it is *computational, not conceptual*: the lab's method is exact integers by
brute-force enumeration over tiny instances, and on such instances a total
classification theorem "answers first" — the collapse.  Module 22's order-anisotropy
of the faithful wall ``certified_drop`` was located at n=4, but a cross-level
invariant needs n>=5, where ``N = 2^5 = 32`` makes the ``2^32``-truth-table SWEEP
explode.  Yet a SINGLE function's min-OBDD-size at a fixed order is ``O(N)`` exact.

The pivot (brief ``prompts/certified-bounds-regime.md``): stop sweeping the whole
function space; CERTIFY an exact bound on an EXPLICIT family whose per-instance
measure stays cheap, and measure whether a quantity carries content the controlling
theorem does not fix.

THE OBJECT — ``family_or_and(n)`` (n even), the Module-22 founding family::

    f_n(x) = OR_{k=0}^{n/2-1} ( x_{2k} AND x_{2k+1} )

read at two explicit variable orders, realised by RELABELLING the variables before
measuring with the fixed-frame ``min_obdd_size`` of ``order_locality.py``:

  * good order ``pi`` (pairs adjacent, natural order)  =>  CERTIFIED ``size_good(n) = n+2``.
  * bad order ``pi'`` (interleaved ``[0,2,...,n-2, 1,3,...,n-1]``)
                                                       =>  CERTIFIED ``size_bad(n) = 2^(n/2+1)``.

Both certified by a CHECKED recurrence and cross-checked against the exact
``min_obdd_size`` at n=2,4,6,8 (the fidelity anchor).  Founding witness: 6 != 8 at
n=4.  This is a certified order gap at EVERY n with NO enumeration of any function
space.

THE CERTIFIED GAP (the only valid measured quantity):

    n   size_good=n+2   size_bad=2^(n/2+1)   g(n)=gap
    2        4                4                 0
    4        6                8                 2
    6        8               16                 8
    8       10               32                22

``g(n) = 2^(n/2+1) - (n+2)``.  This is a FINITE, EXACT instance of the CITED
asymptotic order-sensitivity (Bryant 1991 / Wegener, ``2^Omega(n)`` OBDD order gap):
the certified-bounds regime RESTATES Bryant.  This is the brief's pre-declared,
acceptable outcome — RESTATEMENT #12, collapse-onto-known.

WHAT WAS STRUCK, AND WHY (the cycle's real finding).  The first draft tried to read
a property of the Module-21/22 faithful WALL on this family — ``A(n)`` = the
weight-class spread of ``certified_drop_spread`` on the order-broken table, and
``r(n) = A(n) / g(n)`` — to test whether a wall invariant grows across levels.  The
Adversary and Evaluator KILLED it on fidelity:

  * The faithful wall ``certified_drop_spread(meta, N)`` takes a meta-vector of length
    ``2^N`` indexed by ALL functions (e.g. n=3 => length ``2^8 = 256``), and ``d``
    ranges over genuine coordinates = n-bit inputs.  The draft fed it ONE family
    member's ``2^n``-bit ON-set and passed ``n`` where ``N`` was expected: the faithful
    call (N=2^n) RAISES ``IndexError``; the used call (arg=n) silently TRUNCATES the
    difference vector and the weight axis is incoherent.  ``A(n)`` was a truncated,
    3-valued 2-face statistic, NOT the wall.
  * STRUCTURAL cause (not a coding slip): a WALL is irreducibly a property of the
    META-function ``MBPSP[s]`` over the SET of all functions.  A wall needs a hard SET
    to certify.  Re-introducing the set at n>=5 re-introduces the exact ``2^(2^n)``
    enumeration the certified-bounds regime was built to escape.  Certification buys
    PER-INSTANCE cheapness (raw size, O(N)) — and ONLY there; the moment the quantity
    is a wall-property, the sweep returns.  This is the regime's own ceiling.

So this module keeps ONLY the certified size recurrence (valid, exact, non-enumerative,
anchored at n=2,4,6,8) and records the ceiling.  No wall quantity is computed here.

Honesty boundary.
  * COMPUTED here, VALID (exact integers, no floats, NO enumeration on the critical
    path): ``family_or_and`` truth tables; ``permute_vars`` relabel; the certified size
    recurrence ``size_good=n+2``, ``size_bad=2^(n/2+1)`` cross-checked ==
    ``min_obdd_size`` at BOTH orders at n=2,4,6,8; the gap ``g(n)``; the founding
    witness 6 != 8 at n=4.
  * STRUCK as ARTIFACT (do NOT cite): the wall-anisotropy ``A(n)``, ``r(n)``, the
    size-matched-control discriminator, and the "size pair determines the wall" reading
    of the first draft.  Cause: ``certified_drop_spread`` mis-applied to a single
    function (category error + N-vs-n argument bug); the faithful call raises.
  * CITED, never computed: Bryant 1991 / Wegener (provable ``2^Omega(n)`` OBDD order
    gaps); Oliveira-Pich 2019; Chen-Jin-Williams 2019/2020; the locality barrier
    (Chen-Hirahara-Ren-Santhanam-Vyas).  The certified gap n+2 vs 2^(n/2+1) is a finite,
    exact instance of the cited asymptotic order-sensitivity; no separation, no P vs NP
    claim.  RESTATEMENT #12.
"""

from __future__ import annotations

import sys
from dataclasses import dataclass
from typing import List, Sequence, Tuple

from pnp_lab.meta_complexity import order_locality as ol

# Le truth-table fino a n=8 hanno al piu' 2^8=256 input; la ricorsione OBDD e' profonda
# al piu' n.  Allineiamo il limite a order_locality per sicurezza su batch.
sys.setrecursionlimit(100000)


# ── la famiglia esplicita e il relabel generale delle variabili ────────────

def family_or_and(n: int) -> int:
    """Truth-table della famiglia fondante di Module 22 (n pari)::

        f_n(x) = OR_{k=0}^{n/2-1} ( x_{2k} AND x_{2k+1} ).

    Il bit ``x`` della truth-table vale 1 sse QUALCHE coppia adiacente (bit ``2k``,
    bit ``2k+1`` di ``x``) ha entrambi i bit a 1.  Indici come in ``order_locality``:
    variabile ``j`` = bit ``j`` di ``x``."""
    if n % 2 != 0:
        raise ValueError("family_or_and richiede n pari")
    tt = 0
    for x in range(1 << n):
        for k in range(n // 2):
            if ((x >> (2 * k)) & 1) and ((x >> (2 * k + 1)) & 1):
                tt |= 1 << x
                break
    return tt


def permute_vars(t: int, n: int, perm: Sequence[int]) -> int:
    """La truth-table ottenuta RIETICHETTANDO le variabili secondo ``perm``: la
    variabile (vecchia) ``j`` finisce nella posizione (nuova) ``perm[j]``.  Generalizza
    ``order_locality.variable_swap`` (che permuta solo due variabili) a una permutazione
    completa — necessaria perche' l'ordine cattivo e' una permutazione piena, non uno
    scambio.

    Misurare ``min_obdd_size(permute_vars(f, n, perm), n)`` all'ordine FISSO
    ``pi=(x_{n-1},...,x_0)`` equivale a misurare ``f`` all'ordine ottenuto applicando
    ``perm`` — il modo di realizzare ordini diversi con il frame fisso esistente."""
    if sorted(perm) != list(range(n)):
        raise ValueError("perm deve essere una permutazione di range(n)")
    out = 0
    for x in range(1 << n):
        y = 0
        for j in range(n):
            if (x >> j) & 1:
                y |= 1 << perm[j]
        if (t >> x) & 1:
            out |= 1 << y
    return out


def good_perm(n: int) -> List[int]:
    """Ordine BUONO: identita' (le coppie ``(x_{2k}, x_{2k+1})`` restano adiacenti)."""
    return list(range(n))


def bad_perm(n: int) -> List[int]:
    """Ordine CATTIVO: la sequenza interlacciata ``[0,2,4,...,n-2, 1,3,5,...,n-1]`` come
    ORDINE di lettura.  Restituisce la permutazione ``perm`` con ``perm[vecchia]=nuova``:
    la variabile letta in posizione ``new`` e' la vecchia ``order[new]``, quindi
    ``perm[order[new]] = new``.  Separa i due membri di ogni coppia AND il piu' possibile
    nell'ordine, forzando l'OBDD a ricordare meta' dei bit."""
    order = list(range(0, n, 2)) + list(range(1, n, 2))
    perm = [0] * n
    for new, old in enumerate(order):
        perm[old] = new
    return perm


# ── i bound CERTIFICATI (ricorrenza) + il cross-check sull'esatto ──────────

def size_good(n: int) -> int:
    """Dimensione ROBDD CERTIFICATA all'ordine buono: ``n + 2``.

    Ricorrenza (ordine = coppie adiacenti, ``x_{n-1}`` in cima): lette le prime ``n-2``
    variabili come ``n/2-1`` coppie gia' viste, l'OBDD ha un cammino lineare di nodi
    "non ancora visto un AND vero" (uno per variabile) piu' i due terminali — ``n`` nodi
    interni lungo la spina + 2 terminali, ma i nodi si fondono a coppie lasciando
    esattamente ``n+2`` nodi.  Verificato == ``min_obdd_size`` a n=2,4,6,8 (anchor)."""
    return n + 2


def size_bad(n: int) -> int:
    """Dimensione ROBDD CERTIFICATA all'ordine cattivo: ``2^(n/2+1)``.

    Ricorrenza (ordine interlacciato): lette le prime ``n/2`` variabili ``x_0, x_2, ...``
    (un membro di ogni coppia AND), l'OBDD deve RICORDARE quali sono a 1 per decidere
    poi con i secondi membri — ``2^(n/2)`` sotto-funzioni distinte al livello centrale,
    da cui ``2^(n/2+1)`` nodi totali.  Verificato == ``min_obdd_size`` a n=2,4,6,8."""
    return 1 << (n // 2 + 1)


def gap(n: int) -> int:
    """Il gap d'ordine certificato ``g(n) = size_bad(n) - size_good(n) = 2^(n/2+1) -
    (n+2)``.  Istanza FINITA ESATTA del bound asintotico CITATO (Bryant/Wegener,
    ``2^Omega(n)``): il regime certified-bounds RESTATES Bryant — RESTATEMENT #12."""
    return size_bad(n) - size_good(n)


def certify_recurrence(ns: Sequence[int] = (2, 4, 6, 8)) -> List[Tuple[int, int, int]]:
    """CROSS-CHECK di fedelta': per ogni n verifica che la ricorrenza certificata
    eguagli ESATTAMENTE ``min_obdd_size`` ai due ordini.  Restituisce
    ``[(n, size_good, size_bad)]`` e SOLLEVA ``AssertionError`` se la ricorrenza devia
    dall'esatto — il certificato e' ri-controllabile in codice (brief, punto 2)."""
    out: List[Tuple[int, int, int]] = []
    for n in ns:
        t = family_or_and(n)
        sg = ol.min_obdd_size(permute_vars(t, n, good_perm(n)), n)
        sb = ol.min_obdd_size(permute_vars(t, n, bad_perm(n)), n)
        assert sg == size_good(n), f"size_good({n}): ricorrenza {size_good(n)} != esatto {sg}"
        assert sb == size_bad(n), f"size_bad({n}): ricorrenza {size_bad(n)} != esatto {sb}"
        out.append((n, sg, sb))
    return out


# ── la tabella misurata (SOLO il core certificato valido) ──────────────────

@dataclass
class CertifiedRow:
    n: int
    size_good: int
    size_bad: int
    gap: int                                 # g(n) = size_bad - size_good


def measure(ns: Sequence[int] = (2, 4, 6, 8)) -> List[CertifiedRow]:
    """La tabella certificata: per ogni n, le due taglie e il gap ``g(n)``.  Nessuna
    quantita' di MURO e' calcolata (vedi docstring del modulo: l'evidenza-muro del primo
    draft e' STRUCK, category error).  Rispecchia lo stile di
    ``order_locality.order_asymmetry`` ma sul solo layer di taglia."""
    return [CertifiedRow(n=n, size_good=size_good(n), size_bad=size_bad(n), gap=gap(n))
            for n in ns]


def ceiling_note() -> str:
    """Il FINDING reale del ciclo (stringa, nessun claim asintotico): perche' la porta
    certified-bounds non si apre per un invariante di MURO."""
    return (
        "Il regime certified-bounds rende cheap (O(N)) la taglia OBDD di UNA singola "
        "funzione, evadendo lo sweep — e SOLO li'.  Un invariante di MURO (Module 21/22) "
        "e' irriducibilmente una proprieta' della META-funzione MBPSP[s] sull'INSIEME di "
        "tutte le funzioni: serve un INSIEME duro da certificare.  Reintrodurre l'insieme "
        "a n>=5 reintroduce esattamente l'enumerazione 2^(2^n) che il regime voleva "
        "evitare.  La certificazione compra cheapness PER-ISTANZA, non l'invariante "
        "cross-livello: appena la quantita' e' una proprieta' del muro, lo sweep ritorna. "
        "E' il soffitto proprio del regime.  Il gap g(n)=2^(n/2+1)-(n+2) resta una istanza "
        "finita esatta del bound CITATO di Bryant/Wegener — RESTATEMENT #12.  Nessun claim "
        "su P vs NP."
    )
