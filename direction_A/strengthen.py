"""Strengthening computations for Paper 2 (Direction A follow-ups).

New file; does NOT modify run_direction_A.py / alg_entanglement.py / results.json.
Writes strengthen_results.json next to this script.  Findings are written up in
../paper2/VERIFICATIONS.md.

Tasks (numbering follows paper2/NOTES.md):
  T1 (NOTES item 6): machine-check the SU(2)_L obstruction lemma -- the group of
     unitaries on C^8 mapping span_C{f1,f2,f3} into itself under conjugation is
     exactly {e^{i phi} G(U) : U in U(3)}.  Lie-algebra dimension count, basis
     exponentiation, converse support (mode algebra = M_8), SU(3)-centralizer
     count, Bogoliubov / particle-hole / antilinear variants.
  T2 (NOTES item 7): alpha_Y-normalization rerun of the sector-assignment x
     feature-map search (r-zoo) against the non-GUT-normalized target.
  T4 (NOTES item 8): exp2 weighted-W example reconciliation -- verify stored S
     values from stored weights, locate both quoted points on the matching
     curve, confirm weight-1 support (hence pure gauge) for every stored point.

Run:  python strengthen.py   (numpy + scipy only; ~10 s)
"""
import json
import os
import sys
from itertools import permutations

import numpy as np
from scipy.linalg import expm
from scipy.optimize import brentq

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import alg_entanglement as ae

SEED = 20260609
HERE = os.path.dirname(os.path.abspath(__file__))
rng = np.random.default_rng(SEED)
out = {'seed': SEED}

F = ae.jw_modes()
Fd = [f.conj().T for f in F]
N_op = sum(fd @ f for fd, f in zip(Fd, F))
I8 = np.eye(8)

# CAR sanity (same checks as run_direction_A step 0, abbreviated)
car = 0.0
for i in range(3):
    for j in range(3):
        car = max(car, np.linalg.norm(F[i] @ Fd[j] + Fd[j] @ F[i] - I8 * (i == j)))
        car = max(car, np.linalg.norm(F[i] @ F[j] + F[j] @ F[i]))
assert car < 1e-14

# HS normalization of the modes: Tr(f_i^dag f_j) = 4 delta_ij
gram = np.array([[np.trace(a.conj().T @ b) for b in F] for a in F])
assert np.linalg.norm(gram - 4 * np.eye(3)) < 1e-13


# ==========================================================================
# T1.  Machine check of the SU(2)_L obstruction lemma
# ==========================================================================
print("=" * 70)
print("T1: SU(2)_L obstruction lemma (mode-preserving gauge group = U(3) x phase)")

def herm_basis(d=8):
    """HS-orthonormal real basis of the d x d Hermitian matrices (d^2 elems)."""
    B = []
    for i in range(d):
        E = np.zeros((d, d), complex); E[i, i] = 1.0; B.append(E)
    for i in range(d):
        for j in range(i + 1, d):
            E = np.zeros((d, d), complex)
            E[i, j] = E[j, i] = 1 / np.sqrt(2); B.append(E)
            E = np.zeros((d, d), complex)
            E[i, j] = -1j / np.sqrt(2); E[j, i] = 1j / np.sqrt(2); B.append(E)
    return B

HB = herm_basis()
assert len(HB) == 64


def hs_orthonormalize(mats):
    V = [m / np.sqrt(np.real(np.trace(m.conj().T @ m))) for m in mats]
    G = np.array([[np.trace(a.conj().T @ b) for b in V] for a in V])
    assert np.linalg.norm(G - np.eye(len(V))) < 1e-12, "span not HS-orthogonal"
    return V


def perp(X, V):
    """Component of X HS-orthogonal to span(V), V HS-orthonormal."""
    return X - sum(v * np.trace(v.conj().T @ X) for v in V)


def lie_algebra_nullspace(span_mats, extra_constraints=(), tol=1e-8):
    """Real solution space of  {h Hermitian : [h, f_k] in span_C(span_mats) for
    k = 1..3,  and  C(h) = 0 for C in extra_constraints}.

    Returns (list of Hermitian basis matrices, singular values of the
    constraint matrix, sorted ascending)."""
    V = hs_orthonormalize(span_mats)
    cols = []
    for Hb in HB:
        rows = [perp(Hb @ fk - fk @ Hb, V).flatten() for fk in F]
        rows += [C(Hb).flatten() for C in extra_constraints]
        cols.append(np.concatenate(rows))
    A = np.array(cols).T                      # complex (n_rows, 64)
    Areal = np.vstack([A.real, A.imag])       # real-linear in the 64 real coords
    u, s, vh = np.linalg.svd(Areal)
    null = vh[s.shape[0] - (s < tol).sum():] if (s < tol).sum() else vh[64:]
    # (rows of vh beyond rank; simpler: select rows with padded singular values)
    s_full = np.zeros(64); s_full[:len(s)] = s
    null = vh[s_full < tol]
    basis = [sum(x[b] * HB[b] for b in range(64)) for x in null]
    return basis, np.sort(s)


