"""Test ESATTI per pnp_lab/attractor_theorem/lattice.py (Entry 36).

Gruppo: B_3 (permutazioni x negazioni di input), |B_3| = 48.
n=3: 256 funzioni booleane, 22 orbite B_3 MISURATE.

TROVATO (non ipotesi): i 5 invarianti {cost, gf2_degree, sensitivity,
block_sensitivity, adeg} sono TUTTI complement-invarianti (f e NOT(f) condividono
gli stessi valori); quindi NON esiste separatore da questa famiglia per le 22 orbite
B_3, che non identifica l'output complement.  Il reticolo di ricostruibilita' e'
un'ANTICATENA sul quoziente.
"""

import pytest

from pnp_lab.attractor_theorem.lattice import (
    INV_NAMES,
    orbit_invariant_table,
    reconstructibility_matrix,
    reconstructible_from,
    minimum_separators,
    hasse_diagram,
    summary,
)


# ── fixture condivisa (calcolata una volta per modulo) ──────────────────────

@pytest.fixture(scope="module")
def table3():
    return orbit_invariant_table(3)


@pytest.fixture(scope="module")
def matrix3(table3):
    return reconstructibility_matrix(table3)


@pytest.fixture(scope="module")
def summ3():
    return summary(3)


# ── 1. dimensioni esatte ─────────────────────────────────────────────────────

def test_n_orbits_exact(table3):
    """Su n=3, B_3 ha esattamente 22 orbite (MISURATO)."""
    assert len(table3) == 22


def test_orbit_sizes_cover_all_256(table3):
    """La somma delle dimensioni delle orbite deve essere 256."""
    from pnp_lab.meta_complexity.strata_graph import orbit_B
    total = sum(len(orbit_B(rep, 3)) for rep in table3)
    assert total == 256


def test_all_five_invariants_present(table3):
    """Ogni orbita deve avere esattamente i 5 invarianti."""
    for rep, inv in table3.items():
        assert set(inv.keys()) == set(INV_NAMES), f"orbita {rep} mancante di invarianti"


def test_invariants_are_integers(table3):
    """Tutti i valori degli invarianti sono interi (niente float/Fraction)."""
    for rep, inv in table3.items():
        for k, v in inv.items():
            assert isinstance(v, int), f"orbita {rep}, invariante {k}: tipo {type(v)}"


# ── 2. sanity su orbite note ──────────────────────────────────────────────────

def test_and3_canonical_invariants(table3):
    """AND3 (tt=128): orbita di dimensione 8, canonico = rep minimo.

    Invarianti noti: cost=2, gf2_degree=3, sensitivity=3, block_sensitivity=3.
    adeg_{1/3}(AND3): E_1(AND3)=1/3 <= eps=1/3 => adeg=1.
    """
    from pnp_lab.meta_complexity.strata_graph import orbit_B
    and3_tt = 128  # f(x0,x1,x2) = x0 AND x1 AND x2
    orb = orbit_B(and3_tt, 3)
    assert len(orb) == 8, "orbita di AND3 ha 8 elementi"
    canon = min(orb)
    assert canon in table3
    inv = table3[canon]
    assert inv["cost"] == 2
    assert inv["gf2_degree"] == 3
    assert inv["sensitivity"] == 3
    assert inv["block_sensitivity"] == 3
    assert inv["adeg"] == 1  # E_1(AND3) = 1/3 = eps -> adeg = 1


def test_xor3_canonical_invariants(table3):
    """XOR3 = parita' su 3 var: adeg=3 (grado pieno), sensitivity=3.

    Il canonico e' rep=105 (anti-parita', il minimo dell'orbita {105,150}).
    """
    from pnp_lab.circuits import parity_table
    from pnp_lab.meta_complexity.strata_graph import orbit_B
    xor3 = parity_table(3)  # tt=150
    orb = orbit_B(xor3, 3)
    assert len(orb) == 2, "orbita parita'/anti-parita' ha 2 elementi"
    canon = min(orb)  # = 105 (anti-parita')
    assert canon in table3
    inv = table3[canon]
    assert inv["sensitivity"] == 3
    assert inv["adeg"] == 3  # parita' ha adeg = n (grado pieno, test esistente)


def test_constants_are_singleton_orbits(table3):
    """Le costanti tt=0 e tt=255 sono orbite singleton (B_3 non sposta costanti)."""
    from pnp_lab.meta_complexity.strata_graph import orbit_B
    for tt_const in (0, 255):
        orb = orbit_B(tt_const, 3)
        assert len(orb) == 1 and tt_const in orb
        assert tt_const in table3  # e' il suo stesso canonico
        assert table3[tt_const]["cost"] == 1  # AND(x,NOT(x)) o OR(x,NOT(x))


# ── 3. matrice di ricostruibilita': riflessivita' e transitività ─────────────

def test_matrix_reflexive(matrix3):
    """M[I][I] = True per tutti gli invarianti (riflessivita')."""
    for inv in INV_NAMES:
        assert matrix3[inv][inv] is True, f"M[{inv}][{inv}] dovrebbe essere True"


