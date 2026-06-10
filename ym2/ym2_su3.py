#!/usr/bin/env python3
"""
ym2_su3.py -- SU(3) extension + n-interval analysis for the YM2 coupling-
reconstruction project (companion to ym2_flux.py; this file is NEW and does
not modify any verified base artifact).

SU(3) group data (convention verified against standard sources on 2026-06-09;
see su3_results.json meta and paper3/draft.md Sec. 2):

  irreps R = (p,q), p,q = 0,1,2,...   (Dynkin labels)
  dim(p,q) = (p+1)(q+1)(p+q+2)/2
  C2(p,q)  = (p^2 + q^2 + p q + 3p + 3q)/3

  Normalization check (asserted at runtime): C2(1,0) = 4/3 = (N^2-1)/(2N),
  C2(1,1) = 3 = N.  This is the convention with Tr(T_a T_b) = delta_ab/2 in
  the fundamental -- the same family as C2(j) = j(j+1) for SU(2) (whose
  fundamental j=1/2 gives 3/4 = (N^2-1)/(2N)), i.e. Donnelly's [1406.7304]
  convention with weight e^{-(t/2) C2}, t = g^2 A_sphere.

Formulas implemented (FORMULAS.md (F3),(F4),(C1)-(C7), verified against the
arXiv LaTeX sources):
  (F3) p_R(t) = d_R^2 e^{-(t/2)C2(R)} / Z(t)
  (F4) S_n(t) = -sum p ln p + 2n sum p ln d   (n disjoint intervals;
       Donnelly 1406.7304 eq. (YM2entropy), verbatim from the LaTeX source:
       "S = \\sum_R p(R) (- \\log p(R) + 2n \\log \\dim R)")
  (C3) dS_1/dt = -(t/4) Var(C2)
  (C4) I(t) = Var(C2)/4 ; CRB Var(t-hat) >= 4/(N Var(C2))
  (C5) capacity C(t) = (t^2/4) Var(C2);  C(t) -> dim(G)/2 as t -> 0
  NEW (D1) dS_n/dt = -(t/4) Var(C2) - (n-1) Cov(ln d, C2)
       [from S_n = S_1 + 2(n-1)<ln d> and d<f>/dt = -(1/2) Cov(f, C2)]
  NEW (D2) n-interval Fisher information: the reduced state on n intervals is
       block-diagonal in a SINGLE shared R (the HH state on the circle is a
       class function of one holonomy; the flux through every cut point is
       the same global R).  Hence the joint flux measurement at all 2n cut
       points returns (R, R, ..., R): perfectly correlated, I_n(t) = I_1(t).
       More cuts give NO additional information about t.  Donnelly states
       this in words for the abelian case (1406.7304 source, canonical
       section: "the entropy is independent of the number of intervals
       traced out ... Having access to an additional interval therefore does
       not change the amount of information one can acquire about the
       state.")

Determinism: every random component uses its own stream
np.random.default_rng([SEED, *component_index]), so running the whole script
(`python3 ym2_su3.py`) and running it in stages (`stage1`, `stage2:<t*list>`,
`stage3`, then `merge`) produce bit-identical numbers.

Outputs (all NEW files, in this directory):
  su3_results.json, fig_su3.png, fig_su3.pdf  (+ temporary su3_stage*.json
  when staged; removed by `merge`).
"""

import json
import os
import sys
import time

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.optimize import brentq

SEED = 20260609
HERE = os.path.dirname(os.path.abspath(__file__))
LOG_CUTOFF = 800.0   # curves: truncation error exactly 0 in float64
MLE_CUTOFF = 120.0   # MLE inner loop: relative truncation < 1e-50 (see note)
SLACK = 60.0         # covers the 2 ln d growth in the truncation bound

# ----------------------------------------------------------------------
# Group data
# ----------------------------------------------------------------------

def su3_dim(p, q):
    return (p + 1.0) * (q + 1.0) * (p + q + 2.0) / 2.0


def su3_c2(p, q):
    return (p * p + q * q + p * q + 3.0 * p + 3.0 * q) / 3.0


