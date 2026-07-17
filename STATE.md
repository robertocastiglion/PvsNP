# STATE — PvsNP-lab Fase 2 "Perseverance Run"

## Sessione corrente

**Data:** 2026-07-17
**Entry target:** 40
**Target:** Censimento diagonale g(λ,λ,λ) a d≤12 — tutti gli zeri classificati contro il
dizionario Section F di docs/prior-art-kronecker-zeros.md.

## Ipotesi (Entry 40)

H: tra tutti g(λ,λ,λ)=0 con λ ⊢ d, d≤12, esiste almeno UN zero NON spiegato da:
- segno (1^d)
- due-righe (B1/Rosas)
- hook (B2/Blasiak)
- due-colonne (B6/Pak–Panova)
- near-rettangolo o rettangolo (B4)
- membro g-orbita con due forme speciali

Killer pre-dichiarati:
- K1-ALL-COVERED: tutti i zero ≤d=12 coperti → RESTATEMENT #24
- K2-OMISSION: ogni superstite ha hook/two-col nell'orbita → survival-by-omission
- K3-SATURATION: ogni superstite è un HOLE → RESTATES non-saturazione (Entries 34/39)

## Sotto-task Entry 40 — COMPLETATI

| # | Task | Stato | Esito |
|---|------|-------|-------|
| 1 | Commit Section F prior-art | DONE | 2f309bf |
| 2 | Build diagonal_census.py + tests | DONE | fff2f4b — 60 zeros, 12 uncovered |
| 3 | Adversary attack K1/K2/K3 | DONE | K2 non spara, K3 spara su tutti |
| 4 | Evaluator | DONE | RESTATEMENT #24, 4.5/10 |
| 5 | RESEARCH_LOG Entry 40 | DONE | appended |

## Stato Entry 40

CHIUSO: RESTATEMENT #24. Tutti i 12 uncovered zeros sono HOLE (g(2λ)>0 per tutti).
STRETCH_MAX_D=24 nuova infrastruttura permanente.

## Prossima azione concreta

→ Decidere NEXT direction da Entry 40:
  (a) censire d=13..15 (prevedibile: più HOLEs, RESTATEMENT #25)
  (b) quasi-polinomialità diagonale: transizione hook(2,1^(d-2)) a d=8 — legge predittiva?
  (c) fermarsi: 24 restatement, ESC-2 confermato in Fase 2

## Stato repo

- Prior-art Section F: committato in questo ciclo (vedi sotto)
- diagonal_census.py: da creare
- Suite precedente: 583+ test, green

## Bilancio lab (pre-Entry 40)

23 collassi / 7 arene | 1 falsificazione | 1 non-collasso (M22) |
survival-PASS@1 (M24) | survival-PASS@3 (M25) | 2 control-PASS (M26, M27)
