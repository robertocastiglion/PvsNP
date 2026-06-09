# RESEARCH LOG — PvsNP-lab (autonomous research loop)

Append-only. Una entry per ciclo. All'avvio di ogni esecuzione: ricostruisci lo
stato dall'ULTIMA entry qui + memory/, NON dalla conversazione. Ogni entry termina
con "NEXT unstable direction:".

Ruoli del loop: Explorer → Builder → (misura) → Adversary → Evaluator → Archivist,
orchestrati dal Principal Investigator. Specifica completa: prompts/research-loop.md.

---

## Entry 0 — Stato di partenza (2026-06-07)

**Archi precedenti (CHIUSI, non ripartire da qui):**
- Module 16 `bounded_observer/` — i 4 barrier come Δ≤ε: verdetto downgrade,
  natural proofs e proof complexity sullo stesso lato (debito di pseudorandomness).
- Module 17 `survival_test/` — il test 𝒭=∞: criterio di classificazione, ma audit
  ostile lo ha mostrato PROVABLY CIRCULAR (misura la propria etichetta in input).
- Module 18 `exactness_composes/` — congettura "EXACTNESS COMPOSES" su G*=Cov−LP:
  VERA-ma-banale per tensor (multiplicatività LP, Lovász), FALSA per lifting
  (controesempio OR₂∘XOR = J−I₄: Cov=4, LP=3, G*=1). Congettura UCCISA.
- VERDETTO d'arco: il programma μ_R/G(R) è un DIZIONARIO corretto su
  {Kolmogorov resource-bounded, dualità LP/SDP/game, i 4 barrier, lifting,
  meta-complessità}; nessun contenuto predittivo nuovo. Arco definitivamente chiuso.

Vedi memory/duality-gap-theory.md e memory/bounded-observer-verdict.md per i dettagli.

**Asset riutilizzabili nel repo:** simplex razionale esatto (Module 18), codice Dcc
(comunicazione deterministica, cycle-3), set-cover/packing esatti, modello TM
time-bounded + tableau Cook-Levin, proof-search su Lean reale, switching lemma
depth-d, mondi algebrici / separazione algebrica.

**Direzioni instabili CANDIDATE per il prossimo ciclo (l'Explorer ne sceglie/affina
UNA; sono semi, non vincoli — è benvenuta una direzione nuova non elencata):**

1. *Proof complexity automatizzabilità sul piccolo.* Misurare esattamente, su
   formule UNSAT minuscole, una quantità legata alla non-automatizzabilità
   (Atserias–Müller) o all'interpolazione fattibile — c'è un divario MISURABILE che
   non sia solo riformulazione del debito di pseudorandomness?
   Killer: ogni numero ottenuto si deriva da size/width già nel repo → RESTATEMENT.

2. *Meta-complessità concreta su tavole di verità minuscole.* Calcolare MCSP/MKtP
   esatti su funzioni a ≤4 bit e cercare un fenomeno discriminante (es. una
   transizione) che NON sia immediatamente Hirahara/KT.
   Killer: il fenomeno è esattamente KT-complexity ridefinita.

3. *Lifting lossy con gadget oltre 1 bit, esatto.* Il kill di Module 18 vive sul
   gadget XOR 2×2. Mappare per quali piccoli gadget il gap di integralità nasce vs
   collassa (allineato/misallineato, cycle-3), cercando una REGOLA predittiva su
   quali gadget aprono il gap — sarebbe contenuto nuovo se non segue da Lovász.
   Killer: la regola è il teorema di multiplicatività della frazione di copertura.

**NEXT unstable direction:** PI + Explorer selezionano/affinano una tra le tre
sopra (o ne propongono una nuova con killer dichiarato) ed eseguono il primo ciclo
completo. Criterio di stop: vedi prompts/research-loop.md (fermarsi e chiedere
all'umano su NEW CONTENT robustness≥7 senza flag, o su 2 KILLED/RESTATEMENT di fila
senza nuova direzione, o per decisioni di commit/scope).

---

## Entry 1 — Ciclo 1: regola sui gadget per il gap del lift (2026-06-07)

**Direzione testata:** (3) lifting lossy — QUALI gadget aprono il gap di integralità
G★=Cov−LP nel lift f∘g^k (domanda lasciata aperta da Module 18, che aveva solo UN
controesempio OR₂∘XOR).

