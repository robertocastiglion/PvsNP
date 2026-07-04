"""Cono / politopo dei momenti di Kronecker ESATTO e caccia ai "buchi" (sporadic in-cone).

CONTESTO (PvsNP-lab, Module 30 GCT/Kronecker, Entry 35 — lever umano "implementa il cono di
Klyachko esatto e cerca un buco").  Continua `saturation.py` (Entry 34): lo stretching N=2
splitta i vanishing sporadici in HOLE (g(2*)>0) / RAY (g(2*)=0).  Qui costruiamo un oggetto
PIU' FORTE dello stretch: l'INNER APPROXIMATION esatta del politopo dei momenti

    P_D  =  conv{ point_norm(lam,mu,nu) : g(lam,mu,nu) > 0,  1 <= d <= D }

dove point_norm normalizza la terna a un vettore di Q^{3k} (k = max #parti su d<=D).  P_D e'
un politopo RAZIONALE i cui vertici sono i punti normalizzati delle terne a coefficiente di
Kronecker POSITIVO: una inner approximation, scala per scala, del cono dei momenti di Kronecker
(la chiusura del semigruppo {(lam,mu,nu) : g(N*..)>0 per qualche N}).

IPOTESI (explorer).  Cerca BUCHI = vanishing sporadici (g==0) il cui punto normalizzato cade
DENTRO P_D.  Distingui:
  - SUPERFICIALE : in P_D e g(N*triple) > 0 per qualche N in {2,3,4}  (gia' visto da saturation:
                   il punto e' raggiungibile dilatando di poco — visibile allo stretch).
  - PROFONDO     : in P_D ma g(N*triple) == 0 per OGNI N in {2,3,4}  (il punto e' in cono ma
                   nessuno stretch piccolo lo "accende" — INVISIBILE a saturation.py).
  - FUORI-CONO   : il punto normalizzato non e' in P_D.

KILLER (pre-dichiarato).
  KILLER-1: se OGNI sporadico in-cono e' superficiale (g(N*)>0 per N in {2,3,4}) allora il
            cono = test di stretch esteso => collasso (RESTATEMENT).
  KILLER-2: se OGNI faccetta di P_D e' riconducibile al dizionario noto (nc_length, nc_maxpart,
            equazioni di normalizzazione del simplesso, disuguaglianze Klyachko/Horn note)
            allora l'H-rep di P_D RESTATES Klyachko => collasso.
  SOPRAVVIVENZA: un buco PROFONDO (in-cono, g(N*)=0 per N=2,3,4) OPPURE una faccetta
            FUORI-DIZIONARIO.

Tutto e' ESATTO (Fraction/int, deterministico): point_norm in Q^{3k}, il test di membership
e' un LP di feasibility razionale (Phase-I, minimizza la somma delle variabili artificiali —
feasible sse l'ottimo == 0; NESSUN float), le faccette sono prodotte da un beneath-beyond
RAZIONALE (double description).

CONFINE DI ONESTA' (boundary, EN).  This is an EXACT finite computation: P_D is the convex hull
of normalized Kronecker-positive triple points for d<=D; membership of a vanishing point is an
exact rational LP feasibility test; facets come from an exact beneath-beyond.  P_D is an INNER
approximation of the Kronecker moment cone at a FIXED scale, NOT the cone itself: a "deep hole"
here only means the point is in conv(S) yet g(N*)=0 for N in {2,3,4}; a "facet out of dictionary"
only means it is not implied by the chosen finite list of known inequalities.  No claim is made
about Klyachko/Horn for Kronecker, about the saturation property, or about P vs NP.
"""

from __future__ import annotations

from fractions import Fraction
from itertools import permutations
from math import gcd
from typing import Dict, List, Sequence, Set, Tuple

from .kronecker import (
    Partition,
    kronecker,
    partitions,
    sporadic_vanishing,
    _triples,
    transpose,
)
from .saturation import stretch, perm_key

Triple = Tuple[Partition, Partition, Partition]
Vec = Tuple[Fraction, ...]