def test_matrix_transitive(matrix3):
    """Se M[I][J] e M[J][K] allora M[I][K] (transitività del preordine)."""
    for I in INV_NAMES:
        for J in INV_NAMES:
            for K in INV_NAMES:
                if matrix3[I][J] and matrix3[J][K]:
                    assert matrix3[I][K], \
                        f"transitività violata: M[{I}][{J}] e M[{J}][{K}] ma non M[{I}][{K}]"


def test_matrix_shape(matrix3):
    """La matrice ha le chiavi giuste (5x5)."""
    assert set(matrix3.keys()) == set(INV_NAMES)
    for I in INV_NAMES:
        assert set(matrix3[I].keys()) == set(INV_NAMES)


def test_sensitivity_and_block_sensitivity_mutually_reconstructible(matrix3):
    """sensitivity e block_sensitivity sono mutualmente ricostruibili su n=3 (MISURATO)."""
    assert matrix3["sensitivity"]["block_sensitivity"] is True
    assert matrix3["block_sensitivity"]["sensitivity"] is True


def test_no_cross_reconstructibility_except_s_bs(matrix3):
    """Nessun altro invariante e' ricostruibile da un altro (eccetto s<->bs) su n=3."""
    # coppie attese come False
    incomparables = [
        ("cost", "gf2_degree"), ("cost", "sensitivity"), ("cost", "block_sensitivity"),
        ("cost", "adeg"), ("gf2_degree", "cost"), ("gf2_degree", "sensitivity"),
        ("gf2_degree", "block_sensitivity"), ("gf2_degree", "adeg"),
        ("adeg", "cost"), ("adeg", "gf2_degree"),
        ("adeg", "sensitivity"), ("adeg", "block_sensitivity"),
        ("sensitivity", "cost"), ("sensitivity", "gf2_degree"), ("sensitivity", "adeg"),
        ("block_sensitivity", "cost"), ("block_sensitivity", "gf2_degree"), ("block_sensitivity", "adeg"),
    ]
    for I, J in incomparables:
        assert matrix3[I][J] is False, f"M[{I}][{J}] atteso False, trovato True"


# ── 4. separatori e shape: il TROVATO (collasso) ─────────────────────────────

def test_min_separators_empty_no_separator_exists(table3):
    """TROVATO: nessun sottoinsieme di {cost,gf2_degree,sensitivity,bs,adeg}
    separa tutte le 22 orbite B_3.  Causa: tutti e 5 gli invarianti sono
    complement-invarianti (invarianti anche per la negazione dell'output),
    ma le orbite B_3 NON collassano f e NOT(f) nella stessa orbita.
    """
    seps = minimum_separators(table3)
    assert seps == [], f"atteso nessun separatore, trovato: {seps}"


def test_five_invariants_have_collisions(table3):
    """Il 5-tuple non e' iniettivo sulle orbite: ci sono collisioni (MISURATO)."""
    seen: dict = {}
    collisions = 0
    for rep, inv in table3.items():
        key = tuple(inv[k] for k in INV_NAMES)
        if key in seen:
            collisions += 1
        else:
            seen[key] = rep
    assert collisions >= 8, f"attese >= 8 collisioni, trovate {collisions}"


def test_hasse_shape_is_antichain(matrix3):
    """Il reticolo di ricostruibilita' sul quoziente e' un'ANTICATENA (MISURATO).
    4 classi di equivalenza: {cost}, {gf2_degree}, {sensitivity,block_sensitivity}, {adeg}.
    Nessuna classe e' piu' informativa di un'altra.
    """
    h = hasse_diagram(matrix3)
    assert h["shape"] == "antichain", f"shape attesa 'antichain', ottenuta '{h['shape']}'"
    assert h["arcs"] == [], f"anticatena deve avere archi vuoti, trovato {h['arcs']}"


def test_hasse_four_equivalence_classes(matrix3):
    """4 classi di equivalenza: {cost}, {gf2_degree}, {s,bs}, {adeg} (MISURATO)."""
    h = hasse_diagram(matrix3)
    classes = [frozenset(c) for c in h["classes"]]
    expected = [
        frozenset({"cost"}),
        frozenset({"gf2_degree"}),
        frozenset({"sensitivity", "block_sensitivity"}),
        frozenset({"adeg"}),
    ]
    assert set(classes) == set(expected), f"classi attese {expected}, trovate {classes}"


# ── 5. summary e reconstructible_from ────────────────────────────────────────

def test_summary_keys(summ3):
    """summary() ha tutte le chiavi richieste."""
    for key in ("n_orbits", "min_sep_size", "min_separators", "recon_matrix",
                "hasse", "shape", "group"):
        assert key in summ3


def test_summary_consistent(summ3):
    """Campi interni coerenti."""
    assert summ3["n_orbits"] == 22
    assert summ3["min_sep_size"] is None   # nessun separatore
    assert summ3["min_separators"] == []
    assert summ3["shape"] == "antichain"
    assert summ3["shape"] == summ3["hasse"]["shape"]


def test_reconstructible_from_singleton_consistent_with_matrix(table3):
    """reconstructible_from con S singleton: coerente con la matrice 1-a-1."""
    M = reconstructibility_matrix(table3)
    for I in INV_NAMES:
        for J in INV_NAMES:
            via_matrix = M[I][J]
            via_func = reconstructible_from(I, [J], table3)
            assert via_matrix == via_func, \
                f"discordanza: M[{I}][{J}]={via_matrix} vs reconstructible_from={via_func}"
