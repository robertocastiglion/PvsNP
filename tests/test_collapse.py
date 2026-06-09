"""Test della cristallizzazione di chiusura (Module 19 — Tiny-Instance Collapse).

Verificano in codice i fatti portanti della meta-conclusione su n=3 (veloci) e
n=4 (esaustivo, marcato slow): killer-1 (d_negation≡0), W1 (d_flip = gradiente
esatto di cost), W2 (d_flip NON canonico cost→DT-depth), e l'assenza di
falsificatore nella toolbox.
"""

import pytest

from pnp_lab.circuits import min_formula_sizes
from pnp_lab.meta_complexity.collapse import (
    collapse_summary,
    dflip_canonicity_mismatch,
    dflip_is_cost_gradient,
    dt_depth,
    falsifier_status,
    negation_is_cost_automorphism,
)


# --------------------------------------------------------------------------- #
#  Oracolo DT-depth: sanity esatto                                            #
# --------------------------------------------------------------------------- #

def test_dt_depth_constants_are_zero():
    # costante 0 (tt=0) e costante 1 (tt=0xFF su n=3) hanno profondità 0
    assert dt_depth(0, 3) == 0
    assert dt_depth(0xFF, 3) == 0


def test_dt_depth_projection_is_one():
    # x0 su n=3: tavola = bit 0 dell'indice -> DT di profondità 1
    tt = sum(1 << idx for idx in range(8) if idx & 1)
    assert dt_depth(tt, 3) == 1


def test_dt_depth_parity_is_n():
    # parity su n=3 ha profondità di albero di decisione esattamente 3
    tt = sum(1 << idx for idx in range(8) if bin(idx).count("1") % 2 == 1)
    assert dt_depth(tt, 3) == 3


# --------------------------------------------------------------------------- #
#  Killer-1: input-negation è un automorfismo del costo (d_negation ≡ 0)      #
# --------------------------------------------------------------------------- #

def test_killer1_negation_is_cost_automorphism_n3():
    ct = min_formula_sizes(3)
    assert negation_is_cost_automorphism(ct, 3) == 0


# --------------------------------------------------------------------------- #
#  W1: d_flip è il GRADIENTE esatto di cost (ricostruibile da cost solo)       #
# --------------------------------------------------------------------------- #

def test_w1_dflip_is_exact_cost_gradient_n3():
    ct = min_formula_sizes(3)
    assert dflip_is_cost_gradient(ct, 3) == 0


# --------------------------------------------------------------------------- #
#  W2: d_flip NON è canonico (cambia tra formula-size e DT-depth)              #
# --------------------------------------------------------------------------- #

def test_w2_dflip_not_canonical_n3():
    mism, total = dflip_canonicity_mismatch(3)
    assert total == 256
    # misura esatta riprodotta dall'audit del Ciclo 5: 154/256
    assert mism == 154
    assert 0 < mism < total  # non banale e non totale


# --------------------------------------------------------------------------- #
#  Falsificatore: NON trovato nella toolbox -> collasso confermato            #
# --------------------------------------------------------------------------- #

def test_no_falsifier_in_toolbox_n3():
    fs = falsifier_status(3)
    assert fs.found is False
    assert "Collasso" in fs.note or "collasso" in fs.note


# --------------------------------------------------------------------------- #
#  Sommario completo n=3                                                       #
# --------------------------------------------------------------------------- #

def test_collapse_summary_n3():
    s = collapse_summary(3)
    assert s.num_funcs == 256
    assert s.negation_nonzero == 0
    assert s.gradient_mismatch == 0
    assert s.canonicity_mismatch == 154
    assert s.falsifier_found is False


# --------------------------------------------------------------------------- #
#  n=4 esaustivo (slow)                                                       #
# --------------------------------------------------------------------------- #

@pytest.mark.slow
@pytest.mark.timeout(900)
def test_collapse_summary_n4_exhaustive():
    s = collapse_summary(4)
    assert s.num_funcs == 65536
    # killer-1 e W1 valgono ESATTI anche su n=4 (65536/65536)
    assert s.negation_nonzero == 0
    assert s.gradient_mismatch == 0
    # W2: d_flip resta non canonico su n=4 (frazione non banale)
    assert 0 < s.canonicity_mismatch < s.canonicity_total
    assert s.falsifier_found is False
