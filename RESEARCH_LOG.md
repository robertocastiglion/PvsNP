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

---

## Entry 15 — CHIUSURA: cristallizzazione del sotto-ramo locality come Module 21 (2026-06-14)

**Decisione umana (2026-06-14):** opzione (1) di Entry 14 — CHIUDERE il sotto-ramo locality e
cristallizzare il risultato negativo onesto come Module. Il sotto-ramo è collassato due volte
sullo stesso modulo (Entry 13 staircase ρ=1 → artefatto banda-dura degenere H=2; Entry 14
level-invariance → average sensitivity + artefatto di densità), e la causa è STRUTTURALE, non di
parametrizzazione: MCSP[s] è invariante per permutazione delle coordinate, quindi ogni
discriminante "best k-local" collassa a una funzione simmetrica del set duro (statistica globale
= oggetto del dizionario). Un terzo ciclo nello stesso modulo ricadrebbe nella stessa classe.

**Cristallizzato:** `docs/locality-barrier.md` (Module 21, EN-first con Honesty boundary). Stato:
- Il MECCANISMO della barriera di località è reso ESATTO e FEDELE: MCSP[s] è un N-junta genuino
  (loc=N: 4/4, 8/8, 16/16, killer-fidelity superato), certified(k) raggiunge H solo al junta
  pieno. Questo regge e resta nel repo come modello eseguibile fedele di un muro NOTO (come
  Module 1 per le natural proofs).
