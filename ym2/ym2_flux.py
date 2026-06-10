#!/usr/bin/env python3
"""
ym2_flux.py -- Coupling reconstruction from gauge-invariant entanglement
statistics in 2D Yang-Mills (exactly solvable case).

Implements the formulas fixed in FORMULAS.md (all verified against primary
sources; see that file for citations):

  (F3) p_R(t) = d_R^2 exp(-(t/2) C2(R)) / Z(t),  Z(t) = sum_R d_R^2 e^{-(t/2)C2}
       with t = q^2 * A_sphere   [Donnelly arXiv:1406.7304, eq. (pr)]
  (F4) S(t)  = sum_R p_R [ -ln p_R + 2 ln d_R ]   (one interval, 2 cut points)
       [Donnelly 1406.7304 eq. (YM2entropy); Gromov-Santos 1403.5035 eq. (answ)]
  (C1) S(t)  = ln Z(t) + (t/2) <C2>
  (C3) dS/dt = -(t/4) Var_t(C2)  < 0   (exact monotonicity)
  (C4) Fisher info I(t) = Var_t(C2)/4 ; CRB: Var(t-hat) >= 4/(N Var_t(C2))
  (C5) capacity of entanglement C(t) = (t^2/4) Var_t(C2) = t^2 I(t)
  (C6) MLE for t from flux samples = moment matching on C2 (exponential family)

Groups: SU(2) (j = 0, 1/2, 1, ...; d = 2j+1; C2 = j(j+1))
        compact U(1) (n in Z; d = 1; C2 = n^2; S = Shannon entropy only)

Deterministic: fixed seed SEED. Outputs: results.json, fig_ym2.png, fig_ym2.pdf
(all in the directory of this script).
"""

import json
import os
import time

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.optimize import brentq

SEED = 20260609
HERE = os.path.dirname(os.path.abspath(__file__))

# ----------------------------------------------------------------------
# Group data and the flux distribution p_R(t)
# ----------------------------------------------------------------------

LOG_CUTOFF = 800.0  # keep irreps with (t/2)*C2 - 2 ln d  <  LOG_CUTOFF


def irrep_data(group, t):
    """Labels, dims, Casimirs for all irreps that matter at coupling t.

    Truncation: include all irreps with (t/2)C2 - 2 ln d < LOG_CUTOFF, i.e.
    relative weight > e^-800 ~ 1e-348 -- far below double precision, so the
    truncation error is exactly zero in float64.
    """
    if group == "SU2":
        jmax = 0.5 * (np.sqrt(1.0 + 8.0 * LOG_CUTOFF / t) - 1.0) + 2.0
        j = np.arange(0.0, jmax + 0.5, 0.5)
        d = 2.0 * j + 1.0
        c2 = j * (j + 1.0)
        return j, d, c2
    elif group == "U1":
        nmax = int(np.sqrt(2.0 * LOG_CUTOFF / t)) + 2
        n = np.arange(-nmax, nmax + 1, dtype=float)
        d = np.ones_like(n)
        c2 = n * n
        return n, d, c2
    raise ValueError(group)


def flux_distribution(group, t):
    """Return labels, p_R(t) (normalized), ln Z(t), d_R, C2(R).  (F3)"""
    lab, d, c2 = irrep_data(group, t)
    w = 2.0 * np.log(d) - 0.5 * t * c2  # ln(d^2 e^{-tC2/2})
    wmax = w.max()
    ew = np.exp(w - wmax)
    Z_shift = ew.sum()
    lnZ = wmax + np.log(Z_shift)
    p = ew / Z_shift
    return lab, p, lnZ, d, c2


def moments(group, t):
    """<C2>, Var(C2), <ln d>, Cov(ln d, C2), ln Z under p_R(t)."""
    _, p, lnZ, d, c2 = flux_distribution(group, t)
    m1 = float(p @ c2)
    var = float(p @ (c2 - m1) ** 2)
    lnd = np.log(d)
    mlnd = float(p @ lnd)
    cov = float(p @ ((lnd - mlnd) * (c2 - m1)))
    return m1, var, mlnd, cov, lnZ


