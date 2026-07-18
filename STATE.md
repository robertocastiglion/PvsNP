# STATE — PvsNP-lab Fase 2 "Perseverance Run"

## Sessione corrente

**Data:** 2026-07-18
**Entry completate questa sessione:** 40, 41, 42, 43, 44, 45

## Ultimo stato — Entry 45 CHIUSO

**Congettura C45 (NUOVA, 47 valori verificati):**
```
g((a, 1^{d-a}), (a, 1^{d-a}), (a, 1^{d-a})) = 1 per a <= d <= 3a-2
                                               = 0 per d >= 3a-1 (= d_0(a))
```
Verificato per a=2..7 (6 valori di arm, 47 valori individuali, tutti esatti via g_fast).
Sequenze palindrome. Fat-hooks (b=2) NON soddisfano C45 (g>1 per a>=3). Robustness 7/10.

**C42 addendum (Entry 42+45):** d_0(a)=3a-1 per a=2..7 (7 data points).
**C44 (Entry 44):** d_0(a,b=2)=3a+4 per a=2..6 (5 data points).
**Falsificazione intra-sessione (Entry 43):** d_0^{(3)}(1) != 8 (g((3^8)^3)=1 per rettangolo coperto).

## Infrastruttura permanente da questa sessione

- `pnp_lab/gct_kronecker/diagonal_census.py` (STRETCH_MAX_D=24)
- `pnp_lab/gct_kronecker/hook_depth.py` (HOOK_MAX_D=27; hook_lam, g_hook_diag,
  hook_depth_row, predicted_d0/T/last_hole, fat_hook_lam/diag/predicted_fat_d0)
- `tests/test_hook_depth.py` (46 fast + 5 slow test)
- `examples/run_hook_depth.py`

## Bilancio lab (post-Entry 45)

25 restatements / 7 arene | 1 falsificazione intra-sessione | 1 non-collasso (M22) |
survival-PASS@1 (M24) | survival-PASS@3 (M25) | 2 control-PASS (M26, M27)
C42/C44/C45 = pacchetto computazionale hook-diagonal (Entry-only, non Moduli).

## Commits questa sessione

- 89b50bc: Entry 40 (RESTATEMENT #24)
- 09ea373: Entry 41 (hook_depth.py + tests + example + RESEARCH_LOG)
- fdf3dd9: Entry 42 (predicted_d0/T/last_hole + tests + RESEARCH_LOG)
- d9e0f78: Entry 43 (RESEARCH_LOG falsification + uncoverage mechanism)
- 807d645: Entry 44 (fat_hook_* + tests + RESEARCH_LOG)
- [pending]: Entry 45 (C45 tests + RESEARCH_LOG + STATE)

## Prossima azione concreta — Entry 46 candidates

(a) Dimostrare C45 analiticamente dal Blasiak formula per g(hook^2, hook)
(b) Verificare a=8 (char_table(23) per d=22, char_table(22) per d=21 — fattibile ~24s)
(c) Aggiungere `hook_diagonal_curve(a)` a hook_depth.py come cristallizzazione minima
(d) Fermarsi — ledger 25 restatements + C42/C44/C45 è il contributo Fase 2
