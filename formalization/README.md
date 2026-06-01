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

Compilato e verificato dal kernel di Lean 4.30.0 (`lake build` → exit 0, 9 job).
**22 dichiarazioni `theorem`** in totale.

| File | Contenuto |
|------|-----------|
| `PvsNP/Basic.lean` | `BitString`, `Language`, `IsPoly`, la struttura `Model` (con le sue chiusure poly-time, inclusa `idFn`). |
| `PvsNP/Classes.lean` | `P`, `NP`, **`P_subset_NP`** (P ⊆ NP), `PEqNP`, `PNeqNP`. |
| `PvsNP/Reductions.lean` | riduzioni poly-time, **`reduces_refl`** + **`reduces_trans`** (preordine), **`P_closed_reduction`**, NP-completezza, **`complete_in_P_implies_PEqNP`** (collasso di Cook), il suo converso **`PEqNP_complete_in_P`** e la caratterizzazione **`complete_in_P_iff_PEqNP`** (`L ∈ P ↔ P = NP` per `L` NP-completo). |
| `PvsNP/Barriers.lean` | `RelativizationBarrier` (forma astratta di Baker–Gill–Solovay) e **`relativizing_cannot_settle`**: nessuna dimostrazione valida in *ogni* modello può decidere P vs NP. |
| `PvsNP/Concrete.lean` | **Un `Model` concreto** (il modello *senza limiti di tempo*) che soddisfa tutti gli assiomi della struttura, con enumerazione costruttiva dei testimoni (`stringsOfLen`/`allUpTo`). **`unbounded_NP_subset_P`**: la forza bruta decide ogni problema NP ⇒ **`unbounded_PEqNP`** (P = NP nel modello senza limiti) ⇒ **`collapse_world_exists`** (il "mondo P = NP" della barriera, ora abitato). Chiude la lacuna di *non vacuità* del framework. |
| `PvsNP/SAT.lean` | **CNF-SAT concreto** — il bersaglio di Cook–Levin reso tangibile: `Lit`/`Clause`/`CNF`, valutatore, `Sat`. Teoremi: **`sat_iff_witness`** (la forma-NP: testimone = assegnamento, verificatore = valutatore), **`not_sat_of_nil_clause`** (la clausola vuota ⊥ è insoddisfacibile), **`eval_append`** + **`sat_append_left`** (semantica AND e monotonìa), e la riduzione verificata **`eval_rename`** / **`sat_of_sat_rename`** (sostituzione delle variabili, il mattone di ogni riduzione fra istanze SAT). |

### Verifica di onestà (con `#print axioms`, vedi `Check.lean`)

Nessun `sorry` in tutto il codice. Sugli assiomi siamo precisi:

- **Il nucleo astratto** (gli 8 teoremi di `Classes`/`Reductions`/`Barriers`)
  **non dipende da ALCUN assioma** — nemmeno `propext` o `Classical.choice`:
  sono dimostrazioni puramente logiche.
- **Il livello concreto** (`Concrete`, `SAT`) usa soltanto **`propext`** e
  **`Quot.sound`** — i due assiomi *standard* del kernel di Lean, inevitabili
  appena si calcola con liste e booleani, e accettati da qualunque sviluppo
  (mathlib compreso). **Mai `Classical.choice`**: tutto resta costruttivo (la
  forza bruta è un algoritmo che gira davvero). `eval_rename` e
  `sat_of_sat_rename` sono perfino a **zero assiomi**.

I predicati poly-time del `Model` sono ipotesi esplicite (campi della struttura),
non assiomi globali.

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
