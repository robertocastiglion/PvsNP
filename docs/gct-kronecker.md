# Module 30 — GCT / Kronecker: the 7th-arena collapse (outside Boolean function theory)

*Crystallized 2026-06-20. This cycle **REOPENED** the lab after the grand capstone
"The Attractor Thesis" ([lab-capstone.md](lab-capstone.md), Entry 29) had closed it as a
methodology — because the human injected the one reopening lever the capstone itself named:
**falsifier door 3 / a structurally external, brand-new barrier**. It proves no lower bound
and makes **no claim about P vs NP, Kronecker positivity, or GCT obstructions**. It is the
**15th collapse, in a 7th independent arena — the first OUTSIDE the theory of Boolean
functions** (the objects are representation-theoretic multiplicities of `S_d`). The Attractor
Thesis is **strengthened, not refuted**, and crystallizes the CITED→COMPUTED conversion of
the evaluator's load-bearing flag.*

## The object (exact, a genuinely different arena)

The **Kronecker coefficients** `g(λ, μ, ν)` of the symmetric group `S_d` — the
multiplicities in the tensor product of two irreducibles,
`χ^μ ⊗ χ^ν = Σ_λ g(λ,μ,ν) χ^λ`. Deciding `g(λ,μ,ν) > 0` is **NP-hard** (Ikenmeyer–Mulmuley–
Walter / Pak–Panova): there is *no* known polynomial necessary-and-sufficient combinatorial
rule. This is the central object of the **Geometric Complexity Theory (GCT)** program for
`VP ≠ VNP`, where "GCT obstructions" are *representation-theoretic occurrences* (vanishing /
non-vanishing patterns of such multiplicities). The lab had never left Boolean function
theory before; here the objects are partitions of `d` and `S_d`-character values.

`g` is computed **exactly** (integer, `Fraction` with `assert denom == 1`) via a self-
contained character engine: `mn_character` evaluates irreducible characters by the
**Murnaghan–Nakayama rule**, and `kronecker(λ,μ,ν)` is the exact inner product
`(1/d!) Σ_α z_α^{-1} χ^λ_α χ^μ_α χ^ν_α` over conjugacy classes `α ⊢ d`. Green anchors,
all verified in code:

- `χ^λ(1^d)` = hook-length dimension (`hook_length_dimension`);
- `Σ_λ (dim χ^λ)² = d!`;
- `g([d], μ, ν) = δ_{μν}` (tensoring with the trivial);
- `g(λ, [1^d], ν) = δ_{ν, λ'}` (tensoring with the sign, `λ'` = transpose);
- total `S_3` symmetry of `g` in its three arguments;
- `g ≥ 0` everywhere.

## The hypothesis and its killer

**Lab hypothesis (explorer):** on tiny `d`, the *vanishing pattern* of `g` (the set of
triples with `g = 0`) **collapses** into the known elementary **necessary conditions (NCs)**
for non-vanishing — partition-shape statistics. **Pre-declared killer:** a **sporadic
vanishing** — a triple with `g = 0` yet **all** NCs satisfied — would be content *outside the
dictionary* = a survival.

The predictor `v_pred` uses exactly **two** solid NCs (`nc_length` + its conjugate
`nc_maxpart`, the Dvir length-/max-part bounds): a dominance-style third NC was tried and
**discarded** because it produced false positives already at `d = 3` (better two correct NCs
than three with one broken). The control `nc_false_positive(d)` — triples with `g > 0` but a
NC declaring vanishing impossible — is **empty everywhere on d ≤ 6**, confirming the two NCs
really are necessary on this range (no NC bug masquerading as the killer).

## The decisive measurement (exact, d ≤ 6)

`sporadic_vanishing(d)` (`g = 0` with every NC satisfied — the killer):

| d | #sporadic_vanishing | #nc_false_positive |
|---|---------------------|--------------------|
| 3 | 0                   | 0                  |
| 4 | 2                   | 0                  |
| 5 | 5                   | 0                  |
| 6 | 44                  | 0                  |

Regenerate: `py examples/run_gct_kronecker.py`, or in Python
`from pnp_lab.gct_kronecker import sporadic_vanishing, nc_false_positive`.

So with only the two weak elementary NCs the killer **does fire** from `d = 4` on — an
apparent survival. The Adversary's verdict, below, shows it is an artifact of the weak NC set.

## Verdict — RESTATEMENT-by-collapse (the 15th collapse, 7th arena)