# ======================================================================================
#  1. Punti normalizzati e support
# ======================================================================================
def max_parts(D: int) -> int:
    """k = massimo numero di parti su TUTTE le partizioni di d, per 1<=d<=D.
    E' la lunghezza di padding comune: ogni partizione si estende a k parti con zeri."""
    return max(len(p) for d in range(1, D + 1) for p in partitions(d))


def point(triple: Triple, k: int) -> Vec:
    """Punto normalizzato della terna in Q^{3k}: ogni partizione e' paddata a k parti con
    zeri e divisa per d=|lam| (cosi' ogni blocco somma a 1), poi i tre blocchi sono concatenati.

    L'ordine degli argomenti CONTA (il punto dipende dall'ordine: e' un vettore concatenato),
    ma g e' simmetrico, quindi nel support inseriamo l'intera orbita di permutazione.  ESATTO.
    """
    d = sum(triple[0])
    if d == 0:
        raise ValueError("terna della partizione vuota non normalizzabile")
    out: List[Fraction] = []
    for p in triple:
        if sum(p) != d:
            raise ValueError("le tre partizioni devono avere la stessa somma d")
        padded = list(p) + [0] * (k - len(p))
        if len(padded) != k:
            raise ValueError(f"partizione con piu' di k={k} parti: {p}")
        out.extend(Fraction(x, d) for x in padded)
    return tuple(out)


def support_points(D: int, k: int) -> Set[Vec]:
    """Insieme (deduplicato) di tutti i punti normalizzati delle terne con g>0 a 1<=d<=D.

    Riusa kronecker + _triples (terne non ordinate, sfruttando la simmetria di g per non
    ripetere il calcolo di g) e poi inserisce l'INTERA orbita di permutazione di ogni terna
    positiva (il punto dipende dall'ordine, g no).  ESATTO, finito."""
    S: Set[Vec] = set()
    for d in range(1, D + 1):
        for tri in _triples(d):
            if kronecker(*tri) > 0:
                for perm in set(permutations(tri)):
                    S.add(point(perm, k))
    return S


# ======================================================================================
#  2. LP di feasibility razionale (Phase-I, NESSUN float)
# ======================================================================================
def _feasible_eq(Aeq: List[List[Fraction]], beq: List[Fraction]) -> bool:
    """True sse il sistema { x >= 0, Aeq @ x = beq } e' AMMISSIBILE.  Esatto su Fraction.

    Phase-I del metodo simplesso: si aggiunge una variabile artificiale per ogni riga (dopo
    aver reso beq >= 0 per cambio di segno) e si MINIMIZZA la somma delle artificiali con la
    regola di Bland (anti-ciclo).  Il sistema originale e' ammissibile sse l'ottimo == 0 (tutte
    le artificiali espulse).  E' la stessa aritmetica del simplesso razionale di
    `exactness_composes.gap._simplex_max`, in forma Phase-I per equazioni.
    """
    m = len(Aeq)
    n = len(Aeq[0]) if m else 0
    A = [row[:] for row in Aeq]
    b = list(beq)
    for i in range(m):
        if b[i] < 0:
            A[i] = [-v for v in A[i]]
            b[i] = -b[i]
    total = n + m
    # tableau: m righe vincolo (strutturali | artificiali identita' | RHS)
    T: List[List[Fraction]] = [
        A[i][:] + [Fraction(int(j == i)) for j in range(m)] + [b[i]] for i in range(m)
    ]
    basis = list(range(n, n + m))  # base iniziale = artificiali
    # riga obiettivo W = sum(artificiali).  Costo ridotto r_j = c_j - z_j; con c=1 sulle
    # artificiali (basiche) e 0 sulle strutturali, r_j = -sum_i T[i][j] sulle strutturali e
    # 0 sulle artificiali.  Per MINIMIZZARE scegliamo l'entrante con r_j < 0, cioe' la colonna
    # che riduce W; qui memorizziamo direttamente +sum (la "riduzione" da massimizzare).
    obj: List[Fraction] = [Fraction(0)] * (total + 1)
    for j in range(n):
        obj[j] = sum(T[i][j] for i in range(m))
    obj[total] = sum(T[i][total] for i in range(m))  # valore corrente di W
    T.append(obj)

    while True:
        col = -1
        for j in range(total):
            if T[m][j] > 0:  # questa colonna riduce W (Bland: primo indice valido)
                col = j
                break
        if col == -1:
            break
        row = -1
        best: Fraction | None = None
        for i in range(m):
            if T[i][col] > 0:
                ratio = T[i][total] / T[i][col]
                if (
                    best is None
                    or ratio < best
                    or (ratio == best and basis[i] < basis[row])
                ):
                    best = ratio
                    row = i
        if row == -1:
            raise ValueError("Phase-I illimitato (inatteso).")
        piv = T[row][col]
        T[row] = [v / piv for v in T[row]]
        for i in range(m + 1):
            if i != row and T[i][col] != 0:
                f = T[i][col]
                T[i] = [a - f * bb for a, bb in zip(T[i], T[row])]
        basis[row] = col

    return T[m][total] == 0


