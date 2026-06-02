"""Test per il proof-search su Lean vero (Modulo 11, passo #4).

I test VELOCI usano un checker FINTO e deterministico (niente Lean richiesto,
suite portabile), esattamente come l'LLM del modulo non è mai usato nei test.
Verifichiamo:
  - una policy migliore (euristica) chiude i lemmi con MENO verifiche;
  - soundness: si accetta solo un blocco che il verificatore approva;
  - l'LLM-policy è opzionale e ripiega sull'euristica se fallisce;
  - prompt/parse puri.
Un test d'integrazione con Lean VERO gira solo se `PNP_LEAN_IT=1` (e Lean c'è).
"""

import os

import pytest

from pnp_lab.proof_search import (
    LeanGoal,
    DEFAULT_TACTICS,
    LeanChecker,
    benchmark_lean_goals,
    build_lean_prompt,
    parse_indices,
    prove_with_lean,
    exhaustive_lean_policy,
    heuristic_lean_policy,
    LLMLeanPolicy,
    compare_lean_policies,
    ascii_comparison,
    to_svg_comparison,
    lean_bridge_summary,
)

# blocchi del pool, per riferimento negli oracoli finti
INTROS_RFL = "intros\nrfl"
INTROS_OMEGA = "intros\nomega"
INTROS_SIMP = "intros\nsimp"
CONJ = "intro a b h\nexact ⟨h.2, h.1⟩"

# tabella di chiusura "vera" (quali blocchi chiudono quali lemmi), per il checker finto
CLOSING = {
    "add_zero": {INTROS_RFL, INTROS_OMEGA, INTROS_SIMP},
    "zero_add": {INTROS_OMEGA, INTROS_SIMP},
    "succ_eq": {INTROS_RFL, INTROS_OMEGA, INTROS_SIMP},
    "two_two": {"rfl", "decide", "omega", "simp"},
    "le_refl": {INTROS_OMEGA},
    "and_comm": {CONJ},
}


def fake_check(goal: LeanGoal, block: str) -> bool:
    return block in CLOSING.get(goal.name, set())


def test_fake_checker_proves_all_goals():
    pol = heuristic_lean_policy()
    for g in benchmark_lean_goals():
        r = prove_with_lean(g, pol, fake_check)
        assert r.proved, f"{g.name} non dimostrato"
        # soundness: il blocco vincente è davvero accettato dal checker
        assert fake_check(g, r.winning_block)


def test_heuristic_uses_no_more_checks_than_exhaustive():
    goals = benchmark_lean_goals()
    ex = exhaustive_lean_policy()
    he = heuristic_lean_policy()
    tot_ex = sum(prove_with_lean(g, ex, fake_check).checks for g in goals)
    tot_he = sum(prove_with_lean(g, he, fake_check).checks for g in goals)
    assert tot_he <= tot_ex
    # su and_comm il blocco-chiave è ULTIMO nel pool: l'euristica deve fare molto meno
    g = next(g for g in goals if g.name == "and_comm")
    assert prove_with_lean(g, he, fake_check).checks < prove_with_lean(g, ex, fake_check).checks


def test_heuristic_ordering_features():
    he = heuristic_lean_policy()
    # un goal con ∀ mette prima un blocco con `intro`
    g_all = LeanGoal("x", "∀ n : Nat, n + 0 = n")
    assert "intro" in he(g_all)[0]
    # un goal con ∧ mette prima il costruttore
    g_conj = LeanGoal("y", "∀ p q : Prop, p ∧ q → q ∧ p")
    assert "h.2, h.1" in he(g_conj)[0]
    # un goal chiuso senza binder NON parte con intros
    g_eq = LeanGoal("z", "2 + 2 = 4")
    assert "intro" not in he(g_eq)[0]


def test_soundness_no_false_accept():
    # se il checker rifiuta tutto, nessuna policy "dimostra"
    reject_all = lambda g, b: False
    r = prove_with_lean(benchmark_lean_goals()[0], heuristic_lean_policy(), reject_all)
    assert not r.proved and r.winning_block is None
    assert r.checks == len(DEFAULT_TACTICS)  # le ha provate tutte, invano


def test_llm_policy_proposes_first_then_verified():
    # un "modello" che indica l'indice del blocco corretto per and_comm
    idx = DEFAULT_TACTICS.index(CONJ)
    g = next(g for g in benchmark_lean_goals() if g.name == "and_comm")
    llm = LLMLeanPolicy(call_fn=lambda prompt: str(idx))
    r = prove_with_lean(g, llm, fake_check)
    assert r.proved and r.winning_block == CONJ
    assert r.checks == 1  # proposto per primo, verificato da Lean (qui finto) → 1 sola verifica


def test_llm_policy_falls_back_on_failure():
    g = next(g for g in benchmark_lean_goals() if g.name == "and_comm")
    def boom(_prompt: str) -> str:
        raise RuntimeError("modello non disponibile")
    llm = LLMLeanPolicy(call_fn=boom)
    r = prove_with_lean(g, llm, fake_check)
    assert r.proved  # ripiega sull'euristica, la ricerca non si rompe


def test_prompt_and_parse_pure():
    g = benchmark_lean_goals()[0]
    prompt = build_lean_prompt(g)
    assert g.statement in prompt and "[0]" in prompt
    assert parse_indices("0\n2", DEFAULT_TACTICS) == [DEFAULT_TACTICS[0], DEFAULT_TACTICS[2]]
    assert parse_indices("garbage\n999", DEFAULT_TACTICS) == []


def test_reports_render():
    comp = compare_lean_policies(
        benchmark_lean_goals(),
        {"esaustiva": exhaustive_lean_policy(), "euristica": heuristic_lean_policy()},
        fake_check,
    )
    txt = ascii_comparison(comp, ["esaustiva", "euristica"])
    assert "Lean VERO" in txt
    svg = to_svg_comparison(comp, ["esaustiva", "euristica"])
    assert svg.startswith("<svg") and svg.rstrip().endswith("</svg>")
    assert "LeanDojo" in lean_bridge_summary()


@pytest.mark.skipif(
    os.environ.get("PNP_LEAN_IT") != "1" or not LeanChecker.available(),
    reason="integrazione Lean reale: imposta PNP_LEAN_IT=1 con Lean/lake disponibile",
)
def test_real_lean_proves_benchmark():
    checker = LeanChecker()
    pol = heuristic_lean_policy()
    for g in benchmark_lean_goals():
        r = prove_with_lean(g, pol, checker)
        assert r.proved, f"{g.name} non dimostrato da Lean: provati {r.tried}"
        assert checker(g, r.winning_block)  # ri-verifica (da cache): Lean conferma