**Ipotesi (Explorer):** G★>0 SSE il gadget g è una PERMUTAZIONE 2×2 ({XOR,EQ}) e
l'outer produce una pattern-matrix non integrale. Discriminante dichiarato: EQ è
permutazione ma non-Fourier → se EQ apre il gap come XOR la regola è "permutazione"
(nuovo), altrimenti "pattern-matrix Fourier" (restatement). Killer: una cella con g
non-permutazione e G★>0, oppure g∈{XOR,EQ} con outer "non-apertura" e G★>0.

**Costruito (Builder):** pnp_lab/exactness_composes/gadget_rule.py (gap_table,
predict_gap, is_permutation_gadget; riusa gap.py/compose.py di Module 18) +
tests/test_gadget_rule.py (11 passed, 0.64s) + examples/run_gadget_rule.py.

**Numeri esatti misurati:**
- k=2 esaustivo (54 celle): uniche 4 celle con gap = (OR,XOR),(OR,EQ),(NAND,XOR),
  (NAND,EQ), tutte Cov=4, LP=3, G★=1. predict_gap coincide col misurato su 54/54.
- Discriminante: G★(OR∘XOR²)=G★(OR∘EQ²)=1; bridge strutturale lift(f,XOR,k) =
  lift(f,EQ,k) a meno di permutazione colonne, ogni k.
- k=3: celle sparse (AND/NOR) → G★=0; celle dense con permutazione SALTATE (LP
  esatto su 8×8 dense ~628s — nessun float introdotto).

**Verdetto Adversary:** RESTATEMENT-OF-KNOWN. Demolizioni verificate in codice:
(A) EQ[x][y]==XOR[x][1-y] → EQ è XOR con un input negato = STESSA pattern-matrix di
Fourier; il discriminante "permutazione vs Fourier" è VUOTO (il bridge prova che sono
la stessa matrice, non che permutazione ⊋ Fourier). (B) tutte e 4 le celle-gap sono
J−I₄ (a k=3 J−I₈); Cov(J−I_m)=m, LP=m−1, gap elementare e noto. (C) circolarità:
predict_gap per XOR misura il gemello EQ (provatamente identico); segnale reale = 2
outer × 1 classe gadget, 42/54 celle sono 0=0; MAJ≡AND su 2 bit. (D) {XOR,EQ} = i
soli gadget affini GF(2) non-degeneri = la dicotomia allineato/misallineato di cycle-3
rietichettata. Riduzione precisa: gadget→pattern-matrix (Sherstov/Razborov XOR-lift)
+ pattern→J−I (dualità LP elementare).

**Evaluator:** robustness 8/10. Flag: circolarità, confirmation-bias, off-tiny-
instance (celle dense k=3 non misurate indip.). Verdetto: RESTATEMENT-OF-KNOWN, nessun
contenuto predittivo nuovo. Coerente col verdetto d'arco di Module 18.

**Scritto/committato:** modulo + test + esempio creati, NON committati. Nessun nuovo
Module cristallizzato (verdetto = restatement, non si pubblica).

**Nota infrastruttura (richiesta utente) — RISOLTA.** `py -m pytest` non chiudeva.
Diagnosi (timeout per-file): UN solo file sforava, test_exactness_composes.py, con 3
test esaustivi/densi — test_no_gap_below_4x4 (sweep 3x4 = 4096 set-cover),
test_smallest_gap_matrix_is_4x4_half (enumera fino a 4x4), e
test_lift_counterexamples_all_have_integral_gadget (sweep k=2,3, LP su 8x8 densa
~628s). test_iterate_switching NON era >15min (33s reali: il gonfiamento era da
processi python "zombie" di run interrotti). Fix: installato pytest-timeout; creato
pytest.ini (addopts `--timeout=120 --timeout-method=thread -m "not slow"`); marcati i
3 test `@pytest.mark.slow @pytest.mark.timeout(900)`. Risultato: `py -m pytest` =
264 passed, 1 skipped, 7 deselected in ~63s (prima: non terminava); i lenti restano
con `py -m pytest -m slow`. Strategia bakata in .claude/agents/builder.md. README
aggiornato.

