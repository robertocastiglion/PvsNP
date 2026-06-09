# The duality gap `G(R)` — what really separates (and unifies) the four barriers

*Companion to Modules 15–16. This is a **theory note**, not an executable module: it
records the conclusion of an adversarial stress-test of Module 16's verdict, and the
deeper structure that survives it. It contains no new measured numbers; the honesty
boundary is therefore stricter than usual — every claim here is either a cited theorem
or explicitly marked as a framing.*

## Why this note exists

Module 16 concluded: relativization, algebrization and natural proofs fit the single
inequality `Δ(𝒞; D0, D1) ≤ ε`, while **proof complexity does not**, because its
governing quantity is a witness length `min|Π| ∈ ℕ∪{∞}` rather than a statistical
advantage `sup|E1−E0| ∈ [0,1]`.

That verdict was then attacked, hard, on purely mathematical grounds. The attack
succeeds: **the Module-16 separation is an artifact of a modelling choice, not a
structural fact.** What replaces it is cleaner and includes all four barriers. This
note is the record.

## 1. The demolition of Module 16's "first failure point"

Three independent objections, each fatal:

1. **Proof complexity is already a distinguishing problem in the literature.**
   - *Proof-complexity generators* (Razborov, *Pseudorandom generators hard for
     k-DNF resolution and polynomial calculus resolution*, Ann. of Math. 2015):
     "no short refutation of `τ_g(b)`" **is** a pseudorandomness statement.
   - *Forcing with random variables* (Krajíček, LMS LN 382, 2011): builds models in
     which proof-size lower bounds become **indistinguishability of random
     variables** — a measure-theoretic structure, i.e. exactly the "wrong type" the
     module claimed could not exist.
   - *Non-automatizability via cryptography* (Alekhnovich–Razborov 2008;
     Atserias–Müller, *Automating Resolution is NP-hard*, FOCS'19/JACM'20): proof
     search is hard **because** it would break an indistinguishability.

2. **The two-sided collapse is an artifact of the SAT/UNSAT axis.** Module 16 set
   `D0 = SAT`, `D1 = UNSAT`; soundness then forces the `D0` side to `0`. But that
   conflates the *decision* problem with the *proof* problem. The correct analogue of
   the construction used for barriers 1–3 puts **both worlds in the hard class**:
   `D1 =` UNSAT instances *with* a refutation of size `≤ s`, `D0 =` UNSAT instances
   *without* one. Soundness is now irrelevant and `Δ` is two-sided — precisely the
   generator / forcing setup.

3. **The type argument proves too much.** "`min` over ∃-witnesses, type `ℕ`" is not
   special to proofs: the quantity *underneath* barriers 1 and 3 has the same type —
   decision-tree depth (`min #queries`) and circuit size (`min |C|`) are both
   integer-valued minima over existential witnesses. The module unrolled the
   worst-case→distributional (Yao) reduction for 1–3 and **declined to unroll it for
   4**. Applied symmetrically, `min|Π|` becomes a `Δ` exactly as `min #queries`
   became `t/N`.

Net: barrier 3 (natural proofs) and barrier 4 (proof complexity) land on the **same
side**, both carrying the same (conjectural) pseudorandomness debt — the opposite of
the clean 3-vs-4 split Module 16 asserted.

## 2. The object all three are instances of: `μ_R`

Fix a polynomial-time **verification relation** `R ⊆ X × W` ("`w` certifies `x`") and
a cost on witnesses. Define

```
μ_R(x) = min { cost(w) : R(x, w) = 1 }   ∈  ℕ ∪ {∞}.
```

Query, circuit and proof complexity are **the same `μ_R`** for three choices of `R`:

| measure | `x` | witness `w` | `R(x,w)` | `cost` |
|---|---|---|---|---|
| query / decision tree | function `f`, input | tree / forcing sub-cube | "tree computes `f`" | depth |
| circuit | Boolean function `g` | circuit `C` over a basis | "`C` computes `g`" | #gates |
| proof | UNSAT formula `τ` | derivation `Π` | "`Π` refutes `τ`" | #steps |

This is **resource-bounded Kolmogorov complexity** relative to the structured
decompressor `R`: min circuit size is polynomially `KT` (Allender et al.); query and
proof are the same schema with another decompressor. The minimal formalism that
generates all three is just *"a poly-time verifier `R` + a cost on witnesses."*

## 3. `Δ ≤ ε` is the minimax dual of `μ_R ≥ s`

`μ_R = min |w|` is a covering integer program. By LP/SDP/minimax duality its dual is

```
μ_R(x) ≥ s   ⟺   ∃ distribution/weighting D : every witness of cost ≤ s "fails" on D.
```

That dual — "no cheap certificate has advantage against `D`" — **is** `Δ ≤ ε`. The
statistical advantage is therefore **derived**, the dual of the primal fact that the
cheapest certificate is large. The three classical lower-bound methods are the three
instances of this dual:

- **query → adversary / polynomial method** (Špalek–Szegedy; Reichardt);
- **circuit → natural proofs / discriminator / approximation method** (Razborov–Rudich; Razborov);
- **proof → feasible interpolation / forcing / Prover–Delayer / size–width**
  (Krajíček–Pudlák; Krajíček; Pudlák–Impagliazzo; Ben-Sasson–Wigderson).

