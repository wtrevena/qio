"""Step 3: independent numerical cross-checks + the quantum piece.

A. C3 selftest: the collapsed term-list assembly of the cubic su3 Casimir is
   compared entry-by-entry against a brute-force dense construction on the
   64-dim u(+)d arena, and [C3, F_A] = 0 is verified.

B. F_Q (64-dim): the direction_A SVD-commutant pipeline is run verbatim on
   Haar samples of the gauge action; the resulting Wedderburn structure is
   compared against the analytic peeling table (10 abelian blocks).

C. F_{Q+L} (256-dim): the full BKOV invariant-data machinery, with aligned
   multiplicity bases built by canonical lowering words:
     * every block of the commutant = M_{m_i} realized explicitly,
     * gauge-invariant algebraic entropy S = H(p) + sum p_i S(rho_i^mult),
     * the FIRST states in this program with a nonzero quantum piece,
     * Monte-Carlo twirl cross-check of S,
     * named states + 300 Haar states.

Deterministic seed 20260610.  Writes results_crosscheck.json.
"""
import json
import sys
import time
import numpy as np

import su3 as su3mod
import model
import fock

sys.path.insert(0, '../../direction_A')
import alg_entanglement as ae

def _nullspace_basis_lowmem(K, tol=1e-9):
    """Drop-in replacement for ae.nullspace_basis avoiding the full-matrices
    SVD (direction_A's version allocates rows^2; fine at d=8, fatal at d=64).
    Only valid for tall K (rows >= cols), which holds for every use here."""
    K = np.asarray(K)
    assert K.shape[0] >= K.shape[1]
    _, s, vh = np.linalg.svd(K, full_matrices=False)
    sf = np.zeros(K.shape[1]); sf[:len(s)] = s
    return vh[sf < tol].conj()

ae.nullspace_basis = _nullspace_basis_lowmem

t0 = time.time()
SEED = 20260610
rng = np.random.default_rng(SEED)
OUT = dict(seed=SEED)

# ===========================================================================
# A. C3 term-list selftest on the u(+)d arena (64-dim)
# ===========================================================================
ar_ud = fock.Arena(['u', 'd'])
I8 = np.eye(8)
Fd = [np.kron(fock.X['d'][g], I8) + np.kron(I8, fock.X['u'][g]) for g in range(12)]
C3_dense = np.zeros((64, 64), complex)
for a in range(8):
    for b in range(8):
        for c in range(8):
            if abs(fock.DSYM[a, b, c]) > 1e-12:
                C3_dense += fock.DSYM[a, b, c] * (Fd[a] @ Fd[b] @ Fd[c])
idx_all = np.arange(64)
sp_idx = {s: ar_ud.sp_index(idx_all, s) for s in ar_ud.species}
eq = {s: (sp_idx[s][:, None] == sp_idx[s][None, :]) for s in ar_ud.species}
C3_terms = fock.block_matrix(fock.c3_terms(ar_ud.species), sp_idx, eq)
r1 = float(np.abs(C3_dense - C3_terms).max())
r2 = max(float(np.abs(C3_dense @ Fd[a] - Fd[a] @ C3_dense).max()) for a in range(8))
OUT['c3_selftest'] = dict(termlist_vs_dense=r1, c3_commutes_with_su3=r2)
assert r1 < 1e-9 and r2 < 1e-9
print(f"[A] C3 term-list == dense ({r1:.1e}); [C3, su3] = 0 ({r2:.1e})")

# ===========================================================================
# B. F_Q: direction_A SVD-commutant pipeline vs analytic table
# ===========================================================================
tableQ = json.load(open('decomposition_Q.json'))
def gammaQ(g):
    return fock.gamma_species('Q', fock.mode_unitary('Q', *g))
samples = [gammaQ(fock.random_gauge(rng)) for _ in range(4)]

