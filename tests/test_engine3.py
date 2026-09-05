"""Test del terzo engine indipendente (Frobenius alternante) per i caratteri di S_d
e i coefficienti di Kronecker.

Struttura:
  (a) chi3 vs valori noti a mano per d <= 4
  (b) g3 == g_fast su TUTTE le terne d <= 5  (esauriente, fast)
  (c) Campioni corpus d in [10,24]: valori auditati in STATE.md

I test slow sono marcati con @pytest.mark.slow e deselezionati di default.
Eseguirli con:  py -m pytest tests/test_engine3.py -m slow -v
"""

from __future__ import annotations

import pytest

# Engine indipendente (Frobenius alternante)
from pnp_lab.gct_kronecker.engine3 import chi3, g3

# Engine di riferimento (Murnaghan-Nakayama via tavola precalcolata)
from pnp_lab.gct_kronecker.fast import g_fast

# Utilita' condivise non toccano i caratteri (partitions e' banale)
from pnp_lab.gct_kronecker.kronecker import partitions, _triples


# ===========================================================================
# (a) chi3 vs valori NOTI A MANO per d <= 4
# ===========================================================================

class TestChi3ManualValues:
    """Valori del carattere chi^lam(alpha) calcolati a mano o dalla tavola di S_d."""

    # --- S_1 ---
    def test_s1_trivial(self):
        # S^(1) e' la rapprensentazione banale di S_1: chi=1 su tutto.
        assert chi3((1,), (1,)) == 1

    # --- S_2 ---
    def test_s2_trivial_on_identity(self):
        # S^(2): chi=1 su id=(1,1), chi=1 su (2)
        assert chi3((2,), (1, 1)) == 1

    def test_s2_trivial_on_transposition(self):
        assert chi3((2,), (2,)) == 1

    def test_s2_sign_on_identity(self):
        # S^(1,1) = segno: chi=1 su id, chi=-1 su (2)
        assert chi3((1, 1), (1, 1)) == 1

    def test_s2_sign_on_transposition(self):
        assert chi3((1, 1), (2,)) == -1

    # --- S_3 ---
    def test_s3_trivial(self):
        # S^(3): chi=1 su ogni classe
        assert chi3((3,), (1, 1, 1)) == 1
        assert chi3((3,), (2, 1)) == 1
        assert chi3((3,), (3,)) == 1

    def test_s3_sign(self):
        # S^(1,1,1): chi = sgn(permutazione) = 1, -1, 1 per id, (2,1), (3)
        assert chi3((1, 1, 1), (1, 1, 1)) == 1
        assert chi3((1, 1, 1), (2, 1)) == -1
        assert chi3((1, 1, 1), (3,)) == 1

    def test_s3_standard(self):
        # S^(2,1): dim=2; chi su id=2, su (2,1)=0, su (3)=-1
        assert chi3((2, 1), (1, 1, 1)) == 2
        assert chi3((2, 1), (2, 1)) == 0
        assert chi3((2, 1), (3,)) == -1

    # --- S_4 (tavola 5x5) ---
    def test_s4_trivial(self):
        # S^(4): tutti chi=1
        for alpha in [(1,1,1,1),(2,1,1),(2,2),(3,1),(4,)]:
            assert chi3((4,), alpha) == 1, f"chi3((4,),{alpha}) != 1"

    def test_s4_sign(self):
        # S^(1,1,1,1): chi = sgn = 1,-1,1,1,-1 per id,(2,1,1),(2,2),(3,1),(4,)
        expected = {
            (1,1,1,1): 1,
            (2,1,1): -1,
            (2,2): 1,
            (3,1): 1,
            (4,): -1,
        }
        for alpha, exp in expected.items():
            assert chi3((1,1,1,1), alpha) == exp, (
                f"chi3((1,1,1,1),{alpha}) = {chi3((1,1,1,1),alpha)} != {exp}"
            )

    def test_s4_standard_4cols(self):
        # S^(2,1,1): dim=3; valori dalla tavola di S_4
        # chi: id=3, (2,1,1)=-1, (2,2)=-1, (3,1)=0, (4,)=1
        # (Nota: (2,1,1) ha chi=-1, non +1 come S^(3,1))
        expected = {
            (1,1,1,1): 3,
            (2,1,1): -1,
            (2,2): -1,
            (3,1): 0,
            (4,): 1,
        }
        for alpha, exp in expected.items():
            assert chi3((2,1,1), alpha) == exp, (
                f"chi3((2,1,1),{alpha}) = {chi3((2,1,1),alpha)} != {exp}"
            )

    def test_s4_standard_3cols(self):
        # S^(2,2): dim=2; valori: id=2, (2,1,1)=0, (2,2)=2, (3,1)=-1, (4,)=0
        expected = {
            (1,1,1,1): 2,
            (2,1,1): 0,
            (2,2): 2,
            (3,1): -1,
            (4,): 0,
        }
        for alpha, exp in expected.items():
            assert chi3((2,2), alpha) == exp, (
                f"chi3((2,2),{alpha}) = {chi3((2,2),alpha)} != {exp}"
            )

    def test_s4_hook(self):
        # S^(3,1): dim=3; valori: id=3, (2,1,1)=1, (2,2)=-1, (3,1)=0, (4,)=-1
        # (Nota: (2,1,1) ha chi=+1 per S^(3,1), il contrario di S^(2,1,1))
        expected = {
            (1,1,1,1): 3,
            (2,1,1): 1,
            (2,2): -1,
            (3,1): 0,
            (4,): -1,
        }
        for alpha, exp in expected.items():
            assert chi3((3,1), alpha) == exp, (
                f"chi3((3,1),{alpha}) = {chi3((3,1),alpha)} != {exp}"
            )


