"""Terzo engine INDIPENDENTE per i caratteri di S_d e i coefficienti di Kronecker.

Algoritmo: FORMULA DI FROBENIUS via polinomi alternanti simbolici in ZZ[x_1,...,x_n].
Completamente indipendente da Murnaghan-Nakayama (usato da kronecker.py e fast.py).
NON importa character_table, mn_character, _border_strips da fast.py/kronecker.py.

Principio matematico
--------------------
Dato il gruppo simmetrico S_d con partizioni lam, alpha di d:

  prod_{k in parts(alpha)} p_k(x)  *  a_delta(x)
  = sum_{nu: partizione di d}  chi^nu(alpha)  *  a_{nu+delta}(x)

dove:
  - p_k(x) = x_1^k + ... + x_n^k    (polinomio potenza in n variabili simboliche)
  - a_nu(x) = sum_{sigma in S_n} sgn(sigma) * x^{sigma(nu)}  (alternatore di Weyl)
  - delta = (n-1, n-2, ..., 1, 0)    (vettore staircase con n=ell(lam))
  - chi^nu(alpha) = carattere dell'irriducibile S^nu sulla classe di ciclo-tipo alpha

Leggendo il coefficiente di a_{lam+delta} nel prodotto si ottiene chi^lam(alpha).

Rappresentazione interna
------------------------
I polinomi alternanti sono rapprentati come dict {esponente_dominante: coefficiente_intero}
dove l'esponente dominante e' la tupla (e_0 >= e_1 >= ... >= e_{n-1} >= 0, tutti distinti).
Un singolo alternatore a_nu corrisponde a una singola voce {nu: 1}.
Operazioni su ZZ (int puro, nessun Fraction, nessun float).

Complessita'
-----------
Numero di termini nel dict <= p(d, n parti) <= p(d).
Ogni moltiplicazione per p_k: O(n * |dict|).
chi^lam(alpha): O(len(alpha) * n * p(d)).
g3(lam,mu,nu):  O(p(d) * 3 * max_len * n_max * p(d)).

Velocita' empirica su Windows/Python 3.12:
  d=10 (n<=4): < 0.1 s
  d=15 (n<=5): ~0.5 s
  d=21 (n=6 staircase): ~15 s   [marcato slow]
  d=21 (n=9 self-conj): ~36 s   [marcato slow]

Onesta': questo engine e' indipendente da MN, ma usa la stessa formula matematica
(Frobenius) di partenza. L'indipendenza e' IMPLEMENTATIVA (algoritmo diverso),
non concettuale: entrambi calcolano chi^lam(alpha) in ZZ esatto.
"""

from __future__ import annotations

import sys
from collections import Counter
from math import factorial
from typing import Dict, List, Tuple

# Tipo alias
Partition = Tuple[int, ...]
# Polinomio alternante: esponente dominante (decrescente, distinto) -> coefficiente int
AltPoly = Dict[Tuple[int, ...], int]

# ---------------------------------------------------------------------------
# Utilita' sulle partizioni (reimplementate, senza importare da kronecker.py)
# ---------------------------------------------------------------------------

def _partitions3(d: int) -> List[Partition]:
    """Tutte le partizioni di d in ordine decrescente lessicografico."""
    out: List[Partition] = []

    def rec(rem: int, cap: int, acc: List[int]) -> None:
        if rem == 0:
            out.append(tuple(acc))
            return
        for p in range(min(rem, cap), 0, -1):
            acc.append(p)
            rec(rem - p, p, acc)
            acc.pop()

    rec(d, d, [])
    return out


def _z_alpha3(alpha: Partition) -> int:
    """z_alpha = prod_i (i^{m_i} * m_i!) — fattore di normalizzazione della classe."""
    m = Counter(alpha)
    z = 1
    for i, mi in m.items():
        z *= (i ** mi) * factorial(mi)
    return z


# ---------------------------------------------------------------------------
# Operazioni sull'anello dei polinomi alternanti in ZZ[x_1,...,x_n]
# ---------------------------------------------------------------------------

def _alt_init(n: int) -> AltPoly:
    """Polinomio alternante iniziale: a_delta con delta=(n-1,...,1,0).

    Nel dizionario alternante: {(n-1, n-2, ..., 1, 0): 1}.
    """
    delta = tuple(range(n - 1, -1, -1))
    return {delta: 1}


def _reduce_to_dominant(exp: List[int], n: int) -> Tuple[Tuple[int, ...], int]:
    """Data una lista di esponenti (non necessariamente ordinata), restituisce
    la forma dominante (decrescente) e il segno della permutazione che la produce.

    Se due esponenti sono uguali (la strip e' degenere), ritorna (None, 0).
    """
    # Controllo duplicati rapido
    if len(set(exp)) < n:
        return ((), 0)  # type: ignore[return-value]

    exp_sorted = sorted(exp, reverse=True)
    # Calcola il segno con selection-sort
    sgn = 1
    work = exp[:]
    for a in range(n):
        if work[a] != exp_sorted[a]:
            # Trova exp_sorted[a] in work[a+1:]
            j = work.index(exp_sorted[a], a + 1)
            work[a], work[j] = work[j], work[a]
            sgn *= -1
    return tuple(exp_sorted), sgn


