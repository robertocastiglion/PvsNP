"""Coefficienti di Kronecker g(lam, mu, nu) ESATTI e il loro pattern di vanishing.

g(lam, mu, nu) e' la molteplicita' della irriducibile S^nu nel prodotto tensore
S^lam ⊗ S^mu del gruppo simmetrico S_d (equivalentemente il prodotto interno dei
caratteri).  E' il protagonista del programma GCT (Geometric Complexity Theory):
decidere se g(lam,mu,nu) > 0 — la "Kronecker positivity" — e' #P-hard in generale
(Ikenmeyer-Mulmuley-Walter) e governa le ostruzioni di rappresentazione.

Calcolo ESATTO (Fraction/int, deterministico) via i caratteri di S_d, ottenuti con la
regola di Murnaghan-Nakayama (rimozione di border strip).  Tutto in aritmetica intera
razionale: nessun float.

IPOTESI DI LABORATORIO (dall'explorer): su d<=5 il pattern di vanishing (g==0) COLLASSA
nelle tre condizioni necessarie note per il non-vanishing (length-bound, max-part,
dominance/semigruppo) — cioe' g==0 sse almeno una NC nota e' violata.  KILLER: una terna
con g==0 che soddisfa TUTTE le NC note = vanishing SPORADICO = contenuto fuori dizionario
(falsifica l'ipotesi-lab, sopravvivenza).

Honesty boundary (EN).  This is an EXACT finite computation of Kronecker coefficients on
partitions of d<=6 and a comparison of the observed zero-set with a predictor built from
KNOWN necessary conditions for non-vanishing.  It is NOT a theorem about Kronecker
positivity, GCT occurrence obstructions, or P vs NP.  A non-empty `sporadic_vanishing`
only means the chosen finite set of necessary conditions does not characterize the zero
set on that d — i.e. the lab-hypothesis "vanishing collapses into the known dictionary"
fails there.  No claim about deciding g>0 efficiently is made.
"""

from __future__ import annotations

from fractions import Fraction
from functools import lru_cache
from math import factorial
from typing import Dict, List, Tuple

Partition = Tuple[int, ...]


# --------------------------------------------------------------------------------------
#  Partizioni
# --------------------------------------------------------------------------------------
def partitions(d: int) -> List[Partition]:
    """Tutte le partizioni di d (parti positive in ordine NON crescente), ordinate
    in modo deterministico (decrescente lessicografico).  partitions(0) == [()]."""
    if d == 0:
        return [()]
    out: List[Partition] = []

    def rec(rem: int, cap: int, acc: List[int]) -> None:
        if rem == 0:
            out.append(tuple(acc))
            return
        for part in range(min(rem, cap), 0, -1):
            acc.append(part)
            rec(rem - part, part, acc)
            acc.pop()

    rec(d, d, [])
    return out


def transpose(lam: Partition) -> Partition:
    """Partizione coniugata (trasposta del diagramma di Young)."""
    if not lam:
        return ()
    return tuple(sum(1 for p in lam if p > j) for j in range(lam[0]))


def cycle_type_multiplicities(alpha: Partition) -> Dict[int, int]:
    """m_i = numero di parti di alpha uguali a i (tipo-ciclo come moltiplicita')."""
    m: Dict[int, int] = {}
    for p in alpha:
        m[p] = m.get(p, 0) + 1
    return m


def z_alpha(alpha: Partition) -> int:
    """z_alpha = prod_i ( i^{m_i} * m_i! ), il numero che normalizza la classe di
    coniugio alpha in S_d (|classe| = d!/z_alpha)."""
    m = cycle_type_multiplicities(alpha)
    z = 1
    for i, mi in m.items():
        z *= (i ** mi) * factorial(mi)
    return z


# --------------------------------------------------------------------------------------
#  Caratteri del gruppo simmetrico via Murnaghan-Nakayama
# --------------------------------------------------------------------------------------
def _border_strips(lam: Partition, length: int) -> List[Tuple[Partition, int]]:
    """Tutte le border strip (rim hook) di dimensione `length` rimovibili da lam.
    Ritorna coppie (lam_ridotta, spread) dove ``spread`` = (#righe occupate dalla strip)-1,
    cioe' l'esponente del segno (-1)^spread nella regola di Murnaghan-Nakayama (height-1).

    Beta-sequence convention NON negativa e con padding di una riga: beta_i = lam_i + (m-1-i)
    per i in [0,m), dove m = len(lam)+1 (paddiamo lam con uno zero finale per consentire le
    strip che terminano in una riga "nuova" / svuotano l'ultima riga).  I beta sono distinti
    e decrescenti.  Rimuovere una rim hook di lunghezza k equivale a sostituire un beta = b
    con b - k, purche' b - k >= 0 non sia gia' presente.  Lo spread di segno e' il numero di
    beta strettamente compresi tra (b-k) e b — proprio (#righe della strip)-1.
    """
    m = len(lam) + 1
    padded = list(lam) + [0]
    beta = [padded[i] + (m - 1 - i) for i in range(m)]
    beta_set = set(beta)
    results: List[Tuple[Partition, int]] = []
    for idx in range(m):
        b = beta[idx]
        nb = b - length
        if nb < 0:
            continue
        if nb in beta_set:   # collisione: la rimozione non darebbe una partizione valida
            continue
        spread = sum(1 for x in beta if nb < x < b)
        new_beta = sorted((beta[i] if i != idx else nb for i in range(m)), reverse=True)
        # ricostruisci: lam'_i = new_beta_i - (m-1-i)
        new_lam = tuple(new_beta[i] - (m - 1 - i) for i in range(m))
        new_lam = tuple(p for p in new_lam if p > 0)
        results.append((new_lam, spread))
    return results


