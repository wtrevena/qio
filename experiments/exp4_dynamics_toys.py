"""Experiment 4: dynamics toys — can octonion-algebra Hamiltonians SELECT a vacuum?

The left-multiplication operators L_i = L_{e_i} (i=1..7) of the octonions are
real antisymmetric 8x8 matrices satisfying the Clifford relation
L_i L_j + L_j L_i = -2 delta_ij. On C^8 = three qubits, iL_i is Hermitian.
We test whether Hamiltonians built canonically from this algebra select
vacua with hierarchical entanglement.

  H_lin(c)  = sum_i c_i (i L_i)            (linear / "mass" terms)
  H_quad(J) = sum_{i<j} J_ij (i L_i L_j)   (quadratic / so(7) "rotor" terms)
"""
import json
from itertools import combinations
import numpy as np
import qio_lib as q

# ---- octonion left-multiplication matrices via Cayley-Dickson ----
def cd_mult(x, y, n):
    if n == 0:
        return np.array([x[0] * y[0]])
    h = len(x) // 2
    a, b, c, d = x[:h], x[h:], y[:h], y[h:]
    conj = lambda z: np.concatenate(([z[0]], -z[1:]))
    return np.concatenate([cd_mult(a, c, n-1) - cd_mult(conj(d), b, n-1),
                           cd_mult(d, a, n-1) + cd_mult(b, conj(c), n-1)])

E = np.eye(8)
L = np.zeros((8, 8, 8))
for i in range(8):
    for b in range(8):
        L[i][:, b] = cd_mult(E[i], E[b], 3)
# Clifford check for imaginary units
for i in range(1, 8):
    for j in range(1, 8):
        anti = L[i] @ L[j] + L[j] @ L[i]
        assert np.allclose(anti, -2 * np.eye(8) * (i == j)), (i, j)
print("Clifford relations verified: L_i L_j + L_j L_i = -2 delta_ij")

iL = [None] + [1j * L[i] for i in range(1, 8)]
out = {}

def ground_entropies(H, tol=1e-9):
    w, v = np.linalg.eigh(H)
    deg = int((w < w[0] + tol).sum())
    psi = v[:, 0].reshape(1, 8)
    S = q.single_qubit_entropies(psi)[0]
    return w, deg, S, float(q.three_tangle(psi)[0]), psi

# ---- 1. linear Hamiltonians: spectrum forced by Clifford algebra ----
rng = np.random.default_rng(11)
res_lin = []
for trial in range(200):
    c = rng.standard_normal(7)
    H = sum(c[i-1] * iL[i] for i in range(1, 8))
    w = np.linalg.eigvalsh(H)
    res_lin.append((w[0], (w < w[0] + 1e-9).sum()))
degs = [d for _, d in res_lin]
out['linear'] = dict(
    ground_degeneracy_always=int(degs[0]) if len(set(degs)) == 1 else None,
    note="H = sum c_i iL_i has H^2 = |c|^2: spectrum +-|c|, each 4-fold "
         "degenerate, for EVERY coupling vector c. Linear algebra-canonical "
         "dynamics cannot select a unique vacuum. Within the 4-dim ground "
         "manifold, entropy triples are unconstrained by the dynamics.")
print(f"Linear H: ground degeneracy = {set(degs)} for all 200 random c")

# ---- 2. commuting quadratic triples: discrete vacua ----
# Partition 6 of the 7 indices into 3 disjoint pairs; the three iL_aL_b
# commute, giving a unique joint ground state for generic couplings,
# independent of coupling magnitudes (signs only) -> DISCRETE vacuum set.
res_pairs = []
idx = range(1, 8)
seen_S = set()
for trio in combinations(combinations(idx, 2), 3):
    flat = [x for p in trio for x in p]
    if len(set(flat)) != 6:
        continue
    H = sum(iL[a] @ iL[b] for (a, b) in trio)  # + couplings: signs only matter
    w, deg, S, tau, psi = ground_entropies(H)
    rS = None
    if S[0] > S[1] > S[2] and S[1] - S[2] > 1e-9:
        rS = float((S[0]-S[1])/(S[1]-S[2]))
    res_pairs.append(dict(pairs=str(trio), deg=deg,
                          S=[round(float(s), 6) for s in S],
                          tau3=round(tau, 6), r_S=rS))
    seen_S.add(tuple(np.round(np.sort(S), 6)))