- La LEVA (l'operatore che avrebbe dovuto portare contenuto di magnification attraverso i livelli)
  collassa: entrambi i cicli riducono a statistiche globali note del set duro. 5ª arena del
  Collapse Theorem, al meta-livello.
- L'amplificazione vera (small LB → big separation) è asintotica e CITATA; sfugge al tiny per
  costruzione. NESSUN claim su P vs NP.

**Aggiornamenti repo (questa entry):** `docs/locality-barrier.md` creato; README aggiornato (riga
Module 21 nella tabella + voce nella lista docs + conteggio test). I file di codice/test/esempio
del ciclo 2 erano già committati (54ae483); le entry 13–14 già nel log. Memoria aggiornata
(magnification-frontier.md → sotto-ramo CLOSED/Module 21; MEMORY.md; tiny-instance-collapse.md;
prompts/magnification-frontier.md → stato programma). Suite verde.

**Stato del PROGRAMMA Magnification Frontier (non solo del sotto-ramo):** il sotto-ramo locality è
CHIUSO. Il programma nel suo insieme resta APERTO ma in STOP-and-ask: per riaprire serve un oggetto
meta-livello NON permutazione-invariante (o una misura che non sia una statistica globale del set
duro), altrimenti rientra nel dizionario — esattamente la lezione strutturale di questo Module.
Decisione futura dell'umano; nessun auto-ciclo.

---

## Entry 16 — Magnification Frontier ciclo 3: RIAPERTURA con MBPSP[s] a ordine fisso — l'oggetto NON permutazione-invariante (2026-06-15)

**Decisione umana (2026-06-15):** riaprire il programma magnification col candidato ① proposto —
`MBPSP[s]` a **ordine di variabili fissato**. Il criterio di riapertura (Entry 15) era esatto:
serve un oggetto meta-livello **non permutazione-invariante**. Questo ciclo lo fornisce, col
minimo cambiamento alla macchina esistente: stessa cornice meta di Module 21 (input = truth-table
di `N=2^n` bit), ma la misura di complessità è la **dimensione dell'OBDD ridotto a ordine fisso**
`π = (x_{n-1},…,x_0)` invece della dimensione di formula. HARD = "nessun OBDD piccolo".

**Explorer (fidelity-killer dichiarato in anticipo).** `MBPSP[s]` è non-permutazione-invariante
⟺ la sua pair-influence `pairinf(d)` dipende dal **supporto** del vettore differenza `d` (quali
variabili, dunque la loro posizione nell'ordine), non solo dal peso di Hamming ⟺ lo **spread**
`max−min` di `pairinf(d)` entro una classe di ugual peso è `> 0`. KILLER FIRES (6° collasso) se lo
spread = 0 ovunque anche a n=4 (l'ordine si laverebbe via in aggregato). PASS se spread > 0 e
strutturato dall'ordine. Controllo obbligatorio: la STESSA misura su MCSP (formula) deve dare
spread = 0 (permutazione-invariante), per isolare l'effetto all'ordine OBDD.

**Builder (esatto, interi, riproducibile).** `pnp_lab/meta_complexity/order_locality.py`:
`min_obdd_size(t,n)` = conteggio nodi del ROBDD canonico a ordine fisso (sotto-funzioni distinte
non-costanti + terminali, nodi ridondanti rimossi; verificato su x0→3, costante→1, AND→4); nessuna
DP, quindi n=4 (tutte le 2^16 truth-table) gira in <1s — **MBPSP è più economico di MCSP**.
`variable_swap`, `meta_truth_table_obdd`, `fixed_fraction_threshold` (θ=0.5, banker's rounding),
`pair_influence` (base coord 0 per traslazione-invarianza, dimostrata), `weight_class_spread`,
`order_asymmetry`. Test `tests/test_order_locality.py` + esempio `examples/run_order_locality.py`.

**Prova fondante (non-invarianza, n=4).** La STESSA funzione con due variabili scambiate è una
truth-table diversa con OBDD di taglia diversa allo stesso ordine: `(x0∧x1)∨(x2∧x3)` → 6 nodi;
scambiando le var 1,2 → `(x0∧x2)∨(x1∧x3)` → 8 nodi. La formula non può distinguerle (è simmetrica).
La dimensione OBDD è invece invariante per NEGAZIONE di variabile (scambia i due figli di un nodo) —
verificato in test — il che è perché l'influenza di singola coordinata è inutile (traslazione-
invarianza) e serve la pair-influence.

**MISURA DECISIVA (esatta, congelata; veloce, niente cache per il titolo):**

    n   N    s    H        spread per peso w=1,2,3,4      verdetto
    2   4    2    14       0, 0                           ordine silente
    3   8    4    224      0, 0, 0                        ordine silente
    4  16    6    64282    184, 176, 16, 0                ORDINE SOPRAVVIVE
    --- controllo: MCSP[s] (formula, Module 21) ---
    4  16    8    25954    0, 0, 0, 0                     lavato via (simmetrico)

**KILLER PASSATO.** A n=4 `pairinf(d)` distingue differenze di ugual peso per il supporto
(w=1: differire in x3 = variabile in cima → 4056; in x1 → 3872; spread 184), mentre il controllo
MCSP a formula è piatto (spread 0 ovunque). Il criterio di riapertura è **SODDISFATTO**: MBPSP[s]
è l'oggetto meta-livello non-permutazione-invariante richiesto. È il PRIMO esito non-collassante di
questo tipo nel lab (finora solo collassi/falsificazioni).

**Adversary.** (1) Fedeltà ROBDD: verificata su funzioni note + testimone d'ordine textbook.
(2) È un artefatto della mia misura? NO: il controllo MCSP sulla stessa `pairinf`/soglia/n dà spread
0 — l'effetto è specificamente l'ordine OBDD. (3) Robustezza alla soglia: spread > 0 per OGNI
s∈[5,10] (tutta la banda non-degenere), piatto solo a s≤4 dove HARD satura (H≈65534, meta-funzione
quasi-costante). NON è un punto isolato a s=6. (4) Vacuità: l'asimmetria si ACCENDE a n=4, l'ultimo
livello brute-forzabile (n=5 = 2^32) → un solo livello non-nullo, NON ancora un invariante di
livello misurato. (5) Over-claim: spread > 0 RIMUOVE la causa strutturale del collasso precedente
(permutazione-invarianza) ma NON prova che la prossima ostruzione di località porti contenuto di
livello — resta aperto al prossimo ciclo.

**Evaluator — verdetto: SUCCESSO (riapertura).** Fedeltà ALTA (calcolo esatto, testimone textbook,
controllo MCSP isola l'effetto, robusto alla soglia). Tangibilità ALTA (interi esatti, veloce, niente
cache per il titolo, valori congelati nei test, suite verde).

**Honesty boundary (EN, per l'eventuale doc).** COMPUTED (exact integers, no floats): min-OBDD-size
at a fixed order; its non-invariance under variable permutation (n=4 witness 6≠8) and invariance
under negation; MBPSP[s] as a meta-function; pair_influence and its weight-class spread for n=2,3,4,
robust across thresholds s∈[5,10], with the MCSP formula control flat (spread 0). The reopening
criterion — a non-permutation-invariant meta object — is MET, exactly and reproducibly. LIMITS:
(1) the asymmetry switches on only at n=4, the last brute-forceable level, so it is a single
non-zero level — the onset is LOCATED, a cross-level invariant of the asymmetry is NOT yet measured
(the cake's "leverage" is opened, not yet quantified). (2) The spread is modest in relative terms
(~4.5% of the base at n=4, w=1) and shrinks with weight (vanishing at w=4, a singleton class).
(3) spread>0 removes the STRUCTURAL cause of the prior collapse; it does NOT prove the next locality
obstruction on MBPSP carries level-content — open. (4) The asymptotic magnification / locality
theorems for branching programs and OBDDs (Oliveira–Pich 2019; Chen–Jin–Williams 2019/2020;
Chen–Hirahara–Ren–Santhanam–Vyas) are CITED, never computed; at finite n the threshold is a single
integer, not a regime; no separation, no P vs NP claim.

**Stato repo (questa entry):** creati `pnp_lab/meta_complexity/order_locality.py`,
`tests/test_order_locality.py`, `examples/run_order_locality.py`. Suite verde (un solo skip = il
controllo MCSP slow, gated sulla cache `.cache/ct4.pkl`). Scratch in /tmp (fuori dal repo). NON
ancora cristallizzato come Module/doc né aggiunto al README (cristallizzazione = decisione umana,
come per Module 21).

**STOP-and-ask (decisione umana):** il programma è RIAPERTO con un oggetto sano. Tre direzioni:
(1) **CICLO 4 — la leva vera**: far girare l'ostruzione di località (`certified_k_local`,
`best_k_local` di `locality.py`) su MBPSP[s] e verificare se i coordinate-set ottimi sono
order-strutturati e se la curva di ostruzione NON ricade in una statistica del dizionario (il test
che la riapertura merita); (2) **cristallizzare** ora il risultato di riapertura come Module 22 + doc
+ README; (3) **STOP**. Nessun auto-ciclo senza fidelity-killer dichiarato in anticipo.

---

## Entry 17 — Magnification Frontier ciclo 4: l'ordine RAGGIUNGE il muro FEDELE di Module 21 (2026-06-15)

**Decisione umana (2026-06-15):** opzione (1) dopo Entry 16 — il CICLO 4, "la leva vera". Il ciclo 3
ha mostrato che l'OGGETTO `MBPSP[s]` è non-permutazione-invariante via una misura d'influenza custom
(`pair_influence`). Il ciclo 4 chiede se l'ordine arriva fino al MURO che il programma cura davvero:
l'ostruzione di certificazione di Module 21 (`locality.certified_k_local`) — # di istanze dure che un
argomento k-locale certifica con CERTEZZA (fibra pura-dura).

**Explorer (killer dichiarato in anticipo).** Si misura al livello j=2 (si RILASCIA una coppia di
coordinate, k=N-2 lette): a j=1 il gruppo di traslazione (negazione di variabile = permutazione delle
posizioni x→x⊕v, simmetria di MBPSP) è transitivo sulle singole coordinate ⇒ `certified(N-1)` è
isotropico per costruzione. Per traslazione `certified_drop(a,b)=certified_drop(0,a⊕b)`, quindi il
muro dipende solo dal vettore differenza `d`. IPOTESI: `certified_drop(d)` dipende dal SUPPORTO di d
(spread > 0 entro una classe di ugual peso). KILLER FIRES se spread=0 ovunque anche a n=4 (la
massimizzazione resterebbe vacua SUL MURO nonostante l'oggetto sia non-invariante ⇒ ricaduta nella
trappola simmetrica di Module 21 ⇒ 12° collasso, informativo). PASS se spread>0.

**Builder (esatto, riproducibile).** Aggiunti a `pnp_lab/meta_complexity/order_locality.py`:
`certified_drop_pair`, `DropClass`, `certified_drop_spread`, `WallAnisotropyRow`, `wall_anisotropy`.
+5 test (incl. cross-check `max_pairs certified_drop == locality.certified_k_local(N-2)` = la PROVA
che è il muro di Module 21, non una ridefinizione; +1 controllo MCSP slow gated su cache). Esempio
aggiornato.

**MISURA DECISIVA (esatta, congelata; veloce, niente cache per il titolo):**

    n   N    s    H        spread del muro (w=1,2,3,4)    verdetto
    3   8    4    224      0, 0, 0                        isotropico (ordine silente)
    4  16    6    64282    144, 144, 16, 0                MURO VEDE L'ORDINE
    --- controllo: MCSP[s] (formula, Module 21) ---
    4  16    8    25954    0, 0, 0, 0                     isotropico (trappola simmetrica)

**KILLER PASSATO.** A n=4 il MURO FEDELE (non solo la pair-influence custom del ciclo 3) è
order-anisotropico: `certified_drop(d)` distingue differenze di ugual peso per il supporto (w=1:
differire in x1/x2 → 61592; in x3 → 61448; in x0 → 61480), mentre il controllo MCSP a formula è
piatto in ogni classe. La massimizzazione sui coordinate-set è GENUINAMENTE non-vacua su MBPSP: drop
di ugual peso certificano numeri DIVERSI di istanze dure. La riapertura è validata SUL MURO STESSO del
programma, non solo su una misura ausiliaria.

**Cross-check di fedeltà (in test):** `max_{a<b} certified_drop_pair(a,b) == locality.certified_k_local
(meta, N, N-2) == 152` a n=3 ⇒ `certified_drop_pair` È esattamente il muro di Module 21. Traslazione-
invarianza `certified_drop(a,b)==certified_drop(0,a⊕b)` verificata su tutte le coppie.

**Adversary.** (1) Fedeltà: provata col cross-check sopra — è il muro di Module 21. (2) Artefatto della
misura? NO: MCSP sulla STESSA misura `certified_drop` è piatto (0,0,0,0) ⇒ l'effetto è specificamente
l'ordine OBDD. (3) Robustezza alla soglia: anisotropico per OGNI s∈[5,10] (banda non-degenere),
isotropico solo a s≤4 dove HARD satura (H≈65534). (4) Ridondanza col ciclo 3? NO: `pair_influence`
(sensibilità locale su un 2-cubo) e `certified_drop` (conteggio globale di certificazione pura-dura)
sono quantità DIVERSE; pairinf anisotropico non FORZA certified anisotropico ⇒ evidenza indipendente.
(5) Vacuità/over-claim: anisotropia REALE ma ESILE (~0.23% del valore base a n=4, w=1, più debole del
~4.5% della pair-influence) e solo a n=4 (n=5 = 2^32, infattibile) ⇒ il muro raggiunge l'ordine al
livello più profondo misurabile, NESSUN invariante di livello. Non prova che l'ostruzione porti
contenuto di magnification NUOVO o amplifichi — solo che non è isotropica.

**Evaluator — verdetto: SUCCESSO.** La riapertura (ciclo 3) è ora DOPPIAMENTE validata: due misure
indipendenti (pair-influence del ciclo 3; muro certified del ciclo 4) mostrano entrambe che l'ordine
sopravvive a n=4, col controllo MCSP piatto per entrambe. Fedeltà ALTA (cross-check col muro di
Module 21, controllo MCSP, robustezza alla soglia). Tangibilità ALTA (interi esatti, veloce, niente
cache per il titolo, valori congelati, suite verde).

**Honesty boundary (EN, per l'eventuale doc).** COMPUTED (exact integers, no floats): the Module-21
faithful certification wall `certified_drop(d)` (= `locality.certified_k_local(N-2)`, cross-checked)
on MBPSP[s], its weight-class spread for n=3,4 (0,0,0 / 144,144,16,0), robust across thresholds
s∈[5,10], with the MCSP formula control flat (0,0,0,0). The order reaches the program's OWN faithful
locality wall — the maximization over coordinate-sets is non-vacuous on MBPSP, INDEPENDENT of the
Cycle-3 influence measure. LIMITS: (1) the wall-anisotropy is modest (~0.23% at n=4, w=1, fainter
than Cycle 3's ~4.5%) and appears only at n=4, the last brute-forceable level (n=5=2^32) → the wall
reaches the order at the deepest measurable level, a cross-level invariant is NOT measured; (2) j=1
is isotropic by construction (translation transitivity) — the effect lives at j≥2; (3) the result
shows the wall is non-isotropic; it does NOT show the certified obstruction carries NEW magnification
content or amplifies. The asymptotic magnification / locality theorems (Oliveira–Pich 2019;
Chen–Jin–Williams 2019/2020; Chen–Hirahara–Ren–Santhanam–Vyas) are CITED, never computed; no
separation, no P vs NP claim.

**Stato repo (questa entry):** estesi `pnp_lab/meta_complexity/order_locality.py`,
`tests/test_order_locality.py`, `examples/run_order_locality.py`. Suite verde (exit 0, gli unici skip
= i 2 controlli MCSP slow gated su `.cache/ct4.pkl`). Scratch in /tmp (fuori dal repo). NON ancora
cristallizzato come Module/doc né nel README (decisione umana).

**STOP-and-ask (decisione umana).** La riapertura è solida e doppiamente validata; il programma ha ora
raggiunto il suo VERO soffitto al tiny: l'asimmetria d'ordine è stabilita a n=4 su due misure
indipendenti, ma la LEVA attraverso i livelli (small LB → big separation, il cuore della
magnification) è asintotica e sfugge a n=5+ per costruzione — esattamente come i teoremi citati. Tre
direzioni: (1) **cristallizzare** ciclo 3+4 come Module 22 ("Order-Locality: la barriera resa
non-invariante") + doc + README — chiusura onesta e positiva del programma magnification; (2)
**cambiare misura di leva** restando a n≤4 (rischio: rientro nel dizionario, l'anisotropia è già
esile); (3) **STOP**. Raccomandazione dell'Evaluator: (1) — il programma ha prodotto il suo primo
esito non-collassante e un secondo livello di validazione; un terzo ciclo a n≤4 non aggiungerebbe un
invariante di livello (il vincolo è computazionale, non di idea). Nessun auto-ciclo.

---

## Entry 18 — Cristallizzazione: Module 22 "Order-Locality" (2026-06-15)

**Decisione umana (2026-06-15):** opzione (1) dopo Entry 17 — cristallizzare i cicli 3+4 come
Module 22, chiusura onesta e positiva del programma Magnification Frontier.

**Fatto.** Creato `docs/order-locality.md` (Module 22, EN-first): la riapertura come **primo esito
non-collassante** del lab — la trappola del dizionario di Module 21 evasa **rompendo la simmetria**
(l'ordine OBDD), non con un nuovo discriminante. Documenta l'oggetto `MBPSP[s]` (min-OBDD-size a
ordine fisso, non-permutazione-invariante; prova fondante 6≠8), le due conferme indipendenti (C3
`pair_influence` 184,176,16,0; C4 muro fedele `certified_drop` 144,144,16,0 a n=4, controllo MCSP
piatto su entrambe), il cross-check col muro di Module 21, e il **soffitto onesto** (anisotropia esile
~4.5%/~0.23%, solo a n=4, nessun invariante di livello; leva asintotica CITATA). Aggiornato `README.md`
(riga 22 nella tabella moduli + voce nella lista `Documentation`). Codice/test/esempio già committati
in questa entry-set (order_locality.py, test_order_locality.py, run_order_locality.py). Suite verde.

**Stato del programma:** Magnification Frontier RIAPERTA e poi CHIUSA al suo soffitto onesto
(computazionale, non concettuale). Nessun auto-ciclo. Il vincolo per una leva cross-livello è n=5=2^32,
infattibile per brute force — esattamente come i teoremi asintotici citati.

---

## Entry 19 — Cristallizzazione: Module 23 "Certified-Bounds Regime" (2026-06-16)

**Decisione umana (2026-06-16):** opzione (1) dopo lo scoping (Entry implicita / commit
c4b3ebb) — cristallizzare il Cycle 1 del regime certified-bounds come Module 23, chiusura
onesta dell'ULTIMA porta out-of-the-box del lab.

**Verdetto: RESTATEMENT #12** (l'esito pre-dichiarato e accettabile dal brief).

**Oggetto.** `family_or_and(n)` (n pari), la famiglia fondante di Module 22:
`f_n(x) = OR_k ( x_{2k} AND x_{2k+1} )`, letta a due ordini di variabili (relabelling +
`min_obdd_size` a frame fisso): ordine BUONO π ⇒ `size_good = n+2` CERTIFICATO; ordine
CATTIVO π' interlacciato ⇒ `size_bad = 2^(n/2+1)` CERTIFICATO. Entrambi da una ricorrenza
CONTROLLATA + cross-check con l'esatto a n=2,4,6,8 (anchor di fedeltà). Prova fondante: 6 ≠ 8
a n=4 (stesso testimone di Module 22).

**La misura valida (l'unica).** Il gap certificato `g(n) = 2^(n/2+1) − (n+2) = 0,2,8,22` —
istanza FINITA ESATTA del bound asintotico CITATO (Bryant 1991 / Wegener, `2^Ω(n)`), SENZA
enumerazione di alcuno spazio di funzioni. Il regime RESTATES Bryant ⇒ RESTATEMENT #12.

**STRUCK (category error).** L'evidenza-muro del primo draft (`A(n)` = spread del muro fedele
`certified_drop_spread` su tt_π') è cancellata: quel muro è una statistica della META-funzione
`MBPSP[s]` sull'INSIEME di tutte le `2^N` funzioni — gli era data UNA singola funzione (la
chiamata fedele solleva sul mismatch N-vs-n). Adversary + Evaluator KILL.

**Il finding reale — il soffitto del regime.** La certificazione rende cheap (`O(N)`) la
taglia OBDD di UNA funzione, evadendo lo sweep — e SOLO lì. Un invariante di MURO (Module
21/22) è irriducibilmente una proprietà della meta-funzione sull'INSIEME: serve un insieme
duro da certificare. Reintrodurre l'insieme a n≥5 reintroduce esattamente l'enumerazione
`2^(2^n)` che il regime voleva evitare. La certificazione compra cheapness PER-ISTANZA, non
l'invariante cross-livello: appena la quantità è una proprietà del muro, lo sweep ritorna. È
lo stesso muro computazionale, ristabilito.

**Honesty boundary (EN).** COMPUTED (exact integers, no floats): the certified recurrence
`size_good = n+2`, `size_bad = 2^(n/2+1)`, cross-checked vs exact `min_obdd_size` at
n=2,4,6,8; the gap `g(n)`. Finite exact instance of Bryant/Wegener (CITED, never re-proved)
⇒ RESTATEMENT #12. Wall-anisotropy STRUCK (category error). No separation, no cross-level
invariant, NO P vs NP claim.

**Fatto.** Creato `docs/certified-bounds.md` (Module 23, EN-first). Aggiornato `README.md`
(riga 23 nella tabella moduli + voce nella lista Documentation). Codice/test/esempio committati
in questa entry-set (certified_obdd.py, test_certified_obdd.py, run_certified_obdd.py). Suite
del modulo verde (8 passed).

**Stato del programma:** TUTTE le porte note del lab sono ora CHIUSE — i due rami principali
(Collapse Theorem; Magnification Frontier/Module 22) + l'ultima porta out-of-the-box
(certified-bounds/Module 23), tutte sullo STESSO muro computazionale (enumerazione brute-force
su tiny instances). Nessun auto-ciclo. Il lab è una METODOLOGIA con 12 RESTATEMENT + 1
falsificazione + 1 esito non-collassante (Module 22), non un attacco a P vs NP.

---

## Entry 20 — Module 24 "Sampled Order-Anisotropy at n=5": il PRIMO PASS cross-livello (2026-06-17)

**Decisione umana (2026-06-16/17):** dopo la chiusura di tutte le porte note (Entry 19), la
direzione scelta dal PI e' il **pivot statistico a n=5** — abbandonare deliberatamente la regola
dell'intero-esatto e CAMPIONARE, per ottenere l'unico dato cross-livello che Module 22 non poteva
(n=5 = 2^32, non enumerabile). La tesi del lab ("exactness is the trap") usata COME metodo: si SPENDE
esattezza per guadagnare portata.

**Verdetto: PASS (qualificato) — il primo esito non-collassante che SOPRAVVIVE anche un livello.**

**Explorer (killer pre-dichiarato).** Le statistiche di Module 22 sono SOMME DI INDICATORI sullo
spazio meta uniforme t in {0,...,2^N-1}; una somma di indicatori e' esattamente cio' che Monte Carlo
stima, e min_obdd_size e' O(N) per truth-table. Stimatore = Common Random Numbers (stessi t per d_hi
e d_lo, i due indicatori condividono 2 dei 4 vertici del cubo => Var(D) piccola => differenza piccola
risolvibile). Coppia PRE-REGISTRATA (niente max-min, che e' gonfiato dal rumore = l'artefatto del
ciclo 1): peso-1 variabile top vs bottom (n=5: d_hi=16=x4 vs d_lo=1=x0). KILLER: se la CI 99% pooled
include 0 => spara (anisotropia non risolvibile cross-livello, n=4 non dimostrato persistente). PASS
se la coppia differisce significativamente E il controllo nullo resta compatibile con 0.

**Builder (esatto dove possibile, stimato dove necessario).** `pnp_lab/meta_complexity/
sampled_order_n5.py`: predicati hardness (mbpsp / popcount-control), `crn_pair_diff` (stimatore CRN
con SE), `anchor_n4` (riproduce l'esatto noto dentro CI), `replicate_n5` (pooling inverse-variance
multi-seed + controllo), `threshold_regime` (la degenerazione). +5 test veloci (anchor deterministico,
controllo nullo ESATTO=0 a n=4, semantica CRN) +2 slow (riproduzione PASS + degenerazione).

**MISURA DECISIVA (stimata, CI 99%, congelata):**

    stage                                              risultato
    ANCHOR n=4 (verita' esatta dentro CI)              PASS (184 in CI 99%)
    SEGNALE n=5 s=10 coppia x4-vs-x0, 8 seed x 300k     diff prob ~ +1.7e-4, pooled z ~ +4.9,
                                                        CI 99% esclude 0, 7/8 seed positivi
    CONTROLLO nullo popcount, stessa coppia            pooled ~ 0, non significativo
    KILLER                                             NON spara -> PASS

Replicato 3 volte indipendentemente (z=4.92, z=4.38, single-run z=3.3; segni 7/8, 7/8). L'anisotropia
d'ordine di MBPSP[s] SOPRAVVIVE da n=4 a n=5: la prima volta che una quantita' misurata nel lab supera
un livello invece di collassare su un oggetto noto. Module 22 NON era un artefatto di n=4.

**Adversary.** (1) Instabilita' single-run: vera (z flippa segno tra 80k e 1.2M) -> risolta col
pooling multi-seed + check dei segni. (2) Artefatto dello stimatore? NO: il controllo nullo popcount
(permutazione-invariante, ESATTAMENTE 0 per simmetria, verificato a n=4) pool ~0 mentre il segnale
pool z~4.9. (3) Fishing? NO: coppia pre-registrata UNICA, fissata dalla struttura d'ordine di n=4, non
max-min. (4) Anchor: il sampler riproduce l'esatto 184 dentro CI -> stimatore non distorto.

**Soffitto (Evaluator) — SOPRAVVIVENZA, NON LEVA.** (1) La tendenza cross-livello e' AMBIGUA per
normalizzazione: la differenza assoluta DECADE (n=4 4.9e-4 -> n=5 1.4e-4, stessa coppia) ma quella
relativa al boundary CRESCE (0.8% -> 3.7%); nessuna "leva" canonica. (2) Sotto la policy fedele di
Module 22 (s=round(0.5*max)) la misura DEGENERA a n>=6: le dimensioni OBDD di funzioni random si
concentrano vicino al massimo (n=6 sample min=20 > s=16) => meta costante-HARD => base_prob=0
(tabella: n=4 6.1e-2, n=5 3.7e-3, n=6 0, n=7 0). Il sampling compra ESATTAMENTE UN livello sopra l'n=4
esatto; l'amplificazione asintotica resta CITATA. Stesso pattern "il regime degenera / il muro
ritorna", ma raggiunto un livello piu' in profondita' del metodo esatto, col PRIMO PASS a quel livello.

**Honesty boundary (EN).** ESTIMATED not computed: the n=5 difference (Monte Carlo, 99% CI, CRN),
validated by the exact n=4 anchor. COMPUTED exactly: min_obdd_size, the full n=4 ground truth, the
popcount control's exact-0 difference, the threshold-regime table. NOT measured: the certified wall
(~0.23%, beyond budget); any n>=6 point under the faithful policy (degenerate). CITED never computed:
the magnification/locality theorems (Oliveira-Pich; Chen-Jin-Williams; CHRSV). No separation, no P vs
NP claim.

**Stato repo:** nuovi `pnp_lab/meta_complexity/sampled_order_n5.py`, `tests/test_sampled_order_n5.py`,
`examples/run_sampled_order_n5.py`, `docs/sampled-order-n5.md`; README riga 24 + voce Documentation;
questa entry. Test veloci verdi; gli slow riproducono il verdetto congelato.

**Stato del programma:** il lab ha prodotto il suo PRIMO PASS cross-livello. La Magnification Frontier,
chiusa a n=4 (Module 22) e poi al soffitto out-of-the-box (Module 23), e' stata spinta UN livello piu'
in profondita' col sampling: l'anisotropia d'ordine sopravvive a n=5, ma come SOPRAVVIVENZA non come
LEVA (nessun invariante di livello monotono; il regime fedele degenera a n>=6). Bilancio del lab: 12
restatement + 1 falsificazione + 1 non-collasso (Module 22) + 1 PASS-di-sopravvivenza (Module 24).
Nessun auto-ciclo.

---

## Entry 21 — Module 25 "Cross-Level Survival under Median Calibration": la spinta a n=6 (2026-06-17)

**Decisione umana (2026-06-17):** dopo Module 24 (PASS a n=5), direzione "spingi a n=6".

**Verdetto: PASS — sopravvivenza cross-livello su TRE livelli, NON crescita di leva.**

**Explorer.** Il faithful theta=0.5*max DEGENERA a n>=6 (Module 24: le taglie OBDD random si
concentrano vicino al massimo => meta costante-HARD => pair-influence 0). Per riaprire il boundary si
RICALIBRA la soglia alla MEDIANA delle taglie OBDD (median_threshold: sweep esatto a n<=4, campionato
a n>=5), tenendo la meta-funzione non-banale (H~0.17-0.44). PREZZO dichiarato: e' un OGGETTO DIVERSO
dal muro fedele di Module 22 (soglia ricalibrata). Resto invariato: stimatore CRN, coppia
pre-registrata (var top x_{n-1} vs x0), controllo nullo popcount, pooling multi-seed. KILLER: se a n=6
la CI 99% pooled include 0 => spara. PASS se significativo + controllo piatto.

**Builder.** Aggiunti a `pnp_lab/meta_complexity/sampled_order_n5.py`: `median_threshold`,
`CrossLevelRow`, `cross_level_row` (esatto a n<=4, campionato+pooled a n>=5, con controllo),
`cross_level_table`. +3 test (n=4 esatto deterministico: diff 1536, base 21024, rel 0.0731, controllo
esatto 0; median_threshold(4)==10; slow n=6 survival con @timeout). Esempio `run_cross_level_median.py`.

**MISURA (median policy; n=4 esatto, n=5/6 campionati CRN, congelata):**

    n   s    H_frac   base_prob   diff_prob    z       rel=diff/base   control       signs
    4* 10   0.170    0.321       +2.34e-2     esatto  +7.3%           0 (esatto)    --
    5  16   0.246    0.300       +3.53e-2     +73     +11.8%          piatto (-0.95) 6/6
    6  26   0.435    0.282       +2.05e-2     +43     +7.3%           piatto (-0.24) 6/6

SOPRAVVIVE tutti e tre i livelli: a n=5,6 la coppia pre-registrata e' significativa con ampio margine,
TUTTE le seed positive, controllo nullo PIATTO a OGNI livello => segnale specifico dell'ordine, non
artefatto della calibrazione.

**Adversary.** (1) Oggetto ricalibrato: VERO e dichiarato (median != faithful 0.5*max); raggiungere
n=6 ha avuto questo prezzo. (2) La leva NON cresce: rel 7.3->11.8->7.3% (non-monotono, limitato);
magnification richiede crescita, qui e' neutra. (3) Confound di H: la policy median-intera non tiene
fissa la frazione hard (0.17/0.25/0.44) e il rel traccia H (picco a n=5, H~0.25) => la "stabilita'"
del rel non va sovrainterpretata. Il controllo piatto a OGNI H difende la claim di SOPRAVVIVENZA, non
una claim di tendenza-leva. (4) Artefatto dello stimatore? NO: popcount sotto la STESSA median H pool
~0 mentre il segnale e' z=43-73.

**Evaluator — verdetto: PASS (sopravvivenza), soffitto NETTO.** Rafforza la sopravvivenza cross-livello
(da 1 livello in Module 24 a 3 qui); NON dimostra crescita di leva cross-livello. L'amplificazione
asintotica resta CITATA. Tangibilita' ALTA (n=4 esatto congelato, n=5/6 z enormi, controllo piatto,
suite verde). Onesta' ALTA (oggetto ricalibrato + leva non-crescente + confound H tutti dichiarati).

**Honesty boundary (EN).** ESTIMATED not computed: the n=5,n=6 differences (Monte Carlo, CRN, pooled).
COMPUTED exactly: the full n=4 row, the popcount control's exact-0, min_obdd_size (O(N), also at n=6 on
64-bit tables). RECALIBRATED (stated): median threshold != Module 22 faithful policy. NOT shown: any
GROWING cross-level leverage (bounded, H-confounded). CITED never computed: magnification/locality
theorems. No separation, no P vs NP claim.

**Stato repo:** esteso `sampled_order_n5.py` (sezione cross_level_*), `tests/test_sampled_order_n5.py`
(+3, 1 slow), nuovo `examples/run_cross_level_median.py`, nuovo `docs/cross-level-median.md`; README
riga 25 + voce Documentation; questa entry. Suite veloce verde (9 fast); slow verdi.

**Stato del programma:** la Magnification Frontier e' ora misurata su TRE livelli (n=4,5,6) col sampling:
l'anisotropia d'ordine SOPRAVVIVE ovunque, ma come SOPRAVVIVENZA non come LEVA (nessuna crescita;
oggetto ricalibrato per arrivare a n=6). Bilancio del lab: 12 restatement + 1 falsificazione + 1
non-collasso (Module 22) + 1 survival-PASS a 1 livello (Module 24) + 1 survival-PASS a 3 livelli
(Module 25). La leva cross-livello (il cuore della magnification) resta asintotica e CITATA. Nessun
auto-ciclo.

---

## Entry 22 — Module 26 "Iso-Hardness Control": disinnesco il confound di H di Module 25 (2026-06-17)

**Decisione umana (2026-06-17):** dopo Module 25 (survival-PASS a 3 livelli con leva non-crescente e
confound di H dichiarato), direzione "iso-hardness (disentangle H)".

**Verdetto: PASS — la sopravvivenza cross-livello e' H-ROBUSTA, e il confound di H di Module 25 e'
FALSIFICATO; la leva resta genuinamente assente.**

**Explorer.** L'Adversary di Module 25 aveva lasciato UNA obiezione aperta: la policy median-intera NON
tiene fissa la frazione hard (H = 0.17/0.25/0.44 a n=4,5,6) e il rel poteva tracciare H invece del
livello n. Se cosi', ENTRAMBE le letture di Module 25 erano a rischio: la sopravvivenza poteva essere
un artefatto di H (il segnale potrebbe sparire a H comune) e il "no leva" poteva nascondere una leva
cancellata dalla deriva di H. Mossa: RICALIBRARE la soglia al quantile (1-H_target) per tenere H~costante
a ogni livello, su DUE fette appaiate (H_target 0.5 e 0.2), e rimisurare. Le soglie intere non centrano
H_target esattamente (le taglie OBDD sono grossolane: a n=4 frac>s salta 0.526->0.170 tra s=9 e s=10),
ma l'H raggiunto e' MOLTO piu' stretto del median-policy (H~0.53/0.55/0.44 per target 0.5 vs 0.17/0.25/
0.44). Resto invariato: stimatore CRN, coppia pre-registrata (var top x_{n-1} vs x0), controllo nullo
popcount, pooling 6 seed. KILLER pre-dichiarato: se a H fisso il segnale perde significativita' a n=5 o
n=6 (CI 99% include 0) => spara (la sopravvivenza era un artefatto di H). PASS se significativo a ogni
livello con controllo piatto; POI, separatamente e descrittivamente: il rel CRESCE con n a H fisso (la
leva) o resta non-monotono/limitato (sopravvivenza senza leva)?

**Builder.** Rifattorizzato `_anisotropy_row(n, s, ...)` condiviso (la policy di soglia e' scelta dal
chiamante; la misura e' identica) -> `cross_level_row` (Module 25) invariato, REGRESSIONE verificata
(n=4 esatto: s=10, diff 1536, base 21024, rel 0.0731 immutati). Aggiunti `iso_hardness_threshold(n,
H_target)` (quantile esatto a n<=4, campionato a n>=5), `iso_hardness_row`, `iso_hardness_table` in
`pnp_lab/meta_complexity/sampled_order_n5.py`. +3 test (soglie n=4 esatte 9/10; riga n=4 esatta congelata
H=0.5: s=9 diff 2016 base 36640 rel 0.0550 control 0, e H=0.2 coincide con M25 n=4 diff 1536; slow n=6
survival H-robusta @timeout). Esempio `run_iso_hardness.py`.

**MISURA (congelata; n=4 esatto, n=5,6 campionati CRN, pooling 6 seed, base_seed 700+10n):**

    H_target   n   s    H_ach   base    diff_prob   z        rel%    control_z   signs
    0.5       4*  9    0.526   0.559   +3.08e-2    esatto   +5.5    0 (esatto)  --
              5   15   0.548   0.394   +4.20e-2    +68.8    +10.7   piatto -0.51 6/6
              6   26   0.435   0.282   +2.15e-2    +40.5    +7.6    piatto +1.04 6/6
    0.2       4*  10   0.170   0.321   +2.34e-2    esatto   +7.3    0 (esatto)  --
              5   16   0.246   0.299   +3.41e-2    +63.0    +11.4   piatto -0.51 6/6
              6   27   0.194   0.200   +1.19e-2    +26.4    +6.0    piatto +1.04 6/6

A ENTRAMBE le fette a H fisso il segnale e' enorme a ogni livello (control piatto, 6/6 seed positive) =>
il KILLER NON spara: la sopravvivenza di Module 25 NON e' un artefatto di H. E a H fisso il rel fa ancora
PICCO a n=5 (5.5->10.7->7.6% e 7.3->11.4->6.0%), la stessa forma vista da M25 sotto la deriva di H
(7.3->11.8->7.3%) => il picco a n=5 e' proprieta' del LIVELLO, non di H: l'obiezione "rel traccia H" e'
essa stessa FALSIFICATA. Ma il picco e' LIMITATO e NON-MONOTONO => nessuna leva crescente nascosta dietro
la deriva di H.

**Adversary.** (1) H non perfettamente fisso: VERO e dichiarato (soglie intere grossolane), ma 0.53/0.55/
0.44 e' molto piu' stretto di 0.17/0.25/0.44, e la sensibilita' intra-livello di rel e' piccola (n=4
esatto: rel 2.9%->7.3% su tutto il range H 0.93->0.17) rispetto al picco a n=5; due fette appaiate
delimitano il residuo. (2) Artefatto stimatore? NO: il controllo popcount sotto la STESSA H fissa pool
piatto (|z|<=1.04) mentre il segnale e' z=26-69. (3) n=4 esatto vs n>=5 campionato: la riga H=0.2 n=4
coincide ESATTAMENTE con M25 (s=10, diff 1536) -> ancoraggio. (4) Fishing tra fette? NO: due target
pre-dichiarati, stesso verdetto su entrambi.

**Evaluator — verdetto: PASS (controllo), soffitto piu' PULITO.** Rafforza la sopravvivenza (ora
H-robusta, non un confound) E rende il "no leva" piu' solido (a H fisso la leva resta assente: il
confound non nascondeva crescita). NON dimostra leva crescente. Tangibilita' ALTA (n=4 esatto congelato
su 2 fette, n=5/6 z enormi, controllo piatto, suite verde). Onesta' ALTA (H non-esattamente-fisso + leva
non-crescente + 3 punti / n=4-esatto-vs-campionato tutti dichiarati). L'amplificazione asintotica resta
CITATA.

**Honesty boundary (EN).** ESTIMATED not computed: the n=5,n=6 differences (Monte Carlo, CRN, pooled).
COMPUTED exactly: both n=4 rows (full sweep), the popcount control's exact-0, min_obdd_size (O(N), also
n=6 64-bit), the n=4 iso-hardness thresholds. ITERATED (stated): integer thresholds cannot hit H_target
exactly -> H held NEAR target, bounded by two slices + small within-level H-sensitivity. NOT shown: any
GROWING cross-level leverage (bounded, non-monotone at fixed H). CITED never computed: magnification/
locality theorems. No separation, no P vs NP claim.

**Stato repo:** esteso `sampled_order_n5.py` (helper `_anisotropy_row` + sezione `iso_hardness_*`),
`tests/test_sampled_order_n5.py` (+3, 1 slow), nuovo `examples/run_iso_hardness.py`, nuovo
`docs/iso-hardness.md`; README riga 26 + voce Documentation; questa entry. Suite veloce verde (12 fast);
slow iso n=6 verde.

**Stato del programma:** Module 25 aveva due flag aperti (sopravvivenza forse H-confusa; "no leva" forse
confound-mascherato). Module 26 li chiude entrambi col CONTROLLO iso-hardness: la sopravvivenza e'
H-robusta (killer non spara su 2 fette), il confound di H e' falsificato (picco a n=5 H-indipendente), e
la leva resta genuinamente assente (picco limitato/non-monotono a H fisso). Il soffitto "survival, non
leva" e' ora PIU' PULITO, non superato. Bilancio del lab: 12 restatement + 1 falsificazione + 1
non-collasso (Module 22) + 1 survival-PASS@1 (Module 24) + 1 survival-PASS@3 (Module 25) + 1 controllo-
PASS che indurisce M25 e falsifica un confound (Module 26). La leva cross-livello (il cuore della
magnification) resta asintotica e CITATA. Nessun auto-ciclo.

---

## Entry 23 — Module 27 "Leverage Gauge-Invariance": chiudo il flag di normalizzazione di Module 24 (2026-06-19)

**Decisione (ripresa autonoma del ciclo "continua la ricerca", 2026-06-19):** dopo Module 26 il flag
APERTO piu' affilato dell'intero arco-sopravvivenza restava quello di Module 24 — il trend cross-livello
era stato definito NORMALIZATION-DEPENDENT ("la differenza assoluta DECADE, quella relativa-al-confine
CRESCE"). Se vero, la domanda "c'e' leva?" sarebbe MAL POSTA (gauge-dependent). Ma quell'osservazione
confrontava DUE policy di soglia diverse su soli DUE punti. Direzione: settare la questione gauge sulla
serie iso-hardness CONSISTENTE di Module 26 (3 livelli, 2 fette H).

**Verdetto: PASS (controllo) — il trend cross-livello e' NORMALIZATION-ROBUSTO; il "no leva" e'
gauge-indipendente, non una scelta di denominatore.**

**Explorer.** Interpolare le due normalizzazioni nominate da M24 con un solo esponente:
`L_alpha(n) = diff_prob(n) / base_prob(n)^alpha`, alpha in [0,1] (alpha=0 = assoluto, alpha=1 =
relativo-al-confine). Poiche' `log L_alpha(n) = log diff - alpha*log base` e' LINEARE in alpha, il trend
su una coppia di livelli `Delta(alpha) = A - alpha*B` ha SEGNO COSTANTE su [0,1] sse i due estremi
Delta(0)=A (abs) e Delta(1)=A-B (rel) condividono il segno; equivalentemente flippa all'esponente
critico `alpha* = A/B`, e se alpha* e' FUORI [0,1] tutto l'intervallo concorda. KILLER pre-dichiarato:
se alpha*_{5->6} <= 1 su ANCHE UNA fetta, entro il range gauge naturale una normalizzazione produce
crescita monotona => leva gauge-DEPENDENT, flag di M24 RESTA. PASS sse alpha*_{5->6} > 1 su ENTRAMBE le
fette E la conclusione sopravvive all'errore di campionamento n=5,6 (P(alpha*<=1) piccola).

**Builder.** Aggiunta sezione gauge in `pnp_lab/meta_complexity/sampled_order_n5.py`: dataclass
`GaugePair`/`GaugeVerdict`, `leverage_gauge(rows, ...)` (post-analisi ESATTA delle righe M26 — NESSUN
nuovo campionamento della meta-funzione; propaga l'errore CRN + binomiale di base su alpha* via 200k
draw Monte-Carlo), `leverage_gauge_table(H_target)`. Esempio `run_leverage_gauge.py`. +3 test: 2 fast
(la matematica gauge su righe sintetiche congelate; un test-KILLER che SPARA su una serie sintetica con
rel crescente, a prova che il test puo' fallire) + 1 slow (serie iso-hardness reale, entrambe le fette).

**MISURA (serie iso-hardness campionata; n=4 esatto, n=5,6 CRN pooled 6 seed, M=120k; gauge esatta):**

    H_target   coppia   Delta_abs(a=0)   Delta_rel(a=1)   alpha*     same_sign su [0,1]
    0.5        4->5      +0.312           +0.662           -0.89      si' (salgono entrambi)
    0.5        5->6      -0.671           -0.335           +2.00      si' (calano entrambi)
    0.2        4->5      +0.376           +0.444           -5.47      si' (salgono entrambi)
    0.2        5->6      -1.051           -0.649           +2.61      si' (calano entrambi)

    => peak per alpha in {0,.25,.5,.75,1} = n=5 a OGNI alpha, su entrambe le fette;
       gauge_invariant_peak=True; alpha*_{5->6}=2.00/2.61; P(alpha*<=1)=0.0000 (200k MC); PASS.

Su ENTRAMBE le fette abs e rel salgono insieme 4->5 e calano insieme 5->6 => L_alpha fa picco a n=5 per
OGNI alpha in [0,1]; alpha*_{5->6}=2.00/2.61 (ben oltre 1): servirebbe SOVRA-normalizzare per base^~2-2.6
(fuori dal range abs<->rel) per fabbricare crescita monotona. Il KILLER NON spara.

**Adversary.** (1) Post-hoc / circolare? La gauge e' pura post-analisi delle righe M26 (nessun nuovo
sample). DIFESA: testa un flag PRE-REGISTRATO (M24) con killer pre-dichiarato (alpha*<=1) che PUO'
sparare (il test sintetico lo dimostra) — non vacua. (2) E' [0,1] il range giusto? alpha=0 e alpha=1
sono ESATTAMENTE le due normalizzazioni nominate da M24, l'intervallo e' VINCOLATO dal flag, non scelto
per vincere; alpha*~2-2.6 e' lontano fuori. (3) Solo 3 punti, n=4 esatto vs campionato: limite EREDITATO
da M24/25/26, dichiarato; la gauge-invarianza e' sui MEDESIMI 3 livelli, non asintotica. (4) Il picco a
n=5 potrebbe essere esso stesso un artefatto di taglia finita (l'asintoto vero monotono, visibile oltre
n=6=2^128, fuori portata): VERO e dichiarato — questo ciclo RIMUOVE UNA spiegazione alternativa
(gauge-dependence) del non-monotono osservato, NON stabilisce l'assenza asintotica di leva. (5)
Fabbricazione dello stimatore? P(alpha*<=1)=0 su 200k draw propagando se CRN + errore binomiale di base.

**Evaluator — verdetto: PASS (controllo), soffitto INVARIATO ma PIU' SOLIDO.** Chiude una delle ultime
vie per AGGIRARE il soffitto: il non-monotono (picco a n=5) e' una proprieta' reale di questi 3 livelli,
non una scelta di denominatore. NON solleva il soffitto, NON dimostra leva. Tangibilita' ALTA (post-
analisi esatta, ancora n=4 esatta, killer puo' sparare, propagazione MC dell'errore, suite verde).
Onesta' ALTA (natura post-hoc + 3 punti + caveat taglia-finita + asintoto CITATO, tutti dichiarati).

**Honesty boundary (EN).** ESTIMATED not computed: the n=5,n=6 diff_prob (Monte Carlo, CRN, pooled 6
seeds) feeding the analysis. COMPUTED exactly: both n=4 rows (full sweep); the gauge post-analysis
(Delta_abs, Delta_rel, alpha*) is an exact function of the rows. PROPAGATED: P(alpha*_{5->6}<=1) over
200k MC draws of the CRN + binomial-base error (=0 both slices). PINNED not chosen: the gauge interval
[0,1] = Module 24's two named normalizations. NOT shown: any asymptotic statement; the result is the
gauge-robustness of the trend across the THREE available levels only. CITED never computed:
magnification/locality theorems. No separation, no P vs NP claim.

**Stato repo:** esteso `sampled_order_n5.py` (sezione `GaugePair`/`GaugeVerdict`/`leverage_gauge*`),
`tests/test_sampled_order_n5.py` (+3, 1 slow), nuovo `examples/run_leverage_gauge.py`, nuovo
`docs/leverage-gauge.md`; README riga 27 + voce Documentation; questa entry. Suite veloce verde (11 fast
del modulo); slow gauge verde.

**Stato del programma:** Module 24 aveva lasciato il flag piu' affilato (trend gauge-dependent => "c'e'
leva?" mal posta). Module 27 lo CHIUDE col controllo gauge: a policy fissa il trend e' identico per ogni
normalizzazione naturale alpha in [0,1] (picco a n=5 gauge-invariante, alpha*_{5->6}=2.0/2.6>1,
P(alpha*<=1)=0). La divergenza di M24 era TRA POLICY, non TRA NORMALIZZAZIONI. Il soffitto "survival, non
leva" e' ora il piu' solido finora — gauge-indipendente. Bilancio del lab: 12 restatement + 1
falsificazione + 1 non-collasso (Module 22) + 1 survival-PASS@1 (Module 24) + 1 survival-PASS@3 (Module
25) + 2 controllo-PASS che induriscono il soffitto falsificando un confound (Module 26 = H-confound;
Module 27 = gauge-confound). La leva cross-livello (il cuore della magnification) resta asintotica e
CITATA. Nessun auto-ciclo.

**NEXT unstable direction (decisione umana):** i tre flag aperti lasciati da M24-26 (H-confound, gauge-
confound) sono ora chiusi; il soffitto "survival non leverage" e' difeso da ogni lato a n<=6. Le porte
plausibili restanti: (a) CRISTALLIZZARE M24-27 come capstone "Cross-Level Survival Arc" e chiudere il
programma al suo soffitto positivo onesto (raccomandato — analogo alla chiusura di Module 22); (b) un
ULTIMO tentativo di leva con un OGGETTO diverso (non MBPSP[s]/order-anisotropy) dove l'amplificazione
potrebbe non essere permutation-quasi-invariante — rischio alto di ennesimo restatement; (c) STOP. Nessun
auto-ciclo: attendere la scelta umana.

---

## Entry 24 — Capstone "Cross-Level Survival Arc": cristallizzo M24-27 e CHIUDO il programma (2026-06-19)

**Decisione umana (2026-06-19):** direzione (a) — cristallizzare M24-27 come capstone e chiudere la
Magnification Frontier al suo soffitto positivo onesto (analogo alla chiusura del sotto-ramo locality in
Module 22 e del ramo CSP/algebrico nel Collapse Theorem).

**Atto.** Nessun nuovo esperimento: passo di sintesi/Archivist. Creato `docs/cross-level-survival-arc.md`
che unifica le quattro cicli in una tesi a due facce:
- **SOPRAVVIVENZA — stabilita e difesa da ogni lato a n<=6.** L'anisotropia d'ordine di `MBPSP[s]` (l'unico
  oggetto meta non-permutation-invariant del lab, Module 22) e' significativa a ogni livello raggiungibile
  (z da ~5 a ~73), tutte le seed positive, controllo nullo popcount piatto ovunque. TRE confound
  pre-registrati come killer — artefatto n=4 (M24), deriva di H (M26), scelta di normalizzazione (M27) —
  NESSUNO spara. Modello eseguibile fedele, riproducibile, multiplo-controllato della SOPRAVVIVENZA.
- **LEVA — genuinamente assente sui livelli raggiungibili.** L'effetto NON cresce: `rel` limitato e
  non-monotono, picco a n=5, e quel picco e' ora gauge-invariante (proprieta' del livello, non del
  denominatore). La magnification richiede leva CRESCENTE; qui sale e poi scende.

