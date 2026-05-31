# Modulo 4 — Formalizzazione in Lean 4

Definizioni rigorose di P, NP, riduzioni poly-time, NP-completezza e barriere,
**verificate dal kernel di Lean**. Autosufficiente: usa **solo Lean core**,
nessuna dipendenza da mathlib → compila in pochi secondi.

## Scelta di progetto (onesta)

Una formalizzazione *piena* di P e NP richiede un modello di calcolo concreto
(macchine di Turing con limite di tempo). Qui lavoriamo a livello **astratto**:
tutto è parametrizzato su una struttura `Model` che espone i predicati
"calcolabile in tempo polinomiale" con le loro proprietà di chiusura, date come
assiomi. I teoremi valgono quindi per *ogni* modello che soddisfa quegli assiomi
(in particolare le macchine di Turing). Nessun `sorry`: i teoremi qui sotto sono
dimostrati per davvero.

## Cosa è dimostrato

Compilato e verificato dal kernel di Lean 4.30.0 (`lake build` → exit 0, 7 job).

| File | Contenuto |
|------|-----------|
| `PvsNP/Basic.lean` | `BitString`, `Language`, `IsPoly`, la struttura `Model`. |
| `PvsNP/Classes.lean` | `P`, `NP`, **`P_subset_NP`** (P ⊆ NP), `PEqNP`, `PNeqNP`. |
| `PvsNP/Reductions.lean` | riduzioni poly-time, **`reduces_trans`**, **`P_closed_reduction`**, NP-completezza, **`complete_in_P_implies_PEqNP`** (collasso di Cook). |
| `PvsNP/Barriers.lean` | `RelativizationBarrier` (forma astratta di Baker–Gill–Solovay) e **`relativizing_cannot_settle`**: nessuna dimostrazione valida in *ogni* modello può decidere P vs NP. |

### Verifica di onestà

Nessun `sorry` nel codice, e `#print axioms` (vedi `Check.lean`) conferma che
**tutti e cinque i teoremi non dipendono da alcun assioma** — nemmeno
`propext` o `Classical.choice`: sono dimostrazioni completamente costruttive. I
predicati poly-time del `Model` sono ipotesi esplicite, non assiomi globali.

Il teorema `relativizing_cannot_settle` è il ponte col **Modulo 2**: lì rendiamo
*eseguibili* i due mondi (oracolo TQBF per P^A = NP^A, diagonalizzazione per
P^B ≠ NP^B); qui dimostriamo formalmente *perché* la loro coesistenza blocca le
tecniche relativizzanti.

## Compilare

```bash
cd formalization
lake build
```

### Nota sul toolchain (ambiente di questa macchina)

Il toolchain Lean 4.30.0 è installato e collegato a `elan` col nome locale
`lean-local` (vedi `lean-toolchain`). Questo perché il proxy aziendale blocca
il *certificate revocation check* e quindi `elan` non riesce a scaricare i
toolchain dalla rete: il toolchain è stato scaricato a parte e collegato con
`elan toolchain link lean-local <percorso>`.

Su una macchina con accesso di rete normale si può invece usare il pin
standard mettendo in `lean-toolchain`:

```
leanprover/lean4:v4.30.0
```

e `elan` lo scaricherà da solo al primo `lake build`.