# runtime assertions of the convention (see docstring)
assert su3_dim(0, 0) == 1 and su3_c2(0, 0) == 0.0
assert su3_dim(1, 0) == 3 and abs(su3_c2(1, 0) - 4.0 / 3.0) < 1e-15
assert su3_dim(0, 1) == 3 and abs(su3_c2(0, 1) - 4.0 / 3.0) < 1e-15
assert su3_dim(1, 1) == 8 and abs(su3_c2(1, 1) - 3.0) < 1e-15
assert su3_dim(2, 0) == 6 and abs(su3_c2(2, 0) - 10.0 / 3.0) < 1e-15
assert su3_dim(3, 0) == 10 and abs(su3_c2(3, 0) - 6.0) < 1e-15

DIM_G = {"SU2": 3, "U1": 1, "SU3": 8}


def irrep_data(group, t, cutoff=LOG_CUTOFF):
    """dims and Casimirs of all irreps with relative weight > e^-cutoff."""
    if group == "SU2":
        jmax = 0.5 * (np.sqrt(1.0 + 8.0 * cutoff / t) - 1.0) + 2.0
        j = np.arange(0.0, jmax + 0.5, 0.5)
        return 2.0 * j + 1.0, j * (j + 1.0)
    if group == "U1":
        nmax = int(np.sqrt(2.0 * cutoff / t)) + 2
        n = np.arange(-nmax, nmax + 1, dtype=float)
        return np.ones_like(n), n * n
    if group == "SU3":
        # C2 >= max(p,q)^2/3, so (t/2)C2 > cutoff+SLACK once
        # max(p,q) > sqrt(6(cutoff+SLACK)/t); SLACK covers 2 ln d.
        pmax = int(np.sqrt(6.0 * (cutoff + SLACK) / t)) + 2
        p, q = np.meshgrid(np.arange(pmax + 1, dtype=float),
                           np.arange(pmax + 1, dtype=float), indexing="ij")
        p, q = p.ravel(), q.ravel()
        return su3_dim(p, q), su3_c2(p, q)
    raise ValueError(group)


# ----------------------------------------------------------------------
# Flux distribution, moments, entropies (structure mirrors ym2_flux.py)
# ----------------------------------------------------------------------

def flux_distribution(group, t):
    d, c2 = irrep_data(group, t)
    w = 2.0 * np.log(d) - 0.5 * t * c2
    wmax = w.max()
    ew = np.exp(w - wmax)
    Zs = ew.sum()
    return ew / Zs, wmax + np.log(Zs), d, c2


def entropies(group, t, n_intervals=1):
    """S_n(t), H(t), moments; identities (C1)-(C5),(D1)."""
    p, lnZ, d, c2 = flux_distribution(group, t)
    m1 = float(p @ c2)
    var = float(p @ (c2 - m1) ** 2)
    lnd = np.log(d)
    mlnd = float(p @ lnd)
    cov = float(p @ ((lnd - mlnd) * (c2 - m1)))
    with np.errstate(divide="ignore", invalid="ignore"):
        plogp = np.where(p > 0, p * np.log(p), 0.0)
    H = float(-plogp.sum())
    n = n_intervals
    return {
        "S": lnZ + 0.5 * t * m1 + 2.0 * (n - 1.0) * mlnd,  # (C1)+2(n-1)<ln d>
        "S_direct": H + 2.0 * n * mlnd,                    # (F4)
        "H": H,
        "mean_C2": m1, "var_C2": var, "mean_ln_d": mlnd, "cov_lnd_C2": cov,
        "lnZ": lnZ,
        "dS_dt_analytic": -0.25 * t * var - (n - 1.0) * cov,  # (C3)/(D1)
        "dH_dt_analytic": -0.25 * t * var + cov,              # (C7)
        "fisher_info": 0.25 * var,                            # (C4)
        "capacity": 0.25 * t * t * var,                       # (C5)
    }


# --- fast <C2>(t) for the MLE loop -----------------------------------
# Tier arrays built at threshold t0 are valid for all t >= t0 (weights only
# shrink with t).  MLE_CUTOFF = 120 keeps relative weights > e^-120 ~ 1e-52:
# the truncation bias on <C2> is < 1e-48, i.e. ~46 orders of magnitude below
# the Monte-Carlo noise of the demo; the curves/identities use the exact
# LOG_CUTOFF = 800 arrays.
_TIERS = [0.01, 0.1, 0.5, 2.0, 8.0]
_CACHE = {}


