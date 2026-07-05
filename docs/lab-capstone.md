# THE ATTRACTOR THESIS — grand capstone of the autonomous lab

*Crystallized 2026-06-20. This is the **final, lab-level capstone** of the autonomous
research loop (`RESEARCH_LOG.md`, Entries 1–28). It sits **above** the two branch
capstones — [the Collapse Theorem](collapse-theorem.md) (CSP/algebraic branch) and
[the Cross-Level Survival Arc](cross-level-survival-arc.md) (Magnification Frontier) —
and states what **all** the lab's arenas have in common, what the single exception
shows, and **why the loop now stops**. It proves **no** lower bound and makes **no
claim about P vs NP** (neither `P ≠ NP` nor `P = NP`). It is one falsifiable statement
about the **method** on finite instances, backed entirely by code already in the repo.*

## The statement

> **THE ATTRACTOR THESIS (empirical).** Take any quantity the loop can measure
> **exactly** on tiny, exhaustively-enumerable instances, designed to separate
> objects a parent theorem calls equivalent and so carry *new* content toward a
> separation. Across **six independent arenas** it **collapses**, via an identity
> checked in code, into the **joint orbit-invariant dictionary** — a handful of
> known invariants `(cost, gf2_degree, sensitivity, block_sensitivity, …)` whose
> *total* classification theorem on the tiny instance answers first and absorbs the
> new quantity into its own verdict. The cause is **the regime, not the invariant**:
> **exact enumerability is the trap.** The *only* escape the loop found does not break
> the attractor with a new discriminant — it breaks the **symmetry** the dictionary
> rests on (a fixed variable order), and what it buys is **survival of a non-invariant
> signal, never leverage**: the escaped quantity persists across reachable levels but
> does **not grow**, and growth is exactly the asymptotic content that escapes tiny
> sizes by construction.

## The ledger (the whole evidentiary basis)

Fourteen collapses across six arenas, one falsification, one non-collapse, and the
four sampling outcomes that probed the non-collapse:

| outcome | what | module(s) |
|---|---|---|
| **14 RESTATEMENTs** | every exact tiny discriminant reduces to a dictionary invariant | duality-LP (18), proof-complexity (16), σ(cost) circuit-cost (6, 19), algebraic CSP / Inv–Pol (20), magnification locality (21, 23, 28), approximate degree (29) |
| **1 falsification** | a *falsifiable* composition conjecture broken on 4 bits (`OR₂∘XOR = J−I₄`, `Cov 4 / LP 3 / G★ 1`) | Exactness Composes (18) |
| **1 non-collapse** | the dictionary trap escaped by breaking the symmetry — `MBPSP[s]` = min-OBDD-size at a **fixed order** is **not** permutation-invariant; order-anisotropy `>0` at n=4, MCSP control flat | Order-Locality (22) |
| **survival-PASS @1 level** | the anisotropy survives to n=5 by Monte-Carlo/CRN (pooled z≈4.9, null control flat, killer does not fire) | Sampled Order-Anisotropy (24) |
| **survival-PASS @3 levels** | survives n=4,5,6 (z=73, z=43, control flat at each) on a recalibrated threshold | Cross-Level Median (25) |
| **2 control-PASS** | the two ways to argue the ceiling away are falsified: at fixed hard-fraction the n=5 peak persists (H-confound dead), and "no leverage" holds for every normalization (gauge-confound dead) | Iso-Hardness (26), Leverage Gauge-Invariance (27) |

The two branch capstones carry the per-arena identities; this capstone does not
re-derive them. Each reduction is an identity verified in its own module's tests.

## The three recurring collapse mechanisms

One per layer of the dictionary — stable across all six arenas:

1. **the derivative of a known object is still that object** — `d_flip` is the
   discrete gradient of MCSP-size (19); the optimal-split DAG is built from the cost
   table; the relativization "leverage" is `depth(OR_m)=m` plus arithmetic (28).
2. **a slice/cardinality of a known structure is still dictionary content** —
   `g(Γ)=|Pol₂^{comm,idem}|` is a clone-slice cardinality (20); `adeg` is reconstructible
   from the *joint* of four orbit-invariants (29).
3. **a width/level index inside a total dichotomy is the dichotomy relabeled** —
   `w*` is the width-1/width-2 step (Collapse Theorem); the certified order gap
   `2^{n/2+1}−(n+2)` is a finite instance of Bryant/Wegener (23).

## What the single non-collapse actually established

Module 22 is the lab's one genuine non-collapse, and the four sampling modules
(24–27) are the honest reading of it, defended from every side:

- **Survival is real and multiply-controlled.** A non-permutation-invariant signal
  (order-anisotropy of `MBPSP[s]`) is significant at every reachable level n=4,5,6.
  Three pre-registered confounds — n=4 artifact, hard-fraction drift, normalization
  choice — were each set as a killer; **none fired**.
