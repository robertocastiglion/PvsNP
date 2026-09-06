# STATE — PvsNP-lab Fase 2 "Perseverance Run"

## Sessione corrente

**Data:** 2026-09-06
**Entry completate (totale arc):** 40–76
**Stato:** DECISIONE-B1 ONORE: filone QA-engine3 CHIUSO (Entry 76 — circolarità astratta irriducibile con 3 vincoli, pratica chiusa operativamente)

---

## Ultimo stato — Entry 64 CHIUSO

### Arc hook-diagonal (Entries 40–48, sessioni precedenti):
Programma COMPLETO. Congetture cristallizzate e callable:

```
hook_depth.py (HOOK_MAX_D=27):
  predicted_d0(a)     = 3a-1   (C42)
  predicted_T(a)      = 3a+2   (C42)
  last_hole_value(a)  = a      (C42)
  predicted_fat_d0(a,2) = 3a+4 (C44)
  hook_diagonal_curve(a)       (C45: g=1 per d in [a,3a-2])
  stable_kronecker_b2(k)       (C47: 1,2,7,21k-44 per k>=3)
```

Test suite: 56 fast + 12 slow = 68 test. Ledger entrata: 26 restatements.

---

## Arc Kronecker diagonale (Entries 49–60, questa sessione):

### Congetture attive:

| ID  | Enunciato | Verif. | Wall |
|-----|-----------|--------|------|
| C42 | d_0(a)=3a-1, T(a)=3a+2 | a=2..7 | — |
| C44 | d_0(a,b=2)=3a+4 | a=2..7 | c=8 |
| C45 | g((a,1^{d-a})^3)=1 per d in [a,3a-2] | a=2..9 (68 valori) | — |
| C47 | s_2(k)=21k-44 per k>=3 | k=0..8 | — |
| C49 | g((c^2)^3)=0 c disp., =1 c pari | c=1..13 | c=14 |
| C50 | g((c^3)^3)=floor(c/3) disp., c/2 pari | c=1..9 | c=10 |
| C51 | g((3^k)^3)=0 iff k≡2 mod 5 | k=1..9 (2 zeri: k=2,7) | k=12 |
| C52 | FALSIFICATA (F68/Entry 68) — g((7^4)^3)=21≠9, serie dispari [0,1,4,21] | c=1,3,5→killed | c=7 |
| C53 | FALSIFICATA (F73: g((6^6)^3)=9309≠F(11)=89, d=36) | k=2..5: 1,1,5,21→killed | k=6 |
| C54 | s_3(5)=10826 (wall-limited, speculativa) | non verif. | d=28 |
| χ-circularity | DECISIONE-B1 (Entry 76): [col-orto + row-orto + hook-dim-anchor] NECESSARIO-NON-SUFFICIENTE; gruppo spurio |G|=2,4,8,192 (d=3..6) da permutazioni intra-blocco dim-degenere; circolarità ASTRATTA irriducibile con vincoli zero-parametro interni+dim; circolarità PRATICA chiusa operativamente (23 test + brute-force + indexing λ a priori); filone QA-engine3 fermato | d≤6 |

### Lemmi provati (con verifica meccanica):
- **L55** (parity): g((c^2)^3) non segue τ-parità per k≥3 (c=2,5,6,9 controesempi)
- **L60** (no-ord2): s_3(k) NON soddisfa ricorrenza lineare ord-2 intera [**CERTIFICATO IN LEAN 4**, Entry 69; assiomi: propext, Quot.sound; zero sorry; prova su ℚ 60a=391 non-intero]

### Sequenze chiave:
```
g((k^k)^3): 1,1,1,5,21  (k=1..5)  → F(3k-7) per k>=2 [C53]
g((c^2)^3): 0,1,0,1,...            → 0/1 per c disp/pari [C49]
g((c^3)^3): 0,1,1,2,2,3,...        → floor(c/3) / c/2 [C50]
g((c^4)^3): 0,1,1,5,4,16,...       → ((c-1)/2)^2 disp., formula aperta pari
g((3^k)^3): 1,0,1,1,1,1,0,1,1     (k=1..9) → zeri k=2,7 (k≡2 mod 5?) [C51] (E70: k=5 vale 1, non 2; Entry 70)
s_3(k):     2,14,158,1497,≈10826   → no formula; no ord-2 (L60, Lean-cert); crescita sub-exp [ERRATUM E69: s₃(1)=2 corretto]
```

