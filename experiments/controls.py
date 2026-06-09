"""Null controls A-D (Sec 6.4)."""
import json
import numpy as np
import qio_lib as q

rng = np.random.default_rng(7)
out = {}

# Shared 3-qubit Haar sample with precomputed invariants
N = 10**6
psi = q.haar_states(N, rng=rng)
S = q.single_qubit_entropies(psi)
tau = q.three_tangle(psi)
ordered = (S[:, 0] > S[:, 1]) & (S[:, 1] > S[:, 2])
r = np.full(N, np.nan); r[ordered] = q.gap_ratio(S[ordered])

# ---------- Control A: non-genericity of the SM target ----------
# 300 random ordered coupling triples, log-uniform alpha in [0.001, 0.5].
M = 300
a = np.exp(rng.uniform(np.log(0.001), np.log(0.5), (M, 3)))
a = -np.sort(-a, axis=1)  # alpha_3 > alpha_2 > alpha_1 (descending)
L = np.log(1 / a)
r_targets = (L[:, 0] - L[:, 1]) / (L[:, 1] - L[:, 2])
rows = []
for rt in r_targets:
    m = ordered & (np.abs(r - rt) < 0.01)
    if m.sum() >= 20:
        rows.append((rt, m.sum(), tau[m].mean(), np.median(tau[m])))
rows = np.array(rows)
m_sm = ordered & (np.abs(r - q.R_SM) < 0.01)
sm_tau_mean = float(tau[m_sm].mean())
z = (sm_tau_mean - rows[:, 2].mean()) / rows[:, 2].std()
out['control_A'] = dict(
    n_targets=int(len(rows)),
    sm_matched_tau3_mean=sm_tau_mean,
    random_target_tau3_mean_of_means=float(rows[:, 2].mean()),
    random_target_tau3_std_of_means=float(rows[:, 2].std()),
    z_score_sm_vs_random_targets=float(z),
    note="If |z| < 2, the SM target's matching manifold is statistically "
         "generic among random coupling targets.")
print(f"Control A: SM matched tau3 mean {sm_tau_mean:.4f}; random-target "
      f"mean of means {rows[:,2].mean():.4f} +- {rows[:,2].std():.4f}; z = {z:.2f}")

# ---------- Control B: two-qubit comparison ----------
# Analytic: any 2-qubit PURE state has S1 = S2 (Schmidt decomposition),
# so log(alpha_i^-1) = A + B*S_i forces alpha_2 = alpha_3. Falsified by data.
psi2 = q.haar_states(10**5, nq=2, rng=rng)
S2q = q.single_qubit_entropies(psi2, nq=2)
maxdiff = float(np.abs(S2q[:, 0] - S2q[:, 1]).max())
out['control_B'] = dict(
    max_S1_minus_S2=maxdiff,
    note="2-qubit pure states have S1=S2 identically (Schmidt); the "
         "two-coupling logarithmic map with B!=0 is impossible. Three qubits "
         "is the minimal case where the ansatz has content.")
print(f"Control B: max|S1-S2| over 1e5 two-qubit states = {maxdiff:.2e} (analytic: 0)")

# ---------- Control C: four-qubit comparison ----------
N4 = 10**6
psi4 = q.haar_states(N4, nq=4, rng=rng)
S4 = q.single_qubit_entropies(psi4, nq=4)
# order-preserving triples of 4 qubits
triples = [(0, 1, 2), (0, 1, 3), (0, 2, 3), (1, 2, 3)]
rates = []
for t in triples:
    St = S4[:, t]
    m, _ = q.matching_filter(St)
    rates.append(m.mean())
m3, _ = q.matching_filter(S)
out['control_C'] = dict(
    match_rate_3qubit=float(m3.mean()),
    match_rates_4qubit_per_triple={str(t): float(x) for t, x in zip(triples, rates)},
    mean_match_rate_4qubit=float(np.mean(rates)),
    any_triple_rate=float(np.mean(
        np.any([q.matching_filter(S4[:, t])[0] for t in triples], axis=0))),
    note="If 4-qubit triples match at comparable rates, parameter count, not "
         "division-algebra structure, drives matching.")
print(f"Control C: 3-qubit match rate {m3.mean():.2e}; 4-qubit per-triple "
      f"{np.mean(rates):.2e}; any-of-4 {out['control_C']['any_triple_rate']:.2e}")

# ---------- Control D: shuffled qubit-gauge labels ----------
from itertools import permutations
perm_stats = {}
for p in permutations(range(3)):
    Sp = S[:, p]
    m, _ = q.matching_filter(Sp)
    perm_stats[str(p)] = dict(n_matched=int(m.sum()),
                              tau3_mean=float(tau[m].mean()))
out['control_D'] = dict(
    per_permutation=perm_stats,
    note="Haar measure is exchange-symmetric, so all 6 permutations must be "
         "statistically identical; confirms the label assignment currently "
         "carries no physical content for unconstrained states.")
print("Control D:", {k: v['n_matched'] for k, v in perm_stats.items()})

with open('results/controls_results.json', 'w') as f:
    json.dump(out, f, indent=2)
print("Saved results/controls_results.json")