def mean_c2_fast(group, t):
    t0 = max([x for x in _TIERS if x <= t], default=_TIERS[0])
    key = (group, t0)
    if key not in _CACHE:
        _CACHE[key] = irrep_data(group, t0, cutoff=MLE_CUTOFF)
    d, c2 = _CACHE[key]
    w = 2.0 * np.log(d) - 0.5 * t * c2
    w -= w.max()
    ew = np.exp(w)
    return float(ew @ c2 / ew.sum())


# bracketing grid per group: <C2> is strictly decreasing in t, so a coarse
# monotone table gives a tight bracket and brentq polishes inside it.
_GRID = {}
T_LO, T_HI = 0.02, 120.0


def _grid(group):
    if group not in _GRID:
        tn = np.geomspace(T_LO, T_HI, 241)
        mn = np.array([mean_c2_fast(group, t) for t in tn])
        assert np.all(np.diff(mn) < 0), "grid <C2> not strictly decreasing"
        _GRID[group] = (tn, mn)
    return _GRID[group]


def mle_from_mean(group, mbar):
    """Solve <C2>_t = mbar (C6).  Returns (t_hat, clamped)."""
    tn, mn = _grid(group)
    if mbar >= mn[0]:
        return T_LO, True    # sample looks like t below bracket
    if mbar <= mn[-1]:
        return T_HI, True    # sample looks like t above bracket
    i = int(np.searchsorted(-mn, -mbar))          # mn[i-1] > mbar >= mn[i]
    lo, hi = tn[max(i - 1, 0)], tn[min(i + 1, len(tn) - 1)]
    f = lambda t: mean_c2_fast(group, t) - mbar
    return brentq(f, lo, hi, xtol=1e-10, rtol=1e-12), False


# ----------------------------------------------------------------------
# Monotonicity / inversion (as in base script)
# ----------------------------------------------------------------------

def compute_curves(group, t_grid):
    rows = [entropies(group, t) for t in t_grid]
    out = {k: np.array([r[k] for r in rows]) for k in rows[0]}
    out["t"] = np.asarray(t_grid)
    return out


def analyze_monotonicity(curves):
    t, S = curves["t"], curves["S"]
    dS_num = np.gradient(S, t)
    dS_an = curves["dS_dt_analytic"]
    dH_an = curves["dH_dt_analytic"]
    rel = np.abs(dS_num - dS_an) / np.maximum(np.abs(dS_an), 1e-300)
    pos = dH_an > 0
    shannon = ({"nonmonotonic": True,
                "max_dH_dt": float(dH_an.max()),
                "t_at_max_dH_dt": float(t[int(np.argmax(dH_an))])}
               if pos.any() else
               {"nonmonotonic": False, "max_dH_dt": float(dH_an.max())})
    return {
        "S_strictly_decreasing_on_grid": bool(np.all(np.diff(S) < 0)),
        "max_dS_dt_analytic_on_grid": float(dS_an.max()),
        "max_rel_dev_numeric_vs_analytic_dSdt_interior": float(rel[2:-2].max()),
        "shannon_piece": shannon,
        "max_abs_S_direct_minus_S_C1": float(
            np.abs(curves["S_direct"] - curves["S"]).max()),
        "min_cov_lnd_C2_on_grid": float(curves["cov_lnd_C2"].min()),
    }


def entropy_inversion_demo(group, t_true_list, bracket=(5e-3, 60.0)):
    out = []
    for t_true in t_true_list:
        S_val = entropies(group, t_true)["S"]
        f = lambda t: entropies(group, t)["S"] - S_val
        t_rec = brentq(f, bracket[0], bracket[1], xtol=1e-12, rtol=1e-14)
        out.append({"t_true": float(t_true), "S": float(S_val),
                    "t_recovered": float(t_rec),
                    "abs_error": float(abs(t_rec - t_true))})
    return out


# ----------------------------------------------------------------------
# MLE reconstruction (C6)
# ----------------------------------------------------------------------

