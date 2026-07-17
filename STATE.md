# STATE — PvsNP-lab Fase 2 "Perseverance Run"

## Sessione corrente

**Data:** 2026-07-18
**Entry completate questa sessione:** 40 (RESTATEMENT #24), 41 (RESTATEMENT #25 partial + new content candidate)

## Stato Entry 41 — CHIUSO

CHIUSO: RESTATEMENT #25 (parziale) + new content candidate.
- g(2·(2,1^(d-2)))=0 per d=8..13 (6 data points, killer K_FIRES non spara)
- depth=3 confermato per d=8 (g(3λ)=1646) e d=9 (g(3λ)=1209)
- B5 check RISOLTO: (4,2^6) max g=71, (4,2^7) max g=88 → NON mult-free → uncoverage SOLIDA
- Biforcazione depth: d=5..7 → depth=2; d≥8 → depth≥3 (threshold a d=8)
- GATE: Entry-only (non modulo autonomo; congettua depth=3 non confermata oltre d=9)

## Infrastruttura permanente da questa sessione

- STRETCH_MAX_D=24 (diagonal_census.py)
- HOOK_MAX_D=27 (hook_depth.py)
- diagonal_census.py + hook_depth.py + test suite (15 test fast + 7 slow)

## Bilancio lab (post-Entry 41)

25 restatements (25° parziale) / 7 arene | 1 falsificazione | 1 non-collasso (M22) |
survival-PASS@1 (M24) | survival-PASS@3 (M25) | 2 control-PASS (M26, M27)

## Prossima azione concreta — Entry 42 candidates

→ Decidere NEXT direction da Entry 41:
  (a) Generalizzare fat-hook: (a,b^k) con a≠4 o b≠2 — si vede la stessa transizione depth?
  (b) Quasi-polinomio strutturale: raccogliere più valori N per d=8 se fattibile
  (c) Fermarsi: 25 restatements + ESC-2 re-confermato in Fase 2

## Commits questa sessione

- 89b50bc: Entry 40 (RESTATEMENT #24)
- [pending]: Entry 41 (hook_depth.py + tests + example + RESEARCH_LOG)
