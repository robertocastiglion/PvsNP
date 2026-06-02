# Proof-search on real Lean (LeanDojo-style) — same policy, a real verifier

*Research thread implemented on 2026-06-02. Extends Module 11 from a toy verifier
to Lean 4 itself.*

## Goal

Module 11 runs proof-search over a sound *toy* rewriting prover. This step connects
the **same idea of a policy** to **real Lean 4**: a policy proposes tactic blocks,
and the **Lean kernel** (via `lake env lean`) accepts or rejects them. The policy
never proves anything by itself — the only authority is Lean. A better policy is
measured exactly as in Module 11: in **fewer calls to the verifier**.

## What is executed

- `LeanGoal` — a lemma to prove in Lean core (no mathlib).
- `CheckFn` = `(goal, block) -> bool` — tries a `by …` block. It is **injectable**:
  in production it is `LeanChecker` (writes a temp file and runs `lake env lean`);
  in the tests it is a deterministic **fake** (no Lean needed, fast and portable),
  exactly as the optional LLM is never invoked in the tests.
- Policies: `exhaustive_lean_policy` (fixed order, blind baseline),
  `heuristic_lean_policy` (orders candidates by the goal's syntactic shape), and
  `LLMLeanPolicy` (optional, pluggable `call_fn`, **never on the sound path**:
  Lean has the last word; falls back to the heuristic).
- `prove_with_lean(goal, policy, check)` — tries blocks in the policy's order until
  Lean accepts one; reports `checks` = number of verifier calls (the honest metric).

### Measured against real Lean (benchmark of 6 core lemmas)

| lemma | exhaustive | heuristic |
|---|---:|---:|
| `add_zero` (`∀ n, n+0=n`) | 3 | 1 |
| `zero_add` (`∀ n, 0+n=n`) | 3 | 2 |
| `succ_eq` (`∀ n, n+1=succ n`) | 3 | 1 |
| `two_two` (`2+2=4`) | 1 | 1 |
| `le_refl` (`∀ n, n≤n`) | 3 | 1 |
| `and_comm` (`∀ p q, p∧q→q∧p`) | 9 | 1 |
| **total Lean verifications** | **22** | **7** |

Both policies prove every lemma; the heuristic needs **7** Lean verifications vs the
exhaustive baseline's **22** (`web/assets/lean_proofsearch.svg`). Same honest metric
as Module 11 — fewer states/calls = better policy — but the verifier is now Lean.

## Honesty boundary

- **The policy proves nothing**: every accepted proof is checked by the real Lean
  kernel (`prove_with_lean` only accepts a block when `check` returns true).
- **The LLM is optional and pluggable** (`LLMLeanPolicy`), never on the sound path;
  the test suite uses a fake checker and does **not** invoke Lean, so it stays fast
  and portable. A real-Lean integration test runs only when `PNP_LEAN_IT=1` (and
  Lean is installed).
- This does **not** prove P vs NP. It is the AlphaProof/LeanDojo technique made
  honest and measurable — now on a real verifier instead of a toy.

## Files

```
pnp_lab/proof_search/lean_bridge.py   # LeanGoal, LeanChecker, policies, prove_with_lean
tests/test_lean_bridge.py             # 8 fast tests (fake checker) + 1 real-Lean test (opt-in)
examples/run_lean_proofsearch.py      # demo driving real Lean
web/assets/lean_proofsearch.svg       # verifications per policy
```
