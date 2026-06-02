/-
  P/NP Research Lab — Modulo 4: formalizzazione in Lean 4.

  Radice della libreria: importa tutti i componenti.
    - Basic       : BitString, Language, IsPoly, Model (modello di calcolo astratto)
    - Classes     : P, NP, teorema P ⊆ NP, PEqNP / PNeqNP
    - Reductions  : riduzioni poly-time, NP-completezza, collasso di Cook
    - Barriers    : barriera di relativizzazione (forma astratta) e meta-teorema
    - Concrete    : un Model concreto (modello senza limiti) → P = NP per forza
                    bruta; prova che il framework è non vacuo e realizza il
                    "mondo P = NP" della barriera
    - SAT         : sintassi/semantica concrete di CNF-SAT (il bersaglio di
                    Cook–Levin) con forma-NP e una riduzione verificata
    - CookLevin   : il cuore verificato della riduzione di Cook–Levin
                    (vincolo locale → CNF: ogni funzione booleana è una CNF)
    - NaturalProofs : il nucleo logico della barriera di Razborov–Rudich
                    (Useful/Large/Constructive verificati; barriera come teorema)

  Tutto SOLO con Lean core (niente mathlib): compila con `lake build`.
-/
import PvsNP.Basic
import PvsNP.Classes
import PvsNP.Reductions
import PvsNP.Barriers
import PvsNP.Concrete
import PvsNP.SAT
import PvsNP.CookLevin
import PvsNP.NaturalProofs
