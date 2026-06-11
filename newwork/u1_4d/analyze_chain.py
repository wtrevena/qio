#!/usr/bin/env python3
"""
Analysis of results_chain.json (compact U(1) strip ED; see u1_chain_ed.py, DERIVATION.md).

Tests:
  1. Exponential-family rank test: ln p(n; e2) rows across the coupling grid should lie in
     span{1, T} for a fixed T(n) iff the family is exponential. Curvature measure:
     sigma_3/sigma_2 of the SVD of D[j,n] = ln p_j(n) - ln p_j0(n). Control: exact 2d YM U(1).
  2. Strong-coupling natural parameter: d ln[p(1)/p(0)] / d ln e2 -> -4 (i.e. theta ~ 8 ln e).
  3. Weak-coupling natural parameter: ln[p(1)/p(0)] linear in e2 (theta ~ e2).
  4. Fisher information I(e2) by central differences (triplet runs), entropy derivative,
     and the natural-parameter identity dS/dtheta = -theta * Var(T) - Cov(ln h, T),
     with the globally fitted T and with the two asymptotic statistics T=n^2, T=|n|.
  5. Convergence in hmax and N.

Writes analysis_chain.json and prints a summary. Deterministic (no RNG).
"""
import json, math, os
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
data = json.load(open(os.path.join(HERE, "results_chain.json")))
pts = data["points"]
out = {}


def getp(rec, n):
    lo, hi = rec["n_range"]
    return rec["p_n"][n - lo]


def pvec(rec, ns):
    return np.array([getp(rec, n) for n in ns])


grid = sorted([p for p in pts if p["tag"] == "grid"], key=lambda r: r["e2"])
e2s = np.array([r["e2"] for r in grid])

# ---------- 1. rank test ----------
ns = [-2, -1, 0, 1, 2]
L = np.log(np.array([pvec(r, ns) for r in grid]))  # (J, 5)
D = L - L[0]
sv = np.linalg.svd(D, compute_uv=False)
out["rank_test_full"] = {"singular_values": sv.tolist(),
                         "sigma3_over_sigma2": float(sv[2] / sv[1])}
for name, sel in [("weak_e2<1", e2s < 1.0), ("strong_e2>3", e2s > 3.0)]:
    Dw = L[sel] - L[sel][0]
    svw = np.linalg.svd(Dw, compute_uv=False)
    out[f"rank_test_{name}"] = {"singular_values": svw.tolist(),
                                "sigma3_over_sigma2": float(svw[2] / svw[1])}
# control: exact 2d YM U(1), p_n ∝ exp(-t n^2 / 2), same grid as t
nn = np.arange(-6, 7)
Lc = []
for t in e2s:
    w = np.exp(-0.5 * t * nn ** 2)
    p = w / w.sum()
    Lc.append(np.log(p[(np.abs(nn) <= 2)]))
Lc = np.array(Lc)
svc = np.linalg.svd(Lc - Lc[0], compute_uv=False)
out["rank_test_2dYM_control"] = {"singular_values": svc.tolist(),
                                 "sigma3_over_sigma2": float(svc[2] / max(svc[1], 1e-300))}

# ---------- 2 & 3. natural parameter asymptotics ----------
theta = np.array([-(math.log(getp(r, 1)) - math.log(getp(r, 0))) for r in grid])
A = np.vstack([np.log(e2s[-6:]), np.ones(6)]).T
slope_s, icept_s = np.linalg.lstsq(A, theta[-6:], rcond=None)[0]
out["strong_coupling"] = {
    "dtheta_dln_e2_last6": float(slope_s), "prediction": 4.0,
    "intercept": float(icept_s), "intercept_prediction_ln2": math.log(2.0),
    "p1_over_2c2_at_largest_e2": float(getp(grid[-1], 1) / (2 * (1 / (2 * grid[-1]["e2"] ** 2)) ** 2)),
}


def fit_r2(x, y):
    A = np.vstack([x, np.ones(len(x))]).T
    coef, res, *_ = np.linalg.lstsq(A, y, rcond=None)
    yhat = A @ coef
    ss = 1 - np.sum((y - yhat) ** 2) / np.sum((y - y.mean()) ** 2)
    return float(coef[0]), float(ss)


a_lin, r2_lin = fit_r2(e2s[:6], theta[:6])
a_log, r2_log = fit_r2(np.log(e2s[:6]), theta[:6])
out["weak_coupling"] = {"theta_vs_e2_slope": a_lin, "R2_linear_in_e2": r2_lin,
                        "R2_linear_in_ln_e2": r2_log,
                        "theta_values_first6": theta[:6].tolist(),
                        "e2_first6": e2s[:6].tolist()}