# --- (a) dimension of L = {h = h^dag : [h, f_k] in span{f1,f2,f3}} ----------
L_basis, sv = lie_algebra_nullspace(F)
dimL = len(L_basis)
sv_zero = float(sv[dimL - 1]) if dimL else 0.0
sv_gap = float(sv[dimL])      # smallest NONZERO singular value
print(f"  dim_R L = {dimL}   (expected 10 = dim u(3) + 1)")
print(f"  SVD split: largest 'zero' sv = {sv_zero:.2e}, smallest nonzero sv = {sv_gap:.3f}")
assert dimL == 10
assert sv_zero < 1e-10 and sv_gap > 0.1

# constraint + Hermiticity + number-conservation residuals of the basis
V3 = hs_orthonormalize(F)
res_constraint = max(np.linalg.norm(perp(h @ fk - fk @ h, V3))
                     for h in L_basis for fk in F)
res_herm = max(np.linalg.norm(h - h.conj().T) for h in L_basis)
res_numcons = max(np.linalg.norm(h @ N_op - N_op @ h) for h in L_basis)
print(f"  residuals: constraint {res_constraint:.1e}, hermiticity {res_herm:.1e}, "
      f"[h, N] {res_numcons:.1e}  (every solution conserves particle number)")
assert res_constraint < 1e-12 and res_herm < 1e-12 and res_numcons < 1e-12

# --- (b) L = dGamma(u(3)) + R.1  -------------------------------------------
def dGamma(a):
    """Second quantization of a 3x3 matrix a: sum_ij a_ij f_i^dag f_j."""
    return sum(a[i, j] * Fd[i] @ F[j] for i in range(3) for j in range(3))

herm3 = []
for i in range(3):
    E = np.zeros((3, 3), complex); E[i, i] = 1; herm3.append(E)
for i in range(3):
    for j in range(i + 1, 3):
        E = np.zeros((3, 3), complex); E[i, j] = E[j, i] = 1; herm3.append(E)
        E = np.zeros((3, 3), complex); E[i, j] = -1j; E[j, i] = 1j; herm3.append(E)
expected_gens = [dGamma(a) for a in herm3] + [np.eye(8, dtype=complex)]


def real_span_rank(mats, tol=1e-8):
    M = np.array([np.concatenate([m.real.flatten(), m.imag.flatten()])
                  for m in mats])
    return int(np.linalg.matrix_rank(M, tol=tol))

rank_expected = real_span_rank(expected_gens)
rank_union = real_span_rank(expected_gens + L_basis)
res_expected_in_L = max(np.linalg.norm(perp(g @ fk - fk @ g, V3))
                        for g in expected_gens for fk in F)
print(f"  span{{dGamma(u(3)), 1}}: rank {rank_expected}; union with computed L: "
      f"rank {rank_union}  -> L = dGamma(u(3)) (+) R.1: {rank_union == 10}")
assert rank_expected == 10 and rank_union == 10 and res_expected_in_L < 1e-12

# --- (c) every basis element exponentiates to e^{i phi} G(U), U in U(3) ----
def mode_matrix(W):
    """M with W f_k W^dag = sum_j M_kj f_j (HS extraction), and the residual."""
    M = np.zeros((3, 3), complex)
    img = [W @ fk @ W.conj().T for fk in F]
    for k in range(3):
        for j in range(3):
            M[k, j] = np.trace(Fd[j] @ img[k]) / 4.0
    res = max(np.linalg.norm(img[k] - sum(M[k, j] * F[j] for j in range(3)))
              for k in range(3))
    return M, float(res)

exp_checks = []
test_hs = list(L_basis) + [sum(rng.standard_normal() * h for h in L_basis)
                           for _ in range(20)]
for h in test_hs:
    W = expm(1j * h)
    M, res_mode = mode_matrix(W)
    res_unitary = float(np.linalg.norm(M @ M.conj().T - np.eye(3)))
    U = M.conj().T          # G(U) f_b G^dag = sum_a conj(U_ab) f_a  =>  U = M^dag
    GU = ae.gauge_unitary(U)
    lam = np.trace(GU.conj().T @ W) / 8.0
    res_phase = float(np.linalg.norm(W - lam * GU))
    res_lam = float(abs(abs(lam) - 1.0))
    exp_checks.append((res_mode, res_unitary, res_phase, res_lam))
exp_checks = np.array(exp_checks)
print(f"  exponentiation ({len(test_hs)} elements: 10 basis + 20 random combos):")
print(f"    max ||W f_k W^dag - sum_j M_kj f_j|| = {exp_checks[:,0].max():.1e}")
print(f"    max ||M M^dag - 1||                  = {exp_checks[:,1].max():.1e}")
print(f"    max ||W - e^(i phi) G(M^dag)||       = {exp_checks[:,2].max():.1e}")
assert exp_checks.max() < 1e-10