def in_cone(p: Sequence[Fraction], S: Sequence[Vec]) -> bool:
    """Test ESATTO  p in conv(S):  esiste theta >= 0 con sum theta_i = 1 e sum theta_i s_i = p.

    Lo riduciamo a un sistema di equazioni { x >= 0, Aeq x = beq } dove le righe sono le 3k
    coordinate (sum_i theta_i s_i[coord] = p[coord]) piu' la riga di normalizzazione
    (sum_i theta_i = 1), e risolviamo la feasibility con la Phase-I razionale `_feasible_eq`.
    Tutto Fraction, NESSUN float.
    """
    p = tuple(Fraction(v) for v in p)
    Slist = list(S)
    n = len(Slist)
    dim = len(p)
    Aeq: List[List[Fraction]] = [[Slist[i][d] for i in range(n)] for d in range(dim)]
    beq: List[Fraction] = [p[d] for d in range(dim)]
    Aeq.append([Fraction(1)] * n)  # sum theta = 1
    beq.append(Fraction(1))
    return _feasible_eq(Aeq, beq)


# ======================================================================================
#  3. Buchi: superficiale / profondo / fuori-cono
# ======================================================================================
def is_deep_hole(triple: Triple, S: Sequence[Vec], k: int, n_max: int = 4) -> bool:
    """True sse `triple` e' un buco PROFONDO: il suo punto normalizzato e' in conv(S) MA
    g(N*triple) == 0 per OGNI N in 2..n_max (nessuno stretch piccolo lo "accende").

    Un buco in-cono ma con tutti gli stretch piccoli nulli e' invisibile a `saturation.py`
    (che misura solo g(2*..), o N piccolo): e' il candidato di SOPRAVVIVENZA dell'ipotesi.
    """
    if not in_cone(point(triple, k), S):
        return False
    return all(kronecker(*stretch(triple, N)) == 0 for N in range(2, n_max + 1))


def holes(d: int, D: int, n_max: int = 4) -> Dict[str, object]:
    """Classifica OGNI vanishing sporadico di d (deduplicato per orbita di permutazione)
    rispetto al politopo P_D.  Ritorna un dict con conteggi e liste di terne:

      { 'k', 'n_sporadic', 'n_in_cone', 'n_superficial', 'n_deep', 'n_out',
        'in_cone': [...], 'superficial': [...], 'deep': [...], 'out': [...] }

    SUPERFICIALE = in-cono e g(N*)>0 per qualche N in 2..n_max;
    PROFONDO     = in-cono e g(N*)==0 per ogni N in 2..n_max;
    FUORI-CONO   = punto non in conv(S).  ESATTO.
    """
    k = max_parts(D)
    S = support_points(D, k)
    seen: Set = set()
    in_cone_l: List[Triple] = []
    superficial: List[Triple] = []
    deep: List[Triple] = []
    out: List[Triple] = []
    for t in sporadic_vanishing(d):
        pk = perm_key(t)
        if pk in seen:
            continue
        seen.add(pk)
        if not in_cone(point(t, k), S):
            out.append(t)
            continue
        in_cone_l.append(t)
        if any(kronecker(*stretch(t, N)) > 0 for N in range(2, n_max + 1)):
            superficial.append(t)
        else:
            deep.append(t)
    return {
        "k": k,
        "n_sporadic": len(seen),
        "n_in_cone": len(in_cone_l),
        "n_superficial": len(superficial),
        "n_deep": len(deep),
        "n_out": len(out),
        "in_cone": in_cone_l,
        "superficial": superficial,
        "deep": deep,
        "out": out,
    }


