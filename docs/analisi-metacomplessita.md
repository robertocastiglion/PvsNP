# Analisi: la meta-complessità come oggetto del laboratorio

> Documento analitico (non codice) — registra i ragionamenti e i verdetti maturati
> sul progetto P/NP Research Lab. Complementa README.md (che descrive il codice) e i
> docstring dei moduli. Ultimo aggiornamento: 2026-06-02.
>
> **Principio guida**: onestà intellettuale. Ogni affermazione o si esegue, o è
> dimostrata, o è citata. Niente claim di risoluzione di P vs NP, niente hype.

---

## 0. La domanda di fondo

Il laboratorio nasce attorno a P vs NP e alle sue tre barriere (relativizzazione,
natural proofs, algebrizzazione). La tesi esplorata in questa analisi è più forte:
**il vero oggetto del laboratorio non è P vs NP, ma la meta-complessità** — la
"complessità della conoscenza della complessità": non solo *quanto è difficile un
problema*, ma *quanto è difficile sapere quanto è difficile un problema*.

Tre operazioni meta-computazionali:
- **calcolare** la complessità (MCSP, Kt);
- **dimostrare** la complessità (proof complexity, barriere, indimostrabilità);
- **riconoscere** la complessità (natural proofs / learning).

---

## 1. Gerarchia a 4 livelli (la struttura della tesi)

| Livello | Oggetto | Difficoltà di… |
|---|---|---|
| L0 | calcolare $f$ | risolvere un problema |
| L1 | calcolare la durezza di $f$ | MCSP, MKtP, Kt |
| L2 | dimostrare la durezza di $f$ | proof complexity, barriere, unprovability |
| L3 | riconoscere/apprendere la durezza | natural proofs / learning |

I 14 moduli mappati: M6 (Shannon) è l'ancora L0/L1; M13 (MCSP) è L1; M5 (proof
complexity), M1–M2–M7..M10 (barriere) sono L2; M1 (natural proofs) è L3; M12
(metodo algoritmico di Williams) è la cerniera L0↔L2; M14 tenta l'unificazione.

---

## 2. "Il problema è indimostrabile?" — risposta precisa

No. Distinzione necessaria fra tre affermazioni diverse:

1. **"Non dimostrabile con le tecniche attuali"** — ✔ vero, è ciò che dicono le
   barriere (affermazioni sulle *tecniche*, non sul problema; temporanee).
2. **"Formalmente indipendente da ZFC"** — ✘ mai dimostrato; consenso: improbabile.
3. **"Indimostrabile in teorie deboli"** (Razborov 1995, Pich–Santhanam) — ✔ ma
   *condizionato* e ristretto all'aritmetica limitata ($S^2_2$, PV, APC₁), non ZFC/PA.

Prova che NON è indimostrabile: **Williams 2011** ($\mathrm{NEXP}\not\subset\mathrm{ACC}^0$)
scavalca tutte e tre le barriere. Sono ostacoli, non muri. P vs NP è un enunciato
aritmetico con valore di verità definito; se $P=NP$ è testimoniato da un algoritmo
(quindi dimostrabile); se $P\neq NP$ non c'è evidenza di indipendenza.

---

## 3. Verdetto formale (stile STOC/FOCS) sulla tesi meta-complessità

**Formalizzazione minima.** I tre verbi:
- *calcolare* → linguaggio $Q_\mu=\{(\mathrm{desc}(O),s):\mu(O)\le s\}$ (per $\mu=\mathrm{CC}$ è MCSP);
- *calcolare la complessità della complessità* → la classe di complessità di $Q_\mu$ stesso;
- *dimostrare* → proof complexity $\ell_P(\ulcorner\mu(O)\ge s\urcorner)$.

**Modello unico (e suo limite).** Unificazione legittima solo come *famiglia di
predicati condivisa* $\mathrm{Hard}_{\mu,s}=\{\mathrm{desc}(O):\mu(O)\ge s\}$, con tre
"lenti" computazionali: $L_{\text{comp}}$ (decidere = MCSP), $L_{\text{prove}}$
(certificare = proof complexity), $L_{\text{recog}}$ (riconoscere = natural
proofs/learning). **Non esiste una misura scalare unica** che le unifichi (modelli
di costo non commensurabili). Questo è dichiarato esplicitamente, non aggirato.

**Riduzioni a risultati noti.** $L_{\text{comp}}$: Kabanets–Cai 2000, Hirahara 2018,
Murray–Williams 2017. $L_{\text{recog}}$: Razborov–Rudich 1994, CIKK 2016. 
$L_{\text{prove}}$: Cook–Reckhow 1979, Haken 1985, Razborov 1995, Pich–Santhanam
2019–21. Ponti inter-lente (struttura vera, sono teoremi): Williams 2011,
Impagliazzo–Wigderson 1997.

