#!/usr/bin/env python3
"""
Compact U(1) in 3+1 dimensions: electric flux-sector distribution across a
closed entangling surface, in the weak-coupling (Gaussian / discrete-Gaussian)
regime, on the lattice.

Setup
-----
Kogut-Susskind Hamiltonian on an L^3 periodic spatial lattice,

    H = (g^2/2) sum_links E_l^2 - (1/g^2) sum_plaq cos(theta_p),

with integer E_l (compact U(1)).  At weak coupling the ground state approaches
the noncompact lattice Maxwell ground state, which is Gaussian in E with

    <E_l E_l'> = (1/(2 g^2)) * Sigma0[l,l'],
    Sigma0 = (curl^T curl)^{1/2} restricted to the transverse subspace
           = (1/L^3) sum_{k != 0} omega(k) P_T(k) e^{i k (x - x')},
    omega(k) = sqrt(sum_mu 4 sin^2(k_mu/2)),  P_T = 1 - d d^dag / |d|^2,
    d_mu(k) = e^{i k_mu} - 1.

The flux-sector distribution through a closed surface (here: faces of an RxRxR
cube; cut links = links crossing the surface, oriented outward) is modeled by
the discrete Gaussian

    P({n}; g^2) = exp( - g^2 * T(n) ) / Z(g^2),
    T(n) = n^T Q n,  Q = pinv( Sigma0 restricted to cut links, signed ),

supported on the integer hyperplane sum_l n_l = 0 (Gauss law: no enclosed
charge).  This is a ONE-PARAMETER EXPONENTIAL FAMILY with natural parameter
theta = g^2 (== e^2 in lattice units; any monotone function of 1/e^2 works)
and sufficient statistic T(n).  Hence exactly within this model:

    I(theta) = Var_theta(T),         dS/dtheta = -theta * I(theta),

and in the continuum limit of the discrete sum (g^2 -> 0):

    I(g^2) -> m / (2 g^4),    m = rank(Sigma0_cut) = N_boundary - 1.

This script verifies all of the above numerically (no scipy; deterministic,
seed 20260610):
  1. k-sum covariance vs direct dense construction on a small lattice;
  2. rank and Gauss null vector for cube surfaces R=1,2,3 (N_b=6,24,54);
  3. exact enumeration for R=1: I, S, identity, m-law and its discreteness
     corrections vs g^2;
  4. seeded Metropolis for R=2,3: Var(T) vs m/(2 g^4)  -> area scaling.

Writes results_gauss.json.
"""
import json
import os
import time

import numpy as np

SEED = 20260610
L = 10  # spatial lattice for the k-sum covariance


# ----------------------------------------------------------------------
# covariance
# ----------------------------------------------------------------------
def ksum_cov(pairs, L):
    """Sigma0 entries for given ((x,mu),(x',nu)) pairs via the k-sum."""
    ks = 2 * np.pi * np.arange(L) / L
    KX, KY, KZ = np.meshgrid(ks, ks, ks, indexing='ij')
    K = np.stack([KX.ravel(), KY.ravel(), KZ.ravel()], axis=1)  # (L^3, 3)
    K = K[1:]  # drop k=0 (harmonic modes carry no E fluctuation)
    d = np.exp(1j * K) - 1.0          # (Nk, 3)
    w2 = (np.abs(d) ** 2).sum(axis=1)  # omega^2
    om = np.sqrt(w2)
    out = []
    for (x1, mu), (x2, nu) in pairs:
        dx = np.array(x1, dtype=float) - np.array(x2, dtype=float)
        phase = np.exp(1j * (K @ dx))
        PT = (mu == nu) * 1.0 - d[:, mu] * np.conj(d[:, nu]) / w2
        val = (om * PT * phase).sum().real / L ** 3
        out.append(val)
    return np.array(out)


