"""Approximate degree ESATTO via dualita' LP (il dual polynomial), su istanze minuscole.

Formulazione (EN-first honesty boundary in fondo).  L'errore di miglior approssimazione di
grado <= d,

    E_d(f) = min_{deg(p)<=d}  max_x |p(x) - f(x)| ,

ha per dualita' LP la forma del DUAL POLYNOMIAL (origin-feasible, quindi adatta al simplesso
primale razionale `_simplex_max` di exactness_composes.gap):

    E_d(f) = max_psi  sum_x psi(x) f(x)
             s.t.     sum_x |psi(x)| <= 1
                      sum_x psi(x) chi_S(x) = 0   per ogni monomio |S| <= d   (psi ⟂ gradi bassi)

Spezzando psi = psi+ - psi- (entrambi >= 0): l'origine psi=0 e' ammissibile (obiettivo 0,
vincoli 0<=0 e 0<=1), tutti i b >= 0.  Poi

    adeg_eps(f) = min { d : E_d(f) <= eps } ,   eps = 1/3 di default.

Tutto in aritmetica esatta (Fraction).  E_d decresce in d, E_n(f) = 0 (il grado pieno
interpola), quindi adeg(f) <= n.  Nessun float, nessun claim P vs NP.
"""

from __future__ import annotations

from fractions import Fraction
from typing import Dict, List, Sequence, Tuple

from pnp_lab.exactness_composes.gap import _simplex_max


def chi(s_mask: int, x: int) -> int:
    """Monomio multilineare nella base {0,1}: chi_S(x) = prod_{i in S} x_i = 1 sse S
    e' contenuto nel supporto di x (i bit di S sono tutti accesi in x)."""
    return 1 if (x & s_mask) == s_mask else 0


def monomial_masks(n: int, d: int) -> List[int]:
    """Tutte le maschere dei sottoinsiemi S di [n] con |S| <= d (i monomi di grado <= d)."""
    return [m for m in range(1 << n) if bin(m).count("1") <= d]


def error_degree_d(tt: int, n: int, d: int) -> Fraction:
    """E_d(f) ESATTO via il dual polynomial LP, per la funzione data dalla tavola di verita'
    intera ``tt`` (bit x = f(x)).  Variabili: psi+_x, psi-_x per ogni x in [0, 2^n).
    Ritorna il valore ottimo (Fraction)."""
    N = 1 << n
    f = [(tt >> x) & 1 for x in range(N)]
    # variabili: [psi+_0..psi+_{N-1}, psi-_0..psi-_{N-1}]
    nvar = 2 * N
    # obiettivo: max sum_x (psi+_x - psi-_x) f(x)
    c = [Fraction(f[x]) for x in range(N)] + [Fraction(-f[x]) for x in range(N)]
    A: List[List[Fraction]] = []
    b: List[Fraction] = []
    # vincolo di norma: sum (psi+ + psi-) <= 1
    A.append([Fraction(1)] * nvar)
    b.append(Fraction(1))
    # ortogonalita' ai monomi di grado <= d: sum_x (psi+_x - psi-_x) chi_S(x) = 0
    for s_mask in monomial_masks(n, d):
        coeff = [Fraction(chi(s_mask, x)) for x in range(N)]
        row_pos = coeff + [-cc for cc in coeff]          # <= 0
        A.append(row_pos)
        b.append(Fraction(0))
        A.append([-v for v in row_pos])                   # >= 0  (cioe' -(...) <= 0)
        b.append(Fraction(0))
    return _simplex_max(A, b, c)


def approx_degree(tt: int, n: int, eps: Fraction = Fraction(1, 3)) -> int:
    """adeg_eps(f) ESATTO: il piu' piccolo grado d con E_d(f) <= eps.  Sempre <= n."""
    for d in range(n + 1):
        if error_degree_d(tt, n, d) <= eps:
            return d
    return n


def adeg_table(n: int, eps: Fraction = Fraction(1, 3)) -> Dict[int, int]:
    """adeg esatto di OGNI funzione su n variabili (esaustivo: 2^(2^n) funzioni).
    Fattibile per n <= 3 (256 funzioni)."""
    return {tt: approx_degree(tt, n, eps) for tt in range(1 << (1 << n))}


def adeg_vs_cost(n: int, eps: Fraction = Fraction(1, 3)) -> Tuple[Dict[int, set], bool, bool]:
    """Il test della 6a arena: adeg e' un discriminante NUOVO o ricostruibile dal dizionario
    sigma(cost) (Modulo 6)?  Ritorna:
      * cost_to_adegs: per ogni valore di cost, l'insieme dei valori adeg che vi cadono;
      * adeg_refines_cost: adeg e' COSTANTE su ogni classe di cost (⇒ ricostruibile da cost);
      * cost_refines_adeg: cost e' costante su ogni classe di adeg.
    Se adeg_refines_cost ⇒ adeg = funzione di cost (collasso nel dizionario)."""
    from pnp_lab.meta_complexity.mcsp import complexity_map
    ct = complexity_map(n)
    adeg = adeg_table(n, eps)
    cost_to_adegs: Dict[int, set] = {}
    adeg_to_costs: Dict[int, set] = {}
    for tt in range(1 << (1 << n)):
        cst = ct.cost[tt]
        cost_to_adegs.setdefault(cst, set()).add(adeg[tt])
        adeg_to_costs.setdefault(adeg[tt], set()).add(cst)
    adeg_refines_cost = all(len(v) == 1 for v in cost_to_adegs.values())
    cost_refines_adeg = all(len(v) == 1 for v in adeg_to_costs.values())
    return cost_to_adegs, adeg_refines_cost, cost_refines_adeg


def adeg_vs_dictionary(n: int, eps: Fraction = Fraction(1, 3)) -> Tuple[bool, List[tuple]]:
    """Il reduce-to-known DECISIVO: adeg e' ricostruibile dal dizionario congiunto di
    invarianti d'orbita gia' nel lab — (cost del Modulo 6, gf2_degree, sensitivity,
    block_sensitivity di strata_graph)?  Ritorna (reconstructible, splits): reconstructible
    e' True sse ogni firma del dizionario congiunto mappa a UN SOLO valore di adeg (cioe'
    adeg NON separa nessuna coppia su cui i quattro invarianti concordano).  Su n=3:
    reconstructible=True, splits=[] ⇒ adeg collassa nel dizionario (RESTATEMENT)."""
    from collections import defaultdict
    from pnp_lab.meta_complexity.mcsp import complexity_map
    from pnp_lab.meta_complexity import strata_graph as sg
    ct = complexity_map(n)
    sig: Dict[tuple, set] = defaultdict(set)
    for tt in range(1 << (1 << n)):
        key = (ct.cost[tt], sg.gf2_degree(tt, n), sg.sensitivity(tt, n),
               sg.block_sensitivity(tt, n))
        sig[key].add(approx_degree(tt, n, eps))
    splits = [(k, sorted(v)) for k, v in sig.items() if len(v) > 1]
    return len(splits) == 0, splits


def honesty_note() -> str:
    return (
        "COMPUTED exactly (rational LP, Fraction): the approximate degree adeg_{1/3}(f) of "
        "every function on n<=3 variables, via the dual-polynomial LP solved by the exact "
        "rational simplex of exactness_composes.gap.  CITED, never re-proved: the polynomial "
        "method / quantum-query lower bounds and Paturi's symmetric-function formula.  This "
        "tests whether adeg is new content on tiny instances or collapses to the sigma(cost) "
        "dictionary.  No separation, no P vs NP claim."
    )
