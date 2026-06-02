# P/NP Research Lab

An executable, modular toolkit that makes the pillars of the **P vs NP** problem
**tangible, runnable and verifiable** — including the *barriers* that every proof
attempt must overcome.

---

> ### 🇮🇹 Arrivi da YouTube?
> Vai alla **[dashboard interattiva in italiano](https://robertocastiglion.github.io/PvsNP/)** —
> il sito divulgativo del progetto (canale *La Logica dei Sistemi*), con la
> spiegazione semplice di P vs NP, le tre barriere e tutti i moduli.
>
> ### 🇬🇧 For the Scientific & Lean community
> This repository contains the **executable toolkit for the P vs NP barriers**:
> Python modules that *run* the relativization / natural-proofs / algebrization
> obstructions and the lower bounds that *do* work, plus a **Lean 4**
> formalization with **34 kernel-verified theorems**, zero `sorry`, and **no
> `Classical.choice`**. Architecture, modules and build instructions below.

---

> **Intellectual honesty first.** This project does **not** "find the proof" of
> P vs NP. Nobody knows how to, and we have proofs of *why* the obvious approaches
> fail (relativization, natural proofs, algebrization). What this toolkit does is
> turn those barriers from abstract concepts into **tools that run**: code that,
> given a candidate idea, tells you whether it falls into a known trap — and that
> also shows where lower bounds *genuinely* work.

## Modules

| # | Module | Status | What it does |
|---|--------|--------|--------------|
| 1 | **Natural Proofs Analyzer** | ✅ | Given a combinatorial property of Boolean functions, checks whether it is *constructive* and *large* — i.e. whether it falls into the Razborov–Rudich barrier and therefore **can never separate P from NP**. |
| 2 | **Oracle Separation Sandbox** | ✅ | Builds, by diagonalization, an oracle `B` with `P^B ≠ NP^B` (executed and verified) and uses the PSPACE-complete oracle TQBF to illustrate `P^A = NP^A`. Makes the **relativization** barrier visible. |
| 3 | **Knowledge Graph** | ✅ | A navigable, queryable graph of barriers, approaches, techniques, results and open problems (with references). Knows who blocks whom, who evades whom, and the promising "frontier". Exports Markdown/JSON/Graphviz **+ SVG** in the brand palette. |
| 4 | **Lean 4 Formalization** | ✅ | Rigorous definitions (P, NP, reductions, NP-completeness) and **34 kernel-verified theorems**. Abstract core (zero axioms): `P ⊆ NP`, reductions as a preorder, Cook collapse **and its characterization** (`L∈P ↔ P=NP`), the relativization barrier. **Towards Cook–Levin**: a concrete "unbounded" `Model` where **P = NP by brute force** (`collapse_world_exists`), **concrete CNF-SAT** with its NP-form and a verified reduction, and the **heart of Cook–Levin** (`canonical_correct`: local constraint → CNF). **Razborov–Rudich core** (`NaturalProofs.lean`): Boolean functions as truth tables (count verified `2^(2^n)`), `Useful`, `Large`, abstract `Constructive`, and the **barrier as a theorem** (`rr_barrier`: if cryptography is secure, no natural proof exists). Zero `sorry`; only `propext`/`Quot.sound`, never `Classical.choice`. See `formalization/`. |
| 5 | **Proof Complexity Lab** | ✅ | The other half of the story: a lower bound that **actually works**. Refutes the pigeonhole principle (PHP) with resolution/DPLL and measures proof size, which grows **exponentially** (1·3·11·47·239·1439… nodes — Haken 1985). Via Cook–Reckhow this is a route to `NP ≠ coNP ⇒ P ≠ NP`. SVG output. `pnp_lab/proof_complexity/`. |
| 6 | **Circuit Complexity Sandbox** | ✅ | Two **exact** circuit lower bounds. *Shannon spectrum*: minimal formula size of **all** small functions (almost all hard, yet none explicit). *Parity wall*: the minimal DNF of parity has exactly `2^(n−1)` terms — the exact base case of "parity ∉ AC⁰" (Furst–Saxe–Sipser, Håstad), which **bypasses the Natural Proofs barrier**. Two SVGs. `pnp_lab/circuits/`. |
| 7 | **Algebrization Sandbox** | ✅ | The **third barrier** (Aaronson–Wigderson 2008), executable. *Multilinear extension* of a Boolean function over GF(p) + the *sum-check* protocol (the engine of **IP = PSPACE**) actually run: verifies a sum over `2^n` terms with **a single query**, honest prover accepted and cheater exposed (soundness ≤ d/p). The technique that **bypasses relativization**. SVG output. `pnp_lab/algebrization/`. |
| 8 | **Switching Lemma Lab** | ✅ | Håstad's **switching lemma** in action — the mechanism behind "parity ∉ AC⁰". Random restrictions collapse a width-`w` DNF (empirical check of `Pr[D ≥ s] ≤ (5pw)^s`) while **parity resists** (its optimal decision-tree depth stays = #free vars). **Now iterated in depth `d`** (`circuit.py`, `iterate.py`): chaining the switching level-by-level collapses a real depth-`d` AC⁰ circuit, with the exact invariant `D(parity) = #free` under the *same* restriction, and the quantitative threshold `n ≳ 5^(d−1)·w^d ⇒ size ≥ 2^Ω(n^(1/(d−1)))` (Håstad's asymptotic constant cited). See `docs/switching-profondita-d.md`. SVGs. `pnp_lab/switching/`. |
| 9 | **Algebraic Query Model** | ✅ | The **"algebraic worlds"** of the algebrization barrier (extends Module 7), with **Schwartz–Zippel** over GF(p) verified exactly. *Power world*: detecting a planted bit costs `2^m` Boolean queries but **one** algebraic query (prob. `(1−1/p)^m`). *Limit world*: determining the oracle still needs ~`2^m` queries — an **exact interpolation lower bound** over GF(p), with an adversary exhibiting two indistinguishable oracles. SVG. `pnp_lab/algebraic_worlds/`. |
| 10 | **Algebraic Separation** | ✅ | The **query-complexity core of `P^Ã ≠ NP^Ã`** (the algebraic analogue of Module 2). For OR: the **NP** side = *one* query (guess the witness, check on the cube); the **P** side = exact lower bound **κ** via a **cancellation adversary**. **Now lifted** (`lift.py`, step #1): that adversary becomes the gadget of a real **diagonalization** that builds an oracle `O` and a language in **`NP^Ã \ P^Ã`** — verified by re-running each diagonalized machine against the fixed oracle. The theorem over *all* machines and the **strong version** (communication-complexity lower bound) are the **Aaronson–Wigderson** result, cited. See `docs/lift-query-to-tm.md`. SVGs. `pnp_lab/algebraic_separation/`. |
| 11 | **Proof-Search Lab** | ✅ | **Transparent** proof-search (AlphaProof/LeanDojo style) over a **sound** equational-rewriting mini-prover. A best-first loop explores the proof space guided by a **policy** proposing tactics; every found proof is **re-verified**. Honest metric: a better policy *generates fewer states* (heuristic 68 vs baseline 243). The **LLM is an optional, pluggable policy** (`LLMPolicy`), **never on the verified path**: the core needs no networks or keys. Does **not** prove P vs NP. SVG. `pnp_lab/proof_search/`. |
| 12 | **Algorithmic Method Lab** | ✅ | **Ryan Williams' method** (NEXP ⊄ ACC⁰, 2011): "a SAT algorithm faster than brute force ⇒ a lower bound" — the only approach that **bypasses all three barriers**. Exact executable core: structured circuits have **sparse polynomials**, so `#SAT` over all `2ⁿ` inputs is counted *without enumerating them* (AND: 4096× faster; dense OR: no gain), plus the **win-win chain** and the **super-polynomial** threshold. **Explicit depth-2 #SAT** (`depth2.py`): a DNF solver via inclusion–exclusion, `O(2^m)` instead of `O(2^n)`, with **measured timings** (~38000× at m=4). Easy Witness Lemma, PCP, hierarchy, and the real ACC⁰ algorithm (`2^{n−n^δ}`) are cited. SVG. `pnp_lab/algorithmic_method/`. |
| 13 | **Meta-Complexity Lab** | ✅ | **MCSP & hardness magnification** — the liveliest frontier, where the circle closes. MCSP computed **exactly** (reusing Module 6), MCSP ∈ NP. The **exact link to Natural Proofs** (M1): "f is hard" is useful+large, but making it *constructive* = solving MCSP = breaking PRGs (Razborov–Rudich). Plus **hardness magnification** (cited): tiny `n^{1+ε}` lower bounds amplify to P ≠ NP but stay blocked by the "magnification barrier". SVG. `pnp_lab/meta_complexity/`. |
| 14 | **Enriched Meta-Category** | ✅ · ⚠ *visualization* | An experiment on the **three lenses** (compute/prove/recognize hardness) as morphisms of one quantale-enriched category `C` (Lawvere). On n=3, exact: `C` = Boolean functions + `S_n` renamings, the three realizations of "f is hard", and the **composition-defect matrix**. **Honesty — verdict (V)**: the defect number is a *useful visualization, not a structural invariant* (a finite-size artifact: compute↔recognize → 0 as n→∞; metric not canonical). Full critical analysis in `docs/analisi-metacomplessita.md`. SVG. `pnp_lab/enriched_meta/`. |

## The Natural Proofs barrier in one line

Razborov & Rudich (1994): a property of Boolean functions that is **constructive**
(polynomial-time in the truth-table size) and **large** (true for a fraction
`≥ 2^(−O(n))` of all functions) **cannot** prove super-polynomial circuit lower
bounds — unless pseudorandom generators do not exist, which is believed false.
Since almost all lower-bound techniques use *natural* properties, this is one of
the deep reasons P vs NP resists.

## Quick start

```bash
py -m pip install -r requirements.txt

py examples/run_analyzer.py              # M1  Natural Proofs Analyzer
py examples/run_oracles.py               # M2  Oracle Separation Sandbox
py examples/run_knowledge.py             # M3  Knowledge Graph (+ md/json/dot export)
py examples/run_proof_complexity.py      # M5  Proof Complexity Lab (pigeonhole)
py examples/run_circuits.py              # M6  Circuit Complexity Sandbox (Shannon, parity)
py examples/run_algebrization.py         # M7  Algebrization Sandbox (extension + sum-check)
py examples/run_switching.py             # M8  Switching Lemma Lab (restrictions, Håstad, iterated depth-d)
py examples/run_algebraic_worlds.py      # M9  Algebraic Query Model (Schwartz–Zippel)
py examples/run_algebraic_separation.py  # M10 Algebraic Separation (query core + lift to NP^Ã \ P^Ã)
py examples/run_proof_search.py          # M11 Proof-Search Lab (policy + sound verifier)
py examples/run_algorithmic_method.py    # M12 Algorithmic Method Lab (Williams)
py examples/run_meta_complexity.py       # M13 Meta-Complexity Lab (MCSP)
py examples/run_enriched_meta.py         # M14 Enriched Meta-Category (composition defect)

py -m pytest -q                          # full Python test suite (195 tests)

cd formalization && lake build           # M4  Lean 4 formalization (kernel-verified)
```

### Lean build notes

The Lean core uses **no `mathlib`** (only `Init`), so it is small and fast to
check. Toolchain is pinned in `formalization/lean-toolchain`. Axiom hygiene can be
audited with `lake env lean Check.lean`: the abstract core depends on **zero
axioms**, the concrete layer only on `propext`/`Quot.sound`, and **nothing uses
`Classical.choice`** — the development is constructive.

## Honest limits of Module 1

- **Constructiveness** is not decidable by a program in general: we measure the
  *empirical scaling* of the evaluation time and compare it with `poly(2^n)`. The
  verdict is heuristic, documented as such.
- **Largeness** is computed *exactly* for n ≤ 4 (full enumeration of the `2^(2^n)`
  functions) and *estimated by Monte-Carlo sampling* for larger n.
- The third Razborov–Rudich condition, **usefulness**, is not automatically
  checkable: the tool focuses on the two checkable conditions and flags the trap.

## Documentation

- `docs/switching-profondita-d.md` — iterated switching in depth `d` (Module 8, EN).
- `docs/lift-query-to-tm.md` — lifting the query core to an oracle TM (Module 10, EN).
- `docs/analisi-metacomplessita.md` — full meta-complexity analysis & critique (IT).
- **Interactive divulgative site (IT):** <https://robertocastiglion.github.io/PvsNP/>

## License

Released under the **MIT License** — see [`LICENSE`](LICENSE).