def direct_cov_small(Ls=4):
    """Dense construction of Sigma0 on an Ls^3 lattice (validation)."""
    sites = [(x, y, z) for x in range(Ls) for y in range(Ls) for z in range(Ls)]
    li = {}
    links = []
    for s in sites:
        for mu in range(3):
            li[(s, mu)] = len(links)
            links.append((s, mu))
    nl = len(links)

    def shift(s, mu, d=1):
        s = list(s)
        s[mu] = (s[mu] + d) % Ls
        return tuple(s)

    # plaquettes: (s, mu<nu): theta_mu(s) + theta_nu(s+mu) - theta_mu(s+nu) - theta_nu(s)
    rows = []
    for s in sites:
        for mu in range(3):
            for nu in range(mu + 1, 3):
                r = np.zeros(nl)
                r[li[(s, mu)]] += 1
                r[li[(shift(s, mu), nu)]] += 1
                r[li[(shift(s, nu), mu)]] -= 1
                r[li[(s, nu)]] -= 1
                rows.append(r)
    C = np.array(rows)
    Lmat = C.T @ C
    evals, evecs = np.linalg.eigh(Lmat)
    Sig0 = np.zeros((nl, nl))
    for lam, u in zip(evals, evecs.T):
        if lam > 1e-9:
            Sig0 += np.sqrt(lam) * np.outer(u, u)
    return Sig0, links, li


def validate_ksum(Ls=4):
    Sig0, links, li = direct_cov_small(Ls)
    rng = np.random.default_rng([SEED, 17])
    idx = rng.choice(len(links), size=(40, 2))
    pairs = [((links[i][0], links[i][1]), (links[j][0], links[j][1]))
             for i, j in idx]
    vals = ksum_cov(pairs, Ls)
    ref = np.array([Sig0[i, j] for i, j in idx])
    return float(np.abs(vals - ref).max())


# ----------------------------------------------------------------------
# cut links for a cube region [0,R)^3
# ----------------------------------------------------------------------
def cube_cut_links(R):
    """[( (site, mu), outward_sign )] for region = cube [0,R)^3."""
    inside = lambda s: all(0 <= c < R for c in s)
    cut = []
    seen = set()
    for x in range(-1, R + 1):
        for y in range(-1, R + 1):
            for z in range(-1, R + 1):
                s = (x % L, y % L, z % L)
                raw = (x, y, z)
                for mu in range(3):
                    head_raw = list(raw)
                    head_raw[mu] += 1
                    tin = inside(raw)
                    hin = inside(tuple(head_raw))
                    if tin == hin:
                        continue
                    key = (s, mu)
                    if key in seen:
                        continue
                    seen.add(key)
                    cut.append((key, +1 if tin else -1))
    return cut


def cut_matrices(R):
    cl = cube_cut_links(R)
    nb = len(cl)
    pairs = []
    for i in range(nb):
        for j in range(nb):
            pairs.append((cl[i][0], cl[j][0]))
    vals = ksum_cov(pairs, L)
    Sig = vals.reshape(nb, nb)
    sgn = np.array([s for _, s in cl], dtype=float)
    Sig = Sig * np.outer(sgn, sgn)
    Sig = 0.5 * (Sig + Sig.T)
    evals, evecs = np.linalg.eigh(Sig)
    m = int((evals > 1e-9 * evals.max()).sum())
    Q = np.zeros_like(Sig)
    for lam, u in zip(evals, evecs.T):
        if lam > 1e-9 * evals.max():
            Q += (1.0 / lam) * np.outer(u, u)
    ones = np.ones(nb) / np.sqrt(nb)
    null_resid = float(np.linalg.norm(Sig @ ones))
    return Sig, Q, m, null_resid, nb


# ----------------------------------------------------------------------
# exact enumeration (R=1)
# ----------------------------------------------------------------------
def enumerate_hyperplane(nb, nmax):
    rng = np.arange(-nmax, nmax + 1, dtype=np.int16)
    base = len(rng)
    tot = base ** nb
    idx = np.arange(tot, dtype=np.int64)
    cfg = np.empty((tot, nb), dtype=np.int16)
    for i in range(nb - 1, -1, -1):
        cfg[:, i] = rng[(idx % base).astype(np.int64)]
        idx //= base
    return cfg[cfg.sum(axis=1) == 0]


def exact_R1(Q, m, g2grid, nmax=7):
    cfg = enumerate_hyperplane(6, nmax)
    x = cfg.astype(np.float64)
    T = np.einsum('ci,ij,cj->c', x, Q, x)
    shell = (np.abs(cfg).max(axis=1) == nmax)
    out = []
    for g2 in g2grid:
        wts = np.exp(-g2 * (T - T.min()))
        Z = wts.sum()
        p = wts / Z
        tail = float(p[shell].sum())
        Tm = float((p * T).sum())
        VarT = float((p * T * T).sum() - Tm ** 2)
        S = float(-(p[p > 0] * np.log(p[p > 0])).sum())
        # identity dS/dg2 = -g2 Var(T): finite difference
        de = 0.003 * g2
        Ss = []
        for gg in (g2 - de, g2 + de):
            ww = np.exp(-gg * (T - T.min()))
            pp = ww / ww.sum()
            Ss.append(float(-(pp[pp > 0] * np.log(pp[pp > 0])).sum()))
        dS = (Ss[1] - Ss[0]) / (2 * de)
        out.append({"g2": g2, "S": S, "I_exact": VarT,
                    "I_continuum": m / (2 * g2 * g2),
                    "ratio_to_m_law": VarT * 2 * g2 * g2 / m,
                    "identity_ratio": dS / (-g2 * VarT),
                    "tail_mass_at_shell": tail,
                    "mean_T": Tm})
    return out


