"""Test per il Modulo 15 — Distinguishing Advantage Sandbox (misura esatta n=3).

Verifichiamo, in modo esatto sulla istanza giocattolo:
  - lo split DURE/FACILI copre tutte le 256 funzioni ed è coerente con la soglia;
  - la base di oracle gate è cumulativa (fan-in ≤ ℓ) ⇒ base(1) ⊆ base(2) ⊆ base(3);
  - il vantaggio ε è in [0,1] e MONOTÒNO nei due assi ℓ e s;
  - le celle piccole sono esatte; le grandi sono cote inferiori (exact=False);
  - su questa istanza ENTRAMBI gli assi contribuiscono (corner > solo-info, solo-calc).
"""

from pnp_lab.distinguishing import (
    NUM_FUNCS,
    advantage_matrix,
    ascii_matrix,
    build_local_basis,
    default_split,
    distinguishing_summary,
    frontier_note,
    to_svg_matrix,
)
from pnp_lab.distinguishing.advantage import _advantage


def test_split_partitions_all_functions():
    sp = default_split()
    assert sp.n_hard + sp.n_easy == NUM_FUNCS
    assert set(sp.hard).isdisjoint(sp.easy)
    assert len(set(sp.hard) | set(sp.easy)) == NUM_FUNCS
    # le maschere a 256 bit sono coerenti con gli insiemi
    assert sp.hard_mask == sum(1 << f for f in sp.hard)
    assert sp.easy_mask == sum(1 << f for f in sp.easy)


def test_split_respects_threshold():
    from pnp_lab.circuits import min_formula_sizes
    ct = min_formula_sizes(3)
    sp = default_split()
    assert all(ct.cost[f] >= sp.tau for f in sp.hard)
    assert all(ct.cost[f] < sp.tau for f in sp.easy)


def test_basis_is_cumulative_in_locality():
    b1 = set(build_local_basis(1))
    b2 = set(build_local_basis(2))
    b3 = set(build_local_basis(3))
    assert b1 <= b2 <= b3
    # ogni elemento è una funzione a 256 bit (sta dentro la maschera)
    mask = (1 << NUM_FUNCS) - 1
    assert all(0 <= t <= mask for t in b3)


def test_basis_contains_constants_and_is_complement_closed():
    b1 = build_local_basis(1)
    mask = (1 << NUM_FUNCS) - 1
    assert 0 in b1 and mask in b1                      # costanti 0 e 1
    bset = set(b1)
    assert all((mask ^ t) in bset for t in b1)         # chiusa per complemento


def test_advantage_in_unit_interval():
    sp = default_split()
    m = advantage_matrix(sp)
    for c in m.cells.values():
        assert 0.0 <= c.epsilon <= 1.0


def test_advantage_is_monotone_in_both_axes():
    sp = default_split()
    m = advantage_matrix(sp)
    for ell in (1, 2, 3):
        for s in (1, 2):
            assert m.get(ell, s + 1).epsilon >= m.get(ell, s).epsilon - 1e-12
    for s in (1, 2, 3):
        for ell in (1, 2):
            assert m.get(ell + 1, s).epsilon >= m.get(ell, s).epsilon - 1e-12


def test_small_cells_are_exact():
    sp = default_split()
    m = advantage_matrix(sp)
    # le celle a bassa risorsa sono enumerate esattamente
    for ell, s in [(1, 1), (1, 2), (1, 3), (2, 1), (2, 2), (3, 1)]:
        assert m.get(ell, s).exact


def test_both_axes_contribute_on_this_instance():
    sp = default_split()
    m = advantage_matrix(sp)
    corner = m.get(3, 3).epsilon
    info_only = m.get(3, 1).epsilon      # tanta info, poco calcolo
    comp_only = m.get(1, 3).epsilon      # poca info, tanto calcolo
    # l'angolo supera STRETTAMENTE entrambi gli spigoli: servono i due assi
    assert corner > info_only + 1e-9
    assert corner > comp_only + 1e-9


def test_advantage_helper_matches_definition():
    sp = default_split()
    # il distinguitore "accetta tutto" non separa nulla: ε = 0
    allmask = (1 << NUM_FUNCS) - 1
    assert _advantage(allmask, sp) == 0.0
    assert _advantage(0, sp) == 0.0
    # il distinguitore = indicatore esatto delle DURE separa perfettamente: ε = 1
    assert abs(_advantage(sp.hard_mask, sp) - 1.0) < 1e-12


def test_reports_render():
    sp = default_split()
    m = advantage_matrix(sp)
    assert "ε(ℓ, s)" in ascii_matrix(m)
    assert "Trade-off" in frontier_note(m) or "satura" in frontier_note(m) \
        or "INFORMAZIONE" in frontier_note(m) or "CALCOLO" in frontier_note(m)
    svg = to_svg_matrix(m)
    assert svg.startswith("<svg") and svg.rstrip().endswith("</svg>")
    assert "MODULO 15" in svg
    assert isinstance(distinguishing_summary(), str)