**Adversary: KILLED.** Both character engines agree (the integers are double-checked). The
"survival" is an artifact of restricting the predictor to two *elementary* NCs: **every**
sporadic vanishing is a zero in a family for which an **explicit closed Kronecker formula is
already known** — Rosas (two-row / hook), the classical `std ⊗ std` decomposition,
Bessenrodt–Bowman (rectangles). The reduction is a **pincer**: *per-collapse* (each sporadic
triple is a zero inside a known-formula family) **and** *per-hardness* (the insufficiency of
elementary NCs is exactly Pak–Panova: deciding `g > 0` is NP-hard, so no elementary statistic
can be complete). The genuine killer — a triple whose three partitions are *simultaneously*
non-hook / non-two-row / non-two-column / non-rectangle under **every** `g`-symmetry — only
appears at **d ≥ 7**, the same brute-force wall every other branch of the lab hit.

**Evaluator: RESTATEMENT #15**, rule B2 (re-strategize, do not iterate). **Load-bearing
flag:** the closing step "`uncovered = 0`" was **CITED, not computed**.

## Closing the flag: CITED → COMPUTED

`coverage.py` converts the load-bearing flag into a computed measurement. Exact shape
predicates `is_two_row` / `is_two_column` / `is_hook` / `is_rectangle` / `special_shape`; the
`g`-symmetry orbit `g_orbit` (the `S_3 × V_4` action: simultaneous permutation of the three
arguments **and** simultaneous conjugation of two of them — exactly the symmetries under which
`g` is invariant); and `covered(triple)` = there exists an orbit representative with **≥ 2 of
the three arguments `special_shape`** (the *structural precondition* under which the known
closed formulas yield the value, hence certify any vanishing). Because `g` is **constant on
the whole `g`-symmetry orbit** (a property tested directly, as a bug-killer), it suffices that
the paired special-shape structure appear in *one* representative.

Measured **in-repo, COMPUTED** (`coverage_summary(d) = (#sporadic, #covered, #uncovered)`):

| d | #sporadic | #covered | #uncovered |
|---|-----------|----------|------------|
| 4 | 2         | 2        | 0          |
| 5 | 5         | 5        | 0          |
| 6 | 44        | 44       | 0          |

⇒ **`uncovered == 0` everywhere on d ≤ 6**: every sporadic vanishing falls under the
structural precondition of a known closed formula. The collapse is now **COMPUTED, not merely
CITED**, lifting the evaluator's robustness from ~6.5 toward ~8. Regenerate:
`py examples/run_gct_kronecker.py` (the `#covered / #uncovered` lines), or
`from pnp_lab.gct_kronecker import coverage_summary`.

## Honesty boundary

**COMPUTED exactly** (integer arithmetic, `Fraction` with `assert denom == 1`): the Kronecker
coefficients `g(λ,μ,ν)` for all triples of partitions of `d ≤ 6` (Murnaghan–Nakayama, two
independent character engines cross-checked); the green anchors (`χ(1^d)` = hook dimension,
`Σ dim² = d!`, `g([d],μ,ν)=δ_{μν}`, `g(λ,[1^d],ν)=δ_{ν,λ'}`, full `S_3` symmetry, `g ≥ 0`);
the two necessary conditions with `nc_false_positive = []` on d ≤ 6; the sporadic-vanishing
counts `2, 5, 44`; and — now — the **coverage precondition** `uncovered = 0` (the exact,
elementary, testable shape predicate over the `g`-symmetry orbit).

**CITED, never re-proved:** the **values** of the closed Kronecker formulas (Rosas
two-row/hook, the classical `std ⊗ std` decomposition, Bessenrodt–Bowman rectangles) as
parent theorems; the Pak–Panova / Ikenmeyer–Mulmuley–Walter **NP-hardness** of deciding
`g > 0`. The repo **computes the structural precondition** under which those formulas apply
(`≥ 2` special-shape arguments on the orbit) and **cites the value** the formulas then assign —
that is the documented boundary; it does **not** recompute the formula values.

**NOT shown:** any statement about Kronecker positivity, GCT obstructions, or P vs NP; any new
separating content. The genuine out-of-dictionary discriminant (a triple non-special under
every `g`-symmetry) lives at **d ≥ 7** = the same brute-force wall as every other branch.
Tiny-instance only (d ≤ 6 exhaustive). **No separation, no P vs NP claim.**