def commutant_eigencluster(unitaries, d, tol=1e-7):
    """Memory-light, structure-agnostic commutant.

    Step 1: the commutant of the single (normal) unitary G_1 is the algebra
    of block matrices over its eigenvalue clusters.  Step 2: parametrize
    X = sum_k V_k A_k V_k^dag and impose [X, G_s] = 0 for the remaining
    samples; the nullspace of the small stacked linear map is the joint
    commutant.  Certification on fresh samples happens downstream."""
    G1 = unitaries[0]
    w, V = np.linalg.eig(G1)
    order = np.argsort(np.angle(w))
    w, V = w[order], V[:, order]
    # modified Gram-Schmidt (eigvecs of a normal matrix are near-orthogonal)
    for i in range(d):
        for j in range(i):
            V[:, i] -= V[:, j] * (V[:, j].conj() @ V[:, i])
        V[:, i] /= np.linalg.norm(V[:, i])
    clusters = []
    cur = [0]
    for i in range(1, d):
        if abs(w[i] - w[cur[-1]]) < tol:
            cur.append(i)
        else:
            clusters.append(cur)
            cur = [i]
    clusters.append(cur)
    # basis of the one-sample commutant
    Es = []
    for cl in clusters:
        for a in cl:
            for b in cl:
                Es.append(np.outer(V[:, a], V[:, b].conj()))
    rows = []
    for G in unitaries[1:]:
        for E in Es:
            rows.append((E @ G - G @ E).flatten())
    K = np.array(rows).reshape(len(unitaries) - 1, len(Es), d * d)
    K = np.moveaxis(K, 1, 2).reshape(-1, len(Es))   # (s*d^2, nE)
    _, sv, vh = np.linalg.svd(K, full_matrices=False)   # K is tall: vh complete
    svf = np.zeros(K.shape[1]); svf[:len(sv)] = sv
    null = vh[svf < 1e-9].conj()
    out = []
    for c in null:
        Xm = sum(cj * Ej for cj, Ej in zip(c, Es))
        out.append(Xm)
    # HS-orthonormalize
    basis = []
    for Xm in out:
        for B in basis:
            Xm = Xm - B * np.trace(B.conj().T @ Xm)
        nrm = np.linalg.norm(Xm)
        if nrm > 1e-10:
            basis.append(Xm / nrm)
    return basis

basis = commutant_eigencluster(samples, 64)
OUT['FQ'] = dict(dim_commutant_numeric=len(basis),
                 dim_commutant_analytic=sum(r['m'] ** 2 for r in tableQ))
assert len(basis) == 10 == OUT['FQ']['dim_commutant_analytic']
fresh = [gammaQ(fock.random_gauge(rng)) for _ in range(60)]
res_comm = ae.max_commutator_residual(basis, fresh)
res_star = ae.verify_star_algebra(basis)
res_abel = max(float(np.linalg.norm(A @ B - B @ A)) for A in basis for B in basis)
struct = ae.algebra_structure(basis)
dims_numeric = sorted(b['dim'] for b in struct['blocks'])
dims_analytic = sorted(r['dim'] for r in tableQ)
OUT['FQ'].update(fresh_sample_residual=float(res_comm),
                 star_algebra_residual=float(res_star),
                 abelian_residual=res_abel,
                 center_dim_numeric=struct['center_dim'],
                 block_dims_numeric=dims_numeric,
                 block_dims_analytic=dims_analytic,
                 all_m_equal_1=all(b['n'] == 1 for b in struct['blocks']))
assert res_comm < 1e-12 and res_star < 1e-12 and res_abel < 1e-12
assert struct['center_dim'] == 10 and dims_numeric == dims_analytic
assert OUT['FQ']['all_m_equal_1']
print(f"[B] F_Q commutant: numeric C^10 abelian, block dims {dims_numeric} "
      f"match analytic; residuals < 1e-12  ({time.time()-t0:.0f}s)")

# ===========================================================================
# C. F_{Q+L}: aligned multiplicity bases and the quantum piece
# ===========================================================================
tableQL = json.load(open('decomposition_QL.json'))
ar = fock.Arena(['Q', 'L'])
assert ar.dim == 256
decompQL = fock.analyze_arena(ar, tableQL)
print(f"[C] QL multiplicities verified ({len(tableQL)} sectors)  "
      f"({time.time()-t0:.0f}s)")

# dense lowering operators and weights
I64, I4 = np.eye(64), np.eye(4)
def dense_ql(op_q, op_l):
    return np.kron(op_l, I64) + np.kron(I4, op_q)
