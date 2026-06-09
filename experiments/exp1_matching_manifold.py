"""Experiment 1: characterize the coupling-matching manifold (Sec 6.1).

N Haar-random 3-qubit states; retain those with S1>S2>S3 and
|r_S - 1.8174| < 0.01. Compare entanglement invariants of matched states
against ordering-matched (but ratio-unconstrained) Haar controls.
"""
import json, sys
import numpy as np
from scipy import stats
import qio_lib as q

N_TOTAL = int(sys.argv[1]) if len(sys.argv) > 1 else 10**7
BATCH = 10**6
rng = np.random.default_rng(42)

matched_psi, matched_S, matched_r = [], [], []
ctrl_psi, ctrl_S = [], []   # ordered-but-unconstrained controls
n_ordered = 0

for b in range(N_TOTAL // BATCH):
    psi = q.haar_states(BATCH, rng=rng)
    S = q.single_qubit_entropies(psi)
    mask, r = q.matching_filter(S)
    ordered = (S[:, 0] > S[:, 1]) & (S[:, 1] > S[:, 2])
    n_ordered += int(ordered.sum())
    matched_psi.append(psi[mask]); matched_S.append(S[mask]); matched_r.append(r[mask])
    if b == 0:  # control sample from first batch
        idx = np.where(ordered)[0][:20000]
        ctrl_psi, ctrl_S = psi[idx], S[idx]

psi_m = np.concatenate(matched_psi); S_m = np.concatenate(matched_S)
r_m = np.concatenate(matched_r)

# invariants
tau_m = q.three_tangle(psi_m);      tau_c = q.three_tangle(ctrl_psi)
C_m = q.concurrence_pairs(psi_m);   C_c = q.concurrence_pairs(ctrl_psi)

def summ(x):
    return dict(mean=float(np.mean(x)), std=float(np.std(x)),
                q05=float(np.quantile(x, .05)), q50=float(np.quantile(x, .5)),
                q95=float(np.quantile(x, .95)), min=float(np.min(x)), max=float(np.max(x)))

ks_tau = stats.ks_2samp(tau_m, tau_c)
ks_C = [stats.ks_2samp(C_m[:, i], C_c[:, i]) for i in range(3)]

# fraction of matched states that are W-class (tau3 ~ 0) vs GHZ-class
res = dict(
    N_total=N_TOTAL,
    n_ordered=n_ordered,
    n_matched=int(len(psi_m)),
    match_rate=len(psi_m) / N_TOTAL,
    match_rate_given_ordered=len(psi_m) / n_ordered,
    r_target=q.R_SM, tol=0.01,
    S_matched={f'S{i+1}': summ(S_m[:, i]) for i in range(3)},
    tau3_matched=summ(tau_m), tau3_control=summ(tau_c),
    conc_matched={f'C{p}': summ(C_m[:, i]) for i, p in enumerate(['12', '13', '23'])},
    conc_control={f'C{p}': summ(C_c[:, i]) for i, p in enumerate(['12', '13', '23'])},
    ks_tau3=dict(stat=float(ks_tau.statistic), p=float(ks_tau.pvalue)),
    ks_conc={p: dict(stat=float(k.statistic), p=float(k.pvalue))
             for p, k in zip(['C12', 'C13', 'C23'], ks_C)},
    frac_tau3_below_001_matched=float((tau_m < 0.01).mean()),
    frac_tau3_below_001_control=float((tau_c < 0.01).mean()),
)
with open('results/exp1_results.json', 'w') as f:
    json.dump(res, f, indent=2)
np.savez_compressed('results/exp1_matched_states.npz', psi=psi_m, S=S_m, r=r_m)
print(json.dumps(res, indent=2))