out['quadratic_commuting'] = dict(
    n_partitions=len(res_pairs),
    distinct_sorted_entropy_triples=[list(s) for s in sorted(seen_S)],
    any_hierarchical=any(r['r_S'] is not None for r in res_pairs),
    sample=res_pairs[:6],
    note="Vacua form a DISCRETE set determined by algebra + pairing choice; "
         "coupling magnitudes are irrelevant (commuting involutions).")
print(f"Quadratic commuting: {len(res_pairs)} pairings, "
      f"distinct sorted S-triples: {sorted(seen_S)}")

# ---- 3. generic so(7) quadratic Hamiltonians ----
res_so7 = []
for trial in range(2000):
    Jm = rng.standard_normal((7, 7))
    H = np.zeros((8, 8), complex)
    for a in range(1, 8):
        for b in range(a+1, 8):
            H += Jm[a-1, b-1] * (iL[a] @ iL[b])
    w, deg, S, tau, psi = ground_entropies(H)
    rS = np.nan
    if S[0] > S[1] > S[2] and S[1] - S[2] > 1e-12:
        rS = (S[0]-S[1])/(S[1]-S[2])
    res_so7.append((deg, *S, tau, rS))
arr = np.array([r[1:] for r in res_so7])
degs7 = [r[0] for r in res_so7]
rs = arr[:, 4]
ok = ~np.isnan(rs)
out['so7_random'] = dict(
    n=2000, ground_degeneracy=sorted(set(degs7)),
    frac_ordered_S1_S2_S3=float(ok.mean()),
    frac_match_rS=float((np.abs(rs[ok] - q.R_SM) < 0.05).mean()) if ok.any() else 0.0,
    S_mean=[float(x) for x in arr[:, :3].mean(0)],
    tau3_mean=float(arr[:, 3].mean()),
    note="Generic so(7) rotor Hamiltonians from the Clifford algebra: do "
         "their unique ground states produce hierarchical entropies, and at "
         "what rate do they hit the matching window |r_S-1.8174|<0.05?")
print(f"so(7) random: degeneracies {sorted(set(degs7))}, "
      f"ordered frac {ok.mean():.3f}, "
      f"match frac {(np.abs(rs[ok]-q.R_SM)<0.05).mean():.4f}, "
      f"mean S {arr[:,:3].mean(0).round(4)}")

# ---- 4. octonion-structured so(7): J from the multiplication table ----
SIG = np.zeros((8, 8))
for a in range(8):
    for bb in range(8):
        p = cd_mult(E[a], E[bb], 3)
        SIG[a, bb] = p[a ^ bb]
H = np.zeros((8, 8), complex)
for a in range(1, 8):
    for bb in range(a+1, 8):
        H += SIG[a, bb] * (iL[a] @ iL[bb])
w, deg, S, tau, psi = ground_entropies(H)
out['octonion_structured_so7'] = dict(
    spectrum=[float(x) for x in np.round(w, 6)], ground_degeneracy=deg,
    S=[float(s) for s in S], tau3=tau,
    note="J_ab = sign of e_a e_b: the canonical algebra-derived rotor "
         "Hamiltonian. Degeneracy/symmetry pattern of its vacuum.")
print(f"Octonion-structured so(7): deg={deg}, S={S.round(4)}, tau3={tau:.4f}")

with open('results/exp4_results.json', 'w') as f:
    json.dump(out, f, indent=2)
print("Saved results/exp4_results.json")