def _mul_p_sym(poly: AltPoly, n: int, k: int) -> AltPoly:
    """Moltiplica il polinomio alternante `poly` per p_k = x_1^k + ... + x_n^k.

    Per ogni monomio alternante (exp, c) e ogni variabile i in [0, n):
      - Aggiunge k alla componente i dell'esponente
      - Riduce alla forma dominante (con segno)
      - Accumula nel nuovo dizionario

    Termini con esponenti duplicati (contributo zero) vengono scartati.
    Termini con coefficiente finale zero vengono rimossi.
    """
    new_poly: AltPoly = {}
    for exp, c in poly.items():
        for i in range(n):
            new_exp = list(exp)
            new_exp[i] += k
            dominant, sgn = _reduce_to_dominant(new_exp, n)
            if sgn == 0:
                continue
            val = sgn * c
            prev = new_poly.get(dominant, 0)
            result = prev + val
            if result == 0:
                new_poly.pop(dominant, None)
            else:
                new_poly[dominant] = result
    return new_poly


# ---------------------------------------------------------------------------
# chi3: calcolo del carattere via formula di Frobenius
# ---------------------------------------------------------------------------

def chi3(lam: Partition, alpha: Partition) -> int:
    """Carattere chi^lam(alpha) via formula di Frobenius (alternanti simbolici).

    Moltiplica a_delta per prod_{k in alpha} p_k  nell'anello alternante
    in n = ell(lam) variabili simboliche, poi legge il coefficiente di a_{lam+delta}.

    Algoritmo completamente indipendente da Murnaghan-Nakayama.

    Parametri
    ---------
    lam   : partizione di d (parti decrescenti, non vuota)
    alpha : partizione di d (tipo-ciclo della classe di coniugio)

    Ritorna
    -------
    chi^lam(alpha)  (intero esatto, puo' essere negativo)
    """
    d = sum(lam)
    if sum(alpha) != d:
        raise ValueError(
            f"lam e alpha devono partizionare lo stesso d; "
            f"sum(lam)={d}, sum(alpha)={sum(alpha)}"
        )
    if not lam:
        # lam=() e alpha=(): carattere della rappresentazione banale di S_0
        return 1

    n = len(lam)
    delta = tuple(range(n - 1, -1, -1))
    # Vettore target: lam + delta componente per componente
    target = tuple(lam[i] + delta[i] for i in range(n))

    # Inizia da a_delta e moltiplica per p_{alpha_k} per ogni parte alpha_k
    poly: AltPoly = _alt_init(n)
    for k in alpha:
        poly = _mul_p_sym(poly, n, k)

    return poly.get(target, 0)


# ---------------------------------------------------------------------------
# g3: coefficiente di Kronecker via formula del prodotto triplo di caratteri
# ---------------------------------------------------------------------------

def g3(lam: Partition, mu: Partition, nu: Partition) -> int:
    """Coefficiente di Kronecker g(lam, mu, nu) via engine Frobenius indipendente.

    Formula:
        g = (1/d!) * sum_{alpha |- d}  |C_alpha| * chi^lam(alpha) * chi^mu(alpha) * chi^nu(alpha)

    dove |C_alpha| = d! / z_alpha  (dimensione della classe di coniugio alpha).
    Ogni chi viene calcolato da chi3() (Frobenius, indipendente da MN).
    Aritmetica intera pura; verifica che il numeratore sia divisibile per d! esatto.

    Complessita'
    -----------
    O(p(d) * [chi3(lam,...) + chi3(mu,...) + chi3(nu,...)])
    Per d=15: ~0.5 s. Per d=21 con ell(lam)=6: ~15 s. Vedi modulo per dettagli.
    """
    d = sum(lam)
    if sum(mu) != d or sum(nu) != d:
        raise ValueError(
            f"lam, mu, nu devono partizionare lo stesso d; "
            f"sum(lam)={d}, sum(mu)={sum(mu)}, sum(nu)={sum(nu)}"
        )

    d_fact = factorial(d)
    ps = _partitions3(d)

    num = 0
    for alpha in ps:
        za = _z_alpha3(alpha)
        class_size = d_fact // za            # intero esatto
        cl = chi3(lam, alpha)
        cm = chi3(mu, alpha)
        cn = chi3(nu, alpha)
        num += class_size * cl * cm * cn

    if num % d_fact != 0:
        raise AssertionError(
            f"g3: numeratore {num} non divisibile per d!={d_fact} "
            f"su lam={lam}, mu={mu}, nu={nu}"
        )
    return num // d_fact


if __name__ == "__main__":
    # Demo rapida con stdout utf-8 (sicuro su Windows/cp1252)
    sys.stdout.reconfigure(encoding="utf-8")
    print("engine3.py — terzo engine indipendente (Frobenius alternante)")
    print(f"  chi3((2,1),(1,1,1)) = {chi3((2,1),(1,1,1))}  (atteso 2)")
    print(f"  g3((2,1),(2,1),(2,1)) = {g3((2,1),(2,1),(2,1))}  (atteso 1)")
    print(f"  g3((4,3,2,1)^3) = {g3((4,3,2,1),(4,3,2,1),(4,3,2,1))}  (atteso 117)")