# ----------------------------------------------------------------------
# Metropolis (R=2,3): Var(T) of the discrete Gaussian
# ----------------------------------------------------------------------
def metropolis_varT(Q, g2, nb, nchains=1024, sweeps_burn=400, sweeps_meas=800,
                    seed_extra=0):
    """Vectorized-over-chains Metropolis on {n in Z^nb : sum n = 0}.
    Moves: n_i += d, n_j -= d. Returns (VarT, stderr, acc_rate)."""
    rng = np.random.default_rng([SEED, 101, seed_extra, int(g2 * 1e6), nb])
    n = np.zeros((nchains, nb), dtype=np.int64)
    G = np.zeros((nchains, nb))   # G = Q n per chain
    T = np.zeros(nchains)
    steps_burn = sweeps_burn * nb
    steps_meas = sweeps_meas * nb
    Qd = np.diag(Q)
    acc_count = 0
    tot_count = 0
    meas = []
    chain_means = None
    for phase, nsteps in (("burn", steps_burn), ("meas", steps_meas)):
        Ts_sum = np.zeros(nchains)
        T2_sum = np.zeros(nchains)
        nmeas = 0
        for step in range(nsteps):
            ij = rng.integers(0, nb, size=(nchains, 2))
            same = ij[:, 0] == ij[:, 1]
            ij[same, 1] = (ij[same, 0] + 1) % nb
            i, j = ij[:, 0], ij[:, 1]
            d = rng.integers(0, 2, size=nchains) * 2 - 1
            Gi = np.take_along_axis(G, i[:, None], axis=1)[:, 0]
            Gj = np.take_along_axis(G, j[:, None], axis=1)[:, 0]
            quad = Qd[i] + Qd[j] - 2 * Q[i, j]
            dT = 2 * d * (Gi - Gj) + quad
            accept = rng.random(nchains) < np.exp(np.minimum(0, -g2 * dT))
            acc_count += int(accept.sum())
            tot_count += nchains
            if accept.any():
                rows = np.nonzero(accept)[0]
                n[rows, i[rows]] += d[rows]
                n[rows, j[rows]] -= d[rows]
                G[rows] += d[rows, None] * (Q[i[rows]] - Q[j[rows]])
                T[rows] += dT[rows]
            if phase == "meas" and (step + 1) % nb == 0:
                Ts_sum += T
                T2_sum += T * T
                nmeas += 1
        if phase == "meas":
            # per-chain estimates -> combine; error from chain scatter
            mean_c = Ts_sum / nmeas
            var_c = T2_sum / nmeas - mean_c ** 2
            mu = mean_c.mean()
            # total variance = E[var_c] + Var(mean_c) (law of total variance)
            VarT = var_c.mean() + mean_c.var()
            err = (var_c + (mean_c - mu) ** 2).std() / np.sqrt(nchains)
            chain_means = mean_c
    # exact T recompute check (guards incremental updates)
    Texact = np.einsum('ci,ij,cj->c', n.astype(float), Q, n.astype(float))
    drift = float(np.abs(Texact - T).max())
    assert np.all(n.sum(axis=1) == 0)
    return float(VarT), float(err), acc_count / tot_count, drift


# ----------------------------------------------------------------------
def main():
    import sys
    stage = sys.argv[1] if len(sys.argv) > 1 else "all"
    t0 = time.time()
    here = os.path.dirname(os.path.abspath(__file__))
    part = os.path.join(here, "results_gauss_stage1.json")
    if stage in ("all", "stage1"):
        out = stage1(t0, here)
        with open(part, "w") as f:
            json.dump(out, f, indent=1, default=float)
        if stage == "stage1":
            print("stage1 done (%.0fs)" % (time.time() - t0))
            return
    if stage in ("all", "stage2"):
        with open(part) as f:
            out = json.load(f)
        stage2(out, t0, here)


