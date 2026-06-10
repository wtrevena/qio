"""Direction A: gauge-invariant (algebraic / BKOV) entanglement in the
Jordan-Wigner three-qubit toy.  All computations machine-verified; fixed
seeds; results written to results.json next to this script.

Run from anywhere:  python run_direction_A.py
"""
import json
import os
import sys
from fractions import Fraction
from itertools import permutations

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import alg_entanglement as ae

SEED = 20260609
HERE = os.path.dirname(os.path.abspath(__file__))
R_SM = 1.8174                       # SM log-inverse-coupling gap ratio at M_Z
rng = np.random.default_rng(SEED)
out = {'seed': SEED, 'conventions': {
    'entropy_base': 'bits (log2)',
    'jw_modes': 'f1 = sm x I x I, f2 = Z x sm x I, f3 = Z x Z x sm; '
                'sm = [[0,1],[0,0]]',
    'gauge_action': 'G(U) f_b^dag G(U)^dag = sum_a U[a,b] f_a^dag; weight '
                    'sectors carry 1, U, Lambda^2 U, det U',
    'S_alg': 'S_A = H({p_k}) + sum_k p_k S(rho_k)  (BKOV / Casini-Huerta)'}}

# ==========================================================================
# 0. Verify the Jordan-Wigner / gauge-action machinery
# ==========================================================================
F = ae.jw_modes()
car_res = 0.0
for i in range(3):
    for j in range(3):
        car_res = max(car_res, np.linalg.norm(
            F[i] @ F[j].conj().T + F[j].conj().T @ F[i] - np.eye(8) * (i == j)))
        car_res = max(car_res, np.linalg.norm(F[i] @ F[j] + F[j] @ F[i]))

hom_res = mode_res = uni_res = 0.0
for _ in range(20):
    U = ae.haar_unitary(3, rng)
    V = ae.haar_unitary(3, rng)
    GU, GV = ae.gauge_unitary(U), ae.gauge_unitary(V)
    uni_res = max(uni_res, np.linalg.norm(GU @ GU.conj().T - np.eye(8)))
    hom_res = max(hom_res, np.linalg.norm(GU @ GV - ae.gauge_unitary(U @ V)))
    for b in range(3):
        lhs = GU @ F[b].conj().T @ GU.conj().T
        rhs = sum(U[a, b] * F[a].conj().T for a in range(3))
        mode_res = max(mode_res, np.linalg.norm(lhs - rhs))
out['verification'] = dict(
    CAR_residual=car_res, G_unitarity_residual=uni_res,
    G_homomorphism_residual=hom_res, G_mode_transformation_residual=mode_res)
assert max(car_res, uni_res, hom_res, mode_res) < 1e-10
print(f"[0] JW + G(U) verified: CAR {car_res:.1e}, unitary {uni_res:.1e}, "
      f"homomorphism {hom_res:.1e}, mode action {mode_res:.1e}")

# ==========================================================================
# 1. Commutants of the three gauge choices (machine-computed)
# ==========================================================================
N_SAMP, N_FRESH = 50, 100


def build_commutant(name, sampler):
    gens = [ae.gauge_unitary(sampler()) for _ in range(N_SAMP)]
    basis = ae.commutant(gens)
    fresh = [ae.gauge_unitary(sampler()) for _ in range(N_FRESH)]
    fresh_res = ae.max_commutator_residual(basis, fresh)
    star_res = ae.verify_star_algebra(basis)
    struct = ae.algebra_structure(basis, seed=SEED)
    info = dict(
        n_samples=N_SAMP, dim=len(basis), center_dim=struct['center_dim'],
        structure=ae.structure_string(struct),
        blocks=[dict(n=b['n'], m=b['m'], dim=b['dim'], weights=b['weights'])
                for b in struct['blocks']],
        star_closure_residual=star_res,
        fresh_sample_commutation_residual=fresh_res)
    assert fresh_res < 1e-9 and star_res < 1e-8
    print(f"[1] {name}: dim {len(basis)}, center {struct['center_dim']}, "
          f"structure {info['structure']}")
    return struct, info


struct_u3, info_u3 = build_commutant("U(3) ", lambda: ae.haar_unitary(3, rng))
struct_su3, info_su3 = build_commutant("SU(3)", lambda: ae.haar_su(3, rng))
struct_u1, info_u1 = build_commutant(
    "U(1) ", lambda: np.exp(1j * rng.uniform(0, 2 * np.pi)) * np.eye(3))