**Verdetto: (B)** — riorganizzazione concettuale corretta e non banale di un campo
*già esistente* (meta-complexity). Non (C) (è formalizzabile); non (A) (nessun nuovo
oggetto/teorema). Residuo aperto: se le tre lenti collassino è un problema aperto già
interno alla meta-complessità (programma Hirahara).

---

## 4. Upgrade categoriale: tesi forte = (A) condizionato

Obiezione corretta: "nessuna misura scalare" $=$ nessun funtore fedele
$\mathcal{C}\to(\mathbb{R},\le)$; **non** confuta una tesi basata su un *invariante
strutturale* (equivalenza di trasformazioni) invece che su una funzione.

**Formalismo proposto**: categorie arricchite su quantali (Lawvere 1973). UNA sola
categoria sottostante $\mathcal{C}$ (oggetti $\mathrm{Hard}_{\mu,s}$; frecce =
riduzioni), arricchita tre volte su quantali incompatibili $V_{\text{time}},
V_{\text{proof}}, V_{\text{sample}}$ (cambio di base, Eilenberg–Kelly). Tesi forte =
"le tre lenti sono gli STESSI morfismi di $\mathcal{C}$ visti tramite tre
arricchimenti"; l'invariante = $\mathcal{C}$ sottostante, non uno scalare.

**Stato teorema/aperto** ("le tre lenti arricchiscono la stessa $\mathcal{C}$?"):
- **riconoscere ⟺ apprendere**: equivalenza stretta (CIKK 2016, un *iff* senza perdita);
- **calcolare → riconoscere** (RR 1994), **calcolare → dimostrare** (Williams 2011):
  natural transformation non invertibili/condizionate.

Il divario lasso-vs-equivalenza coincide col gap di Hirahara 2018 + la barriera di
località (Chen–Hirahara–Oliveira–Pich 2020). Quindi tesi forte = **(A) condizionato**:
diventa struttura nuova sse quei gap collassano.

**Invariante di sistema non-scalare candidato**: l'esistenza di pseudocasualità
crittografica (OWF/PRF) — pivot sì/no visto da tutte e tre le lenti (RR 1994 +
Kabanets–Cai 2000 + Razborov 1995). Scheletro qualitativo dell'auto-referenza:
teorema del punto fisso di Lawvere 1969 (Yanofsky 2003).

---

## 5. Modulo 14 (Enriched Meta-Category) — e la sua critica severa

**Cosa fa** (`pnp_lab/enriched_meta/`, 12 test). Rende eseguibile la §4 su $n=3$:
$\mathcal{C}$ = funzioni booleane + rinomine $S_n$; tre realizzazioni del predicato di
durezza $H_s(f)=[\text{cost}>s]$ ($\chi_{\text{comp}}$ esatto, $\chi_{\text{recog}}$ =
influenza totale $>\theta$, $\chi_{\text{prove}}$ = lower bound certificabile entro
budget); matrice dei "difetti di composizione". Risultati a $s=3$: calc↔prove $=0$
(col budget), calc↔recog $=0.117$, recog↔learn $=0$.

**Critica (verdetto: (V) — visualizzazione utile, NON invariante strutturale).**
Il "difetto" misurato è un **artefatto di rappresentazione finita / metrica non
canonica**, non un invariante stabile:

1. **Scaling.** La metrica è una *media uniforme* su $2^{2^n}$ funzioni. Per
   $n\to\infty$: largeness (RR) + concentrazione dell'influenza a $n/2$ + Shannon
   ⇒ $\{\text{cost}>s\}$ e $\{I>\theta\}$ hanno entrambi misura $\to 1$ ⇒
   $\text{defect}(\text{compute},\text{recognize})\to 0$. Il $0.117$ a $n=3$ è
   finite-size, senza significato asintotico.
2. **Tautologie.** $\chi_{\text{prove}}\equiv\chi_{\text{comp}}\wedge(\text{budget}\ge L)$
   e il learner ri-fitta la stessa feature: i due "0" sono imposti dalle definizioni,
   non misurati. Il costo di prova è l'enumerazione brute-force, **non** la lunghezza
   minima in un sistema fissato → non modella Cook–Reckhow.
3. **Metrica non canonica.** L'influenza totale è una statistica scalare arbitraria;
   altre scelte ugualmente naturali danno numeri diversi. La costruttività è una
   nozione *asintotica* ($\text{poly}(N)$), priva di senso a $n$ fisso.
4. **Distribuzione sbagliata.** Il contenuto teorico riguarda funzioni esplicite /
   caso peggiore (misura zero); la media uniforme li ignora.

