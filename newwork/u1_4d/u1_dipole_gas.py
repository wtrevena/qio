#!/usr/bin/env python3
"""
d = 3+1 compact U(1), analytic flux-sector models at the two ends of the coupling axis
(see DERIVATION.md sections B and C). Pure numpy, deterministic, no RNG.

Module 1 (electric/strong-coupling limit): leading-order strong-coupling ground state.
  Straddling plaquettes are independent 3-state systems {0, +dipole, -dipole} with
  p ∝ exp(-theta*T), T in {0,1,1}, theta(e2) = -ln c^2, c = 1/(4 e^4) (4-link plaquette,
  excitation energy 2 e^2, vertex -1/(2 e^2)).  Exact finite-theta verification of:
    I(theta) = Var(T),  dS/dtheta = -theta * I(theta)   (exponential family, h == 1)
  and of the FAILURE of the naive e2-form: dS/de2 = -theta(e2)/4 * (e2 * I(e2)) etc.
  Information is extensive: N_str = 2 * N_cut independent boundary plaquettes.

Module 2 (Coulomb/weak-coupling limit): discrete-Gaussian zero mode, the Donnelly-Wall
  (arXiv:1506.05792, eq. 36) electric flux sector distribution
    p(n) ∝ exp(-(kappa * e2 / 2) n^2),  kappa = geometric (e2-independent) kernel factor.
  Exact verification of: exponential family with natural parameter theta2 = kappa*e2/2,
  sufficient statistic n^2; dS/dtheta2 = -theta2 * Var(n^2); Gaussian asymptotics
  I(e2) -> 1/(2 e2^2) per mode as e2 -> 0 (so total I ≈ N_modes/(2 e2^2) diverges with
  the number of cut links ~ Area/a^2).

Output: results_dipole.json
"""
import json, math, os
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
out = {"seed": 20260610, "note": "deterministic, no RNG"}


# ---------- Module 1: strong-coupling dipole gas ----------
def dipole_stats(theta):
    """3-state exponential family p ∝ (1, e^-theta, e^-theta), T = (0,1,1)."""
    w = np.array([1.0, math.exp(-theta), math.exp(-theta)])
    Z = w.sum()
    p = w / Z
    T = np.array([0.0, 1.0, 1.0])
    ET = (p * T).sum()
    varT = (p * T * T).sum() - ET ** 2
    S = -(p * np.log(p)).sum()
    return p, S, varT


def fisher_theta_fd(theta, d=1e-6):
    """Fisher info in theta by central differences of ln p (per straddling plaquette)."""
    pp, _, _ = dipole_stats(theta + d)
    pm, _, _ = dipole_stats(theta - d)
    p0, _, _ = dipole_stats(theta)
    dlnp = (np.log(pp) - np.log(pm)) / (2 * d)
    return float((p0 * dlnp ** 2).sum())


rows = []
for e2 in [1.5, 2.0, 3.0, 5.0, 8.0, 12.0]:
    c = 1.0 / (4.0 * e2 ** 2)          # c = 1/(4 e^4), e^4 = (e2)^2
    theta = -math.log(c * c)            # = ln(16 e^8) = ln 16 + 4 ln e2
    p, S, varT = dipole_stats(theta)
    I_th = fisher_theta_fd(theta)
    d = 1e-6
    _, Sp, _ = dipole_stats(theta + d)
    _, Sm, _ = dipole_stats(theta - d)
    dS_dth = (Sp - Sm) / (2 * d)
    # identity residual (per straddling plaquette; extensive quantities = N_str * these)
    res = abs(dS_dth + theta * I_th) / abs(dS_dth)
    # naive e2 identity: dS/de2 vs -e2*I(e2); dtheta/de2 = 4/e2
    dth_de2 = 4.0 / e2
    dS_de2 = dS_dth * dth_de2
    I_e2 = (dth_de2 ** 2) * I_th
    naive_ratio = dS_de2 / (-e2 * I_e2)        # prediction: theta/4
    rows.append({
        "e2": e2, "theta": theta, "p_dipole": float(p[1]), "S_per_plaquette": float(S),
        "I_theta": I_th, "VarT": float(varT),
        "identity_dSdth_eq_minus_theta_I_relres": float(res),
        "I_e2_per_plaquette": float(I_e2), "dS_de2": float(dS_de2),
        "naive_e2_ratio": float(naive_ratio), "theta_over_4": theta / 4.0,
    })
