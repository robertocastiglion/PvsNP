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
| 3 | **Knowledge Graph** | ✅ fatto | Grafo navigabile e interrogabile di barriere, approcci, tecniche, risultati e problemi aperti (con riferimenti). Sa chi blocca chi, chi aggira chi, e la "frontiera" promettente. Export Markdown/JSON/Graphviz **+ SVG** nei colori del brand (`pnp_lab/knowledge/render_svg.py`). |
| 4 | **Lean 4 Formalization** | ✅ fatto | Definizioni rigorose (P, NP, riduzioni, NP-completezza) e **26 teoremi** verificati dal kernel. Nucleo astratto (zero assiomi): P ⊆ NP, riduzioni come preordine, collasso di Cook **e la sua caratterizzazione** (`L∈P ↔ P=NP`), barriera di relativizzazione. **Verso Cook–Levin**: un `Model` concreto «senza limiti» in cui **P = NP per forza bruta** (`collapse_world_exists` — il framework non è vacuo), **CNF-SAT concreto** con forma-NP e una riduzione verificata, e **il cuore di Cook–Levin** (`canonical_correct`: vincolo locale → CNF, ogni funzione booleana è una CNF — il passo «computazione valida ⟺ formula soddisfacibile»). Zero `sorry`; il livello concreto usa solo `propext`/`Quot.sound`, mai `Classical.choice`. Vedi `formalization/`. |
| 5 | **Proof Complexity Lab** | ✅ fatto | L'altra metà della storia: un lower bound che **funziona davvero**. Refuta il principio della piccionaia (PHP) con resolution/DPLL e misura la dimensione della prova, che cresce **esponenzialmente** (1·3·11·47·239·1439… nodi — teorema di Haken 1985). Via Cook–Reckhow è una strada verso NP ≠ coNP ⇒ P ≠ NP. Genera grafico SVG. `pnp_lab/proof_complexity/`. |
| 6 | **Circuit Complexity Sandbox** | ✅ fatto | Due lower bound **esatti** sui circuiti. *Spettro di Shannon*: complessità di formula minima di **tutte** le funzioni piccole (quasi tutte difficili, ma nessuna esplicita). *Muro della parità*: la DNF minima della parità ha esattamente 2^(n−1) termini — caso base esatto di «parità ∉ AC0» (Furst–Saxe–Sipser, Håstad), che **aggira la barriera Natural Proofs**. Genera 2 grafici SVG. `pnp_lab/circuits/`. |
| 7 | **Algebrization Sandbox** | ✅ fatto | La **terza barriera** (Aaronson–Wigderson 2008), eseguibile. *Estensione multilineare* di una funzione booleana su GF(p) + il protocollo *sum-check* (motore di **IP = PSPACE**) eseguito davvero: verifica una somma su 2^n termini con **una sola query**, prover onesto accettato e bugiardo smascherato (soundness ≤ d/p). È la tecnica che **scavalca la relativizzazione**. Genera 1 grafico SVG. `pnp_lab/algebrization/`. |
| 8 | **Switching Lemma Lab** | ✅ fatto | Lo **switching lemma di Håstad** in azione, il meccanismo dietro «parità ∉ AC0». Applica restrizioni casuali e misura la profondità dell'albero di decisione *ottimo*: una DNF di larghezza w **collassa** (verifica empirica del bound `Pr[D ≥ s] ≤ (5pw)^s`), mentre la **parità resiste** — la sua profondità resta = numero di variabili libere. Genera 1 grafico SVG. `pnp_lab/switching/`. |
| 9 | **Algebraic Query Model** | ✅ fatto | I **«mondi algebrici»** della barriera dell'algebrizzazione (estende il Modulo 7). Il motore — **Schwartz–Zippel** su GF(p) — verificato in modo esatto. *Mondo potenza*: rilevare un bit piantato costa 2^m query booleane ma **una** algebrica (prob. `(1−1/p)^m`). *Mondo limite*: determinare l'oracolo richiede comunque ~2^m query — **lower bound di interpolazione esatto** su GF(p), con un avversario che esibisce due oracoli indistinguibili. Genera 1 grafico SVG. `pnp_lab/algebraic_worlds/`. |
| 10 | **Algebraic Separation** | ✅ fatto | Il **cuore di query complexity di P^Ã ≠ NP^Ã** (l'analogo algebrico del Modulo 2). Per OR (∃ un 1 nell'oracolo): lato **NP** = *una* query (indovina il testimone, verifica sul cubo); lato **P** = lower bound esatto **κ** via **avversario di cancellazione** — finché le query algebriche sono < κ, posizioni segrete si annullano e l'algoritmo è cieco. κ cresce con N=2^m (campo piccolo: il regime di AW). Onestà: eseguiamo il cuore a query; il sollevamento a oracolo TM e il teorema asintotico di Aaronson–Wigderson sono **citati**. Genera 1 grafico SVG. `pnp_lab/algebraic_separation/`. |
| 11 | **Proof-Search Lab** | ✅ fatto | Proof-search **trasparente** (stile AlphaProof/LeanDojo) su un mini-prover di riscrittura equazionale **sound**. Un loop best-first esplora lo spazio delle prove, guidato da una **policy** che propone tattiche; ogni prova trovata è **riverificata**. Metriche oneste: una policy migliore *genera meno stati* (euristica 68 vs baseline 243 sui benchmark). L'**LLM è una policy opzionale e pluggable** (`LLMPolicy`, interfaccia `build_prompt`/`parse_tactics`), **mai nel percorso verificato**: il core non dipende da reti né chiavi. NON dimostra P vs NP — è una demo onesta della tecnica. Genera 1 grafico SVG. `pnp_lab/proof_search/`. |
| 12 | **Algorithmic Method Lab** | ✅ fatto | Il **metodo di Ryan Williams** (NEXP ⊄ ACC⁰, 2011): «un algoritmo SAT più veloce della forza bruta ⇒ un lower bound» — l'unico approccio che **aggira tutte e tre le barriere**. Cuore eseguibile (esatto): i circuiti strutturati hanno **polinomi sparsi**, quindi si conta #SAT su tutti i 2ⁿ input *senza enumerarli* (AND: 4096× più veloce; OR denso: nessun guadagno). Più la **catena win-win** e la soglia (serve speedup **super-polinomiale**). Onestà: eseguiamo il meccanismo; Easy Witness Lemma, PCP, gerarchia e l'algoritmo ACC⁰ vero sono **citati**. Genera 1 grafico SVG. `pnp_lab/algorithmic_method/`. |
| 13 | **Meta-Complexity Lab** | ✅ fatto | **MCSP & hardness magnification** — la frontiera più viva, dove il cerchio si chiude. MCSP («quanto è complessa questa funzione?») calcolato **esatto** (riuso del Modulo 6), MCSP ∈ NP (testimone = circuito, verifica = N valutazioni). Il **legame esatto con Natural Proofs** (M1): la proprietà «f è dura» è utile+larga, ma renderla *costruttiva* = risolvere MCSP = rompere i PRG (Razborov–Rudich). Più l'**hardness magnification** (citata): lower bound minuscoli `n^{1+ε}` si amplificano in P ≠ NP, ma restano bloccati dalla «barriera di magnificazione». Genera 1 grafico SVG. `pnp_lab/meta_complexity/`. |