def reconstruction_demo(group, t_star, N_list, M, rng):
    p, _, d, c2 = flux_distribution(group, t_star)
    keep = p > 1e-17
    p_k, c2_k = p[keep], c2[keep]
    p_k = p_k / p_k.sum()
    I_t = entropies(group, t_star)["fisher_info"]
    crb_var_1 = 1.0 / I_t
    results = []
    for N in N_list:
        counts = rng.multinomial(N, p_k, size=M)
        mbars = counts @ c2_k / N
        t_hats = np.empty(M)
        n_clamped = 0
        for m in range(M):
            t_hats[m], clamped = mle_from_mean(group, mbars[m])
            n_clamped += clamped
        var = float(t_hats.var(ddof=1))
        rmse = float(np.sqrt(np.mean((t_hats - t_star) ** 2)))
        crb_sd = float(np.sqrt(crb_var_1 / N))
        results.append({
            "N": int(N),
            "bias": float(t_hats.mean() - t_star),
            "sd": float(np.sqrt(var)),
            "rmse": rmse, "crb_sd": crb_sd,
            "rmse_over_crb": rmse / crb_sd,
            "var_over_crb": var / (crb_var_1 / N),
            "n_clamped": int(n_clamped),
        })
    return {"t_star": float(t_star), "fisher_info": float(I_t),
            "M_trials": int(M), "by_N": results}


# ----------------------------------------------------------------------
# n-interval analysis (D1)+(D2)
# ----------------------------------------------------------------------

def n_interval_identity_check(groups, n_list, t_samples, h_rel=1e-5):
    """Verify dS_n/dt = -(t/4)Var(C2) - (n-1)Cov(ln d, C2) by central FD."""
    rows = []
    for g in groups:
        for t in t_samples:
            for n in n_list:
                h = h_rel * t
                fd = (entropies(g, t + h, n)["S"]
                      - entropies(g, t - h, n)["S"]) / (2 * h)
                e = entropies(g, t, n)
                rows.append({
                    "group": g, "t": float(t), "n_intervals": int(n),
                    "S_n": float(e["S"]),
                    "dS_dt_analytic": float(e["dS_dt_analytic"]),
                    "dS_dt_finite_diff": float(fd),
                    "rel_dev": float(abs(fd - e["dS_dt_analytic"])
                                     / max(abs(e["dS_dt_analytic"]), 1e-300)),
                })
    return rows


def n_interval_fisher_demo(group, t_star, N, M, n_intervals, rng):
    """(D2) operational check that extra cuts add no information.

    Each of the M trials prepares N independent copies of the HH circle
    state; each copy is cut into n_intervals intervals (2n cut points).
    Because the reduced state is block-diagonal in ONE shared R per copy,
    the 2n cut-point fluxes of a copy are identical: the 'dataset' of
    2nN flux readings contains only N independent samples.  The MLE from
    the duplicated dataset is EXACTLY the MLE from the N unique samples
    (the sample mean of C2 is unchanged by duplication), so its sd obeys
    the N-sample CRB, not the hypothetical 2nN-sample CRB.
    """
    p, _, d, c2 = flux_distribution(group, t_star)
    keep = p > 1e-17
    p_k, c2_k = p[keep], c2[keep]
    p_k = p_k / p_k.sum()
    I_t = entropies(group, t_star)["fisher_info"]
    counts = rng.multinomial(N, p_k, size=M)
    mbars = counts @ c2_k / N            # mean over the N unique samples
    dup = 2 * n_intervals
    mbars_dup = (counts * dup) @ c2_k / (N * dup)   # duplicated dataset
    # identical as estimators (exact rational identity); float64 summation
    # order differs, so assert agreement to 1e-14 relative and record it
    dup_dev = float(np.max(np.abs(mbars_dup - mbars) / np.abs(mbars)))
    assert dup_dev < 1e-14
    t_hats = np.array([mle_from_mean(group, mb)[0] for mb in mbars])
    sd = float(t_hats.std(ddof=1))
    crb_N = float(np.sqrt(1.0 / (I_t * N)))
    crb_2nN = float(np.sqrt(1.0 / (I_t * N * dup)))
    return {
        "group": group, "t_star": float(t_star), "N_preparations": int(N),
        "M_trials": int(M), "n_intervals": int(n_intervals),
        "n_cut_points": int(dup),
        "mle_identical_on_duplicated_dataset": True,
        "max_rel_dev_duplicated_sample_mean": dup_dev,
        "sd_t_hat": sd,
        "crb_sd_N_samples": crb_N,
        "crb_sd_2nN_samples_hypothetical": crb_2nN,
        "sd_over_crb_N": sd / crb_N,
        "sd_over_crb_2nN": sd / crb_2nN,
        "verdict": ("Fisher information does NOT scale with the number of "
                    "cuts: sd matches the N-sample CRB (ratio ~1), not the "
                    "2nN-sample CRB (ratio ~sqrt(2n)). The flux is one "
                    "global random variable."),
    }


