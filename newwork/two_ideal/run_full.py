"""Step 2: full 32768-dimensional Fock-space numerics.

* Machine-verifies EVERY multiplicity in decomposition_full.json by explicit
  block-diagonal Schur analysis (Casimir spectra in all weight blocks).
* Builds the isotypic projectors and computes the gauge-invariant center
  data {p_i} for the named states, the 5-parameter product family, and a
  Haar ensemble.
* Singlet spectroscopy (the 28 invariant vectors, resolved by species
  numbers -> B and L): the 't Hooft-vertex catalog.
* The three-parameter test: Casimir-moment functionals (F3, F2, F1),
  their Jacobian on the product family, the exact particle-hole covariance
  p_i(psi) = p_ibar(K psi), and the (non-)factorization of the sector lattice.

Deterministic seed 20260610.  Writes results_full.json.
"""
import json
import time
import numpy as np

import model
import fock

t0 = time.time()
SEED = 20260610
rng = np.random.default_rng(SEED)
OUT = dict(seed=SEED)

table = json.load(open('decomposition_full.json'))
arena = fock.Arena(['Q', 'L', 'u', 'd', 'e'])
assert arena.dim == 32768

# ---------------------------------------------------------------------------
# 0. representation sanity checks
# ---------------------------------------------------------------------------
psi_t = rng.standard_normal(arena.dim) + 1j * rng.standard_normal(arena.dim)
psi_t /= np.linalg.norm(psi_t)
gen_mode = {sp: [fock.gen_coeff(sp, g) for g in range(12)] for sp in fock.SP_ORDER}
worst = 0.0
for _ in range(6):
    A, B = rng.integers(0, 12, 2)
    lhs = (arena.apply_onebody(arena.apply_onebody(psi_t, B), A)
           - arena.apply_onebody(arena.apply_onebody(psi_t, A), B))
    rhs = np.zeros_like(psi_t)
    for sp in arena.species:
        comm = gen_mode[sp][A] @ gen_mode[sp][B] - gen_mode[sp][B] @ gen_mode[sp][A]
        O = fock.onebody(sp, comm)
        if np.abs(O).max() > 1e-14:
            rhs += arena.apply_sp_op(psi_t, sp, O)
    worst = max(worst, float(np.linalg.norm(lhs - rhs)))
OUT['lie_algebra_closure_residual'] = worst
assert worst < 1e-10
g1, g2 = (fock.haar_su(3, rng), fock.haar_su(2, rng), rng.uniform(0, 12 * np.pi)), \
         (fock.haar_su(3, rng), fock.haar_su(2, rng), rng.uniform(0, 12 * np.pi))
v1 = arena.apply_gamma(arena.apply_gamma(psi_t, *g2), *g1)
v2 = arena.apply_gamma(psi_t, g1[0] @ g2[0], g1[1] @ g2[1], g1[2] + g2[2])
hom_res = float(np.linalg.norm(v1 - v2))
OUT['gamma_homomorphism_residual'] = hom_res
assert hom_res < 1e-10
eps = 1e-6
U3e = np.eye(3) + 1j * eps * fock.LAM[3] / 2
dv = (arena.apply_gamma(psi_t, U3e, np.eye(2), 0.0) - psi_t) / eps
gen_res = float(np.linalg.norm(dv - 1j * arena.apply_onebody(psi_t, 3)))
OUT['gamma_generator_residual_Oeps'] = gen_res
assert gen_res < 1e-4
print(f"[checks] closure {worst:.1e}, homomorphism {hom_res:.1e}, "
      f"generator {gen_res:.1e}  ({time.time()-t0:.0f}s)")

# ---------------------------------------------------------------------------
# 1. block Schur analysis
# ---------------------------------------------------------------------------
decomp = fock.analyze_arena(arena, table)
OUT['n_block_entries'] = len(decomp['blocks'])
OUT['all_multiplicities_verified'] = True
print(f"[schur] all {len(table)} sector multiplicities verified on the "
      f"32768-dim Fock space  ({time.time()-t0:.0f}s)")

c2_3 = np.array([fock.c2_su3(r['a'], r['b']) for r in table])
c2_2 = np.array([(r['twoj'] / 2) * (r['twoj'] / 2 + 1) for r in table])
ysq = np.array([(r['y'] / 6.0) ** 2 for r in table])
mvec = np.array([r['m'] for r in table])
nvec = np.array([r['dim'] for r in table])
sector_label = [(r['a'], r['b'], r['twoj'], r['y']) for r in table]
sid = {lab: i for i, lab in enumerate(sector_label)}
SINGLET = sid[(0, 0, 0, 0)]