## 4. The gap theory: `G(R) = μ_R − Dual(μ_R)`

`G(R)` is the **integrality / relaxation gap** of the certificate-covering program —
uniform as a *definition* across all three domains (the great-grandparent is Lovász's
fractional-vs-integer covering gap).

### Corners where `G = 0` is a theorem (one per domain — proof the framework is real)

- **query (quantum):** `Q(f) = Θ(ADV±(f))` — Reichardt; the SDP dual is tight. (And
  all classical query measures are polynomially equivalent, so `G` is *always*
  poly-bounded inside query — no superpolynomial barrier is intrinsic to query.)
- **circuit (depth):** formula depth `=` communication complexity of the
  Karchmer–Wigderson relation. Exact.
- **proof (tree-resolution; SOS):** tree-resolution size `=` Prover–Delayer game value
  (Pudlák–Impagliazzo); degree-`d` SOS `=` pseudo-expectations (SDP duality). Exact.

### Where `G` is large = the barriers (as restrictions of the dual)

The barrier is not merely "`G` large" but "`G` large **against a whole structured
class of duals**":

| barrier | the *restricted* dual | why `G` stays large |
|---|---|---|
| relativization | oracle-invariant duals | they see a *coarsened* `R` (closed under oracle access); BGS forces the gap |
| algebrization | algebraic-oracle-invariant duals | same with `R` closed under the low-degree extension (Aaronson–Wigderson) |
| natural proofs | constructive + large duals | a dual closing `G` would break PRFs (Razborov–Rudich) |
| proof complexity (strong systems) | feasible-interpolation duals | interpolation fails under cryptographic assumptions |

Relativization/algebrization are gaps of a **coarsened `R`** (between `μ_R` and `μ` of
an oracle-closed `R`). Natural proofs / proof complexity are **intrinsic** relaxation
gaps made rigid by a pseudorandomness hypothesis — and they sit on the same side.

## 5. Honest verdict (this supersedes Module 16's verdict)

- A unifying **framework** exists: `G(R)` = integrality gap of the certificate IP,
  specializing correctly to query / circuit / proof, with **exact-duality corners
  proven in all three** (Reichardt; Karchmer–Wigderson; Prover–Delayer / SOS).
- The **four barriers are large-gap regimes**, distinguished by *which class of duals*
  is stuck — not by a type mismatch. Natural proofs and proof complexity are the
  **same side** of the same debt.
- A **predictive** theory of `G(R)` does **not** exist, and this is itself a theorem,
  not a gap in our note: outside the convex corners `Dual(μ_R)` is not even
  canonically defined (the approximation method and interpolation are not known to be
  exact convex duals); and where it is defined, *estimating* `G` is meta-computationally
  as hard as the lower bounds themselves (`MCSP`/`MKtP`). The closest thing to a
  cross-cutting theory today is **meta-complexity + bounded-arithmetic forcing**
  (Hirahara; Krajíček), where "`G` large" ⟺ "a weak theory cannot prove the lower
  bound" ⟺ "an indistinguishable model / distinguisher exists".

One line: **`G(R)` is an integrality gap; the barriers are the regimes where an entire
class of duals is stuck on it; and "computing `G`" *is* P-vs-NP seen through
meta-complexity.**

## Honesty boundary (binding for this repo)

- This note contains **no measurements**. It is a theory synthesis; every load-bearing
  claim is a cited theorem or an explicitly labelled framing. It does **not** prove
  (or touch) P vs NP.
- The "minimax dual" is literal only where a convex/feasibility formulation exists
  (query; depth; tree-resolution; SOS). For general non-monotone circuits and strong
  proof systems `Dual(μ_R)` is a *hoped-for* duality, not an established one — stated
  as such above.
- This note **revises** the verdict of `docs/bounded-observer.md`: that document's
  measured numbers stand, but its *interpretation* ("proof complexity cannot be a
  distinguishing advantage; first failure at the advantage step") is downgraded to "an
  artifact of the SAT/UNSAT modelling choice." See §1.

## Pointers (for following up)

- Razborov, *Pseudorandom generators hard for k-DNF resolution…*, Ann. of Math. 2015.
- Krajíček, *Forcing with Random Variables and Proof Complexity*, 2011; *Proof Complexity*, 2019.
- Atserias–Müller, *Automating Resolution is NP-hard*, FOCS 2019 / JACM 2020.
- Reichardt, *Span programs and quantum query complexity: the general adversary bound is nearly tight*, FOCS 2009/2011.
- Karchmer–Wigderson, *Monotone circuits for connectivity require super-logarithmic depth*, 1990.
- Pudlák–Impagliazzo, Prover–Delayer game for tree-resolution, 2000.
- Ben-Sasson–Wigderson, *Short proofs are narrow — resolution made simple*, JACM 2001.
- Razborov–Rudich, *Natural Proofs*, 1994/1997.
- Allender et al., resource-bounded Kolmogorov complexity (`KT`) and circuit size.
- Hirahara, worst-case ↔ average-case meta-complexity; Oliveira–Santhanam, hardness magnification.
