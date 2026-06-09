"""Regola sui gadget per il gap di integralita' del LIFT (Modulo 18, ciclo 1).

Ipotesi dell'EXPLORER da riconfermare/falsificare:
    per il lift  F = f ∘ g^k  con gadget integrale a 1 bit, il gap pinnato sul LP
    si apre  (G* > 0)  SE E SOLO SE
        (a) il gadget g e' una matrice di PERMUTAZIONE 2x2  (un solo 1 per riga e
            per colonna  ->  esattamente {XOR, EQ}),  E
        (b) l'outer f produce una pattern-matrix non integrale per quel gadget.
    Per i 7 gadget non-permutazione (AND, OR, NAND, NOR, IMP, PROJ_X, PROJ_Y)
    il lift resta integrale per OGNI outer.

DISCRIMINANTE chiave (novita' vs restatement):
    EQ = [[1,0],[0,1]] e' una permutazione MA non e' "XOR-Fourier". Se EQ apre il
    gap esattamente come XOR la regola e' "PERMUTAZIONE" (contenuto nuovo); se solo
    XOR lo apre e' "pattern-matrix Fourier" (restatement Sherstov/Razborov).

Tutto e' ESATTO (Fraction): riusa gap.py (gstar/cover_number/frac_cover) e
compose.py (lift_named/GADGETS_1BIT/base_function). Nessuna duplicazione della
logica LP/cover, nessun float introdotto.
"""

from __future__ import annotations

from fractions import Fraction
from itertools import product
from typing import Dict, Sequence, Tuple

from .gap import BoolMatrix, cover_number, frac_cover, gstar
from .compose import GADGETS_1BIT, base_function, lift, lift_named

# Chiave di cella della tabella: (nome_outer, nome_gadget) -> (Cov, LP, G*)
CellKey = Tuple[str, str]
Cell = Tuple[int, Fraction, Fraction]

# Set di default usati dall'Explorer.
DEFAULT_OUTERS = ("AND", "OR", "XOR", "MAJ", "NAND", "NOR")
DEFAULT_GADGETS = tuple(GADGETS_1BIT.keys())  # i 9 gadget a 1 bit


def is_permutation_gadget(g: BoolMatrix) -> bool:
    """True sse il gadget 2x2 g e' una matrice di PERMUTAZIONE.

    Permutazione 2x2  <=>  esattamente un 1 per ogni riga e per ogni colonna.
    Fra i 9 gadget a 1 bit cio' seleziona ESATTAMENTE {XOR, EQ}.
    """
    if len(g) != 2 or len(g[0]) != 2:
        # Generalizzazione difensiva: ogni riga/colonna ha somma 1.
        n = len(g)
        if any(len(row) != n for row in g):
            return False
        rows_ok = all(sum(row) == 1 for row in g)
        cols_ok = all(sum(g[r][c] for r in range(n)) == 1 for c in range(n))
        return rows_ok and cols_ok
    rows_ok = all(sum(row) == 1 for row in g)
    cols_ok = all(sum(g[r][c] for r in range(2)) == 1 for c in range(2))
    return rows_ok and cols_ok


def gap_table(
    outers: Sequence[str] = DEFAULT_OUTERS,
    gadgets: Sequence[str] = DEFAULT_GADGETS,
    k: int = 2,
    skip_dense_threshold: int | None = None,
) -> Dict[CellKey, Cell]:
    """Tabella ESATTA (nome_f, nome_g) -> (Cov, LP, G*) del lift  f ∘ g^k.

    Cov = cover_number, LP = frac_cover, G* = Cov - LP  (tutto da gap.py).

    `skip_dense_threshold`: se valorizzato, le celle in cui la matrice 2^k x 2^k ha
    PIU' di tale numero di entrate-1 vengono SALTATE (non inserite nella mappa).
    Serve a k>=3, dove cover_number (set-cover esatto) non scala alle 8x8 dense.
    Con None nessuna cella e' saltata. Nessun float, nessuna approssimazione: una
    cella o e' calcolata in modo esatto o e' assente.
    """
    table: Dict[CellKey, Cell] = {}
    for fname in outers:
        f = base_function(fname, k)
        for gname in gadgets:
            M = lift(f, GADGETS_1BIT[gname], k)
            if skip_dense_threshold is not None:
                n_ones = sum(sum(row) for row in M)
                if n_ones > skip_dense_threshold:
                    continue
            cov = cover_number(M)
            lp = frac_cover(M)
            table[(fname, gname)] = (cov, lp, Fraction(cov) - lp)
    return table