# --- (d) converse support: {f_k, f_k^dag} generate all of M_8(C) -----------
def generated_algebra_dim(gens, tol=1e-8):
    mats = [np.eye(8, dtype=complex)] + list(gens)
    M = np.array([m.flatten() for m in mats])
    rank = np.linalg.matrix_rank(M, tol=tol)
    while True:
        new = [a @ b for a in mats for b in gens]
        M2 = np.array([m.flatten() for m in mats + new])
        rank2 = np.linalg.matrix_rank(M2, tol=tol)
        if rank2 == rank:
            return int(rank)
        # compress to an independent set via QR of the row space
        q, r, piv = __import__('scipy.linalg', fromlist=['qr']).qr(
            M2.T, mode='economic', pivoting=True)
        keep = piv[:rank2]
        mats = [(mats + new)[k] for k in keep]
        M = np.array([m.flatten() for m in mats])
        rank = rank2

alg_dim = generated_algebra_dim(F + Fd)
print(f"  complex algebra generated by {{f_k, f_k^dag}}: dim {alg_dim} "
      f"(= 64 = M_8(C); Schur step of the converse is valid)")
assert alg_dim == 64

# --- (e) centralizer of the colour action inside L: only span{1, N} --------
su3_samples = [ae.gauge_unitary(ae.haar_su(3, rng)) for _ in range(20)]
cols = []
for h in L_basis:
    cols.append(np.concatenate([(h @ G - G @ h).flatten() for G in su3_samples]))
A = np.array(cols).T
Areal = np.vstack([A.real, A.imag])
u_, s_, vh_ = np.linalg.svd(Areal)
s_full = np.zeros(len(L_basis)); s_full[:len(s_)] = s_
null_c = vh_[s_full < 1e-8]
cent_basis = [sum(x[b] * L_basis[b] for b in range(len(L_basis))) for x in null_c]
dim_cent = len(cent_basis)
rank_IN = real_span_rank([np.eye(8, dtype=complex), N_op.astype(complex)])
rank_cent_union = real_span_rank(cent_basis + [np.eye(8, dtype=complex),
                                               N_op.astype(complex)])
# fresh-sample certification
fresh_su3 = [ae.gauge_unitary(ae.haar_su(3, rng)) for _ in range(20)]
cent_res = max(np.linalg.norm(h @ G - G @ h)
               for h in cent_basis for G in fresh_su3)
print(f"  centralizer of SU(3)_c inside L: dim {dim_cent} "
      f"(expected 2 = span{{1, N}}); union rank with {{1,N}}: {rank_cent_union}; "
      f"fresh-sample residual {cent_res:.1e}")
assert dim_cent == 2 and rank_cent_union == 2 and cent_res < 1e-9
# an su(2) needs a 3-dim NON-abelian algebra; the centralizer is 2-dim abelian
comm_cent = np.linalg.norm(cent_basis[0] @ cent_basis[1]
                           - cent_basis[1] @ cent_basis[0])
assert comm_cent < 1e-12

# --- (f) Bogoliubov variant: allow [h, f_k] in span{f_j, f_j^dag} ----------
LB_basis, svB = lie_algebra_nullspace(F + Fd)
dimLB = len(LB_basis)
svB_zero = float(svB[dimLB - 1]); svB_gap = float(svB[dimLB])
print(f"  Bogoliubov variant: dim_R L_B = {dimLB} "
      f"(expected 16 = dim so(6) + 1; pair terms f_i^dag f_j^dag + h.c. added)")
assert dimLB == 16
assert svB_zero < 1e-10 and svB_gap > 0.1

# pair-term identification: L_B = L (+) span{pair quadratics}
pair_gens = []
for i in range(3):
    for j in range(i + 1, 3):
        P = Fd[i] @ Fd[j]
        pair_gens.append(P + P.conj().T)
        pair_gens.append(1j * (P - P.conj().T))
rank_LB_expected = real_span_rank(expected_gens + pair_gens)
rank_LB_union = real_span_rank(expected_gens + pair_gens + LB_basis)
print(f"  L_B = dGamma(u(3)) (+) R.1 (+) pair terms: rank {rank_LB_expected}, "
      f"union with computed L_B: {rank_LB_union}  -> identified: "
      f"{rank_LB_expected == 16 and rank_LB_union == 16}")
assert rank_LB_expected == 16 and rank_LB_union == 16

# the number-conserving part of L_B is exactly L (dim 10): the weight grading
# kills every number-violating direction
LN_basis, _ = lie_algebra_nullspace(F + Fd, extra_constraints=[
    lambda h: h @ N_op - N_op @ h])
