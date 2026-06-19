"""Cycle 1 — the relativization obstruction read as a leverage operator.

Reuses the verified BGS diagonalization (pnp_lab/oracles/separation.py) and measures the
obstruction across levels: depth(OR)=2^n, the headroom h(n,k)=2^n-n^k, the break-even
staircase n*(k), and the online freshness length-schedule.

Run:  py examples/run_oracle_leverage.py
"""

from pnp_lab.oracles import leverage as lev
from pnp_lab.oracles.separation import EXAMPLE_MACHINES


def main() -> None:
    ks = (1, 2, 3)
    print("Obstruction height depth(OR)=2^n and headroom h(n,k)=2^n - n^k:")
    print(f"  {'n':>2} {'2^n':>6} {'depth(OR)':>10}   " +
          "  ".join(f"h(n,{k})" for k in ks))
    for r in lev.leverage_staircase((1, 2, 3, 4, 5, 6), ks):
        print(f"  {r.n:>2} {r.slice_size:>6} {r.obstruction_height:>10}   " +
              "  ".join(f"{h:>6}" for h in r.headroom_k))

    print("\nBreak-even staircase n*(k) = level beyond which 2^n > n^k forever:")
    for k in ks:
        print(f"  k={k}: n*(k) = {lev.break_even_length(k)}")

    print("\nOnline freshness length-schedule vs greedy arithmetic:")
    fs = lev.freshness_schedule(EXAMPLE_MACHINES)
    print(f"  machines      : {[m.name for m in EXAMPLE_MACHINES]}")
    print(f"  diag lengths  : {fs.lengths}")
    print(f"  greedy lengths: {fs.greedy_lengths}")
    print(f"  matches greedy: {fs.matches_greedy}   all defeated: {fs.all_defeated}")

    print("\n" + lev.honesty_note())


if __name__ == "__main__":
    main()
