"""Door-C (Entry 32): la LEVA cross-livello del lifting letta come crescita del
GAP DI INTEGRALITA' del covering ILP.

Stessa arena del Modulo 18 (lift  f ∘ g^k, matrice di comunicazione 2^k x 2^k),
NUOVA lente: invece di chiedere "il gap si apre?" (gadget_rule), si misura la
SEQUENZA del gap al crescere di k

    G_k = Cov(M_k) - LP(M_k) >= 0,      M_k = lift(f, g, k),

e si chiede se G_3 e' RICOSTRUIBILE da G_2 (e da G_1 / dal solo gadget) via una
delle tre leggi di composizione note (il "killer"):

  (a) MOLTIPLICATIVA (tensore/dualita' LP):   G_3 == (G_2)^2 ;
  (b) AFFINE/RICORSIVA a 2 termini:           G_3 == 2*G_2 - G_1 ;
  (c) POLY-DEL-GADGET:                        G_3 == p(k) con p chiusa nei SOLI
      invarianti del gadget g (Cov(g), LP(g)) -- cioe' G_k dipende solo da g e k,
      non dall'outer f.  Operativamente: per un dato gadget g, G_3 e' previsto
      come "2 volte il gap medio aperto a k=2 dallo stesso g" (la forma chiusa
      lineare in k consistente con G_1=0); se UNA legge fra (a)(b)(c) riproduce
      G_3 esatto, la coppia e' `killed`.

Una coppia (f, g) e' un CANDIDATO door-C NON falsificato sse G_2 e G_3 sono
entrambi esatti, la sequenza (G_1, G_2, G_3) ha >= 2 valori distinti, e NESSUNA
delle tre leggi ricostruisce G_3.

Aritmetica ESATTA (Fraction): Cov intero (set-cover esatto), LP razionale dal
simplesso di gap.py. Il muro di brute-force e' a k=4 (16x16); k=2 (4x4) e k=3
(8x8) sono enumerabili.  Le SOLE celle con gap a k=3 sono le matrici di
DISUGUAGLIANZA J - I_8 (gadget di permutazione XOR/EQ con outer OR/NAND): per
queste l'enumerazione generica dei rettangoli massimali e' costosa, quindi Cov e
LP usano la FORMA CHIUSA ESATTA per J - I_m, verificata contro il risolutore
generico per m <= 6 (vedi test).  NON dimostra P vs NP: misura un gap su istanze
minuscole.
"""

from __future__ import annotations

from fractions import Fraction
from itertools import combinations
from math import comb
from typing import Dict, List, Optional, Sequence, Tuple

from .gap import BoolMatrix, cover_number, frac_cover
from .compose import GADGETS_1BIT, base_function, lift
from .pattern_gap import is_J_minus_I_up_to_perm

# Outer di default (le funzioni nominali definite in base_function).
DEFAULT_OUTERS: Tuple[str, ...] = ("OR", "AND", "XOR", "MAJ", "NAND", "NOR")
DEFAULT_GADGETS: Tuple[str, ...] = tuple(GADGETS_1BIT.keys())


# --------------------------------------------------------------------------- #
#  Forma chiusa ESATTA per la matrice di disuguaglianza  J - I_m              #
# --------------------------------------------------------------------------- #
#  J - I_m = 1 ovunque tranne la diagonale.  I suoi 1-rettangoli MASSIMALI sono
#  esattamente  S x S^c  per S sottoinsieme proprio non vuoto di {0..m-1}
#  (R x C e' tutto-1  <=>  R ∩ C = ∅, e massimale  <=>  C = complemento di R).
#  Il rettangolo S x S^c copre la coppia ordinata (i, j), i != j, sse i ∈ S, j ∉ S.