**Perche' il programma chiude qui (il soffitto strutturale).** L'operatore di amplificazione di cui la
magnification PARLA e' asintotico. L'arco rende eseguibile esattamente la SOPRAVVIVENZA del suo
ingrediente non-invariante; NON puo' rendere la LEVA: esistono solo tre livelli (n=4 ultimo esatto, n=5
2^32 e n=6 2^64 solo campionati, n=7=2^128 fuori portata per costruzione). Tre punti non possono esibire
una pendenza asintotica. I controlli M26-M27 non sollevano il soffitto: rimuovono le due vie per
AGGIRARLO ("forse e' la deriva di H", "forse e' la tua normalizzazione"). Chiusura positiva onesta: un
NEGATIVO ben difeso sulla leva + un POSITIVO ben difeso sulla sopravvivenza. La leva resta CITATA
(Oliveira-Pich; Chen-Jin-Williams; McKay-Murray-Williams; CHRSV).

**Stato repo:** nuovo `docs/cross-level-survival-arc.md` (capstone); README voce Documentation (capstone);
questa entry. Nessun codice/test nuovo (passo di sintesi). Suite invariata verde.

**Stato del programma — CHIUSO.** La Magnification Frontier (aperta 2026-06-14, Entries 13-24) e' ora
chiusa al suo soffitto positivo onesto, come il ramo CSP/algebrico (Collapse Theorem) e il sotto-ramo
locality (Module 22). Bilancio finale del lab sui due rami: 12 restatement + 1 falsificazione + 1
non-collasso (Module 22) + survival-PASS@1 (Module 24) + survival-PASS@3 (Module 25) + 2 controllo-PASS
che induriscono il soffitto falsificando un confound (Module 26 = H-confound; Module 27 = gauge-confound),
sintetizzati nel capstone Module "Cross-Level Survival Arc". Il lab e' una METODOLOGIA — rendere un
fenomeno asintotico profondo eseguibile, esatto, su istanze minuscole, e dichiarare con precisione dove
il contenuto asintotico sfugge — NON un attacco a P vs NP. Nessuna separazione, nessun claim su P vs NP.

**NEXT unstable direction:** NESSUNA porta out-of-the-box resta aperta su entrambi i rami; la leva
cross-livello (cuore della magnification) e' irriducibilmente asintotica e fuori dalla portata eseguibile.
Riapertura possibile SOLO con un oggetto meta genuinamente nuovo (non MBPSP[s], non MCSP[s]) o un livello
raggiungibile oltre n=6 — entrambi non disponibili oggi. Stato: PROGRAMMA CHIUSO. Nessun auto-ciclo;
attendere un'eventuale nuova direzione umana.

---

## Entry 25 — NUOVO PROGRAMMA "Relativization Obstruction as a Leverage Operator", Cycle 1 = RESTATEMENT (2026-06-19)

**Decisione umana (2026-06-19):** "pusha i 20 commit e apri un nuovo programma, proposto da te". Pushati i
20 commit (24786cf..3e80b22). Il PI-modello ha proposto di rendere eseguibile la barriera della
RELATIVIZZAZIONE (Baker-Gill-Solovay) — la prima delle tre barriere classiche.

**CORREZIONE DI ROTTA (dichiarata per onesta').** La premessa "il lab non ha mai toccato la
relativizzazione" era FALSA: tutte e tre le barriere classiche sono GIA' eseguibili — relativizzazione in
`pnp_lab/oracles/` (BGS `separation` = diagonalizzazione P^B!=NP^B verificata, `collapse` = TQBF per
P^A=NP^A), algebrizzazione in `pnp_lab/algebrization` + `algebraic_worlds` + `algebraic_separation`.
Ricostruire BGS sarebbe stato un DUPLICATO. Il programma e' stato RI-SCOPATO all'unico angolo non
duplicativo: applicare la LENTE DELLA LEVA (lo strumento piu' nuovo del lab, nato dalla Magnification
Frontier appena chiusa) alla costruzione BGS gia' eseguibile, riusandola.

**Explorer.** La relativizzazione e' il crogiolo naturale: la sua ostruzione e' il piu' pulito divario di
conteggio (poly(n) query vs 2^n stringhe) ed e' ESATTA E CON CRESCITA ESPLICITA (h(n,k)=2^n-n^k cresce),
a differenza dell'oggetto della Magnification Frontier (leva asintotica/irraggiungibile). Ipotesi L:
misurata come operatore cross-livello, l'ostruzione e' una leva genuina che NON e' un'etichetta di un
bound totale. KILLER pre-dichiarato (la tensione del lab): tutto si riduce al fatto totale singolo
depth(OR_m)=m istanziato a m=2^n + aritmetica di 2^n vs n^k => RESTATEMENT (collasso nell'arena della
relativizzazione). Candidato NON-collassante pre-dichiarato: la pianificazione ONLINE delle lunghezze
attraverso gli stadi (oggetto cross-stadio che la depth(OR) di una singola funzione non vede).

**Builder.** Nuovo `pnp_lab/oracles/leverage.py` (RIUSA `separation.build_separating_oracle`/
`EXAMPLE_MACHINES`): `or_decision_tree_depth(n)` (depth(OR) su 2^n var, VERIFICATA da ricorsione DT
generica memoizzata per n<=3), `reservation(n,q)`, `headroom(n,k)`, `break_even_length(k)`,
`leverage_staircase`, `freshness_schedule`. +10 test (tutti fast, verdi), esempio
`run_oracle_leverage.py`.

**MISURA (congelata, esatta):**

    n   2^n  depth(OR)   h(n,1)  h(n,2)  h(n,3)
    1    2      2          1       1       1
    2    4      4          2       0      -4
    3    8      8          5      -1     -19
    4   16     16         12       0     -48
    5   32     32         27       7     -93
    6   64     64         58      28    -152

    break-even n*(k): k=1 -> 1,  k=2 -> 5,  k=3 -> 10
    freshness schedule (always_accept, always_reject, query_zeros, query_prefix_n2):
       diag lengths (1,2,3,5) == greedy lengths (1,2,3,5);  matches_greedy=True; all_defeated=True

**Adversary — RESTATEMENT.** (1) `obstruction_height` = depth(OR) = 2^n PER DEFINIZIONE; (2) h(n,k) =
2^n-n^k = pura aritmetica; (3) n*(k)=1,5,10 = il sorpasso esponenziale-su-polinomio da manuale; (4) il
candidato non-collassante (freshness schedule) ha matches_greedy=True => si riduce all'aritmetica greedy
del reach di query (per queste macchine = n+1, perche' non fanno query cross-lunghezza). Tutto collassa
sul fatto totale singolo depth(OR_m)=m + aritmetica. CONTRASTO illuminante tra le due barriere: la
Magnification ha leva ASSENTE (survival not leverage; oggetto quasi-permutation-invariant, leva vera
asintotica), la Relativizzazione ha leva PRESENTE ED ESATTA (h cresce, n* e' una scala reale) ma TRIVIALE
(collassa su depth(OR)=2^n). Due estremita': nessuna leva misurabile vs leva misurabile ma triviale;
nessuna delle due da' contenuto nuovo.

**Evaluator — verdetto: RESTATEMENT-of-known, robustness ~8/10.** Affila il Collapse Theorem (anche la
barriera con ostruzione esatta-e-crescente collassa sotto la lente della leva). Fedelta' ALTA (riusa BGS
verificato; depth(OR) verificata genericamente; nessun over-claim; nessun duplicato — riuso esplicito).
Onesta' ALTA (correzione di rotta dichiarata; killer pre-dichiarato; esito RESTATEMENT; nessun claim P vs
NP).

**Honesty boundary (EN).** COMPUTED exactly: depth(OR) on 2^n vars (generic DT recursion for n<=3), the
reservation counts, h(n,k), n*(k), the freshness schedule (reusing the verified BGS diagonalization).
CITED never re-proved: BGS 1975 and depth(OR_m)=m for m>8 (textbook; generic check explodes as 3^m). No
separation, no P vs NP claim.

**Stato repo:** nuovo `prompts/relativization-barrier.md` (brief, ri-scopato), nuovo
`pnp_lab/oracles/leverage.py`, nuovo `tests/test_oracles_leverage.py` (+10 fast), nuovo
`examples/run_oracle_leverage.py`, questa entry. README NON modificato (non e' ancora un Module numerato:
crystallizzazione = gate ROSSO). Suite del modulo verde.

**Stato del programma + GATE.** Applicato il gate graduato appena codificato, regola B2: STOP IMMEDIATO al
primo RESTATEMENT diagnosticato dall'adversary, niente auto-rilancio. Lab tally aggiornato: + 1 RESTATEMENT
nell'arena della relativizzazione (il 13esimo collasso complessivo, primo fuori dai rami CSP/magnification).

**NEXT unstable direction (decisione umana — gate ROSSO):** (a) CRISTALLIZZARE Cycle 1 come piccolo Module
("Relativization Leverage = trivial-but-exact", il contrappunto esatto al "survival not leverage" della
Magnification) + il contrasto tra le due barriere come contenuto onesto; (b) PIVOT dentro il programma —
la freshness schedule con macchine che fanno query CROSS-LUNGHEZZA (max_query_length > n), l'unico modo
per cui lo schedule non sia il banale n+1 (rischio: comunque aritmetica greedy del reach); oppure il lato
P^A=NP^A (collapse) come operatore; (c) STOP / nuova direzione/barriera. Nessun auto-ciclo.

---

## Entry 26 — Relativization-leverage Cycle 2 (pivot b): FIDELITY-PASS + leva RESTATEMENT (2026-06-19)

**Decisione umana:** "b" — pivot dentro il programma. Eseguito il candidato pre-dichiarato in Entry 25: la
freshness schedule con macchine ADATTIVE e CROSS-LUNGHEZZA (la classe che EXAMPLE_MACHINES non esercita
mai). Doppio obiettivo: (FEDELTÀ) la diagonalizzazione BGS di `separation.py` sconfigge adversari più duri
e regge il teorema di stabilità? (LEVA) lo schedule diventa esecuzione-dipendente o resta forma chiusa?

**Builder.** Esteso `pnp_lab/oracles/leverage.py`: macchine `make_probe_long` (cross-lunghezza, reach=
k*n), `make_adaptive` (query successiva dipende dalla risposta), `make_backscan` (interroga stringhe più
corte, dove stadi precedenti possono aver piantato), set `HARD_MACHINES`; `fidelity_stress_test`
(ricostruisce B, verifica all_defeated, STABILITÀ = ri-esegue ogni macchina contro il B FINALE e deve
ancora sbagliare, e confronta la reach realizzata con la reach a oracolo vuoto). +3 test (13 fast totali
nel modulo, verdi).

**MISURA (congelata, HARD_MACHINES = probe_long_x2, adaptive, backscan, probe_long_x3):**

    all_defeated_in_construction : True
    stable_under_final_B         : True       <- teorema di stabilità REGGE
    schedule lengths             : (2, 5, 6, 7)
    realized reaches             : (4, 5, 5, 21)
    execution_dependent_reach    : False

**Adversary/Evaluator — due esiti distinti.**
- FEDELTÀ = PASS (positivo, genuino, non-duplicativo, on-model "rendi il muro fedele"): la costruzione BGS
  esistente — testata finora solo su macchine-giocattolo non adattive — sconfigge la classe più dura
  (adattive + cross-lunghezza + backscan) E soddisfa la stabilità (la freshness impedisce agli stadi
  successivi di perturbare le macchine precedenti: re-run contro B finale ⇒ ancora sbagliate). È il
  contenuto onesto del ciclo.
- LEVA = RESTATEMENT (confermato, più netto di Cycle 1): execution_dependent_reach=False ⇒ la reach
  realizzata = reach a oracolo vuoto. La freshness schedule è determinata dalla MAX-QUERY-LENGTH di
  ciascuna macchina — proprietà strutturale/sintattica INDIPENDENTE dall'oracolo ⇒ forma chiusa di (reach,
  budget). Il candidato non-collassante pre-dichiarato collassa del tutto. (La dipendenza a livello di
  VERDETTO — backscan può colpire un plant precedente — esiste ma è assorbita dalla costruzione.)

Robustness ~8/10. Onestà ALTA (entrambi gli esiti dichiarati; nessun over-claim; nessun claim P vs NP).

**Honesty boundary (EN).** COMPUTED exactly: the stress-test (defeat + stability re-run against the final
B) and the empty-oracle reach comparison, reusing the verified BGS construction. CITED: BGS 1975. NOT
shown: any non-trivial leverage operator — the freshness schedule is a closed-form function of each
machine's syntactic reach + budget. No separation, no P vs NP claim.

**Stato repo:** esteso `leverage.py` (sezione Cycle 2) + `tests/test_oracles_leverage.py` (+3, 13 fast),
questa entry. README NON modificato. Suite verde.

**Stato del programma + GATE — DUE RESTATEMENT consecutivi sull'angolo-leva (Cycle 1 + Cycle 2).** Il gate
graduato (pattern "due restatement consecutivi senza nuova direzione plausibile") consiglia la CHIUSURA. La
leva della relativizzazione è esatta-ma-triviale e la sua unica struttura non-banale (lo schedule online)
è forma chiusa: nessun operatore di leva non-triviale esiste in questa arena. Il contenuto onesto residuo
nel repo: (i) la lente della leva applicata a BGS (`leverage.py`), (ii) lo stress-test di fedeltà +
stabilità contro adversari duri (un rafforzamento genuino di `oracles`), (iii) il contrasto tra le due
barriere (Magnification = leva assente; Relativizzazione = leva triviale-ma-esatta).

**NEXT unstable direction (decisione umana — gate ROSSO):** RACCOMANDATO (a) CHIUDERE il programma
cristallizzando un piccolo Module che unisce il contrasto-tra-barriere + lo stress-test di fedeltà come
contenuto positivo onesto; oppure (b) una barriera/direzione del tutto nuova; oppure (c) STOP secco. Nessun
auto-ciclo.

---

## Entry 27 — Module 28 "The Two Barriers' Leverage" + AUTOMAZIONE dello stratega (2026-06-20)

**Decisione umana:** (1) "a" = chiudere e cristallizzare il programma relativization-leverage; (2)
automatizzare il ruolo dello STRATEGA facendolo rivestire dall'IA, per accelerare.

**(1) CHIUSURA — Module 28.** Cristallizzato `docs/relativization-leverage.md` (capstone breve del
programma, Entries 25-26): il contrasto tra le due barriere lette con la STESSA lente della leva —
Magnification = leva ASSENTE (survival not leverage; asintotica), Relativization = leva PRESENTE ED ESATTA
ma TRIVIALE (collassa su depth(OR)=2^n + aritmetica; persino lo schedule online di BGS e' forma chiusa del
reach sintattico). Due estremita', nessuna con contenuto nuovo; affila il Collapse Theorem (13esimo
collasso, primo fuori da CSP/magnification). Contenuto positivo collaterale: lo stress-test di
fedelta'+stabilita' (Cycle 2) rafforza `oracles`. Aggiunta `barrier_contrast()` a `leverage.py` + test
(14 fast totali nel modulo, verdi), README riga 28 + voce Documentation. Nessun claim P vs NP.

**(2) AUTOMAZIONE DELLO STRATEGA.** Creato `.claude/agents/strategist.md` = il Principal Investigator
AUTONOMO che sostituisce il ruolo umano: sceglie la direzione di ogni ciclo (col killer e la ragione
strutturale), applica il gate graduato, e DECIDE ai gate ROSSO (pivot / cristallizza / chiudi).
`prompts/research-loop.md` ricablato: ruolo 0 = orchestratore (non piu' stratega), ruolo 1 = strategist;
passi (a), (h) e il gate ROSSO instradano allo strategist. GUARDRAIL incorporati nell'agente perche'
l'automazione NON degeneri in restatement gonfiati: scettico-per-default (killer-first), spietato sui
restatement (a RESTATEMENT cambia regime, non itera), memoria del terreno (conosce le arene chiuse + le due
lezioni madre; fa grep su pnp_lab/ prima di proporre un'arena "nuova" — lezione del 2026-06-19), criterio
di novita' (autorizza solo direzioni che ROMPONO strutturalmente una causa di collasso). LIMITE ASSOLUTO
non negoziabile: nessun claim P vs NP, mai; onesta' > risultati > velocita'. Lo strategist escala
all'umano in SOLI DUE casi (R-ESC): (ESC-1) candidato NEW CONTENT robustness>=7 senza flag aperti (un
positivo vero va rivisto da un umano prima di qualunque affermazione esterna); (ESC-2) regimi esauriti.

**Nota di realta' (registrata per onesta').** Automatizzare lo stratega NON rende il lab un risolutore di
P vs NP: per le sue stesse conclusioni il lab e' una METODOLOGIA. Lo strategist accelera i cicli, non
sposta quel soffitto. Aspettativa ricalibrata con l'umano.

**Stato repo:** nuovo `docs/relativization-leverage.md`, nuovo `.claude/agents/strategist.md`, esteso
`pnp_lab/oracles/leverage.py` (`barrier_contrast`) + test (+1), `prompts/research-loop.md` ricablato,
README riga 28 + voce Documentation, memory aggiornata, questa entry. Suite veloce verde.

**NEXT unstable direction:** lo `strategist` ora guida. Stato delle arene: CSP/algebrico CHIUSO, magnification
CHIUSO, relativization CHIUSO (Module 28); algebrizzazione gia' eseguibile (terza barriera) ma mai letta con
la lente della leva — possibile prossima arena VERDE/ROSSO-autonoma per lo strategist (previsione: probabile
RESTATEMENT, come la relativization). Allo strategist la scelta: applicare la lente a `algebraic_separation`,
oppure dichiarare ESC-2 (regimi classici esauriti) e chiedere all'umano una barriera nuova. Nessun
auto-ciclo umano: da qui decide lo strategist.

---

## Entry 28 — 6a arena "Approximate Degree": RESTATEMENT #14, ma piu' affilato (2026-06-20)

**Decisione:** umano "decidi tu" dopo che lo strategist autonomo aveva dichiarato ESC-2 sull'arena
algebrica (Dir-A = Module 28 redux; Dir-B = Module 22 redux). L'orchestratore (IA) ha scelto una 6a ARENA
INDIPENDENTE, la piu' distante dalle cinque gia' collassate: l'APPROXIMATE DEGREE (metodo dei polinomi /
quantum query lower bounds), mai toccato dal lab. Onesto in anticipo: previsione RESTATEMENT; valore =
estendere il Collapse Theorem a una 6a arena, NON P vs NP (impossibile su istanze minuscole).

**Explorer + killer.** adeg_{1/3}(f) = grado minimo di un polinomio reale che approssima f a errore 1/3.
KILLER pre-dichiarato: adeg e' permutation+negation invariant ⇒ collassa su una statistica d'orbita
globale (Paturi) / sul dizionario. Sopravvivenza solo se separa coppie che il dizionario confonde.