# ===========================================================================
# (b) g3 == g_fast su TUTTE le terne d <= 5
# ===========================================================================

class TestG3VsGFastExhaustive:
    """Confronto esauriente g3 == g_fast per d <= 5.

    d=5: p(5)=7 partizioni, C(7+2,3)=84 terne non ordinate. Fast.
    """

    @pytest.mark.parametrize("d", [1, 2, 3, 4, 5])
    def test_all_triples(self, d: int):
        """g3 == g_fast su ogni terna non ordinata di partizioni di d."""
        triples = _triples(d)
        mismatches = []
        for lam, mu, nu in triples:
            g_ref = g_fast(lam, mu, nu)
            g_new = g3(lam, mu, nu)
            if g_ref != g_new:
                mismatches.append((lam, mu, nu, g_ref, g_new))
        if mismatches:
            lines = [
                f"  {lam},{mu},{nu}: g_fast={gr}, g3={gn}"
                for lam, mu, nu, gr, gn in mismatches
            ]
            pytest.fail(
                f"d={d}: {len(mismatches)} mismatch trovati:\n" + "\n".join(lines)
            )


# ===========================================================================
# (c) Campioni corpus STATE.md: d in [10, 24]
# ===========================================================================

class TestCorpusSamples:
    """Validazione spot-check su valori auditati del corpus STATE.md.

    Ogni test verifica g3(lam,lam,lam) == valore_corpus per un singolo campione.
    I test lenti (d>=15 o ell(lam)>=7) sono marcati slow.
    """

    # --- d=10 ---
    def test_delta4_d10(self):
        """g(delta_4^3) = 117  [STAIRCASE k=4, d=10]."""
        lam = (4, 3, 2, 1)
        assert g3(lam, lam, lam) == 117

    def test_c49_c5_d10(self):
        """g((5,5)^3) = 0  [C49 c=5 dispari, d=10]."""
        # C49: g((c^2)^3) = 0 per c dispari, 1 per c pari. c=5 e' dispari -> 0.
        lam = (5, 5)
        assert g3(lam, lam, lam) == 0

    def test_c50_c3_d9(self):
        """g((3,3,3)^3) = 1  [C50 c=3, d=9]."""
        lam = (3, 3, 3)
        assert g3(lam, lam, lam) == 1

    def test_c51_k3_d9(self):
        """g((3,3,3)^3) = 1  [C51 k=3, d=9] (stesso valore di C50 c=3)."""
        lam = (3,) * 3
        assert g3(lam, lam, lam) == 1

    # --- d=12 ---
    def test_c52_c3_d12(self):
        """g((3,3,3,3)^3) = 1  [C52/F68 c=3, d=12]."""
        lam = (3,) * 4
        assert g3(lam, lam, lam) == 1

    def test_c49_c6_d12(self):
        """g((6,6)^3) = 1  [C49 c=6 pari, d=12]."""
        lam = (6, 6)
        assert g3(lam, lam, lam) == 1

    # --- d=16 ---
    @pytest.mark.slow
    @pytest.mark.timeout(120)
    def test_c53_k4_d16(self):
        """g((4,4,4,4)^3) = 5  [C53 k=4, d=16]."""
        lam = (4,) * 4
        assert g3(lam, lam, lam) == 5

    # --- d=15 ---
    @pytest.mark.slow
    @pytest.mark.timeout(60)
    def test_delta5_d15(self):
        """g(delta_5^3) = 18269  [STAIRCASE k=5, d=15]."""
        lam = (5, 4, 3, 2, 1)
        assert g3(lam, lam, lam) == 18269

    @pytest.mark.slow
    @pytest.mark.timeout(60)
    def test_c51_k5_d15(self):
        """g((3^5)^3) = 1  [C51 k=5, d=15].

        NOTA: il corpus STATE.md dichiara 2 per questa voce, ma sia g_fast che g3
        concordano sul valore 1. L'audit.py segnala MISMATCH per C51 k=5 (pre-existing).
        Questo test usa il valore COMPUTATO (1), non quello errato del corpus.
        """
        lam = (3,) * 5
        # Verifica coerenza con g_fast (terzo engine indipendente da MN concorda)
        from pnp_lab.gct_kronecker.fast import g_fast
        assert g_fast(lam, lam, lam) == 1  # g_fast reference
        assert g3(lam, lam, lam) == 1      # engine3 Frobenius concorda

    @pytest.mark.slow
    @pytest.mark.timeout(60)
    def test_c50_c5_d15(self):
        """g((5,5,5)^3) = 1  [C50 c=5, d=15]: formula c//3 per c dispari."""
        lam = (5, 5, 5)
        assert g3(lam, lam, lam) == 1

    @pytest.mark.slow
    @pytest.mark.timeout(60)
    def test_spettro_d15_hook(self):
        """g((6,3,3,1,1,1)^3) = 2881  [SPETTRO d=15 hooks{11,3,1}]."""
        lam = (6, 3, 3, 1, 1, 1)
        assert g3(lam, lam, lam) == 2881

    @pytest.mark.slow
    @pytest.mark.timeout(60)
    def test_spettro_d15_444_3(self):
        """g((4,4,4,3)^3) = 9  [SPETTRO d=15 hooks{7,5,3}]."""
        lam = (4, 4, 4, 3)
        assert g3(lam, lam, lam) == 9

    # --- d=21 ---
    @pytest.mark.slow
    @pytest.mark.timeout(120)
    def test_delta6_d21(self):
        """g(delta_6^3) = 24891165  [STAIRCASE k=6, d=21]."""
        lam = (6, 5, 4, 3, 2, 1)
        assert g3(lam, lam, lam) == 24891165

    @pytest.mark.slow
    @pytest.mark.timeout(300)
    def test_spettro_d21_hooks_17_3_1(self):
        """g((9,3,3,1^6)^3) = 8013  [SPETTRO d=21 hooks{17,3,1}]."""
        lam = (9, 3, 3, 1, 1, 1, 1, 1, 1)
        assert g3(lam, lam, lam) == 8013

    @pytest.mark.slow
    @pytest.mark.timeout(120)
    def test_spettro_d21_hooks_11_9_1(self):
        """g((6,6,3,2,2,2)^3) = 411081  [SPETTRO d=21 hooks{11,9,1}]."""
        lam = (6, 6, 3, 2, 2, 2)
        assert g3(lam, lam, lam) == 411081

    @pytest.mark.slow
    @pytest.mark.timeout(120)
    def test_spettro_d21_555_3_3(self):
        """g((5,5,5,3,3)^3) = 5453  [SPETTRO d=21 hooks{9,7,5}]."""
        lam = (5, 5, 5, 3, 3)
        assert g3(lam, lam, lam) == 5453

    @pytest.mark.slow
    @pytest.mark.timeout(120)
    def test_c49_c10_d20(self):
        """g((10,10)^3) = 1  [C49 c=10 pari, d=20]."""
        lam = (10, 10)
        assert g3(lam, lam, lam) == 1

    @pytest.mark.slow
    @pytest.mark.timeout(60)
    def test_s3_1_via_lim(self):
        """g((10,3)^3) = 2  [approssimazione stabile di s_3(1)=2]."""
        # s_3(1) = lim_{a->inf} g((a,3)^3) = 2; stabile per a >= 7.
        lam = (10, 3)
        assert g3(lam, lam, lam) == 2

    @pytest.mark.slow
    @pytest.mark.timeout(60)
    def test_s3_2_via_lim(self):
        """g((10,3,3)^3) = 14  [approssimazione stabile di s_3(2)=14]."""
        # s_3(2) = lim_{a->inf} g((a,3,3)^3) = 14; stabile per a >= 7.
        lam = (10, 3, 3)
        assert g3(lam, lam, lam) == 14
