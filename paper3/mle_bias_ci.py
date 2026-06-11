#!/usr/bin/env python3
"""
mle_bias_ci.py -- Finite-sample bias and confidence-interval analysis for the
MLE of t = g^2 A from boundary-flux samples in 2d Yang-Mills. Companion to
ym2/ym2_flux.py and ym2/ym2_su3.py (same conventions, formulas (F3)/(C4)/(C6)
of ym2/FORMULAS.md); new for the round-2 revision of paper 3.

For each cell (group, t*, N): M independent batches of N i.i.d. flux samples
R_1..R_N ~ p_R(t*), MLE t-hat by moment matching (exponential family), then:

  * bias = E[t-hat] - t*, compared with the first-order analytic bias for
    this exponential family,
        b_1(t*) = kappa_3(C2) / (N * Var(C2)^2),
    obtained by Taylor-expanding the inverse moment map t-hat = mu^{-1}(mbar)
    around mbar = mu(t*), using mu'(t) = -Var_t(C2)/2 and
    mu''(t) = kappa_3(C2)/4 (cumulant identities of the family).

  * Wald 95% CI: t-hat +/- z_{.975}/sqrt(N I(t-hat)), I(t) = Var_t(C2)/4.

  * Profile-likelihood 95% CI: { t : 2[l(t-hat) - l(t)] <= chi2_{1,.95} }.
    The deviance depends on the data only through the sufficient statistic
    mbar = N^{-1} sum_i C2(R_i):
        D(t) = N [ (t - t-hat) * mbar + 2 (ln Z(t) - ln Z(t-hat)) ].

Coverage = fraction of M batches whose CI contains t*; MC standard error of a
95%-coverage estimate at M = 2000 is ~0.49%.

Groups U(1), SU(2), SU(3); t* in {0.5, 1, 4}; N in {100, 1000, 10000}.
Deterministic: per-cell streams np.random.default_rng([SEED, gi, ti, ni]).
Runs with or without scipy (pure-Python Brent fallback included).
Output: mle_bias_ci.json (in this script's directory) + console table.
"""

import json
import os
import time

import numpy as np

try:
    from scipy.optimize import brentq
except ImportError:  # pure-Python Brent (classic zeroin), same contract
    def brentq(f, xa, xb, xtol=2e-12, rtol=8.881784197001252e-16, maxiter=100):
        xpre, xcur = xa, xb
        fpre, fcur = f(xpre), f(xcur)
        if fpre * fcur > 0:
            raise ValueError("f(a) and f(b) must have different signs")
        if fpre == 0.0:
            return xpre
        if fcur == 0.0:
            return xcur
        xblk = fblk = spre = scur = 0.0
        for _ in range(maxiter):
            if fpre * fcur < 0:
                xblk, fblk = xpre, fpre
                spre = scur = xcur - xpre
            if abs(fblk) < abs(fcur):
                xpre, xcur, xblk = xcur, xblk, xcur
                fpre, fcur, fblk = fcur, fblk, fcur
            delta = (xtol + rtol * abs(xcur)) / 2
            sbis = (xblk - xcur) / 2
            if fcur == 0.0 or abs(sbis) < delta:
                return xcur
            if abs(spre) > delta and abs(fcur) < abs(fpre):
                if xpre == xblk:
                    stry = -fcur * (xcur - xpre) / (fcur - fpre)
                else:
                    dpre = (fpre - fcur) / (xpre - xcur)
                    dblk = (fblk - fcur) / (xblk - xcur)
                    stry = -fcur * (fblk * dblk - fpre * dpre) / (
                        dblk * dpre * (fblk - fpre))
                if 2 * abs(stry) < min(abs(spre), 3 * abs(sbis) - delta):
                    spre, scur = scur, stry
                else:
                    spre = sbis
                    scur = sbis
            else:
                spre = sbis
                scur = sbis
            xpre, fpre = xcur, fcur
            if abs(scur) > delta:
                xcur += scur
            else:
                xcur += delta if sbis > 0 else -delta
            fcur = f(xcur)
        return xcur

SEED = 20260609
HERE = os.path.dirname(os.path.abspath(__file__))

Z975 = 1.959963984540054        # Phi^{-1}(0.975)
CHI2_95 = 3.8414588206941254    # chi^2_{1, 0.95} = Z975^2
CUTOFF = 120.0                  # relative-weight cutoff e^{-120} (cf. ym2 MLE loop)
SLACK = 60.0                    # covers 2 ln d growth in the truncation bound