def entropies(group, t):
    """Full EE S(t) (one interval), Shannon piece H(t), and cross-checks.

    Returns dict with S via (C1), S via direct (F4) sum, H, Var(C2),
    dS/dt analytic via (C3), Fisher info (C4), capacity (C5).
    """
    m1, var, mlnd, cov, lnZ = moments(group, t)
    S_c1 = lnZ + 0.5 * t * m1  # (C1)
    # direct (F4):
    _, p, _, d, c2 = flux_distribution(group, t)
    with np.errstate(divide="ignore", invalid="ignore"):
        plogp = np.where(p > 0, p * np.log(p), 0.0)
    H = float(-plogp.sum())
    S_direct = H + 2.0 * float(p @ np.log(d))
    return {
        "S": S_c1,
        "S_direct": S_direct,
        "H": H,
        "mean_C2": m1,
        "var_C2": var,
        "mean_ln_d": mlnd,
        "cov_lnd_C2": cov,
        "lnZ": lnZ,
        "dS_dt_analytic": -0.25 * t * var,  # (C3)
        "dH_dt_analytic": -0.25 * t * var + cov,  # (C7)
        "fisher_info": 0.25 * var,  # (C4)
        "capacity": 0.25 * t * t * var,  # (C5)
    }


def mean_c2(group, t):
    _, p, _, _, c2 = flux_distribution(group, t)
    return float(p @ c2)


# ----------------------------------------------------------------------
# (a)+(b): curves on a t-grid, monotonicity, invertibility
# ----------------------------------------------------------------------

def compute_curves(group, t_grid):
    rows = [entropies(group, t) for t in t_grid]
    out = {k: np.array([r[k] for r in rows]) for k in rows[0]}
    out["t"] = np.asarray(t_grid)
    return out


def analyze_monotonicity(curves):
    t = curves["t"]
    S = curves["S"]
    H = curves["H"]
    dS_num = np.gradient(S, t)
    dH_num = np.gradient(H, t)
    dS_an = curves["dS_dt_analytic"]
    dH_an = curves["dH_dt_analytic"]
    # relative agreement of numerical and analytic derivative
    rel = np.abs(dS_num - dS_an) / np.maximum(np.abs(dS_an), 1e-300)
    # interior points only (np.gradient is first-order at the ends)
    rel_interior = rel[2:-2]
    S_strictly_decreasing = bool(np.all(np.diff(S) < 0))
    dS_an_max = float(dS_an.max())  # should be < 0
    # Shannon piece: find any region with dH/dt > 0
    pos = dH_an > 0
    if pos.any():
        i0, i1 = np.argmax(pos), len(pos) - 1 - np.argmax(pos[::-1])
        H_nonmono = {
            "nonmonotonic": True,
            "t_interval_where_dH_dt_positive": [float(t[i0]), float(t[i1])],
            "max_dH_dt": float(dH_an.max()),
            "t_at_max_dH_dt": float(t[int(np.argmax(dH_an))]),
        }
    else:
        H_nonmono = {"nonmonotonic": False, "max_dH_dt": float(dH_an.max())}
    return {
        "S_strictly_decreasing_on_grid": S_strictly_decreasing,
        "max_dS_dt_analytic_on_grid": dS_an_max,
        "max_rel_dev_numeric_vs_analytic_dSdt_interior": float(rel_interior.max()),
        "shannon_piece": H_nonmono,
        "max_abs_S_direct_minus_S_C1": float(
            np.abs(curves["S_direct"] - curves["S"]).max()
        ),
        "dH_dt_numeric_max": float(dH_num.max()),
    }


def entropy_inversion_demo(group, t_true_list, bracket=(5e-3, 60.0)):
    """Invertibility in practice: given exact S, recover t by root finding."""
    out = []
    for t_true in t_true_list:
        S_val = entropies(group, t_true)["S"]
        f = lambda t: entropies(group, t)["S"] - S_val
        t_rec = brentq(f, bracket[0], bracket[1], xtol=1e-12, rtol=1e-14)
        out.append(
            {
                "t_true": float(t_true),
                "S": float(S_val),
                "t_recovered": float(t_rec),
                "abs_error": float(abs(t_rec - t_true)),
            }
        )
    return out


# ----------------------------------------------------------------------
# (c): statistical reconstruction demo (MLE + Cramer-Rao)
# ----------------------------------------------------------------------

def mle_from_mean(group, mbar, bracket=(1e-3, 200.0)):
    """Solve <C2>_t = mbar for t (C6). Returns clamped endpoint if needed."""
    lo, hi = bracket
    f = lambda t: mean_c2(group, t) - mbar
    flo, fhi = f(lo), f(hi)
    if flo <= 0:  # mbar >= <C2>(lo): sample looks like t below bracket
        return lo, True
    if fhi >= 0:  # mbar <= <C2>(hi): sample looks like t above bracket
        return hi, True
    return brentq(f, lo, hi, xtol=1e-10, rtol=1e-12), False