@lru_cache(maxsize=None)
def mn_character(lam: Partition, alpha: Partition) -> int:
    """Carattere chi^lam_alpha del gruppo simmetrico via Murnaghan-Nakayama.

    Ricorsione: si rimuove una border strip di lunghezza pari alla PRIMA parte di alpha
    (alpha[0]) in tutti i modi possibili; ogni modo contribuisce (-1)^(altezza-1) volte il
    carattere del diagramma ridotto rispetto al resto di alpha (alpha[1:]).

    Base: chi^()_() = 1 (somma di Young vuota).  ESATTO (intero).
    """
    if sum(lam) != sum(alpha):
        raise ValueError("lam e alpha devono partizionare lo stesso d")
    if not alpha:  # entrambe vuote
        return 1
    k = alpha[0]
    rest = alpha[1:]
    total = 0
    for reduced, spread in _border_strips(lam, k):
        # spread = (#righe della strip) - 1, gia' l'esponente del segno di MN
        total += ((-1) ** spread) * mn_character(reduced, rest)
    return total


# --------------------------------------------------------------------------------------
#  Hook-length formula (ancora di correttezza: dim S^lam = chi^lam_{(1^d)})
# --------------------------------------------------------------------------------------
def hook_length_dimension(lam: Partition) -> int:
    """dim(S^lam) via la formula degli hook: d! / prod_cella hook(cella).  Intero ESATTO."""
    d = sum(lam)
    conj = transpose(lam)
    prod = 1
    for i, row in enumerate(lam):
        for j in range(row):
            arm = row - j - 1           # celle a destra nella riga
            leg = conj[j] - i - 1       # celle sotto nella colonna
            prod *= (arm + leg + 1)
    return factorial(d) // prod


# --------------------------------------------------------------------------------------
#  Coefficiente di Kronecker
# --------------------------------------------------------------------------------------
def kronecker(lam: Partition, mu: Partition, nu: Partition) -> int:
    """g(lam,mu,nu) = (1/d!) sum_alpha (d!/z_alpha) chi^lam_alpha chi^mu_alpha chi^nu_alpha,

    somma sulle partizioni alpha di d (tipi-ciclo).  Equivalentemente, sum_alpha
    chi^lam_alpha chi^mu_alpha chi^nu_alpha / z_alpha.  Aritmetica esatta (Fraction);
    si verifica che il risultato sia intero (denominatore 1) — killer di bug.
    """
    d = sum(lam)
    if sum(mu) != d or sum(nu) != d:
        raise ValueError("lam, mu, nu devono partizionare lo stesso d")
    acc = Fraction(0)
    for alpha in partitions(d):
        za = z_alpha(alpha)
        term = (
            mn_character(lam, alpha)
            * mn_character(mu, alpha)
            * mn_character(nu, alpha)
        )
        acc += Fraction(term, za)
    assert acc.denominator == 1, f"Kronecker non intero: {acc} per {lam},{mu},{nu}"
    return int(acc)


# --------------------------------------------------------------------------------------
#  Condizioni necessarie note per il NON-vanishing (g > 0)
# --------------------------------------------------------------------------------------
def _length(lam: Partition) -> int:
    """ell(lam) = numero di parti (righe del diagramma)."""
    return len(lam)


def nc_length(lam: Partition, mu: Partition, nu: Partition) -> bool:
    """NC length-bound: se g(lam,mu,nu) > 0 allora per OGNI permutazione delle tre
    partizioni vale ell(a) <= ell(b) * ell(c).

    Fonte: il supporto della restrizione di S^lam ⊗ S^mu impone che le righe di nu siano
    al piu' ell(lam)*ell(mu) (Dvir; vedi anche Bessenrodt-Behns).  E' simmetrica nelle
    tre partizioni, quindi richiediamo tutte e tre le disuguaglianze.
    """
    la, lb, lc = _length(lam), _length(mu), _length(nu)
    return (la <= lb * lc) and (lb <= la * lc) and (lc <= la * lb)


