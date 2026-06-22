"""Demo: STRETCHING N=2 dei vanishing sporadici di Kronecker e il collision-finder (killer).

Esegue classify / summary / collisions per d=4,5,6 e stampa la tabella esatta + l'esito del
killer (c'e' o no una collisione: stessa chiave (shape_profile, covered), bit hole/ray opposto).

Run:  py examples/run_gct_saturation.py
"""

import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")  # Δ μ ∘ su cp1252 crasherebbe
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from pnp_lab.gct_kronecker import classify, collisions, summary  # noqa: E402


def _sig(profile):
    """Comprime la firma 4-bit (two-Row, two-Column, Hook, recK) in lettere."""
    names = "RCHK"
    return "/".join(
        "".join(n for n, b in zip(names, s) if b) or "." for s in profile
    )


def main() -> None:
    print("STRETCHING N=2 — split HOLE vs RAY-VANISH dei vanishing sporadici di Kronecker")
    print("HOLE = g(2·triple) > 0 (buco interno, ostruzione non-locale)")
    print("RAY  = g(2·triple) = 0 (ostruzione asintotica che persiste lungo il raggio)\n")

    for d in (4, 5, 6):
        n_sp, n_hole, n_ray, n_coll = summary(d)
        print("=" * 78)
        print(f"d={d}  #sporadic={n_sp}  #hole={n_hole}  #ray={n_ray}  #collisioni={n_coll}")
        for r in classify(d):
            tag = "HOLE" if r["hole"] else "RAY "
            print(
                f"  {tag}  cov={int(r['covered'])}  g(2·t)={r['g_stretch']:<3d}"
                f"  prof=[{_sig(r['shape_profile'])}]  {r['triple']}"
            )
        coll = collisions(d)
        if not coll:
            print("  KILLER: nessuna collisione -> bit hole/ray RICOSTRUIBILE dal dizionario "
                  "(shape_profile, covered) = RESTATEMENT")
        else:
            print(f"  KILLER: {len(coll)} COLLISIONE(I) -> bit hole/ray FUORI-dizionario "
                  "(sopravvivenza enumerabile a 2 livelli):")
            for c in coll:
                print(f"     chiave: prof=[{_sig(c['key'][0])}]  covered={c['key'][1]}")
                print(f"       HOLE: {c['holes']}")
                print(f"       RAY : {c['rays']}")
    print()


if __name__ == "__main__":
    main()