**Invarianza categoriale**: il modulo non la soddisfa nemmeno debolmente — il difetto
non è preservato da cambio di rappresentazione, scelta dei morfismi (usa solo $S_n$;
l'isometria del costo è *definitoria*, non un test), cambio di base, o rifinitura
$n\to n+1$. **Falsificazione**: a $n\to\infty$ il difetto collassa a 0 senza cambiare
la struttura della complessità; passando dalla media al caso peggiore ($\exists$) lo
stesso fenomeno diverge a 1 (counting: l'influenza ha $O(n2^n)$ valori contro
$2^{2^n}$ funzioni). La coesistenza media$\to0$/peggiore$\to1$ prova che il numero è
artefatto della metrica.

**Per spostare M14 verso (S)** servirebbe: (i) enunciato di caso peggiore o ristretto
allo strato di bassa complessità invece della media uniforme; (ii) quantificazione su
*tutte* le proprietà costruttive di una classe, non una statistica; (iii) lunghezza di
prova in un sistema fissato invece dell'esaustione. Senza questi tre, il valore non è
interpretabile come invariante.

---

## 6. Modulo 14 riparato verso (S)

Risposta operativa alla critica (V): si attaccano i tre difetti identificati, su
un'unica misura (dimensione di **circuito**, calcolata esatta). Codice in
`pnp_lab/enriched_meta/synthesis_sat.py`, `recognize_class.py`, `repaired.py`
(11 test, demo `examples/run_enriched_meta_repaired.py`).

**Fix (iii) — "dimostrare" = refutazione reale.** "∃ circuito di ≤ s gate per f" è
codificato come CNF di *exact synthesis*; `size(f) > s` ⟺ UNSAT, e la lunghezza
della refutazione (resolution tree-like, via il DPLL del Modulo 5) è la vera proof
complexity del lower bound. Misure: XOR2 (n=2) refuta `size>2` in **2055 nodi**;
AND3 (n=3) refuta `size>1` in **71 nodi**. Non più tautologico.

**Fix (ii) — "riconoscere" = classe, non statistica.** La lente è il *minimo errore*
della miglior proprietà di una classe a risorse limitate (alberi di decisione prof.
≤ d su feature costruttive), non l'influenza arbitraria. Si misura la curva
errore(d) = **prezzo della costruttività**.

**Fix (i) — metrica stratificata.** Errore misurato sulla *finestra critica*
attorno alla soglia, non sulla media uniforme che la concentrazione rende triviale.

**Risultati.** n=2 (tutto esatto via SAT): la classe separa, errore →0. n=3 (finestra
critica): a s=3 errore(d) = **[0.46, 0.17, 0.05, 0.05]** — *non scende a 0* e fa
**plateau** a ~0.05 aumentando d. A s=2 invece svanisce (regime piccolo). La lente
"dimostrare" a n=3 sulle funzioni dure (size ~6) **esplode** (refutazione oltre
budget, ~60s): il muro reale della proof complexity.

**Regimi di calcolabilità (onesti).** n=2: tre lenti esatte sulla stessa misura
(circuito via SAT, 16 funzioni). n=3: "riconoscere" esatta su dimensione di *formula*
M6 (proxy); "dimostrare" esatta solo sullo strato a bassa complessità.

**Ri-verdetto: (S)-candidato, non (S).** I due artefatti della v1 sono rimossi — la
lente "dimostrare" non è più tautologica e quella "riconoscere" non svanisce sulla
metrica stratificata (resta un residuo ~0.05 che non cala con le risorse, il
fenomeno natural-proofs). Nuovo modo di fallimento *strutturale* (non artefatto): la
lente "dimostrare" esplode (proof complexity). **Limite onesto**: con n ≤ 3
calcolabile, l'invarianza asintotica del residuo NON è verificata — due punti (n=2:
0; n=3: ~0.05) suggeriscono ma non dimostrano stabilità. Per (S) servirebbe mostrare
che il residuo stratificato è stabile per n→∞, fuori dalla portata del calcolo
esatto. Il modulo è quindi salito da **(V) artefatto** a **(S)-candidato difendibile**.

### 6.1 Strada #1 — solver più forte (CDCL) e il terzo punto

Per dare un terzo punto al residuo serviva spingere oltre n=3. Costruito un **CDCL
da zero** (`pnp_lab/enriched_meta/cdcl.py`: 2-watched literals, 1-UIP, backjump,
VSIDS, restart di Luby; 6 test, concorda col DPLL del M5 su PHP, modelli validi).

Esito sul *lato dimostrare*: anche il CDCL **esplode** sulle istanze di sintesi
UNSAT delle funzioni dure (provare `size>s` vicino al vero è un lower bound
genuino) — conferma che il muro è reale, non ingegneria debole. La misura a n=4 è
quindi ottenuta non via SAT ma con la **DP capped del Modulo 6** (formula size fino
a un cap; cap=8 → 39 582 funzioni in ~7s). La DP *completa* a n=4 non termina in
tempi interattivi (esplosione combinatoria) — un altro muro onesto.