def summary(d: int, D: int, n_max: int = 4) -> Tuple[int, int, int, int, int]:
    """(#sporadic, #in_cone, #superficiali, #profondi, #fuori_cono) per d rispetto a P_D."""
    h = holes(d, D, n_max)
    return (
        h["n_sporadic"],
        h["n_in_cone"],
        h["n_superficial"],
        h["n_deep"],
        h["n_out"],
    )


# ======================================================================================
#  4. FACCETTE (KILLER-2): H-rep di P_D via beneath-beyond RAZIONALE
# ======================================================================================
def _rref(rows: List[List[Fraction]], ncol: int) -> Tuple[List[List[Fraction]], List[int]]:
    """Riduzione di Gauss-Jordan ESATTA (Fraction).  Ritorna (righe ridotte non nulle, pivots)."""
    rows = [r[:] for r in rows]
    m = len(rows)
    pr = 0
    pivots: List[int] = []
    for c in range(ncol):
        piv = None
        for r in range(pr, m):
            if rows[r][c] != 0:
                piv = r
                break
        if piv is None:
            continue
        rows[pr], rows[piv] = rows[piv], rows[pr]
        pv = rows[pr][c]
        rows[pr] = [x / pv for x in rows[pr]]
        for r in range(m):
            if r != pr and rows[r][c] != 0:
                f = rows[r][c]
                rows[r] = [a - f * b for a, b in zip(rows[r], rows[pr])]
        pivots.append(c)
        pr += 1
        if pr == m:
            break
    return rows[:pr], pivots


def _affine_coords(S: List[Vec]) -> Tuple[List[Vec], int, List[int]]:
    """Proietta i punti di S in coordinate dell'INVILUPPO AFFINE (rendendo il politopo
    PIENO-dimensionale), cosi' il beneath-beyond opera in R^affdim.

    I vettori differenza s-S[0] vivono in un sottospazio di dimensione affdim; le colonne-pivot
    della loro rref formano una carta (la proiezione su quelle colonne e' iniettiva sul
    sottospazio).  Ritorna (coordinate ridotte, affdim, indici-colonna pivot)."""
    base = S[0]
    n = len(base)
    diffs = [[a - b for a, b in zip(s, base)] for s in S]
    _, piv = _rref([d[:] for d in diffs[1:]], n)
    coords = [tuple(d[c] for c in piv) for d in diffs]
    assert len(set(coords)) == len(set(S)), "proiezione affine non iniettiva"
    return coords, len(piv), piv


def _hyperplane(pts: List[Vec], m: int) -> Tuple[List[Fraction], Fraction] | None:
    """Iperpiano a.x=b passante per `pts` (in R^m), se sono affinemente indipendenti a meno di
    una direzione (nullita' 1).  Ritorna (a, b) oppure None se non determinato."""
    diffs = [[pts[i][t] - pts[0][t] for t in range(m)] for i in range(1, len(pts))]
    R, pv = _rref([d[:] for d in diffs], m)
    nullc = [c for c in range(m) if c not in pv]
    if len(nullc) != 1:
        return None
    fc = nullc[0]
    a = [Fraction(0)] * m
    a[fc] = Fraction(1)
    for i, pc in enumerate(pv):
        a[pc] = -R[i][fc]
    b = sum(a[t] * pts[0][t] for t in range(m))
    return a, b