def ji_cover_number(m: int) -> int:
    """Cov(J - I_m): minimo biclique cover del grafo "crown".

    Forma chiusa classica:  il minimo numero di rettangoli S x S^c che coprono
    tutte le coppie ordinate (i, j), i != j, e'

        Cov(J - I_m) = min { d : C(d, floor(d/2)) >= m }.

    Costruzione (upper bound): assegna a ogni elemento un codice DISTINTO
    A_i ⊆ {0..d-1} con |A_i| = floor(d/2) (possibile perche' C(d,floor(d/2)) >= m);
    il rettangolo t-esimo e' R_t = {i : t ∈ A_i}, C_t = {j : t ∉ A_j}.  Ogni coppia
    i != j ha A_i != A_j di pari taglia, quindi esiste t in (A_i meno A_j) che copre.
    Lower bound matching: risultato noto sui biclique cover delle crown graph.
    Verificato contro il risolutore generico per m <= 6 (test).
    """
    if m <= 1:
        return 0
    d = 1
    while comb(d, d // 2) < m:
        d += 1
    return d


def ji_frac_cover(m: int) -> Fraction:
    """LP(J - I_m): copertura frazionaria esatta.

    Tutte le coppie ordinate (i, j) sono equivalenti sotto il gruppo di simmetria
    S_m che agisce su J - I_m, quindi l'ottimo LP e' simmetrico: peso uniforme
    w_r su tutti i C(m, r) rettangoli S x S^c con |S| = r.  Una coppia fissata e'
    coperta da C(m-2, r-1) rettangoli di taglia r (scegli il resto di S fra gli
    altri m-2 elementi, con i dentro e j fuori).  La copertura frazionaria mette
    tutto il peso su un'unica taglia r* e vale

        LP(J - I_m) = min_{1 <= r <= m-1}  C(m, r) / C(m-2, r-1).

    Verificata contro frac_cover generico per m <= 7 (test): 2, 3, 3, 10/3, 10/3,
    7/2 per m = 2..7, e 7/2 per m = 8.
    """
    if m <= 1:
        return Fraction(0)
    best: Optional[Fraction] = None
    for r in range(1, m):
        val = Fraction(comb(m, r), comb(m - 2, r - 1))
        if best is None or val < best:
            best = val
    assert best is not None
    return best


def _cov_lp(M: BoolMatrix) -> Tuple[int, Fraction]:
    """(Cov, LP) ESATTI di M.

    Usa il risolutore generico (gap.py) ovunque; per le matrici di disuguaglianza
    J - I_m (le SOLE celle dense con gap a k=3, dove l'enumerazione generica dei
    rettangoli massimali esplode) usa la forma chiusa esatta, equivalente al
    risolutore generico ma O(m).
    """
    if is_J_minus_I_up_to_perm(M):
        m = len(M)
        return ji_cover_number(m), ji_frac_cover(m)
    return cover_number(M), frac_cover(M)


def gap_at(fname: str, gname: str, k: int) -> Fraction:
    """G_k = Cov(M_k) - LP(M_k) ESATTO per la cella (f, g) a livello k."""
    M = lift(base_function(fname, k), GADGETS_1BIT[gname], k)
    cov, lp = _cov_lp(M)
    return Fraction(cov) - lp


def gap_sequence(fname: str, gname: str, ks: Sequence[int] = (1, 2, 3)) -> Dict[int, Fraction]:
    """Sequenza {k: G_k} ESATTA per la cella (f, g)."""
    return {k: gap_at(fname, gname, k) for k in ks}


# --------------------------------------------------------------------------- #
#  Riga di sweep e tabella                                                     #
# --------------------------------------------------------------------------- #

# (fname, gname) -> riga
#   G1, G2, G3, Cov2, LP2, Cov3, LP3
class LeverageRow(Tuple):
    pass


def leverage_row(fname: str, gname: str) -> Dict[str, object]:
    """Riga ESATTA per la coppia (f, g): G_1, G_2, G_3, Cov/LP a k=2 e k=3."""
    M1 = lift(base_function(fname, 1), GADGETS_1BIT[gname], 1)
    M2 = lift(base_function(fname, 2), GADGETS_1BIT[gname], 2)
    M3 = lift(base_function(fname, 3), GADGETS_1BIT[gname], 3)
    c1, l1 = _cov_lp(M1)
    c2, l2 = _cov_lp(M2)
    c3, l3 = _cov_lp(M3)
    g1, g2, g3 = Fraction(c1) - l1, Fraction(c2) - l2, Fraction(c3) - l3
    return {
        "f": fname,
        "g": gname,
        "G1": g1,
        "G2": g2,
        "G3": g3,
        "Cov2": c2,
        "LP2": l2,
        "Cov3": c3,
        "LP3": l3,
    }


def sweep(
    outers: Sequence[str] = DEFAULT_OUTERS,
    gadgets: Sequence[str] = DEFAULT_GADGETS,
) -> List[Dict[str, object]]:
    """Sweep ESATTO su tutte le coppie (f, g): una riga leverage_row per coppia."""
    rows: List[Dict[str, object]] = []
    for fname in outers:
        for gname in gadgets:
            rows.append(leverage_row(fname, gname))
    return rows


# --------------------------------------------------------------------------- #
#  Il KILLER: G_3 ricostruito da una delle tre leggi di composizione?         #
# --------------------------------------------------------------------------- #

def law_multiplicative(g1: Fraction, g2: Fraction, g3: Fraction) -> bool:
    """(a) MOLTIPLICATIVA (tensore/dualita' LP):  G_3 == (G_2)^2."""
    return g3 == g2 * g2


def law_affine(g1: Fraction, g2: Fraction, g3: Fraction) -> bool:
    """(b) AFFINE/RICORSIVA a 2 termini:  G_3 == 2*G_2 - G_1.

    E' la continuazione lineare in k della sequenza (G_1, G_2) ai passi
    successivi:  G_k = G_1 + (k-1)*(G_2 - G_1)  ->  G_3 = 2*G_2 - G_1.
    """
    return g3 == 2 * g2 - g1


def law_poly_gadget(
    g1: Fraction,
    g2: Fraction,
    g3: Fraction,
    gadget_g2_by_g: Fraction,
) -> bool:
    """(c) POLY-DEL-GADGET:  G_3 dipende SOLO dal gadget g e da k.

    Per un gadget di permutazione il gap a k=2 vale 0 oppure 1 a seconda
    dell'outer (J - I_4 da' G_2 = 1, le altre 0): se G_k fosse funzione del SOLO
    gadget × una funzione di k, allora tutte le coppie con quel gadget avrebbero
    lo stesso G_3, previsto come  2 * (gap tipico aperto a k=2 da g).  Operativa-
    mente passiamo `gadget_g2_by_g` = il valore di G_2 caratteristico del gadget
    (il MASSIMO G_2 osservato per quel gadget sullo sweep), e prevediamo
    G_3 == 2 * gadget_g2_by_g.  Cattura "G_k = invariante(g) * funzione_lineare(k)".
    """
    return g3 == 2 * gadget_g2_by_g


def killed(row: Dict[str, object], gadget_g2_by_g: Fraction) -> bool:
    """True sse G_3 della coppia e' ricostruito da ALMENO una delle tre leggi."""
    g1 = row["G1"]; g2 = row["G2"]; g3 = row["G3"]  # type: ignore[assignment]
    assert isinstance(g1, Fraction) and isinstance(g2, Fraction) and isinstance(g3, Fraction)
    return (
        law_multiplicative(g1, g2, g3)
        or law_affine(g1, g2, g3)
        or law_poly_gadget(g1, g2, g3, gadget_g2_by_g)
    )


def killer_table(
    outers: Sequence[str] = DEFAULT_OUTERS,
    gadgets: Sequence[str] = DEFAULT_GADGETS,
) -> List[Dict[str, object]]:
    """Tabella completa: per ogni coppia (f, g) la riga + i flag delle leggi + killed.

    `gadget_g2_by_g` (necessario alla legge (c)) e' il massimo G_2 osservato per il
    gadget g sullo sweep, calcolato in una prima passata.
    """
    rows = sweep(outers, gadgets)
    # prima passata: G_2 caratteristico per gadget (max su tutti gli outer)
    g2_by_gadget: Dict[str, Fraction] = {}
    for row in rows:
        gname = row["g"]; g2 = row["G2"]  # type: ignore[assignment]
        assert isinstance(gname, str) and isinstance(g2, Fraction)
        cur = g2_by_gadget.get(gname, Fraction(0))
        if g2 > cur:
            g2_by_gadget[gname] = g2
    out: List[Dict[str, object]] = []
    for row in rows:
        gname = row["g"]  # type: ignore[assignment]
        assert isinstance(gname, str)
        gg2 = g2_by_gadget.get(gname, Fraction(0))
        g1 = row["G1"]; g2 = row["G2"]; g3 = row["G3"]  # type: ignore[assignment]
        assert isinstance(g1, Fraction) and isinstance(g2, Fraction) and isinstance(g3, Fraction)
        rec = dict(row)
        rec["law_mult"] = law_multiplicative(g1, g2, g3)
        rec["law_affine"] = law_affine(g1, g2, g3)
        rec["law_poly"] = law_poly_gadget(g1, g2, g3, gg2)
        rec["killed"] = killed(row, gg2)
        rec["distinct_vals"] = len({g1, g2, g3})
        # candidato door-C non falsificato: G_2,G_3 esatti (sempre qui), >=2 valori
        # distinti nella sequenza, e nessuna legge ricostruisce G_3.
        rec["doorC_candidate"] = (rec["distinct_vals"] >= 2) and (not rec["killed"])
        out.append(rec)
    return out


def doorC_candidates(
    outers: Sequence[str] = DEFAULT_OUTERS,
    gadgets: Sequence[str] = DEFAULT_GADGETS,
) -> List[Dict[str, object]]:
    """Le coppie (f, g) candidate door-C NON falsificate (vedi killer_table)."""
    return [r for r in killer_table(outers, gadgets) if r["doorC_candidate"]]
