# Fable Frontier — impostazione strategica del loop agentico (2026-07-04)

**Autore dell'impostazione:** Fable 5 (sessione one-shot, il modello potente).
**Esecutori dei cicli:** agenti economici (vedi *Policy dei modelli* in fondo).
**Ripresa:** lo stato si ricostruisce SEMPRE da `RESEARCH_LOG.md` (ultima Entry) + `memory/MEMORY.md`,
MAI dalla conversazione. Frase di ripresa: *"continua il ciclo fable-frontier"*.

---

## 1. Dove siamo (una riga per orientare gli agenti)

19 collassi / 7 arene, Attractor Thesis rafforzata; TUTTE le porte interne (A/C/B) chiuse con la
stessa firma (oggetto simmetrico ⇒ ricostruzione dal dizionario d'orbita; sopravvivenze apparenti =
artefatti di rottura di simmetria o omissione di una legge). Restano **genuinamente aperte, oltre il
muro brute-force,** SOLO le due falsifier door del grand capstone:

- **DOOR-2 (certified n≥7 / d≥7):** un invariante certificato — non enumerato — che dica qualcosa
  di vero OLTRE il muro (d≥7 per Kronecker, n≥5..7 per i Boolean).
- **DOOR-3 (leva cross-livello CRESCENTE):** un oggetto il cui contenuto fuori-dizionario CRESCE
  con la scala invece di saturare/collassare.

Ogni ciclo che non punta a una di queste due porte è, per costruzione, un RESTATEMENT in attesa.

## 2. La tesi strategica di Fable 5

Il lever umano di Entry 34→35 (cono dei momenti di Kronecker) è il PRIMO oggetto del lab che
attacca **entrambe** le porte simultaneamente, ed è per questo la direzione giusta:

1. **Le faccette del cono sono certificati scale-free.** P_D = conv{punti normalizzati con g>0}
   è un'inner approximation del cono dei momenti; per convessità ogni faccetta valida su P_D che
   sia faccetta del CONO vale a OGNI scala d. Una disuguaglianza lineare `a·x ≤ b` si verifica su
   una terna di d=7,8 **senza calcolare l'intera g-matrice**: serve solo il punto normalizzato.
   È il primo ponte concreto sopra il muro d≥7 → DOOR-2.
2. **La leva si misura sul turnover delle faccette.** La catena P_3 ⊆ P_4 ⊆ P_5 (⊆ cono) dà una
   misura ESATTA di leva: quante faccette fuori-dizionario nascono/muoiono passando da D a D+1?
   Se il contenuto fuori-dizionario cresce con D → DOOR-3. Se satura → collasso coerente con
   l'attrattore, e va detto.
3. **Il cono è symmetry-respecting per costruzione** (support = orbite di permutazione complete),
   quindi NON può morire dell'artefatto di Entry 34 (proxy che rompe la g-simmetria). Se muore,
   muore di riduzione onesta (Farkas dal dizionario) — informazione pulita in entrambi i casi.

## 3. Le direzioni (in ordine di esecuzione; ciascuna con killer pre-dichiarato)

### CICLO IN CORSO — Entry 35: "buchi e faccette del cono esatto"
Builder GIÀ completo (`pnp_lab/gct_kronecker/moment_cone.py`, 15 test, example). Ipotesi e killer
pre-dichiarati nel docstring del modulo (KILLER-1: tutti i buchi in-cono superficiali ⇒ cono =
stretch esteso ⇒ RESTATEMENT; KILLER-2: H-rep implicata dal dizionario {nonneg, ordering} via
Farkas ⇒ RESTATEMENT; SOPRAVVIVENZA: buco PROFONDO oppure faccetta fuori-dizionario).
Resta: misure → adversary → evaluator → archivist. **Attenzione adversary:** una faccetta
"fuori-dizionario" rispetto al dizionario ELEMENTARE non è ancora contenuto — va tentata la
riduzione a (i) disuguaglianze note in letteratura (Klyachko per il caso rettangolare, condizioni
di dominanza), (ii) faccette ereditate da P_{D-1} per lifting banale, (iii) artefatti
dell'inner-approximation (faccetta di conv(S) che NON è faccetta del cono).

