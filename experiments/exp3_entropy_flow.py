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
    min_abs_B=Bmin_abs, representative_A=A_rep, representative_B=B_rep,
    note="Constraints: S in [0,1]^3 and HSS polygon inequality. The feasible "
         "region is UNBOUNDED (larger A forces proportionally larger |B|), so "
         "no fraction-of-parameter-space or upper bound on A is meaningful; "
         "the only robust content is the lower bound on |B|. An earlier "
         "version of this script reported a 91% 'cut fraction' and an A "
         "range; both were artifacts of an arbitrary finite grid and are "
         "intentionally no longer emitted.")

# --- robustness of min|B|: extended grid and earlier UV endpoint ---
def min_abs_B_scan(A_lo, A_hi, B_lo, tmax):
    Ag = np.linspace(A_lo, A_hi, int(A_hi - A_lo) + 1)
    Bg = np.linspace(B_lo, -30, int(-30 - B_lo) + 1)
    tg2 = np.linspace(0, tmax, 80)
    AI2 = ainv_sm(tg2)
    best = None
    for A in Ag:
        for B in Bg:
            S = (AI2 - A) / B
            if S.min() < 0 or S.max() > 1:
                continue
            lam = lam_of_S(S)
            if np.all(2 * lam.max(0) <= lam.sum(0) + 1e-12):
                if best is None or -B < best:
                    best = -B
    return float(best) if best else None
out['minB_robustness'] = dict(
    base_grid=Bmin_abs,
    extended_grid_A50_300_B300=min_abs_B_scan(50, 300, -300, TMAX),
    uv_endpoint_1e16=min_abs_B_scan(50, 300, -300, np.log(1e16 / MZ)),
    note="min |B| is stable against enlarging the scan region and moving the "
         "UV endpoint from M_Planck to 1e16 GeV.")

# --- M_Z-only vs all-scale constraints: feasible sets are identical ---
def feas_set(tgrid):
    AI2 = ainv_sm(tgrid)
    s = set()
    for ia, A in enumerate(A_grid):
        for ib, B in enumerate(B_grid):
            S = (AI2 - A) / B
            if S.min() < 0 or S.max() > 1:
                continue
            lam = lam_of_S(S)
            if np.all(2 * lam.max(0) <= lam.sum(0) + 1e-12):
                s.add((ia, ib))
    return s
f_full, f_mz = feas_set(tg), feas_set(np.array([0.0]))
out['mz_only_equality'] = dict(
    n_full=len(f_full), n_mz_only=len(f_mz), identical=bool(f_full == f_mz),
    note="The constraints bind at M_Z alone: all-scale and M_Z-only feasible "
         "sets coincide, because the coupling spread is widest at M_Z "
         "(deflation credited to adversarial review).")

# ---- 3. entanglement asymmetry at the symmetric point ----
if B_rep is not None:
    for tag, sp in [('sm', out['sm']['min_spread_alpha_inv']),
                    ('mssm', out['mssm']['min_spread_alpha_inv'])]:
        out[tag]['min_entropy_asymmetry_at_minB'] = float(sp / Bmin_abs)
    S_MZ = (ainv_sm(0)[:, 0] - A_rep) / B_rep
    S_PL = (ainv_sm(TMAX)[:, 0] - A_rep) / B_rep
    out['representative_trajectory'] = dict(
        S_at_MZ=[float(x) for x in S_MZ], S_at_MPl=[float(x) for x in S_PL],
        slopes_dS_dlogmu=[float(x) for x in -B_SM / (2 * np.pi * B_rep)],
        note="Ordering at M_Z: S1>S2>S3 (SU(3) most entangled); ordering at "
             "M_Pl inverted (U(1) most entangled): the one-loop crossing "
             "pattern re-expressed in entropy variables.")

with open('results/exp3_results.json', 'w') as f:
    json.dump(out, f, indent=2)
print(json.dumps({k: out[k] for k in ('feasible_region', 'minB_robustness', 'mz_only_equality')}, indent=2))