### Falsificazioni di questa sessione:
- Entry 43: a=1 FALSIFICA C42 (d_0(1)≠3·1-1=2; valore effettivo d_0(1)=1 per conv.)
- Entry 58: C50 non si estende a k=4 (RESTATEMENT #31)
- Entry 59: predizioni A=1, B=4, C=8 per g((5^5)^3) TUTTE UCCISE (g=21=F(8))
- Entry 61 (H61): g(δ_k^3) ≠ F(3k-7) per k=3,4,5,6 (self-conjugate ≠ Fibonacci)
- Entry 64 (F64): 5 delle 11 partizioni in Entry 63 NON erano self-conjugate; 3 mancanti
- Entry 68 (F68): C52 FALSIFICATA — g((7^4)^3)=21≠9, serie dispari [0,1,4,21]
- Entry 73 (F73): C53 FALSIFICATA — g((6^6)^3)=9309≠F(11)=89, serie Fibonacci [1,1,5,21,9309] aperta

---

## Arc self-conjugate genericness (Entries 61–64, questa sessione):

### Nuove congetture:
| ID  | Enunciato | Verif. | Wall |
|-----|-----------|--------|------|
| C57 | lim R_staircase = 1 (g(δ_k^3)·d!/f³ → 1) | k=1..6 | k=7 (d=28) |
| C59 | RITIRATA / FALSIFICATA da F64 | — | — |
| C60 | R monotona in hook-spread (h_1-h_r)/d tra k-hook a stesso d | d=13,15,21 (k=3) | k≥4 |

### Nuovi lemmi:
- **L61** (H61): g(δ_k^3) ≠ F(3k-7) per k=3,4,5,6 (staircase non Fibonacci)
- **L62** (cond.): VOID (cascata logica post-C53 F73 — R_square condizionato su C53 falsificato)
- **L63**: R_hook(a)→∞ per a→∞ (Stirling + dati)

### Sequenze aggiuntive:
```
g(δ_k^3): 1,1,5,117,18269,24891165  (k=1..6)  [crescita iperesponenziale]

Spettro d=21 self-conjugate (hook-spread order):
hooks        spread    R
{21}         1.000     8101.18  (hook puro)
{17,3,1}     0.762        1.93  (quasi-hook)
{15,5,1}     0.667        1.04
{13,7,1}     0.571        0.997
{13,5,3}     0.476        0.998 \  tie spread
{11,9,1}     0.476        0.993 /
{11,7,3}     0.381        0.954  [δ_6 staircase]
{9,7,5}      0.190        0.838  (più bilanciato)
```

### Spettro corretto d=10,13,15:
```
(5,2,1,1,1)       d=10  hooks={9,1}     R=0.8475
(4,3,2,1)=δ_4     d=10  hooks={7,3}     R=0.9373
(7,1^6)           d=13  hooks={13}      R=7.8934
(5,3,3,1,1)       d=13  hooks={9,3,1}   R=1.0019
(4,4,3,2)         d=13  hooks={7,5,1}   R=0.8380   ← CORRETTO da F64
(8,1^7)           d=15  hooks={15}      R=32.3488
(6,3,3,1,1,1)     d=15  hooks={11,3,1}  R=0.9924   ← CORRETTO da F64
(5,4,3,2,1)=δ_5   d=15  hooks={9,5,1}  R=0.9511
(4,4,4,3)         d=15  hooks={7,5,3}   R=0.8488   ← CORRETTO da F64
```

---

## Bilancio lab (post-Entry 72)

```
33 restatements / 7 arene
7 lemmi (L55, L60 [Lean-cert, Entry 69], L62 VOID post-F73, L63, + 3 da sessioni prev)
7 falsificazioni (Entry 43, Entry 59×3, H61/Entry 61, F64/Entry 64, F68/Entry 68, F73/Entry 73)
3 errata-dati (F64: enumerazione Entry 63; E69: s₃(1) corretto 1→2; E70: C51 k=5 corretto 2→1)
1 non-collasso (M22)
survival-PASS@1 (M24), survival-PASS@3 (M25)
2 control-PASS (M26, M27)

DUAL-ENGINE (Entry 72):
  engine3 (Frobenius) valida corpus fino a d=28 sui valori chiave
  F68 e E70 confermate dual-engine (indipendenza implementativa)
  flag circolarità-residua CHIUSO per d≤21 (post-run d=24/28)
```

---

## Infrastruttura permanente da questa sessione

```
pnp_lab/gct_kronecker/
  fast.py              (g_fast, HOOK_MAX_D=27)
  coverage.py          (covered, sporadic_vanishing)
  hook_depth.py        (C42/C44/C45/C47 callabili)
  diagonal_census.py   (STRETCH_MAX_D=24)
tests/test_hook_depth.py  (68 test: 56 fast + 12 slow)
examples/run_hook_depth.py
```

---

## Azioni possibili successive

(a) **Struttura di C53**: perché F(3k-7)? Connessione Schur-Weyl / plethysm / GL(φ)?
(b) **Formula pari k=4**: trovare g((c^4)^3) per c pari (1,5,16 per c=2,4,6 — pattern aperto)
(c) **C60 a k>3**: spettro a d dove esistono 4-hook shapes (min. d=1+3+5+7=16 — ma d=16 = quadrato (4^4)!)
(d) **R=1 crossing**: per ogni k-hook fisso, trovare lo spread critico dove R attraversa 1
(e) **Nuova arena** (arithmetic circuits, algebrization, plethysm, altro)
(f) **Fermarsi** — ledger 31 restatements + 7 lemmi + 4 falsificazioni soddisfa anti-resa
