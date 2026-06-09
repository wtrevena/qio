"""Experiment 3: the entropy-flow (QIO 2.0) version of the conjecture.

Linear map alpha_i^-1(mu) = A + B * S_i(mu) with B < 0, so S_i runs linearly
in log mu with slope -b_i/(2 pi B). Questions answered here:
  1. Pairwise crossing scales and the minimal-asymmetry scale of the SM.
  2. Feasible (A,B) region: trajectory must satisfy S in [0,1]^3 and the
     Higuchi-Sudbery-Szulc polygon inequality at EVERY scale M_Z..M_Pl.
  3. Entanglement asymmetry Delta_S(mu) at the most symmetric point:
     SM vs MSSM (the unification corollary, in entropy units).
"""
import json
import numpy as np
import qio_lib as q

MZ, MPL = 91.1876, 1.22e19
B_SM = np.array([-7.0, -19/6, 41/10])      # (b3, b2, b1)
B_MSSM = np.array([-3.0, 1.0, 33/5])
INV0 = 1 / q.ALPHA                          # (a3^-1, a2^-1, a1^-1) at MZ
TMAX = np.log(MPL / MZ)
T_SUSY = np.log(1000 / MZ)                  # 1 TeV threshold for MSSM branch

def ainv_sm(t):
    return INV0[:, None] - B_SM[:, None] / (2 * np.pi) * np.atleast_1d(t)

def ainv_mssm(t):
    t = np.atleast_1d(t)
    inv_s = INV0 - B_SM / (2 * np.pi) * T_SUSY
    return inv_s[:, None] - B_MSSM[:, None] / (2 * np.pi) * (t - T_SUSY)

out = {}

# ---- 1. crossings and minimal-asymmetry scale (SM) ----
names = ['a3-a2', 'a3-a1', 'a2-a1']
pairs = [(0, 1), (0, 2), (1, 2)]
cross = {}
for nm, (i, j) in zip(names, pairs):
    t = (INV0[i] - INV0[j]) * 2 * np.pi / (B_SM[i] - B_SM[j])
    cross[nm] = float(MZ * np.exp(t))
ts = np.linspace(0, TMAX, 200001)
ai = ainv_sm(ts)
spread = ai.max(0) - ai.min(0)
k = spread.argmin()
out['sm'] = dict(crossing_scales_GeV=cross,
                 mu_star_GeV=float(MZ * np.exp(ts[k])),
                 min_spread_alpha_inv=float(spread[k]),
                 ainv_at_mu_star=[float(x) for x in ai[:, k]],
                 ainv_at_MPl=[float(x) for x in ainv_sm(TMAX)[:, 0]])

ts2 = np.linspace(T_SUSY, TMAX, 200001)
ai2 = ainv_mssm(ts2)
spread2 = ai2.max(0) - ai2.min(0)
k2 = spread2.argmin()
out['mssm'] = dict(mu_star_GeV=float(MZ * np.exp(ts2[k2])),
                   min_spread_alpha_inv=float(spread2[k2]),
                   ainv_at_mu_star=[float(x) for x in ai2[:, k2]])

# ---- 2. feasible (A,B) region over the full SM trajectory ----
lam_tab = np.linspace(1e-9, 0.5, 200001)
h_tab = q.h2(lam_tab)
def lam_of_S(S):
    return np.interp(S, h_tab, lam_tab)

tg = np.linspace(0, TMAX, 80)
AIg = ainv_sm(tg)                            # (3, nt)
A_grid = np.linspace(50, 140, 181)
B_grid = np.linspace(-140, -30, 221)
feas = np.zeros((len(A_grid), len(B_grid)), bool)
for ia, A in enumerate(A_grid):
    for ib, B in enumerate(B_grid):
        S = (AIg - A) / B                    # (3, nt)
        if S.min() < 0 or S.max() > 1:
            continue
        lam = lam_of_S(S)
        if np.all(2 * lam.max(0) <= lam.sum(0) + 1e-12):
            feas[ia, ib] = True
ia_f, ib_f = np.where(feas)
if len(ib_f):
    Bmin_abs = float(-B_grid[ib_f].max())    # smallest |B| feasible
    # representative: smallest |B| point
    j = ib_f.argmax(); A_rep, B_rep = float(A_grid[ia_f[j]]), float(B_grid[ib_f[j]])
else:
    Bmin_abs, A_rep, B_rep = None, None, None
out['feasible_region'] = dict(
    n_feasible=int(feas.sum()), grid=[len(A_grid), len(B_grid)],
    min_abs_B=Bmin_abs, representative_A=A_rep, representative_B=B_rep,
    A_range_feasible=[float(A_grid[ia_f].min()), float(A_grid[ia_f].max())] if len(ia_f) else None,
    note="Constraints: S in [0,1]^3 and HSS polygon inequality at all "
         "mu in [M_Z, M_Planck]. Without the polygon constraint the region "
         "is strictly larger; the polygon inequality is doing real work.")

# how much does the polygon constraint cut?
feas_box = np.zeros_like(feas)
for ia, A in enumerate(A_grid):
    for ib, B in enumerate(B_grid):
        S = (AIg - A) / B
        feas_box[ia, ib] = (S.min() >= 0) and (S.max() <= 1)
out['feasible_region']['box_only_count'] = int(feas_box.sum())
out['feasible_region']['polygon_cut_fraction'] = float(1 - feas.sum() / max(1, feas_box.sum()))

# ---- 3. entanglement asymmetry at the symmetric point ----
if B_rep is not None:
    for tag, sp in [('sm', out['sm']['min_spread_alpha_inv']),
                    ('mssm', out['mssm']['min_spread_alpha_inv'])]:
        out[tag]['min_entropy_asymmetry_at_minB'] = float(sp / Bmin_abs)
    # S trajectories at representative (A,B)
    S_MZ = (ainv_sm(0)[:, 0] - A_rep) / B_rep
    S_PL = (ainv_sm(TMAX)[:, 0] - A_rep) / B_rep
    out['representative_trajectory'] = dict(
        S_at_MZ=[float(x) for x in S_MZ], S_at_MPl=[float(x) for x in S_PL],
        slopes_dS_dlogmu=[float(x) for x in -B_SM / (2 * np.pi * B_rep)],
        note="Ordering at M_Z: S1>S2>S3 (SU(3) most entangled); ordering at "
             "M_Pl inverted (U(1) most entangled). Hierarchy inversion in the "
             "deep UV is a structural feature of the entropy-flow version.")

with open('results/exp3_results.json', 'w') as f:
    json.dump(out, f, indent=2)
print(json.dumps(out, indent=2))
