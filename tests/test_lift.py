"""Test per il sollevamento query → oracolo TM (Modulo 10, passo #1).

Verifichiamo, in modo esatto su m piccolo:
  - ogni macchina-oracolo campione viene DIAGONALIZZATA (sbaglia su 1ⁿ);
  - il nucleo piantato è davvero invisibile: rieseguendo la macchina contro
    l'oracolo FISSATO, ripete la stessa risposta (sbagliata) — non distingue;
  - il lato NP^Ã: dove 1ⁿ ∈ L_O, un testimone sul cubo si verifica in 1 query;
  - i due rami della diagonalizzazione (accetta-su-zero / rifiuta-su-zero).
"""

from pnp_lab.algebrization import Field, bits
from pnp_lab.algebraic_separation import (
    build_oracle,
    const_machine,
    cube_scan_machine,
    diagonalize_stage,
    default_adversary_machines,
    evaluate,
    np_certificate,
    ascii_lift,
    to_svg_lift,
    lift_summary,
)


def _rerun(machine, n, m, p, slice_):
    """Riesegue la macchina contro l'oracolo FISSATO `slice_` e ne ritorna la risposta."""
    F = Field(p)
    return bool(machine.decide(n, m, lambda r: evaluate(slice_, r, F)))


def test_default_build_all_diagonalized():
    lift = build_oracle(p=3, m=2, base_n=2)
    assert lift.all_diagonalized
    # ogni stadio: la macchina sbaglia (risposta ≠ appartenenza vera)
    for s in lift.stages:
        assert s.diagonalized
        assert s.machine_answer != s.true_membership


def test_planted_kernel_is_invisible():
    # la macchina, rieseguita contro l'oracolo fissato, ripete la stessa risposta
    # (il nucleo piantato è invisibile alle sue query) ⇒ resta in errore.
    machines = default_adversary_machines()
    lift = build_oracle(machines, p=3, m=2, base_n=2)
    for M, s in zip(machines, lift.stages):
        slice_ = lift.oracle[s.n]
        again = _rerun(M, s.n, s.m, s.p, slice_)
        assert again == s.machine_answer            # non distingue
        assert again != lift.in_language(s.n)       # e quindi sbaglia


def test_accept_branch_leaves_oracle_zero():
    # una macchina che accetta vedendo tutti zeri ⇒ oracolo nullo, 1ⁿ ∉ L_O
    stage, slice_ = diagonalize_stage(const_machine(True), n=2, m=2, p=3)
    assert stage.machine_answer is True
    assert stage.planted is None
    assert stage.true_membership is False
    assert not any(slice_)
    assert stage.diagonalized


def test_reject_branch_plants_nonzero_kernel():
    # una macchina che rifiuta ⇒ si pianta un nucleo booleano non nullo, 1ⁿ ∈ L_O
    stage, slice_ = diagonalize_stage(const_machine(False), n=3, m=2, p=3)
    assert stage.machine_answer is False
    assert stage.planted is not None
    assert any(slice_)                     # oracolo non identicamente nullo
    assert stage.true_membership is True
    assert stage.diagonalized


def test_planted_kernel_zero_on_queries():
    # per una macchina che fa query reali, il nucleo piantato è 0 su quei punti
    M = cube_scan_machine(1)
    stage, slice_ = diagonalize_stage(M, n=4, m=2, p=3)
    assert stage.diagonalized
    F = Field(3)
    # riesegui registrando le query e controlla che Ã = 0 su ciascuna
    seen = []
    M.decide(4, 2, lambda r: (seen.append(tuple(F.reduce(x) for x in r)),
                              evaluate(slice_, r, F))[1])
    assert seen  # ha fatto almeno una query
    assert all(evaluate(slice_, r, F) == 0 for r in seen)


def test_np_certificate_one_query():
    lift = build_oracle(p=3, m=2, base_n=2)
    for n in sorted(lift.oracle):
        cert = np_certificate(lift, n)
        if lift.in_language(n):
            assert cert.in_language and cert.witness is not None
            assert cert.queries == 1 and cert.verified
            # il testimone è davvero un 1 sul cubo
            z = sum(b << (lift.oracle_m[n] - 1 - i) for i, b in enumerate(cert.witness))
            assert lift.oracle[n][z] == 1
        else:
            assert not cert.in_language and cert.queries == 0


def test_reports_render():
    lift = build_oracle(p=3, m=2, base_n=2)
    txt = ascii_lift(lift)
    assert "NP^Ã" in txt and "DIAGONALIZZATA" in txt
    svg = to_svg_lift(lift)
    assert svg.startswith("<svg") and svg.rstrip().endswith("</svg>")
    assert "Aaronson" in lift_summary()