def reconstruction_demo(group, t_star, N_list, M, rng):
    """Draw M batches of N flux samples from p_R(t*), MLE-reconstruct t."""
    _, p, _, _, c2 = flux_distribution(group, t_star)
    # drop irreps with p < 1e-17 to keep multinomial small (error << 1/sqrt(N))
    keep = p > 1e-17
    p_k, c2_k = p[keep], c2[keep]
    p_k = p_k / p_k.sum()
    I_t = entropies(group, t_star)["fisher_info"]
    crb_var_1 = 1.0 / I_t  # per-sample CRB on Var
    results = []
    for N in N_list:
        counts = rng.multinomial(N, p_k, size=M)  # (M, K)
        mbars = counts @ c2_k / N
        t_hats = np.empty(M)
        n_clamped = 0
        for m in range(M):
            t_hats[m], clamped = mle_from_mean(group, mbars[m])
            n_clamped += clamped
        bias = float(t_hats.mean() - t_star)
        var = float(t_hats.var(ddof=1))
        rmse = float(np.sqrt(np.mean((t_hats - t_star) ** 2)))
        crb_sd = float(np.sqrt(crb_var_1 / N))
        results.append(
            {
                "N": int(N),
                "bias": bias,
                "sd": float(np.sqrt(var)),
                "rmse": rmse,
                "crb_sd": crb_sd,
                "rmse_over_crb": rmse / crb_sd,
                "var_over_crb": var / (crb_var_1 / N),
                "n_clamped": int(n_clamped),
            }
        )
    return {
        "t_star": float(t_star),
        "fisher_info": float(I_t),
        "M_trials": int(M),
        "by_N": results,
    }


# ----------------------------------------------------------------------
# (d): figure
# ----------------------------------------------------------------------

def make_figure(curves, recon, fname_base):
    fig, axes = plt.subplots(1, 3, figsize=(14.0, 4.2))

    # --- Panel 1: flux distributions p_R(t) ---
    ax = axes[0]
    t_show = [0.5, 2.0, 8.0]
    colors = ["#1f77b4", "#d62728", "#2ca02c"]
    for t, c in zip(t_show, colors):
        j, p, _, _, _ = flux_distribution("SU2", t)
        sel = p > 1e-6
        ax.plot(
            j[sel], p[sel], "o-", ms=4, lw=1.2, color=c,
            label=rf"SU(2), $t={t}$",
        )
        n, pu, _, _, _ = flux_distribution("U1", t)
        sel = (pu > 1e-6) & (n >= 0)
        ax.plot(
            n[sel], pu[sel], "s--", ms=3.5, lw=1.0, color=c, alpha=0.45,
            label=rf"U(1), $t={t}$",
        )
    ax.set_yscale("log")
    ax.set_ylim(1e-6, 1.5)
    ax.set_xlim(-0.2, 8)
    ax.set_xlabel(r"irrep label  ($j$ for SU(2),  $n\geq 0$ for U(1))")
    ax.set_ylabel(r"$p_R(t)$")
    ax.set_title(r"(a) flux distribution  $p_R \propto d_R^2\, e^{-t C_2(R)/2}$")
    ax.legend(fontsize=7, ncol=2, frameon=False)

    # --- Panel 2: S(t) and Shannon piece ---
    ax = axes[1]
    cs, cu = curves["SU2"], curves["U1"]
    ax.plot(cs["t"], cs["S"], "-", color="#1f77b4", lw=2,
            label=r"SU(2): full $S(t)$")
    ax.plot(cs["t"], cs["H"], "--", color="#1f77b4", lw=1.3,
            label=r"SU(2): Shannon piece $H(t)$")
    ax.plot(cs["t"], cs["S"] - cs["H"], ":", color="#1f77b4", lw=1.1,
            label=r"SU(2): $2\langle\ln d_R\rangle$")
    ax.plot(cu["t"], cu["S"], "-", color="#d62728", lw=2,
            label=r"U(1): $S(t)=H(t)$")
    ax.set_xscale("log")
    ax.set_xlabel(r"$t = g^2 A$")
    ax.set_ylabel(r"entropy (nats)")
    ax.set_title(r"(b) $S(t)$;   $dS/dt=-\frac{t}{4}\mathrm{Var}(C_2)<0$")
    ax.legend(fontsize=8, frameon=False)
    ax.set_ylim(bottom=-0.1)

    # --- Panel 3: reconstruction error vs N against CRB ---
    ax = axes[2]
    show = [("SU2", 1.0, "#1f77b4", "o"), ("U1", 1.0, "#d62728", "s"),
            ("SU2", 4.0, "#2ca02c", "^")]
    for grp, tst, c, mk in show:
        rec = next(r for r in recon[grp] if r["t_star"] == tst)
        N = np.array([row["N"] for row in rec["by_N"]])
        rmse = np.array([row["rmse"] for row in rec["by_N"]])
        crb = np.array([row["crb_sd"] for row in rec["by_N"]])
        ax.loglog(N, rmse, mk, color=c, ms=6,
                  label=rf"{'SU(2)' if grp=='SU2' else 'U(1)'}, $t^*={tst}$")
        ax.loglog(N, crb, "-", color=c, lw=1.2, alpha=0.7)
    ax.loglog([], [], "-", color="0.4", label="Cramér–Rao bound")
    ax.set_xlabel(r"$N$ flux samples")
    ax.set_ylabel(r"RMSE of $\hat{t}_{\rm MLE}$")
    ax.set_title(r"(c) reconstruction error vs $N$ (MLE), CRB lines")
    ax.legend(fontsize=8, frameon=False)

    fig.tight_layout()
    fig.savefig(fname_base + ".png", dpi=200)
    fig.savefig(fname_base + ".pdf")
    plt.close(fig)