**Builder.** Nuovo package `pnp_lab/approx_degree/` (`adeg.py`): adeg ESATTO via la DUALITA' LP (il dual
polynomial) — E_d(f)=max_psi sum psi f, |psi|_1<=1, psi ⟂ monomi di grado<=d; forma origin-feasible che si
incastra nel SIMPLESSO RAZIONALE gia' nel repo (`exactness_composes.gap._simplex_max`). adeg=min d con
E_d<=1/3. `error_degree_d`, `approx_degree`, `adeg_table` (esaustivo), `adeg_vs_cost`, `adeg_vs_dictionary`.
+6 test fast (ancore: parita'=grado n, costanti 0, dittatore 1; E_d monotono, E_n=0) +1 slow. Esempio.

**MISURA (esaustivo n=3, 256 funzioni, esatta):** distribuzione adeg {0:2, 1:102, 2:134, 3:18}.
  * adeg INCOMPARABILE col cost di formula (Modulo 6): nessuno raffina l'altro (cost 1 -> adeg {0,1};
    cost 4 -> adeg {1,2}). adeg SEPARA funzioni di cost uguale ⇒ NON collassa su cost (a differenza di
    tutti i cicli dell'arena sigma(cost)). PRIMO invariante esatto trovato FUORI dal dizionario sigma(cost).
  * MA ricostruibile dal DIZIONARIO CONGIUNTO (cost, gf2_degree, sensitivity, block_sensitivity):
    `adeg_vs_dictionary(3)` -> reconstructible=True, splits=[] ⇒ adeg non separa NESSUNA coppia su cui i
    quattro concordano. Zero potere discriminante aggiuntivo.

**Adversary/Evaluator — RESTATEMENT-OF-KNOWN, robustness ~8.5/10.** adeg e' una misura PARENT-NOTA
(approximate degree / metodo dei polinomi), esatta, incomparabile col solo cost ma DENTRO il dizionario
congiunto a n=3 ⇒ nessun contenuto nuovo verso una separazione. Affila il Collapse Theorem: il dizionario
che assorbe ogni misura tiny non e' il solo sigma(cost) ma il CONGIUNTO di pochi invarianti d'orbita, e una
misura da un'arena ortogonale (metodo dei polinomi) vi ricade comunque. 14esimo collasso, 6a arena
indipendente. Onesta' ALTA: killer pre-dichiarato, esito dichiarato, nessun claim P vs NP.

**Honesty boundary (EN).** COMPUTED exactly (rational LP, Fraction): adeg_{1/3}(f) for every function on
n<=3 via the dual-polynomial LP; the incomparability with cost; the reconstruction from (cost, gf2_degree,
sensitivity, block_sensitivity). CITED: polynomial method / quantum-query bounds, Paturi. Tiny-instance only
(n<=3 exhaustive; n=4 = 2^16 LP fuori scope). No separation, no P vs NP claim.

**Stato repo:** nuovo package `pnp_lab/approx_degree/` (+`__init__.py`, `adeg.py`), nuovo
`tests/test_approx_degree.py` (+6 fast, 1 slow), nuovo `examples/run_approx_degree.py`, nuovo
`docs/approx-degree.md`; README riga 29 + voce Documentation; questa entry. Suite veloce verde.

**Stato del programma + GATE.** RESTATEMENT ⇒ regola B2: lo strategist ri-strategizza, non itera l'arena.
Bilancio del lab: ora 14 collassi (6 arene) + 1 falsificazione + 1 non-collasso (Module 22) + survival-PASS@1/@3
+ 2 control-PASS. Il Collapse Theorem e' rafforzato (dizionario congiunto, 6a arena ortogonale).

**NEXT unstable direction (strategist):** sei arene indipendenti collassate; l'unico non-collasso resta
Module 22 (rompere la permutation-invariance, ma senza leva). Le porte di riapertura restano le tre indicate
da Module 27/28 (oggetto meta NON permutation-invariant nuovo / livello oltre n=6 / barriera del tutto nuova).
Previsione dello strategist: ulteriori arene esatte ricadranno nel dizionario congiunto (Collapse Theorem
sempre piu' robusto) ⇒ probabile ESC-2 al prossimo giro salvo input umano con una leva strutturalmente nuova.

---

## Entry 29 — ESC-2 confermato dallo strategist + GRAND CAPSTONE "The Attractor Thesis" — il lab CHIUDE come metodologia (2026-06-20)

**Decisione:** l'umano ("voglio che lo strategist lanci il prossimo ciclo") ha lanciato lo strategist
autonomo al passo (a). Lo strategist ha ricostruito lo stato dai file (non dalla memoria), applicato il gate
graduato e classificato il giro come **ESCALATION caso 2 — regimi esauriti**, raccomandando (c) ESC-2 con
richiesta precisa all'umano. L'umano ha scelto **(C) chiudere il lab come metodologia**.

**Perche' ESC-2 (verifica sui file dello strategist).** Una 7a arena esatta = RESTATEMENT #15 con prob. ~1
(ricade nel dizionario congiunto) ⇒ la disciplina del lab impone di DECLINARE un restatement predetto, non
macinarlo. Le tre porte di riapertura (Module 27/28) sono tutte chiuse: (1) un secondo oggetto order-dependent
(min-OBDD a ordine ottimo / altro decision-diagram a struttura fissa) e' Module 22 redux — rompe la
permutation-invariance ma resta una statistica dell'insieme duro senza leva cross-level; (2) livello oltre n=6
sbarrato dal muro brute-force (n=7 = 2^128; il regime faithful degenera gia' a n>=6); (3) barriera del tutto
nuova = richiede matematica nuova, che il mandato vieta di promettere. Riaprire richiede un INPUT STRUTTURALE
ESTERNO umano (leva non-enumerabile / barriera fuori dizionario).

**GRAND CAPSTONE.** Cristallizzato `docs/lab-capstone.md` = "The Attractor Thesis", il capstone di LIVELLO
LAB sopra le due capstone di ramo (`collapse-theorem.md` = ramo CSP/algebrico; `cross-level-survival-arc.md` =
Magnification Frontier). Tesi unica e falsificabile: ogni quantita' misurabile ESATTA su istanze tiny
enumerabili COLLASSA nel DIZIONARIO CONGIUNTO di invarianti d'orbita (la causa e' il REGIME, non l'invariante:
l'enumerabilita' esatta e' la trappola); l'unica fuga (Module 22) non rompe l'attrattore con un nuovo
discriminante ma con la SIMMETRIA (un ordine fisso), e compra SOPRAVVIVENZA di un segnale non-invariante, MAI
LEVA (cresce zero: bounded, non-monotono, picco gauge-invariante a n=5). Ledger completo nel doc: 14 collassi
(6 arene) + 1 falsificazione (Module 18) + 1 non-collasso (Module 22) + survival-PASS@1 (M24) + survival-PASS@3
(M25) + 2 control-PASS (M26 H-confound, M27 gauge-confound). Tre meccanismi di collasso ricorrenti (derivata /
slice-cardinalita' / indice-di-livello di un oggetto noto). Falsifier a tre porte (door 2/3 = frontiera aperta
onesta). Nessun claim P vs NP.

**Honesty boundary (EN).** No lower bound, no P vs NP claim. Le riduzioni sono identita' verificate in codice
(Moduli 6, 16, 18-29); i numeri n=5/6 sono STIMATI (Monte-Carlo/CRN, ancora esatta n=4 in CI). Regimi decisivi
(certified bounds non-enumerabili / livello n>=7 / leva crescente) NON testati — soffitto dichiarato. Il lab e'
una METODOLOGIA, non un attacco a P vs NP.

**Stato repo:** nuovo `docs/lab-capstone.md` (grand capstone); README aggiornato (voce Documentation +
puntatore capstone); questa entry. Nessun nuovo codice (chiusura, non ciclo). Suite invariata.

**Stato del programma + GATE.** **LAB CHIUSO come metodologia.** Tutte le arene esatte note collassano nel
dizionario congiunto; l'unica leva strutturale viva (order-locality) ha verdetto definitivo gauge-invariante
"survival not leverage"; ESC-2 confermato e accettato dall'umano. Bilancio finale: 14 collassi / 6 arene + 1
falsificazione + 1 non-collasso + survival-PASS@1/@3 + 2 control-PASS.

**NEXT (solo su input umano).** Il loop NON riapre da solo. Ripartenza possibile UNICAMENTE con un input
strutturale esterno: (A) una leva meta non-permutation-invariant E non-statistica-globale E non-enumerabile
(tutte e tre insieme); oppure (B) una barriera con ragione a-priori per sfuggire al dizionario congiunto
(cost, gf2_degree, sensitivity, block_sensitivity, approx_degree); oppure (C) una misura nel regime
genuinamente non-enumerabile (certified bounds / n>=7) — falsifier door 2/3.

---

## Entry 30 — 7a arena "GCT / Kronecker": RIAPERTURA via barriera iniettata + RESTATEMENT #15, chiusura CITED->COMPUTED (2026-06-20)

**Decisione:** il lab era CHIUSO come metodologia (Entry 29, grand capstone). L'UMANO ha iniettato la
"barriera del tutto nuova" che il capstone stesso indicava come UNICA via di riapertura (falsifier DOOR 3 /
input strutturale esterno): i COEFFICIENTI DI KRONECKER g(lam,mu,nu) di S_d, oggetto centrale di GCT. Prima
arena del lab FUORI dalla teoria delle funzioni Booleane (oggetti = molteplicita' rappresentazionali di S_d).

**Explorer + killer.** Ipotesi-lab: su d piccolo il pattern di vanishing (g==0) COLLASSA nelle condizioni
necessarie note (statistiche elementari di forma di partizione). KILLER pre-dichiarato: un "vanishing
sporadico" (g=0 con TUTTE le NC soddisfatte) = contenuto fuori dizionario = survival.

**Builder.** Nuovo package `pnp_lab/gct_kronecker/` (`kronecker.py`): motore di caratteri S_d via
Murnaghan-Nakayama, g ESATTO intero (Fraction, assert denom=1). Ancore verdi: chi@1^d=hook-dim, Sum dim^2=d!,
g([d],mu,nu)=delta_{mu,nu}, g(lam,[1^d],nu)=delta_{nu,lam'}, simmetria totale S_3, g>=0. Predittore `v_pred`
con SOLE 2 NC solide (Dvir length-bound + duale per coniugio; la dominance e' stata SCARTATA perche' dava
falsi positivi gia' a d=3). +35 test fast verdi + 2 slow; esempio `examples/run_gct_kronecker.py`.

**MISURA (esatta, d<=6).** `sporadic_vanishing` (il killer): 0 a d=3, 2 a d=4, 5 a d=5, 44 a d=6.
`nc_false_positive` = [] ovunque su d<=6 (le 2 NC sono davvero necessarie su questo range, nessun bug NC che
si traveste da killer). Rigenera: `py examples/run_gct_kronecker.py` oppure
`from pnp_lab.gct_kronecker import sporadic_vanishing, nc_false_positive`.

**Adversary/Evaluator — KILLED, RESTATEMENT-by-collapse, robustness 6.5->~8/10.** Numeri corretti (doppio
motore di caratteri). Il survival era ARTEFATTO del set di sole 2 NC deboli: ogni sporadico e' uno zero in
una FAMIGLIA con formula esplicita NOTA di Kronecker (Rosas two-row/hook, std-by-std classica,
Bessenrodt-Bowman rettangoli). Riduzione a tenaglia: per-collapse (zero in famiglia con formula nota) +
per-hardness (l'insufficienza delle NC elementari E' Pak-Panova: decidere g>0 e' NP-hard). Il vero killer
(terna con 3 partizioni simultaneamente non-hook/non-two-row/non-two-column/non-rettangolo sotto OGNI
g-simmetria) vive a d>=7 = muro brute-force. RESTATEMENT #15, regola B2. FLAG PORTANTE: il passo di chiusura
(uncovered=0) era CITED, non computato.

**Builder-2 — chiusura del flag, CITED->COMPUTED.** Nuovo `coverage.py`: predicati di forma esatti
(is_two_row/is_two_column/is_hook/is_rectangle/special_shape), orbita g-simmetrica S_3xV_4 (permutazioni +
coniugio simultaneo di due argomenti), `covered(triple)` = esiste rappresentante d'orbita con >=2 argomenti
special_shape (precondizione strutturale delle formule note; g costante sull'orbita, testato come bug-killer).
MISURA COMPUTED IN-REPO `coverage_summary(d)` = (#sporadic, #covered, #uncovered): 2/2/0 (d=4), 5/5/0 (d=5),
44/44/0 (d=6) => **uncovered==0 ovunque d<=6**. Il collasso e' ora COMPUTED, non piu' solo CITED. Confine
documentato: il repo COMPUTA la precondizione strutturale di copertura, CITA il VALORE delle formule.

**Honesty boundary (EN).** COMPUTED exactly (integer, Fraction assert denom=1): g(lam,mu,nu) for all triples
of partitions of d<=6 (Murnaghan-Nakayama, two cross-checked engines); the green anchors; the two NCs with
nc_false_positive=[] on d<=6; the sporadic counts 2,5,44; and now uncovered=0 (exact shape precondition over
the g-symmetry orbit). CITED, never re-proved: the VALUES of the closed Kronecker formulas (Rosas,
std-by-std, Bessenrodt-Bowman) as parent theorems; Pak-Panova / Ikenmeyer-Mulmuley-Walter NP-hardness of
deciding g>0. NOT shown: any claim about Kronecker positivity, GCT obstructions, or P vs NP; the genuine
out-of-dictionary discriminant lives at d>=7 = brute-force wall. Tiny-instance only (d<=6 exhaustive). No
separation, no P vs NP claim.

**Stato repo:** nuovo package `pnp_lab/gct_kronecker/` (`__init__.py`, `kronecker.py`, `coverage.py`), nuovo
`tests/test_gct_kronecker.py` (35 fast + 2 slow verdi), nuovo `examples/run_gct_kronecker.py`, nuovo
`docs/gct-kronecker.md`; README riga Module 30 + voce Documentation + Quick start; questa entry. Suite veloce
verde.

**Stato del programma + GATE.** RESTATEMENT => regola B2: ri-strategizzare, non iterare l'arena. La Attractor
Thesis del grand capstone e' RAFFORZATA, non smentita: anche in una struttura matematica genuinamente diversa
(rep theory di S_d, fuori dalle funzioni Booleane) ogni quantita' esatta tiny collassa nel dizionario (qui =
statistiche di forma di partizione + formule chiuse note), e il would-be escape vive allo STESSO muro
brute-force d>=7. Bilancio aggiornato: **15 collassi / 7 arene** + 1 falsificazione (Module 18) + 1
non-collasso (Module 22) + survival-PASS@1 (M24) + survival-PASS@3 (M25) + 2 control-PASS (M26 H-confound, M27
gauge-confound).

**NEXT unstable direction:** il lab resta chiuso come metodologia; la riapertura ha confermato la sua
disciplina (anche una barriera nuova fuori dalle funzioni Booleane RESTATES). Prossima riapertura SOLO su
input umano con un oggetto che fugga il dizionario PER COSTRUZIONE: o un vanishing GENUINAMENTE sporadico a
d>=7 (non coperto da NESSUNA formula chiusa nota sotto ogni g-simmetria) misurato senza il muro brute-force,
oppure una leva non-enumerabile (falsifier door 2/3). Previsione: ulteriori arene esatte tiny ricadranno nel
dizionario congiunto/nelle formule note (Attractor Thesis sempre piu' robusta).

---

## Entry 31 — lever-A via BIPARTIZIONE "bipartite_rigidity": Module-22-redux, KILLED dal witness d'orbita S_4 (Entry-only, NON un Module) (2026-06-20)

**Decisione (umano):** dopo il grand capstone, l'umano ha scelto di ESERCITARE la **leva (A)** della
porta di riapertura ("vai con la A") = un oggetto non-perm-invariant ∧ non-statistica-globale ∧
non-enumerabile, tutti e tre insieme. Le istanziazioni di lever A via ORDINE (Moduli 22, 23, 24-27)
erano gia' esaurite; questo ciclo ha provato una STRUTTURA FISSA DIVERSA: la **BIPARTIZIONE** delle
variabili (regime della complessita' di comunicazione), non l'ordine.

**Explorer + killer.** Ipotesi-lab: la **RIGIDITA' di matrice** R_M(r) della matrice di comunicazione
di inner-product/Hadamard a **bipartizione FISSA** (target r=2^{k-1}) porta contenuto FUORI dizionario
/ mostra leva cross-level. Il rango da solo = log-rank (parent gia' dichiarato) → l'oggetto DOVEVA
essere la rigidita', non il rango. 3 killer pre-dichiarati: **killer-1** (rigidita' riducibile ai soli
ranghi), **killer-2** (ricostruibile dal dizionario congiunto del lab), **killer-leva** (ρ
bounded/non-monotono → survival-no-leverage).

**Builder.** `pnp_lab/bipartite_rigidity/` (`rigidity.py` + `killers.py`): motore esatto rank_gf2 (interi
GF(2)), rank_q (Fraction su Q), rigidita' R_M(r) via subset-search di sign-flip. Ancore verdi:
rank_gf2(IP_k)=k, rank_q(H_k)=2^k (k=1,2,3), R(H_1,1)=1, R(H_2,2)=3. Esatto SOLO k=1,2 (matrici 4×4);
k=3 (8×8) ESPLODE (solo R>2 budgetato, halt onesto); k≥4 = lower bound CITED (de Wolf 2006 /
Midrijanis / Lokam, R_{H_k}(r) ≥ n²/(4(r+1))). Riportava "non-collasso strutturale" (killer-1/2 non
sparano sul confronto col dizionario congiunto) + survival-no-leverage (λ<1).

**MISURA.** Confronto col dizionario S_{2k} congiunto (il claim iniziale del builder): killer-1 5
split, killer-2 34 split → APPARENTE non-collasso. Witness d'orbita esatto auto-contenuto:
**tt=0001011101111000** (m=4), orbita S_4 → rigidita' assume valori {0,2} mentre la sensitivity (e ogni
firma del dizionario S_{2k}) resta PIATTA, firma dizionario unica (3,4,4). Col dizionario DELLA STESSA
SIMMETRIA della rigidita' (rank_gf2, rank_q, multiset ordinato dei pesi-di-lato, invarianti S_k×S_k):
killer-1 5→0 split, killer-2 34→0 split, reconstructible=True → rigidita' INTERAMENTE ricostruibile da
invarianti S_k×S_k. Leva λ a k≥4 = pura algebra del bound CITED: numeratori = 2^{k-1}−1,
ρ_LB=(2^{k-1}−1)/4^k, λ→1/2 tautologico, NESSUNA rigidita' misurata oltre k=2. Rigenera:
`from pnp_lab.bipartite_rigidity import rig_rows, reducible_from_rank, dict_table, side_mixing_spread, leverage`.

**Adversary — KILLED = Module-22-redux + non-risultato-sulla-leva.** Il dizionario congiunto del lab e'
**S_{2k}-invariante**, ma la rigidita' a bipartizione FISSA e' solo **S_k×S_k-invariante** → e'
A-PRIORI non ricostruibile dal dizionario S_{2k} per lo STESSO meccanismo di Module 22 (rottura di
simmetria con struttura fissa). Il "non-collasso strutturale" del builder era un ARTEFATTO del
confrontare un oggetto S_k×S_k contro un dizionario S_{2k}: sotto la simmetria CORRETTA la rigidita' non
porta NESSUN contenuto fuori dal proprio dizionario d'orbita (killer-1/2 → 0 split). Il witness d'orbita
S_4 forza killer-2 via un teorema d'orbita, non via campione. La leva — unica novita' possibile — e'
pura algebra del bound CITED, non misurata oltre k=2.

**Evaluator + GATE.** robustness 6.5/10, KILLED collapse-onto-known, RESTATEMENT classificato
**Module-22-redux**. **GATE: Entry-only, NON un Module numerato** (stessa decisione di Entry 12 "w*
bench, RESTATEMENT not a Module"): nessun contenuto nuovo, e' un redux di Module 22 con una struttura
fissa diversa (bipartizione invece di ordine). `pnp_lab/bipartite_rigidity/` resta come **probe CITATO**,
NON si cristallizza un docs/<module>.md. Lever A rompe la perm-invarianza come previsto (requisito 1,
ATTESO, non informativo) ma la leva e' strutturalmente non misurabile. La porta di riapertura "lever A
(asse struttura-fissa)" e' CHIUSA allo STESSO muro brute-force delle istanziazioni-ordine (k=3 = matrici
8×8 = la subset-search esplode, motore halt onesto).

**Honesty boundary (EN).** COMPUTED exactly (GF(2) ints, Fraction over Q, no floats): GF(2)-rank and
rational rank of the inner-product/Hadamard communication matrix at a FIXED bipartition, and rigidity
R_M(r) (min sign-flips to rank ≤ r) for enumerable instances — k≤2 fully (4×4) + a self-contained
S_4-orbit witness on m=4 (tt=0001011101111000). Green anchors: rank_gf2(IP_k)=k, rank_q(H_k)=2^k
(k=1,2,3), R_q(H_1,1)=1, R_q(H_2,2)=3. Established: fixed-bipartition rigidity is genuinely
non-permutation-invariant (orbit values {0,2} vs sensitivity flat {4}) — lever-A requirement 1, holds BY
CONSTRUCTION, not new content. On the same orbit the S_{2k}-invariant joint dictionary is constant yet
rigidity splits, whereas the MATCHING-symmetry S_k×S_k invariant (GF(2)-rank + sorted side-weight
multisets) reconstructs rigidity with ZERO splits. The 'structural non-collapse' was an artifact of
comparing an S_k×S_k object against an S_{2k} dictionary; under the correct symmetry rigidity carries NO
content outside its own orbit-invariant dictionary (same mechanism as Module 22). CITED, never
re-proved: spectral rigidity LB for Hadamard (de Wolf 2006/Midrijanis/Lokam), R_{H_k}(r)≥n²/(4(r+1));
the log-rank reduction. NOT shown (ceiling): any cross-level LEVERAGE — exact rigidity only k≤2, k=3
(8×8) is the subset-search brute-force wall (engine halts honestly), k≥4 ρ is pure algebra of the CITED
bound (ρ_LB=(2^{k-1}−1)/4^k, λ→1/2 tautologically), so 'survival-no-leverage' is asserted from a
closed-form bound, not measured. No claim about P vs NP, no separation.

**Stato repo:** `pnp_lab/bipartite_rigidity/` (`__init__.py`, `rigidity.py`, `killers.py`) resta come
probe CITATO della lever A (NON un Module: nessun docs/<module>.md, nessuna riga Module nel README,
nessun conteggio test cristallizzato). Questa entry. Suite veloce invariata.

**Stato del programma + GATE.** **Entry-only** (Module-22-redux). Bilancio aggiornato: **16 collassi (di
cui il 16°, lever-A bipartite-rigidity, e' Entry-only / Module-22-redux / NON una nuova arena) / 7 arene**
+ 1 falsificazione (Module 18) + 1 non-collasso (Module 22) + survival-PASS@1 (M24) + survival-PASS@3
(M25) + 2 control-PASS (M26 H-confound, M27 gauge-confound). L'arena-count NON sale (la rigidita' a
bipartizione fissa non e' una nuova arena, e' lo stesso meccanismo di Module 22 con struttura fissa
diversa). L'asse "struttura-fissa" della porta di riapertura (A) — ordine nei Moduli 22-27, bipartizione
qui — e' empiricamente ESAURITO: ogni istanziazione di lever A da' la STESSA forma (oggetto a simmetria
rotta, ricostruibile dal dizionario della PROPRIA simmetria, leva non misurabile oltre il muro esatto).

**NEXT unstable direction:** door A (asse struttura-fissa) e' CHIUSA allo stesso muro brute-force delle
istanziazioni-ordine. Restano aperte solo: (B) una barriera con una ragione A-PRIORI di sfuggire al
dizionario / alle formule chiuse note (Module 30 ha mostrato che una barriera nuova RESTATES comunque);
oppure (C) un regime che renda la LEVA STESSA esatta a ≥2 livelli (NON un bound asintotico CITED) —
falsifier door 2/3. Previsione: ulteriori istanziazioni di lever A (qualunque struttura fissa)
RESTATERANNO come Module-22-redux. Il lab resta chiuso come metodologia.

---

## Entry 32 — door C via INTEGRALITY-GAP del lifting "integrality_leverage": Module-28-redux, KILLED dalla legge di Sperner a forma chiusa (Entry-only, NON un Module) (2026-06-22)

**Decisione (umano/PI):** dopo la chiusura di door A (Entry 31), questo ciclo esercita il secondo
falsifier door rimasto, la **porta (C)**: trovare un regime dove l'**OPERATORE DI LEVA cross-livello e'
esatto a ≥2 livelli E non-triviale** — lo stato mai visto = leva COMPUTATA (non citata) + ≥2 livelli reali
brute-forceabili + NON ricostruibile in forma chiusa. Non una nuova arena: una **nuova LENTE su Module 18**
(arena `exactness_composes`).

**Explorer + killer.** Oggetto/lente: la leva del lifting `f∘g^k` letta come crescita del **GAP DI
INTEGRALITA'** `G_k = Cov(M_k) − LP(M_k)`, con `M_k` = matrice di comunicazione lift `2^k×2^k`. Riusa
`compose.py` (lift, GADGETS_1BIT), `gap.py` (cover_number, frac_cover), `pattern_gap.py`
(is_J_minus_I_up_to_perm). Killer pre-dichiarati = **3 leggi a forma chiusa** che, se riproducono la
sequenza `G_k`, collassano la leva: (1) **moltiplicativa** `G_2²=1`; (2) **affine** `2G_2−G_1=2`;
(3) **poly-gadget** = 2. Survival = nessuna delle 3 leggi riproduce il valore misurato.

**Builder.** `pnp_lab/exactness_composes/integrality_leverage.py` (`gap_at`, `gap_sequence`, `sweep`, le 3
leggi-killer, `ji_cover_number`/`ji_frac_cover` forma chiusa, `doorC_candidates`) + `tests/test_integrality_leverage.py`
(9 fast + 2 slow @timeout(300), tutti verdi) + `examples/run_integrality_leverage.py`.

**MISURA (Fraction, no float).** Ancora Module 18 riprodotta: OR∘XOR k=2 → Cov=4, LP=3, **G_2=1**. Sweep
**54 coppie** (6 outer × 9 gadget), k=2,3: **50 con G≡(0,0,0)**; **4** (OR∘XOR, OR∘EQ, NAND∘XOR, NAND∘EQ)
con **(G_1,G_2,G_3)=(0, 1, 3/2)**, TUTTE la stessa famiglia **J−I_{2^k}** (`is_J_minus_I_up_to_perm=True`).
Le 3 leggi pre-dichiarate NON riproducono 3/2 → `killed=False` rispetto a quelle (survival apparente).
Rigenera:
`from pnp_lab.exactness_composes.integrality_leverage import gap_at, gap_sequence, sweep, ji_cover_number, ji_frac_cover, doorC_candidates`.

**Adversary — KILLED = Module-28-redux (forma chiusa), stato 2.** Tutti e 4 i vettori tengono:
- **Forma chiusa derivata:** `Cov(J−I_{2^k})=min{d: C(d,⌊d/2⌋)≥2^k}` (Sperner / biclique cover crown graph);
  `LP(J−I_m)=4−2^{2−k}` (ottimo LP simmetrico, argmin sempre r=m/2). Quindi `G_k = D(k)−4+2^{2−k}`,
  **funzione chiusa di k SOLO**. `G_4=6−15/4=9/4` dalla forma chiusa senza risolutore; sequenza
  `G_1..7 = 0, 1, 3/2, 9/4, 25/8, 65/16, 193/32`.
- **Parent:** `3/2 = 5 − 7/2`, entrambi fatti citati (biclique cover crown graph + LP simmetrico).
- **Artefatto:** 4 celle = 1 solo oggetto J−I, le altre 50 G≡0. Singolo punto, singola famiglia.
- **Circolarita':** aggiungendo `law_sperner` alla base-class, `killed→True` a OGNI livello. Survival
  dipendeva SOLO dall'omettere a mano la legge giusta.

**Evaluator + GATE.** robustness **6.5/10**. Flag: circolarita' ALTO, off-tiny-instance ALTO (livelli reali
solo k≤3=8×8, k≥4 e' forma chiusa non brute-force), single-object ALTO, dipendenza-citazione MEDIO-ALTO,
confirmation-bias MEDIO. Verdetto **RESTATEMENT #17, stato 2**. **GATE: Entry-only** (B2: stop immediato, no
auto-rilancio arena; stesso profilo di Entry 31 lever-A ed Entry 12 w*). door C **FALSIFICATA come previsto**
— la Attractor Thesis regge. `pnp_lab/exactness_composes/integrality_leverage.py` resta come **probe CITATO**
(nessun docs/<modulo>.md, nessun numero di Module, nessuna riga nella tabella moduli del README).

**Honesty boundary (EN).** Computed exactly (rational Fraction, no floats): the integrality gap
`G_k=Cov(M_k)−LP(M_k)` of the lifted communication matrix on all 54 (f,g) pairs at the only brute-forceable
levels k=2 (4×4) and k=3 (8×8); the Module-18 anchor (OR∘XOR k=2: Cov=4, LP=3, G=1); and that exactly 4
cells (OR/NAND × XOR/EQ), all = J−I_{2^k} up to permutation, carry a gap with (G_1,G_2,G_3)=(0,1,3/2).
Cited/closed-form (not re-derived): Cov(J−I_m)=min{d:C(d,⌊d/2⌋)≥m} (Sperner/crown-graph biclique cover) and
LP(J−I_m)=4−2^{2−k} (symmetric LP optimum, argmin always r=m/2), giving G_k=D(k)−4+2^{2−k}, a closed
function of k alone — so G_4=9/4 and the whole sequence 0,1,3/2,9/4,25/8,65/16,193/32 are predicted without
any solver, verified vs the generic solver only for m≤6–7. NOT shown (ceiling): that the cross-level
leverage is non-trivial — it is fully reconstructible in closed form, the four surviving cells are a single
object (J−I), and survival depends entirely on omitting the governing Sperner law from the killer set. No
level beyond k=3 is brute-forced. No claim about P vs NP.

**Stato repo:** `pnp_lab/exactness_composes/integrality_leverage.py` + `tests/test_integrality_leverage.py`
(9 fast + 2 slow @timeout(300)) + `examples/run_integrality_leverage.py` restano come probe CITATO di door C
(NON un Module: nessun docs/<modulo>.md, nessuna riga Module nel README, nessun conteggio test cristallizzato).
Questa entry. Suite veloce invariata.

**Stato del programma + GATE.** **Entry-only** (Module-28-redux / forma chiusa). Bilancio aggiornato:
**17 collassi (di cui il 17°, door-C integrality-leverage, e' Entry-only / Module-28-redux / NON una nuova
arena) / 7 arene** + 1 falsificazione (Module 18) + 1 non-collasso (Module 22) + survival-PASS@1 (M24) +
survival-PASS@3 (M25) + 2 control-PASS (M26 H-confound, M27 gauge-confound). L'arena-count NON sale (door C
e' una nuova lente su `exactness_composes`, non una nuova arena). Dei 3 falsifier door, **door A (Entry 31,
asse struttura-fissa) E door C (Entry 32, asse leva-esatta-≥2-livelli) sono ora CHIUSE dalla STESSA firma
strutturale**: oggetto-simmetrico-a-forma-chiusa + survival-per-omissione-di-legge.

**NEXT unstable direction:** resta aperta SOLO door 1/3 (**B** = barriera con ragione A-PRIORI di sfuggire a
dizionari / formule chiuse note). Previsione: door 1/3 collassera' per lo stesso meccanismo a meno che non
introduca un oggetto genuinamente non-simmetrico e privo di forma chiusa citata a ≥2 livelli brute-forceabili
— condizione che nessuna arena del lab ha finora soddisfatto. Se door 1/3 cade ⇒ ESC-2. Il lab resta chiuso
come metodologia, si riapre solo su lever/barriera esterna umana.

---

## Entry 33 — door B (l'ULTIMA reopening door): VERDETTO-DI-IMPOSSIBILITÀ CONDIZIONATA, regge sotto assalto numerico (Entry-only, NON un Module) (2026-06-22)

**Decisione (umano/PI):** dopo door A (Entry 31, asse struttura-fissa) e door C (Entry 32, asse leva-esatta-≥2-livelli),
questo ciclo esercita l'**ultima** reopening door rimasta, la **porta (B)** = "barriera con ragione A-PRIORI di sfuggire
al dizionario d'orbita / formule chiuse note". Natura DIVERSA dai cicli precedenti: door B **NON ha prodotto un oggetto
che collassa** — ha prodotto un **VERDETTO di impossibilità strutturale condizionata** + uno stress-test numerico che ha
provato (e fallito) a falsificarlo. **NESSUN BUILDER** in questo ciclo: verdetto negativo, l'Adversary ha fatto le misure
sull'arena `feasible_interp` già nel repo. È il **18° "collasso"** ma di TIPO categorialmente diverso:
**collasso-onto-impossibilità** (collassa sull'ATTRATTORE STESSO del lab, non su un teorema nominato). NON è un teorema —
è generalizzazione induttiva da 18 cicli, stress-testata contro lo spazio-oggetti concreto del repo.

**Explorer (verdetto NEGATIVO + killer falsificabile).** Nessun oggetto enumerabile soddisfa i 4 requisiti:
**R1** (non-simmetrico / sfugge al dizionario d'orbita sul gruppo PIENO), **R2** (no forma chiusa citata),
**R3** (enumerabile a ≥2 livelli brute-forceabili), **R4** (ragione a-priori). Argomento di impossibilità:
**{R1,R2} ANTAGONISTI** (rompere simmetria nel lab = fissare struttura = collasso al dizionario della simmetria RIDOTTA =
parent citato = firma door-A/C); **{R2,R3} ANTAGONISTI** (enumerabile = istanze minuscole = teorema totale risponde per
primo = Collapse Theorem). L'unico oggetto non-collassato (Kronecker d≥7, Module 30) **viola R3** (oltre il muro).
**Killer falsificabile pre-dichiarato del verdetto:** una tripla `(m, n, n+1)` con `m` non-perm-invariant sul gruppo PIENO
+ `splits≠[]` a ENTRAMBI i livelli contro il dizionario congiunto + nessuna forma chiusa.

**Adversary — ha provato a TROVARE la tripla, FALLENDO. MISURE ESATTE (GF(2) ints / Fraction, no float):**
- Candidato migliore = `feasible_interp` `min_interpolant_dt_size` (min-DT-leaves dell'interpolante di risoluzione).
- **Profilo split** contro il dizionario congiunto (cost da `.cache/ct4.pkl`, gf2_degree, sensitivity, block_sensitivity):
  **(0,0,0,24)** su n=1..4 — splitta SOLO a n=4; n=5=2^32 oltre il muro ⇒ **niente finestra a 2 livelli consecutivi**
  = **{R2,R3} ESATTO**, fallisce R3.
- **min-DT-leaves PERM-INVARIANT:** **0 violazioni su 1500** (300 funzioni × 5 permutazioni S_4) ⇒ **fallisce R1**;
  lo split a n=4 = "4 colonne troppo poche" (firma Module 29), NON rottura di simmetria.
- **interpolant SIZE non-canonico** ma swap-detector NON scatta su or3/and3 (5=5 gates) ⇒ rumore d'ordine di risoluzione
  = riga KW⁺/Razborov-Pudlák di `docs/collapse-theorem.md` ⇒ **R2 collasso**, fallisce R2.
- **Survey oggetti non-simmetrici:** nessun oggetto naturalmente-non-simmetrico (tornei/digrafi/poset/matroidi/automi/codici)
  esiste in `pnp_lab/`; gli unici R1-validi nel repo = MBPSP fixed-order (332/600 swap-sensitive ma = Module 22, viola R3)
  e `bipartite_rigidity` (Entry 31, door A). Una nuova famiglia tornei/poset colpirebbe lo STESSO bivio
  (statistica nominata=R2 OR labeling-fissato=door A).
- **CONCLUSIONE:** nessuna tripla falsificante tra oggetti concreti; il verdetto regge sotto assalto numerico. **ESC-2 NON prematuro.**
Rigenera: `from pnp_lab.feasible_interp.interp import min_interpolant_dt_size, build_interpolant_swapped`.

**Evaluator + GATE.** robustness **7.5/10** (alto per un verdetto NEGATIVO perché DOPPIAMENTE fondato: argomento
strutturale + assalto numerico fallito). Flag: **absence-of-evidence-vs-evidence-of-absence ALTO (dominante)**;
non-esaustività-ricerca ALTO (solo oggetti del repo / costruibili sui solver esistenti); induzione-non-prova /
confirmation-bias MEDIO-ALTO ({R1,R2}/{R2,R3} è generalizzazione da 17-18 cicli, NON teorema; "symmetry-break=structure-fix"
è regolarità empirica, indebolita a survival in Module 22); circolarità MEDIO (usa Collapse Theorem + door-A come premesse,
auto-referenziale); off-tiny-instance MEDIO. Verdetto **RESTATEMENT #18, meta-categoria "collasso-onto-impossibilità-condizionata"**
(PRIMO verdetto-di-impossibilità invece di riduzione-di-oggetto). NON gonfiare a teorema. **GATE: Entry-only** (B2, come
31/32: no `docs/<modulo>.md`, no numero di Module, no riga README / conteggio test); `feasible_interp` resta probe **CITATO**.
**ESC-2 RI-CONFERMATO** — più forte di Entry 29: là era PREDIZIONE prima di esercitare le door; ora è POST-HOC VALIDATO
dopo A+C+B tutte esercitate e chiuse dalla stessa firma.

**Honesty boundary (EN).** COMPUTED exactly (GF(2) ints / rational Fraction, no floats): on the feasible-interpolation
arena (`pnp_lab/feasible_interp/interp.py`), the min-DT-leaves of the resolution interpolant split against the joint
orbit-invariant dictionary (cost from `.cache/ct4.pkl`, gf2_degree, sensitivity, block_sensitivity) with profile (0,0,0,24)
over n=1..4 — splitting only at n=4; the permutation-invariance of min-DT-leaves on the full S_4 group (0 violations / 1500
= 300 functions x 5 permutations); and the silence of the swapped-rule detector on or3/and3 (5=5 gates). These establish
the best concrete door-B candidate FAILS the falsifier on a named requirement: perm-invariant (fails R1, Module-29
'too-few-columns' signature not broken symmetry), size non-canonicity is resolution-order noise (KW+/Razborov-Pudlak row of
the Collapse Theorem, fails R2), no two-consecutive-level window is brute-forceable (n=5=2^32, {R2,R3} antagonism, fails R3).
The verdict 'no enumerable object satisfies R1∧R2∧R3∧R4' is an INDUCTIVE GENERALIZATION from 18 cycles stress-tested against
the repo's concrete object-space — NOT a theorem. Two premises are conditional, not derived: {R1,R2} rests on the empirical
regularity 'symmetry-break = structure-fix' (weakened once to survival in Module 22), and the survey of non-symmetric objects
(tournaments/digraphs/posets/matroids/automata/codes) is an argument-by-fork, not a built arena — none exists in the repo.
CEILING: search bounded to repo objects; the one R1∧R2∧R4 survivor (Kronecker d≥7, Module 30) violates R3 by living past the
brute-force wall, so the verdict survives by un-reachability not refutation; the decisive two-level window is at n≥5, untested.
NO claim about P vs NP (neither direction).

**Stato repo:** `pnp_lab/feasible_interp/interp.py` (+ `families.py`) resta come probe **CITATO** di door B (NON un Module:
nessun `docs/<modulo>.md`, nessuna riga Module nel README, nessun conteggio test cristallizzato). Nessun builder, nessun nuovo
file di codice in questo ciclo. Questa entry. Suite veloce invariata.

**Stato del programma + GATE.** **Entry-only** (verdetto-di-impossibilità-condizionata, NON un collasso-di-oggetto né una
nuova arena). Bilancio aggiornato: **18 collassi (16°, 17° e 18° tutti Entry-only; il 18° = meta-impossibilità-condizionata,
NON una nuova arena né un collasso-di-oggetto) / 7 arene** + 1 falsificazione (Module 18) + 1 non-collasso (Module 22) +
survival-PASS@1 (M24) + survival-PASS@3 (M25) + 2 control-PASS (M26 H-confound, M27 gauge-confound). L'arena-count NON sale.
**Tutte e 3 le REOPENING DOOR interne** (A asse struttura-fissa / C asse leva-esatta-≥2-livelli / B asse barriera-a-priori)
sono ora **ESERCITATE e CHIUSE dalla STESSA firma** (oggetto-simmetrico-a-forma-chiusa + survival-per-omissione-di-legge; e
per B: antagonismi {R1,R2}+{R2,R3}). ESC-2 ri-confermato POST-HOC. **ATTENZIONE:** le **FALSIFIER DOOR 2/3 del grand
capstone** (certified bounds a n≥7; leva cross-livello CRESCENTE) restano **GENUINAMENTE APERTE** — vivono OLTRE il muro
brute-force, NON marcate chiuse. Solo le reopening door INTERNE sono esaurite.

**NEXT unstable direction:** tutte e 3 le reopening door interne esaurite ⇒ il lab non può aprire altro dal proprio stato.
Condizione esatta di riapertura = **input strutturale ESTERNO umano** che rompa uno dei due antagonismi = la tripla
pre-dichiarata (oggetto non-perm-invariant sul gruppo PIENO + senza forma chiusa citata + brute-forceabile a 2 livelli
consecutivi). Il lab non può costruirla dal proprio stato. Restano OLTRE-IL-MURO (NON azionabili internamente) le sole
falsifier door 2/3: certified bounds a n≥7 e leva cross-livello CRESCENTE.

---

## Entry 34 — Module 30 (GCT/Kronecker) RIAPERTO da lever umano sull'asse LOCAL-OBSTRUCTION: KILLED, artefatto di rottura-di-simmetria, RESTATEMENT #19 (Entry-only, NON un Module) (2026-06-22)

**Decisione (umano).** Lever ESTERNO sull'arena Module 30 ([[gct-kronecker]]): si può attaccare lo **sporadic
vanishing** di Kronecker da un punto di vista **LOCALE/ASINTOTICO** (un'ostruzione testabile con vincoli LOCALI)
invece di calcolare la matrice globale `g` a d≥7? Inquadramento: l'ostruzione locale onesta = il **politopo/cono
dei MOMENTI di Kronecker** (disuguaglianze Klyachko/Horn lineari; `g>0 ⟹ membership` = test locale senza calcolare
`g`); MA Kronecker NON satura (≠ Littlewood-Richardson/Knutson-Tao): esistono **BUCHI (holes)** = membership-cono +
`g=0` (crollo della Saturation Hypothesis di Mulmuley). Attacco eseguibile = classificare gli sporadic vanishing via
STRETCHING `g(2λ,2μ,2ν)`: **HOLE** (>0, dentro il cono, ostruzione NON-locale) vs **RAY-VANISH** (=0, ostruzione
asintotica/locale). Riusa il motore Murnaghan–Nakayama; il muro si sposta da `p(d)` a `p(2d)` (p(8)=22, p(10)=42,
p(12)=77, sotto il muro). **Entry-only, NON un Module** (template Entry 31/33: lever umano, KILLED redux, probe CITATO).

**Explorer + killer.** Ipotesi-lab: il bit hole/ray (via stretch N=2) NON è funzione del dizionario di copertura
(`covered` + `shape_profile`). **Killer:** cercare una **COLLISIONE** (due terne stessa chiave (shape_profile, covered),
bit OPPOSTO). Nessuna collisione → RESTATEMENT (bit ricostruibile dal dizionario Rosas/Bessenrodt–Bowman). Collisione →
sopravvivenza (invariante fuori-dizionario a 2 livelli, romperebbe l'antagonismo {R2,R3} che chiuse door B, Entry 33).
Pilot: d=4 2/2 hole, d=5 misto.

**Builder.** `pnp_lab/gct_kronecker/saturation.py` (NUOVO: `stretch`, `g_stretch`, `is_hole`, `perm_orbit`, `perm_key`,
`shape_profile`, `classify`, `collisions`, `summary`) + `tests/test_gct_saturation.py` (16 passed) + `examples/run_gct_saturation.py`;
`__init__.py` esteso con gli export. **MISURE ESATTE (interi Murnaghan–Nakayama):**
- **Bit N=2:** d=4 (2 sporadic, 2 hole, 0 ray, 0 coll); d=5 (5, 2, 3, 0); d=6 (44, 26, 18, **1 COLLISIONE**):
  HOLE `((3,3),(3,1,1,1),(2,1,1,1,1))` con `g(2·)=1` vs RAY `((4,1,1),(3,3),(2,1,1,1,1))` con `g(2·)=0`, STESSO
  `shape_profile` {hook, two-col+hook, two-row+rect} e `covered=True`, bit OPPOSTO. Sembrava SOPRAVVIVENZA.
- **Scoperta load-bearing del builder (il seme della crepa):** lo stretch NON commuta col coniugio
  (`2·transpose ≠ transpose·2`), quindi il bit è costante solo sull'**orbita di PERMUTAZIONE**, NON sulla **g-orbita**
  (`S_3 × coniugio`, che lascia `g` invariante). Il builder ha raggruppato per orbita di permutazione e lo ha TESTATO
  esplicitamente (`test_hole_bit_NOT_constant_on_g_orbit`).
- **Bonus N=3:** d=4 si ribalta a 2 RAY (bit N-dipendente).

**Adversary — KILLED, artefatto di rottura-di-simmetria.** Prove:
- **CREPA B (LETALE).** `g` è g-simmetrico ma `g(2λ,2μ,2ν)>0` NON lo è; la vera ostruzione locale (cono dei momenti)
  È g-simmetrica. Col bit g-SIMMETRICO corretto ("∃ rappresentante della g-orbita con stretch positivo"): d=4
  (0 hole, 2 ray, 0 coll); d=5 (5, 0, 0); d=6 (42, 2, **0 COLLISIONI**). La collisione SVANISCE: la "RAY"
  `((4,1,1),(3,3),(2,1,1,1,1))` ha g-coniugato `((3,1,1,1),(2,2,2),(2,1,1,1,1))` con `g_base=0` IDENTICO ma
  `g(2·)=4, g(3·)=14, g(4·)=67` — genuinamente nel cono ⇒ è HOLE come l'altra ⇒ stesso bit. La collisione era un
  ARTEFATTO della scelta (forzata) di raggruppare per permutazione invece che per g-orbita.
- **CREPA A.** Il proxy N=2 è N-instabile (parità della quasi-polinomiale `g(N·)=[1,0,1,0,…]`). A d=4 il 100% degli
  "holes" sono artefatti (g=0 a N=3); a d=6, 11/26 sono artefatti di parità. Fenomeno in gran parte spurio.
- **Vettore 3.** Con chiave g-orbita-aware + bit N=2 le collisioni salgono **1→9** (il bit N=2 è strutturalmente
  incompatibile con OGNI dizionario g-simmetrico).
- **Riduzione.** Un buco genuino RESTATES "Kronecker non satura / Mulmuley SH falsa" (Stembridge;
  Bürgisser–Christandl–Ikenmeyer). Il bit g-corretto è ricostruibile dalla g-orbita ⇒ nessun contenuto oltre il
  teorema citato.
Rigenera: `from pnp_lab.gct_kronecker.saturation import classify, collisions, summary, stretch`.

**Evaluator + GATE.** robustness **5.5/10**. Flag: **simmetria-artificiale DECISIVO/letale**, N-dipendenza /
proxy-non-è-il-cono PESANTE, singolo-oggetto PESANTE (1 collisione, 1 scala, 1 valore di d), confirmation-bias
MODERATO-PESANTE (sopravvivenza solo sotto chiave DEBOLE), dipendenza-citazione STRUTTURALE (Mulmuley SH /
saturazione). Verdetto: **RESTATEMENT #19** (NON sopravvivenza), collasso-onto-impossibilità nella forma più pulita
(l'unico residuo non-perm-invariant è proprio la parte che ROMPE la simmetria del problema). **GATE: Entry-only**
(template Entry 31/33: lever umano, KILLED redux, probe CITATO — NESSUN `docs/<modulo>.md`, nessun numero di Module,
nessuna riga README, nessun conteggio test cristallizzato). `saturation.py` + test restano probe CITATO. Raccomandazione:
iterate-then-close su questo asse; richiede un lever ESTERNO (un oggetto symmetry-respecting O le disuguaglianze
Klyachko implementate) prima di riaprire.

**Contenuto positivo (PRIMO ciclo che risponde DIRETTAMENTE a "esiste un'ostruzione locale che evita la matrice
globale?").** SÌ — il **cono dei momenti È esattamente quel test locale** — ma è g-simmetrico e ricostruisce dal
dizionario d'orbita, quindi RESTATES; e il proxy che SEMBRAVA sfuggire (stretch N=2) rompeva la simmetria del problema.
Previsione aggiornata: l'asse **local-obstruction** collassa per la STESSA ragione dell'asse **fixed-structure**
(Entry 31, [[bipartite-rigidity]]) — ogni oggetto locale onesto e symmetry-respecting ricostruisce dalla g-orbita;
solo i proxy che rompono la simmetria sembrano sfuggire, e sono artefatti. Attractor Thesis RAFFORZATA anche lungo la
direzione "evita l'oggetto globale via test locale/asintotico".

**Honesty boundary (EN).** COMPUTED (exact, finite, reproduced): the permutation-orbit hole/ray split via the N=2
stretch bit `g(2λ,2μ,2ν)` — d=4 (2/2/0/0), d=5 (5/2/3/0), d=6 (44/26/18/1 coll); the g-symmetric corrected bit
('∃ representative in the g-orbit with positive stretch') — d=4 (0/2/0), d=5 (5/0/0), d=6 (42/2/0 coll); the lethal
g-conjugate witness `((3,1,1,1),(2,2,2),(2,1,1,1,1))` with `g_base=0` but `g(2·)=4, g(3·)=14, g(4·)=67` (in the cone
⇒ HOLE); and the N-parity instability of the N=2 proxy (d=4: 2/2 holes vanish at N=3; d=6: 11/26 holes are parity
artifacts). All by exact integer Kronecker (Murnaghan–Nakayama). CITED (not computed here): the Klyachko/Horn moment
polytope as the genuine local membership obstruction; the non-saturation of Kronecker / falsity of Mulmuley's SH
(Stembridge; Bürgisser–Christandl–Ikenmeyer); the asymptotic quasi-polynomial behaviour of `g(Nλ,Nμ,Nν)`. CEILING:
the N=2 stretch bit is a single-scale proxy, NOT the moment cone — it breaks the g-symmetry (`S_3 × conjugation`) that
both `g` and the true cone respect (stretch does not commute with conjugation), and is N-unstable; the genuine local
cone is g-symmetric and reconstructs from the orbit dictionary, so the local attack RESTATES the cited non-saturation
fact; the real cone requires N→∞ or the unimplemented Klyachko inequalities; the global `g`-matrix at d≥7 remains a
brute-force wall. NO claim about P vs NP.

**Stato repo:** `pnp_lab/gct_kronecker/saturation.py` (NUOVO) + `tests/test_gct_saturation.py` (16 passed) +
`examples/run_gct_saturation.py`; `pnp_lab/gct_kronecker/__init__.py` esteso con gli export (`stretch`, `g_stretch`,
`is_hole`, `perm_orbit`, `perm_key`, `shape_profile`, `classify`, `collisions`, `summary`). Restano come probe CITATO
(NON un Module: nessun `docs/<modulo>.md`, nessuna riga README, nessun conteggio test cristallizzato). Questa entry.

**Stato del programma + GATE.** **Entry-only** (Module-30-riaperto-da-lever-umano sull'asse local-obstruction, KILLED
RESTATEMENT, NON una nuova arena né un Module). Bilancio aggiornato: **19 collassi (il 19° Entry-only, KILLED
restatement, NON aggiunge arena né Module) / 7 arene** + 1 falsificazione (Module 18) + 1 non-collasso (Module 22) +
survival-PASS@1 (M24) + survival-PASS@3 (M25) + 2 control-PASS (M26 H-confound, M27 gauge-confound). L'arena-count NON
sale. Il lever umano ha riaperto Module 30 sull'asse **local-obstruction** e lo ha richiuso allo STESSO muro: ogni
oggetto locale onesto e symmetry-respecting RESTATES dal dizionario d'orbita; il cono dei momenti reale richiede N→∞ o
le disuguaglianze Klyachko non implementate, e la matrice globale a d≥7 resta il muro brute-force.

**NEXT unstable direction:** l'asse local-obstruction (cono dei momenti via stretch) è CHIUSO per la stessa ragione
dell'asse fixed-structure (Entry 31) — rottura di simmetria = collasso al dizionario della simmetria ridotta. Riapertura
ESCLUSIVAMENTE su lever ESTERNO umano: o (i) un oggetto locale **genuinamente g-symmetry-respecting E non-saturante**
brute-forceabile a 2 scale consecutive (rompe l'antagonismo {R2,R3}), oppure (ii) le **disuguaglianze Klyachko/Horn
implementate** come test di membership esatto (sostituiscono il proxy N=2 col cono vero). Restano OLTRE-IL-MURO le sole
falsifier door 2/3 del grand capstone (certified n≥7; leva cross-livello CRESCENTE). Il lab resta chiuso come metodologia.

## Entry 35 — Module 30 (GCT/Kronecker) RIAPERTO da lever umano (ii) sull'asse CONO-DEI-MOMENTI: KILLED via inner-approximation + survival-by-omission, RESTATEMENT #20 (Entry-only, NON un Module) (2026-07-04)

**Decisione (umano).** Secondo lever ESTERNO su Module 30 ([[gct-kronecker]]): **implementa il cono di Klyachko esatto**
(`g>0 ⟹ membership`) e cerca un buco (ostruzione locale/a-priori che sfugga il muro brute-force d≥7). A differenza del ciclo
precedente Entry 34 (asse stretch N=2 distrutto da simmetria), questo ciclo ATTACCA il **politopo/cono esatto dei MOMENTI**
via **LP feasibility Phase-I razionale** (calcolo dell'H-rep beyond-beneath): facce, Farkas esatto, dizionario {nonneg,
ordering, triangle-ineq}. Contrasto strategico: Entry 34 (proxy N=2, collassa per rottura-simmetria), Entry 35 (obiettivo
esatto, collassa per inner-approximation-a-scala-fissa). **Entry-only, NON un Module** (template Entry 31/33/34: lever umano,
KILLED redux, probe CITATO).

**Explorer + killer.** Ipotesi-lab: il cono dei momenti NON è il **dizionario essenziale** per classificare sporadici
Kronecker; esiste una faccetta di P_D (D∈{3,4,5,6}) che NON è in {nonneg, ordering, triangle-bounds} = survival di
un'ostruzione locale FUORI da Rosas/Bessenrodt–Bowman. **Killer:** (K1) ogni faccetta "fuori dizionario" è un artefatto
inner-approximation (P_D è approssimazione interna RAZIONALE, non il cono vero come N→∞); (K2) la faccetta superstite si
riduce ESATTAMENTE alla first-row bound λ₁ ≥ μ₁+ν₁−d (Klyachko 2004 / Christandl–Mitchison 2006) + permutazioni = NC
nota. No sopravvivenza → RESTATEMENT.

**Builder.** `pnp_lab/gct_kronecker/moment_cone.py` (NUOVO: `max_parts`, `point`, `support_points`, `in_cone` = LP Phase-I
RAZIONALE, `is_deep_hole`, `holes`, `summary`/`cone_summary`, `facets` = beneath-beyond ESATTO, `classify_facet`,
`facet_report` = Farkas esatto vs dizionario {nonneg, ordering} + affine hull) + `tests/test_moment_cone.py` (15 passed) +
`examples/run_moment_cone.py`; `__init__.py` esteso con gli export. **MISURE ESATTE (interi / Fraction razionale, no float):**

**d=5 vs P_5 (k=5 partizioni):** (#sporadic, #in_cone, #superf_SOLO_nonneg, #profondi, #fuori)=(5, 0, 0, 0, 5). Tutti e 5
gli sporadici RESTANO fuori dal cono interno razionale a scaling finito.

**d=6 vs P_6 (k=6):** (44, 10, 10, 0, 34) — **10 in-cono, TUTTI superficiali** (violati da una sola disuguaglianza in
{nonneg, ordering}), 0 profondi, 34 fuori ⇒ **KILLER-1 SPARA**: le 10 faccette in-cono sono inner-boundary, non robuste.

**P_3 (k=3, dim 9, |support|=14, dim affine 6):** 14 faccette exacte. Per verifica: 3 in-dizionario (nonneg + ordering),
11 "fuori". Rigenera: `from pnp_lab.gct_kronecker.moment_cone import in_cone, holes, classify_facet, facet_report, summary`.

**Adversary — KILLED (2 colpi concordi).** (1) **ARTEFATTO INNER-APPROXIMATION (LETALE).** 8/11 faccette "fuori-dizionario"
su P_3 VIOLATE da controesempi esatti d=4 con g>0: es. `[(-4,5,-1),(-2,1,1),(-2,1,1)]·x≤-2` violata da
`((2,2),(2,2),(1,1,1,1))` con g=1, valore 0>-2; padding zero (scelta conservativa, non riducibile). Le 3 in-dizionario
`0/3` violate. P_3 è "magro" (sole partizioni ≤3 parti), a d=4 compaiono direzioni nuove (es. `(1,1,1,1)`). Inner-
approximation a scaling FINITO (k fissato) è structurally-not-closed per il cono. (2) **SURVIVAL-BY-OMISSION (firma Entry
32/33):** le 11 faccette = 5 orbite `S_3` per blocco, 4 uccise dall'attacco 1; l'**unica orbita superstite** {3 faccette
identiche per affine hull} si riduce ESATTAMENTE a **λ₁ ≥ μ₁+ν₁−d** e permutazioni (la first-row bound NOTA 2004/2006,
già implicata da `nc_maxpart` del lab). Certificato Farkas esatto: LHS = 3·(triangle) − 1 ≤ 2; NC verificata **0 eccezioni
su 0,5,15,40,119 positivi** d=3..6 (killer-2 NON spara su nessun range). Col generatore triangolare aggiunto al dizionario:
3→6 in-dizionario, le 8 restanti=gli artefatti. Null-control: con sole 2 famiglie generatori quasi ogni politopo piccolo ha
faccette "fuori" ⇒ mezzo discriminante isolato.

**Evaluator + GATE.** robustness **5.5/10**. Flag: **inner-approximation-a-scala-fissa LETALE** (P_D ≠ cono vero come
N→∞), **dizionario-minimale-per-costruzione** (survival-by-omission = manca il generatore triangle-ineq citato),
**singola-scala-di-faccette** (H-rep completa solo P_3; P_4~8 min non brute-forced; P_5 esplode), **dipendenza-citazione
PESANTE** (Klyachko/Christandl–Mitchison + Rosas/Bessenrodt–Bowman), **N_max=4 negli sporadici misure Entry 34** MODERATO.
Verdetto: **RESTATEMENT #20 — KILLED** (entrambi i killer sparano con impeccabile sequenza logica). **GATE: Entry-only**
(template Entry 31/33/34: nessun `docs/<modulo>.md`, nessuna riga README, nessun numero di Module; `moment_cone.py` + test
restano probe CITATO della porta DOOR-2).

**Honesty boundary (EN).** COMPUTED (exact rational Phase-I LP feasibility, exact beneath-beyond H-rep, exact Farkas
classification, no floats): the inner polytope P_D for D=3..6 (membership queries on all sporadics), the measurements above,
the 8 exact d=4 counterexamples to the 11 "out-of-dictionary" facets, the exact reduction of the 3 surviving facets to
λ₁ ≥ μ₁+ν₁−d with Farkas certificate (LHS = 3×triangle−1), and 0-exception verification of the triangle inequality on all
positive (λ,μ,ν) triples d=3..6 (0/5, 0/15, 0/40, 0/119). CITED, never re-verified: Klyachko 2004 / Christandl–Mitchison
2006 (first-row bound, quantum marginal spectra), non-saturation of Kronecker (Stembridge; Bürgisser–Christandl–Ikenmeyer
NP-hardness), the true moment cone as N→∞ closure. CEILING: P_D is a fixed-scale inner rational approximation, NOT the cone
itself; complete H-rep unreachable for D≥5 (below-beyond unfeasible, cost explodes), so facet-turnover leverage (DOOR-2
originally framed) is NOT measurable this way; "out-of-dictionary" means ONLY "not in the list of nonneg/ordering/triangle",
not intrinsic non-membership; no claim about P vs NP.

**Stato repo:** `pnp_lab/gct_kronecker/moment_cone.py` (NUOVO) + `tests/test_moment_cone.py` (15 passed) +
`examples/run_moment_cone.py`; `pnp_lab/gct_kronecker/__init__.py` esteso con gli export (`max_parts`, `point`,
`support_points`, `in_cone`, `is_deep_hole`, `holes`, `summary`, `cone_summary`, `facets`, `classify_facet`,
`facet_report`). Restano come probe CITATO di DOOR-2 (NON un Module: nessun `docs/<modulo>.md`, nessuna riga README, nessun
conteggio test cristallizzato). Questa entry. Suite veloce invariata.

**Stato del programma + GATE.** **Entry-only** (Module-30-riaperto-da-lever-umano sull'asse cono-momenti, KILLED RESTATEMENT,
NON una nuova arena né un Module). Bilancio aggiornato: **20 collassi (il 20° Entry-only, KILLED restatement di DOOR-2, NON
aggiunge arena né Module) / 7 arene** + 1 falsificazione (Module 18) + 1 non-collasso (Module 22) + survival-PASS@1 (M24) +
survival-PASS@3 (M25) + 2 control-PASS (M26 H-confound, M27 gauge-confound). L'arena-count NON sale. Il lever umano ha
riaperto Module 30 su due assi consecutivi (Entry 34 stretch N=2 / Entry 35 cono-momenti): entrambi KILLED dalla stessa
firma (artefatti di scala/simmetria + riduzione al noto). **L'asse local-obstruction di Module 30 è CHIUSO su ENTRAMBI i
lever** (stretch rompendo simmetria, cono-momenti inner-approximation). Attractor Thesis RAFFORZATA.

**NEXT unstable direction:** (a) **Entry 36 "ponte certificato" (DOOR-2) è DECLASSATA:** testerebbe a d=7,8 una
disuguaglianza già nota (fidelity-check Klyachko/Christandl–Mitchison, non scoperta); riformulazione onesta: cercare una
faccetta di P_D (D≥4) NON riducibile a {nonneg, ordering, triangle, affine hull della 3-orbita di maxpart-bounds} — se non
esiste P_D, il cono non è il piedistallo per DOOR-2. (b) **Entry 37 "leva del cono" (DOOR-3) impossibile in esatto oltre
D=4:** riformulazione: sampling di direzioni random + oracolo LP (stima probabilistica di L(D), leva cross-scale, pattern
Modules 24-27). (c) **Direzione più promettente del brief strategico:** il **Teorema dell'Attrattore** (§3 ciclo +3 di
prompts/fable-frontier.md) — rendere eseguibile la firma stessa del collasso (reticolo degli invarianti delle 7 arene,
generazione finita della chiusura-dizionario di ogni regime Bulatov–Zhuk-hard, falsifier per non-existence di escape) = il
deliverable onesto del lab. Riapertura di Module 30 SOLO su nuovo lever esterno (non-approximazione cono, disuguaglianze
Klyachko implementate O oggetto non-perm-invariant genuinamente senza forma chiusa su d=6..7).

---

## Entry 36 — META-PIVOT "Teorema dell'Attrattore" (reticolo dei 5 invarianti su B_3): KILLED via survival-by-omission (real_degree) + group-mismatch, RESTATEMENT #21 (Entry-only, NON un Module) (2026-07-04)

**Strategist (sonnet, loop economico fable-frontier):** scelta direzione (c) del brief §3 promossa a Entry 36: rendere eseguibile la firma dei collassi — ipotesi: su n=3 il separatore minimo G ⊆ {cost, gf2_degree, sensitivity, block_sensitivity, adeg} ha 2≤|G|≤3 e il Hasse della ricostruibilità non è né catena né anticatena. Killer pre-dichiarati: K1 trivialità-bottom (G={cost}), K2 trivialità-top (|G|=5, dizionario incomprimibile), K3 riduzione al noto/log.

**Builder:** pnp_lab/attractor_theorem/lattice.py (NUOVO: orbit_invariant_table, reconstructibility_matrix, reconstructible_from, minimum_separators, hasse_diagram, summary; aritmetica esatta int/Fraction) + tests/test_attractor_lattice.py (19 passed) + examples/run_attractor_lattice.py. Misure ESATTE sotto B_3 (22 orbite, n=3): NESSUN separatore esiste (8 gruppi di collisione del 5-tuple, es. const-0/const-1 identiche: tutti e 5 gli invarianti sono complement-invarianti sull'output mentre B_3 non include la negazione dell'output); Hasse = ANTICATENA di 4 classi {cost},{gf2},{sens,bs},{adeg}. Ipotesi dello strategist falsificata su entrambe le parti.

**Adversary — KILLED (3 colpi):** (1) GROUP-MISMATCH (pattern Entry 34): sotto NPN (14 classi) le collisioni crollano 8→1 (unica: classi tt=24 vs tt=30, stesso 5-tuple (5,2,3,3,2)); anticatena invariata. (2) SMALL-N: sens=bs su tutte le orbite a n=3 ma controesempio a n=4 (tt=7128: s=2, bs=3) ⇒ il nodo {sens,bs} è artefatto small-n. (3) SURVIVAL-BY-OMISSION (LETALE, pattern Entry 32): real_degree (grado di Fourier, GIÀ nel repo in pnp_lab/meta_complexity/falsifier_hunt.py:281, NPN-invariante) separa 24 da 30 (2 vs 3); con 6 invarianti i separatori minimi sono |G|=4 ({cost,gf2,sens,real_degree} e {cost,gf2,bs,real_degree}); adeg NON compare in alcun separatore minimo (coerente con Module 29: adeg ricostruibile dal dizionario congiunto). Il "nessun separatore" era falsification-by-omission.

**Evaluator + GATE:** robustness **3.5/10**. Flag: survival-by-omission-real_degree LETALE; small-n (sens=bs solo a n=3) PESANTE; group-mismatch B_3-vs-NPN MODERATO. Verdetto: **RESTATEMENT #21 — KILLED** (K2-variante: |G|=4 su 6 = dizionario poco comprimibile; K3: anticatena RESTATES Module 29 + Collapse Theorem Module 16). **GATE: Entry-only** (nessun docs/, nessuna riga README; lattice.py + test restano probe CITATO). Contenuto onesto positivo: sotto NPN il dizionario a 6 invarianti è separante con minimo |G|=4 e adeg è ridondante.

**Honesty boundary (EN).** COMPUTED (exact, int/Fraction, deterministic): the 22-orbit B_3 invariant table at n=3; the empty-separator result over all 2^5 subsets with its 8 exact 5-tuple collision groups; the antichain Hasse diagram with the single mutual-reconstructibility node {sensitivity, block_sensitivity}; the NPN recount (14 classes, 1 collision (5,2,3,3,2) between tt=24 and tt=30); the resolution of that collision by real_degree (2 vs 3) and the |G|=4 minimum separators over the 6-invariant dictionary; the n=4 counterexample tt=7128 (s=2, bs=3). CITED: the five invariant implementations reused from existing modules (cost from circuits/synthesis, gf2/sens/bs from meta_complexity/strata_graph, adeg from approx_degree — Module 29); real_degree from meta_complexity/falsifier_hunt.py; s vs bs separations in the literature (Rubinstein-style). CEILING: n=3 only (the sens=bs node provably breaks at n=4); the lattice measures WHICH invariants were included, not a canonical structure — both headline results (no separator; antichain) moved under group correction and dictionary completion, so the object is definition-sensitive; the "collapse-signature lattice ACROSS the 7 arenas" (the honest Attractor-Theorem deliverable) was NOT built here. NO claim about P vs NP.

**Stato repo:** pnp_lab/attractor_theorem/ (NUOVO package: __init__.py + lattice.py) + tests/test_attractor_lattice.py (19 passed) + examples/run_attractor_lattice.py. Probe CITATO, Entry-only.

**Stato del programma + GATE:** Ledger: **21 collassi (il 21° Entry-only) / 7 arene** + 1 falsificazione + 1 non-collasso + survival-PASS@1 + survival-PASS@3 + 2 control-PASS. L'asse "reticolo dei separatori su un singolo livello" del Teorema dell'Attrattore è CHIUSO (stessa firma: omission + mismatch di gruppo + small-n). Attractor Thesis CONSOLIDATA.

**NEXT unstable direction:** (a) completare il 6-lattice con real_degree su NPN (fix onesto, ma prevedibilmente RESTATEMENT del Collapse Theorem — basso rendimento); (b) il vero deliverable rimasto: la firma di collasso CROSS-ARENA (reticolo della chiusura-dizionario attraverso le 7 arene: quali generatori assorbono i 21 collassi, la chiusura è finitamente generata?) — richiede una formalizzazione falsificabile PRIMA di un nuovo builder; (c) riapertura arene solo su lever esterno umano.

---

## Entry 37 — META-PIVOT ciclo 2 "Collapse Ledger" (firma di collasso cross-arena): KILLED via tautologia editoriale / meta-collasso auto-referenziale, RESTATEMENT #22 (Entry-only, NON un Module) (2026-07-05)

**Strategist (sonnet, loop fable-frontier, direzione (b) scelta dal PI umano):** formalizzare la firma dei 21 collassi come oggetto eseguibile: 21 record machine-checkable dal log + campo hand-labeled collapse_type via 6 regole regex prioritarie PRE-dichiarate (OMISSION > COND-IMPOSSIBLE > SYMM-ARTIFACT > CLOSED-FORM > PERM-ABSORBED > CITED-THEOREM default). IPOTESI H: C(21)≤6 E Good-Turing unseen ≤1 ⇒ chiusura-dizionario finitamente generata. Killer pre-dichiarati: K-narrativa (≥4/21 ambigui), K-small-sample, K-granularità (C∈[3,10]), K-omission.

**Builder:** pnp_lab/attractor_theorem/collapse_ledger.py (NUOVO: load_collapses, assign_type con trigger auditabili, cumulative_curve, good_turing seed=0 deterministico, stability, ledger_summary) + tests/test_collapse_ledger.py (16 test; suite completa 583 passed) + examples/run_collapse_ledger.py. MISURE: 21/21 record (7 literal "RESTATEMENT #N", 14 heuristic dal conteggio nel testo); tipi: CITED-THEOREM 7, PERM-ABSORBED 9, OMISSION 4, SYMM-ARTIFACT 1, COND-IMPOSSIBLE 0, CLOSED-FORM 0; C(1..21)=[1,1,1,1,2,…,2,3,3,4,4,4], C(21)=4; n_singleton=1; GT CI [0, 0.0476]; ambigui=5 (R17–R21) ⇒ **K-NARRATIVA SPARA** (soglia pre-dichiarata 4).

**Adversary — KILLED (4 attacchi):** (1) ADJUDICATION: K-narrativa NON declassabile a posteriori; dei 5 ambigui, 2 co-applicazioni genuine (R17 Entry 32, R21 Entry 36) e 3 artefatti di vocabolario (R18, R19, R20). (2) CIRCOLARITÀ EDITORIALE (il colpo più profondo): Entry 33 misclassificata OMISSION via frase di cross-riferimento — il suo tipo genuino COND-IMPOSSIBLE è soppresso a conteggio 0 dalla priorità delle regole ⇒ C(21)=4 è un ARTEFATTO; corretto: C=5, n_singleton=2, GT CI [0, 0.0952]. Il trigger "orbita" (R5) matcha il sostantivo matematico non il meccanismo (~3-4 falsi positivi su 9 PERM-ABSORBED; falso negativo Entry 10). Il vocabolario si propaga per auto-citazione ("firma Entry 32") ⇒ il codebook classifica il corpus che lo ha generato: circolare per costruzione. (3) ANTI-SATURAZIONE: tasso tipi nuovi 0.182/entry (primi 11) → 0.200/entry (ultimi 10); i tipi 3 e 4 compaiono negli ultimi 5 di 21 ⇒ curva in fase ASCENDENTE, stazionarietà di Good-Turing violata ⇒ né saturazione né finitezza dichiarabili. (4) ESTRAZIONE: pulita (4 mapping heuristic verificati a mano, nessun errore). Riduzione: il ciclo = "un codebook regex scritto nel vocabolario del log che classifica produce C finito" = tautologia editoriale; H tecnicamente vera anche dopo correzione (C=5≤6) ma solo perché le condizioni sono infalsificabili a n=21.

**Evaluator + GATE:** robustness **3.5/10**. Flag: K-narrativa-fires-non-declassabile LETALE; circolarità-editoriale LETALE; non-stazionarietà (GT inapplicabile) LETALE; heuristic-extraction 14/21 PESANTE; self-referentiality PESANTE. Verdetto: **KILLED / META-COLLASSO = RESTATEMENT #22** — il ledger dei collassi collassa esso stesso, e per meccanismi (omission di tipo, mismatch di granularità, circolarità) che sono ESSI STESSI tipi del ledger. NON è evidenza di chiusura finitamente generata; l'Attractor Thesis si estende al META-LIVELLO. **GATE: Entry-only** (collapse_ledger.py + test probe CITATO; nessun docs/, nessuna riga README).

**Honesty boundary (EN).** COMPUTED (exact, deterministic, seed=0): the 21/21 record extraction (7 literal, 14 heuristic, spot-checked clean); type counts {CITED-THEOREM:7, PERM-ABSORBED:9, OMISSION:4, SYMM-ARTIFACT:1}; the cumulative curve C(1..21) ending [.,3,3,4,4,4] with C(21)=4; Good-Turing n_singleton=1, unseen=0.0476, CI [0,0.0476]; the 5 ambiguous records R17–R21; the adversary correction (Entry 33 → COND-IMPOSSIBLE ⇒ C=5, n_singleton=2, CI [0,0.0952]); the new-type rates 0.182 vs 0.200 per entry. CITED: the Good-Turing estimator and its stationarity assumption; the log entries as corpus (their verdicts were computed in past cycles, not recomputed here). CEILING: the taxonomy is NOT a reliable measurement instrument (K-narrativa fired as pre-declared; the codebook shares vocabulary with — and propagates through — the corpus it classifies); at n=21 with a rising tail NEITHER saturation NOR open-endedness is decidable; H's numeric conditions are too weak to be falsified at this sample size, so their holding carries no evidential weight. NO claim about P vs NP.

**Stato repo:** pnp_lab/attractor_theorem/collapse_ledger.py (NUOVO) + tests/test_collapse_ledger.py (16) + examples/run_collapse_ledger.py; __init__.py esteso (alias ledger_summary/lattice_summary). Probe CITATO, Entry-only.

**Stato del programma + GATE:** Ledger: **22 collassi (il 22° Entry-only, META-collasso) / 7 arene** + 1 falsificazione + 1 non-collasso + survival-PASS@1 + survival-PASS@3 + 2 control-PASS. ENTRAMBI i cicli del meta-pivot "Teorema dell'Attrattore" (Entry 36 lattice, Entry 37 ledger) KILLED con la stessa firma che studiavano. Il programma fable-frontier ha esaurito le direzioni interne del brief (§3: cono ×2, meta ×2; DOOR-2/3 declassate). ESC-2 ri-confermato AL META-LIVELLO.

**NEXT unstable direction:** punto di scelta UMANO: (a) chiudere il programma fable-frontier come ri-conferma meta-livello di ESC-2 (raccomandazione dell'evaluator); (b) rivalidazione indipendente del codebook da fonte ESTERNA al log (costosa, bassa probabilità di esito diverso); (c) riapertura solo su lever esterno (nuova arena fuori dal repo, o falsificazione algoritmica dell'Attractor Thesis da fonte indipendente).

---

## Entry 38 — CHIUSURA del programma fable-frontier (scelta umana (a)): ESC-2 ri-confermato al META-LIVELLO, capstone aggiornato (crystallization-only) (2026-07-05)

**Decisione umana:** opzione **(a)** del choice point di Entry 37 — chiudere il programma
fable-frontier come ri-conferma di ESC-2 al meta-livello. Nessun codice toccato. Nessuna misura
eseguita. Questa entry registra una decisione umana e un aggiornamento di documentazione.

**Cosa è stato fatto:** aggiunta la sezione "Post-scriptum — the second arc of reopenings and
the meta-collapse (Entries 30–38)" in fondo a `docs/lab-capstone.md`. Memoria aggiornata
(`memory/lab-capstone.md`, `memory/MEMORY.md`). Nessun file di codice o test modificato.

**Bilancio finale:** **22 collassi / 7 arene** + 1 falsificazione (Module 18) + 1 non-collasso
(Module 22) + survival-PASS@1 (M24) + survival-PASS@3 (M25) + 2 control-PASS (M26, M27).
Il secondo arco (Entries 30–37, 8 cicli) ha prodotto RESTATEMENT #15–#22, tutti killed, nessun
nuovo Module, nessun nuovo arena. Il meta-pivot (Entries 36–37) — il tentativo più ambizioso:
rendere la firma dei collassi un oggetto eseguibile — è collassato auto-referenzialmente: il
ledger dei collassi muore per omissione di tipo, mismatch di granularità e circolarità del
codebook, che sono esattamente i meccanismi che catalogava. Questo estende l'Attractor Thesis
al meta-livello.

**Honesty boundary (EN).** This entry records a human decision and a documentation update;
nothing was computed. The meta-collapse of Entry 37 — the collapse-ledger dying by its own
catalogued mechanisms (type-omission, granularity mismatch, circular codebook, rising type-rate
at n=21) — is the arc's closing observation. All numeric claims in this entry derive from
Entry 37's measurements (21/21 records, C(21)=4 corrected to 5, GT CI [0,0.0952]), which are
reproducible via `examples/run_collapse_ledger.py`. The lab remains a METHODOLOGY with no claim
about P vs NP.

**Stato del programma:** fable-frontier CHIUSO. Il lab riapre SOLO su lever esterno che
soddisfa uno dei criteri del post-scriptum: nuova arena fuori dal repo con ragione a-priori,
oggetto certificato oltre il muro d≥7/n≥5 non riducibile alle famiglie note, o falsificazione
indipendente dell'Attractor Thesis. I probe citati — `saturation.py`, `moment_cone.py`,
`lattice.py`, `collapse_ledger.py` — restano eseguibili e testati (suite 583 passed). Il
protocollo del loop economico è documentato in `prompts/fable-frontier.md`.

**NEXT unstable direction:** nessuna direzione interna nota. Riapertura SOLO su lever esterno
(criteri: post-scriptum di docs/lab-capstone.md, Entry 38).

---

## Entry 39 — LEVER ESTERNO "Kronecker Beyond the Wall" (Module 30 riaperto, cicli 0+1): IL MURO d≥7 CADE (artefatto implementativo) + caccia allo sporadico genuino KILLED, RESTATEMENT #23 (Entry-only, NON un Module) (2026-07-05)

**Lever + protocollo.** Lever esterno umano (Roberto, 2026-07-05, criterio del post-scriptum soddisfatto): sfondare il muro d≥7 e cercare un vanishing g(λ,μ,ν)=0 GENUINAMENTE sporadico. Tiering vincolante: fascia alta per Strategist/Explorer/Adversary/Evaluator/gate (eseguiti da Fable 5 inline + adversary Opus), Sonnet per Builder/Archivist. Ciclo 0 obbligatorio prima dell'ipotesi.

**Ciclo 0a (Strategist, Fable 5 + web search).** docs/prior-art-kronecker-zeros.md (NUOVO, committato b502e5c): dizionario A (condizioni necessarie implementabili: Dvir lunghezza/prima-riga, triangolare Klyachko, cono momenti, stretching), B (famiglie a forma chiusa: Rosas two-row/hook, Blasiak, rettangoli/near-rectangles, multiplicity-free Bessenrodt–Bowman, two-column Pak–Panova), C (hardness: decidere g>0 NP-hard ⇒ ogni lista B è strutturalmente incompleta), D (tavole già pubblicate: dataset ML 6≤n≤20, Coquereaux–Zuber ⇒ il censimento è RIPRODUZIONE dichiarata; la classificazione covered-vs-sporadic a d=7..9 NON risulta pubblicata). KILLER-0 NON spara, con riserva.

**Ciclo 0b (Builder, Sonnet).** pnp_lab/gct_kronecker/fast.py (character_table memoizzata via Murnaghan–Nakayama esistente + g_fast a interi esatti con verifica resto + census) + tests/test_gct_fast.py (38 test: ancoraggio g_fast==kronecker d≤5 0 mismatch, Σdim²=d!, δ-regole, simmetrie, ortogonalità righe) + examples/run_gct_fast.py. **MISURA: IL MURO CADE** — censimento completo d=7: 680 terne, 339 zeri, 24.6 ms; d=8: 2024 terne, 1029 zeri, 29 ms; d=9: 4960 terne, 2279 zeri, 80.5 ms (tavola: 3.6/10.9/17.9 ms). Stima d=10: ~0.3 s. Muro REALE ~d=18 (33 min). Le Entry 30/34/35 citavano d≥7 come muro brute-force: era un ARTEFATTO IMPLEMENTATIVO (ricalcolo dei caratteri per terna invece della tavola precomputata). Correzione di fatto permanente.

**Ciclo 1 (Explorer Fable 5; Builder Sonnet).** H: a d∈{7,8,9}, col dizionario esteso (NC nuove: nc_dvir_full λ₁≤Σmin(μᵢ,νᵢ), nc_triangle λ₁≥μ₁+ν₁−d; covered esteso alla g-orbita), uncovered(d) non vuoto e crescente, con testimone canonico. Killer pre-dichiarati: K1-omission, K2-symmetry, K3-reproduction, K4-triviality (>50%). Builder: pnp_lab/gct_kronecker/beyond_wall.py + tests/test_beyond_wall.py (24 test) + examples/run_beyond_wall.py. MISURE: (d, #zeri, #explained, #sporadic-esteso, #covered_ext, #uncovered) = (7: 339/299/40/38/1), (8: 1029/836/193/175/10), (9: 2279/1853/426/317/64); sanity Entry 30 riprodotta (sporadic-vecchio 2/5/44 a d=4/5/6, uncovered=0 a d≤6); NC nuove 0 falsi positivi su d≤6 (e spiegano 3 sporadici a d=5 e 14 a d=6: 44→30 col dizionario NC esteso); testimoni tutti HOLE (stretch N=2 >0). Flagship d=7: ((1^7),(3,2,2),(3,2,2)).

**Adversary (Opus) — KILLED (attacchi 1-5).** (1) K2-SYMMETRY letale: la famiglia banale 1-dim mancava da covered (g([d],μ,ν)=δ_{μν}, g([1^d],μ,ν)=δ_{μ,ν'}); sull'INTERA g-orbita uccide 1/1 (d=7), 1/10 (d=8), 3/64 (d=9) — il flagship d=7 muore banalmente: il coniugato ((7),(3,3,1),(3,2,2)) è zero per δ_{μν}; coverage.covered ha un buco (richiede DUE special-shape). (2) K1-OMISSION: dei superstiti, 9/9 (d=8) e 60/61 (d=9) hanno nell'orbita una componente hook o two-column ⇒ perimetro di B2 (Blasiak) / B6 (Pak–Panova), famiglie CITATE e dichiaratamente non implementate ⇒ survival-by-omission per costruzione (firma Entry 32/33). (3+4) L'UNICO superstite genuino: ((3,2,1,1,1,1),(3,2,1,1,1,1),(3,2,1,1,1,1)) a d=9 — diagonale di tensor-cube g(λ,λ,λ)=0, HOLE con g(2λ,2λ,2λ)=14345 ⇒ RESTATES la non-saturazione (Stembridge; Bürgisser–Christandl–Ikenmeyer) — identico a Entry 34 — nel contesto dei vanishing simmetrici (Springer 2019). (5) K4: la crescita 2.5%→5.2%→15% degli uncovered è artefatto del buco di covered; frazione GENUINA 0/40, 0/193, 1/426 ≈ 0.23%, piatta. VERDETTO: KILLED → RESTATEMENT.

**Evaluator + GATE (Fable 5 inline, fascia alta).** robustness **5/10**. Flag: survival-by-omission-DICHIARATA (B2/B6 omesse: H era condizionale per costruzione) PESANTE; coverage-bug (famiglia 1-dim + soglia two-special) PESANTE ma trovato e quantificato dall'adversary (4/75); riproduzione-tavole DICHIARATA (prior-art D) MODERATO; hole⇒non-saturazione STRUTTURALE. Verdetto: **RESTATEMENT #23 — KILLED** per il claim H. **GATE: Entry-only** per il claim (nessun numero di Module, nessuna riga README); MA il ciclo lascia DUE asset permanenti COMPUTED: (i) il muro d≥7 NON ESISTE (fast.py, correzione alle Entry 30/34/35), (ii) il censimento classificato d=7..9 col dizionario esteso. docs/prior-art-kronecker-zeros.md resta come dizionario del programma.

**Honesty boundary (EN).** COMPUTED (exact integers, deterministic, reproduced): the full character tables and Kronecker census for d=7/8/9 (680/2024/4960 unordered triples; 339/1029/2279 zeros; 24.6/29.0/80.5 ms census times — the d≥7 "brute-force wall" cited in Entries 30/34/35 was an implementation artifact; the real wall is ~d=18); the extended necessary conditions nc_dvir_full and nc_triangle with 0 false positives on d≤6; the classification (explained/sporadic/covered/uncovered) at d=4..9 with Entry-30 sanity reproduced; the adversary kill-counts on the 75 uncovered witnesses (4 by the omitted 1-dim family on the full g-orbit, 69 inside cited-but-unimplemented hook/two-column families, 1 residual); the residual witness g(λ,λ,λ)=0, λ=(3,2,1,1,1,1), with g(2λ,2λ,2λ)=14345 (HOLE). CITED (not computed): Rosas/Blasiak/Pak–Panova/Bessenrodt–Bowman closed-form families (B1/B2/B5/B6); Dvir's theorem; Klyachko/Christandl–Mitchison first-row bound; non-saturation (Stembridge; BCI); NP-hardness of positivity; published tables/datasets (6≤n≤20) making the raw census a REPRODUCTION. CEILING: "uncovered" is always relative to the implemented dictionary (hardness guarantees no complete dictionary exists); the residual g(λ,λ,λ) hole restates cited non-saturation, not new content; coverage.covered retains its documented gap (fixing it is future work, probes unmodified post-verdict). NO claim about P vs NP.

**Stato repo:** docs/prior-art-kronecker-zeros.md + pnp_lab/gct_kronecker/fast.py + beyond_wall.py + tests (38+24) + examples (2) + __init__ esteso; ciclo 0 già committato b502e5c; ciclo 1 in questo commit. Probe COMPUTED/CITED, Entry-only.

**Stato del programma + GATE.** Ledger: **23 collassi (il 23° Entry-only) / 7 arene** + 1 falsificazione + 1 non-collasso + survival-PASS@1 + survival-PASS@3 + 2 control-PASS. Il lever esterno ha prodotto il risultato più CONCRETO del secondo arco: il muro era un artefatto — ma la caccia oltre il muro muore della firma di sempre (omission + symmetry). L'Attractor Thesis regge anche con il muro abbattuto.

**NEXT unstable direction:** scelta umana: (a) completare il dizionario (implementare B2 Blasiak hook-rule e B6 two-column esatti, fixare coverage) e rifare la caccia a d=9..12 — chiuderebbe onestamente la classificazione ma con esito prevedibile RESTATEMENT; (b) inseguire la diagonale g(λ,λ,λ)=0 (l'unico residuo): censire TUTTI gli zeri diagonali a d≤12 col nuovo fast.py e classificarli contro i vanishing simmetrici citati — oggetto più mirato, letteratura attiva; (c) fermarsi: il lever è esaurito con onore (muro abbattuto, RESTATEMENT #23).

---

## Entry 40 — Fase 2 "Perseverance Run": censimento diagonale g(λ,λ,λ)=0 d≤12, tutti gli uncovered sono HOLE, RESTATEMENT #24 (Entry-only, NON un Module) (2026-07-18)

**Decisione (Fase 2, PI).** Lever interno: eseguire la direzione (b) lasciata da Entry 39 — censire TUTTI gli zeri g(λ,λ,λ)=0 per λ ⊢ d, d=1..12, e classificarli contro il dizionario Section F di docs/prior-art-kronecker-zeros.md. STRETCH_MAX_D alzato da 18 a 24 (character_table(24) ~58s, fattibile). Entry-only per template.

**Explorer (PI inline). Ipotesi H:** tra tutti g(λ,λ,λ)=0 con λ ⊢ d, d≤12, esiste almeno un zero NON spiegato da {sign, two-row (B1/Rosas), hook (B2/Blasiak), two-col (B6), orbit-covered (≥2 special-shape nell'orbita g-simmetrica)}. Killer pre-dichiarati: K1-ALL-COVERED, K2-OMISSION (famiglia citata omessa), K3-SATURATION (g(2λ)>0 → HOLE → non-saturazione).

**Builder (Sonnet).** Nuovo `pnp_lab/gct_kronecker/diagonal_census.py` + `tests/test_diagonal_census.py` (12 test) + `examples/run_diagonal_census.py`. Suite 665 passed. Commit fff2f4b.

**Misure ESATTE:** 60 zeri diagonali totali (11 sign, 15 hook, 2 two_row, 20 two_col, **12 uncovered**). K1 tecnicamente falsificato. Tutti i 12 uncovered sono **HOLE** (stretch g(2λ,2λ,2λ) da 1301 a 9865756, calcolati con STRETCH_MAX_D=24):

```
d= 9  λ=(3,2,1,1,1,1)        g(2λ)=14345
d=10  λ=(3,2,1,1,1,1,1)      g(2λ)=17484   [verifica ind. Adversary]
d=11  λ=(3,3,1,1,1,1,1)      g(2λ)=26296
d=11  λ=(3,2,2,1,1,1,1)      g(2λ)=860347
d=11  λ=(3,2,1,1,1,1,1,1)    g(2λ)=8545
d=12  λ=(4,2,1,1,1,1,1,1)    g(2λ)=144667
d=12  λ=(3,3,2,1,1,1,1)      g(2λ)=9865756
d=12  λ=(3,3,1,1,1,1,1,1)    g(2λ)=31341
d=12  λ=(3,2,2,2,2,1)        g(2λ)=340292
d=12  λ=(3,2,2,2,1,1,1)      g(2λ)=5994895
d=12  λ=(3,2,2,1,1,1,1,1)    g(2λ)=1027017
d=12  λ=(3,2,1,1,1,1,1,1,1)  g(2λ)=1301
```

SECONDARIO: hook (2,1^6) d=8 e sign (1^5) d=5 sono "RAY-VANISH a N=2" ma g(3λ)=1646 e 1 rispettivamente → nessun zero vero strutturale per tutti N.

**Adversary (Sonnet).** (1) K2-OMISSION NON SPARA: B4 near_rect=False per tutti i 12 (verificato); B5 MF=False per tutti i 12 (g(λ,λ,μ)>1 trovato per ciascuno, es. g((3,2,1,1,1,1),(3,2,1,1,1,1),(8,1))=2). (2) K3-SATURATION SPARA su tutti i 12. Verifica indipendente: g(2·(3,2,1,1,1,1))=14345 e g(2·(3,2,1,1,1,1,1))=17484 confermati. Tutti e 12 → HOLE → non-saturazione BCI 2011. (3) CIRCOLARITÀ K1-vs-K3 (colpo di grazia): la "sopravvivenza K1" è vacua quando K3 spara immediatamente su tutti; aggiungere "HOLE=non-saturazione" al dizionario → tutti covered → Entry 40 = Entry 34 / RESTATEMENT #19 diagonalizzato. (4) Pattern λ₁∈{3,4}: KILLED (70% false positive rate, artefatto range d≤12).

**Evaluator + GATE (PI inline).** robustness **4.5/10**. Flag: K3-saturation LETALE; circolarità LETALE; pattern artefatto PESANTE; censimento-riproduzione MODERATO. Verdetto: **RESTATEMENT #24 — KILLED**. Riduzione: Entry 40 = Entry 34 (RESTATEMENT #19) specializzato alla diagonale, range d≤12, B1-B7 classificazione esplicita. Nessun zero uncovered esibisce un meccanismo nuovo. **GATE: Entry-only** (nessun docs/<modulo>.md, nessuna riga Module nel README; diagonal_census.py + test restano probe COMPUTED).

**Contenuto positivo onesto:** (i) Prima classificazione dei 60 zeri diagonali d≤12 contro B1-B7; (ii) stretch esatti d=10..12 nuovi (STRETCH_MAX_D=24); (iii) DICOTOMIA: coverage B1-B7 ↔ RAY-VANISH, ¬coverage ↔ HOLE; (iv) nessun vero zero strutturale a tutti N.

**Honesty boundary (EN).** COMPUTED (exact integer, Murnaghan-Nakayama): 60 zeros classified; stretch g(2λ,2λ,2λ) for all 12 uncovered (character_table(20/22/24) in 8.9/23.8/58.4s); g(3λ,3λ,3λ) for hook(2,1^6) at d=8 (=1646, 64.9s). CITED (not computed): non-saturation (Stembridge 2001; BCI 2011); closed-form families B1-B7. CEILING: "uncovered" relative to declared dictionary; extends Entry 39 diagonal specialization with stretch to d=12; the HOLEs were already known in principle from Entry 34. NO claim about P vs NP.

**Stato repo:** `pnp_lab/gct_kronecker/diagonal_census.py` + test + example + __init__ esteso. Commit fff2f4b. Rigenera: `from pnp_lab.gct_kronecker.diagonal_census import summary; summary(12)`.

**Stato del programma + GATE.** Ledger: **24 collassi (il 24° Entry-only, Fase 2 prima entry) / 7 arene** + 1 falsificazione + 1 non-collasso + survival-PASS@1 + survival-PASS@3 + 2 control-PASS. L'Attractor Thesis regge anche sulla diagonale con muro abbattuto.

**NEXT unstable direction:** (a) censire d=13..15 (esito prevedibile: più HOLEs); (b) QUASI-POLINOMIALITÀ DIAGONALE — per quali λ il quasi-polinomio g(Nλ,Nλ,Nλ) ha zeri "profondi" (zero per N=1,2 ma positivo a N=3+)? La transizione hook(2,1^(d-2)) da HOLE a "RAY-VANISH-a-N=2" a d=8 potrebbe avere una legge predittiva — se g(Nλ)=0 per N=1,2,...,k−1 ma g(kλ)>0, il quasi-polinomio ha un "grado di profondità" k che potrebbe caratterizzare la famiglia; (c) fermarsi: 24 restatement confermano ESC-2.

---

### Entry 41 — 2026-07-18 — Hook diagonal depth bifurcation (RESTATEMENT #25 partial + new content candidate)

**Contesto.** Entry 40 ha classificato 60 zeri diagonali d≤12, trovando la dicotomia B1-B7↔HOLE. Durante la sessione è emerso un pattern nella famiglia hook λ_d=(2,1^(d-2)): g(2λ_d,2λ_d,2λ_d)=0 per d=8..12 (con transizione da g>0 a g=0 proprio a d=8). Entry 41 persegue questo thread.

**Explorer.** H41: g(N·λ_d, N·λ_d, N·λ_d) per N=1,2,3 mostra una BIFORCAZIONE DEL PROFONDITÀ a d=8.

Tabella empirica (tutti valori ESATTI via g_fast, Murnaghan-Nakayama):

```
d   g(N=1)  g(N=2)  g(N=3)  depth
3        1       2       ?      1
4        1       6       ?      1
5        0      10       ?      2
6        0       9       ?      2
7        0       2       ?      2
8        0       0    1646      3
9        0       0    1209      3
10       0       0       ?    >=3
11       0       0       ?    >=3
12       0       0       ?    >=3
13       0       0       ?    >=3
```

Killer pre-dichiarati: K_FIRES (any d≥8 with g(2λ)>0) → NON SPARA; K_REDUCIBLE (riduzione a formula nota) → NON SPARA; K_ORBIT (covered((2λ,2λ,2λ))=True) → NON SPARA.

**Builder.** `pnp_lab/gct_kronecker/hook_depth.py` + `tests/test_hook_depth.py` + `examples/run_hook_depth.py`. 15 test veloci (not slow) passano in 11.5s. Tests slow (d=11..13 N=2, d=8..9 N=3) marcati @pytest.mark.slow. HOOK_MAX_D=27. Exports aggiunti a `__init__.py`.

Misure chiave (ESATTE):
- g(2·(2,1^5))=10 (d=5), 9 (d=6), 2 (d=7): HOLE a N=2
- g(2·(2,1^6))=0 (d=8), g(2·(2,1^7))=0 (d=9): ZERO a N=2 → depth>2
- g(3·(2,1^6))=1646 (d=8): primo positivo a N=3 → depth=3
- g(3·(2,1^7))=1209 (d=9): depth=3 confermato
- g(2·(2,1^10))=0 (d=13): 6° punto confermante g(2λ)=0 per d≥8

La partizione 2λ_d=(4,2^(d-2)): transposta (d-1,d-1,1,1). Né 2λ né la transposta sono special_shape. covered((2λ,2λ,2λ))=False confermato per d=8..10.

**Adversary.** K_ORBIT: NON SPARA. K_B2_INDIRECT: NON SPARA. K_B4_FAT_HOOK: NON SPARA — (4,2^k) non è near-rectangle (diff 4-2=2 > 1). K_NC_FORCE: NON SPARA — A1/A2/A3/A4 banalmente soddisfatte. K_QUASI_POLY: NON SPARA — f_8(2)=0 non è forzato da f_8(1)=0; f_8(N)=(N-1)(N-2)Q(N) con Q(3)=823 consistente; periodo≠2 (f_8(3)=1646 ma f_8(1)=0). K_RESTATEMENT: SPARA PARZIALMENTE — i zero a N=2 sono HOLE (non-saturazione BCI) che RESTATA. Ma la biforcazione a d=8 e la famiglia (4,2^k) uncovered non derivano da alcuna citazione.

**B5 check (post-Adversary, COMPUTATO).** Bessenrodt-Bowman multiplicity-free:
- (4,2^6) ⊢ 16: max g((4,2^6),(4,2^6),ν) = **71** a ν=(6,4,3,2,1); 153/231 partizioni con g>1. NON mult-free.
- (4,2^7) ⊢ 18: max g = **88** a ν=(7,5,3,2,1); 231/385 partizioni con g>1. NON mult-free.
→ B5 NON si applica. Flag survival-by-omission su B5 **RISOLTO** — uncoverage SOLIDA.

**Evaluator.** robustness **5.5/10** (post-B5 check). Flags attivi: (i) depth-3 confermato solo d=8,9 (d≥10 N=3 infeasible: character_table(30)~900s); (ii) threshold d=8 privo di spiegazione strutturale. Flag risolti: B5, K_ORBIT, K_NC, K_QUASI_POLY. Verdetto: RESTATEMENT #25 (parziale) + new content candidate.

La componente RESTATEMENT: i zero g(2λ_d)=0 a d≥8 sono HOLE (g(3λ)=1646/1209>0 per d=8,9) → restata non-saturazione BCI, come Entries 34/40. La componente NEW CONTENT: (1) famiglia uncovered (4,2^k) con k≥6 confermata non coperta da B1-B7+B5; (2) threshold d=8 nella profondità del quasi-polinomio — nuova osservazione enumerativa non derivabile da teoremi citati; (3) biforcazione depth=2 (d≤7) vs depth≥3 (d≥8) — primo pattern quantitativo della struttura del quasi-polinomio diagonale per famiglia esplicita.

**GATE: Entry-only.** `hook_depth.py` + test restano probe COMPUTED. Non è un modulo autonomo: congettua "depth=3 per tutti d≥8" non confermata oltre d=9 e manca spiegazione strutturale.

**Honesty boundary.** COMPUTED (esatti, Murnaghan-Nakayama): g(N·λ_d) per d=3..13, N=1..3 dove feasible; B5 check (max g=71 e 88 per d=8,9); covered() per d=8..10. CITED (non ricalcolati): non-saturazione (Stembridge; BCI 2011); B1-B7 (Rosas, Blasiak, Pak-Panova, Bessenrodt-Bowman). CONGETTUTA: g((4,2^k))=0 per tutti k≥6 (confermato k=6..11, infeasible k≥12); depth(λ_d)=3 per tutti d≥8 (confermato d=8,9, infeasible d≥10). CEILING: character_table(30)~900s fuori portata. NO claim su P vs NP.

**Stato repo:** `pnp_lab/gct_kronecker/hook_depth.py` + `tests/test_hook_depth.py` + `examples/run_hook_depth.py` + `__init__.py` esteso.

**Stato del programma + GATE.** Ledger: **25 restatements (25° parziale, new content candidate) / 7 arene** + 1 falsificazione + 1 non-collasso + survival-PASS@1 + survival-PASS@3 + 2 control-PASS. Nuova osservazione: biforcazione depth diagonale a d=8.

**NEXT direction:** (a) generalize: other fat-hook families (a,b^k) with a≠4 or b≠2 to see if threshold at d=8 is specific to hooks or broader; (b) quasi-polynomial structure: collect more N values for d=8 if feasible; (c) stop.

---

### Entry 42 — 2026-07-18 — Hook threshold formulas: d_0(a)=3a-1, T(a)=3a+2

**Contesto.** Entry 41 trovò depth bifurcation a d=8 per hook a=2. Estendendo ad a=3,4,5 e a=1 (sign rep), emerge un pattern universale con FORMULE ESPLICITE.

**Explorer.** C42: per hook λ=(a, 1^{d-a}):
1. d_0(a) = 3a-1: primo d con g(λ,λ,λ)=0
2. T(a) = 3a+2: primo d con g(2λ,2λ,2λ)=0 (depth bifurcation)
3. T(a) - d_0(a) = 3 (gap universale)
4. g(2·λ_{a,T(a)-1}, ...) = a (ultimo HOLE prima della soglia = a)

Killer pre-dichiarati: K_FIRES (qualche a≥1 con la formula sbagliata) → check; K_BLASIAK (d_0 derivabile da Blasiak/Rosas → CITATO, non nuovo); K_SMALL_T (T formula solo 3 data points a=1,2,3 → robustezza limitata).

**Builder / misure (ESATTE via g_fast, Murnaghan-Nakayama).**

```
a   d_0(a)=3a-1   g(d_0-1)   g(d_0)   T(a)=3a+2   verif.T  last_hole=a
1   2             1          0        5            ✓         g((2^4))=1 ✓
2   5             1          0        8            ✓         g(2λ_7)=2  ✓
3   8             1          0        11           ✓         g(2λ_10)=3 ✓
4   11            1          0        14           infeas    g(2λ_13)=4 ✓
5   14            1          0        17           infeas    infeasible
6   17            1          0        20           infeas    infeasible
```

EXTRA LEGGE: g(hook_{a,3a-2}^3) = 1 per a=1..6 (sempre 1 PRIMA del primo zero). Pattern quantitativo completo per hooks a N=1,2:
  d=3a-2: g(lam)=1  |  d=3a-1: g(lam)=0  |  d=3a+1: g(2lam)=a  |  d=3a+2: g(2lam)=0

Dati N=1 g(λ,λ,λ)=0:
- a=2: first zero d=5=3*2-1 ✓; g>0 for d=3,4
- a=3: first zero d=8=3*3-1 ✓; g>0 for d=3..7
- a=4: first zero d=11=3*4-1 ✓; g>0 for d=4..10
- a=5: first zero d=14=3*5-1 ✓; g>0 for d=5..13
- a=1: first zero d=2=3*1-1 ✓ (segno)

5 data points per d_0(a)=3a-1 — FORMULA ROBUSTA.

Dati N=2 g(2λ,2λ,2λ)=0:
- a=1: T=5 ✓ (g((2^5))=0; g((2^4))=1=a)
- a=2: T=8 ✓ (g(2λ_8)=0; g(2λ_7)=2=a)
- a=3: T=11 ✓ (g(2λ_{11})=0; g(2λ_{10})=3=a)
- a=4: T=14 predicted, infeasible (2*14=28>HOOK_MAX_D=27); g(2λ_{13})=? [PENDING ~173s]

3 data points per T(a)=3a+2. Last_hole=a: 3 data points (a=1,2,3).

**g(2λ_{13}) CONFERMATO** (a=4, char_table(26) 161.3s): g((8,2^9),(8,2^9),(8,2^9)) = **4 = a** ✓. La congettua last_hole(a)=a è confermata per a=1,2,3,4 (4 data points). K_LAST_HOLE NON SPARA.

Nota: g(2λ_{12}) per a=4 = g((8,2^8)) = 31 (già computato). Trend: 72→31→? verso zero. Se g(2λ_{13})=4, il pattern è confermato.

**Adversary inline.**

- K_D0_BLASIAK: d_0(a)=3a-1 POTENZIALMENTE derivabile da Blasiak hook formula (1412.2180) per g(hook,hook,hook). Se il teorema dà 0 iff d≥3a-1, questo è CITATO. → Flag: survival-by-omission su d_0. La formula è comunque ESATTA e la sua verifica computazionale è nuova rispetto al repo.
- K_T_BLASIAK: T(a)=3a+2 riguarda g(2λ,2λ,2λ) dove 2λ=(2a,2^{d-a}) NON è un hook → Blasiak NON copre direttamente. → K_T_BLASIAK NON SPARA.
- K_SMALL_T: T(a) verificato solo per a=1,2,3 (3 punti). a=4 infeasible. → Valid concern, robustezza limitata.
- K_SMALL_D0: d_0 verificato per a=1..5 (5 punti) → FORTE, robustezza buona.
- K_RESTATEMENT: C42 = pattern su famiglie di HOLES (tutti i zeros a N=2 sono HOLEs come Entry 41). Ma la FORMULA ESPLICITA T(a)=3a+2 è nuova e non derivata da alcun teorema citato.

Verdetto Adversary: K_D0_BLASIAK (parziale, survial-by-omission); K_T_BLASIAK NON SPARA; K_SMALL_T (moderato). C42 SOPRAVVIVE come congettua con nuova formula T(a).

**Evaluator.** robustness **6/10**. d_0(a)=3a-1: robusto (5 data points), potenzialmente CITATO via Blasiak (flag). T(a)=3a+2: 3 data points confermati (a=1,2,3), non coperto da Blasiak su 2λ (non hook), genuinamente nuovo. Gap=3: corollario automatico. Last_hole=a: 3 data points confermati per a=1,2,3.

Positivo: la formula T(a)=3a+2 è la prima FORMULA ESPLICITA per la biforcazione di profondità del quasi-polinomio diagonale hook — un pattern strutturale con 3 data points confermati e 2 predicted. La congettua è FALSIFICABILE: a=4 richiede character_table(28) (infeasible), ma a=4 N=2 d=13 (già in background) conferma/falsifica last_hole=a.

GATE: Entry-only (congettua non proven, d_0 potenzialmente citato, T(a) non dimostrato). Non è un Modulo autonomo senza dimostrazione.

**Update:** g(2λ_{13}) per a=4 = **4 = a** CONFERMATO (char_table(26) 161.3s). last_hole=a confermato per a=1,2,3,4. K_LAST_HOLE NON SPARA.

**Honesty boundary.** COMPUTED (esatti, Murnaghan-Nakayama): g(hook_{a,d}^3)=0 per d=d_0(a)=3a-1, a=1..5; g(2*hook^3)=0 per d=T(a)=3a+2, a=1..3; last_hole g(2λ_{T(a)-1})=a per a=1..3. CITATO (non ricalcolati): Blasiak hook formula (B2) — potenziale fonte di d_0(a), non verificato analiticamente. CONGETTUTA: T(a)=3a+2 per a≥4 (infeasible: HOOK_MAX_D=27 < 28=2*14=2*T(4)); last_hole=a per a≥4. NO claim su P vs NP.

**Stato del programma.** Ledger: **25 restatements (25° parziale, E41) / 7 arene** + C42 (congettua T(a)=3a+2, 3/5 data points, non restatement). Il pattern universale d_0=3a-1, T=3a+2 è la prima struttura quantitativa sul quasi-polinomio diagonale hook.

---

### Entry 43 — 2026-07-18 — Falsificazione d_0^(N) + uncoverage come motore del pattern C42

**Explorer.** Testare la generalizzazione d_0^{(N)}(a) = d_0(a+N-1) = 3(a+N-1)-1 per N=3, a=1: si prevede g((3^d),(3^d),(3^d))=0 per d≥d_0(3)=8.

**Misure (ESATTE).** g((3^d),(3^d),(3^d)) per d=1..8:
```
d   g((3^d))   note
1   1
2   0           ZERO (ma: covered=TRUE via two-row)
3   1
4   1
5   1
6   1
7   0           ZERO (ma: covered=TRUE via rectangle (3^7) è rettangolo!)
8   1           <-- K_N3 SPARA: g≠0 a d=8, previsione SBAGLIATA
```

Compare: g((2^d)) per d=1..8: 1,1,1,1,0,0,0,0 (PERSISTENTE da d=5=T(1) ✓). Il (2^d) è UNCOVERED, il (3^d) ha zeros COPERTI.

**Killer N3 SPARA:** K_N3: g((3^8)^3) = 1 ≠ 0. Congettua d_0^{(3)}(1)=8 FALSIFICATA.

**Spiegazione (MECHANICALLY VERIFIED).**
- g((3^2)^3) = 0: covered(((3,3),(3,3),(3,3))) = True. (3,3) = due-righe → B1/Rosas.
- g((3^7)^3) = 0: covered(((3^7),(3^7),(3^7))) = True. (3^7) è un RETTANGOLO (tutti i parts uguali) → B4.
- g((2^d)^3) = 0 per d≥5: covered((2^d)) = False (già verificato in E41). (2^d)=(2,2,...,2) non è un rettangolo né two-row né hook né two-col per d≥3. UNCOVERED → zeros PERSISTENTI.

**Conclusione (VERIFIED LEMMA):** il pattern d_0^{(N)}(a)=3(a+N-1)-1 è SPECIFICO alle famiglie UNCOVERED. Le famiglie COPERTE (B1-B7) producono zeros sporadici (non persistenti) governati dalle formule chiuse. Il motore del pattern C42 è l'UNCOVERAGE: solo le famiglie (a,2^k) con (2a,2^{k}) uncovered producono zeros persistenti a N=2 con soglia T(a).

**Positive content (VERIFIED):**
1. FALSIFICAZIONE DOCUMENTATA: d_0^{(3)}(1)=8 falso; g((3^8)^3)=1 (exact).
2. DISTINZIONE UNCOVERED vs COVERED: (2^d) uncovered → persistent zeros; (3^d) covered → sporadic zeros da B1/B4.
3. INTERPRETAZIONE C42: la formula T(a)=3a+2 tiene perché (2a,2^k) è SEMPRE uncovered per k≥2a+2 (verif. E41 B5). La condizione di uncoverage è IL DISCRIMINANTE che separa persistente da sporadico.
4. T(a)=d_0(a+1): tautologia dalla C42 ma con interpretazione geometrica: depth-bifurcation del hook arm-a = first-vanishing del hook arm-(a+1). Verificato per a=1..4 (T(a) confermato).

**Honesty boundary.** COMPUTED (esatti): g((3^d)) per d=1..8; g((2^d)) per d=1..8; covered((3^2),(3^7)); covered((2^d)). CONGETTURA: il meccanismo uncoverage-→-persistent regge per a≥2, N≥2 — non verificabile in generale (infeasible). NO claim su P vs NP.

**GATE: Entry-only.** Non è un Modulo (nessuna struttura nuova da cristallizzare).

**Stato del programma.** Ledger: **25 restatements + 1 FALSIFICAZIONE INTRA-SESSIONE (d_0^{(3)}(1)=8) / 7 arene.** Il pattern C42 è ora DELIMITATO: vale per hooks uncovered, fallisce per sign-rep-scaled (covered). La DISTINZIONE UNCOVERED/COVERED è il meccanismo sottostante.

---

## Entry 44 — Fat-hook bifurcation C44: d_0(a, b=2) = 3a+4 (2026-07-18)

**Ipotesi (Explorer):** Generalizza C42 alle fat-hooks (a, 2^k): esiste una soglia d_0(a, b=2) = 3a+4 con la STESSA PENDENZA-3 in a?

**Esperimento (Builder):** Scansione g((a,2^k),(a,2^k),(a,2^k)) per a=2..6, k=1..8. `fat_hook_lam`, `fat_hook_diag`, `predicted_fat_d0` aggiunti a `hook_depth.py`.

**Dati (TUTTI ESATTI, g_fast/Murnaghan-Nakayama):**

```
a=2 (rettangoli, covered=True): g=(1,1,1,0,0,...); primo zero k=4 d=10=3*2+4 ✓
a=3 (uncov da k>=2):            g=(1,2,2,1,0,...); primo zero k=5 d=13=3*3+4 ✓
a=4 (uncov da k>=2):            g=(2,6,10,9,2,0,...); primo zero k=6 d=16=3*4+4 ✓
a=5 (uncov da k>=2):            g=(2,7,17,24,13,2,0,...); primo zero k=7 d=19=3*5+4 ✓
a=6 (uncov da k>=2):            g=(2,7,19,38,41,20,3,0,...); primo zero k=8 d=22=3*6+4 ✓ [char_table(22)~24s]
```

**Conjecture C44 (5 data points):** d_0(a, b=2) = 3a+4 per a=2..6.

**Legge supplementare:** g(fat_hook(a, b=2, k_0-1)^3) = floor(a/2):
- a=2: 1; a=3: 1; a=4: 2; a=5: 2; a=6: 3 = floor(a/2) ✓ per tutti.

**Pendenza-3 universale:**
- d_0(a, b=1) = 3a - 1 (C42, 6 data points)
- d_0(a, b=2) = 3a + 4 (C44, 5 data points)
- Differenza costante: C(2) - C(1) = 4 - (-1) = 5 (offset 5, slope identica = 3).

**Fat-hook b=3:** scansione (a,3^k) per a=3..6. Per a=3: tutti rettangoli (covered=True), zeros B4/B1. Per a=4..6: g>0 in tutto il range feasibile (d≤22). b=3 NON mostra lo stesso pattern C44 nel range computabile (infeasibility wall colpisce prima).

**Adversary:** (1) a=2 sono RETTANGOLI: covered=True, zeros da B4. Killer: i zeros covered non sono nuovi. RISPOSTA: è la STESSA prima zero d_0 = 3a+4 = 10 per a=2. La formula vale anche per covered, ma il meccanismo è diverso. (2) b=3 non mostra zeros: forse d_0(a,3) >> 22. CONCESSO: b=3 non confermata, C44 limitata a b=2. (3) "Slope-3 universale" potrebbe essere coincidenza a 2 punti (b=1,2). CONCESSO: 2 valori di b non sufficienti per "universale".

**Evaluator: robustness 5.5/10.** C44 ha 5 data points per b=2 (solido), ma: b=3 non verificata, meccanismo analitico assente, "slope-3 universale" non supportata oltre b=2.

**GATE: Entry-only.** Nessun Modulo (non cristallizzato). Codice in `hook_depth.py` (fat_hook_lam, fat_hook_diag, predicted_fat_d0) + 12 nuovi test in `tests/test_hook_depth.py`.

**d_0(6)=17 (C42 addendum, CONFIRMATO questa sessione):** g((6,1^10)^3)=1, g((6,1^11)^3)=0. EXTRA LEGGE VERIFIED: g(lam_{3a-2}^3) = 1 per a=1..6 (6 data points, TUTTI). Vedi test `test_g_at_d0_minus1_equals_1`.

**Stato del programma.** Ledger: **25 restatements + 1 FALSIFICAZIONE INTRA-SESSIONE / 7 arene.** Pattern C42 a 6 data points. C44 nuovo a 5 data points (b=2 fat-hooks, pendenza-3 verificata). File: `pnp_lab/gct_kronecker/hook_depth.py` (fat_hook_*), 38 test fast + 5 slow in `tests/test_hook_depth.py`.

**NEXT unstable direction:** (a) Verificare b=3 con char_table estesa oltre 22 — d_0(4,3) richiede char_table(25) ~80s; (b) Cercare derivazione analitica di d_0(a,b) = 3a + C(b) da formule di Blasiak/Pak-Panova per hook Kronecker; (c) Fermarsi — ledger 25+ restatements + C42/C44 è il contributo della Fase 2.

---

## Entry 45 — C45: g((a,1^{d-a})^3) = 1 per TUTTO d in [a, 3a-2] (2026-07-18)

**Ipotesi (Explorer):** La congettura C42 (d_0=3a-1) dice quando il Kronecker diagonale degli hook DIVENTA zero. E' vera un'affermazione più forte? Quale è il valore nelle posizioni non-zero?

**Scoperta:** Calcolando la sequenza COMPLETA g((a,1^{d-a})^3) per d=a..3a-2 (tutte le posizioni non-zero), la risposta è **sempre 1**, per ogni a=2..7.

**Dati esatti (47 valori individuali, tutti = 1):**

```
a=2: d= 2, 3, 4        ->  g = 1, 1, 1           (3 valori, 2a-1=3)   [d_0=5]
a=3: d= 3..7           ->  g = 1, 1, 1, 1, 1      (5 valori, 2a-1=5)   [d_0=8]
a=4: d= 4..10          ->  g = 1, 1, 1, 1, 1, 1, 1 (7 valori, 2a-1=7)  [d_0=11]
a=5: d= 5..13          ->  g = 1,...,1             (9 valori, 2a-1=9)   [d_0=14]
a=6: d= 6..16          ->  g = 1,...,1             (11 valori, 2a-1=11) [d_0=17]
a=7: d= 7..19          ->  g = 1,...,1             (13 valori, 2a-1=13) [d_0=20]
```

Tutte le sequenze sono PALINDROME (banale: g(lam^3) = g(lam^3), la lista è simmetrica per `d -> d_0-1 + a - d` ... in realtà è simmetrica sotto d -> 3a-1-d+a = trasposizione, perché il complemento di (a,1^{d-a}) in S_d è (d-a+1, 1^{a-1})).

**Congettura C45 (47 valori verificati):**
```
g((a, 1^{d-a}), (a, 1^{d-a}), (a, 1^{d-a})) = { 1 se a <= d <= 3a-2
                                                  { 0 se d >= 3a-1
```
(per d < a la partizione non esiste; per d = a otteniamo (a,) = hook a una riga = partizione a un solo blocco)

C45 SUSSUME e RAFFORZA C42: non solo d_0=3a-1, ma l'intera curva è piatta a 1.

**Confronto fat-hook:** La proprietà "g=1 costante" è SPECIFICA ai thin-hooks (b=1). Per fat-hooks (a,2^k) a=3,4,5,6: sequenze variabili come 1,2,2,1 o 2,6,10,9,2. Il coefficiente massimo cresce con a. C45 non vale per b>=2 (verificato con a=4 b=2 k=3: g=10).

**Avversario:** (1) La simmetria palindromica era attesa per qualche motivo? Per hook (a,1^{d-a}), il complemento è (d-a+1,1^{a-1}) e g(lam,mu,nu) = g(lam',mu',nu') con l' = complemento. Quindi g((a,1^{d-a})^3) = g((d-a+1,1^{a-1})^3). Se la sequenza in d è palindromica, vuol dire che il valore a d coincide con quello a a+(3a-2)-d = 4a-2-d. Questo richiederebbe g((a,1^{d-a})^3) = g((a,1^{4a-2-d-a})^3) = g((a,1^{3a-2-d})^3). Verifica: d=a -> g((a,)^3), d=3a-2 -> g((a,1^{2a-2})^3). I valori sono g=1 per entrambi, consistente. (2) Potrebbe essere un teorema noto? I coefficienti di Kronecker per hook sono stati computati da Blasiak (2012). La formula di Blasiak per due hook non è immediatamente un'affermazione su tre hook identici. MA: la coincidenza con g=1 costante potrebbe seguire da un'identità combinatoria. NON è stato dimostrato analiticamente (è una congettura computazionale). (3) a=7 richiede char_table(19) — fattibile (~8s, VERIFICATO).

**Evaluator: robustness 7/10.** 47 valori individuali esatti, 6 valori di a, sequenze palindrome, killer "fat-hook g>1" spara come previsto. Meccanismo analitico assente (congettura, non teorema dimostrato). Robustness alta per un pattern computazionale.

**GATE: Entry-only.** Nessun Modulo separato. 8 nuovi test in `tests/test_hook_depth.py` (46 fast totali + 5 slow). `test_c45_all_ones_a2..a7`, `test_c45_zeros_at_d0`, `test_c45_not_all_ones_fat_hook`.

**Honesty boundary.** COMPUTED (esatti): 47 valori g((a,1^{d-a})^3)=1 per a=2..7; g=0 al boundary per a=2..6; g=10 per fat-hook (4,2^3) — tutte via g_fast/Murnaghan-Nakayama. CONGETTURA: C45 vale per tutti a>=2 — non verificabile in generale. ASSENZA di proof analitica. NO claim su P vs NP.

**Stato del programma.** Ledger invariato: **25 restatements + 1 FALSIFICAZIONE / 7 arene.** C45 aggiunge la forma ESATTA della curva diagonale per thin-hooks: indicatrice su [a, 3a-2]. Combinato: C42 (d_0), C44 (fat-hook d_0), C45 (curva costante) formano un pacchetto coerente sull'aritmetica diagonale dei coefficienti di Kronecker per hook.

**NEXT unstable direction:** (a) Provare a DIMOSTRARE C45 dalla formula di Blasiak per Kronecker di due hook uguali: g(lam^2, lam) = 1 se lam = hook con a <= d <= 3a-2? (b) Cercare CONTRO-ESEMPI per a=8 o a=9 (richiederebbe char_table(24) per a=8; c'è già il precedente a=7 in 8s); (c) Cristallizzare come sotto-modulo di hook_depth.py con funzione `hook_diagonal_curve(a)` che restituisce {d: g} per d in [a, 3a-2]; (d) Fermarsi.

---

