"""Test del Modulo 14 — Enriched Meta-Category (difetto di composizione)."""

from pnp_lab.circuits import parity_table
from pnp_lab.meta_complexity import complexity_map
from pnp_lab.enriched_meta import (
    Category,
    apply_perm,
    check_isometry,
    cikk_island,
    defect_matrix,
    enriched_metacategory_summary,
    evaluate_lenses,
    formulas_of_size,
    framework_citations,
    irreducible_recognize_gap,
    proof_budget_curve,
    proof_length_for_threshold,
    total_influence,
)


# ── la categoria sottostante C ────────────────────────────────────────────

def test_category_objects_and_morphisms():
    cat = Category(n=3)
    assert len(cat.objects) == 256          # 2^(2^3)
    assert len(cat.morphisms) == 6          # 3! rinomine


def test_orbits_partition_function_space():
    cat = Category(n=3)
    orbits = cat.orbits()
    # le orbite partizionano esattamente lo spazio delle funzioni
    assert sum(len(o) for o in orbits) == 256
    flat = set()
    for o in orbits:
        flat |= o
    assert len(flat) == 256


def test_apply_perm_identity_is_noop():
    # la permutazione identità lascia ogni funzione invariata
    for tt in (0, 1, 0b10110100, parity_table(3)):
        assert apply_perm(tt, 3, (0, 1, 2)) == tt


def test_complexity_is_isometry_on_C():
    # il costo MCSP è costante su ogni orbita ⇒ i morfismi di C sono isometrie
    ct = complexity_map(3)
    rep = check_isometry(Category(n=3), ct.cost, measure="MCSP")
    assert rep.invariant
    assert rep.violations == 0


# ── le tre lenti ──────────────────────────────────────────────────────────

def test_parity_has_maximal_influence():
    # la parità è massimamente sensibile: ogni flip di bit cambia l'output
    n = 3
    assert total_influence(parity_table(n), n) == (1 << n) * n   # N·n = 24


def test_evaluate_lenses_covers_all_functions():
    ct = complexity_map(3)
    v = evaluate_lenses(ct, s=3, proof_budget=10)
    assert len(v.compute) == 256
    assert len(v.recognize) == 256
    assert len(v.prove) == 256
    # χ_comp coincide per definizione col costo esatto
    assert all(v.compute[t] == (ct.cost[t] > 3) for t in ct.cost)


def test_proof_length_grows_and_base_case():
    # taglia 0 = i 2n letterali
    assert formulas_of_size(0, 3) == 6
    # la lunghezza di prova è strettamente crescente nella soglia
    lengths = [proof_length_for_threshold(s, 3) for s in range(4)]
    assert all(lengths[i] < lengths[i + 1] for i in range(len(lengths) - 1))


# ── l'esperimento: difetto di composizione ────────────────────────────────

def test_defect_matrix_diagonal_zero_and_symmetric():
    ct = complexity_map(3)
    v = evaluate_lenses(ct, s=3, proof_budget=10)
    dm = defect_matrix(v)
    n = len(dm.labels)
    for i in range(n):
        assert dm.matrix[i][i] == 0.0
        for j in range(n):
            assert dm.matrix[i][j] == dm.matrix[j][i]


def test_cikk_island_is_strict_equivalence():
    # riconoscere ⟺ apprendere: round-trip esatto, difetto 0 (CIKK 2016)
    ct = complexity_map(3)
    v = evaluate_lenses(ct, s=3, proof_budget=10)
    island = cikk_island(ct, v)
    assert island.round_trip_defect == 0.0
    assert island.equivalent


def test_proof_axis_is_closable_by_budget():
    # calcolare ↔ dimostrare: budget insufficiente ⇒ difetto pieno; sufficiente ⇒ 0
    ct = complexity_map(3)
    s = 3
    needed = proof_length_for_threshold(s, 3)
    curve = proof_budget_curve(ct, s, budgets=[0, needed - 1, needed, needed * 2])
    below = [p for p in curve if p.budget < needed]
    above = [p for p in curve if p.budget >= needed]
    assert all(p.defect_compute_prove > 0 for p in below)   # lower bound non dimostrato
    assert all(p.defect_compute_prove == 0.0 for p in above)  # dimostrato ⇒ coincide


def test_recognize_axis_has_residual_gap_somewhere():
    # calcolare ↔ riconoscere: esiste una soglia s in cui la proprietà costruttiva
    # NON riproduce il costo esatto, nemmeno con θ ottimale (la barriera)
    ct = complexity_map(3)
    gaps = [irreducible_recognize_gap(ct, s) for s in range(ct.max_cost)]
    assert all(g.residual_defect >= 0.0 for g in gaps)
    assert any(g.residual_defect > 0.0 for g in gaps)


# ── verdetto e citazioni ──────────────────────────────────────────────────

def test_summary_and_citations_well_formed():
    v = enriched_metacategory_summary()
    assert "condizionato" in v.conclusion.lower()
    assert "non risolve p vs np" in v.honesty.lower()
    cits = framework_citations()
    assert len(cits) >= 5
    assert all(c.reference and c.claim for c in cits)
    joined = " ".join(c.reference for c in cits)
    assert "Lawvere" in joined and "Carmosino" in joined
