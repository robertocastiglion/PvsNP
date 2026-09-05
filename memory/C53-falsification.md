---
type: project
slug: C53-falsification
---

# C53 Falsification — Entry 73

**Conjecture (now falsified):** g((k^k)^3) = F(3k-7) for k≥2 (Fibonacci series).

**Verification:** k=2,3,4,5 → g=1,1,5,21 = F(−1), F(1), F(5), F(8) ✓

**Killer (F73, pre-registered):** k=6 d=36
- g((6^6)^3) = 9309 (dual-engine: g_fast 1.2s + engine3 pending cross-check)
- Predicted F(11) = 89
- Scarto = 9309 − 89 = 9220 (huge, zero-parameter falsification)

**Cascata logica:**
- [[L62-void]]: R_square(k)→0 was conditional "IF C53 holds"
- Post-kill: L62 now VOID (hypothesis vacuous)

**Series status:** [1,1,5,21,9309] — non-Fibonacci, open.

**Corpus impact:** Adds 1 to falsification count (7 total post-F73).

**Decision:** No new direction on k^k powers. C53 closed.

---
Related: [[L62-void]], [[dual-engine-validation]], Entry 73