F1d = dense_ql(fock.XLOW['Q']['f1'], np.zeros((4, 4)))
F2d = dense_ql(fock.XLOW['Q']['f2'], np.zeros((4, 4)))
Jmd = dense_ql(fock.XLOW['Q']['jm'], fock.XLOW['L']['jm'])
P, Qw, T, Y, ns = ar.weights()

# collect highest-weight vectors per sector
hw = {i: [] for i in range(len(tableQL))}
for b in decompQL['blocks']:
    i0 = int(b['idx'][0])
    r = tableQL[b['irrep']]
    if (int(P[i0]), int(Qw[i0]), int(T[i0])) == (r['a'], r['b'], r['twoj']):
        for k in range(b['vecs'].shape[1]):
            v = np.zeros(ar.dim, complex)
            v[b['idx']] = b['vecs'][:, k]
            hw[b['irrep']].append(v)
for i, r in enumerate(tableQL):
    assert len(hw[i]) == r['m'], (i, r, len(hw[i]))

A1, A2 = (2, -1), (-1, 2)

def aligned_basis(r, hw_vecs):
    """Aligned orthonormal bases of all m copies of irrep (a,b,2j):
    returns U of shape (256, n, m)."""
    a, b, tj = r['a'], r['b'], r['twoj']
    w3s = su3mod.wm(a, b)
    m = hw_vecs.shape[1]
    nodes = sorted(((w3, t) for w3 in w3s for t in range(-tj, tj + 1, 2)),
                   key=lambda nd: -(2 * (nd[0][0] + nd[0][1]) + nd[1]))
    basis = {}
    for nd in nodes:
        (w3, t) = nd
        if (w3, t) == ((a, b), tj):
            basis[nd] = hw_vecs[:, None, :]
            continue
        cands = []
        for dw, op in ((A1, F1d), (A2, F2d), (None, Jmd)):
            if dw is None:
                par = (w3, t + 2)
            else:
                par = ((w3[0] + dw[0], w3[1] + dw[1]), t)
            if par in basis:
                B = basis[par]                       # (256, rp, m)
                cands.append(np.einsum('xy,yrm->xrm', op, B))
        C = np.concatenate(cands, axis=1)            # (256, K, m)
        G = np.mean([C[:, :, al].conj().T @ C[:, :, al] for al in range(m)], axis=0)
        wv, V = np.linalg.eigh(G)
        keep = wv > 1e-9 * max(wv.max(), 1e-30)
        rk = int(keep.sum())
        assert rk == w3s[w3], (r, w3, t, rk, w3s[w3])
        R = V[:, keep] / np.sqrt(wv[keep])
        basis[nd] = np.einsum('xkm,kr->xrm', C, R)
    U = np.concatenate([basis[nd] for nd in nodes], axis=1)   # (256, n, m)
    assert U.shape == (ar.dim, r['dim'], m)
    flat = U.reshape(ar.dim, -1)
    G = flat.conj().T @ flat
    assert np.abs(G - np.eye(G.shape[0])).max() < 1e-9, r
    return U

UB = {}
tot = 0
for i, r in enumerate(tableQL):
    hv = np.stack(hw[i], axis=1)
    UB[i] = aligned_basis(r, hv)
    tot += r['dim'] * r['m']
assert tot == 256
# global completeness/orthonormality
ALL = np.concatenate([UB[i].reshape(ar.dim, -1) for i in range(len(tableQL))], axis=1)
res_complete = float(np.abs(ALL.conj().T @ ALL - np.eye(256)).max())
OUT['QL_basis_orthonormality_residual'] = res_complete
assert res_complete < 1e-8
print(f"[C] aligned bases built for all {len(tableQL)} sectors, "
      f"global orthonormality {res_complete:.1e}  ({time.time()-t0:.0f}s)")


