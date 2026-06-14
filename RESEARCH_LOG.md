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

## Entry 12 — PRIMO ciclo del pivot di regime: larghezza di consistenza locale CSP, |D|=3 (2026-06-14)

**Contesto-pivot:** dopo Entry 11 (RESTATEMENT #9, cristallizzata come Module 20 "Inv-Pol
Collapse"), l'umano ha deciso (1) cristallizzare il [FATTO] poi (2) PIVOTARE fuori
dall'esatto-finito verso il regime Bulatov–Zhuk-hard, dove la dicotomia è muta sul VALORE
(non sul verdetto). Questo è il PRIMO ciclo del pivot. Cambio dichiarato di arena: dai
politomorfismi (Inv-Pol) alla LARGHEZZA DI CONSISTENZA locale.

**Ipotesi H (Explorer):** w*(Γ) = min{k : ∀Φ∈T(Γ) (≤6 var su D=3),
(k,k+1)-consistenza(Φ) ⟺ is_sat(Φ)} — la larghezza di consistenza locale misurata DENTRO
la classe bounded-width. H: w* separa Γ marker-equivalenti (stesso g, stesso profilo
simmetrico, tutti WNU) e non è ricostruibile da |Pol-slice| né dal verdetto. Regime
dichiarato (a): esatto-per-istanza su campione. Killer principale dichiarato in anticipo:
K-bw23 (Barto–Kozik: bounded width = (2,3) → w*≤2).

**Costruito (Builder):** `pnp_lab/csp/local_consistency3.py` (CSP, is_sat forza-bruta esatta
≤3^6=729, kk1_consistent = (k,k+1)-minimalità di Barto–Kozik a punto fisso, T batteria
congelata di istanze-test incl. gadget ciclici UNSAT-ma-localmente-consistenti, w_star,
analyze_consistency + 4 predicati-killer) + `tests/test_local_consistency3.py` (9 test, incl.
gap esibito: 4-ciclo di C3={(0,1),(1,2),(2,0)} UNSAT ma 1-consistente, scoperto solo da k=2)
+ `examples/run_local_consistency3.py`. Suite verde.

**Numeri esatti misurati (Builder, 7 Γ; rigenerabili da `py examples/run_local_consistency3.py`):**
between w*=1, cycle3 w*=2, eq012 w*=1, impl01 w*=1, leq w*=1, lt w*=1, min_graph w*=1.
K-bw23=True (w*≤2 ovunque), w1_tracks_majority=False (min_graph semilattice w*=1 senza
maggioranza), K-Pol-slice=True, h_separates=False.

**Verdetto Adversary: RESTATEMENT (decimo collasso); esito "campione magro" ESCLUSO
costruttivamente.** Ha ALLARGATO il campione 67× → tutte le 472 relazioni binarie WNU su D=3
(universo 2^9 completo filtrato WNU): distribuzione w*={1:455, 2:17}, zero None, zero w*≥3.
h_separates=False su tutte le 17 classi (g,σ) → FATTO non artefatto. **Matrice di confusione
w* ↔ marker width-1 PERFETTA: (1,width-1)=455, (2,non-width-1)=17, off-diagonale=0.**
Riduzione esibita: w*=1 ⟺ width-1 (Feder–Vardi 1998 / Dalmau–Pearson 1999:
arc-consistency/Datalog ⟺ politomorfismi totalmente simmetrici di OGNI arietà); w*=2 ⟺
bounded-width-non-width-1 (Barto–Kozik JACM 2014). w* è il GRADINO width-1 vs width-2 noto, un
verdetto binario {1,2} rietichettato come intero — NON la grandezza quantitativa ricca
promessa. Vettore batteria: per width-1 nessuna batteria alza w* (arc-consistency
sound&complete) → w* non è artefatto-batteria. w*=2 = fenomeno odd-cycle di 2-colorazione
(triangolo di ≠: UNSAT, 1-consistente, catturato da k=2).

**Evaluator: RESTATEMENT-OF-KNOWN, robustness 8.5/10.** Ha RIPRODOTTO indipendentemente la
matrice di confusione perfetta su 472 punti. Imprecisione dell'Adversary CORRETTA: il claim
"confermato ad arietà 4" è impreciso — 2 dei 17 (C3 e il suo inverso) HANNO un TSI di arietà 4
(profilo non-monotono True/False/True) ma falliscono all'arietà 3, quindi correttamente
non-width-1; la riduzione regge SOLO col profilo simmetrico pieno "TSI di OGNI arietà", non con
un marker a singola arietà (con la sola arietà-3 la confusione si sporca a (2,True)=15).
FLAG-CHIAVE: **il pivot di regime è rimasto ESATTO/ENUMERABILE** (472 binarie = 2^9, simmetriche
fino arietà 4 = ≤531441, tutto forza-bruta) → il regime DECISIVO Bulatov–Zhuk-hard (WNU alta
arietà, |D|≥4, dove l'enumerazione è genuinamente impossibile e servono BOUND CERTIFICATI) NON
è stato testato. Il pivot ha cambiato ARENA, non REGIME.

**Honesty boundary (inglese, per il doc se si cristallizza):** w*(Γ) is exact only over the
ENUMERABLE regime on D={0,1,2}: all 472 binary WNU relations (complete 2^9 universe) and
symmetric-idempotent ops up to arity 4 (brute force). w*∈{1,2} with a perfect confusion matrix
against the width-1 marker: w*=1 ⟺ full totally-symmetric-idempotent profile (Dalmau–Pearson
width-1), w*=2 ⟺ bounded-width-not-width-1 (Barto–Kozik, bounded width=(2,3)). w* carries NO
information beyond the known width-1/width-2 step — a binary verdict relabeled as an integer.
h_separates=False on all 17 frontier classes (a fact, not small-sample). The regime pivot did
NOT reach the decisive arena: "exact-per-instance on a sample" stayed entirely inside the
enumerable, with no certified bounds; the Bulatov–Zhuk-hard regime (high-arity WNU, |D|≥4)
remains untested. The pivot changed the arena, not the regime. NO claim about P vs NP. One
imprecision corrected: single fixed-arity markers do NOT reconstruct w* (C3 has an arity-4
TSI); only the full "TSI at every arity" characterization does.

**STOP-and-ask:** SCATTA. DECIMO collasso; il pivot ha riprodotto il collasso al primo ciclo
perché è rimasto nell'enumerabile. Diagnosi: su tiny+enumerabile la dicotomia è muta sul valore
ma assorbe ogni nuova quantità (tutto si riduce al profilo polimorfico). Scratch da rimuovere
prima di un eventuale commit: NESSUNO nella working tree principale (solo i file di modulo/test/
esempio; l'unico `_*.out` residuo, `.claude/worktrees/crazy-jones-cc416e/_cycle1E_n4.out`, sta
nel worktree stale, fuori dal tree principale). Decisione di commit PENDENTE sull'umano.

**NEXT unstable direction (STOP-and-ask — decisione umana, raccomandazioni dell'Evaluator):**
(1) cristallizzare il meta-risultato "su istanze tiny-enumerabili ogni discriminante locale
collassa sul profilo polimorfico noto" e CHIUDERE il ramo CSP; (2) il VERO pivot — abbandonare
l'enumerazione, |D|≥4 con WNU alta arietà via bound CERTIFICATI (rischio: serve dimostrazione,
non esperimento); (3) cambiare arena (lasciare CSP/algebra, satura di teoremi-attrattore, p.es.
proof-complexity su famiglie esplicite). Raccomandazione netta Evaluator: NON iterare un
undicesimo ciclo nell'enumerabile (RESTATEMENT #11 quasi certo).

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

---

## Entry 8 — Ciclo 6: caccia al falsificatore (la ripresa dichiarata) (2026-06-13)

**Direzione testata:** l'UNICA ripresa ammessa da Entry 7 — cercare ATTIVAMENTE il
FALSIFICATORE esplicito (un discriminante su n≤4 che separi due funzioni di pari
MCSP-size ∧ pari cover-LP NON ricostruibile da `cost`/μ_R). Finora `falsifier_status`
(collapse.py) ASSUMEVA, senza cercare, che il resto della toolbox fosse dizionarizzato.

**Ipotesi/setup (Explorer+Builder, reso TEST FINITO):** μ_R = insieme GENERATORE di
invarianti, tutti B_n±-invarianti (B_n± = perm × neg-input × {id, neg-output} = gruppo
degli automorfismi del costo). P_Σ = partizione per vettore-dizionario congiunto;
P_orbit± = partizione per orbita B_n±. Poiché ogni generatore è B_n±-invariante,
P_orbit± RAFFINA SEMPRE P_Σ (|P_Σ| ≤ |P_orbit±|). Allora: FALSIFICATORE ESISTE ⟺ una
classe di P_Σ si spezza in ≥2 orbite (due funzioni identiche su TUTTO μ_R ma in orbite
diverse). Killer dichiarato: P_Σ == P_orbit± → nessun falsificatore, collasso indurito.

**Costruito (Builder):** `pnp_lab/meta_complexity/falsifier_hunt.py` (cost_orbit/orbit_canon
B_n±, comm_matrix + multiset G★/cover/frac-cover ripiegati su neg-output, support_folded,
generatori "forti" cover_number/frac_cover/average_sensitivity/real_degree/
fourier_fingerprint, dictionary_vector, hunt, named_separators) + `tests/test_falsifier_hunt.py`
+ `examples/run_falsifier_hunt.py`. + `docs/falsifier-hunt.md`.

**Numeri esatti misurati (rigenerabili):**
- n=3 (256 funz): NAIVE(B_n) 8 split → B_n± 1 split (coppia 24,30) → B_n±+support
  0 split, P_Σ==P_orbit±. ENTRAMBE le chiusure (neg-output, support) necessarie.
- n=4 (65536 funz, esaustivo, ~52 min): |P_orbit±|=222. Dizionario STRONG a 11
  generatori → |P_Σ|=221, **UN SOLO split**: coppia (2025, 5742), cost 11,
  `named_separators=[]` (identica su tutti gli 11 generatori), orbite B_n± disgiunte
  (96 ciascuna), g≠¬f. → CANDIDATO FALSIFICATORE.

**Verdetto Adversary (verificato in codice, cache della tabella costi in pickle):** il
candidato è UCCISO, dentro σ(cost). Aggiunto il 12° generatore `cofactor_cost_profile`
(multiset su i di sorted(cost(f|xi=0),cost(f|xi=1)) con cost = formula-size esatta a
(n-1)-var = la RICORSIONE stessa di formula-size, dentro σ(cost)): |P_Σ|=222,
#splits=0, **P_Σ==P_orbit±==222 ESATTAMENTE** → collasso COMPLETO anche a n=4. cofactor
f={(2,7),(2,7),(5,5),(5,5)} ≠ g={(4,5),(4,5),(4,7),(4,7)}. Lo stesso split è ucciso,
indipendentemente, dal sensitivity-profile per-punto (raffinamento di sensitivity/
average_sensitivity già nel dizionario). Il dizionario codificato falliva SOLO perché
usava le versioni SCALARI COARSE (cost scalare, sens max/somma) dei propri invarianti.

**Bug intercettato dalla guardia (onestà di processo):** un cofactor "ingenuo" che legge
i costi dei cofattori (n-1)-var sulla tabella a n var misura il costo dell'embedding
`g∧¬xi` (NON B_n±-invariante) → produsse |P_Σ|=243>222, #splits=0 VACUO. La guardia di
legittimità `|P_Σ| ≤ |P_orbit±|` lo ha smascherato; la versione corretta usa la tabella
a (n-1) var. Test di regressione: `test_naive_cofactor_would_over_refine`.

**Evaluator:** RESTATEMENT-OF-KNOWN / COLLAPSE-HARDENED. Nessun falsificatore genuino
fuori-dizionario a n≤4. La meta-conclusione "tiny-instance collapse" (Module 19) esce
RAFFORZATA: persino l'unica apparente via di fuga a n=4 muore per un raffinamento di
`cost`. SESTO esito collapse-hardened consecutivo. Honesty boundary: metodo su istanze
FINITE, NON un claim su P vs NP.

**Scritto/committato:** modulo falsifier_hunt + 12° generatore cofactor_cost_profile +
test (22 fast verdi + 1 slow n=4 collasso completo) + esempio + docs/falsifier-hunt.md +
questa entry + memoria aggiornata → COMMITTATI come risultato negativo onesto (decisione
umana: cristallizzare e committare). Scratch `_cycle6_*`/`_probe_*`/`_cost_n4.pkl` rimossi.

**NEXT unstable direction:** NESSUNA. Il falsificatore dichiarato da Entry 7 è stato
cercato esaustivamente a n≤4 e NON esiste (l'unico candidato collassa in σ(cost)). Il
loop resta CHIUSO. Ripresa solo su una direzione genuinamente fuori dal dizionario μ_R,
con falsificatore dichiarato in anticipo, e su n≥5 (oltre la portata esatta attuale).

---

## Entry 9 — Restart program, direzione A: geometria dello spazio delle soluzioni (2026-06-13)

**Decisione umana:** ripartire col restart program out-of-dictionary (E→A→B,
ricostruito in `prompts/restart-out-of-dictionary.md` dopo che i file 2026-06-12 erano
andati persi). Diagnosi del programma: i discriminanti collassano perché tutti (1)
scalari, (2) minimi di copertura/gradienti, (3) unari; una direzione è ammessa solo se ne
rompe una. Scelta la **direzione A** (geometria dell'INSIEME delle formule ottime): rompe
(1) [insieme/grafo] e (3) [relazionale].

**Ipotesi H-A (Explorer):** la geometria dello spazio delle soluzioni separa funzioni di
pari (cost, |orbita B_n±|, N_min). Oggetto esatto e canonico: il DAG degli SPLIT OTTIMI
`OptSplit(f)={(op,a,b):op(a,b)=f, cost[a]+cost[b]+1=cost[f]}`, ricostruito dal cost table.
Invarianti su FUNZIONI (non stringhe) → già encoding-indipendenti. Killer dichiarati: K1
ricostruibile dagli scalari; K2 verdetto instabile ordinato↔non-ordinato; K3 = Aut(f)/orbita.

**Costruito (Builder):** `pnp_lab/meta_complexity/solution_geometry.py` (optimal_splits +
builder DP per n=4; reach/DAG; n_min ordinato e AC-quozientato; geometria = dag_size +
branching + frontier; analyze + check adversariale `sigma_cost_dominated`) +
`tests/test_solution_geometry.py` (8 fast + 1 slow n=4) + `examples/run_solution_geometry.py`.

**Numeri esatti misurati:**
- n=3 (256 funz): SOTTO-SOGLIA — chiave-scalare già 14 classi == |P_orbit±|=14, nessuno
  spazio per la geometria (test vacuo). K2 canonico.
- n=4 (65536 funz, ~28 min): geometria raffina 209 → **222 == |P_orbit±|**, separa **12+**
  coppie di pari (cost,|orbita|,N_min), K2-canonica → verdetto INGENUO "candidate new content".

**Verdetto Adversary (verificato in codice):** RESTATEMENT. (1) Il K1 ingenuo era troppo
debole: il criterio di Entry 7 è "NON ricostruibile da cost". La geometria è costruita
INTERAMENTE dal cost table → σ(cost) per costruzione. (2) Essendo B_n±-invariante, ogni
coppia separata sta in orbite diverse; il dizionario del Ciclo 6 è orbit-completo a n=4
(|P_Σ|=222) → separa GIÀ tutte quelle coppie. Verifica: il solo `cofactor_cost_profile`
(∈ σ(cost)) separa tutte e 12 le coppie (cover#/fracLP 10/12, fourier 12/12). Bug
corretto nel modulo (`sigma_cost_dominated`). K2 NON scatta (canonico), K3 assorbito in K1.

**Evaluator:** RESTATEMENT-OF-KNOWN, robustness alta come negativo (≈7/10): l'adversary ha
trovato un bug definitorio reale (weak-K1 → false signal) e l'ha ucciso con garanzia
logica + verifica per-coppia; l'invariante è K2-canonico (a differenza di S/d_flip). 7°
collasso consecutivo. LEZIONE DI METODO: la direzione A era STRUTTURALMENTE incapace di
produrre il falsificatore — ogni suo invariante è a valle della formula-size (σ(cost));
rompe scalare+unario ma NON "ricostruibile-da-cost", l'asse richiesto. Per uscire da
σ(cost) serve una struttura NON derivata dal costo → direzione B.

**Scritto/committato:** modulo + test + esempio + `prompts/restart-out-of-dictionary.md`
(programma ricostruito) + questa entry + memoria → COMMITTATI come negativo onesto
(decisione umana). Scratch `_run_geometry_n4.py`/`_geometry_n4.out` rimossi.

**NEXT unstable direction:** PIVOT a **direzione B (politomorfismi / cloni-minion,
Bulatov–Zhuk)** — l'unica del programma che rompe σ(cost) (lascia il mondo formula-size/
copertura per l'algebra delle CSP). Parent-killer dichiarato: BLP ⟺ politomorfismi
simmetrici. Se anche B collassa su un teorema noto → forte evidenza meta che "tutto è una
dualità/algebra nota" e STOP.

---

## Entry 10 — Restart program, direzione B: politomorfismi (fuori da σ(cost)) (2026-06-13)

**Direzione testata:** B del restart program — i POLITOMORFISMI di una relazione (la sua
chiusura algebrica), oggetto NON derivato dal costo → unica direzione che lascia σ(cost),
nell'arena CSP/Bulatov–Zhuk. Parent-killer dichiarato: BLP ⟺ politomorfismi simmetrici di
ogni arità (Kun et al./Barto–Kozik).

**Ipotesi H-B (Explorer):** il profilo simmetrico di Γ (per quali arità esiste un
politomorfismo simmetrico idempotente) porta informazione OLTRE i marker noti.

**Costruito (Builder):** `pnp_lab/csp/` (nuovo package) + `pnp_lab/csp/polymorphism.py`
(preserves/op_value, symmetric_ops, has_symmetric_polymorphism, symmetric_profile,
marker noti AND2/OR2/MAJ3/MINORITY3, schaefer_tractable, blp_solvable, is_degenerate,
analyze su tutte le relazioni booleane di arità data) + `tests/test_polymorphism.py` (7 test).

**Numeri esatti misurati (dominio booleano D={0,1}):**
- arità 2 (3 relazioni non degeneri) e arità 3 (63 non degeneri): nel setting IDEMPOTENTE
  il profilo simmetrico (avere simmetrici per OGNI arità fino a 6-7) coincide ESATTAMENTE
  con la BLP-risolvibilità → **parent-killer REGGE, 0 mismatch**.
- ≠={(0,1),(1,0)}: ha simmetrici solo di arità DISPARI (parità) → non BLP (coerente).

**Verdetto Adversary (3 errori miei intercettati, tutti = killer dichiarati):**
(1) marker SBAGLIATO Schaefer (=P) vs BLP: divergeva sull'affine = noto gap BLP⊊P, non
contenuto. (2) marker ancora sbagliato: MAJ (bounded-width, 2-SAT) ≠ BLP (semilattice);
≠ è MAJ-chiusa ma non BLP. Corretto blp_solvable = 0/1-valid o AND/OR (semilattice). (3)
K-deg: le 0/1-valid sono BLP-banali via la costante NON-idempotente → mismatch artefatto,
escluse col setting idempotente. Dopo le correzioni: coincidenza esatta → RESTATEMENT.

**Evaluator:** RESTATEMENT-OF-KNOWN (parent-killer confermato). **OTTAVO collasso.**
SIGNIFICATO: il pattern "tutto è una dualità/dicotomia nota" trascende anche σ(cost) — n
all'arena algebrica CSP il discriminante si riduce al teorema BLP⟺simmetrici. CAVEAT
(off-threshold): il dominio BOOLEANO è completamente classificato (Post/Schaefer), lì il
parent-killer è un teorema → confermarlo è quasi tautologico. Il test DECISIVO della
direzione B (dove Bulatov–Zhuk è profondo) è su dominio |D|≥3, non ancora fatto.

**Scritto/committato:** package csp + modulo + test + questa entry + memoria → COMMITTATI
come negativo onesto. Nessuno scratch.

**NEXT unstable direction:** dominio |D|=3 (il vero banco di Bulatov–Zhuk): un Γ ternario
dove il profilo dei politomorfismi (WNU/Taylor/simmetrici) dia un discriminante NON
riducibile alla dicotomia nota. Se anche lì collassa → la meta-conclusione "tutto-è-noto"
trascende σ(cost) ed è robusta su 4 arene → STOP globale con forte evidenza.

---

## Entry 11 — Restart program, direzione B ciclo 2: politomorfismi ternari, |D|=3 (2026-06-14)

**Direzione testata:** dominio |D|=3 (il vero banco di Bulatov–Zhuk), continuazione della
direzione B = il NEXT dichiarato da Entry 10. L'arena algebrica CSP fuori da σ(cost), ora
nel regime genuinamente non-classico (dove la dicotomia booleana Post/Schaefer non si applica).

**Ipotesi H-B2 (Explorer):** g(Γ) = #WNU binari idempotenti commutativi (27 candidati su
D={0,1,2}) che preservano Γ, quozientato per gli automorfismi unari di Γ. H: g separa coppie
marker-identiche e NON è funzione del profilo simmetrico né di |Aut|. Killer dichiarati in
anticipo: K-marker, K-σ, K-aut, K-feasibility.

**Costruito (Builder):** `pnp_lab/csp/polymorphism3.py` (op_value3 base-3, preserves3,
commutative_idempotent_binary_ops=27, unary_automorphisms, count_wnu_witnesses, g col
quoziente per orbite Aut, has_wnu k=2 esatto/k=3 limitato, symmetric_idempotent_ops +
symmetric_profile3 esatto fino k=4, CATALOG di 8 relazioni, analyze3 coi 3 killer) +
`tests/test_polymorphism3.py` (10 test default + 1 slow) + `examples/run_polymorphism3.py`.
Suite intera verde (`py -m pytest -q`), nessuna regressione.

**Numeri esatti misurati (tabella g, da `py examples/run_polymorphism3.py`):**
alldiff3 g=0 σ=() |Aut|=6; between g=8 σ=(2,3) |Aut|=1; cycle3 g=3 σ=(2,) |Aut|=3;
leq g=8 σ=(2,3) |Aut|=1; lt g=9 σ=(2,3) |Aut|=1; min_graph g=1 σ=(2,3) |Aut|=1; nae3 g=0;
neq g=0. Testimoni H: (between,lt) e (leq,lt) con firma-marker identica
(wnu2,wnu3,σ,|Aut|)=(T,T,(2,3),1) ma g∈{8,8,9}. In prima battuta NESSUNO dei 3 killer
scatta (verdetto numerico del Builder).

**Verdetto Adversary: RESTATEMENT (riduzione esibita), NONO collasso.** 5 vettori tutti
misurati in codice:
1. Marker grossolano corretto: enumerando le 2187 WNU ternarie idempotenti reali, wnu3=True
   è corretto su between/leq/lt (la sotto-stima majority/median NON ha falsato la firma); ma
   la firma "identica" è separata da marker NOTI banali — riflessività (leq g=8 / lt g=9) e
   arietà (between/leq).
2. Artefatto bordo riflessivo: aggiungendo elementi diagonali (rumore pp-banale) a lt, g
   salta 9→10→12→6→8 non-monotono → g dipende dalla diagonale.
3. Quoziente Aut VACUO: su tutte le 8 righe g==count_wnu_witnesses; su tutte le testimoni
   |Aut|=1; persino nell'unico caso |Aut|>1 con testimoni (cycle3, C₃) ogni orbita ha size 1
   → il quoziente non riduce mai sul catalogo → g qui ≡ scalare-conteggio (viola
   l'ammissibilità della regola di restart (1)).
4. Non encoding-invariante: between/leq/lt = 3 codifiche dello stesso ordine lineare → g le
   separa ma non è invariante per ricodifica = killer K2 di Entry 9.
5. RIDUZIONE ESIBITA: la colonna indipendente |{f binaria comm idem ∈ Pol(R)}| riproduce g
   esattamente su 8/8 righe → g(Γ) = |Pol₂^{comm,idem}(Γ)|, cardinalità di una fetta del
   clone (Inv-Pol). Zero contenuto predittivo nuovo.

**Evaluator: RESTATEMENT-OF-KNOWN, robustness 8.5/10.** Flag APERTI: off-tiny-instance
(catalogo 8 relazioni, |D|=3, WNU binari; il regime decisivo Bulatov–Zhuk = WNU alta arietà
/ |D| grande resta fuori portata esatta — le 3^27 operazioni ternarie non sono mai
enumerate); circolarità residua (g vive dentro il linguaggio Inv-Pol che doveva
trascendere); overfitting catalogo a mano (quoziente vacuo "qui", non teorema generale —
l'Adversary ha killato g-come-misurato, non g-in-generale); confirmation-bias mitigato. Flag
CHIUSO: has_wnu3 sotto-stima (verificato con enum 2187).

**Honesty boundary (inglese, per il doc se si cristallizza):** This cycle establishes a
negative, exact result on a tiny finite arena and makes NO claim about P vs NP. g(Γ) reduces
exactly to |Pol₂^{comm,idem}(Γ)| on the 8-relation catalog over D={0,1,2}; the intended
Aut-quotient is structurally vacuous (verified including cycle3, Aut≅C₃, all orbits size 1).
|D|=3 is the genuinely non-classical Bulatov–Zhuk regime, but the decisive content lives in
high-arity WNU operations and larger domains, out of exact reach here (the 3^27 ternary
operations are never enumerated). A reusable exact finite-instance diagnostic for
Inv–Pol-dictionary collapse — not a separation result.

**STOP-and-ask:** SCATTA. NONO collasso; secondo RESTATEMENT consecutivo senza nuova
direzione plausibile (Entry 9 dir-A, Entry 10 dir-B booleano, ora Entry 11 dir-B ternario).
Meta-conclusione "tutto-è-noto su istanze tiny/finite" corroborata trasversalmente: 4 arene,
9 collassi. Scratch da rimuovere prima del commit: NESSUNO (la working tree ha solo i file di
modulo/test/esempio; nessun `_*.py`/`_*.out`/probe presente).

**NEXT unstable direction (STOP-and-ask — decisione umana):** (1) cristallizzare in un Module
g(Γ)=|Pol₂^{comm,idem}| come diagnostico esatto di collasso Inv-Pol su istanze finite
(deprecando il quoziente Aut come vacuo); (2) cambiare regime FUORI-esatto = WNU alta arietà
/ |D| grande (le 3^27 ternarie non enumerabili a mano → serve struttura simbolica, non
forza-bruta), unica via per toccare il cuore di Bulatov–Zhuk; (3) STOP globale (9 collassi su
4 arene = punto fermo robusto: il metodo del loop su istanze finite collassa sempre su un
oggetto del dizionario). NESSUN auto-ciclo senza una direzione genuinamente fuori-dizionario
con falsificatore dichiarato in anticipo.

---

## Entry 13 — Magnification Frontier ciclo 1: la barriera di località esatta su MCSP[s] — FALSIFICAZIONE della leva (2026-06-14)

**Contesto-programma:** dopo la chiusura del ramo CSP (Collapse Theorem capstone, bb0e052),
l'umano ha aperto il NUOVO programma "Magnification Frontier" (ea5f391): far GIRARE esattamente
al meta-livello la hardness magnification + barriera di località su MCSP[s] (truth-table di
funzioni n-bit come N=2^n coordinate), faithful-not-new-content, misurando la LEVA attraverso i
livelli n=2→3→4 invece di un muro statico (il "terzo taglio della torta"). Questo è il
completamento del ciclo 1, il cui Builder era in pausa per limite di sessione.

**Oggetto (Builder, `pnp_lab/meta_complexity/locality.py`):** meta-funzione MCSP[s]:{0,1}^N→{0,1},
N=2^n, HARD = (formula minima esatta di Module 6 > s). Misure esatte: `relevant_coordinates`/`loc`
(junta), `best_k_local` A(k), `certified_k_local` (istanze dure che un argomento k-locale certifica
con CERTEZZA = fibra pura-dura), tabella `obstruction`, e la LEVA `leverage` su più livelli con la
policy banda-dura s=maxcost-1. + `tests/test_locality.py` + `examples/run_locality.py`.

**Ipotesi H (la staircase):** per la funzione PIÙ DURA serve leggere l'INTERO truth-table a ogni
livello (k*=N, rho=1), e k* RADDOPPIA 4→8→16. Killer-fidelity dichiarato: loc=N (junta genuino,
non degenere). Predizione esplicita codificata nel test slow: cert(N−1)=0 ⇒ k*=16, rho=1 a n=4.

**Numeri esatti misurati (build n=4 completo: complete=True, max_cost=15, 65536 funzioni; cachato
in `.cache/ct4.pkl`, ~500–900s):**

    n   N    H     k*   rho      coda cert(N−j)/H (j=0..3)
    2   4    2      4   1.000    1.00, 0,    0,    0
    3   8    2      8   1.000    1.00, 0,    0,    0
    4  16  114     14   0.875    1.00, 0.21, 0.07, 0     (cert: 114, 24, 8, 0)

loc=16/16 a n=4 → killer-fidelity SUPERATO (junta genuino, muro reale). MA cert(15)=24≠0 e
cert(14)=8≠0 ⇒ per monotonia k*=14<16, rho=0.875<1.

**Verdetto: IPOTESI DELLA LEVA FALSIFICATA esattamente a n=4** (terzo punto-dato). La staircase
"rho=1 a ogni livello, k* raddoppia 4→8→16" è FALSA. **Diagnosi esatta (il taglio orizzontale):**
il rho=1 a n≤3 era l'ARTEFATTO della banda-dura degenere H=2 (solo la parità e la sua negazione
sono massimamente dure; con 2 sole istanze, massimamente sparse, nessuna fibra di N−1 bit è
pura-dura → cert(N−1)=0 → rho=1 banale). Appena la popolazione dura è reale (H=114 a n=4)
compaiono fibre pura-dura sotto il junta pieno e rho<1. La leva NON misura un operatore di
magnification ma la TAGLIA+dispersione della banda più dura: H=2,2,114, NON monotona. Il
MECCANISMO di località (cert(k) basso finché k<N, junta genuino) regge; cade la STORIA "staircase
rho=1". È l'undicesima volta che il segnale tiny si riduce a un oggetto noto/banale — qui visto
ATTRAVERSO i livelli (la pendenza), non a un livello solo.

**Correzioni applicate (faithful):** `k_star` riscritto a DISCESA dall'alto (corretto + efficiente:
nel regime banda-dura k* è vicino a N, si toccano solo C(16,15),C(16,14),…, niente C(16,8)
catastrofico); blocco-leva, docstring di `leverage()` e `magnification_threshold_note()` aggiornati
con la falsificazione; esempio riscritto coi numeri reali; test `test_leverage_staircase_FALSIFIED_at_n4`
asserisce k*=[4,8,14], rho=[1,1,0.875], H=[2,2,114] e la coda [114,24,8,0] (era k*=[4,8,16],rho=1).
Suite verde (7 test veloci + 1 slow). Cache `.cache/ct4.pkl` evita il rebuild da 500–900s.

**Honesty boundary (inglese, per il doc se si cristallizza):** This cycle makes the locality
obstruction of hardness magnification EXACT on the meta-function MCSP[s] and makes NO claim about
P vs NP. The locality MECHANISM holds exactly (certified(k) stays low until the full junta;
MCSP[s] is a genuine N-junta, loc=N). But the "leverage staircase" hypothesis — rho=k*/N=1 at
every level, k* doubling 4→8→16 — is EXACTLY FALSIFIED at n=4: k*=14, rho=0.875. The rho=1 at
n≤3 is an artifact of the degenerate hardest band H=2 (only parity and its negation are maximally
hard; with two maximally-spread instances no (N−1)-subset has a pure-hard fibre). Once H is a real
population (H=114 at n=4) pure-hard fibres appear below the full junta. The leverage measure
tracks the size/spread of the hardest band (H=2,2,114, non-monotone), not a magnification
operator. The amplification (sub-quadratic LB ⇒ NP⊄P/poly) is asymptotic and CITED (Oliveira–Pich
2019; Chen–Jin–Williams 2019/2020; locality barrier Chen–Hirahara–Ren–Santhanam–Vyas); it escapes
tiny n. A negative, exact, faithful finite-instance result: the tiny-instance leverage signal
reduces to a band-population artifact — the lab's recurring collapse, seen across levels.

**STOP-and-ask:** SCATTA. Il ciclo 1 ha prodotto una FALSIFICAZIONE pulita (non un RESTATEMENT
crystallizzabile come FATTO): la leva-come-staircase non regge, e ciò che regge (meccanismo di
località + collasso su artefatto di banda) è il pattern già noto del lab. Scratch da rimuovere
prima di un eventuale commit: NESSUNO nel tree principale (modulo/test/esempio + `.cache/ct4.pkl`,
da .gitignorare o committare come cache opzionale; gli script di misura stanno in /tmp). Decisione
di commit PENDENTE sull'umano.

**NEXT unstable direction (STOP-and-ask — decisione umana):** (1) il taglio orizzontale ONESTO —
non la banda-dura (H non monotona, degenere a n piccolo) ma una FRAZIONE FISSA o un GAP-MCSP
(s = maxcost/2, gap-MCSP[s,2s]) che mantenga H confrontabile attraverso i livelli, per vedere se
la pendenza cert(N−1)/H ha una tendenza pulita o resta governata dalla combinatoria della banda;
(2) misurare l'OPERATORE giusto — non k* (min) ma l'intera curva certified(k)/H e la sua pendenza
al variare di n, accettando che a n finito non c'è regime ma solo punti; (3) STOP del programma
magnification (la barriera di località, come la natural-proofs di Module 1, è un muro CITABILE
reso esatto: il meccanismo gira ma l'amplificazione è asintotica e sfugge al tiny — 5° arena,
stesso collasso). NESSUN auto-ciclo senza una direzione con falsificatore dichiarato in anticipo.

---

## Entry 14 — Magnification Frontier ciclo 2: il taglio orizzontale onesto (frazione fissa θ=0.5) — curva di ostruzione normalizzata c(j) (2026-06-14)

**Contesto:** dopo Entry 13 (ciclo 1: staircase rho=1 FALSIFICATA, artefatto della banda-dura
degenere H=2, non monotona attraverso i livelli), l'umano ha lanciato il ciclo 2 = l'opzione (1)
del NEXT precedente, il "taglio orizzontale ONESTO": abbandonare la policy banda-dura (H=maxcost−1,
H non monotona) per una policy a FRAZIONE FISSA s=round(maxcost·θ), θ=0.5, che mantenga H
NON-degenere e confrontabile tra i livelli, e misurare se la pendenza dell'ostruzione ha una
tendenza pulita o resta combinatoria del set duro.

**Oggetto (Builder, `pnp_lab/meta_complexity/locality.py`):** aggiunti `fixed_fraction_threshold(ct,
theta=0.5)` (round banker's: s=2,4,8 a n=2,3,4), `obstruction_curve(meta,N,jmax=2)` → [c(0),c(1),
c(2)] con la curva normalizzata c(j)=certified(N−j)/H in `Fraction` ESATTE (no float), dataclass
`LevelCurve`, `level_curves`. Test nuovi in `tests/test_locality.py` (5, incl. lo slow decisivo
`test_level_invariance_n3_vs_n4_KILLER_A` con `@pytest.mark.timeout(300)` che carica la cache
`.cache/ct4.pkl`). Esempio aggiornato. Suite: 11 fast + slow verdi.

**Ipotesi H (Explorer):** con θ=0.5 la curva normalizzata c(j)=certified(N−j)/H è un INVARIANTE DI
LIVELLO — c(j) indipendente da n, ovvero c(1) e c(2) COINCIDONO tra n=3 e n=4. Killer dichiarati:
KILLER-A (c(1)@n3 ≠ c(1)@n4 → riduzione a istogramma del set duro); KILLER-B (degenerazione a n
piccolo: loc<N oppure H<3); KILLER-C (c(j) derivabile da H/2^N con formula chiusa → invarianza
aritmetica). Policy scelta = frazione fissa, NON gap-MCSP (che a n=4 con maxcost=15 darebbe la
finestra dura cost≥16 VUOTA).

**Numeri esatti misurati (razionali; riprodotti indipendentemente dall'Adversary dal raw cost dict):**

    n   N   s   H        loc      c(0)   c(1)            c(2)
    2   4   2   2        4/4      1      0               0
    3   8   4   50       8/8      1      8/25            4/25
    4  16   8   25954    16/16    1      8990/12977      6068/12977

KILLER-A SCATTATO: c(1)@n3 = 8/25 = 0.320 ≠ c(1)@n4 = 8990/12977 ≈ 0.693; c(2)@n3 = 4/25 = 0.160 ≠
c(2)@n4 = 6068/12977 ≈ 0.468. **Ipotesi level-invariant FALSIFICATA.** Solo c(0)=1 regge (banale: il
junta pieno certifica per costruzione tutto H). KILLER-B SUPERATO (loc=N, H non degenere ovunque).
Indipendentemente verificati: certified(N−1)@n4 = 17980, certified(N−2)@n4 = 12136.

**Verdetto Adversary = RESTATEMENT/KILLED (collasso #11 del lab), tutto misurato in codice:**
- **KILL STRUTTURALE (solo j=1):** MCSP[s] è invariante per permutazione delle coordinate ⇒
  certified(N−1) è IDENTICO su tutti gli assi (tutti = 17980 a n=4, tutti = 16 a n=3) ⇒ la
  massimizzazione "best k-local set S" è VACUA a j=1. CORREZIONE dell'Evaluator: vale SOLO per j=1;
  a j≥2 il max MORDE (a n=3 le coppie danno certified(N−2) ∈ {0,8}, max=8 > media) ⇒ NON estendere
  "max vacuo" a j≥2.
- **RIDUZIONE-A-NOTO:** c(1) = 2·E_axis/H = 1 − AvgSensitivity_restricted/N = densità degli archi
  del set duro nell'ipercubo = average sensitivity di MCSP[s], oggetto Fourier/influence da manuale,
  NON località.
- **NULL-MODEL:** per un set duro random di densità p, c(j) ≈ 2^j·p^(2^j−1) → predice la crescita
  misurata (c(1): 0.39→0.79; c(2): 0.030→0.248). "c(j) cresce con n" = concentrazione triviale.
- **ARTEFATTO DI SOGLIA:** θ=0.5 NON fissa la densità (p=0.195 a n=3, 0.396 a n=4); c(1) traccia p →
  il gap è un confronto fra densità NON appaiate.
- **STRAW-MAN:** l'invarianza-di-livello non era mai stata plausibile.

**Evaluator: robustness 8/10. VERDETTO = RESTATEMENT-of-known** (falsificazione GENUINA: sì;
contenuto residuo nuovo: no). Flag APERTI: off-tiny-instance, straw-man, artefatto-di-soglia,
vacuità-del-max (solo j=1; NON dimostrata a j≥2), overfitting (lieve). Flag CHIUSI: circolarità
(numeri rigenerati indip. dal raw cost dict), confirmation-bias (il team ha cercato e dichiarato il
proprio kill).

**Misura residua j≥2 (inline dopo l'Evaluator, per chiudere il regime dove il max morde):** eccesso
di clustering c(2)−null(4p^3): n=3 → 0.1600−0.0298 = +0.1302; n=4 → 0.4676−0.2484 = +0.2191.
L'eccesso CRESCE (non è invariante di livello) ⇒ anche il regime j≥2 collassa: nessun segnale di
livello sopravvive. Chiusura pulita.

**Fix d'igiene applicato:** il test slow del ciclo 1 `test_leverage_staircase_FALSIFIED_at_n4` ora
carica `.cache/ct4.pkl` (se presente) + `@pytest.mark.timeout(900)` invece di ricostruire n=4 →
passa in ~240s (prima andava in timeout a 120s, non eseguibile). La falsificazione del ciclo 1 è
ora CI-rigenerabile.

**Honesty boundary (inglese, per il doc se si cristallizza):** This cycle COMPUTES, as exact
rationals (no floats), the normalized obstruction curve c(j)=certified(N−j)/H of MCSP[s]:{0,1}^N→
{0,1}, N=2^n, at n=2,3,4 under the fixed-fraction threshold s=round(maxcost·θ), θ=0.5. The measured
rationals (c(1)@n3=8/25, c(1)@n4=8990/12977; c(2)@n3=4/25, c(2)@n4=6068/12977) are reproduced
independently and exactly falsify the level-invariance hypothesis: only c(0)=1 holds (trivially).
The c(1) datum is permutation-invariant in the coordinates of MCSP[s] (certified(N−1) identical for
every dropped axis), so the best-k-local-set maximization is vacuous at j=1 and c(1) reduces exactly
to a global statistic — the average sensitivity / hypercube edge-density of the hard set, a textbook
Fourier/influence quantity, not a locality effect. θ=0.5 does not hold the hard-set density fixed
across levels (≈0.195 at n=3 vs 0.396 at n=4), so the observed growth of c(j) tracks unmatched
densities and is reproduced by a random-hard-set concentration null model 2^j·p^(2^j−1). For j≥2 the
subset maximization is NOT vacuous, but the excess over the null model also grows with n
(0.130→0.219), so no level-invariant signal survives there either. The asymptotic magnification
theorems (Oliveira–Pich 2019; Chen–Jin–Williams 2019/2020; McKay–Murray–Williams 2019) and the
locality barrier (Chen–Hirahara–Ren–Santhanam–Vyas) are CITED, never computed; at finite n the
threshold is a single integer, not a regime. No P vs NP claim. A faithful finite measurement method,
not a result.

**STOP-and-ask:** SCATTA. Il sotto-ramo "locality barrier" del programma magnification ha ora
collassato DUE volte sullo stesso modulo (Entry 13 staircase→artefatto banda-dura H=2; Entry 14
level-invariance→average sensitivity + artefatto di densità), entrambe riducibili a statistiche
globali note. Diagnosi STRUTTURALE: MCSP[s] è permutazione-invariante, quindi ogni discriminante
"best k-local" collassa a una funzione simmetrica del set duro. Scratch da rimuovere: NESSUNO
(working tree pulita; gli script di misura sono in /tmp, fuori dal repo; `.cache/` è gitignorato).
Decisione di commit del ciclo 2 PENDENTE sull'umano.

**NEXT unstable direction (decisione umana):** (1) CHIUDERE il sotto-ramo locality (raccomandazione
netta dell'Evaluator: 2 collassi strutturali, un terzo giro ricadrebbe nella stessa classe);
(2) cambiare arena DENTRO il programma magnification meta-livello, ma serve un oggetto NON
permutazione-invariante o una misura che non sia una statistica globale del set duro (rischio:
rientra comunque nel dizionario); (3) STOP del programma magnification nel suo insieme (5ª arena,
stesso collasso: muro citabile reso esatto, meccanismo gira ma amplificazione asintotica sfugge al
tiny). NESSUN auto-ciclo senza falsificatore dichiarato in anticipo.