- **Leverage is genuinely absent.** The effect is bounded and non-monotone, peaking
  at n=5, and that peak is **gauge-invariant** (holds for every normalization
  `α∈[0,1]`). Magnification needs a *growing* slope; this is a curve that rises then
  falls across the only three levels that exist.
- **Only three levels exist, by construction.** n=4 is the last exact level; n=5
  (`2^32`) and n=6 (`2^64`) need sampling; **n=7 is `2^128` truth tables** — out of
  reach. Three points cannot exhibit an asymptotic slope. The leverage stays
  **CITED** (Oliveira–Pich; Chen–Jin–Williams; McKay–Murray–Williams; CHRSV).

So even the escape confirms the thesis from the other side: breaking the symmetry
buys *survival* of new signal but not the *amplification* that would be new content
toward a separation — and the amplification is precisely what tiny exact sizes cannot
hold.

## Why the loop stops here (the strategist's ESC-2)

> **Addendum (Entries 31–33, 2026-06-22).** The three reopening doors below were listed
> as *predicted* closed at Entry 29. They have since been **exercised and closed** by
> human-launched cycles, all collapsing by the same signature: door **(A)**
> fixed-structure (bipartite rigidity, Entry 31), door **(C)** exact-lever-at-≥2-levels
> (lifting integrality gap, Entry 32), and door **(B)** a-priori-barrier (Entry 33). Door
> (B) was different in kind — it produced not a collapsing object but a
> **conditional-impossibility verdict** (no enumerable object is non-symmetric on the
> full group *and* closed-form-free *and* brute-forceable at ≥2 levels, forced by the
> {R1,R2} and {R2,R3} antagonisms) which a numerical assault on the
> `feasible_interp` arena tried and **failed** to falsify (best candidate perm-invariant
> 0/1500, split profile (0,0,0,24) over n=1..4). So **ESC-2 is now POST-HOC VALIDATED**,
> not merely predicted. **Crucially, this does NOT touch falsifier doors 2 and 3 below**
> (certified bounds at n≥7; *growing* cross-level leverage): those live past the
> brute-force wall and remain **genuinely open**. Ledger updated to **18 collapses (the
> 16th, 17th, and 18th — bipartite-rigidity / integrality-leverage / conditional
> meta-impossibility — are Entry-only redux/meta, not new arenas) / 7 arenas**.