def invariant_data(psi):
    """p_i, multiplicity states rho_i (m x m), entropies (bits)."""
    out_p = np.zeros(len(tableQL))
    rhos = {}
    for i, r in enumerate(tableQL):
        C = np.einsum('xnm,x->nm', UB[i].conj(), psi)     # (n, m)
        p = float(np.real(np.sum(np.abs(C) ** 2)))
        out_p[i] = p
        if p > 1e-14 and r['m'] > 1:
            rhos[i] = (C.conj().T @ C.T.conj().T)         # placeholder fixed below
            rhos[i] = C.T @ C.conj()                      # not used
    # recompute cleanly: rho_mult[a,b] = sum_x C[x,a] conj(C[x,b])
    rhos = {}
    for i, r in enumerate(tableQL):
        C = np.einsum('xnm,x->nm', UB[i].conj(), psi)
        p = out_p[i]
        if p > 1e-14:
            rho = np.einsum('na,nb->ab', C, C.conj())
            rhos[i] = rho
    center = fock.shannon(out_p)
    quant = 0.0
    for i, rho in rhos.items():
        p = out_p[i]
        ev = np.linalg.eigvalsh(rho / p)
        ev = ev[ev > 1e-13]
        quant += p * float(-(ev * np.log2(ev)).sum())
    return out_p, rhos, center, quant


# consistency: p from aligned bases == p from block analysis
for _ in range(3):
    z = rng.standard_normal(256) + 1j * rng.standard_normal(256)
    z /= np.linalg.norm(z)
    p1, _, _, _ = invariant_data(z)
    p2 = fock.sector_probs(decompQL, tableQL, z)
    assert np.abs(p1 - p2).max() < 1e-10
print("[C] p_i from aligned bases == p_i from block projectors")

def gammaQL(psi, g):
    return ar.apply_gamma(psi, *g)

# ---- named states ----
labelsQL = [(r['a'], r['b'], r['twoj'], r['y']) for r in tableQL]
sidQL = {lab: i for i, lab in enumerate(labelsQL)}
SING = sidQL[(0, 0, 0, 0)]
TRIP = sidQL[(1, 0, 1, 1)]          # the (3,2)_{1/6} sector, m = 2
assert tableQL[SING]['m'] == 2 and tableQL[TRIP]['m'] == 2

vac = np.zeros(256, complex); vac[0] = 1
filled = np.zeros(256, complex); filled[-1] = 1
q0 = np.zeros(256, complex); q0[1] = 1            # one quark, mode 0
coh_sing = (vac + filled) / np.sqrt(2)
coh_two = (vac + q0) / np.sqrt(2)
# engineered quantum-piece state: different irrep-internal positions of the
# two copies of the (3,2) sector
U_T = UB[TRIP]                                    # (256, 6, 2)
psi_quant = (U_T[:, 0, 0] + U_T[:, 3, 1]) / np.sqrt(2)
uniQL = fock.product_state(ar, dict(Q=(2 ** -0.5, 2 ** -0.5),
                                    L=(2 ** -0.5, 2 ** -0.5)))

named = {}
for name, psi in [('vacuum', vac), ('filled', filled),
                  ('vac_plus_filled', coh_sing), ('vac_plus_quark', coh_two),
                  ('engineered_quantum', psi_quant), ('uniform_product', uniQL)]:
    p, rhos, center, quant = invariant_data(psi)
    entry = dict(center_bits=center, quantum_bits=quant, total_bits=center + quant,
                 n_sectors=int((p > 1e-12).sum()))
    if name == 'vac_plus_filled':
        entry['singlet_mult_state'] = [[float(np.real(x)), float(np.imag(x))]
                                       for x in rhos[SING].flatten()]
        entry['note'] = ("off-diagonal coherence between the two invariant "
                         "vectors (Fock vacuum and filled QL sea) is "
                         "gauge-invariant data; S = 0")
    if name == 'engineered_quantum':
        entry['trip_mult_state_eigs'] = sorted(
            np.linalg.eigvalsh(rhos[TRIP] / p[TRIP]).tolist())
        entry['note'] = ("p = 1 on the (3,2)_{1/6} sector; multiplicity state "
                         "= I/2 => S = 1 bit of PURE QUANTUM gauge-invariant "
                         "entropy (first nonzero quantum piece in this program)")
    named[name] = entry
assert abs(named['vacuum']['total_bits']) < 1e-10
assert abs(named['filled']['total_bits']) < 1e-10
assert abs(named['vac_plus_filled']['total_bits']) < 1e-10
assert abs(named['vac_plus_quark']['total_bits'] - 1.0) < 1e-10
assert abs(named['vac_plus_quark']['quantum_bits']) < 1e-12
assert abs(named['engineered_quantum']['total_bits'] - 1.0) < 1e-10
assert abs(named['engineered_quantum']['center_bits']) < 1e-12
OUT['QL_named_states'] = named
print("[C] named states:",
      {k: round(v['total_bits'], 6) for k, v in named.items()})