def nc_maxpart(lam: Partition, mu: Partition, nu: Partition) -> bool:
    """NC max-part (duale della length-bound via coniugio simultaneo di DUE partizioni).

    Fatto noto: g(lam,mu,nu) e' invariante per coniugio simultaneo di due qualunque delle
    tre partizioni (il segno della trasposizione si elide quando moltiplicato due volte):
        g(lam,mu,nu) = g(lam',mu',nu) = g(lam',mu,nu') = g(lam,mu',nu').
    Quindi se g(lam,mu,nu) > 0 allora ciascuno di quei tre coefficienti e' > 0, e ad
    ognuno si applica la length-bound nc_length.  Applicando nc_length alle tre versioni
    coniugate-a-coppie si ottiene un vincolo sulle MAX-PART (lam' ha #righe = lam[0]).

    Questa e' una NC SOLIDA E DIMOSTRATA (verificata empiricamente: 0 falsi positivi su
    d<=5).  NB: la forma DIRETTA "nu_1 <= ell(lam)*ell(mu)" e la forma "nc_length su TUTTE
    e tre le trasposte" sono ENTRAMBE SBAGLIATE (producono falsi positivi gia' a d=3, p.es.
    g((3,),(3,),(3,))=1 le viola) perche' g(lam',mu',nu') NON e' g(lam,mu,nu); le evitiamo.
    """
    lamp, mup, nup = transpose(lam), transpose(mu), transpose(nu)
    return (
        nc_length(lamp, mup, nu)
        and nc_length(lamp, mu, nup)
        and nc_length(lam, mup, nup)
    )


# --------------------------------------------------------------------------------------
#  Predittore di vanishing e tabella
# --------------------------------------------------------------------------------------
def v_pred(lam: Partition, mu: Partition, nu: Partition) -> bool:
    """Predizione "g == 0": True se ALMENO UNA delle NC scelte e' violata.

    NC incluse nel predittore (solide e dimostrate, 0 falsi positivi su d<=5):
      - nc_length   (length-bound, Dvir)
      - nc_maxpart  (max-part bound via coniugio simultaneo di due partizioni)
    Volutamente NON includiamo la "max-part diretta" (nu_1 <= ell*ell): e' una NC SBAGLIATA
    (falsi positivi gia' a d=3) come istruito — meglio 2 NC solide che 3 di cui una rotta.
    """
    nc_ok = nc_length(lam, mu, nu) and nc_maxpart(lam, mu, nu)
    return not nc_ok


def _triples(d: int) -> List[Tuple[Partition, Partition, Partition]]:
    """Tutte le terne ordinate (lam,mu,nu) di partizioni di d, con lam<=mu<=nu nell'ordine
    della lista `partitions` (sfruttiamo la simmetria totale di g per non ripetere)."""
    ps = partitions(d)
    idx = {p: i for i, p in enumerate(ps)}
    out = []
    for i, lam in enumerate(ps):
        for j in range(i, len(ps)):
            mu = ps[j]
            for k in range(j, len(ps)):
                nu = ps[k]
                out.append((lam, mu, nu))
    return out


def vanishing_table(d: int) -> Dict[Tuple[Partition, Partition, Partition], Tuple[int, bool, bool]]:
    """Mappa ogni terna NON ordinata (lam<=mu<=nu) -> (g, V=[g==0], V_pred).

    Usa la simmetria totale di g(lam,mu,nu): basta enumerare le terne con indici
    crescenti.  V_pred usa il predittore-lab (v_pred, 2 NC solide)."""
    table: Dict[Tuple[Partition, Partition, Partition], Tuple[int, bool, bool]] = {}
    for lam, mu, nu in _triples(d):
        g = kronecker(lam, mu, nu)
        table[(lam, mu, nu)] = (g, g == 0, v_pred(lam, mu, nu))
    return table


def mismatches(d: int) -> List[Tuple[Partition, Partition, Partition]]:
    """Terne dove V (vanishing osservato) != V_pred (vanishing predetto)."""
    return [t for t, (g, v, vp) in vanishing_table(d).items() if v != vp]


def sporadic_vanishing(d: int) -> List[Tuple[Partition, Partition, Partition]]:
    """IL KILLER: terne con g == 0 ma TUTTE le NC del predittore soddisfatte
    (V True, V_pred False).  Se non vuoto, l'ipotesi-lab e' FALSIFICATA su quel d:
    esiste vanishing SPORADICO non spiegato dalle NC note."""
    return [
        t
        for t, (g, v, vp) in vanishing_table(d).items()
        if v and not vp
    ]


def nc_false_positive(d: int) -> List[Tuple[Partition, Partition, Partition]]:
    """Terne con g > 0 ma il predittore dichiara impossibile (V False, V_pred True).
    Questo significherebbe che una NC inclusa NON e' una vera condizione necessaria
    (= bug nella NC / nella sua implementazione), da escludere prima di leggere il killer.
    """
    return [
        t
        for t, (g, v, vp) in vanishing_table(d).items()
        if (not v) and vp
    ]


def honesty_note() -> str:
    return (
        "Honesty boundary: exact finite computation of Kronecker coefficients on "
        "partitions of d, compared against a predictor of KNOWN necessary conditions "
        "for non-vanishing (Dvir length-/max-part bounds). A non-empty "
        "sporadic_vanishing only falsifies the lab-hypothesis that vanishing collapses "
        "into those NCs on that d; it is NOT a statement about Kronecker positivity, "
        "GCT obstructions, or P vs NP."
    )