# ----------------------------------------------------------------------
# figure
# ----------------------------------------------------------------------

def make_figure(curves_su3, recon, fname_base):
    fig, axes = plt.subplots(1, 3, figsize=(14.0, 4.2))

    ax = axes[0]
    colors = ["#1f77b4", "#d62728", "#2ca02c"]
    for t, c in zip([0.5, 2.0, 8.0], colors):
        p, _, d, c2 = flux_distribution("SU3", t)
        sel = p > 1e-6
        order = np.argsort(c2[sel])
        ax.plot(c2[sel][order], p[sel][order], "o", ms=3.5, color=c,
                label=rf"$t={t}$")
    ax.set_yscale("log")
    ax.set_ylim(1e-6, 1.5)
    ax.set_xlim(-0.5, 30)
    ax.set_xlabel(r"$C_2(p,q)$")
    ax.set_ylabel(r"$p_R(t)$")
    ax.set_title(r"(a) SU(3) flux distribution $p_R \propto d_R^2 e^{-tC_2/2}$")
    ax.legend(fontsize=8, frameon=False)

    ax = axes[1]
    t = curves_su3["t"]
    ax.plot(t, curves_su3["S"], "-", color="#1f77b4", lw=2,
            label=r"$n=1$: $S(t)$")
    for n, ls in [(2, "--"), (3, ":")]:
        Sn = curves_su3["H"] + 2 * n * curves_su3["mean_ln_d"]
        ax.plot(t, Sn, ls, color="#1f77b4", lw=1.2,
                label=rf"$n={n}$ intervals")
    ax.plot(t, curves_su3["H"], "-", color="#d62728", lw=1.2,
            label=r"Shannon piece $H(t)$ (any $n$)")
    ax.set_xscale("log")
    ax.set_xlabel(r"$t = g^2 A$")
    ax.set_ylabel("entropy (nats)")
    ax.set_title(r"(b) SU(3): $S_n = H + 2n\langle\ln d\rangle$, all decreasing")
    ax.legend(fontsize=8, frameon=False)

    ax = axes[2]
    for tst, c, mk in [(1.0, "#1f77b4", "o"), (4.0, "#2ca02c", "^")]:
        rec = next(r for r in recon if r["t_star"] == tst)
        N = np.array([row["N"] for row in rec["by_N"]])
        rmse = np.array([row["rmse"] for row in rec["by_N"]])
        crb = np.array([row["crb_sd"] for row in rec["by_N"]])
        ax.loglog(N, rmse, mk, color=c, ms=6, label=rf"SU(3), $t^*={tst}$")
        ax.loglog(N, crb, "-", color=c, lw=1.2, alpha=0.7)
    ax.loglog([], [], "-", color="0.4", label="Cramér–Rao bound")
    ax.set_xlabel(r"$N$ flux samples")
    ax.set_ylabel(r"RMSE of $\hat{t}_{\rm MLE}$")
    ax.set_title(r"(c) SU(3) reconstruction vs CRB")
    ax.legend(fontsize=8, frameon=False)

    fig.tight_layout()
    fig.savefig(fname_base + ".png", dpi=200)
    fig.savefig(fname_base + ".pdf")
    plt.close(fig)


# ----------------------------------------------------------------------
# stages
# ----------------------------------------------------------------------

T_GRID = np.geomspace(0.05, 20.0, 400)
T_STARS_ALL = [0.5, 1.0, 2.0, 4.0]
N_LIST = [30, 100, 300, 1000, 3000, 10000, 30000]
M_TRIALS = 400


