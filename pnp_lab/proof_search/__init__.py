"""Proof-Search Lab — proof-search trasparente, con policy pluggable (stile AlphaProof).

ONESTÀ, PRIMA DI TUTTO. Questo modulo NON dimostra P vs NP e NON "risolve" la
matematica con un LLM. È una dimostrazione trasparente e misurabile della tecnica
dietro AlphaProof/LeanDojo: un loop di ricerca che esplora lo spazio delle prove,
guidato da una *policy* che propone tattiche. La policy non prova nulla da sola —
propone solo mosse; a verificare è un motore di riscrittura SOUND e
autosufficiente. Una policy migliore si misura in NODI ESPANSI, non in promesse.

  - ``engine``   : termini, pattern-matching, riscrittura equazionale (mini-prover
                   di teoria dei gruppi). Ogni prova è ricontrollabile.
  - ``search``   : il loop best-first, con metriche oneste (nodi, successo/fallimento).
  - ``policies`` : baseline esaustiva, euristica trasparente, e l'interfaccia
                   OPZIONALE per un modello esterno (LLMPolicy). Il core non
                   dipende dall'LLM; i test non usano mai un modello reale.
  - ``lab``      : benchmark + RIVERIFICA di ogni prova + ASCII/SVG.

Collega il Modulo 4 (Lean): è lo stesso paradigma — proporre tattiche a un
verificatore — su un verificatore-giocattolo che possiamo eseguire e testare.
"""

from .engine import (
    Var,
    Term,
    Rule,
    Tactic,
    Goal,
    show,
    match,
    instantiate,
    positions,
    apply_tactic,
    applicable_tactics,
    distance,
    group_rules,
    benchmark_goals,
)
from .search import SearchState, SearchResult, search, replay
from .policies import (
    exhaustive_policy,
    heuristic_policy,
    build_prompt,
    parse_tactics,
    LLMPolicy,
)
from .lab import (
    PolicyReport,
    run_policy,
    run_benchmark,
    ascii_report,
    to_svg_benchmark,
    write_svg,
)
from .lean_bridge import (
    LeanGoal,
    CheckFn,
    DEFAULT_TACTICS,
    LeanProofResult,
    LeanChecker,
    PolicyComparison,
    exhaustive_lean_policy,
    heuristic_lean_policy,
    LLMLeanPolicy,
    build_prompt as build_lean_prompt,
    parse_indices,
    prove_with_lean,
    benchmark_lean_goals,
    compare_lean_policies,
    ascii_comparison,
    to_svg_comparison,
    lean_bridge_summary,
)

__all__ = [
    "Var", "Term", "Rule", "Tactic", "Goal",
    "show", "match", "instantiate", "positions",
    "apply_tactic", "applicable_tactics", "distance",
    "group_rules", "benchmark_goals",
    "SearchState", "SearchResult", "search", "replay",
    "exhaustive_policy", "heuristic_policy", "build_prompt", "parse_tactics", "LLMPolicy",
    "PolicyReport", "run_policy", "run_benchmark", "ascii_report", "to_svg_benchmark", "write_svg",
    # — proof-search su Lean vero (passo #4) —
    "LeanGoal", "CheckFn", "DEFAULT_TACTICS", "LeanProofResult", "LeanChecker",
    "PolicyComparison", "exhaustive_lean_policy", "heuristic_lean_policy", "LLMLeanPolicy",
    "build_lean_prompt", "parse_indices", "prove_with_lean", "benchmark_lean_goals",
    "compare_lean_policies", "ascii_comparison", "to_svg_comparison", "lean_bridge_summary",
]
