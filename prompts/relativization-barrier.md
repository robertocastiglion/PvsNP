# Program — the Relativization Obstruction as a Leverage Operator

New research program, opened 2026-06-19 after the Magnification Frontier closed
(`docs/cross-level-survival-arc.md`, RESEARCH_LOG Entries 13–24). Human PI delegated the
choice of direction.

> **CORRECTION (2026-06-19, recorded for honesty).** The PI-model first proposed "make the
> relativization barrier executable", believing the lab had never touched it. That premise
> was WRONG: **all three classic barriers are already executable** — relativization in
> `pnp_lab/oracles/` (BGS `separation` = the verified diagonalization `P^B ≠ NP^B`, and
> `collapse` = TQBF giving `P^A = NP^A`), and algebrization in `pnp_lab/algebrization`,
> `algebraic_worlds`, `algebraic_separation`. Re-building BGS would DUPLICATE existing
> modules. The program was therefore **re-scoped** to the one genuinely non-duplicative
> angle below.

## Why this program (and why now)

`pnp_lab/oracles/separation.py` already runs and verifies the BGS diagonalization, but it
never measures the **cross-level leverage operator** — and that is no accident: the
**leverage principle is the lab's newest tool**, born from the Magnification Frontier that
just closed. That program tried for cycles to measure a faithful cross-level amplification
operator and never could, because its object's leverage was asymptotic (n=7 = 2^128 out of
reach). Relativization is the natural **crucible** for the same lens, because its
obstruction is the cleanest counting gap in complexity AND it is **exact and explicitly
growing**: a poly-time oracle machine inspects ≤ `q(n) = n^k` of the `2^n` strings of
length n, so the **diagonalization headroom `h(n,k) = 2^n − n^k`** is an exact integer that
really grows.

So the program does NOT re-make a wall executable (done). It asks, reusing
`pnp_lab/oracles`: **measured with the magnification frontier's leverage lens, is the
relativization obstruction a genuine cross-level leverage operator — or does it collapse
to the single total fact `depth(OR) = 2^n`?** This pits the lab's two closed-branch
findings against each other directly.

It is the right crucible because it puts the lab's two big findings in direct collision:

- **"Exact enumerability is the trap"** (`docs/collapse-theorem.md`): every exact
  discriminant on a tiny object collapsed onto a dictionary invariant.
- **"Leverage escapes because it is asymptotic"** (`docs/cross-level-survival-arc.md`):
  the cross-level amplification operator could never be measured (n=7 = 2^128 out of
  reach).

Relativization's obstruction is **exact AND explicitly growing**: a poly-time oracle
machine inspects ≤ q(n) = n^k strings, but the length-n slice has 2^n strings, so the
**diagonalization headroom h(n,k) = 2^n − n^k** is an exact integer that genuinely grows.
So: when the obstruction is exact *and* has real cross-level growth, does the lab finally
measure a faithful **leverage operator** — or does "exact = trap" strike again (it
collapses to the textbook decision-tree depth of OR, a total bound)? That is the new,
falsifiable, on-model question.

## The faithful core (what is made exact)

The BGS theorem has two halves; the runnable, decisive half is the separation.

**∃ oracle B with P^B ≠ NP^B (the diagonalization — Cycle 1 target).**
- Test language: `L_B = { 1^n : B ∩ {0,1}^n ≠ ∅ }`. This is in `NP^B` always (guess an
  n-bit witness x, accept iff x ∈ B — one query).
- The faithful abstraction of a poly-time oracle machine deciding `1^n`: on the length-n
  slice of the oracle (the `2^n`-bit characteristic vector), it adaptively reads at most
  `q(n)` bits, then outputs accept/reject — i.e. it is a **decision tree of depth ≤ q(n)**
  over the `2^n` slice-variables. The slice-membership predicate of `L_B` is exactly the
  `2^n`-bit **OR** of those variables.
- BGS works because **a depth-q decision tree cannot compute OR of 2^n variables when
  q < 2^n**: whatever ≤ q < 2^n strings the machine reserves/queries, an unread string
  remains, and its value flips OR — so the machine is fooled. The diagonalization sets
  that free string to make `L_B(1^n)` disagree with the machine.

**∃ oracle A with P^A = NP^A (the easy half — later cycle).** Take A powerful enough that
the existential guess is simulable deterministically with oracle help (BGS use a
PSPACE-complete A). On a bounded universe this is the "collapse side"; deferred.

## The leverage principle (inherited, BINDING)