rank_LN_union = real_span_rank(LN_basis + L_basis)
print(f"  {{h in L_B : [h, N] = 0}}: dim {len(LN_basis)}, union with L: rank "
      f"{rank_LN_union}  -> equals L: {len(LN_basis) == 10 and rank_LN_union == 10}")
assert len(LN_basis) == 10 and rank_LN_union == 10

# every number-violating element of L_B breaks the weight grading and does NOT
# preserve span{f}: exhibit it on a pair generator and on a random element of
# the complement
Pw = [np.diag((ae.WEIGHT == w).astype(float)) for w in range(4)]
def grading_breaks(h):
    """(||[h,N]||, max off-diagonal weight-block norm of expm(ih),
        ||component of [h,f_1] orthogonal to span{f}||)."""
    G = expm(1j * h)
    off = max(np.linalg.norm(Pw[a] @ G @ Pw[b])
              for a in range(4) for b in range(4) if a != b)
    return (float(np.linalg.norm(h @ N_op - N_op @ h)), float(off),
            float(np.linalg.norm(perp(h @ F[0] - F[0] @ h, V3))))

gb_pair = grading_breaks(pair_gens[0])
# random element of L_B orthogonal to L (in HS sense)
hr = sum(rng.standard_normal() * h for h in LB_basis)
for h in L_basis:   # project out L
    hr = hr - h * np.real(np.trace(h.conj().T @ hr)) / np.real(
        np.trace(h.conj().T @ h))
gb_rand = grading_breaks(hr)
print(f"  pair generator f1+f2+ + h.c.: ||[h,N]|| = {gb_pair[0]:.3f}, "
      f"max off-weight block of e^ih = {gb_pair[1]:.3f}, "
      f"perp-to-span{{f}} part of [h,f1] = {gb_pair[2]:.3f}")
print(f"  random L_B element with L projected out: ||[h,N]|| = {gb_rand[0]:.3f}, "
      f"off-weight {gb_rand[1]:.3f}, perp {gb_rand[2]:.3f}")
assert min(gb_pair) > 0.1 and min(gb_rand) > 1e-3

# --- (g) particle-hole component: exists, but swaps span{f} <-> span{f^dag}
X = np.array([[0, 1], [1, 0]], complex)
Wph = np.kron(np.kron(X, X), X)
C_expected = np.diag([1.0, -1.0, 1.0])
res_ph = max(np.linalg.norm(Wph @ F[k] @ Wph.conj().T
                            - C_expected[k, k] * Fd[k]) for k in range(3))
res_ph_N = float(np.linalg.norm(Wph @ N_op @ Wph.conj().T - (3 * I8 - N_op)))
# Wph maps span{f} to span{f^dag}, which intersects span{f} trivially:
res_ph_span = float(np.linalg.norm(perp(Wph @ F[0] @ Wph.conj().T, V3))
                    / np.linalg.norm(Wph @ F[0] @ Wph.conj().T))
print(f"  particle-hole W = XXX: W f_k W^dag = (f1^dag, -f2^dag, f3^dag), "
      f"residual {res_ph:.1e}; W N W^dag = 3 - N, residual {res_ph_N:.1e}; "
      f"image of f_1 is 100% orthogonal to span{{f}}: {res_ph_span:.3f}")
assert res_ph < 1e-14 and res_ph_N < 1e-14 and abs(res_ph_span - 1.0) < 1e-12

# --- (h) antilinear maps add nothing: all f_k are real, K G(U) K = G(conj U)
res_real = max(np.linalg.norm(f - f.conj()) for f in F)
res_conjG = 0.0
for _ in range(5):
    U = ae.haar_unitary(3, rng)
    res_conjG = max(res_conjG, np.linalg.norm(
        ae.gauge_unitary(U).conj() - ae.gauge_unitary(U.conj())))
print(f"  antilinear: f_k real (residual {res_real:.1e}); "
      f"conj(G(U)) = G(conj U) (residual {res_conjG:.1e}) -> antiunitaries "
      f"preserving span{{f}} are exactly K . e^(i phi) G(U)")
assert res_real == 0.0 and res_conjG < 1e-12

