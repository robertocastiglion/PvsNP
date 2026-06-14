# Module 21 — Locality Barrier (Magnification Frontier): the wall made exact, and why the leverage collapses

*Crystallized 2026-06-14. This closes the **locality sub-branch** of the executable
Magnification Frontier program (`RESEARCH_LOG.md`, Entries 13–14; `prompts/
magnification-frontier.md`). It does **not** prove a lower bound and makes **no claim
about P vs NP**. Like Module 1 (Natural Proofs) it makes a **citable wall an exact
integer**; unlike a discovery, its two cycles both collapsed, and this note states
**what was faithfully exact** and **why the leverage carried no new content** — the
fifth arena of the [Collapse Theorem](collapse-theorem.md), now at the **meta level**.*

## The object (faithful, exact)

Hardness magnification (Oliveira–Pich 2019; Chen–Jin–Williams 2019/2020;
McKay–Murray–Williams 2019) says barely super-linear lower bounds for gap-MCSP / MKtP
would *amplify* into `NP ⊄ P/poly`; they stay unproven because the known techniques are
**local** and a counting obstruction (the *locality barrier*: Chen–Hirahara–Ren–
Santhanam–Vyas) blocks any local argument from crossing the magnification threshold.

We make one finite slice exact on the meta-function itself:

> `MCSP[s] : {0,1}^N → {0,1}`, `N = 2^n`, input = the **whole truth table** of an
> `n`-bit function read as `N` coordinates; `HARD = (exact min formula size > s)`
> (reusing Module 6, `min_formula_sizes`); `H = #{hard}`.

Exact, integer/rational measures (`pnp_lab/meta_complexity/locality.py`):
`relevant_coordinates`/`loc` (junta), `certified_k_local(k)` = # hard instances a
`k`-local argument certifies **with certainty** (its `S`-fibre is pure-hard), the
`obstruction` table, and the **leverage** across levels `n = 2,3,4` (n=4 cached in
`.cache/ct4.pkl`).

**The mechanism is real and faithfully exact.** `MCSP[s]` is a *genuine* `N`-junta
(`loc = N`: 4/4, 8/8, 16/16 — the fidelity killer passes, the wall is not a toy), and
`certified(k)` stays low and reaches `H` only at the full junta `k = N`. That gap is the
counting obstruction in miniature. What follows is about the **leverage** — the quantity
meant to carry magnification content *across* levels — not about this mechanism.

## Two cycles, two collapses

| cycle (Entry) | leverage hypothesis | exact measurement | collapsed to |
|---|---|---|---|
| C1 (13) | hardest-band `s=maxcost−1`: `ρ = k*/N = 1` at every level, `k*` doubling 4→8→16 | `k* = 4, 8, 14`; `ρ = 1, 1, 0.875` | a **degenerate-band artifact**: `H = 2, 2, 114` (non-monotone). `ρ=1` at `n≤3` only because the hardest band is the 2-element set {parity, ¬parity}, so no `(N−1)`-subset has a pure-hard fibre |
| C2 (14) | fixed-fraction `s=round(maxcost·θ)`, θ=0.5: the normalized curve `c(j)=certified(N−j)/H` is a **level invariant** | `c(1) = 8/25` (n=3) ≠ `8990/12977` (n=4); `c(2) = 4/25` ≠ `6068/12977` | the **average sensitivity / hypercube edge-density** of the hard set; its growth is trivial concentration + a threshold artifact |

## The structural cause (why a third cycle would collapse too)

`MCSP[s]` is **invariant under permutation of its `N` coordinates**. Therefore
`certified(N−1)` is *identical for every choice of dropped axis* (measured: all 16 axes
give `17980` at n=4, all 8 give `16` at n=3) — the `max over |S|=k` "best `k`-local set"
is **vacuous at `j=1`**, and `c(1)` reduces exactly to a **global statistic**:

> `c(1) = 2·E_axis / H = 1 − AvgSensitivity_restricted / N` = the edge-density of the
> hard set in the hypercube — a textbook Fourier/influence quantity, **not** a locality
> effect.

The observed "growth with `n`" is reproduced by a random-hard-set concentration null
model `c(j) ≈ 2^j · p^(2^j − 1)`, and θ=0.5 does **not** hold the density fixed across
levels (`p ≈ 0.195` at n=3 vs `0.396` at n=4), so the cross-level comparison is between
unmatched densities. For `j ≥ 2` the maximization is **not** vacuous (e.g. at n=3 the
pairs give `certified(N−2) ∈ {0,8}`, max bites), but the **excess over the null model
still grows** (`0.130 → 0.219`), so no level-invariant signal survives there either.

Hence the general obstruction: because `MCSP[s]` is symmetric in its coordinates, **any
"best `k`-local" discriminant collapses to a symmetric function of the hard set** — a
global statistic (sensitivity, edge-expansion, concentration), i.e. a dictionary object.
This is why the sub-branch is closed rather than iterated.

## Decision: the locality sub-branch is CLOSED

Per the loop's stop rule (two consecutive collapses with no plausible in-regime
direction) and the human PI decision (2026-06-14), the locality sub-branch **stops**.
Both collapses reduce to global statistics of the hard set; the cause is structural
(permutation-invariance), not a parameter choice, so a third threshold/normalization
would fall in the same class. Reopening the *program* (not this sub-branch) would
require a meta-level object that is **not** permutation-invariant, or a measure that is
**not** a global statistic of the hard set — otherwise it re-enters the dictionary.

## Honesty boundary (binding for this repo)

- **COMPUTED here** (exact integers / rationals, no floats on the critical path): the
  meta-function `MCSP[s]` as a genuine `N`-junta, `certified(k)`, the obstruction table,
  and the leverage `k*`, `ρ`, `c(j)` for `n = 2,3,4`. All numbers are reproduced
  independently and frozen in `tests/test_locality.py`.
- **CITED, never computed**: the asymptotic magnification theorems and the locality
  barrier proper. At finite `n` the "threshold" is a single integer, not a regime; the
  amplification (small LB → big separation) is asymptotic and **escapes tiny size by
  construction**. We exhibit the *mechanism* (local arguments cannot certify hard
  instances below the full junta), not the amplification.
- The two cycles establish a **faithful negative**: the locality *mechanism* is exact,
  but every *leverage* quantity built across levels reduces to a known global statistic
  of the hard set (band size/spread; average sensitivity / edge-density). This is the
  fifth arena of the Collapse Theorem, seen at the meta level. **No `P ≠ NP` or
  `P = NP` claim is made or implied.** A measurement method, not a result.

## Files

```
pnp_lab/meta_complexity/locality.py   # MCSP[s] meta-function, loc/junta, certified(k),
                                      #   obstruction, leverage; fixed_fraction policy
tests/test_locality.py                # exact frozen numbers (11 fast + 2 slow, cache)
examples/run_locality.py              # the wall + both cycles, printed exact
docs/collapse-theorem.md              # the capstone this 5th arena extends
RESEARCH_LOG.md                       # Entries 13–14 — the full audited trail
.cache/ct4.pkl                        # n=4 ComplexityTable (gitignored, rebuildable)
```
