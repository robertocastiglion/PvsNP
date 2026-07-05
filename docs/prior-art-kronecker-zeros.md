# Prior art — vanishing dei coefficienti di Kronecker (CICLO 0a, "Kronecker Beyond the Wall")

**Data:** 2026-07-05. **Autore:** Strategist (Fable 5), ricognizione con web search.
**Scopo:** questo file È il dizionario contro cui l'Adversary uccide. Un vanishing a d=7..9 può
essere dichiarato "genuinamente sporadico" SOLO se sopravvive a OGNI criterio/famiglia elencata
qui. Se un criterio noto manca da questo elenco, ogni claim di sporadicità è survival-by-omission
(firma Entry 32/33/36).

## A. Condizioni necessarie / criteri di vanishing IMPLEMENTABILI ESATTAMENTE

| # | Criterio | Fonte (CITED) | Stato nel repo |
|---|---|---|---|
| A1 | Lunghezza: `g>0 ⟹ ℓ(λ) ≤ ℓ(μ)·ℓ(ν)` (e permutazioni) | Dvir 1993; Clausen–Meier | **IMPLEMENTATO** `kronecker.nc_length` |
| A2 | Prima riga (Dvir): `g>0 ⟹ λ₁ ≤ |μ ∩ ν|` (intersezione dei diagrammi; e permutazioni) | Dvir 1993, Thm 1.6 | **IMPLEMENTATO** (variante) `kronecker.nc_maxpart` — verificare che sia la forma piena di Dvir, non un rilassamento |
| A3 | Triangolare/prima riga: `λ₁ ≥ μ₁+ν₁−d` e permutazioni ("first-row bound") | Klyachko 2004; Christandl–Mitchison 2006 | **COMPUTED** in Entry 35 (faccette P_3); da promuovere a checker esplicito |
| A4 | Cono dei momenti (membership, inner approx a scala fissa) | Klyachko/Horn; repo Entry 35 | **IMPLEMENTATO** `moment_cone.in_cone` (inner approx, non il cono vero) |
| A5 | Stretching/saturazione: `g(λ,μ,ν)=0` ma `g(N·)>0` = buco di non-saturazione (diagnostica, non criterio) | Stembridge; Bürgisser–Christandl–Ikenmeyer 2011 | **IMPLEMENTATO** `saturation.stretch` (N≤4) |
| A6 | Parità/contenuto banale: `g(λ,μ,ν)` con vincoli di segno del carattere su classi (es. colonna non-vanishing sse classe pari) | letteratura caratteri S_d | CITABILE; non checker diretto di g |

## B. Famiglie a FORMA CHIUSA con criterio di zero esatto (il dizionario `covered`)