out['task1_su2L_lemma'] = dict(
    claim='The unitaries W on C^8 with W span{f1,f2,f3} W^dag <= span{f1,f2,f3} '
          'are exactly {e^{i phi} G(U) : U in U(3)}; hence no SU(2)_L can act '
          'as a mode gauge symmetry on this one-generation ideal.',
    dim_L=dimL, expected_dim='10 = dim u(3) + 1 (global phase)',
    svd_split=dict(largest_zero_sv=sv_zero, smallest_nonzero_sv=sv_gap),
    residuals=dict(constraint=res_constraint, hermiticity=res_herm,
                   number_conservation=res_numcons),
    L_equals_dGamma_u3_plus_identity=dict(
        rank_expected=rank_expected, rank_union=rank_union,
        expected_gens_constraint_residual=float(res_expected_in_L)),
    exponentiation=dict(
        n_elements_checked=len(test_hs),
        max_mode_reconstruction_residual=float(exp_checks[:, 0].max()),
        max_M_unitarity_residual=float(exp_checks[:, 1].max()),
        max_phase_times_GU_residual=float(exp_checks[:, 2].max()),
        note='W = expm(i h) for all 10 basis elements and 20 random real '
             'combinations; each satisfies W f_k W^dag = sum_j M_kj f_j with '
             'M unitary, and W = e^{i phi} G(M^dag) exactly.'),
    converse=dict(
        mode_algebra_dim=alg_dim,
        note='Group-level converse: if W span{f} W^dag <= span{f}, CAR forces '
             'the coefficient matrix M to be unitary (M M^dag = 1 from '
             '{W f_i W^dag, (W f_j W^dag)^dag} = delta_ij); then W G(M^dag)^dag '
             'commutes with every f_k, f_k^dag, whose generated algebra is all '
             'of M_8(C) (machine: dim 64), so Schur gives W = e^{i phi} G(M^dag). '
             'No extra components exist.'),
    su3_centralizer_in_L=dict(
        dim=dim_cent, equals_span_1_N=bool(rank_cent_union == 2),
        fresh_sample_residual=float(cent_res),
        commutator_of_basis=float(comm_cent),
        note='An SU(2)_L gauge factor must commute with the colour action and '
             'preserve the modes. The space of such generators is the '
             '2-dimensional ABELIAN algebra span{1, N}; su(2) needs a '
             '3-dimensional non-abelian algebra. Obstruction is machine-exact.'),
    bogoliubov_variant=dict(
        dim_LB=dimLB, expected='16 = dim so(6) + 1',
        svd_split=dict(largest_zero_sv=svB_zero, smallest_nonzero_sv=svB_gap),
        identified_as='dGamma(u(3)) (+) R.1 (+) 6 pair terms '
                      'f_i^dag f_j^dag + h.c., i(f_i^dag f_j^dag - h.c.)',
        rank_checks=dict(expected=rank_LB_expected, union=rank_LB_union),
        number_conserving_part=dict(dim=len(LN_basis),
                                    equals_L=bool(rank_LN_union == 10)),
        grading_violation=dict(
            pair_generator=dict(norm_comm_N=gb_pair[0],
                                max_off_weight_block_of_exp=gb_pair[1],
                                perp_to_modespan_of_comm_f1=gb_pair[2]),
            random_complement_element=dict(norm_comm_N=gb_rand[0],
                                           max_off_weight_block_of_exp=gb_rand[1],
                                           perp_to_modespan_of_comm_f1=gb_rand[2])),
        note='Allowing f_i -> sum_j (U_ij f_j + V_ij f_j^dag) enlarges the '
             'LINEAR-constraint solution space from 10 to 16 (the Bogoliubov '
             'algebra so(6) (+) phase), but every added direction violates '
             'particle number, moves states across Hamming-weight (= charge) '
             'sectors, and fails to map span{f} into itself. The '
             'number-conserving / span-preserving part collapses back to '
             'u(3) (+) phase exactly.'),
    particle_hole=dict(
        W='X(x)X(x)X', action='f_k -> (f1^dag, -f2^dag, f3^dag)',
        residual=float(res_ph), N_inversion_residual=res_ph_N,
        image_orthogonal_to_modespan=res_ph_span,
        note='A particle-hole unitary exists but SWAPS span{f} with '
             'span{f^dag} and inverts the charge grading (N -> 3 - N); it is '
             'not in the span-preserving group, and SU(2), being connected, '
             'cannot live in a disconnected coset.'),
    antilinear=dict(f_real_residual=float(res_real),
                    conjG_residual=float(res_conjG),
                    note='All f_k are real matrices, so every antiunitary '
                         'preserving span{f} is K (entrywise conjugation) '
                         'composed with a span-preserving unitary; K G(U) K = '
                         'G(conj U). Antilinear maps add no new symmetry.'))

# ==========================================================================
# T2.  alpha_Y normalization rerun of the r-zoo
# ==========================================================================
print("=" * 70)
print("T2: alpha_Y-normalization rerun")

alpha3, alpha2, alpha1 = 0.1179, 0.03374, 0.01695     # PDG values used in [1]
a3i, a2i, a1i = 1 / alpha3, 1 / alpha2, 1 / alpha1
r_SM = (np.log(a3i) - np.log(a2i)) / (np.log(a2i) - np.log(a1i))
assert abs(r_SM - 1.8174) < 5e-5, r_SM                # reproduces paper target
assert abs(a1i - 59.00) < 0.005                       # alpha_1^-1 = 59.00 OK