out['commutants'] = {'U3': info_u3, 'SU3': info_su3, 'U1': info_u1}

# expected structures (verify-or-refute targets from the task)
assert info_u3['dim'] == 4 and all(b['n'] == 1 for b in info_u3['blocks'])
assert sorted(b['m'] for b in info_u3['blocks']) == [1, 1, 3, 3]
assert info_su3['dim'] == 6 and info_su3['center_dim'] == 3
assert sorted((b['n'], b['m']) for b in info_su3['blocks']) == [(1, 3), (1, 3), (2, 1)]
assert info_u1['dim'] == 20 and info_u1['center_dim'] == 4
assert sorted((b['n'], b['m']) for b in info_u1['blocks']) == \
    [(1, 1), (1, 1), (3, 1), (3, 1)]
# SU(3): the M2 block must live on span{|000>, |111>}
blk2 = [b for b in struct_su3['blocks'] if b['n'] == 2][0]
P2_expected = np.zeros((8, 8))
P2_expected[0, 0] = P2_expected[7, 7] = 1
assert np.linalg.norm(blk2['P'] - P2_expected) < 1e-9
out['commutants']['SU3']['M2_block_support'] = '|000>, |111>  (nu and e+)'
print("[1] expected structures confirmed: U(3)->C^4 abelian; "
      "SU(3)->M2(+)C(+)C; U(1)->M1(+)M3(+)M3(+)M1")

STRUCTS = {'U3': struct_u3, 'SU3': struct_su3, 'U1': struct_u1}

# ==========================================================================
# 2. Named states
# ==========================================================================
e = np.eye(8)
rotor = np.concatenate([[np.sqrt(7)], -1j * np.ones(7)]) / np.sqrt(14)
W = (e[1] + e[2] + e[4]) / np.sqrt(3)
GHZ = (e[0] + e[7]) / np.sqrt(2)
with open(os.path.join(HERE, '..', 'experiments', 'results',
                       'exp2_results.json')) as fh:
    exp2 = json.load(fh)
ex = exp2['weighted_W']['examples'][0]
wW = np.zeros(8, complex)
# exp2 convention: psi[1], psi[2], psi[4] = sqrt(a2), sqrt(b2), sqrt(c2)
wW[1], wW[2], wW[4] = np.sqrt(ex['a2']), np.sqrt(ex['b2']), np.sqrt(ex['c2'])
wW /= np.linalg.norm(wW)
STATES = {'rotor_vacuum': rotor, 'W': W, 'GHZ': GHZ,
          'weighted_W_matching': wW}

# exact sector probabilities (Fractions, machine-checked against numerics)
def exact_fractions(p, max_den=10000, tol=1e-10):
    fr = [Fraction(x).limit_denominator(max_den) for x in p]
    assert all(abs(float(f) - x) < tol for f, x in zip(fr, p)), \
        "sector probabilities are not simple rationals"
    return [str(f) for f in fr]


out['states'] = {}
for name, psi in STATES.items():
    p = ae.sector_probs(psi)
    rec = dict(amplitudes_note='', sector_probs=p.tolist(),
               single_qubit_entropies=ae.single_qubit_entropies(psi).tolist())
    try:
        rec['sector_probs_exact'] = exact_fractions(p)
    except AssertionError:
        rec['sector_probs_exact'] = None
    for gname, struct in STRUCTS.items():
        s = ae.algebraic_entropy(psi, struct)
        rec[f'S_alg_{gname}'] = dict(center=s['center'], quantum=s['quantum'],
                                     total=s['total'], block_probs=s['p'])
    out['states'][name] = rec
    print(f"[2] {name}: p={np.round(p, 6)}  "
          f"S_U3={rec['S_alg_U3']['total']:.6f}  "
          f"S_SU3={rec['S_alg_SU3']['total']:.6f}  "
          f"S_U1={rec['S_alg_U1']['total']:.6f}")

# rotor exact values
p_rot = ae.sector_probs(rotor)
assert out['states']['rotor_vacuum']['sector_probs_exact'] == \
    ['1/2', '3/14', '3/14', '1/14']
