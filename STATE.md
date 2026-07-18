# STATE — PvsNP-lab Fase 2 "Perseverance Run"

## Sessione corrente

**Data:** 2026-07-18
**Entry completate questa sessione:** 40, 41, 42, 43, 44, 45, 46, 47, 48

## Ultimo stato — Entry 48 CHIUSO (cristallizzazione)

**Programma hook COMPLETO. Nessun nuovo claim matematico in Entry 48.**

### Pacchetto hook_depth.py (Entry 41–48):

```
hook_lam(d)                         # (2, 1^{d-2})
g_hook_diag(d, N)                   # g(N*lam_d^3) esatto
hook_depth_row(d, N_max)            # tabella profondità
predicted_d0(a)          = 3a-1     # C42
predicted_T(a)           = 3a+2     # C42
last_hole_value(a)       = a        # C42
fat_hook_lam(a, b, k)               # (a, b^k)
fat_hook_diag(a, b, k)              # g(fat_hook^3)
predicted_fat_d0(a, 1)   = 3a-1     # C42
predicted_fat_d0(a, 2)   = 3a+4     # C44
hook_diagonal_curve(a)              # {d:1} per d in [a, 3a-2]  (C45)
stable_kronecker_b2(k)              # s(k): 1,2,7,21k-44 per k>=3  (C47)
```

### Congetture verificate:

- **C42:** d_0(a)=3a-1, T(a)=3a+2, last_hole=a — verificato a=2..7 (a=1 falsificato in Entry 43)
- **C44:** d_0(a,b=2)=3a+4 — verificato a=2..6
- **C45:** g((a,1^{d-a})^3)=1 per a≤d≤3a-2, 0 per d≥3a-1 — verificato a=2..8 (62 valori)
- **C47:** s(k)=21k-44 per k≥3, s(0..8)=1,2,7,19,40,61,82,103,124 — verificato k=0..8

### Test suite:

```
tests/test_hook_depth.py: 56 fast + 12 slow = 68 total
Fast: 56/56 PASS in 18s
Slow: 12 (require @pytest.mark.slow; a=8 C45=73s, s(8)=287s, etc.)
```

## Infrastruttura permanente da questa sessione

- `pnp_lab/gct_kronecker/diagonal_census.py` (STRETCH_MAX_D=24)
- `pnp_lab/gct_kronecker/hook_depth.py` (HOOK_MAX_D=27; 12 callable)
- `tests/test_hook_depth.py` (68 test)
- `examples/run_hook_depth.py`

## Bilancio lab (post-Entry 48)

26 restatements / 7 arene | 1 falsificazione (Entry 43) | 1 non-collasso (M22) |
survival-PASS@1 (M24) | survival-PASS@3 (M25) | 2 control-PASS (M26, M27)

Programma hook-diagonal CHIUSO (C42/C44/C45/C47 callable + test).

## Commits questa sessione

- 89b50bc: Entry 40 (RESTATEMENT #24)
- 09ea373: Entry 41 (hook_depth.py + tests + example + RESEARCH_LOG)
- fdf3dd9: Entry 42 (predicted_d0/T/last_hole + tests + RESEARCH_LOG)
- d9e0f78: Entry 43 (RESEARCH_LOG falsification + uncoverage mechanism)
- 807d645: Entry 44 (fat_hook_* + tests + RESEARCH_LOG)
- 9873c9c: Entry 45 (C45 tests + RESEARCH_LOG + STATE)
- f108d53: Entry 46 (a=8 verification + 2 slow tests)
- db78034: Entry 47 (stable Kronecker s(k)=21k-44, gen.func., s(7)=103, s(8)=124 confirmed)
- [pending]: Entry 48 (hook_diagonal_curve + stable_kronecker_b2 + 7 tests + STATE)

## Azioni possibili successive

(a) Analisi analitica della gen. function (1+4x^2+7x^3+9x^4)/(1-x)^2
    via plethysm GL(2) / reduced Kronecker theory
(b) Pivot su nuova arena (arithmetic circuits, algebraic complexity, altro)
(c) Fermarsi — ledger 26 restatements + C42/C44/C45/C47 soddisfa anti-resa