def _beneath_beyond(P: List[Vec]) -> List[Tuple[Tuple[Fraction, ...], Fraction]]:
    """H-rep (faccette a.x<=b) di conv(P) per P PIENO-dimensionale in R^m, via beneath-beyond
    incrementale ESATTO (Fraction).  Algoritmo classico: si parte dal simplesso di affdim+1
    vertici affinemente indipendenti, se ne calcolano le faccette orientate verso l'interno,
    poi si inseriscono i punti uno per volta aggiornando l'H-rep tramite gli orizzonti
    (ridge tra faccetta violata e faccetta mantenuta).  Deterministico."""
    m = len(P[0])
    # simplesso iniziale: affdim+1 = m+1 punti affinemente indipendenti
    chosen = [0]
    basis: List[List[Fraction]] = []
    for i in range(1, len(P)):
        v = [P[i][t] - P[0][t] for t in range(m)]
        R, _ = _rref([r[:] for r in basis + [v]], m)
        if len(R) == len(basis) + 1:
            basis.append(v)
            chosen.append(i)
        if len(chosen) == m + 1:
            break
    assert len(chosen) == m + 1, "P non e' pieno-dimensionale in R^m"
    simplex = [P[i] for i in chosen]
    interior = [
        Fraction(sum(simplex[j][t] for j in range(m + 1)), m + 1) for t in range(m)
    ]
    facets: List[Tuple[Tuple[Fraction, ...], Fraction]] = []
    for skip in range(m + 1):
        pts = [simplex[j] for j in range(m + 1) if j != skip]
        hp = _hyperplane(pts, m)
        assert hp is not None
        a, b = hp
        if sum(a[t] * interior[t] for t in range(m)) > b:
            a = [-x for x in a]
            b = -b
        facets.append((tuple(a), b))

    Vused = list(simplex)
    rest = [P[i] for i in range(len(P)) if i not in chosen]
    for q in rest:
        viol = [f for f in facets if sum(f[0][t] * q[t] for t in range(m)) > f[1]]
        if not viol:
            Vused.append(q)
            continue
        keep = [f for f in facets if sum(f[0][t] * q[t] for t in range(m)) <= f[1]]
        Vall = Vused + [q]
        new_facets: List[Tuple[Tuple[Fraction, ...], Fraction]] = []
        for fv in viol:
            for fk in keep:
                # vertici comuni alle due faccette (il ridge dell'orizzonte)
                tv = [
                    v
                    for v in Vused
                    if sum(fv[0][t] * v[t] for t in range(m)) == fv[1]
                    and sum(fk[0][t] * v[t] for t in range(m)) == fk[1]
                ]
                if len(tv) < m - 1:
                    continue
                if m >= 2:
                    dd = [[tv[i][t] - tv[0][t] for t in range(m)] for i in range(1, len(tv))]
                    R, _ = _rref([d[:] for d in dd], m)
                    if len(R) != m - 2:
                        continue
                hp = _hyperplane(tv + [q], m)
                if hp is None:
                    continue
                a, b = hp
                vals = [sum(a[t] * v[t] for t in range(m)) for v in Vall]
                if all(v <= b for v in vals):
                    pass
                elif all(v >= b for v in vals):
                    a = [-x for x in a]
                    b = -b
                else:
                    continue
                new_facets.append((tuple(a), b))
        facets = _dedup_ineqs(keep + new_facets, m)
        Vused.append(q)
    return facets


