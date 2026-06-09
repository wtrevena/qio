"""Figure 2: the entropy-flow (QIO 2.0) version."""
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import qio_lib as q

MZ, MPL = 91.1876, 1.22e19
B_SM = np.array([-7.0, -19/6, 41/10])
B_MSSM = np.array([-3.0, 1.0, 33/5])
INV0 = 1 / q.ALPHA
TMAX = np.log(MPL / MZ); T_SUSY = np.log(1000 / MZ)
r3 = json.load(open('results/exp3_results.json'))
A_rep, B_rep = r3['feasible_region']['representative_A'], r3['feasible_region']['representative_B']

fig, axes = plt.subplots(1, 3, figsize=(13.5, 3.8))
ts = np.linspace(0, TMAX, 800)
mus = MZ * np.exp(ts)
ai = INV0[:, None] - B_SM[:, None] / (2 * np.pi) * ts

# (a) running entropies at representative (A,B)
S = (ai - A_rep) / B_rep
lbl = [r'$S_1$ (SU(3))', r'$S_2$ (SU(2))', r'$S_3$ (U(1))']
for i, c in enumerate(['tab:red', 'tab:green', 'tab:blue']):
    axes[0].plot(mus, S[i], color=c, label=lbl[i])
axes[0].set_xscale('log'); axes[0].set_xlabel(r'$\mu$ (GeV)')
axes[0].set_ylabel(r'$S_i(\mu)$'); axes[0].legend(fontsize=8)
axes[0].set_title(f'(a) Running entropies, $A$={A_rep:.0f}, $B$={B_rep:.0f}', fontsize=10)

# (b) feasible (A,B) region
lam_tab = np.linspace(1e-9, 0.5, 100001); h_tab = q.h2(lam_tab)
A_grid = np.linspace(50, 200, 151); B_grid = np.linspace(-220, -30, 191)
tg = np.linspace(0, TMAX, 60); AIg = INV0[:, None] - B_SM[:, None] / (2 * np.pi) * tg
feas = np.zeros((len(A_grid), len(B_grid)))
for ia, A in enumerate(A_grid):
    for ib, B in enumerate(B_grid):
        Sg = (AIg - A) / B
        if Sg.min() < 0 or Sg.max() > 1: continue
        lam = np.interp(Sg, h_tab, lam_tab)
        feas[ia, ib] = 1 if np.all(2 * lam.max(0) <= lam.sum(0) + 1e-12) else 0.5
axes[1].imshow(feas.T, origin='lower', aspect='auto', cmap='Blues',
               extent=[A_grid[0], A_grid[-1], B_grid[0], B_grid[-1]])
axes[1].plot([A_rep], [B_rep], 'r*', ms=10)
axes[1].set_xlabel('A'); axes[1].set_ylabel('B')
axes[1].set_title('(b) Feasible (A,B): box (light) vs +polygon (dark)', fontsize=10)

# (c) entanglement asymmetry: spread/|B| SM vs MSSM
Bmin = abs(B_rep)
spread_sm = (ai.max(0) - ai.min(0)) / Bmin
axes[2].plot(mus, spread_sm, 'b-', label='SM')
ts2 = np.linspace(T_SUSY, TMAX, 800)
inv_s = INV0 - B_SM / (2 * np.pi) * T_SUSY
ai2 = inv_s[:, None] - B_MSSM[:, None] / (2 * np.pi) * (ts2 - T_SUSY)
axes[2].plot(MZ * np.exp(ts2), (ai2.max(0) - ai2.min(0)) / Bmin, 'g--', label='MSSM (1 TeV)')
axes[2].set_xscale('log'); axes[2].set_yscale('log')
axes[2].set_xlabel(r'$\mu$ (GeV)'); axes[2].set_ylabel(r'$\Delta S(\mu)$')
axes[2].legend(fontsize=8)
axes[2].set_title('(c) Entanglement asymmetry: SM never symmetrizes', fontsize=10)

plt.tight_layout()
plt.savefig('results/fig2_entropy_flow.pdf')
plt.savefig('results/fig2_entropy_flow.png', dpi=160)
print('saved fig2')
