"""Test del ciclo 3 (research loop): feasible interpolation misurata sul piccolo.

Verifichiamo: (1) la refutazione DAG trova la clausola vuota sulle famiglie split;
(2) l'interpolante estratto è SEMANTICAMENTE corretto su TUTTI gli α (oracolo);
(3) i numeri attesi: #MUX = #variabili shared; interpolante ≈ interpolante minimo
(entrambi lineari) → la taglia dell'interpolante NON dipende dal numero (esplosivo)
di passi di saturazione, ma dai passi-su-shared del DAG.
"""
import pytest

from pnp_lab.feasible_interp.families import or_family, and_family
from pnp_lab.feasible_interp.interp import (
    Split, dag_refute, build_interpolant, verify_interpolant,
    min_interpolant_dt_size, eval_gate,
)
from pnp_lab.proof_complexity.formula import Clause


@pytest.mark.parametrize("fam", [or_family, and_family])
@pytest.mark.parametrize("n", [1, 2, 3, 4])
def test_split_is_well_formed(fam, n):
    fam(n).check_split()  # non solleva


@pytest.mark.parametrize("fam", [or_family, and_family])
@pytest.mark.parametrize("n", [1, 2, 3, 4])
def test_refutation_found(fam, n):
    ref = dag_refute(fam(n))
    assert ref.found_empty


@pytest.mark.parametrize("fam", [or_family, and_family])
@pytest.mark.parametrize("n", [1, 2, 3, 4])
def test_interpolant_is_semantically_correct(fam, n):
    s = fam(n)
    interp = build_interpolant(s, dag_refute(s))
    ver = verify_interpolant(s, interp)
    assert ver["ok"], ver["violations"]


@pytest.mark.parametrize("n", [1, 2, 3, 4])
def test_or_family_interpolant_is_OR(n):
    s = or_family(n)
    interp = build_interpolant(s, dag_refute(s))
    zs = sorted(s.shared)
    from itertools import product
    for bits in product((0, 1), repeat=n):
        z = dict(zip(zs, bits))
        assert eval_gate(interp.root, z) == (1 if any(bits) else 0)


@pytest.mark.parametrize("n", [1, 2, 3, 4])
def test_and_family_interpolant_is_AND(n):
    s = and_family(n)
    interp = build_interpolant(s, dag_refute(s))
    zs = sorted(s.shared)
    from itertools import product
    for bits in product((0, 1), repeat=n):
        z = dict(zip(zs, bits))
        assert eval_gate(interp.root, z) == (1 if all(bits) else 0)


@pytest.mark.parametrize("n", [1, 2, 3, 4, 5])
def test_mux_count_equals_shared_vars(n):
    # CLAIM centrale: #MUX dell'interpolante = #variabili shared = #passi-su-shared del DAG.
    s = or_family(n)
    interp = build_interpolant(s, dag_refute(s))
    assert interp.mux_gates == n


@pytest.mark.parametrize("n", [1, 2, 3, 4, 5])
def test_construction_close_to_minimal(n):
    # interpolante della costruzione ≈ minimo (entrambi lineari): la costruzione
    # NON è asintoticamente più grande del minimo su queste famiglie.
    s = or_family(n)
    interp = build_interpolant(s, dag_refute(s))
    mn = min_interpolant_dt_size(s)["min_leaves"]
    # min DT leaves = n+1 ; #MUX costruzione = n  → differenza costante (≤1)
    assert abs((interp.mux_gates + 1) - mn) <= 1


def test_interpolant_size_decouples_from_saturation_steps():
    # I passi di SATURAZIONE esplodono (super-lineari) mentre l'interpolante resta
    # lineare: l'interpolante traccia i passi-su-shared del DAG, non la saturazione.
    steps, muxes = [], []
    for n in range(1, 6):
        s = or_family(n)
        ref = dag_refute(s)
        steps.append(ref.steps)
        muxes.append(build_interpolant(s, ref).mux_gates)
    # saturazione super-lineare
    assert steps[-1] / steps[0] > muxes[-1] / muxes[0] * 5
    # interpolante esattamente lineare
    assert muxes == [1, 2, 3, 4, 5]


def test_minimal_interpolant_well_defined():
    s = or_family(3)
    res = min_interpolant_dt_size(s)
    assert res["interpolatable"] is True
    assert res["min_leaves"] == 4  # OR su 3 bit: 4 foglie
