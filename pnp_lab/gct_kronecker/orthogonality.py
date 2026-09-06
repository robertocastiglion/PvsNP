"""Verifica dell'ortogonalita' di colonna E di riga della tavola dei caratteri di S_d.
Analisi dei blocchi degeneri per dimension di hook-length e del gruppo spurio residuo.

Relazione di ortogonalita' di colonna (Teoria dei Caratteri, ZZ esatto):

    sum_{lambda |- d}  chi^lam(alpha) * chi^lam(beta)  =  z_alpha * delta_{alpha, beta}

Relazione di ortogonalita' di riga (seconda formula di ortogonalita'):

    sum_{alpha |- d}  (1/z_alpha) * chi^lam(alpha) * chi^rho(alpha)  =  delta_{lam, rho}

equivalente (moltiplicata per d!) a:

    sum_{alpha |- d}  (d!/z_alpha) * chi^lam(alpha) * chi^rho(alpha)  =  d! * delta_{lam, rho}

dove d!/z_alpha = |C_alpha| e' la dimensione della classe di coniugio di tipo alpha.

Usa esclusivamente chi3 (Frobenius alternante, engine3.py) per i caratteri;
hook_length_dimension da kronecker.py (formula degli hook, indipendente da chi3/MN)
per il raggruppamento in blocchi degeneri.

Funzioni esportate
------------------
column_orthogonality_check(d)   -> OrthogonalityResult
row_orthogonality_check(d)      -> RowOrthogonalityResult
dim_degeneracy_blocks(d)        -> List[List[Partition]]  (solo blocchi di taglia >= 2)
spurious_group_size(d)          -> int  (prodotto di len(blocco)! sui blocchi degeneri)
"""

from __future__ import annotations

from math import factorial
from typing import Dict, List, NamedTuple, Tuple

from pnp_lab.gct_kronecker.engine3 import chi3, _partitions3, _z_alpha3
from pnp_lab.gct_kronecker.kronecker import hook_length_dimension

Partition = Tuple[int, ...]


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


class RowViolation(NamedTuple):
    """Una violazione dell'ortogonalita' di riga per la coppia (lam, rho)."""
    lam: tuple
    rho: tuple
    expected: int   # d! se lam==rho, 0 altrimenti (dopo moltiplicazione per d!)
    obtained: int   # sum_{alpha} |C_alpha| * chi^lam(alpha) * chi^rho(alpha)


class RowOrthogonalityResult(NamedTuple):
    """Risultato dell'ispezione di riga per un dato d."""
    d: int
    num_irreps: int         # numero di irriducibili = p(d)
    num_pairs_checked: int  # coppie (lam, rho) con indice lam <= rho
    all_pass: bool
    violations: List[RowViolation]


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


# ---------------------------------------------------------------------------
# Ortogonalita' di riga
# ---------------------------------------------------------------------------

def row_orthogonality_check(d: int) -> RowOrthogonalityResult:
    """Verifica l'ortogonalita' di riga della tavola dei caratteri di S_d.

    Per ogni coppia (lam, rho) di partizioni di d calcola (aritmetica INTERA):

        S(lam, rho) = sum_{alpha |- d}  |C_alpha| * chi3(lam, alpha) * chi3(rho, alpha)

    dove |C_alpha| = d! / z_alpha e' la dimensione della classe di coniugio.
    Verifica:
        S(lam, rho) == d!   se lam == rho
        S(lam, rho) == 0    altrimenti

    Moltiplica per d! per restare su ZZ esatto (evita Fraction).
    Itera solo su coppie con indice lam <= rho (simmetria).

    Parametri
    ---------
    d : grado del gruppo simmetrico S_d

    Ritorna
    -------
    RowOrthogonalityResult con campi d, num_irreps, num_pairs_checked, all_pass, violations.
    """
    parts = _partitions3(d)
    d_fact = factorial(d)

    # Pre-calcola la riga di caratteri per ogni lam:
    # chi_row[lam] = [chi3(lam, alpha) for alpha in parts]
    chi_row: Dict[Partition, List[int]] = {}
    for lam in parts:
        chi_row[lam] = [chi3(lam, alpha) for alpha in parts]

    # Pre-calcola i pesi |C_alpha| = d! / z_alpha (interi esatti)
    class_sizes = [d_fact // _z_alpha3(alpha) for alpha in parts]

    violations: List[RowViolation] = []
    num_pairs = 0

    for i, lam in enumerate(parts):
        row_lam = chi_row[lam]
        for j in range(i, len(parts)):
            rho = parts[j]
            row_rho = chi_row[rho]
            num_pairs += 1

            # Prodotto scalare pesato su ZZ
            total = sum(cs * cl * cr for cs, cl, cr in zip(class_sizes, row_lam, row_rho))

            expected = d_fact if lam == rho else 0

            if total != expected:
                violations.append(RowViolation(
                    lam=lam,
                    rho=rho,
                    expected=expected,
                    obtained=total,
                ))

    return RowOrthogonalityResult(
        d=d,
        num_irreps=len(parts),
        num_pairs_checked=num_pairs,
        all_pass=(len(violations) == 0),
        violations=violations,
    )


# ---------------------------------------------------------------------------
# Blocchi degeneri per hook-length dim e gruppo spurio
# ---------------------------------------------------------------------------

def dim_degeneracy_blocks(d: int) -> List[List[Partition]]:
    """Blocchi di partizioni di d con la stessa hook-length dimension (solo blocchi >= 2).

    Raggruppa le partizioni lam |- d per valore di hook_length_dimension(lam).
    Restituisce solo i blocchi di taglia >= 2 (i blocchi degeneri), ciascuno come lista
    di partizioni. I blocchi di taglia 1 (dim unica) NON sono inclusi.

    Usa hook_length_dimension da kronecker.py (formula del prodotto degli hook,
    completamente esterna a chi3 e a MN).

    Parametri
    ---------
    d : grado del gruppo simmetrico S_d

    Ritorna
    -------
    Lista di blocchi degeneri, ciascuno una lista di Partition.
    """
    parts = _partitions3(d)
    # Raggruppa per valore di dimensione
    by_dim: Dict[int, List[Partition]] = {}
    for lam in parts:
        dim = hook_length_dimension(lam)
        if dim not in by_dim:
            by_dim[dim] = []
        by_dim[dim].append(lam)

    # Restituisce solo i blocchi di taglia >= 2
    return [block for block in by_dim.values() if len(block) >= 2]


def spurious_group_size(d: int) -> int:
    """Taglia del gruppo di permutazioni di righe spurie che sopravvivono ai tre vincoli.

    I tre vincoli sono: ortogonalita' di colonna + ortogonalita' di riga + ancoraggio
    hook-length dim (dim > 0). Le permutazioni di righe INTERNE ai blocchi a dim-degenere
    preservano tutti e tre i vincoli, generando un gruppo spurio.

    Il gruppo spurio = prodotto diretto dei gruppi simmetrici sui blocchi degeneri.
    Taglia = prod_{blocco degenero} len(blocco)!

    Include l'identita'. Se non ci sono blocchi degeneri, ritorna 1.

    Parametri
    ---------
    d : grado del gruppo simmetrico S_d

    Ritorna
    -------
    int: |gruppo spurio| = prod_blocco len(blocco)!
    """
    blocks = dim_degeneracy_blocks(d)
    result = 1
    for block in blocks:
        result *= factorial(len(block))
    return result