On 2026-06-20 the autonomous strategist (the lab's Principal Investigator role)
applied the graduated gate and declared **ESC-2 — regimes exhausted**, escalating to
the human, who chose to **close the lab as a methodology**. The reasoning, verified
against the files:

- **A seventh exact arena would be RESTATEMENT #15 with probability ≈ 1** — it would
  fall into the joint dictionary, strengthening the thesis but adding no content. The
  loop's own discipline is to **decline a predicted restatement**, not grind it.
- **The three reopening doors are closed.** (1) A *second* order-dependent meta object
  (min-OBDD at optimal order, another fixed-structure decision diagram) predictably
  reproduces Module 22: it would break permutation-invariance but remain a statistic
  of the hard set with no cross-level leverage. (2) A level beyond n=6 is barred by the
  brute-force wall (n=7 = `2^128`; the faithful regime already degenerates at n≥6).
  (3) A genuinely new barrier requires a notion of obstruction with an *a-priori*
  reason to escape the joint dictionary — which the lab cannot manufacture from its
  own state without inventing new mathematics, exactly what the mandate forbids it to
  promise.

Reopening therefore needs a **structural external input** — a non-enumerable lever, or
a barrier provably outside the joint dictionary — supplied by a human. Absent that, no
further cycle adds content.

## The falsifier (what would overturn this)

The Attractor Thesis is falsifiable. It is broken by **either**:

1. a discriminant, measurable exactly on tiny instances, that separates two objects a
   parent theorem declares equivalent **and** is provably *not* reconstructible from
   the joint dictionary by an exact identity (the Module-19/29 falsifier — hunted
   exhaustively, **not found**); **or**
2. a measurement in the **genuinely non-enumerable** regime (high arity / large
   domain / level n≥7, via *certified bounds* rather than brute force) where the
   controlling theorem is *not* total, carrying content the theorem does not fix;
   **or**
3. a non-permutation-invariant escaped quantity that exhibits **growing cross-level
   leverage**, not merely survival — the open edge Module 22's arc could not reach.

Doors 2 and 3 are the honest open frontier and the reason this is a statement about
the **method**, not a closed theorem of complexity theory.

## Honesty boundary (binding for this repo)

- This is an **empirical, falsifiable statement about the method** of the loop on
  **finite, exactly-enumerable** instances. It is **not** a theorem of complexity
  theory, **not** a lower bound, and makes **no claim about P vs NP**.
- "Fourteen collapses across six arenas + one falsification + one non-collapse +
  survival/control PASSes" is exact and reproducible: every reduction is an identity
  checked in code (Modules 6, 16, 18–29 and `RESEARCH_LOG.md` Entries 1–28); the n=5/6
  numbers are **estimated** (Monte-Carlo, CRN, pooled over seeds) with the exact n=4
  anchor inside their CIs.
- The decisive regimes — non-enumerable certified bounds, level n≥7, and growing
  leverage — are **untested**. The thesis claims robustness *only* over the
  exactly-enumerable tiny regime and explicitly leaves the asymptotic / certified-bound
  regime open. That open door is the whole content of falsifier doors 2 and 3.
- The lab is a **methodology**: make a deep phenomenon run, exactly, on tiny
  instances, and report precisely where the asymptotic content escapes. It is **not**
  an attack on P vs NP, and never was.

## Files

```
docs/collapse-theorem.md            # branch capstone — CSP/algebraic (Entries 1–12)
docs/cross-level-survival-arc.md    # branch capstone — Magnification Frontier (Entries 13–24)
docs/tiny-instance-collapse.md      # σ(cost) arena (Module 19)
docs/invpol-collapse.md             # algebraic CSP arena (Module 20)
docs/locality-barrier.md            # magnification meta arena (Module 21)
docs/order-locality.md              # the one non-collapse (Module 22)
docs/sampled-order-n5.md            # survival-PASS @1 (Module 24)
docs/cross-level-median.md          # survival-PASS @3 (Module 25)
docs/iso-hardness.md                # control-PASS, H-confound (Module 26)
docs/leverage-gauge.md              # control-PASS, gauge-confound (Module 27)
docs/relativization-leverage.md     # relativization arena (Module 28)
docs/approx-degree.md               # approximate-degree arena (Module 29)
RESEARCH_LOG.md                     # Entries 1–29 — the full audited trail
```

## Post-scriptum — the second arc of reopenings and the meta-collapse (Entries 30–38)

*Added 2026-07-05. No code was changed; this section records a sequence of human-launched
cycles and their shared outcome.*

After Entry 29, the lab was reopened eight times on human levers and traversed Entries 30–37,
all ending in KILLED / RESTATEMENT (#15 through #22) across the same 7 arenas. The arc covers:
Module 30 (7th arena, GCT/Kronecker, Entry 30); the bipartite-rigidity instantiation of lever A
(Entry 31); the integrality-gap instantiation of door C (Entry 32); the conditional-impossibility
verdict of door B (Entry 33); the Kronecker local-obstruction stretch probe (Entry 34); the
exact rational moment-cone probe (Entry 35). Every internal reopening door (A, B, C) was
exercised and closed by the same structural signature that ESC-2 had predicted.

The most ambitious attempt — turning the collapse signature itself into an executable object —
spanned Entries 36–37 (the "meta-pivot" of the fable-frontier program). The invariant lattice
(Entry 36) collapsed via real-degree omission and group-mismatch. The collapse ledger (Entry 37)
collapsed auto-referentially: the codebook shared vocabulary with the corpus it classified, the
type curve was in an ascending phase at n=21 (stationarity of Good-Turing violated), and the
dominant type PERM-ABSORBED contained ~3–4 false positives from a mathematical noun misread as a
mechanism. The ledger of collapses died by omission of type, granularity mismatch, and circular
codebook — exactly the mechanisms it catalogued. This extends the Attractor Thesis to the
meta-level and re-confirms ESC-2 beyond the original prediction.

**Final ledger (Entry 38):** 22 collapses / 7 arenas + 1 falsification (Module 18) + 1
non-collapse (Module 22) + survival-PASS@1 level (Module 24) + survival-PASS@3 levels
(Module 25) + 2 control-PASS (Modules 26–27). The 7th through 22nd collapses are Entry-only;
no new Module was produced in the second arc.

**Reopening criteria (tightened).** The lab reopens only on a structural external input that
satisfies at least one of: (1) a new arena entirely outside the current repo with an
a-priori reason to escape the joint dictionary; (2) a certified object past the d≥7 / n≥5
brute-force wall, not reducible to known inequalities or existing closed-formula families;
(3) an independent algorithmic falsification of the Attractor Thesis (a discriminant measurable
exactly, not reconstructible from the joint dictionary by an exact identity). The falsifier doors
2 and 3 of the original capstone remain genuinely open on these same terms.

**Operational note.** The fable-frontier loop (prompts/fable-frontier.md) documented a reusable
methodology: strategic framing by a capable model (Fable 5 / equivalent), execution by economical
models (sonnet / haiku). Both meta-pivot cycles were run under this protocol. The protocol is
reusable; the program is closed.