| # | Famiglia | Fonte (CITED) | Stato nel repo |
|---|---|---|---|
| B1 | μ, ν two-row: formula chiusa / quasi-polinomiale, zeri espliciti | Rosas 2001 ([two-row/hook](https://arxiv.org/abs/math/0001084)); Briand–Orellana–Rosas ([0812.0861](https://arxiv.org/abs/0812.0861)) | parz. in `coverage.covered` (Entry 30) |
| B2 | μ o ν hook: regola combinatoria semplificata, zeri espliciti | Rosas 2001; Blasiak ([1412.2180](https://arxiv.org/abs/1412.2180)) | parz. in `coverage.covered` |
| B3 | std⊗std e prodotti con [d−1,1] | elementare (Entry 30) | in `coverage.covered` |
| B4 | Rettangoli e near-rectangles: formule/criteri espliciti | Bessenrodt–Behns; Bessenrodt–Bowman 2017; Tewari ([near-rectangular](https://www2.math.upenn.edu/~vvtewari/Kronecker-v2.0.pdf)); Manivel; BCI 2011 (quadrati, GCT) | parz. in `coverage.covered`; near-rectangles PROBABILMENTE MANCANTI |
| B5 | Prodotti multiplicity-free (classificazione completa) ⇒ zeri strutturali nei prodotti classificati | Bessenrodt–Bowman ([1609.03596](https://arxiv.org/abs/1609.03596)) | NON implementato; implementabile (classificazione finita) |
| B6 | λ due colonne / hook + a,b: classificazione completa della positività | Pak–Panova e coautori (two-column/hook) | NON implementato; CITABILE |
| B7 | Doppi hook: `λ` fuori da ogni double hook con μ hook, ν two-row ⟹ g=0 | Rosas 2001 | parz. coperto da B1/B2 |

## C. Contesto (CITED, non checker)

- **Hardness:** decidere `g>0` è NP-hard (Ikenmeyer–Mulmuley–Walter); calcolare g è #P-hard /
  GapP-completo ([complexity](https://dmtcs.episciences.org/3622/pdf); [positività caratteri ≥ PH](https://arxiv.org/abs/2207.05423)).
  ⇒ NESSUN criterio generale può esistere (se le classi non collassano): la lista B è
  necessariamente incompleta per ragioni strutturali. Questo è il motivo per cui uno "sporadico
  genuino" a d piccolo non contraddice nulla — ma anche il motivo per cui la sporadicità è
  SEMPRE relativa al dizionario dichiarato.
- **Riduzione:** ogni Kronecker è un Kronecker ridotto ([Cambridge/Forum Pi](https://www.cambridge.org/core/journals/forum-of-mathematics-pi/article/all-kronecker-coefficients-are-reduced-kronecker-coefficients/8D984A05F46D4690E6E994854972AE37)) — le tavole ridotte coprono le non-ridotte.
- **Kronecker simmetrici rettangolari:** buchi nel semigruppo, vanishing infiniti ([Springer 2019](https://link.springer.com/article/10.1007/s13366-019-00466-7)) — oggetto AFFINE ma distinto (variante simmetrica).

## D. Tavole e dataset già pubblicati (rischio-riproduzione, DICHIARATO)

- **Dataset ML:** coefficienti computati per **6 ≤ n ≤ 20** (con estensioni condizionali oltre)
  in [Interpretable ML for Kronecker](https://arxiv.org/abs/2502.11774); dataset analoghi in
  [Machine-Learning Kronecker Coefficients](https://arxiv.org/abs/2306.04734) (classificazione
  zero/non-zero, accuracy ~0.98–0.99, bound di precisione ~85% per feature 1-D).
- **Tavole:** Coquereaux–Zuber, *Conjugation properties of tensor product multiplicities*,
  J. Phys. A 47 (2014) 455202 (tavole per n piccoli).
- ⇒ Il CENSIMENTO numerico d=7..9 è RIPRODUZIONE di dati già esistenti altrove (e di ciò che
  SageMath/Mathematica calcolano di routine). Il contenuto potenzialmente nuovo NON è il
  censimento ma la **classificazione covered-vs-uncovered contro il dizionario A+B completo**:
  nelle ricerche condotte NON risulta pubblicata una classificazione esaustiva degli zeri di
  d=7..9 per famiglie note. (Se l'Adversary la trova, KILLER-0 spara retroattivamente.)

## E. Verdetto KILLER-0 (gate del ciclo 0a)

**KILLER-0 NON SPARA**, con riserva: (i) le tavole esistono ⇒ il censimento è riproduzione e va
dichiarato tale nell'honesty boundary; (ii) la classificazione covered/sporadic a d=7..9 non
risulta pubblicata ⇒ il discriminante del ciclo 1 è legittimo; (iii) OBBLIGO derivato: prima di
dichiarare "sporadico genuino" un vanishing, `coverage.covered` va ESTESO ad A2-pieno, A3, B4
(near-rectangles), B5 (multiplicity-free) — altrimenti l'esito è survival-by-omission per
costruzione. La lista A+B è il dizionario minimo; l'Adversary ha mandato di cercare criteri
mancanti PRIMA di validare qualunque sopravvivenza.

**NO claim about P vs NP.**