Terzo punto, residuo della lente "riconoscere" su finestre interne (soglia
relativa, campione 300):

| n | finestra | residuo |
|---|---|---|
| 2 | (banale) | 0 |
| 3 | s=3 centrale | 0.046 |
| 4 | s=6 interna | 0.173 (0.097–0.167 su s∈{5,6,7}) |

Il residuo **cresce con n** e a n=4 è **robusto** (non svanisce aumentando le
risorse della classe, plateau ~0.1–0.17). Questo rafforza il (S)-candidato:
coerente con un prezzo *strutturale* della costruttività (natural proofs).

**Caveat onesti.** A n=3 il residuo è positivo solo nella banda centrale (s=3) e
nullo a s=5,6: dipende dalla posizione. Le finestre n=4 sono *sotto la mediana
vera* (size>8 fuori portata) e *campionate*; il residuo è relativo a *questa*
classe di 4 feature. Tre punti (n=2,3,4) non sono invarianza asintotica. **Verdetto
invariato: (S)-candidato rafforzato, non (S) confermato.** Per (S) servirebbe
l'andamento al regime mediano e per n→∞, fuori dalla portata del calcolo esatto.

### 6.2 Strada #2 — l'enunciato di caso peggiore (∃/∀)

La barriera natural-proofs non è una media: la *utilità* è un ∀ (rifiutare TUTTE le
funzioni facili). Codice in `pnp_lab/enriched_meta/worstcase.py` (5 test). Due
oggetti distribution-free:

**Collisioni di feature** (ostruzione ∃). Una funzione dura con lo stesso vettore di
feature di una facile non è separabile da NESSUNA proprietà nello spazio, a qualsiasi
risorsa. Misura:

| n | s | frazione di collisioni | larghezza utile max (=1−frac) |
|---|---|---|---|
| 2 | 1 | 0.000 | 1.000 |
| 3 | 3 | 0.100 | 0.900 |
| 4 | 6 | **0.914** | **0.086** |

**Quasi un teorema, non solo empirico**: k feature con poly(N) valori danno
2^O(k·log N) vettori distinti contro 2^(2^n) funzioni ⇒ per pigeonhole la frazione di
collisioni → 1 per n→∞, per QUALUNQUE classe di feature fissa. Il salto 0.10→0.91 ne
è l'istanza calcolata.

**Tradeoff utilità-larghezza**: la massima larghezza di una proprietà *utile* (∀
facili rifiutate) a risorse d resta bassa (n=4, d=3: ~0.30 su campione, ≤0.086 sul
window pieno per le collisioni). La classe costruttiva non può essere utile *e* larga.

**Interpretazione (onesta).** Nella forma worst-case l'ostruzione è **robusta e
cresce con n** — il segnale strutturale che la media non dava. MA è esattamente la
condizione di utilità di **Razborov–Rudich** resa eseguibile: come oggetto
strutturale è reale (S-supporting), come *nuovo* invariante è **(B)** — riduce alla
barriera nota. La frazione numerica dipende dalla classe di feature; il limite →1 è
dell'argomento di counting, non del modulo.

### 6.3 Sintesi delle due strade

Tre forme dello stesso difetto, tre comportamenti:
- **media uniforme** (v1) → 0 per concentrazione = **artefatto (V)**;
- **media stratificata** (riparazione + strada #1) → residuo che cresce con n
  (0, 0.05, 0.17) ma fragile/relativo alla classe = **(S)-candidato**;
- **caso peggiore ∃/∀** (strada #2) → ostruzione robusta → 1 per counting, ma
  **coincide con la barriera natural-proofs** = strutturale ma **(B)** come invariante.

**Verdetto complessivo onesto.** M14 non è un *nuovo* invariante: nella sua forma
matematicamente corretta (worst-case) il difetto È la barriera di Razborov–Rudich,
resa eseguibile e quantificata su n piccolo. Questo è un esito di valore — un
*rendering* fedele e misurabile di un teorema profondo — ma non una nuova struttura.
La domanda (S) originale ("invariante categoriale stabile") resta non dimostrata; la
sua versione difendibile è: *il difetto worst-case è strutturale e noto*.

---

## 7. Riferimenti citati

Baker–Gill–Solovay 1975 · Razborov–Rudich 1994 · Aaronson–Wigderson 2008 ·
Cook–Reckhow 1979 · Haken 1985 · Razborov 1995 · Kabanets–Cai 2000 ·
Carmosino–Impagliazzo–Kabanets–Kolokolova 2016 · Hirahara 2018 · Williams 2011 ·
Impagliazzo–Wigderson 1997 · Oliveira–Pich 2018 · Chen–Hirahara–Oliveira–Pich 2020 ·
Pich–Santhanam 2019–21 · Lawvere 1969, 1973 · Yanofsky 2003 · Gödel 1956 (lettera a
von Neumann).