## Pagina divulgativa

In `web/index.html` c'è una pagina (stile *La Logica dei Sistemi*) che spiega P vs NP
in modo semplice, le tre barriere, cosa fanno i tredici moduli e i risultati raggiunti.
Apri il file in un browser; i grafici sono inclusi come SVG in `web/assets/`.

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
py examples/run_proof_complexity.py  # Modulo 5: Proof Complexity Lab (piccionaia)
py examples/run_circuits.py          # Modulo 6: Circuit Complexity Sandbox (Shannon, parità)
py examples/run_algebrization.py     # Modulo 7: Algebrization Sandbox (estensione + sum-check)
py examples/run_switching.py         # Modulo 8: Switching Lemma Lab (restrizioni, Håstad)
py examples/run_algebraic_worlds.py  # Modulo 9: Algebraic Query Model (Schwartz–Zippel)
py examples/run_algebraic_separation.py  # Modulo 10: separazione P^Ã ≠ NP^Ã (query)
py examples/run_proof_search.py      # Modulo 11: Proof-Search Lab (policy + verificatore sound)
py examples/run_algorithmic_method.py # Modulo 12: Algorithmic Method Lab (Williams)
py examples/run_meta_complexity.py   # Modulo 13: Meta-Complexity Lab (MCSP)

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
