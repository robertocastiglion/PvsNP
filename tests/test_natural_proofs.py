"""Test del Natural Proofs Analyzer.

Eseguibili con: py -m pytest    (oppure: py tests/test_natural_proofs.py)
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from pnp_lab.natural_proofs import (  # noqa: E402
    BooleanFunction,
    measure_largeness,
    analyze,
)
from pnp_lab.natural_proofs.boolean import num_functions  # noqa: E402
from pnp_lab.natural_proofs import properties as P  # noqa: E402


def test_boolean_function_roundtrip():
    for n in range(1, 5):
        total = num_functions(n)
        # solo codici validi per questo n (0 .. 2^(2^n)-1)
        codes = {c for c in (0, 1, 7, total - 1) if 0 <= c < total}
        for code in codes:
            f = BooleanFunction.from_int(n, code)
            assert f.to_int() == code
            assert len(f.truth_table) == (1 << n)


def test_boolean_function_call():
    # AND su 2 variabili: truth table = [f(00), f(01), f(10), f(11)] = [0,0,0,1]
    f = BooleanFunction(2, [0, 0, 0, 1])
    assert f(0, 0) == 0
    assert f(0, 1) == 0
    assert f(1, 0) == 0
    assert f(1, 1) == 1


def test_balanced_largeness_exact():
    # Su n=2 (16 funzioni) le bilanciate hanno peso 2: C(4,2)=6 funzioni.
    r = measure_largeness(P.is_balanced, 2)
    assert r.method == "exact"
    assert r.count == 6
    assert r.total == 16
    assert abs(r.fraction - 6 / 16) < 1e-12


def test_constant_largeness_exact():
    # Solo 2 funzioni costanti per ogni n.
    for n in (2, 3, 4):
        r = measure_largeness(P.is_constant, n)
        assert r.count == 2, f"n={n}: attese 2 costanti, trovate {r.count}"


def test_parity_largeness_exact():
    # Esattamente 2 funzioni: parità e sua negazione.
    for n in (2, 3, 4):
        r = measure_largeness(P.is_parity, n)
        assert r.count == 2


def test_balanced_is_natural():
    # is_balanced deve risultare costruttiva + larga -> NATURALE.
    report = analyze(P.is_balanced)
    assert report.is_large is True
    assert report.is_constructive is True
    assert "NATURALE" in report.verdict


def test_constant_is_not_large():
    # is_constant: costruttiva ma decadimento super-lineare -> NON larga.
    report = analyze(P.is_constant)
    assert report.is_large is False


def test_high_circuit_complexity_small_n_artifact():
    # Lezione onesta: a n piccolo la larghezza della complessità di circuito
    # NON si manifesta (a n=2 nessuna funzione è 'difficile' con questa
    # codifica). Verifichiamo questo fatto deterministico, non il timing.
    r2 = measure_largeness(P.high_circuit_complexity, 2)
    assert r2.fraction == 0.0, "a n=2 tutte le funzioni sono semplici"
    r3 = measure_largeness(P.high_circuit_complexity, 3)
    assert r3.fraction > 0.0, "a n=3 cominciano a comparire funzioni difficili"


def test_constructiveness_is_a_diagnostic():
    # measure_constructiveness è un diagnostico empirico (basato sul tempo),
    # non una prova: verifichiamo solo che produca un report ben formato.
    report = analyze(P.is_balanced)
    c = report.constructiveness
    assert c is not None
    assert len(c.seconds) == len(c.ns) == len(c.table_sizes)
    assert all(s >= 0 for s in c.seconds)


if __name__ == "__main__":
    # runner minimale senza dipendere da pytest
    fns = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    failed = 0
    for fn in fns:
        try:
            fn()
            print(f"  PASS  {fn.__name__}")
        except AssertionError as e:
            failed += 1
            print(f"  FAIL  {fn.__name__}: {e}")
        except Exception as e:  # noqa: BLE001
            failed += 1
            print(f"  ERROR {fn.__name__}: {type(e).__name__}: {e}")
    print()
    print(f"  {len(fns) - failed}/{len(fns)} test superati")
    sys.exit(1 if failed else 0)
