# Restart program — out of the μ_R dictionary

Addendum to `prompts/research-loop.md`. Reconstructed 2026-06-13 (the original
2026-06-12 file was never committed and was lost; see memory `research-loop-system`).

## Why a special restart is needed

The loop closed (Module 19, RESEARCH_LOG Entry 7) and the falsifier hunt (Entry 8)
HARDENED the Tiny-Instance Collapse: on n≤4 every discriminant tried dies inside
σ(cost). **Diagnosis of why the collapse keeps firing** — every discriminant so far was

1. **scalar** (a single number per function), and/or
2. the **minimum of a covering program** (cover-LP / KW partition) or a gradient of one,
   and/or
3. **unary** (a property of one function in isolation).

**Admissibility rule:** a new direction is allowed ONLY if it explicitly BREAKS at least
one of (1)–(3). Each direction below declares its parent-killer in advance (the known
theorem it would reduce to). Honesty > positive results: "collapse onto a known object"
is the expected, acceptable outcome — report it and move on.

## Program order

- **E — count of optimal circuits `N_min(f)`** (entry probe). Hypothesis H-E: N_min =
  #optimal formulas; NPN group order 96 on n=3. **Killer:** N_min is a function of
  (cost, |orbit|). Bridges to A. *(Explorer was done in a prior session; brief lost.)*

- **A — solution-space geometry / tiny OGP (MAIN).** Breaks (1) [a set/graph, not a
  number] and (3) [relational: structure of a set of optima]. Formula-size is not a
  covering program → also breaks (2). Object: the optimal-split DAG `OptSplit(f)`,
  reconstructible exactly from the cost table. **Killers:** K1 geometry reconstructible
  from (cost,|orbit|,N_min); K2 verdict flips under encoding change (ordered↔unordered
  tree count); K3 geometry determined by Aut(f)/orbit. *(BUILT 2026-06-13:
  `pnp_lab/meta_complexity/solution_geometry.py`; n=3 is below the falsifiability
  threshold — scalar key already injective on the 14 orbits; n=4 is the decisive run.)*

- **B — polymorphism clones / minions (pivot; Bulatov–Zhuk).** Breaks (2) by leaving the
  covering world for the algebraic CSP-dichotomy world. **Parent-killer:** BLP ⟺
  symmetric polymorphisms.

- **Reserves: C** conditional `KT(f|g)` / symmetry of information; **D** approximation
  curve `ε ↦ cost_ε`.

- **F — dictionary COMPLETENESS relative to a declared grammar G** (only after 2 more
  restatements): prove that every poly-time invariant in G is a function of the μ_R
  generators, making the collapse a theorem relative to G.

## Run

`/loop esegui prompts/restart-out-of-dictionary.md` — Explorer picks/refines ONE
direction with its killer, Builder implements the exact experiment, then measure →
adversary → evaluator → archivist as per research-loop.md. STOP-and-ask criteria
unchanged.
