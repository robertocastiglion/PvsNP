import PvsNP

-- Da quali assiomi dipendono i teoremi chiave? (controllo di onestà)
#print axioms PvsNP.P_subset_NP
#print axioms PvsNP.reduces_refl
#print axioms PvsNP.reduces_trans
#print axioms PvsNP.P_closed_reduction
#print axioms PvsNP.complete_in_P_implies_PEqNP
#print axioms PvsNP.complete_in_P_iff_PEqNP
#print axioms PvsNP.relativizing_cannot_settle

-- Modello concreto: il framework è non vacuo, e il "mondo P = NP" è abitato.
#print axioms PvsNP.unbounded_PEqNP
#print axioms PvsNP.collapse_world_exists

-- CNF-SAT concreto (il bersaglio di Cook–Levin) e la riduzione verificata.
#print axioms PvsNP.SAT.not_sat_of_nil_clause
#print axioms PvsNP.SAT.eval_append
#print axioms PvsNP.SAT.eval_rename
#print axioms PvsNP.SAT.sat_of_sat_rename

-- Cuore di Cook–Levin: vincolo locale → CNF (ogni funzione booleana è una CNF).
#print axioms PvsNP.SAT.forbid_eval_false
#print axioms PvsNP.SAT.canonical_correct
#print axioms PvsNP.SAT.canonical_sat

-- Nucleo di Razborov–Rudich (Natural Proofs): conteggio funzioni, utilità,
-- larghezza, e la barriera verificata.
#print axioms PvsNP.NaturalProofs.card_allFns
#print axioms PvsNP.NaturalProofs.hardnessProperty_useful
#print axioms PvsNP.NaturalProofs.hardnessProperty_large
#print axioms PvsNP.NaturalProofs.rr_barrier
#print axioms PvsNP.NaturalProofs.natural_property_breaks_crypto
