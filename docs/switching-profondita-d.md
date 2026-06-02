# Switching iterato in profondità *d* — chiudere quantitativamente «parità ∉ AC⁰»

*Filone di ricerca implementato il 2026-06-02. Estende il Modulo 8 (Switching
Lemma Lab) dal singolo livello all'induzione completa di Håstad.*

## Obiettivo

Il Modulo 8 «base» applicava **una** restrizione casuale e mostrava che una DNF
(profondità 2) si appiattisce, mentre la parità no. Questo passo concatena lo
switching **livello dopo livello** su un vero circuito AC⁰ di profondità *d*, per:

1. far **collassare** l'intero circuito, una restrizione per livello;
2. mostrare che la parità, sotto le **stesse** restrizioni, **non collassa mai**;
3. **chiudere quantitativamente** la separazione parità ∉ AC⁰.

## Cosa viene eseguito (in modo esatto)

- `circuit.py` — un **circuito AC⁰ concreto** a livelli alternati ∧/∨, con
  fan-in al fondo *w*, valutato in modo esatto sulla tabella di verità.
  `parity_as_dnf(n)` costruisce la parità come DNF canonica (2^(n-1) mintermini di
  larghezza *n*): il «muro» a profondità 2.
- `iterate.py` — il **motore iterato**. Ad ogni round applica una nuova
  restrizione alle variabili ancora libere (cumulativa) e rimisura la **profondità
  dell'albero di decisione ottimo** della funzione superstite. La novità di rigore:
  `iterate_collapse_joint` valuta circuito e parità sotto la **medesima** ρ, così
  il numero di variabili libere è identico e l'invariante «D(parità) = #liberi»
  è **esatto**, non statistico.

### Risultato misurato (n = 50, d = 3, w = 2, schedule p = 0.18, 400 trial)

| round | #liberi | D(AC⁰) | D(parità) | collasso AC⁰ |
|------:|--------:|-------:|----------:|-------------:|
|   1   |  8.77   |  0.57  |   8.77    |     85 %     |
|   2   |  1.53   |  0.06  |   1.53    |     99 %     |

A ogni round **D(parità) = #liberi** *esattamente* (stessa ρ): la parità resta
sulla diagonale, deve leggere **tutte** le variabili superstiti. L'AC⁰ invece
cade sotto la diagonale e collassa al ~99 %. La visualizzazione onesta è il
rapporto **D ÷ #liberi**: parità ≡ 1.0 (retta piatta), AC⁰ → 0
(`web/assets/switching_iterated.svg`).

### La parità non collassa — invariante verificato

`test_parity_dt_depth_equals_free_vars_exact` controlla, su 40 restrizioni
casuali, che `D(parità|ρ) == numero di variabili libere`, **esattamente**. Non ci
si fida del teorema: lo si esegue.

## La chiusura quantitativa

`parity_lower_bound(n, d)` esegue la parte **finita** del conto di Håstad:

- con *d−1* restrizioni che tengono ogni variabile con prob. *p*, sopravvivono in
  media **n·p^(d−1)** variabili libere;
- lo switching fa collassare un AC⁰ di fan-in *w* quando **5·p·w < 1**, cioè
  *w < 1/(5p)*;
- la parità sulle *k* superstiti ha profondità DT = *k*, sempre.

Perché la parità **non** collassi servono superstiti *k > 0* mentre l'AC⁰ è già
piatto: imponendo *p = 1/(5w)* e *n·p^(d−1) > w* si ottiene la soglia

> **n ≳ 5^(d−1) · w^d**   ⟹   **size ≥ 2^Ω(n^(1/(d−1)))**.

Esempio (n = 1000, d = 3): superstiti attese ≈ 3.42, soglia di fan-in ≈ 3.42,
dimensione minima ≈ 2^3.16.

## Confine di onestà

- **Eseguito ed esatto**: la costruzione del circuito AC⁰, il collasso iterato
  livello dopo livello, la sopravvivenza della parità (invariante esatto) e la
  parte finita del conto quantitativo.
- **Citato**: la **costante asintotica** della forma `2^Ω(n^(1/(d−1)))` è il
  teorema di Håstad (1986/1987). Non la deriviamo da capo: la richiamiamo.
- **Nessun risultato nuovo**: questo è un *lower bound che funziona davvero*, ma
  contro una **classe ristretta** (AC⁰). Non tocca P vs NP — anzi, è proprio una
  delle tecniche che, da sole, cadono nelle barriere (è una proprietà «naturale»
  ai sensi del Modulo 1). Resta un esercizio di rendere **eseguibile e
  verificabile** un meccanismo profondo, in linea con tutto il toolkit.

## File

```
pnp_lab/switching/circuit.py      # circuito AC⁰ concreto + parity_as_dnf
pnp_lab/switching/iterate.py      # motore iterato, joint, conto quantitativo, SVG
tests/test_iterate_switching.py   # 10 test (esatti)
examples/run_switching.py         # demo (sezione "switching iterato")
web/assets/switching_iterated.svg # traiettoria del collasso
```
