# Program — the Magnification Frontier (executable)

New research program, opened 2026-06-14 after the CSP/algebraic branch closed
(`docs/collapse-theorem.md`, RESEARCH_LOG Entries 1–12, ten collapses). Human PI
chose direction ① (hardness magnification + the locality barrier).

> **STATUS (2026-06-15).** The **locality-barrier sub-branch is CLOSED** —
> crystallized as **Module 21** (`docs/locality-barrier.md`), RESEARCH_LOG Entries
> 13–15. Two cycles (staircase ρ=1; fixed-fraction level-invariance) both collapsed:
> the locality *mechanism* is faithfully exact (genuine `N`-junta), but every
> *leverage* quantity reduces to a global statistic of the hard set, because
> `MCSP[s]` is permutation-invariant.
>
> **REOPENED — Cycle 3 (Entry 16, human-launched candidate ①).** The reopening
> criterion is MET: `MBPSP[s]` = min-OBDD-size at a **fixed variable order**
> (HARD = "no small OBDD") is the non-permutation-invariant meta object. Built
> `pnp_lab/meta_complexity/order_locality.py` (+ tests + example). Decisive measure:
> the pair-influence spread within a Hamming-weight class is `0,0 / 0,0,0 /
> 184,176,16,0` at `n=2,3,4` (ORDER SURVIVES at n=4), vs the MCSP formula control
> flat (`0,0,0,0`); robust across thresholds `s∈[5,10]`. FIRST non-collapse outcome.
>
> **Cycle 4 (Entry 17) — the order REACHES the program's faithful wall.** Ran the
> Module-21 certification wall (`locality.certified_k_local`, cross-checked:
> `max_pairs certified_drop == certified_k_local(N-2) == 152` @n3) on `MBPSP[s]` at
> j=2 (j=1 isotropic by construction). The wall-anisotropy spread is `0,0,0` @n3 and
> `144,144,16,0` @n4 (WALL SEES ORDER), MCSP control flat — the maximization over
> coordinate-sets is genuinely non-vacuous on MBPSP, INDEPENDENT of Cycle-3's custom
> measure. Reopening DOUBLY validated.
>
> **STOP-and-ask — the program has hit its tiny ceiling.** The order-asymmetry is
> established at n=4 on two independent measures, but the LEVERAGE across levels
> (small LB → big separation) is asymptotic and escapes n=5+ (2^32 truth tables) by
> construction. Recommended: crystallize Cycle 3+4 as **Module 22** ("Order-Locality:
> the barrier made non-invariant") — an honest, positive close. No auto-cycle.

## Why this program is DIFFERENT from the loop that just closed

The CSP loop was a **discovery** loop: it hunted for a *local discriminant with new
content*, and the adversary's job was to reduce it to a known theorem. It collapsed
ten times — that is the honest finding (the Collapse Theorem). **Do not run this
program the same way.** Hunting for "new content" on tiny instances will collapse
again, by the very theorem we just proved empirically.

Instead, run it like Modules 1–12: **make a known, deep, asymptotic phenomenon
RUN — exactly — on tiny instances.** The deliverable is an *executable, faithful,
tangible* model of the magnification frontier, NOT a separation and NOT new content.
This is legitimate precisely where the CSP loop was not, because:

- **Tiny is on-model here.** Magnification is about circuits computing **MCSP/MKtP
  themselves**, whose input is the `N = 2^n`-bit truth table. For `n = 3`, `N = 8`;
  the meta-function and weak circuit lower bounds on it are *exactly* computable
  (Module 6/13 territory). The asymptotics are cited; the *mechanism* is run.

## The success criterion (and the adversary's new job)

A cycle SUCCEEDS if it produces an exact, reproducible, **faithful** executable
model of a piece of the magnification frontier — even though it proves nothing new.

The **adversary's job changes**: not "does this reduce to a known theorem?" (of
course it does — it IS the known theorem, made runnable) but **"is the executable
model FAITHFUL, or a misleading toy?"** Attack vectors:
- **Infidelity**: the tiny model exhibits behavior that does NOT actually reflect
  the theorem (wrong direction of the implication, a finite-size artifact sold as
  the mechanism, the "amplification" being trivial at this size).
- **Vacuity**: the model is technically correct but shows nothing the asymptotic
  statement contains (e.g. the threshold is invisible at `n = 3`).
- **Over-claim**: the doc/comment claims more than the tiny instance licenses.
The evaluator scores **fidelity + tangibility**, and writes the honesty boundary
(what is cited vs computed, where the asymptotic content escapes tiny size).

## The leverage principle (the cake's third cut) — BINDING reframing