S_u3_exact = 0.5 + 0.5 * np.log2(14) - (3 / 7) * np.log2(3)
S_su3_exact = (4 / 7) * (np.log2(7) - 2) + (3 / 7) * (np.log2(14) - np.log2(3))
assert abs(out['states']['rotor_vacuum']['S_alg_U3']['total'] - S_u3_exact) < 1e-12
assert abs(out['states']['rotor_vacuum']['S_alg_SU3']['total'] - S_su3_exact) < 1e-12
out['states']['rotor_vacuum']['exact_values'] = dict(
    sector_probs='(1/2, 3/14, 3/14, 1/14)',
    S_U3='1/2 + (1/2)log2(14) - (3/7)log2(3) = %.12f bits' % S_u3_exact,
    S_SU3='(4/7)(log2 7 - 2) + (3/7)log2(14/3) = %.12f bits' % S_su3_exact,
    S_U1='= S_U3 (quantum piece vanishes for pure states)')
print(f"[2] rotor exact: p=(1/2,3/14,3/14,1/14), S_U3={S_u3_exact:.12f}, "
      f"S_SU3={S_su3_exact:.12f}")

# SU(3) singlet-block (M2) reduced state of rotor and GHZ: the gauge-invariant
# nu/e+ coherence retained when only SU(3) is gauged
def m2_block_state(psi):
    rho = np.outer(psi, psi.conj())
    sub = rho[np.ix_([0, 7], [0, 7])]
    p = np.trace(sub).real
    return (sub / p), p


for nm in ('rotor_vacuum', 'GHZ'):
    sub, p = m2_block_state(STATES[nm])
    out['states'][nm]['SU3_singlet_block'] = dict(
        prob=float(p), state_re=np.real(sub).tolist(),
        state_im=np.imag(sub).tolist(),
        purity=float(np.trace(sub @ sub).real))

# W is gauge-equivalent to a single Fock state |001>: exhibit the gauge
# transformation and verify the algebraic reductions agree
Ucol = np.array([[1 / np.sqrt(2), 1 / np.sqrt(6), 1 / np.sqrt(3)],
                 [-1 / np.sqrt(2), 1 / np.sqrt(6), 1 / np.sqrt(3)],
                 [0, -2 / np.sqrt(6), 1 / np.sqrt(3)]])
GW = ae.gauge_unitary(Ucol)
w_from_fock = GW @ e[1]
assert np.linalg.norm(w_from_fock - W) < 1e-12
EW = ae.cond_expectation(np.outer(W, W.conj()), struct_u3['basis'])
EF = ae.cond_expectation(np.outer(e[1], e[1].conj()), struct_u3['basis'])
out['W_is_pure_gauge'] = dict(
    note='W = G(U)|001> for an explicit U in SU(3) (column 3 = (1,1,1)/sqrt3)',
    construction_residual=float(np.linalg.norm(w_from_fock - W)),
    U3_reduction_residual=float(np.linalg.norm(EW - EF)),
    single_qubit_S_of_W=ae.single_qubit_entropies(W).tolist(),
    single_qubit_S_of_001=ae.single_qubit_entropies(e[1]).tolist())
print("[2] W = G(U)|001> verified: identical U(3)-invariant data, "
      "different (gauge-variant) single-qubit entropies")

# ==========================================================================
# 3. Gauge invariance of S_A  (the whole point)
# ==========================================================================
N_INV = 20
inv = {}
for name, psi in STATES.items():
    inv[name] = {}
    for gname, struct, sampler in (
            ('U3', struct_u3, lambda: ae.haar_unitary(3, rng)),
            ('SU3', struct_su3, lambda: ae.haar_su(3, rng)),
            ('U1', struct_u1,
             lambda: np.exp(1j * rng.uniform(0, 2 * np.pi)) * np.eye(3))):
        s0 = ae.algebraic_entropy(psi, struct)['total']
        dS_alg, dS_qubit = 0.0, 0.0
        for _ in range(N_INV):
            G = ae.gauge_unitary(sampler())
            phi = G @ psi
            dS_alg = max(dS_alg,
                         abs(ae.algebraic_entropy(phi, struct)['total'] - s0))
            dS_qubit = max(dS_qubit, float(np.max(np.abs(
                ae.single_qubit_entropies(phi)
                - ae.single_qubit_entropies(psi)))))
        inv[name][gname] = dict(max_dS_alg=dS_alg,
                                max_dS_single_qubit=dS_qubit)
        assert dS_alg < 1e-9