aYi = (5.0 / 3.0) * a1i                               # alpha_Y = (3/5) alpha_1
r_Y = (np.log(a3i) - np.log(a2i)) / (np.log(a2i) - np.log(aYi))
# rounded-table variant (draft.md Sec 6.3 table: 8.48, 29.64, 59.00)
aYi_r = (5.0 / 3.0) * 59.00
r_Y_rounded = (np.log(8.48) - np.log(29.64)) / (np.log(29.64) - np.log(aYi_r))
print(f"  alpha_1^-1 = {a1i:.4f} (GUT)  ->  alpha_Y^-1 = (5/3) alpha_1^-1 = "
      f"{aYi:.4f}  [rounded-table variant: {aYi_r:.4f}]")
print(f"  r_SM (GUT)   = {r_SM:.6f}")
print(f"  r_Y  (alpha_Y) = {r_Y:.6f}   [rounded-table variant {r_Y_rounded:.6f}]")

rotor = np.concatenate([[np.sqrt(7)], -1j * np.ones(7)]) / np.sqrt(14)
p = ae.sector_probs(rotor)
assert np.linalg.norm(p - np.array([1 / 2, 3 / 14, 3 / 14, 1 / 14])) < 1e-14


def r_zoo(p, target):
    feats = {'p': p, 'log2_p': np.log2(p), 'minus_p_log2_p': -p * np.log2(p)}
    zoo = []
    n_enumerated = 0
    for fname, f in feats.items():
        for (i, j, k) in permutations(range(4), 3):
            n_enumerated += 1
            denom = f[j] - f[k]
            if abs(denom) < 1e-14:
                continue
            r = float((f[i] - f[j]) / denom)
            zoo.append(dict(feature=fname, sectors=[i, j, k], r=r,
                            dist=abs(r - target)))
    zoo.sort(key=lambda d: d['dist'])
    return zoo, n_enumerated

zoo_Y, n_enum = r_zoo(p, r_Y)
zoo_SM, _ = r_zoo(p, r_SM)            # cross-check against results.json
assert n_enum == 72 and len(zoo_Y) == 60
assert abs(zoo_SM[0]['dist'] - 0.1826) < 1e-3         # matches results.json
print(f"  zoo: 72 enumerated, {len(zoo_Y)} finite (p1 = p2 kills 12)")
print(f"  cross-check GUT target: best miss {zoo_SM[0]['dist']:.4f} "
      f"(results.json: 0.1826)  OK")
print(f"  alpha_Y target {r_Y:.4f}: best miss {zoo_Y[0]['dist']:.4f} at "
      f"r = {zoo_Y[0]['r']:.4f} (feature {zoo_Y[0]['feature']}, sectors "
      f"{zoo_Y[0]['sectors']}); within 0.05: {zoo_Y[0]['dist'] < 0.05}")
for z in zoo_Y[:5]:
    print(f"    r = {z['r']:+.6f}  dist = {z['dist']:.4f}  "
          f"[{z['feature']}, sectors {z['sectors']}]")
# distance of the rounded-table variant (same zoo, shifted target)
best_rounded = min(abs(z['r'] - r_Y_rounded) for z in zoo_Y)

out['task2_alphaY_rerun'] = dict(
    alpha_inputs=dict(alpha3=alpha3, alpha2=alpha2, alpha1_GUT=alpha1,
                      alpha1_inv=float(a1i), alphaY_inv=float(aYi),
                      alphaY_inv_from_rounded_59=float(aYi_r)),
    r_SM_GUT=float(r_SM),
    r_Y=float(r_Y), r_Y_rounded_table=float(r_Y_rounded),
    n_enumerated=n_enum, n_finite=len(zoo_Y),
    cross_check_GUT_best_dist=float(zoo_SM[0]['dist']),
    best=dict(feature=zoo_Y[0]['feature'], sectors=zoo_Y[0]['sectors'],
              r=zoo_Y[0]['r'], dist_to_r_Y=zoo_Y[0]['dist']),
    top5=[dict(feature=z['feature'], sectors=z['sectors'], r=z['r'],
               dist_to_r_Y=z['dist']) for z in zoo_Y[:5]],
    best_dist_rounded_variant=float(best_rounded),
    any_within_0p05=bool(zoo_Y[0]['dist'] < 0.05),
    any_within_0p01=bool(zoo_Y[0]['dist'] < 0.01),
    note='Same 60-assignment zoo (3 feature maps x 24 ordered sector triples, '
         '12 indeterminate by p1 = p2) re-targeted at the non-GUT-normalized '
         'gap ratio r_Y. No assignment lands within 0.05 (or 0.01). The '
         'p1 = p2 degeneracy and the four-sectors-vs-three-couplings mismatch '
         'are normalization-independent.')