# ---------------------------------------------------------------------------
# 2. singlet spectroscopy
# ---------------------------------------------------------------------------
sing = {}
for b in decomp['blocks']:
    if b['irrep'] != SINGLET:
        continue
    i0 = int(b['idx'][0])
    nv = tuple(bin(int(arena.sp_index(np.array([i0]), s)[0])).count('1')
               for s in arena.species)
    sing[nv] = sing.get(nv, 0) + b['vecs'].shape[1]
sing_table = []
for nv, cnt in sorted(sing.items()):
    nQ, nL, nu, nd, ne = nv
    B = (nQ + nu + nd) / 3.0
    L = float(nL + ne)
    sing_table.append(dict(n=dict(Q=nQ, L=nL, u=nu, d=nd, e=ne),
                           count=int(cnt), B=B, Lnum=L, BminusL=B - L,
                           fermion_number=int(sum(nv))))
OUT['singlet_spectroscopy'] = sing_table
assert sum(r['count'] for r in sing_table) == 28
assert (3, 1, 0, 0, 0) not in sing
OUT['QQQL_singlet_absent'] = True
assert sing.get((0, 0, 1, 2, 0)) == 1 and sing.get((1, 1, 1, 1, 0)) == 1
blvals = sorted({r['BminusL'] for r in sing_table})
OUT['BminusL_values_in_singlet_sector'] = blvals
assert len(blvals) > 1
print(f"[singlets] 28 invariant vectors over {len(sing_table)} species sectors; "
      f"B-L values {blvals}  ({time.time()-t0:.0f}s)")

# ---------------------------------------------------------------------------
# 3. states and their gauge-invariant center data
# ---------------------------------------------------------------------------

def probs(psi):
    return fock.sector_probs(decomp, table, psi)

def probs_batch(Psi):
    p = np.zeros((len(table), Psi.shape[1]))
    for b in decomp['blocks']:
        amp = b['vecs'].conj().T @ Psi[b['idx'], :]
        p[b['irrep'], :] += (np.abs(amp) ** 2).sum(axis=0)
    return p

def functionals(p):
    return dict(F3_C2su3=float(p @ c2_3), F2_C2su2=float(p @ c2_2),
                F1_Ysq=float(p @ ysq))

states = {}
vac = np.zeros(arena.dim, complex); vac[0] = 1
filled = np.zeros(arena.dim, complex); filled[-1] = 1
states['vacuum'] = vac
states['filled'] = filled
states['vac_plus_filled'] = (vac + filled) / np.sqrt(2)
uni = fock.product_state(arena, {s: (1 / np.sqrt(2), 1 / np.sqrt(2))
                                 for s in arena.species})
states['uniform_product'] = uni
th0 = dict(Q=0.7, L=0.9, u=1.1, d=0.5, e=1.3)
gen_state = fock.product_state(arena, {s: (np.cos(th0[s]), np.sin(th0[s]))
                                       for s in arena.species})
states['generic_product'] = gen_state

state_results = {}
for name, psi in states.items():
    assert abs(np.linalg.norm(psi) - 1) < 1e-12
    p = probs(psi)
    assert abs(p.sum() - 1) < 1e-9, (name, p.sum())
    nz = np.argsort(-p)[:12]
    state_results[name] = dict(
        center_entropy_bits=fock.shannon(p),
        n_sectors_occupied=int((p > 1e-12).sum()),
        functionals=functionals(p),
        top_sectors=[dict(label=sector_label[i], p=float(p[i])) for i in nz
                     if p[i] > 1e-12],
    )

pv, pf = probs(vac), probs(filled)
assert abs(pv[SINGLET] - 1) < 1e-12 and abs(pf[SINGLET] - 1) < 1e-12
state_results['vacuum']['note'] = (
    "p concentrated on the singlet sector; pure state in one sector with "
    "pure multiplicity state => total algebraic entropy 0")
state_results['vac_plus_filled']['note'] = (
    "both components are gauge singlets: the coherence between particle "
    "number 0 and 15 (Delta B = 4, Delta L = 3) is fully gauge-invariant "
    "data; still S = 0 (pure state in one sector)")
OUT['states'] = state_results

ginv_worst = 0.0
for name in ('uniform_product', 'generic_product', 'vac_plus_filled'):
    psi = states[name]
    p0 = probs(psi)
    for _ in range(3):
        g = fock.random_gauge(rng)
        p1 = probs(arena.apply_gamma(psi, *g))
        ginv_worst = max(ginv_worst, float(np.abs(p1 - p0).max()))