out["strong_coupling_dipole_gas"] = rows
out["strong_coupling_notes"] = {
    "N_str": "2 * N_cut straddling plaquettes; all totals are N_str * per-plaquette values",
    "extensivity": "I_total = N_str * I_per_plaquette ∝ Area/a^2 -> information scales with cut area (unlike d=2)",
}

# ---------- Module 2: Coulomb-phase discrete-Gaussian zero mode ----------
rows2 = []
nn = np.arange(-200, 201)
for e2 in [0.05, 0.1, 0.2, 0.4, 0.8, 1.0]:
    kappa = 1.0  # geometric factor, e2-independent in the Coulomb phase
    th2 = 0.5 * kappa * e2
    w = np.exp(-th2 * nn ** 2)
    p = w / w.sum()
    S = float(-(p[p > 0] * np.log(p[p > 0])).sum())
    T = (nn ** 2).astype(float)
    varT = float((p * T * T).sum() - ((p * T).sum()) ** 2)
    d = 1e-6 * e2
    wp = np.exp(-0.5 * kappa * (e2 + d) * nn ** 2); pp = wp / wp.sum()
    wm = np.exp(-0.5 * kappa * (e2 - d) * nn ** 2); pm = wm / wm.sum()
    msk = (p > 1e-300) & (pp > 1e-300) & (pm > 1e-300)
    dlnp = (np.log(pp[msk]) - np.log(pm[msk])) / (2 * d)
    I_e2 = float((p[msk] * dlnp ** 2).sum())
    Sp = float(-(pp[msk] * np.log(pp[msk])).sum())
    Sm = float(-(pm[msk] * np.log(pm[msk])).sum())
    dS_de2 = (Sp - Sm) / (2 * d)
    res = abs(dS_de2 + e2 * I_e2) / abs(dS_de2)   # natural parameter ∝ e2 -> identity in e2
    rows2.append({
        "e2": e2, "theta2": th2, "S": S, "I_e2": I_e2,
        "gaussian_limit_1_over_2e4": 1.0 / (2 * e2 ** 2),
        "I_over_gaussian_limit": I_e2 * 2 * e2 ** 2,
        "identity_dSde2_eq_minus_e2_I_relres": float(res),
        "VarT_n2": varT,
    })
out["coulomb_zero_mode"] = rows2
out["coulomb_notes"] = {
    "model": "Donnelly-Wall 1506.05792 eq.(36): p(n) ∝ exp(-(q_B^2 Vol(B)/2) n^2); kappa stands for q_B^2 Vol(B)/e2-scaling",
    "identity": "natural parameter is ∝ e2, so dS/de2 = -e2*I(e2) holds here (the direct 2dYM analog)",
    "divergence": "full cut: one such mode per independent boundary link mode; I_total ≈ N_modes/(2 e2^2), N_modes ∝ Area/a^2 -> divergent as a->0",
}

with open(os.path.join(HERE, "results_dipole.json"), "w") as f:
    json.dump(out, f, indent=1)

print("=== strong-coupling dipole gas (per straddling plaquette) ===")
for r in rows:
    print(" e2=%5.1f theta=%6.3f p_dip=%.3e S=%.3e I_th=%.3e relres(dS/dth=-th*I)=%.2e "
          "naive_ratio=%.3f (theta/4=%.3f)"
          % (r["e2"], r["theta"], r["p_dipole"], r["S_per_plaquette"], r["I_theta"],
             r["identity_dSdth_eq_minus_theta_I_relres"], r["naive_e2_ratio"], r["theta_over_4"]))
print()
print("=== Coulomb-phase zero mode (discrete Gaussian, kappa=1) ===")
for r in rows2:
    print(" e2=%5.2f S=%7.4f I(e2)=%.4e  I/(1/2e4)=%.4f  relres(dS/de2=-e2*I)=%.2e"
          % (r["e2"], r["S"], r["I_e2"], r["I_over_gaussian_limit"],
             r["identity_dSde2_eq_minus_e2_I_relres"]))
print("\nsaved results_dipole.json")
