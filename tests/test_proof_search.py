"""Test del Modulo 11 — Proof-Search Lab (loop trasparente, policy pluggable)."""

from pnp_lab.proof_search import (
    Goal,
    LLMPolicy,
    Term,
    Var,
    apply_tactic,
    applicable_tactics,
    benchmark_goals,
    build_prompt,
    exhaustive_policy,
    group_rules,
    heuristic_policy,
    match,
    parse_tactics,
    replay,
    run_benchmark,
    search,
    show,
)
from pnp_lab.proof_search.search import SearchState


# ── motore: matching e riscrittura ────────────────────────────────────────

def test_match_binds_variables():
    x = Var("x")
    pat = Term("mul", (Term("e"), x))
    term = Term("mul", (Term("e"), Term("a")))
    s = match(pat, term, {})
    assert s is not None and s["x"] == Term("a")


def test_match_fails_on_mismatch():
    pat = Term("mul", (Term("e"), Var("x")))
    term = Term("inv", (Term("a"),))
    assert match(pat, term, {}) is None


def test_apply_tactic_rewrites():
    rules = group_rules()
    term = Term("mul", (Term("e"), Term("a")))
    tacs = applicable_tactics(rules, term, allow_reverse=False)
    # id_left si applica alla radice
    assert any(t.rule == "id_left" for t in tacs)
    fwd = next(t for t in tacs if t.rule == "id_left")
    assert apply_tactic(rules, term, fwd) == Term("a")


# ── ricerca: trova prove, e sono SOUND ────────────────────────────────────

def test_search_finds_proof_and_it_replays():
    rules = group_rules()
    g = Goal("inv_inv", Term("inv", (Term("inv", (Term("a"),)),)), Term("a"))
    res = search(g, rules, heuristic_policy(top_k=4))
    assert res.success
    assert replay(g, rules, res.proof)        # soundness: la prova ricostruisce il target
    assert res.proof_length >= 1


def test_search_all_benchmarks_solved_and_verified():
    rules = group_rules()
    for g in benchmark_goals():
        res = search(g, rules, heuristic_policy(top_k=4))
        assert res.success, f"non risolto: {g.name}"
        assert replay(g, rules, res.proof), f"prova non valida: {g.name}"


def test_unsolvable_goal_fails_cleanly():
    rules = group_rules()
    # 'a = b' non è dimostrabile: la ricerca deve fallire pulita (niente prova falsa)
    g = Goal("bogus", Term("a"), Term("b"))
    res = search(g, rules, heuristic_policy(top_k=4), max_nodes=500)
    assert not res.success
    assert res.proof == []


# ── policy: l'euristica è almeno efficiente quanto la baseline ────────────

def test_heuristic_generates_fewer_states():
    reports = run_benchmark(max_nodes=4000)
    baseline, heur = reports[0], reports[1]
    assert heur.solved == baseline.solved == len(benchmark_goals())
    assert heur.all_proofs_valid and baseline.all_proofs_valid
    # entrambe chiudono tutto, ma l'euristica impegna MENO ramificazione
    # (genera strettamente meno stati): è la misura onesta di una policy migliore
    assert heur.total_generated < baseline.total_generated


# ── interfaccia LLM (PURA, senza modello reale) ───────────────────────────

def test_build_and_parse_prompt_roundtrip():
    rules = group_rules()
    term = Term("mul", (Term("e"), Term("a")))
    state = SearchState(term, Term("a"), rules)
    prompt = build_prompt(state)
    assert "Tattiche applicabili" in prompt and "target" in prompt
    # un "modello" che sceglie la mossa [0]
    chosen = parse_tactics("0", state)
    assert len(chosen) == 1
    assert chosen[0] == applicable_tactics(rules, term)[0]


def test_parse_ignores_garbage_and_out_of_range():
    rules = group_rules()
    state = SearchState(Term("mul", (Term("e"), Term("a"))), Term("a"), rules)
    # indici non validi / testo spazzatura → scartati (il motore resta l'autorità)
    assert parse_tactics("bla bla\n9999\n-1\nciao", state) == []


def test_llm_policy_falls_back_on_failure():
    rules = group_rules()
    g = Goal("inv_inv", Term("inv", (Term("inv", (Term("a"),)),)), Term("a"))

    def broken_call(_prompt: str) -> str:
        raise RuntimeError("nessuna rete / nessuna chiave")

    # se il modello fallisce, la policy ripiega sull'euristica e la ricerca regge
    res = search(g, rules, LLMPolicy(broken_call))
    assert res.success and replay(g, rules, res.proof)
