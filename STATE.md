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

## Sotto-task

| # | Task | Stato | Agente |
|---|------|-------|--------|
| 1 | Commit docs/prior-art-kronecker-zeros.md (Section F) | COMPLETATO | PI |
| 2 | Build pnp_lab/gct_kronecker/diagonal_census.py + tests + examples | IN CORSO | Builder |
| 3 | Adversary attack: killer K1/K2/K3 + classificazione | APERTO | Adversary |
| 4 | Evaluator: robustness score + verdetto + GATE | APERTO | Evaluator |
| 5 | Archivist: RESEARCH_LOG Entry 40 + memory + commit | APERTO | Archivist |

## Prossima azione concreta

→ Leggere output Builder (sotto-task 2) e lanciare Adversary.

## Stato repo

- Prior-art Section F: committato in questo ciclo (vedi sotto)
- diagonal_census.py: da creare
- Suite precedente: 583+ test, green

## Bilancio lab (pre-Entry 40)

23 collassi / 7 arene | 1 falsificazione | 1 non-collasso (M22) |
survival-PASS@1 (M24) | survival-PASS@3 (M25) | 2 control-PASS (M26, M27)