# global T(n) from rank-2 fit: project out constants, leading right-singular vector,
# symmetrized, affinely normalized T(0)=0, T(1)=1
ones = np.ones(len(ns)) / math.sqrt(len(ns))
Dp = D - np.outer(D @ ones, ones)
U2, S2, Vt2 = np.linalg.svd(Dp, full_matrices=False)
Traw = Vt2[0]
Traw = 0.5 * (Traw + Traw[::-1])
T = (Traw - Traw[ns.index(0)]) / (Traw[ns.index(1)] - Traw[ns.index(0)])
out["fitted_T"] = {"n": ns, "T": T.tolist(),
                   "comment": "T(0)=0,T(1)=1; T(2) measures statistic shape: |n| -> 2, n^2 -> 4"}

# ---------- 4. Fisher information and identity (triplets) ----------
fish = [p for p in pts if p["tag"] == "fisher"]
bases = [0.4, 0.7, 1.0, 1.5, 2.5, 4.0, 6.0]
fish_rows = []
for b in bases:
    d = 0.01 * b
    rec0 = min(fish, key=lambda r: abs(r["e2"] - b))
    recp = min(fish, key=lambda r: abs(r["e2"] - (b + d)))
    recm = min(fish, key=lambda r: abs(r["e2"] - (b - d)))
    lo, hi = rec0["n_range"]
    nsf = [n for n in range(lo, hi + 1)
           if getp(rec0, n) > 1e-14 and getp(recp, n) > 1e-14 and getp(recm, n) > 1e-14]
    p0 = pvec(rec0, nsf); pp = pvec(recp, nsf); pm = pvec(recm, nsf)
    dlnp = (np.log(pp) - np.log(pm)) / (2 * d)
    I_e2 = float(np.sum(p0 * dlnp ** 2))
    Sfun = lambda p: float(-(p * np.log(p)).sum())
    dS_de2 = (Sfun(pp / pp.sum()) - Sfun(pm / pm.sum())) / (2 * d)
    sel = [i for i, n in enumerate(nsf) if abs(n) <= 2]
    nsel = [nsf[i] for i in sel]
    Tsel = np.array([T[ns.index(n)] for n in nsel])
    p0s = p0[sel] / p0[sel].sum()
    th0 = -(math.log(getp(rec0, 1)) - math.log(getp(rec0, 0)))
    thp = -(math.log(getp(recp, 1)) - math.log(getp(recp, 0)))
    thm = -(math.log(getp(recm, 1)) - math.log(getp(recm, 0)))
    dth_de2 = (thp - thm) / (2 * d)
    varT = float(np.sum(p0s * Tsel ** 2) - np.sum(p0s * Tsel) ** 2)
    lnh = np.log(p0[sel]) + th0 * Tsel
    covhT = float(np.sum(p0s * lnh * Tsel) - np.sum(p0s * lnh) * np.sum(p0s * Tsel))
    dS_dth = dS_de2 / dth_de2 if dth_de2 != 0 else float("nan")
    pred = -th0 * varT - covhT
    variants = {}
    for vname, Tfun in (("T_n2", lambda n: n * n), ("T_absn", lambda n: abs(n))):
        Tv = np.array([Tfun(n) for n in nsel], dtype=float)
        varTv = float(np.sum(p0s * Tv ** 2) - np.sum(p0s * Tv) ** 2)
        lnhv = np.log(p0[sel]) + th0 * Tv
        covv = float(np.sum(p0s * lnhv * Tv) - np.sum(p0s * lnhv) * np.sum(p0s * Tv))
        predv = -th0 * varTv - covv
        variants[vname] = {"VarT": varTv, "Cov_lnh_T": covv, "pred": predv,
                           "rel_residual": float(abs(dS_dth - predv) / max(abs(dS_dth), 1e-300))}
    fish_rows.append({
        "e2": b, "I_e2": I_e2, "dS_de2": dS_de2, "theta": th0, "dtheta_de2": dth_de2,
        "VarT": varT, "Cov_lnh_T": covhT, "dS_dtheta": dS_dth,
        "identity_pred_-thVar-Cov": pred,
        "identity_rel_residual": float(abs(dS_dth - pred) / max(abs(dS_dth), 1e-300)),
        "naive_e2_identity_ratio": float(dS_de2 / (-b * I_e2)) if I_e2 > 0 else None,
        "theta_over_4": th0 / 4.0,
        "variants": variants,
    })
