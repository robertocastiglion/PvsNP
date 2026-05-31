/-
  P/NP Research Lab — Modulo 4: formalizzazione in Lean 4.

  Radice della libreria: importa tutti i componenti.
    - Basic       : BitString, Language, IsPoly, Model (modello di calcolo astratto)
    - Classes     : P, NP, teorema P ⊆ NP, PEqNP / PNeqNP
    - Reductions  : riduzioni poly-time, NP-completezza, collasso di Cook
    - Barriers    : barriera di relativizzazione (forma astratta) e meta-teorema

  Tutto SOLO con Lean core (niente mathlib): compila con `lake build`.
-/
import PvsNP.Basic
import PvsNP.Classes
import PvsNP.Reductions
import PvsNP.Barriers