A cake cut three times yields 8 pieces only if the third cut is **horizontal** —
in a dimension the problem statement never forbade. The Collapse Theorem showed our
ten failed cycles were all **vertical** cuts in the same plane ("measure an exact
property of a small object"), absorbed by a *total classification theorem* — the
ceiling. The escape is the dimension **with no ceiling**: the **meta level /
self-reference**. There is no total classification theorem for MCSP's own
complexity (we do not even know if MCSP is NP-hard), so the collapse has nothing to
absorb the measurement with. That is *why* magnification is the right instinct: it
cuts upward, into functions-of-truth-tables.

The cake also dictates **what to measure**. The value of the horizontal cut is not
the size of any one slice — it is the **multiplication**. So:

> **Measure the LEVERAGE, not the step.** Do not measure a static wall at a single
> `n`. Measure the **amplification operator itself** — how the quantity grows across
> levels `n = 2 → 3 → 4`: the slope of the staircase, its growth rate, whether it
> has a fixed point. Magnification *is* a doubling operator; render the operator
> exact on tiny instances, not a single snapshot of one of its outputs.

This also upgrades the fidelity-killer: a wall that is "invisible at `n=3`" is not a
failure — it is a *measurement of where the staircase starts*; you read it by
climbing, not by standing still.

## Two sub-targets (Explorer picks ONE per cycle, declares its fidelity-killer)

- **A — the amplification mechanism.** Make the self-reduction / anti-checker
  structure that makes a *weak* lower bound for gap-MCSP/MKtP **amplify** into a
  strong separation run on exact tiny instances. Show the blow-up concretely.
  *Parent theorems (cited):* Oliveira–Pich 2019; Chen–Jin–Williams 2019/2020;
  McKay–Murray–Williams 2019.
- **B — the locality barrier (closer to the lab's DNA).** Make "a lower-bound
  argument is **local** (inspects only `k` bits / is a small-fan-in/streaming/
  small-space proof)" an **exact, measurable** property on tiny instances, and
  exhibit the **counting obstruction** by which local arguments cannot cross the
  magnification threshold. This is to the magnification barrier what Module 1 is to
  Natural Proofs: it makes the wall measurable. *Parent (cited):* Chen–Hirahara–
  Ren–Santhanam–Vyas; Chen–Jin–Williams "sharp threshold".

## Discipline (inherited)

Repo conventions (doc EN-first + code/tests/example, `py -m pytest`, exact integers,
no floats; README + memory updated). Each cycle: Explorer (hypothesis + **fidelity**
-killer) → Builder (exact runnable model + tests) → measure → Adversary (fidelity/
vacuity/over-claim) → Evaluator (fidelity+tangibility score + honesty boundary) →
Archivist. Honesty boundary is BINDING: cite the asymptotic theorems, never claim a
separation, mark every finite-size artifact. No P vs NP claim, ever.

## Cycle 1 — IN PROGRESS (Explorer DONE, Builder paused on session limit 2026-06-14)

Sub-target **B (locality barrier)**, reframed by the leverage principle above.

**Explorer hypothesis (done).** The magnification object is the meta-function
`MCSP[s]: {0,1}^N → {0,1}`, `N = 2^n`, input = the `N`-bit truth table. At `n=3`,
`N=8`, `MCSP[s]` is an exact 8-bit Boolean function (already in `min_formula_sizes(3)`,
256 inputs). Make exact and measurable:
- **loc / relevant coordinates** — a `k`-local argument decides `MCSP[s]` inspecting
  only `k` of the `N` truth-table bits (a `k`-junta). `loc(MCSP[s])` = min `k`;
  relevant coords = bits `i` with a pair differing only in `i` that flips the output.
- **A(k)** — best `k`-local classifier: `max_S Σ_fibers max(#hard, #easy)` over coord
  sets `|S|=k` (at `N=8`: `Σ C(8,k)=256`, trivial to enumerate).
- **obstruction** — the wall as integers: `(k, A(k), H, H−A(k))`, `H = #{hard}`.
  At `n=3, s=4`: `H = #{cost>4} = 50`.

**PI reframing (the cake — BINDING for the Builder).** Do NOT freeze the wall at a
single `n=3`. Build `obstruction` as a **function of `n`** (n=2 → N=4, n=3 → N=8,
n=4 → N=16) and measure the **leverage**: how `loc`, `H`, and the gap `H−A(k)` GROW
per level — the slope of the staircase, not one step. The deliverable is the
amplification operator made tangible across levels, with the single-`n` table as a
slice of it.

**Decisive first measurement (passes/fails the fidelity-killer).** Compute
`relevant_coordinates(MCSP[4], N=8)`. If 8/8 → `MCSP[4]` is a genuine 8-junta, killer
PASSED, proceed. If ≤3 → KILLER-FID fires (barrier invisible at `n=3`); per the
leverage principle that is not failure — record it and CLIMB to `n=4` (N=16:
`MCSP[s]` over 16 bits is one function on `2^16=65536` inputs, enumerable for one
threshold; the `n=4` cost table already exists from `min_formula_sizes(4)`).

**Feasibility note.** `A(k)` at `N=16` enumerates `Σ C(16,k)` coord sets — fine for
small `k`, mark `slow` for large `k`. Keep everything exact integers.

**Files to create:** `pnp_lab/meta_complexity/locality.py` + `tests/test_locality.py`
+ `examples/run_locality.py`. Reuse `pnp_lab/circuits` (ComplexityTable) and
`pnp_lab/meta_complexity/frontier.py`. Then measure → Adversary (fidelity/vacuity/
over-claim, + does the LEVERAGE grow faithfully or is it a finite-size artifact?) →
Evaluator (fidelity+tangibility, honesty boundary) → Archivist.

## Run

Launch the Explorer with sub-target A or B (Cycle 1 = B, in progress above). State
lives in `RESEARCH_LOG.md` + `memory/`, as always.
