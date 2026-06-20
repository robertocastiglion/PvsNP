# Module 28 — The Two Barriers' Leverage: relativization is trivial-but-exact, magnification is absent

*Crystallized 2026-06-20. Closes the short program "Relativization Obstruction as a
Leverage Operator" (`prompts/relativization-barrier.md`, RESEARCH_LOG Entries 25–26) at its
honest ceiling. It proves **no** lower bound and makes **no claim about P vs NP**. Its two
deliverables are: (1) an honest **contrast** between the two barriers read with the same
leverage lens, and (2) a genuine **fidelity stress-test** that strengthens the existing
`pnp_lab/oracles` relativization construction.*

## Why this program existed (and why it is short)

After the Magnification Frontier closed (`docs/cross-level-survival-arc.md`), the leverage
lens — the lab's newest tool — was applied to a second barrier. A **course correction**, on
record: the PI first thought the lab had never made relativization executable; it had —
`pnp_lab/oracles/` already runs and verifies the Baker–Gill–Solovay construction (`separation`
= `P^B ≠ NP^B`, `collapse` = `P^A = NP^A` via TQBF), and all three classic barriers were
already present (algebrization lives in `pnp_lab/algebrization`, `algebraic_worlds`,
`algebraic_separation`). So the program was **re-scoped to reuse**, not rebuild: apply the
leverage lens to the existing BGS construction. (Lesson, recorded for the loop: check the
existing `pnp_lab/` packages before proposing a "new" arena.)

The crucible question: relativization's obstruction is the cleanest counting gap in
complexity, and unlike the magnification object it is **exact and explicitly growing** (a
poly machine inspects `≤ n^k` of the `2^n` length-n strings). Measured as a cross-level
operator, is it a genuine leverage staircase — or does it collapse to one total bound?

## Cycle 1 — the leverage operator (RESTATEMENT)

`pnp_lab/oracles/leverage.py` reuses the verified BGS diagonalization and measures, exactly:

| n | 2^n | depth(OR) | h(n,1) | h(n,2) | h(n,3) |
|---|-----|-----------|--------|--------|--------|
| 1 | 2   | 2         | 1      | 1      | 1      |
| 2 | 4   | 4         | 2      | 0      | −4     |
| 3 | 8   | 8         | 5      | −1     | −19    |
| 4 | 16  | 16        | 12     | 0      | −48    |
| 5 | 32  | 32        | 27     | 7      | −93    |
| 6 | 64  | 64        | 58     | 28     | −152   |

with the break-even staircase `n*(k) = 1, 5, 10` (the first level beyond which `2^n > n^k`
forever). `depth(OR)` over `2^n` variables is **verified** (not assumed) by a generic
decision-tree recursion for `n ≤ 3`; it is the exact **reservation lemma** at the heart of
BGS (until all `2^n` strings are read, a free one flips the OR).

**Adversary — RESTATEMENT.** Everything reduces to the single total fact `depth(OR_m) = m`
instantiated at `m = 2^n`, plus elementary arithmetic of `2^n` vs `n^k`. The
`obstruction_height` column *is* `depth(OR)` by definition; `h`, `n*` are arithmetic. The
pre-declared non-collapsing candidate — the **online freshness length-schedule** across
diagonalization stages — also collapsed: for `EXAMPLE_MACHINES` it equals the greedy
budget arithmetic exactly (`matches_greedy = True`).

## Cycle 2 — fidelity stress-test (PASS) + the schedule (RESTATEMENT)

`EXAMPLE_MACHINES` are all simple and never query above their input length. Cycle 2 builds a
strictly harder class — **adaptive** (next query depends on prior answers), **cross-length**
(`probe_long`, reach `= k·n`), and **backscan** (queries shorter strings, where earlier
stages may have planted) — and stresses the existing construction.

Measured (`HARD_MACHINES`):

```
all_defeated_in_construction : True
stable_under_final_B         : True      ← the stability theorem holds
schedule lengths             : (2, 5, 6, 7)
realized reaches             : (4, 5, 5, 21)
execution_dependent_reach    : False
```

- **Fidelity = PASS (the genuine positive).** `build_separating_oracle` defeats the harder
  class, **and** the **stability theorem** holds: re-running each machine against the
  *final* oracle `B` still defeats it. This confirms the load-bearing freshness invariant —
  later stages never perturb earlier machines — on a class the existing tests never
  exercised. A real strengthening of `pnp_lab/oracles`.
- **Leverage = RESTATEMENT (cleaner than Cycle 1).** `execution_dependent_reach = False`:
  the realized reach equals the empty-oracle reach, so the freshness schedule is a
  **closed-form function of each machine's syntactic max-query-length + budget**, independent
  of the oracle. The non-collapsing candidate fully collapses.

## The honest result: the two barriers' leverage

Read with the same cross-level leverage lens, the two barriers sit at **opposite extremes**,
and neither yields new content:

| Barrier | Leverage operator | Verdict |
|---------|-------------------|---------|
| **Magnification** (`MBPSP[s]` order-anisotropy) | **ABSENT** — survives but does not amplify; true leverage is asymptotic (`n=7 = 2^128` unreachable); object is quasi-permutation-invariant | survival, not leverage |
| **Relativization** (BGS counting obstruction) | **PRESENT and EXACT** — `h(n,k)` grows, `n*(k)` is a real staircase — but **TRIVIAL**: collapses to `depth(OR) = 2^n` + arithmetic; even the online schedule is closed-form | exact, but trivial |

One has no measurable leverage; the other has fully-measurable-but-trivial leverage. This is
the program's positive content: the leverage lens, applied to a second barrier, locates the
other extreme — and **sharpens the Collapse Theorem** (`docs/collapse-theorem.md`) by showing
that even the one barrier whose obstruction is exact *and* growing collapses to a known total
bound. It is the 13th collapse overall and the first outside the CSP/magnification branches.

## Honesty boundary

COMPUTED exactly: `depth(OR)` on `2^n` variables (generic decision-tree recursion for
`n ≤ 3`, where `2^n ≤ 8`); the reservation counts `2^n − q`; `h(n,k)`; `n*(k)`; the freshness
schedule; the fidelity stress-test (defeat + stability re-run against the final `B`) — all
reusing the verified BGS diagonalization in `separation.py`. CITED, never re-proved:
Baker–Gill–Solovay 1975 (the barrier) and `depth(OR_m) = m` for `m > 8` (textbook; the
generic verification explodes as `3^m`). NOT shown: any non-trivial leverage operator — the
relativization obstruction is exact-but-trivial. **No separation, no P vs NP claim.**