def stage1():
    t0 = time.time()
    curves = compute_curves("SU3", T_GRID)
    mono = analyze_monotonicity(curves)
    cap_small_t = float(curves["capacity"][0])
    inv = entropy_inversion_demo("SU3", [0.3, 0.7, 1.5, 3.0, 6.0, 12.0])
    print(f"  S strictly decreasing: {mono['S_strictly_decreasing_on_grid']}, "
          f"max dS/dt = {mono['max_dS_dt_analytic_on_grid']:.3e}")
    print(f"  max|S_direct - S_C1| = {mono['max_abs_S_direct_minus_S_C1']:.2e}, "
          f"FD max rel dev = "
          f"{mono['max_rel_dev_numeric_vs_analytic_dSdt_interior']:.2e}")
    print(f"  Shannon piece: {mono['shannon_piece']}")
    print(f"  capacity at t={T_GRID[0]}: {cap_small_t:.6f} "
          f"(dim G/2 = {DIM_G['SU3']/2})")
    print(f"  inversion worst err = {max(r['abs_error'] for r in inv):.2e}")
    sub = slice(0, len(T_GRID), 5)
    curves_json = {k: [float(x) for x in curves[k][sub]]
                   for k in ["t", "S", "H", "mean_C2", "var_C2", "mean_ln_d",
                             "cov_lnd_C2", "dS_dt_analytic", "fisher_info",
                             "capacity"]}
    out = {"curves_SU3": curves_json, "monotonicity_SU3": mono,
           "capacity_small_t_SU3": {"t": float(T_GRID[0]),
                                    "capacity": cap_small_t,
                                    "dim_G_over_2": DIM_G["SU3"] / 2.0},
           "entropy_inversion_demo_SU3": inv}
    with open(os.path.join(HERE, "su3_stage1.json"), "w") as f:
        json.dump(out, f, indent=1)
    print(f"  stage1 done in {time.time()-t0:.1f} s")
    return out


def stage2(t_stars):
    t0 = time.time()
    recs = []
    for ts in t_stars:
        rng = np.random.default_rng([SEED, 2, int(round(10 * ts))])
        r = reconstruction_demo("SU3", ts, N_LIST, M_TRIALS, rng)
        recs.append(r)
        head = {row["N"]: row for row in r["by_N"]}
        print(f"  t*={ts}: rmse(N=1e3)={head[1000]['rmse']:.4f} "
              f"(CRB {head[1000]['crb_sd']:.4f}, ratio "
              f"{head[1000]['rmse_over_crb']:.3f}); "
              f"rmse(N=1e4)={head[10000]['rmse']:.4f} "
              f"(ratio {head[10000]['rmse_over_crb']:.3f})")
    fn = os.path.join(HERE, f"su3_stage2_{'_'.join(str(x) for x in t_stars)}.json")
    with open(fn, "w") as f:
        json.dump(recs, f, indent=1)
    print(f"  stage2{t_stars} done in {time.time()-t0:.1f} s")
    return recs


def stage3():
    t0 = time.time()
    ident = n_interval_identity_check(["SU2", "U1", "SU3"], [1, 2, 3, 4],
                                      [0.3, 1.0, 3.0, 8.0])
    worst = max(r["rel_dev"] for r in ident)
    print(f"  dS_n/dt identity: worst FD rel dev = {worst:.2e} "
          f"over {len(ident)} (group, t, n) combinations")
    fisher_demo = [
        n_interval_fisher_demo("SU3", 1.0, 1000, 400, 3,
                               np.random.default_rng([SEED, 3, 0])),
        n_interval_fisher_demo("SU2", 1.0, 1000, 400, 3,
                               np.random.default_rng([SEED, 3, 1])),
    ]
    for fd in fisher_demo:
        print(f"  {fd['group']}: sd/CRB_N = {fd['sd_over_crb_N']:.3f}, "
              f"sd/CRB_2nN = {fd['sd_over_crb_2nN']:.3f} "
              f"(sqrt(2n) = {np.sqrt(2*fd['n_intervals']):.3f})")
    out = {"identity_dSn_dt": ident, "worst_rel_dev": worst,
           "fisher_scaling_demo": fisher_demo,
           "verdict": "Fisher information does NOT scale with n. The "
                      "n-interval entropy grows linearly in n through the "
                      "edge term 2n<ln d>, but the flux variables at the 2n "
                      "cut points are copies of ONE global R; the joint "
                      "measurement carries I(t)=Var(C2)/4 regardless of n. "
                      "Entropy scales; information does not."}
    with open(os.path.join(HERE, "su3_stage3.json"), "w") as f:
        json.dump(out, f, indent=1)
    print(f"  stage3 done in {time.time()-t0:.1f} s")
    return out


