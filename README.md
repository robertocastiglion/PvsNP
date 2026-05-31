# P/NP Research Lab

Un toolkit modulare che rende **tangibili, eseguibili e verificabili** i pilastri del
problema P vs NP — comprese le *barriere* che ogni tentativo di dimostrazione deve superare.

> **Onestà intellettuale prima di tutto.** Questo progetto **non** "trova la dimostrazione"
> di P vs NP. Nessuno sa come farlo, e abbiamo dimostrato *perché* gli approcci ovvi
> falliscono (relativizzazione, natural proofs, algebrizzazione). Quello che questo
> toolkit fa è trasformare quelle barriere da concetti astratti in **strumenti che girano**:
> codice che, data un'idea candidata, ti dice se cade in una trappola nota.

## Moduli

| # | Modulo | Stato | Cosa fa |
|---|--------|-------|---------|
| 1 | **Natural Proofs Analyzer** | ✅ fatto | Data una proprietà combinatoria delle funzioni booleane, verifica se è *costruttiva* e *larga* — cioè se cade nella barriera di Razborov–Rudich e quindi **non potrà mai separare P da NP**. |
| 2 | **Oracle Separation Sandbox** | ✅ fatto | Costruisce per diagonalizzazione l'oracolo B con P^B ≠ NP^B (eseguito e verificato) e usa l'oracolo PSPACE-completo TQBF per illustrare P^A = NP^A. Rende visibile la barriera della **relativizzazione**. |
| 3 | **Knowledge Graph** | ✅ fatto | Grafo navigabile e interrogabile di barriere, approcci, tecniche, risultati e problemi aperti (con riferimenti). Sa chi blocca chi, chi aggira chi, e la "frontiera" promettente. Export Markdown/JSON/Graphviz. |
| 4 | **Lean 4 Formalization** | ✅ fatto | Definizioni rigorose (P, NP, riduzioni, NP-completezza) e teoremi verificati dal kernel: P ⊆ NP, transitività delle riduzioni, collasso di Cook, e la barriera di relativizzazione. Zero `sorry`, zero assiomi. Vedi `formalization/`. |

## La barriera Natural Proofs in una riga

Razborov & Rudich (1994): una proprietà delle funzioni booleane che sia
**costruttiva** (calcolabile in tempo polinomiale nella dimensione della tabella di verità)
e **larga** (vera per una frazione ≥ 2^(−O(n)) di tutte le funzioni) **non può** servire a
dimostrare lower bound super-polinomiali sui circuiti — a meno che non esistano i
generatori pseudo-casuali, cosa ritenuta falsa. Poiché quasi tutte le tecniche di lower
bound usano proprietà *naturali*, questa è una delle ragioni profonde per cui P vs NP
resiste.

## Quick start

```bash
py -m pip install -r requirements.txt
py examples/run_analyzer.py    # Modulo 1: Natural Proofs Analyzer
py examples/run_oracles.py     # Modulo 2: Oracle Separation Sandbox
py examples/run_knowledge.py   # Modulo 3: Knowledge Graph (+ export md/json/dot)

cd formalization && lake build # Modulo 4: formalizzazione Lean 4 (kernel-verified)
```

## Limiti onesti del Modulo 1

- La **costruttività** non è decidibile da un programma in generale: misuriamo lo
  *scaling empirico* del tempo di valutazione e lo confrontiamo con poly(2^n). Il
  verdetto è euristico, documentato come tale.
- La **larghezza** è calcolata in modo *esatto* per n ≤ 4 (enumerazione completa delle
  2^(2^n) funzioni) e *stimata via campionamento Monte Carlo* per n maggiori.
- La terza condizione di Razborov–Rudich, l'**utilità** (la proprietà implica lower bound),
  non è verificabile automaticamente: il tool si concentra sulle due condizioni
  controllabili e segnala la trappola.