GROUPS = ["U1", "SU2", "SU3"]
T_STARS = [0.5, 1.0, 4.0]
N_LIST = [100, 1000, 10000]
M_TRIALS = 2000


def su3_dim(p, q):
    return (p + 1.0) * (q + 1.0) * (p + q + 2.0) / 2.0


def su3_c2(p, q):
    return (p * p + q * q + p * q + 3.0 * p + 3.0 * q) / 3.0


assert su3_dim(1, 0) == 3 and abs(su3_c2(1, 0) - 4.0 / 3.0) < 1e-15
assert su3_dim(1, 1) == 8 and abs(su3_c2(1, 1) - 3.0) < 1e-15


def irrep_data(group, t, cutoff=CUTOFF):
    """dims and Casimirs of all irreps with relative weight > e^-(cutoff)."""
    if group == "SU2":
        jmax = 0.5 * (np.sqrt(1.0 + 8.0 * (cutoff + SLACK) / t) - 1.0) + 2.0
        j = np.arange(0.0, jmax + 0.5, 0.5)
        return 2.0 * j + 1.0, j * (j + 1.0)
    if group == "U1":
        nmax = int(np.sqrt(2.0 * (cutoff + SLACK) / t)) + 2
        n = np.arange(-nmax, nmax + 1, dtype=float)
        return np.ones_like(n), n * n
    if group == "SU3":
        pmax = int(np.sqrt(6.0 * (cutoff + SLACK) / t)) + 2
        p, q = np.meshgrid(np.arange(pmax + 1, dtype=float),
                           np.arange(pmax + 1, dtype=float), indexing="ij")
        p, q = p.ravel(), q.ravel()
        return su3_dim(p, q), su3_c2(p, q)
    raise ValueError(group)


class Family:
    """ln Z, moments of C2 for one group on a FIXED irrep set (valid t >= t_lo)."""

    def __init__(self, group, t_lo):
        self.d, self.c2 = irrep_data(group, t_lo)
        self.ln_d2 = 2.0 * np.log(self.d)

    def _weights(self, t):
        w = self.ln_d2 - 0.5 * t * self.c2
        wmax = w.max()
        ew = np.exp(w - wmax)
        return wmax, ew

    def lnZ(self, t):
        wmax, ew = self._weights(t)
        return wmax + np.log(ew.sum())

    def p(self, t):
        _, ew = self._weights(t)
        return ew / ew.sum()

    def moments(self, t):
        """<C2>, Var(C2), kappa_3(C2) under p_R(t)."""
        p = self.p(t)
        m1 = float(p @ self.c2)
        dc = self.c2 - m1
        var = float(p @ dc**2)
        k3 = float(p @ dc**3)
        return m1, var, k3

    def mean_c2(self, t):
        p = self.p(t)
        return float(p @ self.c2)


