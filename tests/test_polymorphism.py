"""Direzione B, ciclo 1 — politomorfismi di relazioni booleane piccole (fuori da σ(cost)).

Risultato ESATTO: nel setting IDEMPOTENTE (escluse le degeneri 0/1-valid) il profilo dei
politomorfismi SIMMETRICI coincide con la BLP-risolvibilità su TUTTE le relazioni booleane
di arità ≤3 → il parent-killer 'BLP ⟺ simmetrici di ogni arità' (Kun et al./Barto–Kozik)
REGGE. Restatement. Le 'divergenze' apparenti erano marker sbagliati (Schaefer⊋BLP;
MAJ/bounded-width⊋BLP) e l'artefatto K-deg (la costante non-idempotente delle 0/1-valid).
"""

from pnp_lab.csp.polymorphism import (
    AND2,
    MAJ3,
    MINORITY3,
    OR2,
    analyze,
    blp_solvable,
    has_symmetric_polymorphism,
    is_degenerate,
    preserves,
    symmetric_ops,
    symmetric_profile,
)

NEQ = frozenset({(0, 1), (1, 0)})          # x≠y: affine E bijunctive, ma NON BLP
IMPL = frozenset({(0, 0), (0, 1), (1, 1)})  # x→y: Horn (AND-chiusa) → BLP-risolvibile


def test_preserves_basic():
    assert preserves(AND2, 2, IMPL)        # implicazione è Horn
    assert not preserves(AND2, 2, NEQ)     # ≠ non è Horn
    assert preserves(MAJ3, 3, NEQ)         # ≠ è bijunctive (chiusa sotto MAJ)
    assert preserves(MINORITY3, 3, NEQ)    # ≠ è affine (chiusa sotto XOR)


def test_symmetric_ops_count():
    for k in range(2, 6):
        assert len(symmetric_ops(k, idempotent=True)) == 1 << (k - 1)


def test_disequality_is_not_blp_and_has_only_odd_symmetric():
    """≠ è bounded-width (MAJ) e affine (XOR) ma NON BLP: ha simmetrici idempotenti solo
    di arità DISPARI (le parità), mai pari → non 'di ogni arità' → non BLP-risolvibile."""
    assert blp_solvable(NEQ) is False
    prof = symmetric_profile(NEQ, max_arity=6)
    assert 3 in prof and 5 in prof          # parità dispari preservano l'affine
    assert 2 not in prof and 4 not in prof  # nessun simmetrico pari
    assert has_symmetric_polymorphism(NEQ, 2) is False


def test_implication_is_blp_with_all_symmetric():
    """x→y è Horn (AND) → BLP-risolvibile → ha simmetrici idempotenti di OGNI arità."""
    assert blp_solvable(IMPL) is True
    assert symmetric_profile(IMPL, max_arity=6) == (2, 3, 4, 5, 6)


def test_degenerate_detection():
    assert is_degenerate(frozenset({(0, 0, 0), (0, 1, 1)}))   # 0-valid
    assert is_degenerate(frozenset({(1, 1, 1), (0, 1, 0)}))   # 1-valid
    assert not is_degenerate(NEQ)


def test_parent_killer_holds_arity2_and_3():
    """Il claim centrale del ciclo: nel setting idempotente il profilo simmetrico ==
    BLP-risolvibile su TUTTE le relazioni booleane non degeneri di arità 2 e 3."""
    for arity, msa in [(2, 7), (3, 6)]:
        r = analyze(arity, max_sym_arity=msa)
        assert r.parent_killer_holds, r.mismatches[:3]
        assert r.verdict.startswith("RESTATEMENT")


def test_degenerate_relations_are_the_K_deg_artifact():
    """Senza escludere le degeneri, compaiono mismatch — TUTTI 0/1-valid (K-deg):
    BLP-risolvibili via la costante non-idempotente, profilo idempotente vuoto."""
    r = analyze(3, max_sym_arity=6, idempotent_only=False)
    assert len(r.mismatches) > 0
    for R, prof, blp in r.mismatches:
        assert is_degenerate(R)             # ogni mismatch è degenere (0/1-valid)
        assert blp is True                  # BLP-banale via la costante non-idempotente
        assert prof != (2, 3, 4, 5, 6)       # MA manca qualche arità → has_all_sym False