# ==========================================================================
# T4.  exp2 weighted-W example reconciliation
# ==========================================================================
print("=" * 70)
print("T4: exp2 weighted-W example reconciliation")

with open(os.path.join(HERE, '..', 'experiments', 'results',
                       'exp2_results.json')) as fh:
    exp2 = json.load(fh)
R_SM_exp2 = r_SM      # exp2 used qio_lib.R_SM computed from the same alphas


def h2(x):
    if x <= 0 or x >= 1:
        return 0.0
    return float(-x * np.log2(x) - (1 - x) * np.log2(1 - x))


def h2inv(S):
    """Smaller-eigenvalue branch: x in [0, 1/2] with h2(x) = S."""
    if S <= 0:
        return 0.0
    return brentq(lambda x: h2(x) - S, 1e-15, 0.5)


# rebuild the three invariant-algebra structures (same machinery as
# run_direction_A; fresh samples, same seed stream continues)
def build_struct(sampler, n=50):
    basis = ae.commutant([ae.gauge_unitary(sampler()) for _ in range(n)])
    return ae.algebra_structure(basis, seed=SEED)

struct_u3 = build_struct(lambda: ae.haar_unitary(3, rng))
struct_su3 = build_struct(lambda: ae.haar_su(3, rng))
struct_u1 = build_struct(lambda: np.exp(1j * rng.uniform(0, 2 * np.pi))
                         * np.eye(3))
assert (len(struct_u3['basis']), len(struct_su3['basis']),
        len(struct_u1['basis'])) == (4, 6, 20)

GRID_STEP = 0.65 / 199          # exp2 scanned S3 over linspace(0.30, 0.95, 200)

def analyze_point(a2, b2, c2):
    psi = np.zeros(8, complex)
    psi[1], psi[2], psi[4] = np.sqrt(a2), np.sqrt(b2), np.sqrt(c2)
    norm_def = float(abs(a2 + b2 + c2 - 1.0))
    psi = psi / np.linalg.norm(psi)
    S = ae.single_qubit_entropies(psi)              # (S1, S2, S3)
    r = float((S[0] - S[1]) / (S[1] - S[2]))
    p = ae.sector_probs(psi)
    w1_support = float(p[1])
    s_alg = [ae.algebraic_entropy(psi, st)['total']
             for st in (struct_u3, struct_su3, struct_u1)]
    return dict(S=[float(s) for s in S], r_S=r, norm_deficit=norm_def,
                sector_probs=[float(x) for x in p],
                weight1_support=w1_support,
                S_alg=dict(U3=s_alg[0], SU3=s_alg[1], U1=s_alg[2]))

# --- the 5 stored curve points ("examples") --------------------------------
ex_records = []
maxs = dict(dS=0.0, dr=0.0, dp=0.0, dSalg=0.0, dnorm=0.0)
for ex in exp2['weighted_W']['examples']:
    rec = analyze_point(ex['a2'], ex['b2'], ex['c2'])
    dS = max(abs(rec['S'][0] - ex['S1']), abs(rec['S'][1] - ex['S2']),
             abs(rec['S'][2] - ex['S3']))
    maxs['dS'] = max(maxs['dS'], dS)
    maxs['dr'] = max(maxs['dr'], abs(rec['r_S'] - R_SM_exp2))
    maxs['dp'] = max(maxs['dp'], abs(rec['weight1_support'] - 1.0))
    maxs['dSalg'] = max(maxs['dSalg'], max(abs(v) for v in rec['S_alg'].values()))
    maxs['dnorm'] = max(maxs['dnorm'], rec['norm_deficit'])
    rec['stored'] = ex
    ex_records.append(rec)
print(f"  5 stored examples: max |S(recomputed) - S(stored)| = {maxs['dS']:.2e}")
print(f"    max |r_S - r_SM| = {maxs['dr']:.2e}; max |p1 - 1| = {maxs['dp']:.2e}")
print(f"    max |S_alg| over all 3 algebras = {maxs['dSalg']:.2e}; "
      f"max weight-normalization deficit = {maxs['dnorm']:.2e}")
assert maxs['dS'] < 1e-9 and maxs['dr'] < 1e-6 and maxs['dp'] < 1e-12
assert maxs['dSalg'] < 1e-12

# --- the draft.md Fig 1c point ("weighted_W_example") ----------------------
wex = exp2['weighted_W_example']
S1q, S2q, S3q = wex['S']                    # (0.9783, 0.8947, 0.8487)
c2q, b2q, a2q = h2inv(S1q), h2inv(S2q), h2inv(S3q)
rec_fig1c = analyze_point(a2q, b2q, c2q)
dS_fig1c = max(abs(np.array(rec_fig1c['S']) - np.array(wex['S'])))
dr_fig1c = abs(rec_fig1c['r_S'] - wex['r_S'])
print(f"  Fig-1c point reconstructed from S via h2inv: weights "
      f"(a2,b2,c2) = ({a2q:.6f}, {b2q:.6f}, {c2q:.6f})")
