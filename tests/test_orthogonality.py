"""Test dell'ortogonalita' di colonna per la tavola dei caratteri di S_d.

Verifica che chi3 soddisfi la relazione esatta:
    sum_{lambda |- d} chi^lam(alpha) * chi^lam(beta) = z_alpha * delta_{alpha, beta}

per ogni coppia di classi (alpha, beta) partizioni di d.

Questo test e' genuinamente indipendente dalla formula g: usa solo chi3 (Frobenius),
mai g3/g_fast. La relazione di ortogonalita' e' una proprieta' fondamentale della
tavola dei caratteri — se chi3 la soddisfa su ogni coppia, non e' un artefatto della
formula g condivisa.

Struttura:
  (a) test manuali su coppie note per d=3 (diagonale e off-diagonale)
  (b) test esaurienti su d=2,3,4,5,6  (fast)
  (c) test slow su d=7,8
"""

from __future__ import annotations

import pytest
from pnp_lab.gct_kronecker.orthogonality import column_orthogonality_check
from pnp_lab.gct_kronecker.engine3 import chi3, _partitions3, _z_alpha3


# ===========================================================================
# (a) Casi noti a mano per d=3
# ===========================================================================

class TestManualD3:
    """Verifica manuale dell'ortogonalita' di colonna per S_3.

    Partizioni di 3: (3,), (2,1), (1,1,1).
    z_{(3,)} = 3^1 * 1! = 3
    z_{(2,1)} = 2^1 * 1! * 1^1 * 1! = 2
    z_{(1,1,1)} = 1^3 * 3! = 6
    """

    def test_diagonal_alpha_3(self):
        """sum_lam chi^lam((3,))^2 == z_{(3,)} == 3."""
        d = 3
        alpha = (3,)
        partitions = _partitions3(d)
        total = sum(chi3(lam, alpha) ** 2 for lam in partitions)
        assert total == _z_alpha3(alpha), (
            f"Diagonale alpha={alpha}: atteso {_z_alpha3(alpha)}, ottenuto {total}"
        )

    def test_diagonal_alpha_21(self):
        """sum_lam chi^lam((2,1))^2 == z_{(2,1)} == 2."""
        d = 3
        alpha = (2, 1)
        partitions = _partitions3(d)
        total = sum(chi3(lam, alpha) ** 2 for lam in partitions)
        assert total == _z_alpha3(alpha), (
            f"Diagonale alpha={alpha}: atteso {_z_alpha3(alpha)}, ottenuto {total}"
        )

    def test_diagonal_alpha_111(self):
        """sum_lam chi^lam((1,1,1))^2 == z_{(1,1,1)} == 6."""
        d = 3
        alpha = (1, 1, 1)
        partitions = _partitions3(d)
        total = sum(chi3(lam, alpha) ** 2 for lam in partitions)
        assert total == _z_alpha3(alpha), (
            f"Diagonale alpha={alpha}: atteso {_z_alpha3(alpha)}, ottenuto {total}"
        )

    def test_offdiagonal_3_vs_21(self):
        """sum_lam chi^lam((3,)) * chi^lam((2,1)) == 0."""
        d = 3
        alpha = (3,)
        beta = (2, 1)
        partitions = _partitions3(d)
        total = sum(chi3(lam, alpha) * chi3(lam, beta) for lam in partitions)
        assert total == 0, (
            f"Off-diagonale alpha={alpha}, beta={beta}: atteso 0, ottenuto {total}"
        )

    def test_offdiagonal_3_vs_111(self):
        """sum_lam chi^lam((3,)) * chi^lam((1,1,1)) == 0."""
        d = 3
        alpha = (3,)
        beta = (1, 1, 1)
        partitions = _partitions3(d)
        total = sum(chi3(lam, alpha) * chi3(lam, beta) for lam in partitions)
        assert total == 0, (
            f"Off-diagonale alpha={alpha}, beta={beta}: atteso 0, ottenuto {total}"
        )

    def test_offdiagonal_21_vs_111(self):
        """sum_lam chi^lam((2,1)) * chi^lam((1,1,1)) == 0."""
        d = 3
        alpha = (2, 1)
        beta = (1, 1, 1)
        partitions = _partitions3(d)
        total = sum(chi3(lam, alpha) * chi3(lam, beta) for lam in partitions)
        assert total == 0, (
            f"Off-diagonale alpha={alpha}, beta={beta}: atteso 0, ottenuto {total}"
        )


# ===========================================================================
# (b) Ortogonalita' esauriente per d=2..6 (fast)
# ===========================================================================

class TestExhaustiveFast:
    """Verifica column_orthogonality_check su d=2,3,4,5,6 — tutti devono passare."""

    @pytest.mark.parametrize("d", [2, 3, 4, 5, 6])
    def test_column_orthogonality(self, d: int):
        """Ortogonalita' di colonna per S_d: tutte le coppie (alpha, beta) esatte."""
        result = column_orthogonality_check(d)
        assert result.all_pass, (
            f"d={d}: {len(result.violations)} violazioni\n"
            + "\n".join(
                f"  alpha={v.alpha}, beta={v.beta}, atteso={v.expected}, ottenuto={v.obtained}"
                for v in result.violations[:5]  # prime 5 per brevita'
            )
        )


# ===========================================================================
# (c) Ortogonalita' slow per d=7,8
# ===========================================================================

class TestExhaustiveSlow:
    """Verifica column_orthogonality_check su d=7,8 — marcati slow."""

    @pytest.mark.slow
    @pytest.mark.timeout(300)
    def test_column_orthogonality_d7(self):
        """Ortogonalita' di colonna per S_7."""
        result = column_orthogonality_check(7)
        assert result.all_pass, (
            f"d=7: {len(result.violations)} violazioni\n"
            + "\n".join(
                f"  alpha={v.alpha}, beta={v.beta}, atteso={v.expected}, ottenuto={v.obtained}"
                for v in result.violations[:5]
            )
        )

    @pytest.mark.slow
    @pytest.mark.timeout(600)
    def test_column_orthogonality_d8(self):
        """Ortogonalita' di colonna per S_8."""
        result = column_orthogonality_check(8)
        assert result.all_pass, (
            f"d=8: {len(result.violations)} violazioni\n"
            + "\n".join(
                f"  alpha={v.alpha}, beta={v.beta}, atteso={v.expected}, ottenuto={v.obtained}"
                for v in result.violations[:5]
            )
        )