def stage1(t0, here):
    out = {"seed": SEED, "L": L}

    print("[1] validating k-sum covariance against dense construction (L=4)")
    diff = validate_ksum(4)
    out["ksum_vs_direct_maxdiff"] = diff
    assert diff < 1e-9, diff
    print("    max diff %.2e" % diff)

    print("[2] cube surfaces: rank and Gauss null vector")
    surf = {}
    for R in (1, 2, 3):
        Sig, Q, m, null_resid, nb = cut_matrices(R)
        surf["R%d" % R] = {"N_b": nb, "m_rank": m, "null_resid": null_resid,
                           "diag_Sigma0_mean": float(np.diag(Sig).mean())}
        assert nb == 6 * R * R
        assert m == nb - 1, (R, m, nb)
        assert null_resid < 1e-8
        print("    R=%d: N_b=%d rank=%d (=N_b-1) null=%.1e" %
              (R, nb, m, null_resid))
    out["surfaces"] = surf

    print("[3] R=1 exact enumeration")
    g2grid = [0.4, 0.5, 0.6, 0.8, 1.0, 1.25, 1.5, 2.0, 3.0, 4.0, 6.0]
    _, Q1, m1, _, _ = cut_matrices(1)
    out["R1_exact"] = exact_R1(Q1, m1, g2grid, nmax=7)
    for row in out["R1_exact"]:
        print("    g2=%.2f  I=%.4f  I/(m/2g4)=%.4f  identity=%.6f  tail=%.1e"
              % (row["g2"], row["I_exact"], row["ratio_to_m_law"],
                 row["identity_ratio"], row["tail_mass_at_shell"]))
        assert abs(row["identity_ratio"] - 1) < 1e-3
    return out


def stage2(out, t0, here):
    print("[4] R=2,3 Metropolis: area scaling of I  (elapsed %.0fs)"
          % (time.time() - t0))
    rows_todo = [(2, 0.4), (2, 0.7), (2, 1.0), (3, 0.5), (3, 1.0)]
    Qcache = {}
    mc = []
    for k, (R, g2) in enumerate(rows_todo):
        rowfn = os.path.join(here, "mc_row_%d.json" % k)
        if os.path.exists(rowfn):
            with open(rowfn) as f:
                mc.append(json.load(f))
            continue
        if time.time() - t0 > 32:
            print("BUDGET: rerun 'gauss4d.py stage2' to continue MC rows")
            return
        if R not in Qcache:
            Qcache[R] = cut_matrices(R)
        _, Q, m, _, nb = Qcache[R]
        VarT, err, acc, drift = metropolis_varT(Q, g2, nb)
        row = {"R": R, "g2": g2, "N_b": nb, "m": m,
               "I_MC": VarT, "I_MC_err": err,
               "I_continuum": m / (2 * g2 * g2),
               "ratio_to_m_law": VarT * 2 * g2 * g2 / m,
               "acc_rate": acc, "T_drift_check": drift}
        assert drift < 1e-6
        with open(rowfn, "w") as f:
            json.dump(row, f, default=float)
        mc.append(row)
        print("    R=%d g2=%.2f I=%.2f+-%.2f  m/(2g4)=%.2f ratio=%.3f acc=%.2f"
              % (R, g2, VarT, err, row["I_continuum"],
                 row["ratio_to_m_law"], acc))
    out["MC"] = mc

    # area-scaling table at the weak end
    table = []
    r1 = [r for r in out["R1_exact"] if abs(r["g2"] - 0.4) < 1e-9][0]
    table.append({"R": 1, "N_b": 6, "m": 5, "g2": 0.4,
                  "I_times_2g4": r1["I_exact"] * 2 * 0.4 ** 2,
                  "method": "exact enumeration"})
    for row in mc:
        if row["g2"] in (0.4, 0.5):
            table.append({"R": row["R"], "N_b": row["N_b"], "m": row["m"],
                          "g2": row["g2"],
                          "I_times_2g4": row["I_MC"] * 2 * row["g2"] ** 2,
                          "err": row["I_MC_err"] * 2 * row["g2"] ** 2,
                          "method": "Metropolis"})
    out["area_scaling_table"] = table

    out["elapsed_s"] = time.time() - t0
    with open(os.path.join(here, "results_gauss.json"), "w") as f:
        json.dump(out, f, indent=1, default=float)
    print("wrote results_gauss.json (%.0fs)" % out["elapsed_s"])


if __name__ == "__main__":
    main()