def predict_gap(fname: str, gname: str, k: int) -> bool:
    """REGOLA prevista: 'g e' permutazione AND f apre la pattern-matrix'.

    Implementa la PREVISIONE strutturale dell'ipotesi, non una misura:
      * condizione necessaria (a): is_permutation_gadget(g);
      * condizione (b): l'outer f, applicato attraverso una permutazione, produce
        una pattern-matrix non integrale.  Per i gadget di permutazione il lift
        f ∘ g^k e' una "permutazione" delle celle del lift con il gadget EQ
        (identita' di pattern), quindi (b) si decide UNA volta sola sul gadget EQ:
            apre_pattern(f, k)  :=  G*(f ∘ EQ^k) > 0.
        Cosi' la previsione e' coerente per XOR ed EQ (entrambe permutazioni) e
        falsa per i 7 gadget non-permutazione, come da ipotesi.

    Nota: predict_gap usa la misura su EQ solo per stabilire la proprieta' (b)
    dell'OUTER; la TESI da verificare e' che questa previsione coincida con
    G* > 0 misurato su OGNI gadget (incluso XOR).
    """
    g = GADGETS_1BIT[gname]
    if not is_permutation_gadget(g):
        return False
    # (b) pattern non integrale dell'outer, decisa sul rappresentante EQ.
    return gstar(lift_named(fname, "EQ", k)) > 0


def measured_gap(fname: str, gname: str, k: int) -> Fraction:
    """G* ESATTO misurato per la cella (f, g) a livello k."""
    return gstar(lift_named(fname, gname, k))


def xor_eq_same_up_to_col_perm(fname: str, k: int) -> bool:
    """True sse  lift(f, XOR, k)  e  lift(f, EQ, k)  coincidono a meno di una
    PERMUTAZIONE delle colonne di Bob (y -> ~y, negazione bit a bit).

    Questa e' la chiave ESATTA del discriminante EQ-vs-XOR: XOR = EQ con i bit di
    Bob negati per coordinata, quindi i due lift sono uguali a meno di permutare le
    colonne. Una permutazione di righe/colonne preserva Cov, LP e G* in modo esatto,
    dunque  G*(f∘XOR^k) = G*(f∘EQ^k)  per OGNI k, SENZA ricalcolare l'LP costoso
    sulle 8x8 dense.  Se questo e' True, EQ apre il gap esattamente come XOR ->
    la regola e' "PERMUTAZIONE" (contenuto nuovo), non "XOR-Fourier".
    """
    Mx = lift_named(fname, "XOR", k)
    Me = lift_named(fname, "EQ", k)
    ys = list(product([0, 1], repeat=k))
    idx = {y: i for i, y in enumerate(ys)}
    # y -> indice della colonna con i bit negati
    p = [idx[tuple(1 - b for b in y)] for y in ys]
    Me_perm = tuple(tuple(row[p[j]] for j in range(len(row))) for row in Me)
    return Mx == Me_perm


def rule_matches_measurement(
    outers: Sequence[str] = DEFAULT_OUTERS,
    gadgets: Sequence[str] = DEFAULT_GADGETS,
    k: int = 2,
) -> Tuple[bool, list]:
    """Verifica che predict_gap coincida con (G* > 0) su TUTTE le celle.

    Ritorna (tutto_coerente, discrepanze) dove discrepanze elenca le celle in cui
    previsione e misura divergono: (f, g, predetto, G*_misurato).
    """
    mismatches = []
    for fname in outers:
        for gname in gadgets:
            pred = predict_gap(fname, gname, k)
            meas = measured_gap(fname, gname, k) > 0
            if pred != meas:
                mismatches.append((fname, gname, pred, measured_gap(fname, gname, k)))
    return (not mismatches, mismatches)