# bonus: S_A for the U(1) and SU(3) algebras is invariant even under the FULL
# U(3) action (G(U) normalizes the weight decomposition); verify on the rotor
extra = {}
for gname, struct in (('U1', struct_u1), ('SU3', struct_su3)):
    s0 = ae.algebraic_entropy(rotor, struct)['total']
    d = max(abs(ae.algebraic_entropy(
        ae.gauge_unitary(ae.haar_unitary(3, rng)) @ rotor, struct)['total'] - s0)
        for _ in range(N_INV))
    extra[gname] = d
    assert d < 1e-9
out['gauge_invariance'] = dict(
    n_random_gauge_elements=N_INV, per_state=inv,
    S_U1_and_S_SU3_invariant_under_full_U3=extra,
    note='S_alg invariant to ~1e-12 under its gauge group; single-qubit '
         'entropies shift by O(1) under the same transformations')
print("[3] gauge invariance verified: max |dS_alg| < 1e-9 across all states/"
      "groups; single-qubit entropies change by up to "
      f"{max(v['U3']['max_dS_single_qubit'] for v in inv.values()):.3f} bits")

# ==========================================================================
# 4. Haar ensemble (10^4 states)
# ==========================================================================
N_HAAR = 10 ** 4
z = rng.standard_normal((N_HAAR, 8)) + 1j * rng.standard_normal((N_HAAR, 8))
psis = z / np.linalg.norm(z, axis=1, keepdims=True)
a2 = np.abs(psis) ** 2
P = np.stack([a2[:, ae.WEIGHT == w].sum(axis=1) for w in range(4)], axis=1)


def H_rows(p):
    q = np.clip(p, 1e-30, 1.0)
    return -(np.where(p > 1e-15, q * np.log2(q), 0.0)).sum(axis=1)


S_u3 = H_rows(P)                                   # = S_U1 for pure states
S_su3 = H_rows(np.stack([P[:, 0] + P[:, 3], P[:, 1], P[:, 2]], axis=1))
# cross-check the fast formulas against the full machinery on 200 states
chk = 0.0
qmax = 0.0
for i in range(200):
    for gname, struct, fast in (('U3', struct_u3, S_u3[i]),
                                ('SU3', struct_su3, S_su3[i]),
                                ('U1', struct_u1, S_u3[i])):
        s = ae.algebraic_entropy(psis[i], struct)
        chk = max(chk, abs(s['total'] - fast))
        qmax = max(qmax, abs(s['quantum']))
assert chk < 1e-9
# analytic Dirichlet means: p ~ Dir(1,3,3,1) => E[H] via digamma
from scipy.special import digamma
def dir_mean_H(alpha):
    a0 = sum(alpha)
    return sum((a / a0) * (digamma(a0 + 1) - digamma(a + 1))
               for a in alpha) / np.log(2)
mean_u3_analytic = dir_mean_H([1, 3, 3, 1])
mean_su3_analytic = dir_mean_H([2, 3, 3])
out['haar_ensemble'] = dict(
    n=N_HAAR,
    S_U3=dict(mean=float(S_u3.mean()), std=float(S_u3.std()),
              min=float(S_u3.min()), max=float(S_u3.max()),
              analytic_mean_Dirichlet_1331=float(mean_u3_analytic)),
    S_SU3=dict(mean=float(S_su3.mean()), std=float(S_su3.std()),
               min=float(S_su3.min()), max=float(S_su3.max()),
               analytic_mean_Dirichlet_233=float(mean_su3_analytic)),
    S_U1='identical to S_U3 for every pure state (quantum piece = 0)',
    fast_vs_full_machinery_max_residual=float(chk),
    max_quantum_piece_over_sample=float(qmax),
    note='for PURE states all three algebras give purely classical (center) '
         'entropy; every block has n_k = 1 or m_k = 1')
assert abs(S_u3.mean() - mean_u3_analytic) < 0.01
assert abs(S_su3.mean() - mean_su3_analytic) < 0.01
print(f"[4] Haar(10^4): <S_U3>={S_u3.mean():.4f} (analytic "
      f"{mean_u3_analytic:.4f}), <S_SU3>={S_su3.mean():.4f} (analytic "
      f"{mean_su3_analytic:.4f}); max quantum piece {qmax:.1e}")