def _normalize_int(a: Sequence[Fraction], b: Fraction) -> Tuple[Tuple[int, ...], int]:
    """Normalizza (a, b) a coefficienti interi coprimi (clear-denominators + gcd)."""
    dens = [x.denominator for x in a] + [b.denominator]
    L = 1
    for dv in dens:
        L = L * dv // gcd(L, dv)
    ai = tuple(int(x * L) for x in a)
    bi = int(b * L)
    g = 0
    for x in ai:
        g = gcd(g, abs(x))
    g = gcd(g, abs(bi)) or 1
    return tuple(x // g for x in ai), bi // g


def _dedup_ineqs(
    facets: List[Tuple[Tuple[Fraction, ...], Fraction]], m: int
) -> List[Tuple[Tuple[Fraction, ...], Fraction]]:
    """Deduplica le disuguaglianze a.x<=b per forma intera normalizzata."""
    seen: Set = set()
    out: List[Tuple[Tuple[Fraction, ...], Fraction]] = []
    for a, b in facets:
        key = _normalize_int(a, b)
        if key not in seen:
            seen.add(key)
            out.append((a, b))
    return out


def facets(D: int = 3) -> List[Tuple[Tuple[int, ...], int]]:
    """H-representation di P_D in coordinate AMBIENT (Q^{3k}), come lista di (a, b) interi
    coprimi con la convenzione  a . x <= b.

    Procedura: (1) support S e proiezione nell'inviluppo affine; (2) beneath-beyond razionale
    nel sottospazio per ottenere le faccette; (3) per ogni faccetta, ri-deriva l'inequazione in
    coordinate AMBIENT dall'iperpiano passante per i suoi vertici-tight ambient (cosi' e'
    direttamente confrontabile col dizionario), orientata col verso che contiene tutto S.

    ATTENZIONE PRESTAZIONI: D=3 (dim affine 6, |S|=14) e' ISTANTANEO.  D=4 (dim affine 9,
    |S|=53, 264 faccette) e' FATTIBILE ma LENTO (~8 minuti col beneath-beyond Fraction): va
    eseguito solo in test marcati `slow` con timeout alto.  Per D>=5 il beneath-beyond esplode
    (non tentato).  Il default e' D=3.
    """
    k = max_parts(D)
    S = sorted(support_points(D, k))
    coords, affdim, piv = _affine_coords(S)
    red_facets = _beneath_beyond(coords)
    amb = len(S[0])
    out: List[Tuple[Tuple[int, ...], int]] = []
    seen: Set = set()
    for a_red, b_red in red_facets:
        # vertici tight nella faccetta (in coordinate ridotte)
        tight_idx = [
            i
            for i, c in enumerate(coords)
            if sum(a_red[t] * c[t] for t in range(affdim)) == b_red
        ]
        tight_amb = [S[i] for i in tight_idx]
        # ri-deriva l'iperpiano AMBIENT dai vertici tight, modulo le equazioni dell'affine hull
        a_amb, b_amb = _ambient_facet(tight_amb, S, amb)
        key = _normalize_int(a_amb, b_amb)
        if key not in seen:
            seen.add(key)
            out.append(key)
    out.sort()
    return out


def _affine_equations(S: List[Vec], amb: int) -> List[Tuple[List[Fraction], Fraction]]:
    """Equazioni dell'inviluppo affine di S in coordinate ambient: {(n, c) : n.x = c su S}.
    Sono le normalizzazioni implicite (ogni blocco somma a 1, e relazioni indotte)."""
    base = S[0]
    diffs = [[a - b for a, b in zip(s, base)] for s in S[1:]]
    R, piv = _rref(diffs, amb)
    free = [c for c in range(amb) if c not in piv]
    eqs: List[Tuple[List[Fraction], Fraction]] = []
    for fc in free:
        v = [Fraction(0)] * amb
        v[fc] = Fraction(1)
        for i, pc in enumerate(piv):
            v[pc] = -R[i][fc]
        eqs.append((v, sum(x * y for x, y in zip(v, base))))
    return eqs


def _ambient_facet(
    tight: List[Vec], S: List[Vec], amb: int
) -> Tuple[List[Fraction], Fraction]:
    """Inequazione AMBIENT a.x<=b della faccetta i cui vertici-tight (ambient) sono `tight`.

    L'iperpiano e' determinato a meno delle equazioni dell'inviluppo affine: imponiamo
    a ortogonale alle differenze dei vertici-tight E alle normali affini, l'unica direzione
    residua e' a.  Orientiamo a in modo che a.s <= b per ogni s in S."""
    eqs = _affine_equations(S, amb)
    diffs = [[tight[i][t] - tight[0][t] for t in range(amb)] for i in range(1, len(tight))]
    M = diffs + [list(n) for n, _ in eqs]
    R, pv = _rref([row[:] for row in M], amb)
    nullc = [c for c in range(amb) if c not in pv]
    # scegli la PRIMA direzione libera che dia un'inequazione valida (orientabile su tutto S)
    for fc in nullc:
        a = [Fraction(0)] * amb
        a[fc] = Fraction(1)
        for i, pc in enumerate(pv):
            a[pc] = -R[i][fc]
        b = sum(a[t] * tight[0][t] for t in range(amb))
        vals = [sum(a[t] * s[t] for t in range(amb)) for s in S]
        if all(v <= b for v in vals):
            return a, b
        if all(v >= b for v in vals):
            return [-x for x in a], -b
    # fallback (non dovrebbe accadere): ritorna la prima direzione comunque
    fc = nullc[0]
    a = [Fraction(0)] * amb
    a[fc] = Fraction(1)
    for i, pc in enumerate(pv):
        a[pc] = -R[i][fc]
    b = sum(a[t] * tight[0][t] for t in range(amb))
    return a, b


# ======================================================================================
#  5. classify_facet: dentro/fuori il dizionario noto (test di RIDUCIBILITA' esatto)
# ======================================================================================
def _dictionary_generators(
    S: List[Vec], amb: int, k: int
) -> Tuple[List[Tuple[List[Fraction], Fraction]], List[Tuple[List[Fraction], Fraction]]]:
    """Generatori del DIZIONARIO noto come disuguaglianze valide su P_D (in forma g.x <= rhs)
    piu' le equazioni dell'inviluppo affine.  Ritorna (gens_ineq, eqs).

    Dizionario elementare (tutte VERE su ogni punto normalizzato di partizioni):
      - NON-NEGATIVITA':  x_i >= 0   (le parti normalizzate sono >= 0)   ->  -x_i <= 0;
      - ORDINAMENTO:      x_i >= x_{i+1}  entro ogni blocco (parti non crescenti)
                                                                        ->  x_{i+1}-x_i <= 0.
    Equazioni affini: le normalizzazioni implicite (ogni blocco somma 1 + relazioni indotte),
    catturate ESATTAMENTE da `_affine_equations` (sono le uguaglianze che annullano tutto S).

    NB ONESTA': NON codifichiamo le disuguaglianze di Klyachko/Horn per Kronecker — NON sono
    note in forma chiusa generale (e' il punto aperto del campo).  Il dizionario qui e' la
    lista ELEMENTARE {nonneg, ordering} + l'affine hull.  Una faccetta NON implicata da questi
    generatori e' 'out_of_dictionary': un LIMITE SUPERIORE onesto del contenuto
    fuori-dal-dizionario-elementare, non un verdetto su Klyachko.
    """
    gens: List[Tuple[List[Fraction], Fraction]] = []
    for i in range(amb):  # -x_i <= 0
        v = [Fraction(0)] * amb
        v[i] = Fraction(-1)
        gens.append((v, Fraction(0)))
    for blk in range(amb // k):  # x_{i+1}-x_i <= 0 entro il blocco
        for j in range(k - 1):
            i = blk * k + j
            v = [Fraction(0)] * amb
            v[i + 1] = Fraction(1)
            v[i] = Fraction(-1)
            gens.append((v, Fraction(0)))
    eqs = _affine_equations(S, amb)
    return gens, eqs


def _is_implied(
    a: Sequence[int],
    b: int,
    gens: List[Tuple[List[Fraction], Fraction]],
    eqs: List[Tuple[List[Fraction], Fraction]],
    amb: int,
) -> bool:
    """True sse la disuguaglianza a.x <= b e' IMPLICATA (su P_D) dai generatori del dizionario:
    esistono mu >= 0 (sui gens) e lambda LIBERO (sulle eqs, spezzato in lam+,lam->=0) e uno
    slack s >= 0 tali che

        sum mu_g g_vec + sum lambda_e n_e = a        (uguaglianza dei coefficienti)
        sum mu_g g_rhs + sum lambda_e c_e + s = b     (RHS combinato <= b)

    cioe' a.x<=b e' una conseguenza conica del dizionario (Farkas).  Feasibility ESATTA via la
    Phase-I razionale `_feasible_eq` — NESSUN float."""
    cols: List[List[Fraction]] = [g[0] for g in gens]
    rhs: List[Fraction] = [g[1] for g in gens]
    for n, c in eqs:  # lambda libero = lam+ - lam-
        cols.append(list(n))
        rhs.append(c)
        cols.append([-x for x in n])
        rhs.append(-c)
    nv = len(cols)
    # righe-coordinata: sum_j cols[j][t] * w_j (+0*slack) = a[t]
    Aeq: List[List[Fraction]] = [
        [cols[j][t] for j in range(nv)] + [Fraction(0)] for t in range(amb)
    ]
    beq: List[Fraction] = [Fraction(int(a[t])) for t in range(amb)]
    # riga-RHS: sum_j rhs[j] * w_j + slack = b
    Aeq.append([rhs[j] for j in range(nv)] + [Fraction(1)])
    beq.append(Fraction(int(b)))
    return _feasible_eq(Aeq, beq)


def classify_facet(
    ineq: Tuple[Sequence[int], int],
    S: List[Vec],
    k: int,
) -> str:
    """Classifica una faccetta a.x<=b di P_D rispetto al DIZIONARIO noto.  Ritorna:

      'in_dictionary'     : la disuguaglianza e' IMPLICATA (conseguenza conica esatta) dai
                            generatori {nonneg, ordering} modulo l'inviluppo affine;
      'out_of_dictionary' : NON e' implicata — candidato fuori-dizionario.

    Il test e' un Farkas ESATTO (`_is_implied`), NON un pattern-matching: rigoroso e
    deterministico.  Vedi `_dictionary_generators` per il confine di onesta' sul dizionario.
    """
    amb = len(S[0])
    gens, eqs = _dictionary_generators(S, amb, k)
    a, b = ineq
    return "in_dictionary" if _is_implied(a, b, gens, eqs, amb) else "out_of_dictionary"


def facet_report(D: int = 3) -> Dict[str, object]:
    """Calcola le faccette di P_D e le classifica col test di riducibilita' ESATTO.  Ritorna:

      { 'D', 'k', 'n_facets', 'n_in_dictionary', 'n_out_of_dictionary',
        'out_of_dictionary': [faccette fuori-dizionario],
        'examples': {classe: faccetta-esempio} }.

    KILLER-2: n_out_of_dictionary == 0  => H-rep nel dizionario => collasso (RESTATEMENT);
    > 0 => faccette fuori-dizionario (candidate sopravvivenza, riportate esattamente).
    """
    k = max_parts(D)
    S = sorted(support_points(D, k))
    amb = len(S[0])
    gens, eqs = _dictionary_generators(S, amb, k)
    F = facets(D)
    in_dict: List[Tuple[Tuple[int, ...], int]] = []
    out_dict: List[Tuple[Tuple[int, ...], int]] = []
    for ineq in F:
        if _is_implied(ineq[0], ineq[1], gens, eqs, amb):
            in_dict.append(ineq)
        else:
            out_dict.append(ineq)
    examples: Dict[str, Tuple] = {}
    if in_dict:
        examples["in_dictionary"] = in_dict[0]
    if out_dict:
        examples["out_of_dictionary"] = out_dict[0]
    return {
        "D": D,
        "k": k,
        "n_facets": len(F),
        "n_in_dictionary": len(in_dict),
        "n_out_of_dictionary": len(out_dict),
        "out_of_dictionary": out_dict,
        "examples": examples,
    }