def merge(stage1_out=None, recon=None, stage3_out=None, runtime=None):
    if stage1_out is None:
        with open(os.path.join(HERE, "su3_stage1.json")) as f:
            stage1_out = json.load(f)
    if recon is None:
        recon = []
        for ts_chunk in [[0.5, 1.0], [2.0, 4.0]]:
            fn = os.path.join(
                HERE, f"su3_stage2_{'_'.join(str(x) for x in ts_chunk)}.json")
            with open(fn) as f:
                recon.extend(json.load(f))
    if stage3_out is None:
        with open(os.path.join(HERE, "su3_stage3.json")) as f:
            stage3_out = json.load(f)
    # figure needs curves as arrays
    curves = {k: np.array(v) for k, v in stage1_out["curves_SU3"].items()}
    make_figure(curves, recon, os.path.join(HERE, "fig_su3"))
    results = {
        "meta": {
            "seed": SEED,
            "date": "2026-06-09",
            "t_definition": "t = g^2 * A_total (sphere/HH state), "
                            "weight e^{-(t/2) C2(R)}",
            "su3_convention": {
                "irreps": "(p,q), p,q >= 0 (Dynkin labels)",
                "dim": "(p+1)(q+1)(p+q+2)/2",
                "C2": "(p^2+q^2+pq+3p+3q)/3",
                "checks": "C2(1,0)=4/3=(N^2-1)/2N, C2(1,1)=3=N, dim(1,1)=8 "
                          "(asserted at runtime)",
                "note": "Same normalization family as C2(j)=j(j+1) for SU(2) "
                        "(Tr T_aT_b = delta_ab/2 in the fundamental); any "
                        "rescaling C2 -> kappa C2 is the reparametrization "
                        "t -> kappa t. Verified against standard sources "
                        "2026-06-09 (see paper3/draft.md references).",
            },
            "n_interval_setting": {
                "state": "Hartle-Hawking sphere state on a spatial circle, "
                         "region A = n disjoint intervals (2n cut points), "
                         "Donnelly 1406.7304 eq. (YM2entropy): "
                         "S = sum_R p(R)(-log p(R) + 2n log dim R)",
                "p_R_n_independence": "p_R is independent of n: the physical "
                         "state is a class function of one holonomy, so the "
                         "boundary irrep R is a single global random variable "
                         "shared by all 2n cut points (verified against the "
                         "1406.7304 LaTeX source, canonical and replica "
                         "sections; GS14 eq. (answ) with chi=2, l=n agrees).",
            },
            "mle_truncation_note": "MLE inner loop uses cutoff e^-120 "
                         "(relative truncation < 1e-50); curves/identities "
                         "use e^-800 (exactly zero error in float64).",
            "runtime_seconds": runtime,
        },
        "curves_SU3": stage1_out["curves_SU3"],
        "monotonicity_SU3": stage1_out["monotonicity_SU3"],
        "capacity_small_t_SU3": stage1_out["capacity_small_t_SU3"],
        "entropy_inversion_demo_SU3": stage1_out["entropy_inversion_demo_SU3"],
        "reconstruction_SU3": recon,
        "n_intervals": stage3_out,
    }
    with open(os.path.join(HERE, "su3_results.json"), "w") as f:
        json.dump(results, f, indent=1)
    # clean up stage files
    for fn in os.listdir(HERE):
        if fn.startswith("su3_stage"):
            os.remove(os.path.join(HERE, fn))
    print("  wrote su3_results.json, fig_su3.png, fig_su3.pdf")


def main():
    args = sys.argv[1:]
    if not args:
        t0 = time.time()
        s1 = stage1()
        recon = stage2([0.5, 1.0]) + stage2([2.0, 4.0])
        s3 = stage3()
        merge(s1, recon, s3, runtime=round(time.time() - t0, 1))
        return
    for a in args:
        if a == "stage1":
            stage1()
        elif a.startswith("stage2:"):
            stage2([float(x) for x in a.split(":")[1].split(",")])
        elif a == "stage3":
            stage3()
        elif a == "merge":
            merge()
        else:
            raise SystemExit(f"unknown arg {a}")


if __name__ == "__main__":
    main()