# ==========================================================================
# 5. Task 4: the well-posed coupling question
# ==========================================================================
# 5a. independent gauge-invariant parameters of a pure state (single copy,
#     accessible through the invariant observable algebra = E_A data):
out['parameter_count'] = dict(
    U3='3 real parameters: (p1, p2, p3); p0 = 1 - p1 - p2 - p3. The center '
       'is the charge (Hamming-weight) distribution; nothing else survives.',
    SU3='4 real parameters: (p1, p2) + the pure qubit in the M2 (nu/e+ '
        'singlet) block (2 Bloch parameters).',
    U1='11 real parameters: 3 sector probabilities + pure conditional states '
       'in the two M3 blocks (4 each, projectively).',
    note='E_A captures all single-copy gauge-invariant measurement data. '
         'Multi-copy (polynomial) invariants are richer; see '
         'beyond_EA_invariants.')

# 5b. the rotor vacuum's invariant data and its degeneracy
p = ae.sector_probs(rotor)
out['task4'] = {}
out['task4']['rotor_invariant_data'] = dict(
    p=['1/2', '3/14', '3/14', '1/14'],
    p1_minus_p2=float(p[1] - p[2]),
    independent_parameters=2,
    note='p1 = p2 EXACTLY (uniform |amplitude| over the 7 imaginary units '
         'forces p_k proportional to sector dimension on weights 1..3). The '
         'algebra-canonical vacuum has only TWO independent invariant '
         'parameters -- fewer than the three couplings.')
assert abs(p[1] - p[2]) < 1e-12

# 5c. exhaustive search for an affine/log match of r_SM from the rotor's
#     invariant data: all ordered triples of distinct sectors x feature maps
feats = {'p': p, 'log2_p': np.log2(p), 'minus_p_log2_p': -p * np.log2(p)}
zoo = []
for fname, f in feats.items():
    for (i, j, k) in permutations(range(4), 3):
        denom = f[j] - f[k]
        if abs(denom) < 1e-14:
            continue
        r = float((f[i] - f[j]) / denom)
        zoo.append(dict(feature=fname, sectors=[i, j, k], r=r,
                        dist_to_R_SM=abs(r - R_SM)))
zoo.sort(key=lambda d: d['dist_to_R_SM'])
out['task4']['r_matching_zoo'] = dict(
    R_SM=R_SM, n_assignments_tested=len(zoo),
    best=zoo[0], top5=zoo[:5],
    any_within_0p05=bool(zoo[0]['dist_to_R_SM'] < 0.05),
    any_within_0p01=bool(zoo[0]['dist_to_R_SM'] < 0.01),
    note='Every ordered assignment of three distinct charge sectors to the '
         'three couplings, under feature maps p, log2 p, -p log2 p. None '
         'reproduces r_SM = 1.8174 within the tolerance 0.05 used in the '
         'paper (Section 6.2), let alone 0.01 (Section 6.1).')
print(f"[5] r-zoo: best |r - r_SM| = {zoo[0]['dist_to_R_SM']:.4f} "
      f"(r = {zoo[0]['r']:.4f}, feature {zoo[0]['feature']}, sectors "
      f"{zoo[0]['sectors']}); none within 0.05")

# 5d. the weighted-W matching curve collapses: every weight-1 state has the
#     SAME invariant data p = (0,1,0,0) and S_alg = 0 for all three algebras
collapse = []
for exd in exp2['weighted_W']['examples']:
    v = np.zeros(8, complex)
    v[1], v[2], v[4] = np.sqrt(exd['a2']), np.sqrt(exd['b2']), np.sqrt(exd['c2'])
    v /= np.linalg.norm(v)
    collapse.append([ae.algebraic_entropy(v, s)['total']
                     for s in (struct_u3, struct_su3, struct_u1)])
collapse = np.array(collapse)
assert np.max(np.abs(collapse)) < 1e-9
out['task4']['weighted_W_collapse'] = dict(
    n_curve_points_tested=len(collapse),
    max_S_alg_over_curve_and_algebras=float(np.max(np.abs(collapse))),
    note='The entire exp2 coupling-matching weighted-W curve is pure gauge: '
         'every point has p = (0,1,0,0), S_alg = 0 for U(3), SU(3), U(1). '
         'Each is gauge-equivalent to a single Fock basis state (one d-bar '
         'quark in a rotated color frame).')

# 5e. multi-copy invariants beyond E_A (for honesty): the cross-sector
#     invariant w = <v3*, v1 ^ v2> and friends, nonzero for the rotor vacuum
def cross_invariants(psi):
    v0 = psi[0]
    v1 = np.array([psi[i] for i in ae.W1_IDX])     # mode components (f1,f2,f3)
    v2 = np.array([psi[i] for i in ae.W2_IDX])     # pair basis (12),(13),(23)
    v3 = psi[7]
    wedge = v1[0] * v2[2] - v1[1] * v2[1] + v1[2] * v2[0]   # v1 ^ v2 in det rep
    return dict(abs_w_v1_wedge_v2=float(abs(wedge)),
                abs_conj_v3_times_wedge=float(abs(np.conj(v3) * wedge)),
                abs_conj_v0_v3_conj_wedge=float(
                    abs(np.conj(v0) * v3 * np.conj(wedge))))
