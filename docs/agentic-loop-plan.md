# Piano dell'agentic loop: routing dei modelli, tecniche di prompting, guardrail token

Questo documento è il risultato di uno studio (2026-09-04) sulle tecniche di prompting
più efficaci per il ragionamento matematico con LLM e sulle strutture di agentic loop
con controllo dei costi. Definisce il piano operativo applicato al loop del PvsNP-lab
(`prompts/research-loop.md` + `.claude/agents/*.md`).

## 1. Evidenze dallo studio

### Tecniche di prompting efficaci per il ragionamento matematico
- **Verifica > generazione.** Addestrare/usare un verificatore che ri-classifica le
  soluzioni migliora il solve-rate più che potenziare il solo generatore. Nel loop il
  verificatore è l'Adversary: deve avere un modello almeno forte quanto l'Explorer.
- **Plan-and-Solve.** Far pianificare esplicitamente (oggetti, grandezze, teoremi
  rilevanti) prima di risolvere riduce gli errori da passi mancanti e di calcolo su
  MATH/GSM8K. Applicato all'Explorer.
- **Draft-Sketch-Prove.** Scomporre in uno sketch di passi verificabili uno per uno,
  poi verificarli formalmente/esattamente. Nel lab: sketch dell'Explorer, verifica
  esatta del Builder passo per passo (test-first).
- **Multi-agent debate, ma limitato.** Un round di critica-replica migliora il
  ragionamento e riduce le allucinazioni; round ulteriori danno guadagni decrescenti a
  costo token pieno. Applicato: l'Adversary conduce un solo round e lascia una singola
  obiezione residua per il ciclo successivo.
- **Anti-overthinking.** Sui modelli piccoli, forzare ragionamento esteso su task
  semplici PEGGIORA le prestazioni. Applicato: l'Archivist (haiku) ha mandato
  esplicitamente meccanico, senza ri-analisi.
- **Killer pre-dichiarato.** La pratica del lab (predizione + killer dichiarati prima
  di misurare) coincide con la letteratura su verifica e falsificabilità: mantenuta
  come tecnica portante, non modificata.

### Strutture di agentic loop e costi
- I sistemi multi-agente consumano ~15x i token di una chat singola (dato Anthropic):
  senza budget duri il costo scala con ogni iterazione.
- Best practice consolidate: budget token per agente e per workflow applicati in modo
  deterministico PRIMA della chiamata; circuit breaker (halt, non retry) al
  superamento; orchestrator-worker con contesto minimo passato ai worker; plan-and-
  execute per ridurre il numero di chiamate; caching dei risultati già letti.
- Sotto budget di ragionamento uguale, un singolo agente forte batte spesso un
  multi-agente su reasoning multi-hop: il multi-agente si giustifica solo dove i ruoli
  sono separati per mandato (qui: chi genera ≠ chi valuta, che è il fondamento di
  onestà del lab — quindi la struttura multi-agente resta, ma con ruoli minimi).

## 2. Routing dei modelli per ruolo

| Ruolo | Modello | Perché |
|---|---|---|
| strategist | opus | Decisioni di merito rare e ad alto impatto; poche chiamate per ciclo. |
| explorer | opus | La creatività matematica dell'ipotesi è il collo di bottiglia della qualità. |
| builder | sonnet | Implementazione codice: sonnet è forte sul codice a costo molto minore. |
| adversary | opus | Il verificatore deve essere ≥ del generatore (evidenza chiave dello studio). |
| evaluator | sonnet | Sintesi strutturata di attacchi già condotti: rubrica, non creatività. |
| archivist | haiku | Trascrizione meccanica; il ragionamento qui è dannoso oltre che costoso. |

Upgrade puntuale: ai gate ROSSO con candidato NEW CONTENT o a ESC-1 lo strategist può
essere invocato con override `model: fable` per la singola decisione critica.

## 3. Guardrail token (riassunto; testo vincolante in prompts/research-loop.md)

- T1: una invocazione per ruolo per ciclo; solo il builder ha max 2 riparazioni interne.
- T2: contesto minimo in ingresso ai subagenti (direzione + puntatore all'ultima entry
  del log); mai incollare interi file nel prompt.
- T3: output cap per ruolo (40/40/30/30/10 righe); sfondare il cap = overthinking.
- T4: builder INCONCLUSIVE dopo i cap → il ciclo chiude INCONCLUSIVE, nessun rilancio.
- T5: stato ricostruito dalla coda del log e dall'indice memory/MEMORY.md, non da
  letture integrali.

Questi si sommano ai breaker già esistenti del gate graduato (B1: max 3 cicli VERDI;
B2: stop al primo RESTATEMENT; B3: ogni ciclo committato e loggato).

## 4. Cosa NON è cambiato

- La separazione chi-genera ≠ chi-valuta e tutti i guardrail di onestà.
- Il gate graduato VERDE/ROSSO/R-ESC e il LIMITE ASSOLUTO (nessun claim P vs NP).
- Il criterio di "risultato rilevante" e la sezione Honesty boundary.

## Fonti dello studio

- [Anthropic — How we built our multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system)
- [Plan-and-Solve Prompting](https://learnprompting.org/docs/advanced/decomposition/plan_and_solve)
- [LLM-Based Theorem Provers (survey)](https://www.emergentmind.com/topics/llm-based-theorem-provers)
- [APOLLO: Automated LLM and Lean Collaboration](https://arxiv.org/pdf/2505.05758)
- [Single-Agent LLMs Outperform Multi-Agent Systems under Equal Thinking Token Budgets](https://arxiv.org/pdf/2604.02460)
- [BAMAS: Structuring Budget-Aware Multi-Agent Systems](https://arxiv.org/pdf/2511.21572)
- [Token Economics for LLM Agents](https://arxiv.org/html/2605.09104v1)
- [Adaptive heterogeneous multi-agent debate](https://link.springer.com/article/10.1007/s44443-025-00353-3)
- [Mutual Reasoning Makes Smaller LLMs Stronger Problem-Solvers](https://arxiv.org/pdf/2408.06195)
- [The Multi-Agent Trap](https://towardsdatascience.com/the-multi-agent-trap/)
