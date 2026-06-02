# From the query core to a Turing-machine oracle: a language in NP^Ã \ P^Ã

*Research thread implemented on 2026-06-02. Extends Module 10 (Algebraic
Separation) from the query model to a genuine relativized separation.*

## Goal

The rest of Module 10 runs the separation in the **query model**: for the OR
problem under algebraic oracle access, the NP side costs **one** query (guess a
witness on the cube, check `Ã(z)=A(z)=1`), while the P side needs **κ** queries,
proved by a *cancellation adversary*. This step **lifts** that core into a real
**diagonalization** that builds an algebraic oracle `O` and a language

```
L_O = { 1ⁿ : the oracle slice at length n is not identically zero }
```

with `L_O ∈ NP^Ã` but `L_O ∉ P^Ã`.

## Mechanism (the query core, reused as a diagonalization gadget)

For each machine `M_i`, at a fresh input length `n` with an `m`-bit oracle slice:

1. run `M_i(1ⁿ)` against the **all-zero** oracle (`Ã ≡ 0`), recording the set `R`
   of algebraic points it queries;
2. if `M_i` **accepts** while seeing only zeros, leave the slice zero — then
   `1ⁿ ∉ L_O` but `M_i` accepts → wrong;
3. if `M_i` **rejects**, find a nonzero **boolean kernel** `A` with `Ã(r)=0` for
   all `r ∈ R` (this is `boolean_kernel_witness`; it exists whenever the queries
   fail to kill every kernel — guaranteed if `|R| < κ`, and possible even with
   `|R| ≥ κ` if the queries are poorly chosen, e.g. only on the cube). Plant it:
   `M_i` re-walks the identical path and still rejects, but now `1ⁿ ∈ L_O` → wrong.

Either way `M_i` is diagonalized. A machine survives only by making `≥ κ`
**well-chosen** queries; but κ grows with `N = 2^m`, while a polynomial-time
machine makes far too few, eventually.

## What is executed (exact, on small m)

- `lift.py` — `build_oracle(machines, p, m, base_n)` wires one diagonalization
  stage per length; `diagonalize_stage` performs the gadget above and **reuses**
  `boolean_kernel_witness` / `deterministic_lower_bound` from the query core.
- `np_certificate(lift, n)` — the NP^Ã side on the constructed oracle: a witness
  on the cube, verified in **one** query.

### Measured (GF(3), m = 2, default adversary machines)

| machine | 1ⁿ | queries | κ | answer | 1ⁿ ∈ L_O | result |
|---|---|---:|---:|---|---|---|
| const_accept | 1² | 0 | 2 | accept | no | diagonalized |
| const_reject | 1³ | 0 | 2 | reject | yes | diagonalized |
| cube_scan_1  | 1⁴ | 1 | 2 | reject | yes | diagonalized |
| cube_scan_2  | 1⁵ | 2 | 2 | reject | yes | diagonalized |
| field_probe_2| 1⁶ | 2 | 2 | reject | yes | diagonalized |

`cube_scan_2` makes `κ = 2` queries yet is still fooled: its two queries are on
the cube (poorly chosen), so a kernel survives. The crucial test
(`test_planted_kernel_is_invisible`) **re-runs** each machine against the *fixed*
oracle and confirms it repeats the same (wrong) answer — it cannot tell.

## Honesty boundary

- **Executed**: the per-stage gadget and its wiring over a concrete, finite list
  of oracle machines; the NP^Ã witness; the kernel-invisibility check.
- **Cited**: the theorem over **all** polynomial-time machines (standard
  diagonalization), and the **strong version** with the communication-complexity
  lower bound — that is the **Aaronson–Wigderson** theorem.
- **No new result**: this is a *relativized* world, and precisely because it
  relativizes it **cannot** settle P vs NP. It makes the relativized algebraic
  separation executable, in the same spirit as the rest of the toolkit.

## Files

```
pnp_lab/algebraic_separation/lift.py   # diagonalization, oracle/language, NP cert, SVG
tests/test_lift.py                     # 7 exact tests (incl. kernel-invisibility re-run)
examples/run_algebraic_separation.py   # demo (section "sollevamento")
web/assets/algebraic_lift.svg          # per-stage queries vs κ
```
