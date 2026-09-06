"""Verifica dell'ortogonalita' di colonna della tavola dei caratteri di S_d.

Relazione di ortogonalita' di colonna (Teoria dei Caratteri, ZZ esatto):

    sum_{lambda |- d}  chi^lam(alpha) * chi^lam(beta)  =  z_alpha * delta_{alpha, beta}

dove z_alpha = prod_i (i^{m_i} * m_i!) e' il fattore di centralizzatore.

Usa esclusivamente chi3 (Frobenius alternante, engine3.py) — mai g3, mai g_fast.
L'ortogonalita' e' verificata con uguaglianza INTERA esatta, senza tolleranza float.

Funzioni esportate
------------------
column_orthogonality_check(d)  -> OrthogonalityResult
"""

from __future__ import annotations

from typing import List, NamedTuple

from pnp_lab.gct_kronecker.engine3 import chi3, _partitions3, _z_alpha3


# ---------------------------------------------------------------------------
# Tipi risultato
# ---------------------------------------------------------------------------

class Violation(NamedTuple):
    """Una violazione dell'ortogonalita' per la coppia (alpha, beta)."""
    alpha: tuple
    beta: tuple
    expected: int   # z_alpha se alpha==beta, 0 altrimenti
    obtained: int   # valore effettivo di sum_lam chi^lam(alpha)*chi^lam(beta)


class OrthogonalityResult(NamedTuple):
    """Risultato dell'ispezione di colonna per un dato d."""
    d: int
    num_classes: int      # numero di classi di coniugio = p(d)
    num_pairs_checked: int  # numero di coppie (alpha, beta) verificate (con alpha <= beta)
    all_pass: bool        # True sse nessuna violazione
    violations: List[Violation]  # lista vuota se all_pass


# ---------------------------------------------------------------------------
# Implementazione principale
# ---------------------------------------------------------------------------

def column_orthogonality_check(d: int) -> OrthogonalityResult:
    """Verifica l'ortogonalita' di colonna della tavola dei caratteri di S_d.

    Itera su tutte le coppie (alpha, beta) di partizioni di d (con indice alpha <= beta
    per evitare la doppia conta; per simmetria del prodotto basta verificare meta').
    Per ogni coppia calcola:
        S(alpha, beta) = sum_{lam |- d} chi3(lam, alpha) * chi3(lam, beta)
    e verifica:
        S(alpha, beta) == z_alpha   se alpha == beta
        S(alpha, beta) == 0         altrimenti

    Aritmetica intera pura (int Python), nessuna tolleranza float.

    Parametri
    ---------
    d : grado del gruppo simmetrico S_d

    Ritorna
    -------
    OrthogonalityResult con campi d, num_classes, num_pairs_checked, all_pass, violations.
    """
    partitions = _partitions3(d)
    num_classes = len(partitions)

    # Pre-calcola la colonna di caratteri per ogni alpha:
    # chi_col[alpha] = [chi3(lam, alpha) for lam in partitions]
    # Questo evita di ricalcolare chi3(lam, alpha) per ogni coppia.
    chi_col = {}
    for alpha in partitions:
        chi_col[alpha] = [chi3(lam, alpha) for lam in partitions]

    violations: List[Violation] = []
    num_pairs = 0

    for i, alpha in enumerate(partitions):
        z_a = _z_alpha3(alpha)
        col_alpha = chi_col[alpha]

        for j in range(i, len(partitions)):
            beta = partitions[j]
            col_beta = chi_col[beta]
            num_pairs += 1

            # Prodotto scalare esatto su ZZ
            total = sum(ca * cb for ca, cb in zip(col_alpha, col_beta))

            if alpha == beta:
                expected = z_a
            else:
                expected = 0

            if total != expected:
                violations.append(Violation(
                    alpha=alpha,
                    beta=beta,
                    expected=expected,
                    obtained=total,
                ))

    return OrthogonalityResult(
        d=d,
        num_classes=num_classes,
        num_pairs_checked=num_pairs,
        all_pass=(len(violations) == 0),
        violations=violations,
    )