**NEXT unstable direction:** Tutte le celle-gap trovate finora sono J−I (gap di
integralità banale). Per salvare un claim servirebbe un gap di TIPO DIVERSO da J−I:
cercare la più piccola pattern-matrix f(x⊕y) con G★>0 che NON sia J−I (outer a 3 bit:
MAJ3, 1-in-3, threshold), oppure un gap su gadget a 2 bit (4×4) non riducibile a XOR
lineare. Se ogni gap≤ una certa taglia è J−I → ulteriore conferma "collapse onto
LP-dualità elementare" e l'arco lifting/G★ va dichiarato CHIUSO come Module 18.
Killer: la prima pattern-matrix-gap non-J−I a ≤3 bit. (Se due cicli di fila danno
restatement senza direzione nuova → STOP e chiedere all'umano, da spec.)

---

## Entry 2 — Ciclo 2: gap di lift non-J−I? (2026-06-07)

**Direzione testata:** esiste un gap di integralità G★>0 da LIFT (pattern-matrix
f(x⊕y)) che NON sia J−I, a ≤3 bit? (killer del "tutto-è-J−I" del ciclo 1).

**Costruito (Explorer+Builder):** pnp_lab/exactness_composes/pattern_gap.py
(pattern_matrix, is_J_minus_I_up_to_perm, named_3bit_outers, all_3bit_outers,
pattern_gap_table, first_non_JI_gap) + tests/test_pattern_gap.py (9 veloci + 1 slow
esaustivo) + examples/run_pattern_gap.py. Riusa gap.py. Suite non bloccata.

**Numeri esatti (8×8 = 3 bit):** il KILLER del "tutto-è-J−I" SCATTA subito —
ONE_IN_3 → adiacenza ipercubo Q3, Cov=8, LP=6, G★=2, NON J−I. Censimento esaustivo
≤32 ones (256 funz, 395s): 56 celle con gap, tutte G★=2 non-J−I. peso-56 → tutte
J−I (G★=1, famiglia ciclo 1). Quindi il ciclo 1 "tutto-è-J−I" è FALSIFICATO: esistono
gap di lift non-J−I già a 3 bit.

**Verdetto Adversary:** RESTATEMENT-OF-KNOWN. Riduzione esatta verificata: G★(Q3) =
bc(G) − bc*(G) = integrality gap del biclique/rectangle-cover LP di un grafo bipartito
(= nondeterministic communication / rectangle cover; Lovász set-cover duality). J−I è
il caso K_m, Q3 il caso Cayley 3-regolare di Z2³. DISCRIMINANTI: (1) (Cov,LP,G★) è
determinato da |S| (connection set): |S|=3 → (8,6,2) per TUTTI i 35 set; ONE_IN_3/Q3
non è speciale. (2) grafi 3-regolari bipartiti GENERICI (non-Cayley): G★∈{0,½,1}, mai
2 → la struttura Cayley MASSIMIZZA un gap noto (più C₄/bicliques), ma non è una
predizione nuova della teoria. La pattern-matrix è la XOR-lift di Sherstov/Razborov,
con connection set più ricco. Niente contenuto predittivo nuovo.

**Evaluator:** robustness 8/10. Flag: confirmation-bias (in calo). Verdetto:
RESTATEMENT-OF-KNOWN. "Non-J−I" vero come stringa, vuoto come contenuto (stessa
famiglia biclique-cover-LP). Honesty boundary: misure esatte ≤3 bit, non asintotiche.

**Scritto/committato:** pattern_gap.py + test + esempio creati, NON committati.
Nessun Module cristallizzato.

**STOP — criterio di spec raggiunto.** Due cicli consecutivi (Entry 1 + Entry 2) =
RESTATEMENT-OF-KNOWN. Pattern convergente RAFFORZATO: OGNI gap di lift G★ misurato
(J−I e Q3 e tutti i |S|=3) si riduce all'integrality gap del rectangle/biclique-cover
LP — la dualità set-cover elementare. L'arena lift NON produce contenuto nuovo oltre
questa dualità. Il loop si ferma e CHIEDE ALL'UMANO: dichiarare l'arena lift/G★
definitivamente chiusa (come Module 18) e, se si vuole proseguire, PIVOT a un
programma di ricerca genuinamente diverso (NON G★/lift/cover) — candidati fuori-arena:
proof complexity automatizzabilità (dir.1 di Entry 0, mai tentata) o meta-complessità
concreta MCSP/MKtP su tavole minuscole (dir.2 di Entry 0, mai tentata).

**NEXT unstable direction (in attesa di decisione umana):** se PIVOT → dir.1 o dir.2
di Entry 0 (fuori dall'arena cover/LP, dove il restatement-a-Lovász non si applica).

---

## Entry 3 — ARC PIVOT: Proof complexity / automatizzabilità (2026-06-07)

**Decisione umana:** chiuso l'arco lift/G★ (doppio RESTATEMENT su dualità cover-LP),
PIVOT a un programma fuori-arena = PROOF COMPLEXITY (dir.1 di Entry 0). Motivo: l'intero
arco μ_R/G★/lift collassava su dualità LP set-cover (Lovász); serve un'arena dove quel
restatement NON si applica. Contesto compattato prima di iniziare; questo è il punto di
ripresa pulito — il prossimo ciclo riparte DA QUI, non dalla conversazione.

**Asset nel repo per questa arena:** Module 5 (pnp_lab/proof_complexity/, resolution/
DPLL su PHP, misura size esponenziale Haken), Module 11 (proof_search + Lean reale),
formalization/ (Lean: Tableau, NaturalProofs, Cook-Levin). Il modello TM time-bounded +
tableau (Module 4) e CDCL/branch (test_cdcl, test_branch) sono riusabili.

**Sotto-domande candidate (l'Explorer ne sceglie/affina UNA con killer dichiarato;
preferire ciò che NON è un'altra dualità LP):**
1. *Feasible interpolation, misurata sul piccolo.* Da una refutazione resolution di una
   formula split A(x,z)∧B(y,z) estrai il circuito interpolante; misura ESATTAMENTE su
   istanze ≤6 var se la sua taglia traccia la monotone-circuit lower bound (Krajíček).
   C'è un divario MISURABILE non riducibile a width/size già in Module 5?
   Killer: la taglia dell'interpolante = funzione diretta di width/size → RESTATEMENT.
2. *Gap tree-resolution vs DAG-resolution, esatto.* Su formule UNSAT minuscole misura
   size(tree-res) / size(DAG-res) e cerca una regola predittiva su CHI forza il gap
   (riuso/lemma). Killer: il gap = il noto Prover–Delayer / pebbling già in letteratura.
3. *Automatizzabilità empirica.* La proof-search di Module 11 trova la ref-minima in
   poly(size) sulle famiglie tiny, o c'è un salto super-poly misurabile (eco di
   Atserias–Müller a taglia finita)? Killer: è solo la nota durezza di MCSP/TFNP
   ri-etichettata, oppure un artefatto di taglia finita non estrapolabile.

**Killer d'arco (meta):** se anche la prima sotto-domanda collassa su una dualità LP/
game nota (interpolazione = comunicazione, tree-res = Prover–Delayer = pebbling), allora
il pattern "tutto è una dualità nota" trascende l'arena cover/LP → conclusione forte
(meta-restatement) da dichiarare, e STOP.

**NEXT unstable direction:** Explorer sceglie tra 1–3 sopra (preferire #1 feasible
interpolation: è il punto dove proof complexity tocca circuit lower bounds, l'unico
"trasferimento cross-domain" che NON è già LP set-cover). Eseguire un ciclo completo.

---

## Entry 4 — Ciclo 3: feasible interpolation sul piccolo (2026-06-07)

**Direzione testata:** sotto-domanda #1 di Entry 3 — feasible interpolation. Ipotesi H3
(Explorer): la taglia dell'interpolante estratto da una refutazione resolution di una
formula split A(p,z)∧B(q,z) è funzione diretta della taglia/larghezza già in Module 5;
nessuna grandezza misurabile la decoupla. Killer-per-NEW-CONTENT: un divario tra
interpolante-costruito e interpolante-minimo non spiegato da una misura di comunicazione
nota (KW monotono).

**Costruito (Builder):** pnp_lab/feasible_interp/ (interp.py = refutazione DAG +
costruzione Krajíček/Pudlák [assioma-A→0, assioma-B→1, pivot-shared→MUX, pivot-priv→
OR/AND] + verifica SEMANTICA su tutti gli α + interpolante minimo via DT; families.py =
or_family/and_family) + tests/test_feasible_interp.py (44 test) + esempio. Riusa
proof_complexity.{formula,resolution}. Suite veloce, non committato.

**Numeri esatti misurati (or_family/and_family, n=1..5):** interpolante verificato OK
su tutti gli α; #MUX=n; min-DT-leaves=n+1; passi di saturazione 10,40,143,447,1422
(super-lineari) vs interpolante lineare.

**Verdetto Adversary (red-team indip., numeri riprodotti + controesempi in codice):**
- Claim "interpolante corretto" = teorema di Krajíček 1997/Pudlák 1997 verbatim → RESTATEMENT.
- Claim "#MUX = #variabili shared" → KILLED: controesempio `proj_family` (variabili
  shared inerti: #shared cresce 1→5, #MUX resta 1). Vale solo "#MUX = #pivot-shared
  risolti" = TAUTOLOGICO.
- Claim "decoupling dai passi di saturazione" → KILLED: artefatto di un saturatore
  stupido; il DAG effettivamente usato è lineare (4n+3). or_family ≡ and_family (duale
  di De Morgan) → un solo fenomeno.
- Claim "interpolante ~minimo" → INCONCLUSIVE/vuoto: min_interpolant_dt_size misura
  foglie di ALBERO DI DECISIONE, NON la monotone-circuit LB né la comunicazione KW
  monotona (Θ(log n) per OR_n, non n). Il contenuto Razborov–Pudlák (feasible interp.
  monotona = comunicazione KW) NON è mai calcolato.
- Buco serio: la regola privata a→OR/b→AND NON è esercitata — scambiandola
  (a→AND/b→OR) la semantica regge su n=1..4 (operandi privati sempre costanti/uguali).

**Evaluator:** robustness 3/10. Flag APERTI (tutti e 5): circolarità, confirmation-bias,
off-tiny-instance, unfalsifiable-here, overfitting. Verdetto: RESTATEMENT-OF-KNOWN
(Claim 2-3 KILLED, Claim 4 vuoto). Honesty boundary scritta. Il META-KILLER d'arco NON
scatta in codice (il banco non tocca la comunicazione) MA la riduzione interpolazione-
monotona ⟺ comunicazione KW è GIÀ nel dizionario μ_R/G(R) (docs/duality-gap-theory.md
§3-4). Nessun contenuto predittivo nuovo.

**Scritto/committato:** modulo + test + esempio creati, NON committati. Nessun Module
cristallizzato.

**PI — STOP E CHIEDI ALL'UMANO (decisione di scope).** Conteggio: Entry 1 RESTATEMENT,
Entry 2 RESTATEMENT (→ l'umano decise il PIVOT proof-complexity), Entry 3 RESTATEMENT =
3 di fila. PERÒ il ciclo 3 ha fallito di BANCO (il codice non ha mai toccato la
comunicazione/KW, il punto dove proof-complexity tocca i circuit LB in modo non-LP):
il pivot non è stato davvero messo alla prova. Esiste UNA direzione nuova precisa
(cycle 4 sotto). Ma è una build costosa e l'esito atteso (dal dizionario) è meta-
restatement → è una decisione di scope da portare all'umano, non da auto-eseguire.

**NEXT unstable direction (in attesa di decisione umana):**
(A) Cycle 4 mirato nell'arena: misurare la grandezza GIUSTA — la comunicazione del gioco
   Karchmer–Wigderson monotono su clique/coloring (Razborov), oppure un interpolante
   monotono su uno split che FORZA la regola privata (gate con operandi non costanti).
   Killer: se taglia-interpolante traccia esattamente la KW-comm → conferma del
   dizionario, META-KILLER scatta → chiudere il pivot e STOP. Se emerge un divario
   non riducibile a width/size → primo segnale di contenuto nuovo.
(B) Dichiarare chiuso ORA il pivot proof-complexity come meta-restatement (3 restatement
   di fila; "tutto è una dualità nota" trascende anche quest'arena).
(C) Pivot a dir.2 di Entry 0: meta-complessità concreta MCSP/MKtP su tavole ≤4 bit
   (mai tentata), fuori dall'arena dualità.

---

## Entry 5 — Ciclo 4: feasible interpolation MONOTONA, grandezza giusta (2026-06-09)

**Direzione testata:** Entry 4 opzione A (decisa dall'umano) — arena feasible
interpolation MONOTONA. Misurare la grandezza GIUSTA (comunicazione KW monotona, mai
calcolata nel ciclo 3) e FORZARE la regola privata (mai esercitata nel ciclo 3). È il
make-or-break del pivot proof-complexity: se collassa, scatta il META-KILLER d'arco.

**Ipotesi (Explorer):** su f = triangolo su K₄ (6 var = archi di K₄), tre interi
indipendenti — S = taglia interpolante monotono, P = partition number della matrice KW⁺
(4 minterm × 7 maxterm), C = Dcc (comunicazione deterministica del gioco KW⁺).
Killer/discriminante: S=P=2^C(±1) → RESTATEMENT; S−P>1 strutturale → segnale di
contenuto nuovo non riducibile a width/size.

**Costruito (Builder):** nuovo modulo `pnp_lab/kw_communication/kw.py` (minterms/maxterms
forza bruta, kw_plus_matrix, partition_number = exact-cover B&B esatto, dcc = ricorsione
memoizzata esatta, clique_f); `clique_triangle_K4()` in
`pnp_lab/feasible_interp/families.py`; `build_interpolant_swapped()` in interp.py (per il
test buco-2); `tests/test_kw_communication.py` (12 test, 2.66s con slow);
`examples/run_kw_communication.py`. Suite intera: 325 passed, 1 skipped in ~92s, non si
blocca.

**Numeri esatti misurati** (rigenerabili da `py examples/run_kw_communication.py`):
- S=19 (11 MUX + 8 bool_gates), P=10 (certificato ottimo), C=4 → 2^C=16, S−P=9.
- Refutazione = 93.823 passi del saturatore BFS (cap alzato a 200000).
  min_interpolant_dt_size=18.
- Buco-2 CHIUSO: lo swap a→AND/b→OR rompe verify_interpolant su 21/64 α (la regola
  privata è davvero forzata, a differenza del ciclo 3).
- Altre istanze: K₃ (P=3, C=2), MAJ-2/3 (P=5, C=3).

**Verdetto Adversary (verificato in codice):** discriminante S−P NON regge.
(1) ARTEFATTO: cambiando SOLO l'ordine di iterazione del saturatore (a parità di
f/split/93823 passi), S oscilla 19→32 (gate MUX 11→17, bool 7→17) — S non è canonico.
(2) CATEGORY-ERROR: S mescola 11 MUX NON-monotoni con P,C monotoni; bool_gates=8 < P=10
= solo "interpolante non ottimo" (noto). (3) RESTATEMENT+VACUO: P,C calcolati dalla SOLA
matrice KW⁺ = Razborov–Pudlák/Karchmer–Wigderson verbatim = partition/cover-LP del
dizionario μ_R/G(R); inoltre P ≤ 2^C è TEOREMA obbligato (log₂P ≤ Dcc) →
"non-coincidenza" vacua. (4) nessuna regola tra istanze oltre P≤2^C. (5) P=10, C=4
certificati ottimi (unici numeri solidi, ma noti). META-KILLER d'arco: SCATTA SI.

**Evaluator:** robustness 2/10 (ciclo 3 era 3/10; più basso perché il discriminante
esplicito è stato falsificato in modo COSTRUTTIVO). Flag APERTI:
artefatto-implementativo (fatale), vacuous-discriminant, category-error,
circolarità/restatement, off-tiny-instance. Flag CHIUSI: confirmation-bias (buona
onestà di processo), unfalsifiable-here (era falsificabile, falsificato). Verdetto:
RESTATEMENT-OF-KNOWN, discriminante KILLED. META-KILLER d'arco SI: il pivot
proof-complexity, reso onesto a misurare la grandezza giusta, collassa SOLO su
invarianti KW già dizionarizzati, legati dall'identità nota log₂P≤Dcc. Cosa di onesto
SOPRAVVIVE: (a) chiusura buco-2 (miglioramento di banco verificato); (b) P=10/C=4
misure canoniche esatte ma note.

**Scritto/committato:** modulo kw_communication + modifiche feasible_interp + test +
esempio CREATI, NON committati. Nessun Module cristallizzato ANCORA (decisione di scope
pendente sull'umano).

**Conteggio restatement:** Entry 1, 2, 4, 5 = QUATTRO restatement (Entry 3 era il pivot
deciso dall'umano). Il META-KILLER d'arco è ora scattato: "tutto è una dualità nota"
trascende anche l'arena proof-complexity.

**NEXT unstable direction (in attesa di decisione umana — il PI si FERMA e CHIEDE):**
Il pivot proof-complexity è da dichiarare CHIUSO come meta-restatement. Opzioni:
(B-cristallizza) cristallizzare SOLO il banco di misura (calcolatore KW⁺ esatto + test
forzatura regola privata) come Module-strumento etichettato "tiny-instance measurement,
non risultato", deprecando S come metrica incanonica; (C) pivot all'ultima arena mai
tentata = meta-complessità concreta MCSP/MKtP su tavole ≤4 bit (dir.2 di Entry 0), fuori
dall'arena dualità/cover-LP; (D) STOP globale del loop (4 restatement + meta-killer =
forte evidenza che il programma μ_R "tutto-è-dualità-nota" è robusto e la ricerca
esplorativa su questo repo ha raggiunto un punto fermo).

---

## Entry 6 — Ciclo 5: meta-complessità concreta su tavole ≤4 bit (2026-06-09)

**Direzione testata:** PIVOT deciso dall'umano = dir.2 di Entry 0 — meta-complessità
concreta su tavole di verità ≤4 bit, FUORI dall'arena dualità/cover-LP. Killer d'arena
dichiarato: "il fenomeno è KT-complexity ridefinita".

**Ipotesi (Explorer H5 + raffinamento PI):** un down-degree LOCALE stratifica funzioni
di pari MCSP-size (formula-size esatta, Module 6). Mossa-controllo = input-negation
(automorfismo del costo → down-degree atteso d≡0). Mossa genuina = d_flip(f) = #{flip di
1 bit dell'output : cost[f'] < cost[f]}. Discriminante: se d_flip è ricostruibile da
invarianti già noti (sensitivity, gf2_degree, cover-LP) → RESTATEMENT; se separa funzioni
di pari MCSP-size in modo NON ricostruibile → primo segnale di contenuto nuovo.

**Costruito (Builder):** `pnp_lab/meta_complexity/strata_graph.py` (negate_input,
flip_output, down_degree_negation, down_degree_flip, gf2_degree via Möbius, sensitivity,
block_sensitivity via packing backtracking, orbit_B = gruppo iperottaedrale, strata,
partition_refinement, analyze; riusa complexity_map / min_formula_sizes di Module 6) +
`tests/test_strata_graph.py` (9 test fast n=3 + 2 slow n=4) + `examples/run_strata_graph.py`.
Suite intera: 334 passed, 1 skipped in ~93s (rigenerabile da `py -m pytest`).

**Numeri esatti misurati** (rigenerabili da `py examples/run_strata_graph.py`):
- Killer-1 CONFERMATO: d_negation ≡ 0 (n=3: 256/256 funzioni; n=4: 65536/65536).
  L'input-negation è un automorfismo del costo → down-degree identicamente nullo.
- d_flip n=3: |{valori d_flip}| ≥ 2 ai cost 2,3,4,5; relazione coi killer varia per strato.
- n=4 esaustivo (~35 min, max_cost=15): negli strati centrali cost 4–11, d_flip è
  INCOMPARABILE con sensitivity / block_sensitivity / gf2_degree, e RAFFINA la partizione
  per orbita-B₄ (gruppo iperottaedrale).

**Verdetto Adversary (tutto verificato in codice):**
(1) RIDUZIONE ESATTA: d_flip(f) = #{k : cost[f XOR (1<<k)] < cost[f]} ricostruito esatto
    su 256/256 (n=3) e 65536/65536 (n=4) → d_flip è il GRADIENTE DISCRETO di MCSP-size sul
    cubo delle tavole di verità; nessun oracolo oltre `cost`, B_n-invarianza ereditata da
    cost. Non è un nuovo invariante: è la derivata di un oggetto-KT.
(2) RESIDUO INFORMATIVO ILLUSORIO: n=3 H(d_flip | cost,sens,bsens,deg,ones) = 0.000 bit
    (overfit della piccola istanza); n=4 residuo 1.19 bit MA = la MCSP-size dei vicini, non
    informazione nuova.
(3) ARTEFATTO IMPLEMENTATIVO: sostituendo cost→DT-depth, d_flip cambia su 154/256 e
    collassa 194/256 in un solo strato → d_flip NON è canonico (stesso difetto di S nel
    ciclo 4).
(4) OVERFITTING: la regola (cost,deg,ones)→d_flip appresa su n=3 predice 1/65 su n=4.
(5) misure-killer corrette (0 mismatch nelle riduzioni). META-KILLER d'arena
    "tutto è KT" SCATTA: SI.

**Evaluator:** robustness 4/10 (ciclo 3 = 3, ciclo 4 = 2; SALE perché il banco è onesto e
il segnale grezzo è reale — d_flip è davvero incomparabile coi classici e raffina B₄ — ma
il claim è DISSOLTO dalla riduzione esatta, non dalla misura). Flag APERTI:
circolarità/restatement, gradient-of-known (flag NUOVO), artefatto-implementativo,
overfitting, off-tiny-instance, vacuous-discriminant. Flag CHIUSI: confirmation-bias,
killer-1-banale (d_negation≡0 dimostrato), misure-classiche (corrette). Verdetto:
RESTATEMENT-OF-KNOWN (d_flip = gradiente di MCSP-size + non canonico + nessuna regola tra
istanze). META-KILLER d'arena SI: la derivata di un oggetto-KT è ancora KT.

**Scritto/committato:** modulo strata_graph + test + esempio CREATI, NON committati.
Nessun Module cristallizzato.

**META-CONCLUSIONE (cristallizzabile, falsificabile — formulata dall'Evaluator):** nel
regime n≤4, ogni "discriminante locale" finora costruito si riduce, tramite un'identità
ESATTA verificata in codice, a un invariante già nel dizionario μ_R (cover-LP /
proof-complexity / KT). Il pattern TRASCENDE TRE arene: dualità/cover-LP (μ_R/G★, Entry
1–2), proof-complexity (Module 16 + ciclo 4 KW, Entry 5), meta-complessità (ciclo 5 =
gradiente di KT, questa entry). FALSIFICATORE richiesto: un discriminante misurabile su
n≤4 che separi due funzioni di pari MCSP-size E pari cover-LP/G★ E NON ricostruibile da
`cost` né da μ_R tramite un'identità esatta. AVVERTENZA: è una constatazione sul METODO
del loop su istanze finite, NON un claim su P vs NP.

**Conteggio restatement:** Entry 1, 2, 4, 5, 6 = QUINTO restatement consecutivo. Il
META-KILLER è ora scattato in 2 arene OLTRE l'originale (proof-complexity + meta-complessità).

**NEXT unstable direction (il PI si FERMA e CHIEDE all'umano — STOP globale raccomandato):**
il loop esplorativo ha raggiunto un punto fermo. Opzioni per l'umano: (1) cristallizzare
SOLO la meta-conclusione (tiny-instance collapse + falsificatore esplicito) come Module di
chiusura, deprecando d_flip come metrica incanonica; (2) STOP globale del loop; (3)
tentare il falsificatore esplicito sopra (cercare ATTIVAMENTE un discriminante che separi
pari-MCSP ∧ pari-cover-LP NON ricostruibile da cost) come ULTIMO ciclo prima dello stop.

---

## Entry 7 — CHIUSURA: cristallizzazione della meta-conclusione (2026-06-09)

**Decisione umana:** opzione (1) di Entry 6 — cristallizzare SOLO la meta-conclusione
(tiny-instance collapse + falsificatore esplicito) come Module di chiusura, deprecando
d_flip come metrica incanonica, e committare il lavoro come risultato negativo onesto.
Poi STOP globale. NON è un nuovo ciclo di ricerca: è la chiusura riproducibile.

**Cristallizzato = Module 19 "Tiny-Instance Collapse":**
- `pnp_lab/meta_complexity/collapse.py` — i tre witness ESATTI + il falsificatore:
  (killer-1) `negation_is_cost_automorphism` → 0 nonzero; (W1) `dflip_is_cost_gradient`
  → 0 mismatch (d_flip ∈ σ(cost), gradiente discreto di MCSP-size); (W2)
  `dflip_canonicity_mismatch` → cambia oracolo formula-size→DT-depth (secondo oracolo
  esatto `dt_depth` via cofattori memoizzati); `falsifier_status` → NON trovato nella
  toolbox. `collapse_summary` aggrega tutto.
- `tests/test_collapse.py` (8 test fast n=3 + 1 slow esaustivo n=4); `examples/run_collapse.py`.
- `docs/tiny-instance-collapse.md` (English-first, honesty boundary: è sul METODO su
  istanze finite, NON P vs NP; tabella delle 3 arene; falsificatore esplicito).
- Deprecazione in testa a `strata_graph.py`: d_flip etichettato "banco di misura, NON
  discriminante strutturale".
- README aggiornata: riga Module 19, quick-start, docs list, conteggio test (342 fast).

**Numeri esatti riprodotti** (da `py examples/run_collapse.py`, e in test):
- n=3 (256 funzioni): killer-1 = 0; W1 mismatch = 0; W2 = 154/256 (60.2%); falsifier = False.
- n=4 (65536 funzioni, slow): killer-1 = 0; W1 mismatch = 0; W2 non banale; falsifier = False.
- Suite intera: `py -m pytest` = 342 passed, 1 skipped, 15 deselected in ~66s.

**Stato finale del loop:** 5 RESTATEMENT-OF-KNOWN consecutivi (Entry 1,2,4,5,6),
META-KILLER scattato in 3 arene (cover-LP, proof-complexity, meta-complessità). La
meta-conclusione (memory/tiny-instance-collapse.md) è ora cristallizzata e riproducibile
in codice per l'arena meta-complessità; le altre due arene sono citate (Module 16/18 +
Entry 1–2,4–5), non ri-derivate. d_flip DEPRECATO come metrica.

**STOP GLOBALE del loop.** L'esplorazione su questo repo ha raggiunto un punto fermo.
Per ripartire in futuro servirebbe il FALSIFICATORE esplicito (un discriminante su n≤4
che separi pari-MCSP ∧ pari-cover-LP NON ricostruibile da cost) — non trovato nella
toolbox attuale. Niente più cicli automatici senza una direzione fuori-dizionario nuova.

**NEXT unstable direction:** NESSUNA (loop chiuso). Eventuale ripresa solo su una
direzione genuinamente fuori dal dizionario μ_R, con falsificatore dichiarato in anticipo.