OUT['gauge_invariance_max_dp'] = ginv_worst
assert ginv_worst < 1e-9
print(f"[states] gauge invariance of p_i verified, max |dp| = {ginv_worst:.1e}"
      f"  ({time.time()-t0:.0f}s)")

# --- particle-hole / conjugation structure ---
conj_id = np.array([sid[(r['b'], r['a'], r['twoj'], -r['y'])] for r in table])
n = arena.nmodes
idx = np.arange(arena.dim)
eps = np.ones(arena.dim)
for i in range(n):
    for j in range(i):
        both = ((idx >> i) & 1) & (~(idx >> j) & 1)
        eps = np.where(both.astype(bool), -eps, eps)
comp = (~idx) & (arena.dim - 1)

def Kmap(psi):
    out = np.zeros_like(psi)
    out[comp] = eps * psi
    return out

# exact covariance p_i(psi) = p_ibar(K psi) -- the particle-hole theorem
ph_worst = 0.0
for psi in (uni, gen_state, psi_t):
    pa, pb = probs(psi), probs(Kmap(psi))
    ph_worst = max(ph_worst, float(np.abs(pa - pb[conj_id]).max()))
OUT['particle_hole_covariance_max_gap'] = ph_worst
assert ph_worst < 1e-10
# but the uniform state is NOT K-invariant: only PARTIAL degeneracy survives
p_uni = probs(uni)
gap = np.abs(p_uni - p_uni[conj_id])
pairs_mask = conj_id != np.arange(len(table))
OUT['uniform_state_conjugation'] = dict(
    max_gap=float(gap.max()),
    n_conjugate_pairs=int(pairs_mask.sum() // 2),
    n_pairs_exactly_degenerate=int(((gap < 1e-12) & pairs_mask).sum() // 2),
    n_self_conjugate_sectors=int((~pairs_mask).sum()),
    n_occupied_sectors=int((p_uni > 1e-14).sum()),
    n_distinct_p_values=int(len(np.unique(np.round(
        np.sort(p_uni[p_uni > 1e-14]), 13)))),
)
print(f"[degeneracy] PH covariance exact ({ph_worst:.1e}); uniform state: "
      f"{OUT['uniform_state_conjugation']['n_pairs_exactly_degenerate']} of "
      f"{OUT['uniform_state_conjugation']['n_conjugate_pairs']} pairs degenerate, "
      f"max gap {gap.max():.2e}")

# is the uniform state's p proportional to m*n (the Paper-2 mechanism)?
expected_p = mvec * nvec / arena.dim
OUT['uniform_state_p_vs_mn_over_D_max_gap'] = float(
    np.abs(p_uni - expected_p).max())

# ---------------------------------------------------------------------------
# 4. Haar ensemble
# ---------------------------------------------------------------------------
NH = 200
Z = (rng.standard_normal((arena.dim, NH)) + 1j * rng.standard_normal((arena.dim, NH)))
Z /= np.linalg.norm(Z, axis=0, keepdims=True)
PH_ = probs_batch(Z)
assert np.abs(PH_.sum(axis=0) - 1).max() < 1e-9
ce = np.array([fock.shannon(PH_[:, k]) for k in range(NH)])
OUT['haar'] = dict(
    n_samples=NH,
    center_entropy_mean=float(ce.mean()), center_entropy_std=float(ce.std()),
    max_abs_dev_meanp_vs_mn_over_D=float(np.abs(PH_.mean(axis=1) - expected_p).max()),
    center_entropy_of_mn_over_D=fock.shannon(expected_p),
    functionals_mean=dict(F3=float(PH_.mean(axis=1) @ c2_3),
                          F2=float(PH_.mean(axis=1) @ c2_2),
                          F1=float(PH_.mean(axis=1) @ ysq)),
)
print(f"[haar] center entropy {ce.mean():.3f} +- {ce.std():.3f} bits "
      f"({NH} states)  ({time.time()-t0:.0f}s)")

# ---------------------------------------------------------------------------
# 5. the three-parameter test
# ---------------------------------------------------------------------------
def direct_expectations(psi):
    e3 = sum(np.vdot(arena.apply_onebody(psi, A),
                     arena.apply_onebody(psi, A)).real for A in range(8))
    e2 = sum(np.vdot(arena.apply_onebody(psi, 8 + a),
                     arena.apply_onebody(psi, 8 + a)).real for a in range(3))
    e1 = np.vdot(arena.apply_onebody(psi, 11),
                 arena.apply_onebody(psi, 11)).real
    return np.array([e3, e2, e1])

for name in ('uniform_product', 'generic_product'):
    p = probs(states[name])
    fa = np.array([p @ c2_3, p @ c2_2, p @ ysq])
    fb = direct_expectations(states[name])
    res = float(np.abs(fa - fb).max())
    OUT.setdefault('functional_crosscheck_residuals', {})[name] = res
    assert res < 1e-8, (name, fa, fb)

def F_of_theta(th):
    psi = fock.product_state(arena, {s: (np.cos(th[s]), np.sin(th[s]))
                                     for s in arena.species})
    return direct_expectations(psi)

h = 1e-5
J = np.zeros((3, 5))
for k, s in enumerate(arena.species):
    tp = dict(th0); tp[s] += h
    tm = dict(th0); tm[s] -= h
    J[:, k] = (F_of_theta(tp) - F_of_theta(tm)) / (2 * h)
sv = np.linalg.svd(J, compute_uv=False)
OUT['three_parameter_test'] = dict(
    theta0=th0,
    F_at_theta0=[float(x) for x in F_of_theta(th0)],
    jacobian_F3_F2_F1_by_thetaQ_L_u_d_e=J.tolist(),
    singular_values=sv.tolist(),
    rank=int((sv > 1e-8 * sv[0]).sum()),
)
assert OUT['three_parameter_test']['rank'] == 3
Jp = np.linalg.pinv(J)
moves = {}
for k, nm in enumerate(['F3_su3', 'F2_su2', 'F1_Y2']):
    d = Jp[:, k]
    chk = J @ d
    moves[nm] = dict(dtheta=d.tolist(), achieved_dF=[float(x) for x in chk])
    tgt = np.zeros(3); tgt[k] = 1
    assert np.abs(chk - tgt).max() < 1e-6
OUT['three_parameter_test']['single_factor_directions'] = moves
print(f"[3-param] Jacobian rank 3 (sv {sv}); single-factor directions exist"
      f"  ({time.time()-t0:.0f}s)")

# 5c. mutual information of the sector labels
def label_MI(p):
    import collections
    P3, P2, P1 = collections.Counter(), collections.Counter(), collections.Counter()
    P32, P31, P21 = collections.Counter(), collections.Counter(), collections.Counter()
    for i, r in enumerate(table):
        if p[i] <= 0:
            continue
        l3, l2, l1 = (r['a'], r['b']), r['twoj'], r['y']
        P3[l3] += p[i]; P2[l2] += p[i]; P1[l1] += p[i]
        P32[(l3, l2)] += p[i]; P31[(l3, l1)] += p[i]; P21[(l2, l1)] += p[i]
    def H(c):
        v = np.array(list(c.values()))
        return fock.shannon(v / v.sum())
    return dict(I_su3_su2=H(P3) + H(P2) - H(P32),
                I_su3_Y=H(P3) + H(P1) - H(P31),
                I_su2_Y=H(P2) + H(P1) - H(P21),
                H_su3=H(P3), H_su2=H(P2), H_Y=H(P1))

OUT['label_mutual_information'] = dict(
    haar_mean_measure=label_MI(expected_p),
    uniform_state=label_MI(p_uni),
)
print("[labels] MI under Haar measure:", OUT['label_mutual_information']['haar_mean_measure'])

# 5d. blocks where a quantum piece is possible (n>1 and m>1)
nm_both = [i for i in range(len(table)) if mvec[i] > 1 and nvec[i] > 1]
OUT['sectors_with_n_and_m_gt1'] = dict(
    count=len(nm_both),
    fraction_of_fock_dim=float(sum(int(mvec[i]) * int(nvec[i]) for i in nm_both)
                               / arena.dim),
    examples=[dict(label=sector_label[i], m=int(mvec[i]), n=int(nvec[i]))
              for i in nm_both[:8]],
)

OUT['structure'] = dict(
    n_sectors=len(table), dim_commutant=int((mvec.astype(object) ** 2).sum()),
    dim_center=len(table), max_m=int(mvec.max()),
    sum_mn=int((mvec * nvec).sum()),
    n_sectors_m1=int((mvec == 1).sum()),
    largest_sectors_by_m=[dict(label=sector_label[i], m=int(mvec[i]),
                               n=int(nvec[i]))
                          for i in np.argsort(-mvec)[:10]],
)

with open('results_full.json', 'w') as f:
    json.dump(OUT, f, indent=1, default=float)
print(f"results_full.json written  ({time.time()-t0:.0f}s total)")