### CICLO +1 — Entry 36: "il ponte certificato" (DOOR-2, il vero colpo)
SE Entry 35 produce faccette fuori-dizionario sopravvissute all'adversary: prendile come
**predizioni certificate a d=7,8**. Protocollo: (a) genera terne MIRATE di d=7 vicine alla
faccetta (tight o quasi-tight); (b) per ciascuna calcola SOLO quei g(λ,μ,ν) (Murnaghan–Nakayama su
singole terne è fattibile a d=7-8; è l'ENUMERAZIONE COMPLETA a essere il muro, non la singola
valutazione); (c) verifica: la faccetta separa davvero g=0 da g>0 oltre il muro?
KILLER: la faccetta smette di essere valida a d=7 (era un artefatto dell'inner approximation a
D piccolo) oppure non separa nulla di nuovo. SOPRAVVIVENZA: prima predizione certificata del lab
verificata OLTRE il muro. Questo sarebbe il primo attraversamento genuino di DOOR-2.

### CICLO +2 — Entry 37: "la leva del cono" (DOOR-3)
Misura il turnover: faccette(P_3) → faccette(P_4) [già fattibile, ~8 min, marcato slow] → P_5 se
il beneath-beyond regge (altrimenti: solo conteggio faccette fuori-dizionario via campione di
direzioni + LP, senza H-rep completa — resta esatto per direzione). Grandezza-leva:
`L(D) = #fuori-dizionario(P_D) / #faccette(P_D)` e la sua monotonia.
KILLER: L(D) costante o decrescente ⇒ il contenuto extra satura ⇒ RESTATEMENT (attrattore).

### CICLO +3 (meta, se 35-37 collassano) — "il Teorema dell'Attrattore"
Il deliverable onesto del lab NON è P vs NP: è il fatto che 19 oggetti indipendenti in 7 arene
collassano con la STESSA firma. Renderlo un OGGETTO ESEGUIBILE: costruire il reticolo (lattice)
degli invarianti calcolati in tutte le arene (ordinato per ricostruibilità-Farkas / splits=0) e
misurare se la chiusura-dizionario è FINITAMENTE GENERATA (pochi generatori assorbono tutto).
KILLER: il reticolo non è finitamente generato o la firma non è formalizzabile ⇒ la tesi resta
narrativa. SOPRAVVIVENZA: un teorema empirico del lab, cristallizzabile come capstone finale.

### ARENA DI RISERVA (solo su gate ROSSO ripetuto) — "quantum marginal problem"
Il cono dei momenti di Kronecker È il cono di compatibilità degli spettri dei marginali quantistici
(Christandl–Mitchison). Stesso oggetto, seconda incarnazione: riusa `kronecker.py` per testare se
il dizionario dell'arena 7 ricostruisce la membership QMP. Pivot a una clausola, costo ~0.

## 4. Protocollo del ciclo (invariato dal lab, con gate graduato)

explorer → builder → **misure esatte** → adversary (il passo più importante) → evaluator
(robustness + flag + honesty boundary EN) → archivist (RESEARCH_LOG append-only + memory/ +
commit). Gate: sopravvivenza vera ⇒ Module + docs; KILLED/RESTATEMENT ⇒ Entry-only, probe CITATO.
Regole ferree: solo aritmetica ESATTA (Fraction/int), killer PRE-dichiarati, nessun claim su
P vs NP nell'honesty boundary.

## 5. Policy dei modelli (economia del loop)

| Ruolo | Modello | Perché |
|---|---|---|
| strategist (cicli 36+) | sonnet | decisioni di direzione, non servono idee nuove: il menu è QUESTO file |
| explorer | haiku | l'ipotesi dei cicli 35-37 è già scritta qui; deve solo istanziarla |
| builder | sonnet | codice esatto + test: serve affidabilità, non genialità |
| adversary | **sonnet** | il ruolo critico; haiku è troppo debole per il red-team matematico |
| evaluator | haiku | scoring templato (flag/robustness/honesty boundary) |
| archivist | haiku | append log + memoria, templato |
| escalation | fable/opus | SOLO su sopravvivenza vera post-adversary o su gate ROSSO strutturale |

Regola d'oro: l'unica cosa che NON si delega ai modelli piccoli è il giudizio "sopravvivenza vs
artefatto". Se l'evaluator dà robustness ≥ 7 o l'adversary NON trova il killer, si ESCALA a un
modello forte prima di cristallizzare.