out["fisher_identity"] = fish_rows

# ---------- 5. convergence ----------
conv = [p for p in pts if p["tag"] == "conv"]
conv_out = {}
for hm in (1, 3):
    rows = []
    for r in [c for c in conv if c["hmax"] == hm and c["N"] == 6]:
        cands = [p for p in pts if p["N"] == 6 and p["hmax"] == 2]
        m = min(cands, key=lambda c: abs(c["e2"] - r["e2"]))
        if abs(m["e2"] - r["e2"]) < 1e-9:
            rows.append({"e2": r["e2"], "dS": abs(r["shannon_pn"] - m["shannon_pn"]),
                         "dp1": abs(getp(r, 1) - getp(m, 1))})
    conv_out[f"hmax{hm}_vs_2_N6"] = rows
for Nv in (4, 7):
    rows = []
    for r in [c for c in conv if c["N"] == Nv]:
        cands = [p for p in pts if p["N"] == 6 and p["hmax"] == 2]
        m = min(cands, key=lambda c: abs(c["e2"] - r["e2"]))
        if abs(m["e2"] - r["e2"]) < 1e-9:
            rows.append({"e2": r["e2"], "dS": abs(r["shannon_pn"] - m["shannon_pn"]),
                         "dp1": abs(getp(r, 1) - getp(m, 1))})
    conv_out[f"N{Nv}_vs_N6_hmax2"] = rows
out["convergence"] = conv_out

# ---------- 6. summary curves ----------
out["curves"] = [{"e2": r["e2"], "p0": getp(r, 0), "p1": getp(r, 1), "p2": getp(r, 2),
                  "shannon": r["shannon_pn"], "ee_heights": r["ee_heights"]} for r in grid]

with open(os.path.join(HERE, "analysis_chain.json"), "w") as f:
    json.dump(out, f, indent=1)

# ---------- print ----------
print("=== exponential-family rank test (sigma3/sigma2; 0 = exact exp family) ===")
print(" full grid   :", out["rank_test_full"]["sigma3_over_sigma2"])
print(" weak  e2<1  :", out["rank_test_weak_e2<1"]["sigma3_over_sigma2"])
print(" strong e2>3 :", out["rank_test_strong_e2>3"]["sigma3_over_sigma2"])
print(" 2dYM control:", out["rank_test_2dYM_control"]["sigma3_over_sigma2"])
print("singular values full:", ["%.3e" % s for s in sv])
print()
print("=== natural parameter ===")
print(" strong: dtheta/dln(e2) =", "%.4f" % out["strong_coupling"]["dtheta_dln_e2_last6"],
      "(pred 4); intercept", "%.4f" % out["strong_coupling"]["intercept"],
      "(pred ln2=%.4f)" % math.log(2))
print(" p(1)/(2c^2) at e2=8:", "%.4f" % out["strong_coupling"]["p1_over_2c2_at_largest_e2"])
print(" weak: theta vs e2 slope %.4f, R2=%.6f (R2 in ln e2: %.6f)" % (a_lin, r2_lin, r2_log))
print(" fitted T:", ["%.3f" % t for t in T], "(|n|->T(2)=2, n^2->T(2)=4)")
print()
print("=== Fisher & identity ===")
for r in fish_rows:
    print(" e2=%.2f I=%.4e dS/de2=%.4e theta=%.3f dS/dth=%.4e pred=%.4e relres=%.3f "
          "naive-e2-ratio=%.3f (theta/4=%.3f)"
          % (r["e2"], r["I_e2"], r["dS_de2"], r["theta"], r["dS_dtheta"],
             r["identity_pred_-thVar-Cov"], r["identity_rel_residual"],
             r["naive_e2_identity_ratio"] or float('nan'), r["theta_over_4"]))
    print("   variants relres: T=n^2 %.3f | T=|n| %.3f" %
          (r["variants"]["T_n2"]["rel_residual"], r["variants"]["T_absn"]["rel_residual"]))
print()
print("=== convergence (max |dS|, max |dp1|) ===")
for k, rows in conv_out.items():
    if rows:
        print(" %s: max dS=%.2e max dp1=%.2e (n=%d pts)" %
              (k, max(r["dS"] for r in rows), max(r["dp1"] for r in rows), len(rows)))
print("\nsaved analysis_chain.json")