ci = cross_invariants(rotor)
# verify gauge invariance of |w| etc. under random G(U)
dmax = 0.0
for _ in range(20):
    ci2 = cross_invariants(ae.gauge_unitary(ae.haar_unitary(3, rng)) @ rotor)
    dmax = max(dmax, max(abs(ci[k] - ci2[k]) for k in ci))
assert dmax < 1e-10
out['task4']['beyond_EA_invariants'] = dict(
    rotor_values=ci, gauge_invariance_residual=float(dmax),
    exact_note='|v1 ^ v2| = 1/14 exactly for the rotor vacuum; '
               '|conj(v3) (v1^v2)| = 14^{-3/2}',
    note='The polynomial invariant ring is strictly richer than the E_A '
         '(single-copy) data: these degree-(2,2)/(3,3) invariants are not '
         'functions of (p0..p3). They are inaccessible to single-copy '
         'gauge-invariant measurements but exist as state invariants.')
assert abs(ci['abs_w_v1_wedge_v2'] - 1 / 14) < 1e-12

# 5f. SU(2)_L is not representable in this one-ideal toy
out['task4']['SU2L_obstruction'] = dict(
    statement='No unitary representation of SU(2)_L acts on this C^8 ideal '
              'as a gauge symmetry of the construction.',
    reasons=[
        'The mode-rotation (Bogoliubov, number-conserving) gauge group of '
        'three JW modes is exactly U(3) = (SU(3)_c x U(1))/Z3; there is no '
        'room for an independent SU(2) factor acting on color modes.',
        'The ideal (nu, dbar_i, u_i, e+) contains NO weak-isospin doublet '
        'pair: nu_L pairs with e-_L (absent; the ideal has e+), u_L with d_L '
        '(absent; the ideal has dbar). SU(2)_L raising/lowering operators '
        'would map this ideal into a DIFFERENT ideal of Cl(6) (in Furey\'s '
        'full construction SU(2)_L acts on the quaternionic factor of '
        'C (x) H (x) O, i.e. between ideals, not within one).',
        'Charge bookkeeping: SU(2)_L does not commute with electric charge '
        'Q = N/3, so any implementation would have to move states between '
        'Hamming-weight sectors by Delta(weight) = 3Q steps; the only '
        'weight-0/weight-3 pair is (nu, e+), which is not a doublet.'],
    consequence='At most TWO gauge factors (SU(3)_c and U(1)_em) act on the '
                'toy at all; a three-coupling question cannot even be posed '
                'gauge-covariantly on one generation ideal.')

# 5g. verdict
out['task4']['verdict'] = (
    'NO-GO, now sharp instead of ill-posed. (1) The U(3)-invariant data of '
    'any pure state is its charge-sector distribution (p0,p1,p2,p3): 3 real '
    'parameters indexed by ELECTRIC CHARGE, not by gauge factor; no natural '
    'bijection {4 charge sectors} -> {3 gauge factors} exists. (2) The '
    'algebra-canonical rotor vacuum has p = (1/2, 3/14, 3/14, 1/14) with '
    'p1 = p2 exactly: only 2 independent invariant parameters, fewer than 3 '
    'couplings -- the permutation degeneracy of the frame-dependent analysis '
    'survives gauge-invariantly as a sector degeneracy. (3) Exhaustive '
    'search over sector-to-coupling assignments and feature maps finds no '
    'match of r_SM (best miss 0.18). (4) The previous "positive" result -- '
    'the weighted-W coupling-matching curve -- collapses: it is pure gauge, '
    'S_alg = 0 identically. (5) SU(2)_L is not representable on the ideal. '
    'The well-posed question has a definite answer: the gauge-invariant '
    'entanglement of a single pure state in this toy CANNOT encode three '
    'independent couplings.')
print("[5] verdict recorded: sharp no-go")

# ==========================================================================
# save
# ==========================================================================
with open(os.path.join(HERE, 'results.json'), 'w') as fh:
    json.dump(out, fh, indent=2)
print("Saved", os.path.join(HERE, 'results.json'))
