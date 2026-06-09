"""Generate paper figures from experiment results."""
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import qio_lib as q

fig, axes = plt.subplots(1, 3, figsize=(13.5, 3.8))

# --- Panel 1: r_SM(mu) under one-loop running ---
MZ = 91.1876
b = np.array([-7.0, -19/6, 41/10])
inv_MZ = np.log(1 / q.ALPHA) * 0 + 1 / q.ALPHA
mus = np.logspace(1, 13.5, 2000)
rs = []
for mu in mus:
    invs = inv_MZ - b / (2 * np.pi) * np.log(mu / MZ)
    L = np.log(invs)
    rs.append((L[0] - L[1]) / (L[1] - L[2]))
rs = np.array(rs)
ax = axes[0]
ax.plot(mus, rs, 'b-', lw=1.5)
ax.axhline(q.R_SM, color='gray', ls=':', lw=1)
ax.axvline(MZ, color='gray', ls='--', lw=0.8)
ax.annotate(r'$M_Z$', (MZ * 1.5, 0.5), fontsize=9)
ax.set_xscale('log'); ax.set_ylim(-1, 6)
ax.set_xlabel(r'$\mu$ (GeV)'); ax.set_ylabel(r'$r_{SM}(\mu)$')
ax.set_title('(a) Scale dependence of gap ratio', fontsize=10)

# --- Panel 2: tau3 distributions, matched vs control ---
d = np.load('results/exp1_matched_states.npz')
tau_m = q.three_tangle(d['psi'])
rng = np.random.default_rng(3)
psi_c = q.haar_states(10**5, rng=rng)
S_c = q.single_qubit_entropies(psi_c)
ordc = (S_c[:, 0] > S_c[:, 1]) & (S_c[:, 1] > S_c[:, 2])
tau_c = q.three_tangle(psi_c[ordc])
ax = axes[1]
bins = np.linspace(0, 1, 50)
ax.hist(tau_c, bins=bins, density=True, alpha=0.5, label='Haar (ordered)', color='gray')
ax.hist(tau_m, bins=bins, density=True, alpha=0.6, label=r'matched $|r_S - r_{SM}|<0.01$',
        color='tab:blue')
ax.set_xlabel(r'3-tangle $\tau_3$'); ax.set_ylabel('density')
ax.legend(fontsize=8)
ax.set_title('(b) Matching manifold is generic', fontsize=10)

# --- Panel 3: weighted-W matching curve in the weight simplex ---
# fast h2 inverse via interpolation table
_lam = np.linspace(1e-9, 0.5, 200001)
_h = q.h2(_lam)
def weight(S):
    return np.interp(S, _h, _lam)
pts = []
for S3 in np.linspace(0.30, 0.97, 400):
    s2g = np.linspace(S3 + 1e-6, 0.999, 2000)
    S1g = s2g + q.R_SM * (s2g - S3)
    valid = S1g < 1
    s2g, S1g = s2g[valid], S1g[valid]
    res = weight(S1g) + weight(s2g) + weight(S3) - 1
    for i in np.where(np.diff(np.sign(res)) != 0)[0]:
        # linear refine
        x0, x1, y0, y1 = s2g[i], s2g[i+1], res[i], res[i+1]
        s2 = x0 - y0 * (x1 - x0) / (y1 - y0)
        S1 = s2 + q.R_SM * (s2 - S3)
        pts.append((weight(S3), weight(s2), weight(S1)))  # a^2, b^2, c^2
pts = np.array(pts)
ax = axes[2]
ax.plot(pts[:, 0], pts[:, 2], 'r-', lw=2, label=r'$c^2$ (qubit 1, $S_1$)')
ax.plot(pts[:, 0], pts[:, 1], 'b-', lw=2, label=r'$b^2$ (qubit 2, $S_2$)')
ax.plot(pts[:, 0], pts[:, 0], 'k:', lw=1, label=r'$a^2$ (qubit 3, $S_3$)')
ax.set_xlabel(r'$a^2$'); ax.set_ylabel('weights')
ax.legend(fontsize=8)
ax.set_title(r'(c) Weighted-$W$ matching curve ($\tau_3 = 0$)', fontsize=10)

plt.tight_layout()
plt.savefig('results/fig1_experiments.pdf')
plt.savefig('results/fig1_experiments.png', dpi=160)
print('saved results/fig1_experiments.pdf/png; weighted-W curve points:', len(pts))
