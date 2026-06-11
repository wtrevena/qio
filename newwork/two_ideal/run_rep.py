"""Step 1: exact decomposition of the Fock space Lambda^*(V) under
SU(3)_c x SU(2)_L x U(1)_Y, for
  * the full 15-mode one-generation space (dim 32768),
  * the Q-only subspace (6 modes, dim 64)      -- numerical cross-check arena,
  * the Q+L subspace (8 modes, dim 256)        -- quantum-piece arena.

Every multiplicity is triple-verified:
  (1) the peeling terminates with the weight multiset exactly exhausted
      (exact integer arithmetic; asserts inside peel()),
  (2) sum_i m_i dim_i == 2^n,
  (3) independent character identity  sum_i m_i chi_i(g) == det(1 + U(g))
      at random torus elements (Schur/Weyl formulas, no Freudenthal),
  (4) sum_i m_i^2 and m_singlet reproduced by exact Weyl-integration
      quadrature of |chi_F|^2 and chi_F.

Also: anomaly bookkeeping, the Z6 congruence on the realized sector lattice,
self-conjugacy of the table, the particle-vs-conjugate convention lemma, and
the nu_R corollary.

Deterministic; writes decomposition_{full,Q,QL}.json and rep_checks.json.
"""
import json
import numpy as np

import su3
import model

su3.selftest()

OUT = {}

ARENAS = {
    'full': list(range(15)),
    'Q': model.SPECIES_SLOTS['Q'],
    'QL': model.SPECIES_SLOTS['Q'] + model.SPECIES_SLOTS['L'],
}

tables = {}
for name, slots in ARENAS.items():
    wd, _ = model.fock_weight_dict(slots)
    table = model.peel(wd)
    dim_sum = sum(r['m'] * r['dim'] for r in table)
    assert dim_sum == 1 << len(slots), (name, dim_sum)
    cerr = model.character_verification(table, slots, nrand=20)
    assert cerr < 1e-8, (name, cerr)
    dimc_peel = sum(r['m'] ** 2 for r in table)
    nsing_peel = sum(r['m'] for r in table
                     if (r['a'], r['b'], r['twoj'], r['y']) == (0, 0, 0, 0))
    dimc_q, nsing_q = model.weyl_quadrature_sums(slots)
    assert dimc_q == dimc_peel, (name, dimc_q, dimc_peel)
    assert nsing_q == nsing_peel, (name, nsing_q, nsing_peel)
    bad_z6 = model.z6_congruence(table)
    assert not bad_z6, (name, bad_z6[:5])
    bad_conj = model.conjugation_symmetry(table) if name in ('full',) else None
    if name == 'full':
        assert not bad_conj, bad_conj[:5]
    tables[name] = table
    OUT[name] = dict(
        n_modes=len(slots),
        fock_dim=1 << len(slots),
        n_sectors=len(table),                       # = dim of the CENTER
        dim_commutant=dimc_peel,                    # = sum m_i^2
        n_invariant_vectors=nsing_peel,             # singlet multiplicity
        max_multiplicity=max(r['m'] for r in table),
        n_multiplicity_ge2=sum(1 for r in table if r['m'] >= 2),
        char_check_max_err=cerr,
        z6_congruence_violations=0,
        table=table,
    )
    with open(f'decomposition_{name}.json', 'w') as f:
        json.dump(table, f, indent=1)
    print(f"[{name}] modes={len(slots)} sectors={len(table)} "
          f"dim_commutant={dimc_peel} singlets={nsing_peel} "
          f"max_m={OUT[name]['max_multiplicity']} char_err={cerr:.2e}")

# --- anomalies ---
anom = model.anomaly_checks()
print("anomalies:", anom)
for k, v in anom.items():
    if k.startswith(('su3', 'su2', 'grav', 'Y^3', 'sum_modes')):
        assert str(v) == '0', (k, v)
assert anom['Witten SU(2) (# doublets)'] % 2 == 0
OUT['anomalies'] = anom

# --- convention lemma: Lambda^*(V) == Lambda^*(V') as G-reps, where V' has the
# RH singlets conjugated to LH antiparticle modes (u^c,d^c,e^c). Verified as a
# character identity at random torus elements. ---
rng = np.random.default_rng(20260610)
worst = 0.0
for _ in range(50):
    p1, p2, ps, et = rng.uniform(0, 2 * np.pi, 4)
    cv = model.char_fock(ARENAS['full'], p1, p2, ps, et, conj_singlets=False)
    cc = model.char_fock(ARENAS['full'], p1, p2, ps, et, conj_singlets=True)
    worst = max(worst, abs(cv - cc))
OUT['convention_lemma_max_char_diff'] = worst
assert worst < 1e-9, worst
print(f"convention lemma (particle vs LH-conjugate modes): max char diff {worst:.2e}")

# --- nu_R corollary: adding a sterile (1,1)_0 mode doubles every multiplicity:
# Lambda^*(V + nu_R) = Lambda^*(V) (x) (C|0> + C|nu_R>) = 2 x same table. ---
OUT['nuR_corollary'] = ("Lambda^*(V (+) (1,1)_0) = Lambda^*(V) (x) C^2 with trivial "
                        "G-action on C^2: every multiplicity doubles, sectors unchanged; "
                        "dim commutant -> 4x, center identical.")

# --- the sector LATTICE: how 'three-factor' is it? ---
t = tables['full']
labels3 = sorted({(r['a'], r['b']) for r in t})
labels2 = sorted({r['twoj'] for r in t})
labels1 = sorted({r['y'] for r in t})
OUT['sector_lattice'] = dict(
    n_su3_labels=len(labels3), n_su2_labels=len(labels2), n_u1_labels=len(labels1),
    product_count=len(labels3) * len(labels2) * len(labels1),
    realized_count=len(t),
    su3_labels=labels3, su2_labels_2j=labels2, u1_labels_6Y=labels1,
)
print("sector lattice: realized", len(t), "of product",
      OUT['sector_lattice']['product_count'])

# --- one-generation 't Hooft check: NO (QQQL)-type singlet, i.e. the singlet
# at (n_Q,n_L,n_u,n_d,n_e) = (3,1,0,0,0) is absent; verified later on Fock
# space, but here via the QL table: any (0,0,0,y=0) irrep at fermion number 4
# cannot be resolved by the table alone (k not a G-label) -> done in run_full.
OUT['note'] = "species-resolved singlet spectroscopy is in results_full.json"

with open('rep_checks.json', 'w') as f:
    json.dump(OUT, f, indent=1)
print("rep_checks.json written")
