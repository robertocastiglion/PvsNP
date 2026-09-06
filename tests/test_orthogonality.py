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
from pnp_lab.gct_kronecker.orthogonality import (
    column_orthogonality_check,
    row_orthogonality_check,
    dim_degeneracy_blocks,
    spurious_group_size,
)
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


# ===========================================================================
# (d) Ortogonalita' di RIGA per d=3..6 (fast) e d=7 (slow)
# ===========================================================================

class TestRowOrthogonalityFast:
    """Verifica row_orthogonality_check su d=3,4,5,6 — tutti devono passare."""

    @pytest.mark.parametrize("d", [3, 4, 5, 6])
    def test_row_orthogonality(self, d: int):
        """Ortogonalita' di riga per S_d: sum_{alpha} |C_alpha| chi^lam(a) chi^rho(a) = d!*d_{lr}."""
        result = row_orthogonality_check(d)
        assert result.all_pass, (
            f"d={d}: {len(result.violations)} violazioni\n"
            + "\n".join(
                f"  lam={v.lam}, rho={v.rho}, atteso={v.expected}, ottenuto={v.obtained}"
                for v in result.violations[:5]
            )
        )


class TestRowOrthogonalitySlow:
    """Verifica row_orthogonality_check su d=7 — marcato slow."""

    @pytest.mark.slow
    @pytest.mark.timeout(300)
    def test_row_orthogonality_d7(self):
        """Ortogonalita' di riga per S_7."""
        result = row_orthogonality_check(7)
        assert result.all_pass, (
            f"d=7: {len(result.violations)} violazioni\n"
            + "\n".join(
                f"  lam={v.lam}, rho={v.rho}, atteso={v.expected}, ottenuto={v.obtained}"
                for v in result.violations[:5]
            )
        )


# ===========================================================================
# (e) REGRESSIONE: spurious_group_size — il killer del ciclo Entry 76
#
# Il sistema [col-orto + riga-orto + ancoraggio hook-length dim] NON e' caratterizzante
# per la tavola dei caratteri di S_d. Il gruppo spurio residuo (permutazioni di righe
# interne ai blocchi dim-degeneri) sopravvive a tutti e tre i vincoli.
# Conteggi MISURATI dall'explorer: |gruppo| = 2, 4, 8, 192 per d = 3, 4, 5, 6.
# ===========================================================================

class TestSpuriousGroup:
    """Regressione sui conteggi del gruppo spurio misurati dall'explorer (Entry 76)."""

    @pytest.mark.parametrize("d,expected_size", [
        (3, 2),
        (4, 4),
        (5, 8),
        (6, 192),
    ])
    def test_spurious_group_size(self, d: int, expected_size: int):
        """spurious_group_size(d) deve coincidere con il valore misurato dall'explorer."""
        size = spurious_group_size(d)
        assert size == expected_size, (
            f"d={d}: spurious_group_size={size}, atteso={expected_size}\n"
            f"Blocchi degeneri: {dim_degeneracy_blocks(d)}"
        )

    @pytest.mark.parametrize("d", [3, 4, 5, 6])
    def test_spurious_group_nontrivial(self, d: int):
        """Il gruppo spurio e' sempre non banale (> 1) per d >= 3: la circolarita' NON e' chiusa."""
        size = spurious_group_size(d)
        assert size > 1, (
            f"d={d}: gruppo spurio banale (size={size}), ma ci aspettiamo > 1"
        )