print(f"    weight-sum deficit |a2+b2+c2-1| = {rec_fig1c['norm_deficit']:.2e} "
      f"(lies on the curve), S round-trip residual {dS_fig1c:.2e}, "
      f"|r_S - stored| = {dr_fig1c:.2e}")
print(f"    weight-1 support = {rec_fig1c['weight1_support']:.15f}; "
      f"S_alg = ({rec_fig1c['S_alg']['U3']:.2e}, "
      f"{rec_fig1c['S_alg']['SU3']:.2e}, {rec_fig1c['S_alg']['U1']:.2e})")
assert rec_fig1c['norm_deficit'] < 1e-8
assert abs(rec_fig1c['weight1_support'] - 1.0) < 1e-12
assert max(abs(v) for v in rec_fig1c['S_alg'].values()) < 1e-12

# --- same point or different? grid-index arithmetic ------------------------
S3_examples = [ex['S3'] for ex in exp2['weighted_W']['examples']]
steps_between_examples = np.diff(S3_examples) / GRID_STEP
steps_fig1c = (S3q - S3_examples[0]) / GRID_STEP
min_dist_to_examples = min(abs(S3q - s) for s in S3_examples)
print(f"  exp2 S3 grid step = 0.65/199 = {GRID_STEP:.10f}")
print(f"  stored examples sit at grid steps {np.round(steps_between_examples, 9)}"
      f" apart (= 8 each); Fig-1c point sits {steps_fig1c:.9f} grid steps from "
      f"examples[0]")
print(f"  -> Fig-1c point is curve index 21 (the midpoint of the 43-point "
      f"curve, examples are indices 0,8,16,24,32); min |S3 - examples.S3| = "
      f"{min_dist_to_examples:.4f}  (DIFFERENT point, same curve)")
assert np.allclose(steps_between_examples, 8.0, atol=1e-6)
assert abs(steps_fig1c - 21.0) < 1e-6

out['task4_exp2_reconciliation'] = dict(
    claim='The S-triple (0.9995, 0.8580, 0.7802) quoted in Paper 2 and the '
          'S-triple (0.978, 0.895, 0.849) quoted in draft.md Fig. 1c / Sec 6.2 '
          'are DIFFERENT points on the SAME exp2 weighted-W matching curve; '
          'no inconsistency. Every stored point has support only on the '
          'weight-1 sector, hence S_alg = 0 (pure gauge).',
    grid=dict(S3_scan='linspace(0.30, 0.95, 200)', step=float(GRID_STEP),
              n_curve_points=int(exp2['weighted_W']['n_solutions_on_grid']),
              examples_are_curve_indices=[0, 8, 16, 24, 32],
              fig1c_point_is_curve_index=21,
              fig1c_steps_from_example0=float(steps_fig1c)),
    examples_verification=dict(
        n=len(ex_records),
        max_S_recompute_residual=maxs['dS'],
        max_r_S_minus_r_SM=maxs['dr'],
        max_weight1_support_deficit=maxs['dp'],
        max_S_alg_all_algebras=maxs['dSalg'],
        max_weight_sum_deficit=maxs['dnorm'],
        per_example=[dict(stored_S=[e['stored']['S1'], e['stored']['S2'],
                                    e['stored']['S3']],
                          recomputed_S=e['S'], r_S=e['r_S'],
                          weight1_support=e['weight1_support'],
                          S_alg=e['S_alg']) for e in ex_records]),
    fig1c_point=dict(
        stored_S=wex['S'], stored_r_S=wex['r_S'],
        reconstructed_weights=dict(a2=float(a2q), b2=float(b2q), c2=float(c2q)),
        weight_sum_deficit=rec_fig1c['norm_deficit'],
        S_roundtrip_residual=float(dS_fig1c),
        r_S_residual=float(dr_fig1c),
        weight1_support=rec_fig1c['weight1_support'],
        S_alg=rec_fig1c['S_alg']),
    verdict='Different points on the same matching curve. Paper 2 quotes exp2 '
            'examples[0] (curve grid index 0, S3 = 0.7802); draft.md Fig. 1c '
            'quotes the separately stored "weighted_W_example" (curve grid '
            'index 21 of 43, the curve midpoint, S3 = 0.8487). Both satisfy '
            'r_S = r_SM to solver precision, both are weight-1 states with '
            'S_alg = 0 for all three algebras. Recommend a footnote, not a '
            'correction.')

# ==========================================================================
# save
# ==========================================================================
with open(os.path.join(HERE, 'strengthen_results.json'), 'w') as fh:
    json.dump(out, fh, indent=2)
print("=" * 70)
print("Saved", os.path.join(HERE, 'strengthen_results.json'))