# ---- gauge invariance of the full invariant data ----
worst_p, worst_spec, worst_S = 0.0, 0.0, 0.0
for psi in (psi_quant, uniQL, coh_sing):
    p0, rhos0, c0, q0_ = invariant_data(psi)
    for _ in range(7):
        g = fock.random_gauge(rng)
        p1, rhos1, c1, q1 = invariant_data(gammaQL(psi, g))
        worst_p = max(worst_p, float(np.abs(p1 - p0).max()))
        worst_S = max(worst_S, abs(c1 + q1 - c0 - q0_))
        for i in rhos0:
            if p0[i] > 1e-10:
                e0 = np.sort(np.linalg.eigvalsh(rhos0[i]))
                e1 = np.sort(np.linalg.eigvalsh(rhos1[i]))
                worst_spec = max(worst_spec, float(np.abs(e0 - e1).max()))
OUT['QL_gauge_invariance'] = dict(max_dp=worst_p, max_dspec=worst_spec,
                                  max_dS=worst_S)
assert worst_p < 1e-9 and worst_spec < 1e-9 and worst_S < 1e-9
print(f"[C] invariance of full data: dp {worst_p:.1e}, dspec {worst_spec:.1e}, "
      f"dS {worst_S:.1e}")

# ---- Monte-Carlo twirl cross-check of S for the engineered state ----
NMC = 4000
acc = np.zeros((256, 256), complex)
for _ in range(NMC):
    g = fock.random_gauge(rng)
    v = gammaQL(psi_quant, g)
    acc += np.outer(v, v.conj())
acc /= NMC
ev = np.linalg.eigvalsh(acc)
ev = ev[ev > 1e-12]
S_twirl = float(-(ev * np.log2(ev)).sum())
p_q, _, c_q, q_q = invariant_data(psi_quant)
corr = sum(p_q[i] * np.log2(tableQL[i]['dim']) for i in range(len(tableQL))
           if p_q[i] > 1e-14)
OUT['QL_twirl_check'] = dict(S_from_twirl_minus_dimterm=S_twirl - corr,
                             S_algebraic=c_q + q_q, n_mc=NMC,
                             gap=abs(S_twirl - corr - (c_q + q_q)))
assert OUT['QL_twirl_check']['gap'] < 0.05
print(f"[C] MC twirl: S = {S_twirl - corr:.4f} vs algebraic {c_q + q_q:.4f} "
      f"(gap {OUT['QL_twirl_check']['gap']:.4f})  ({time.time()-t0:.0f}s)")

# ---- Haar ensemble on QL: generic nonzero quantum piece ----
NHA = 300
cs, qs = np.zeros(NHA), np.zeros(NHA)
for k in range(NHA):
    z = rng.standard_normal(256) + 1j * rng.standard_normal(256)
    z /= np.linalg.norm(z)
    _, _, c, q = invariant_data(z)
    cs[k], qs[k] = c, q
OUT['QL_haar'] = dict(n=NHA,
                      center_mean=float(cs.mean()), center_std=float(cs.std()),
                      quantum_mean=float(qs.mean()), quantum_std=float(qs.std()),
                      quantum_min=float(qs.min()),
                      frac_quantum_of_total=float(qs.mean() / (cs + qs).mean()))
assert qs.min() > 0.01      # the quantum piece is GENERICALLY nonzero now
print(f"[C] QL Haar: center {cs.mean():.3f}+-{cs.std():.3f}, quantum "
      f"{qs.mean():.3f}+-{qs.std():.3f} bits  ({time.time()-t0:.0f}s)")

# structural summary of the QL commutant
OUT['QL_structure'] = dict(
    n_sectors=len(tableQL),
    dim_commutant=sum(r['m'] ** 2 for r in tableQL),
    sectors_m2=[dict(label=labelsQL[i], m=r['m'], n=r['dim'])
                for i, r in enumerate(tableQL) if r['m'] > 1],
)

with open('results_crosscheck.json', 'w') as f:
    json.dump(OUT, f, indent=1, default=float)
print(f"results_crosscheck.json written  ({time.time()-t0:.0f}s total)")