# ----------------------------------------------------------------------
# main
# ----------------------------------------------------------------------

def main():
    t0 = time.time()
    rng = np.random.default_rng(SEED)

    t_grid = np.geomspace(0.05, 20.0, 400)
    groups = ["SU2", "U1"]

    print("== (a)+(b) curves, monotonicity, invertibility ==")
    curves, mono, inv_demo = {}, {}, {}
    for g in groups:
        curves[g] = compute_curves(g, t_grid)
        mono[g] = analyze_monotonicity(curves[g])
        inv_demo[g] = entropy_inversion_demo(g, [0.3, 0.7, 1.5, 3.0, 6.0, 12.0])
        print(f"  {g}: S strictly decreasing on grid: "
              f"{mono[g]['S_strictly_decreasing_on_grid']}, "
              f"max dS/dt = {mono[g]['max_dS_dt_analytic_on_grid']:.3e}, "
              f"max|S_direct-S_C1| = {mono[g]['max_abs_S_direct_minus_S_C1']:.2e}")
        print(f"      Shannon piece: {mono[g]['shannon_piece']}")
        worst = max(r["abs_error"] for r in inv_demo[g])
        print(f"      entropy-inversion worst |t_rec - t_true| = {worst:.2e}")

    print("== (c) statistical reconstruction demo ==")
    t_stars = [0.5, 1.0, 2.0, 4.0]
    N_list = [30, 100, 300, 1000, 3000, 10000, 30000]
    M = 400
    recon = {}
    for g in groups:
        recon[g] = []
        for ts in t_stars:
            r = reconstruction_demo(g, ts, N_list, M, rng)
            recon[g].append(r)
            head = {row["N"]: row for row in r["by_N"]}
            print(f"  {g} t*={ts}: rmse(N=1e3)={head[1000]['rmse']:.4f} "
                  f"(CRB {head[1000]['crb_sd']:.4f}, ratio "
                  f"{head[1000]['rmse_over_crb']:.3f}); "
                  f"rmse(N=1e4)={head[10000]['rmse']:.4f} "
                  f"(CRB {head[10000]['crb_sd']:.4f}, ratio "
                  f"{head[10000]['rmse_over_crb']:.3f})")

    print("== (d) figure ==")
    make_figure(curves, recon, os.path.join(HERE, "fig_ym2"))

    print("== (e) results.json ==")
    # coarse subsample of curves for the JSON (every 5th point: 80 points)
    sub = slice(0, len(t_grid), 5)
    curves_json = {}
    for g in groups:
        c = curves[g]
        curves_json[g] = {
            k: [float(x) for x in c[k][sub]]
            for k in ["t", "S", "H", "mean_C2", "var_C2",
                      "dS_dt_analytic", "fisher_info", "capacity"]
        }
    results = {
        "meta": {
            "seed": SEED,
            "date": "2026-06-09",
            "t_definition": "t = g^2 * A_total (sphere/HH state), weight e^{-(t/2) C2(R)}",
            "formulas": "see FORMULAS.md (F3),(F4),(C1)-(C7) with citations",
            "groups": {
                "SU2": "j=0,1/2,1,...; d=2j+1; C2=j(j+1)",
                "U1": "n in Z; d=1; C2=n^2",
            },
            "runtime_seconds": None,  # filled below
        },
        "curves": curves_json,
        "monotonicity": mono,
        "entropy_inversion_demo": inv_demo,
        "reconstruction": recon,
    }
    results["meta"]["runtime_seconds"] = round(time.time() - t0, 1)
    with open(os.path.join(HERE, "results.json"), "w") as f:
        json.dump(results, f, indent=1)
    print(f"done in {results['meta']['runtime_seconds']} s")


if __name__ == "__main__":
    main()