def run_cell(group, t_star, N, M, rng):
    t_lo, t_hi = t_star / 8.0, t_star * 8.0 + 40.0
    fam = Family(group, t_lo)

    # sampling distribution at t*
    p_star = fam.p(t_star)
    keep = p_star > 1e-17
    p_k = p_star[keep] / p_star[keep].sum()
    c2_k = fam.c2[keep]

    m1, var, k3 = fam.moments(t_star)
    I_star = 0.25 * var
    bias_analytic = k3 / (N * var * var)
    lnZ_cache = {}

    def lnZ(t):
        if t not in lnZ_cache:
            lnZ_cache[t] = fam.lnZ(t)
        return lnZ_cache[t]

    counts = rng.multinomial(N, p_k, size=M)        # (M, K)
    mbars = counts @ c2_k / N

    t_hats = np.empty(M)
    wald_cover = np.zeros(M, dtype=bool)
    prof_cover = np.zeros(M, dtype=bool)
    wald_len = np.empty(M)
    prof_len = np.empty(M)
    n_clamped = 0

    for m in range(M):
        mbar = mbars[m]
        lnZ_cache.clear()
        f = lambda t: fam.mean_c2(t) - mbar
        if f(t_lo) <= 0.0:
            t_hat, clamped = t_lo, True
        elif f(t_hi) >= 0.0:
            t_hat, clamped = t_hi, True
        else:
            t_hat = brentq(f, t_lo, t_hi, xtol=1e-10, rtol=1e-12)
            clamped = False
        n_clamped += clamped
        t_hats[m] = t_hat

        # Wald CI with observed (plug-in) Fisher information
        _, var_hat, _ = fam.moments(t_hat)
        half = Z975 / np.sqrt(N * 0.25 * var_hat)
        wlo, whi = t_hat - half, t_hat + half
        wald_cover[m] = (wlo <= t_star <= whi)
        wald_len[m] = whi - wlo

        # profile-likelihood CI via the deviance D(t)
        lnZ_hat = lnZ(t_hat)

        def dev(t):
            return N * ((t - t_hat) * mbar + 2.0 * (lnZ(t) - lnZ_hat)) - CHI2_95

        if dev(t_lo) <= 0.0:
            plo = t_lo  # CI extends past bracket (recorded via n_clamped path)
        else:
            plo = brentq(dev, t_lo, t_hat, xtol=1e-9, rtol=1e-10)
        if dev(t_hi) <= 0.0:
            phi = t_hi
        else:
            phi = brentq(dev, t_hat, t_hi, xtol=1e-9, rtol=1e-10)
        prof_cover[m] = (plo <= t_star <= phi)
        prof_len[m] = phi - plo

    bias = float(t_hats.mean() - t_star)
    sd = float(t_hats.std(ddof=1))
    return {
        "group": group, "t_star": t_star, "N": int(N), "M": int(M),
        "fisher_info": I_star,
        "crb_sd": float(np.sqrt(1.0 / (N * I_star))),
        "bias": bias,
        "bias_se": float(sd / np.sqrt(M)),
        "bias_analytic_first_order": float(bias_analytic),
        "N_times_bias": float(N * bias),
        "N_times_bias_analytic": float(N * bias_analytic),
        "sd": sd,
        "rmse": float(np.sqrt(np.mean((t_hats - t_star) ** 2))),
        "wald_coverage": float(wald_cover.mean()),
        "profile_coverage": float(prof_cover.mean()),
        "wald_mean_length": float(wald_len.mean()),
        "profile_mean_length": float(prof_len.mean()),
        "n_clamped": int(n_clamped),
    }


def main():
    t0 = time.time()
    cells = []
    print(f"{'group':5s} {'t*':>4s} {'N':>6s} | {'bias':>9s} {'b1(anlyt)':>9s} "
          f"{'N*bias':>7s} {'N*b1':>7s} | {'cov_W':>6s} {'cov_P':>6s} "
          f"{'len_W':>7s} {'len_P':>7s} | clamp")
    for gi, group in enumerate(GROUPS):
        for ti, t_star in enumerate(T_STARS):
            for ni, N in enumerate(N_LIST):
                rng = np.random.default_rng([SEED, gi, ti, ni])
                cell = run_cell(group, t_star, N, M_TRIALS, rng)
                cells.append(cell)
                print(f"{group:5s} {t_star:4.1f} {N:6d} | "
                      f"{cell['bias']:+9.5f} {cell['bias_analytic_first_order']:+9.5f} "
                      f"{cell['N_times_bias']:+7.3f} {cell['N_times_bias_analytic']:+7.3f} | "
                      f"{cell['wald_coverage']:6.4f} {cell['profile_coverage']:6.4f} "
                      f"{cell['wald_mean_length']:7.4f} {cell['profile_mean_length']:7.4f} | "
                      f"{cell['n_clamped']}", flush=True)
    out = {
        "meta": {
            "seed": SEED,
            "date": "2026-06-10",
            "M_trials": M_TRIALS,
            "z975": Z975, "chi2_1_95": CHI2_95,
            "wald": "t_hat +/- z975/sqrt(N I(t_hat)), plug-in information",
            "profile": "deviance N[(t-t_hat)mbar + 2(lnZ(t)-lnZ(t_hat))] <= chi2",
            "bias_first_order": "b1 = kappa3(C2)/(N Var(C2)^2) at t*",
            "runtime_seconds": round(time.time() - t0, 1),
        },
        "cells": cells,
    }
    out["meta"]["runtime_seconds"] = round(time.time() - t0, 1)
    with open(os.path.join(HERE, "mle_bias_ci.json"), "w") as fjson:
        json.dump(out, fjson, indent=1)
    print(f"done in {out['meta']['runtime_seconds']} s -> mle_bias_ci.json")


if __name__ == "__main__":
    main()
# end of file (padding line against mount truncation)