Do not freeze the obstruction at one n. Measure the **operator across levels**:
- `D(n)` = exact decision-tree depth of the n-slice OR (the obstruction's height);
- `h(n,k) = 2^n − n^k` = the diagonalization headroom for a degree-k poly machine;
- `n*(k) = min{ n : 2^n > n^k }` = the **break-even stage** — the first length at which a
  poly-k machine is defeated (the staircase the magnification program could not find).
Measure how these grow, and whether the growth is a genuine amplification operator or
collapses to the single total fact "depth(OR) = 2^n".

## The success criterion + the adversary's job (fidelity, not reduce-to-known)

A cycle SUCCEEDS if it produces an exact, reproducible, **faithful** executable model of a
piece of the relativization barrier. The adversary attacks:
- **Infidelity** — the tiny model exhibits behavior that does NOT reflect BGS (wrong
  direction; a finite-size artifact sold as the mechanism; the "diagonalization" not
  actually fooling the machine class it claims).
- **Vacuity** — technically correct but shows nothing the barrier contains (e.g. the
  obstruction invisible at tiny n).
- **Over-claim** — the doc claims more than the tiny instance licenses (especially: any
  hint of a P-vs-NP statement; the model proves the barrier, i.e. that *these techniques*
  cannot settle P vs NP, NOT anything about P vs NP itself).

The evaluator scores **fidelity + tangibility** and writes the honesty boundary (BGS
cited; what is computed vs cited; where the asymptotic content escapes tiny size).

## Cycle 1 — Explorer hypothesis (declared, with fidelity-killer)

**Object.** The n-slice OR (the `NP^B` test predicate) and the depth-q decision-tree model
of a `P^B` machine, for n = 1,2,3,4 (slice sizes `2^n` = 2,4,8,16).

**Faithful claim to verify exactly.**
1. The deterministic decision-tree depth of OR over `2^n` variables is **exactly `2^n`**
   (any tree of depth `< 2^n` is fooled by an adversary that keeps the read bits 0 and
   flips an unread bit) — the exact reservation argument.
2. The BGS diagonalization, run against an explicit finite list of machines (each = a
   query budget `q_i(n)` + an adaptive query strategy), produces a concrete oracle `B` and
   a **certificate** that `L_B` disagrees with every `M_i` at its stage.

**Decisive first measurement (passes/fails the fidelity-killer).** Compute, exactly:
`D(n)` (= `2^n`), `h(n,k)`, `n*(k)` for k=1,2,3. **Fidelity-killer:** if some depth-q tree
with `q < 2^n` computes the slice-OR (obstruction vacuous), or if the diagonalization
fails to certify disagreement against a budgeted machine, the model is INFIDEL → fires.
Predicted: killer PASSES (OR's deterministic depth is the full `2^n`; the headroom is
positive for every poly-k once `n > n*(k)`).

**Falsifiable hypothesis + declared killer (the lab's tension).**
- *Hypothesis L:* the relativization obstruction, read as a function of level n, is a
  genuine cross-level **leverage operator** (`h(n,k)` grows, the break-even schedule
  `n*(k)` is a real staircase) that is NOT a relabeling of one total bound.
- *Declared adversary kill:* everything reduces to the single total fact "the deterministic
  decision-tree depth of OR on m variables is m", instantiated at `m = 2^n`; then `h`,
  `n*` are mere arithmetic of `2^n` vs `n^k` = the textbook counting bound. That would be a
  **RESTATEMENT** — the lab's signature collapse, now in the relativization arena (this is a
  legitimate, sharpening result, not a failure).
- *KILLER (what would make it NON-collapsing):* a measured obstruction quantity that does
  NOT reduce to `depth(OR)` — candidate: the **online/freshness schedule** across stages
  (`separation.py` carries `next_min_length = max(n+1, max_query_length+1)`), i.e. the
  minimal length-schedule to diagonalize a *sequence* of machines without perturbing past
  stages, which is a cross-stage object single-function decision-tree depth does not see.
  Pre-commit: if that schedule too reduces to greedy arithmetic of the budgets, declare
  RESTATEMENT.

**Reuse, do not rebuild.** Build ON `pnp_lab/oracles` (`build_separating_oracle`,
`SeparationStage`, `EXAMPLE_MACHINES`). New file `pnp_lab/oracles/leverage.py` +
`tests/test_oracles_leverage.py` + `examples/run_oracle_leverage.py` + (on crystallization,
a RED gate) `docs/relativization-leverage.md`. Exact integers only; `py -m pytest`. Then
measure → Adversary (reduce-to-known / fidelity) → Evaluator (+ honesty boundary) →
Archivist.

## Discipline (inherited)

Repo conventions (doc EN-first + code/tests/example, `py -m pytest`, exact integers, no
floats, code/docstring Italian; README + memory + RESEARCH_LOG updated). Governance: the
**graduated gate** in `prompts/research-loop.md` (GREEN = pre-declared confound-control,
same arena, no claim/close; RED = pivot / new content / close / commit-scope; ≤3 GREEN
before a RED; stop on first RESTATEMENT diagnosis). Honesty boundary is BINDING: cite BGS,
never claim a separation, mark every finite-size artifact. **No P vs NP claim, ever** — the
deliverable is the barrier made measurable, i.e. why relativizing techniques cannot settle
the question.

## Run

State lives in `RESEARCH_LOG.md` + `memory/`. Launch Cycle 1 = Builder on the Explorer
hypothesis above.
