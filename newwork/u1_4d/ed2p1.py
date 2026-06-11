#!/usr/bin/env python3
"""
Exact diagonalization of compact U(1) lattice gauge theory in 2+1 dimensions
(Kogut-Susskind Hamiltonian, dual height representation), and the electric
flux-sector distribution through closed entangling curves.

Theory and conventions
----------------------
Spatial lattice: Lx x Ly periodic torus. Links carry compact angles theta_l
with conjugate integer electric fields E_l, [theta_l, E_l] = i.

    H = (g^2/2) sum_links E_l^2  -  (1/g^2) sum_plaq cos(theta_p),
    theta_p = theta_x(x,y) + theta_y(x+1,y) - theta_x(x,y+1) - theta_y(x,y).

Gauss law (vacuum, no charges): (div E)|psi> = 0 at every site.  Solved
exactly by the dual height representation: integer h_p on plaquettes
(defined up to a global shift; winding sectors w = 0 for the ground state),

    E_x(x,y) = h(x,y) - h(x,y-1),     E_y(x,y) = h(x-1,y) - h(x,y),

so that div E = 0 identically and the plaquette operator U_p = e^{i theta_p}
acts as h_p -> h_p + 1 (checked: it raises E on the four links with the signs
with which they enter theta_p).  Dual Hamiltonian:

    H = (g^2/2) sum_{dual bonds <pp'>} (h_p - h_{p'})^2
        - (1/(2g^2)) sum_p (S_p^+ + S_p^-),     S_p^± : h_p -> h_p ± 1.

We gauge-fix h_{(0,0)} = 0 and truncate |h_p| <= Hmax for the others.
S^±_{(0,0)} then shifts ALL free heights by ∓1.

Sector observable (electric-centre / extended-lattice choice, CHR 1312.1183;
Soni-Trivedi 1510.07455): for a region A (set of sites), the cut links are
those with exactly one endpoint in A; the superselection sectors are labeled
by the outward fluxes n_l = ±E_l on the cut links; Gauss law forces
sum_l n_l = 0 (asserted at runtime).  p({n}; g^2) is obtained by binning
|psi_0(h)|^2 over the cut-link values.

Ground state: cyclically restarted two-pass Lanczos (no scipy), with
checkpointing so each invocation stays under a wall-clock budget.

Usage:
    python3 ed2p1.py run  Lx Ly Hmax g2 [budget_seconds]
    python3 ed2p1.py grid                  # print the run list (task queue)
    python3 ed2p1.py auto [budget_seconds] # work through pending runs
    python3 ed2p1.py analyze               # -> results_ed.json

Deterministic: seed 20260610.
"""
import json
import os
import sys
import time

import numpy as np

SEED = 20260610
OUTDIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ed_out")
RESID_TOL = 1e-9
MAX_CYCLES = 400


def lanczos_m(dim):
    """Cycle length chosen so one restarted cycle (2m matvecs) fits well
    inside a 45 s invocation even for the largest bases."""
    return 60 if dim < 2.0e6 else 14

# ----------------------------------------------------------------------
# task grid
# ----------------------------------------------------------------------
EPS_REL = 0.01  # relative half-step for d/dg^2 finite differences

CENTERS_33 = [0.6, 0.8, 1.0, 1.4, 2.0, 3.0, 4.0, 6.0]
CENTERS_23 = [0.4, 0.5, 0.6, 0.8, 1.0, 1.4, 2.0, 3.0, 4.0, 6.0, 8.0]


def task_list():
    tasks = []
    for c in CENTERS_23:
        for g2 in (c * (1 - EPS_REL), c, c * (1 + EPS_REL)):
            tasks.append((2, 3, 5, g2))
    for c in CENTERS_33:
        for g2 in (c * (1 - EPS_REL), c, c * (1 + EPS_REL)):
            tasks.append((3, 3, 2, g2))
    # truncation checks at the weak end (central values only)
    for c in (0.6, 1.0):
        tasks.append((3, 3, 3, c))
    for c in (0.4, 0.6):
        tasks.append((2, 3, 7, c))
    return tasks


def cuts_for(Lx, Ly):
    if (Lx, Ly) == (3, 3):
        return {"A1": [(0, 0)],
                "A2": [(0, 0), (1, 0)],
                "A3": [(0, 0), (1, 0), (0, 1), (1, 1)]}
    if (Lx, Ly) == (2, 3):
        return {"A1": [(0, 0)]}
    raise ValueError


# ----------------------------------------------------------------------
# lattice / dual-representation machinery
# ----------------------------------------------------------------------
class Dual:
    def __init__(self, Lx, Ly, Hmax):
        self.Lx, self.Ly, self.H = Lx, Ly, Hmax
        self.plaqs = [(x, y) for x in range(Lx) for y in range(Ly)]
        self.p0 = (0, 0)
        self.free = [p for p in self.plaqs if p != self.p0]
        self.nfree = len(self.free)
        self.axis = {p: i for i, p in enumerate(self.free)}
        self.dim = (2 * Hmax + 1) ** self.nfree
        self.shape = (2 * Hmax + 1,) * self.nfree
        # links: ('x',x,y): (x,y)->(x+1,y);  ('y',x,y): (x,y)->(x,y+1)
        self.links = [('x', x, y) for x in range(Lx) for y in range(Ly)] + \
                     [('y', x, y) for x in range(Lx) for y in range(Ly)]

    def link_plaqs(self, link):
        """(p_plus, p_minus) with E_link = h[p_plus] - h[p_minus]."""
        d, x, y = link
        Lx, Ly = self.Lx, self.Ly
        if d == 'x':
            return (x, y), (x, (y - 1) % Ly)
        return ((x - 1) % Lx, y), (x, y)

    def h_broadcast(self, p):
        """h values of plaquette p as a broadcastable array (0 for p0)."""
        if p == self.p0:
            return np.zeros((1,) * self.nfree, dtype=np.int16)
        ax = self.axis[p]
        v = np.arange(-self.H, self.H + 1, dtype=np.int16)
        shp = [1] * self.nfree
        shp[ax] = 2 * self.H + 1
        return v.reshape(shp)

    def link_E(self, link):
        """Full (broadcast) integer array of E on a link over the basis."""
        pp, pm = self.link_plaqs(link)
        return (self.h_broadcast(pp).astype(np.int16)
                - self.h_broadcast(pm).astype(np.int16))

    def diag_electric(self, g2):
        """(g^2/2) sum_links E^2 over the basis, as float64 of self.shape."""
        acc = np.zeros(self.shape, dtype=np.float64)
        for link in self.links:
            E = self.link_E(link).astype(np.float64)
            acc = acc + E * E  # broadcasting
        return 0.5 * g2 * acc

    def make_applyH(self, g2):
        diag = self.diag_electric(g2)
        hop = 1.0 / (2.0 * g2)
        n = self.nfree

        def applyH(psi):
            out = diag * psi
            for ax in range(n):
                lo = [slice(None)] * n
                hi = [slice(None)] * n
                lo[ax] = slice(0, -1)
                hi[ax] = slice(1, None)
                lo, hi = tuple(lo), tuple(hi)
                out[hi] -= hop * psi[lo]
                out[lo] -= hop * psi[hi]
            # gauge-fixed plaquette p0: shift all axes simultaneously
            lo = (slice(0, -1),) * n
            hi = (slice(1, None),) * n
            out[lo] -= hop * psi[hi]
            out[hi] -= hop * psi[lo]
            return out

        return applyH

    # ---------------- cut machinery ----------------
    def cut_links(self, region):
        """[(link, outward_sign)] for region = list of sites."""
        reg = set(region)
        Lx, Ly = self.Lx, self.Ly
        out = []
        for link in self.links:
            d, x, y = link
            head = ((x + 1) % Lx, y) if d == 'x' else (x, (y + 1) % Ly)
            tail = (x, y)
            tin, hin = tail in reg, head in reg
            if tin and not hin:
                out.append((link, +1))
            elif hin and not tin:
                out.append((link, -1))
        return out

    def sector_distribution(self, psi, region):
        """Joint distribution of outward fluxes on the cut links.

        Returns (configs [ncfg x nb int16], probs)."""
        cl = self.cut_links(region)
        nb = len(cl)
        H4 = 4 * self.H  # |E| <= 2H, so outward flux in [-2H, 2H]
        base = 2 * H4 + 1
        key = np.zeros(self.shape, dtype=np.int64)
        for i, (link, s) in enumerate(cl):
            E = (s * self.link_E(link)).astype(np.int64) + H4
            key = key * base + E  # broadcasting builds full array
        key = key.ravel()
        w = (psi.ravel() ** 2)
        uniq, inv = np.unique(key, return_inverse=True)
        probs = np.bincount(inv, weights=w, minlength=len(uniq))
        # decode configs
        cfg = np.zeros((len(uniq), nb), dtype=np.int16)
        k = uniq.copy()
        for i in range(nb - 1, -1, -1):
            cfg[:, i] = (k % base) - H4
            k //= base
        # Gauss check: sum of outward fluxes = 0 on every config with weight
        mask = probs > 1e-300
        assert np.all(cfg[mask].sum(axis=1) == 0), "Gauss law violated"
        order = np.argsort(-probs)
        return cfg[order], probs[order]


# ----------------------------------------------------------------------
# Lanczos (two-pass, cyclically restarted, checkpointed)
# ----------------------------------------------------------------------
def lanczos_cycle(applyH, v0, m):
    """One restarted cycle; returns (ritz_vector, ritz_value)."""
    alphas, betas = [], []
    v_prev = None
    v = v0.copy()
    for _ in range(m):
        w = applyH(v)
        a = float(np.vdot(v.ravel(), w.ravel()).real)
        w -= a * v
        if v_prev is not None:
            w -= betas[-1] * v_prev
        b = float(np.linalg.norm(w.ravel()))
        alphas.append(a)
        if b < 1e-13:
            betas.append(b)
            break
        betas.append(b)
        v_prev = v
        v = w / b
    k = len(alphas)
    T = np.zeros((k, k))
    for i in range(k):
        T[i, i] = alphas[i]
        if i + 1 < k:
            T[i, i + 1] = T[i + 1, i] = betas[i]
    evals, evecs = np.linalg.eigh(T)
    y = evecs[:, 0]
    th = evals[0]
    # pass 2: rebuild Ritz vector
    u = y[0] * v0
    v_prev = None
    v = v0.copy()
    for j in range(k - 1):
        w = applyH(v)
        w -= alphas[j] * v
        if v_prev is not None:
            w -= betas[j - 1] * v_prev
        b = betas[j]
        if b < 1e-13:
            break
        v_prev = v
        v = w / b
        u += y[j + 1] * v
    nrm = np.linalg.norm(u.ravel())
    return u / nrm, th


def ground_state(dual, g2, tag, budget_s):
    """Converge ground state with checkpointing. Returns psi or None."""
    ck = os.path.join(OUTDIR, "ck_%s.npz" % tag)
    rng = np.random.default_rng([SEED, dual.Lx, dual.Ly, dual.H,
                                 int(round(g2 * 1e9))])
    applyH = dual.make_applyH(g2)
    if os.path.exists(ck):
        d = np.load(ck)
        v = d["v"].reshape(dual.shape)
        cyc = int(d["cycle"])
    else:
        v = np.zeros(dual.shape, dtype=np.float64)
        v[(dual.H,) * dual.nfree] = 1.0  # h = 0
        v += 1e-3 * rng.standard_normal(dual.shape)
        v /= np.linalg.norm(v.ravel())
        cyc = 0
    t0 = time.time()
    m_cycle = lanczos_m(dual.dim)
    while cyc < MAX_CYCLES:
        v, th = lanczos_cycle(applyH, v, m_cycle)
        cyc += 1
        r = applyH(v) - th * v
        resid = np.linalg.norm(r.ravel()) / max(1.0, abs(th))
        if resid < RESID_TOL:
            if os.path.exists(ck):
                os.remove(ck)
            return v, th, resid, cyc
        if time.time() - t0 > budget_s:
            np.savez_compressed(ck, v=v.ravel(), cycle=cyc)
            print("CHECKPOINT %s cycle=%d resid=%.2e" % (tag, cyc, resid))
            return None
    raise RuntimeError("no convergence: %s resid=%.2e" % (tag, resid))


# ----------------------------------------------------------------------
# run / auto
# ----------------------------------------------------------------------
def tag_of(Lx, Ly, Hmax, g2):
    return "%dx%d_H%d_g%.9f" % (Lx, Ly, Hmax, g2)


def do_run(Lx, Ly, Hmax, g2, budget_s=33.0):
    os.makedirs(OUTDIR, exist_ok=True)
    tag = tag_of(Lx, Ly, Hmax, g2)
    fn = os.path.join(OUTDIR, "run_%s.npz" % tag)
    if os.path.exists(fn):
        return True
    dual = Dual(Lx, Ly, Hmax)
    res = ground_state(dual, g2, tag, budget_s)
    if res is None:
        return False
    psi, E0, resid, cycles = res
    payload = {"E0": E0, "resid": resid, "cycles": cycles, "g2": g2,
               "Lx": Lx, "Ly": Ly, "Hmax": Hmax}
    arrays = {}
    for name, region in cuts_for(Lx, Ly).items():
        cfg, probs = dual.sector_distribution(psi, region)
        keep = probs > 1e-16
        arrays["cfg_" + name] = cfg[keep]
        arrays["p_" + name] = probs[keep]
        payload["ptrunc_" + name] = float(probs[~keep].sum())
    # weak-coupling sanity: store <E_l E_l'> on the A1 cut links for the
    # Gaussian-model cross-check
    cl = dual.cut_links(cuts_for(Lx, Ly)["A1"])
    nb = len(cl)
    C = np.zeros((nb, nb))
    Es = [(s * dual.link_E(l)).astype(np.float64) for l, s in cl]
    w = psi ** 2
    for i in range(nb):
        for j in range(i, nb):
            C[i, j] = C[j, i] = float((Es[i] * Es[j] * w).sum())
    arrays["EEcov_A1"] = C
    np.savez_compressed(fn, meta=json.dumps(payload), **arrays)
    print("DONE %s E0=%.10f resid=%.1e cycles=%d" % (tag, E0, resid, cycles))
    return True


def cmd_auto(budget_s=38.0):
    t0 = time.time()
    for (Lx, Ly, Hmax, g2) in task_list():
        if time.time() - t0 > budget_s - 3:
            print("BUDGET REACHED; rerun auto")
            return
        left = budget_s - (time.time() - t0)
        ok = do_run(Lx, Ly, Hmax, g2, budget_s=left)
        if not ok:
            print("PENDING (checkpointed): rerun auto")
            return
    print("ALL RUNS COMPLETE")


# ----------------------------------------------------------------------
# Gaussian (noncompact lattice Maxwell) model on the same lattice
# ----------------------------------------------------------------------
def maxwell_cov0(Lx, Ly):
    """Sigma0 with <E E> = Sigma0/(2 g^2): Sigma0 = (curl^T curl)^{1/2}
    restricted to the transverse subspace. Link ordering as in Dual.links."""
    dual = Dual(Lx, Ly, 1)
    links = dual.links
    li = {l: i for i, l in enumerate(links)}
    nl = len(links)
    npq = Lx * Ly
    C = np.zeros((npq, nl))
    for pi, (x, y) in enumerate(dual.plaqs):
        C[pi, li[('x', x, y)]] += 1.0
        C[pi, li[('y', (x + 1) % Lx, y)]] += 1.0
        C[pi, li[('x', x, (y + 1) % Ly)]] -= 1.0
        C[pi, li[('y', x, y)]] -= 1.0
    L = C.T @ C
    evals, evecs = np.linalg.eigh(L)
    Sig0 = np.zeros((nl, nl))
    for lam, u in zip(evals, evecs.T):
        if lam > 1e-10:
            Sig0 += np.sqrt(lam) * np.outer(u, u)
    return Sig0, links


def model_for_cut(Lx, Ly, region):
    """(Sigma0_cut_signed, T-matrix Q = pinv(Sigma0_cut), m=rank)."""
    Sig0, links = maxwell_cov0(Lx, Ly)
    li = {l: i for i, l in enumerate(links)}
    dual = Dual(Lx, Ly, 1)
    cl = dual.cut_links(region)
    idx = [li[l] for l, s in cl]
    sgn = np.array([s for l, s in cl], dtype=float)
    Sub = Sig0[np.ix_(idx, idx)] * np.outer(sgn, sgn)
    evals, evecs = np.linalg.eigh(Sub)
    m = int((evals > 1e-9 * evals.max()).sum())
    Q = np.zeros_like(Sub)
    for lam, u in zip(evals, evecs.T):
        if lam > 1e-9 * evals.max():
            Q += (1.0 / lam) * np.outer(u, u)
    # null vector should be the all-ones (Gauss) direction
    ones = np.ones(len(idx)) / np.sqrt(len(idx))
    null_resid = float(np.linalg.norm(Sub @ ones))
    return Sub, Q, m, null_resid


def enumerate_hyperplane(nb, nmax):
    """Integer configs in [-nmax, nmax]^nb with sum = 0."""
    rng = np.arange(-nmax, nmax + 1, dtype=np.int16)
    base = len(rng)
    tot = base ** nb
    if tot > 3e7:
        raise MemoryError("enumeration too large: %d" % tot)
    idx = np.arange(tot, dtype=np.int64)
    cfg = np.empty((tot, nb), dtype=np.int16)
    for i in range(nb - 1, -1, -1):
        cfg[:, i] = rng[(idx % base).astype(np.int32)]
        idx //= base
    cfg = cfg[cfg.sum(axis=1) == 0]
    return cfg


def model_distribution(Q, g2, cfg):
    """Discrete-Gaussian model probs on given configs.
    exponent = -g^2 * T(n),  T(n) = n^T Q0 n with Q = pinv(Sigma0_cut)."""
    x = cfg.astype(np.float64)
    T = np.einsum('ci,ij,cj->c', x, Q, x)
    ex = -g2 * T
    ex -= ex.max()
    w = np.exp(ex)
    return w / w.sum(), T


# ----------------------------------------------------------------------
# analysis
# ----------------------------------------------------------------------
def load_run(Lx, Ly, Hmax, g2):
    fn = os.path.join(OUTDIR, "run_%s.npz" % tag_of(Lx, Ly, Hmax, g2))
    d = np.load(fn, allow_pickle=False)
    meta = json.loads(str(d["meta"]))
    return d, meta


def dist_dict(d, cut):
    cfg = d["cfg_" + cut]
    p = d["p_" + cut]
    return {tuple(int(v) for v in row): float(pp) for row, pp in zip(cfg, p)}


def fisher_entropy(Lx, Ly, Hmax, c, cut, pthresh=1e-13):
    """I(g2), S(g2), dS/dg2 at center c via the (c(1-eps), c, c(1+eps)) runs."""
    runs = [load_run(Lx, Ly, Hmax, g2)[0]
            for g2 in (c * (1 - EPS_REL), c, c * (1 + EPS_REL))]
    dm, d0, dp = [dist_dict(d, cut) for d in runs]
    support = set(d0) | set(dm) | set(dp)
    delta = c * EPS_REL
    I = 0.0
    excl = 0.0
    for cfgt in support:
        p0 = d0.get(cfgt, 0.0)
        pm = dm.get(cfgt, 0.0)
        pp = dp.get(cfgt, 0.0)
        if p0 < pthresh:
            excl += p0
            continue
        dpd = (pp - pm) / (2 * delta)
        I += dpd * dpd / p0
    def ent(dd):
        return -sum(p * np.log(p) for p in dd.values() if p > 0)
    S0 = ent(d0)
    dS = (ent(dp) - ent(dm)) / (2 * delta)
    return I, S0, dS, excl


def tv_distance(dd, cfg, probs):
    md = {tuple(int(v) for v in row): float(pp) for row, pp in zip(cfg, probs)}
    keys = set(dd) | set(md)
    return 0.5 * sum(abs(dd.get(k, 0.0) - md.get(k, 0.0)) for k in keys)


def rank_test(mats):
    """mats: list of dicts config->p over a g2 window. Returns s2/s1 of the
    double-centered log-prob matrix on the common well-supported configs."""
    common = set(mats[0])
    for m in mats[1:]:
        common &= set(m)
    common = [c for c in common if all(m[c] > 1e-9 for m in mats)]
    if len(common) < 3:
        return None, len(common)
    Y = np.array([[np.log(m[c]) for m in mats] for c in common])
    Y = Y - Y.mean(axis=0, keepdims=True)
    Y = Y - Y.mean(axis=1, keepdims=True)
    s = np.linalg.svd(Y, compute_uv=False)
    if s[0] < 1e-12:
        return 0.0, len(common)
    return float(s[1] / s[0]), len(common)


def cmd_analyze():
    res = {"seed": SEED,
           "hamiltonian": "H = (g2/2) sum E^2 - (1/g2) sum cos(theta_p)",
           "lattices": {}}

    # ---------------- 2x3 wide scan (A1 cut, Nb=4, m=3) ----------------
    res["lattices"]["2x3_H5"] = scan_lattice(2, 3, 5, CENTERS_23)
    # ---------------- 3x3 (A1,A2,A3 cuts) ----------------
    res["lattices"]["3x3_H2"] = scan_lattice(3, 3, 2, CENTERS_33)

    # truncation checks
    trunc = {}
    for (Lx, Ly, Hlo, Hhi, gs) in [(3, 3, 2, 3, [0.6, 1.0]),
                                   (2, 3, 5, 7, [0.4, 0.6])]:
        for g2 in gs:
            dlo, mlo = load_run(Lx, Ly, Hlo, g2)
            dhi, mhi = load_run(Lx, Ly, Hhi, g2)
            tv = tv_distance(dist_dict(dlo, "A1"),
                             dhi["cfg_A1"], dhi["p_A1"])
            trunc["%dx%d_g%.2f_H%d_vs_H%d" % (Lx, Ly, g2, Hlo, Hhi)] = {
                "TV_A1": tv, "dE0": mhi["E0"] - mlo["E0"]}
    res["truncation_checks"] = trunc
    with open("results_ed.json", "w") as f:
        json.dump(res, f, indent=1, default=float)
    print(json.dumps(res["summary"] if "summary" in res else
                     {k: "ok" for k in res["lattices"]}, indent=1))
    print("wrote results_ed.json")


def scan_lattice(Lx, Ly, Hmax, centers):
    out = {"centers": centers, "cuts": {}}
    for cut, region in cuts_for(Lx, Ly).items():
        Sub, Q, m, null_resid = model_for_cut(Lx, Ly, region)
        nb = Sub.shape[0]
        entry = {"Nb": nb, "m_rank": m, "null_resid": null_resid,
                 "points": []}
        # enumeration range for the model: adaptive
        for c in centers:
            I_ed, S_ed, dS_ed, excl = fisher_entropy(Lx, Ly, Hmax, c, cut)
            d0 = dist_dict(load_run(Lx, Ly, Hmax, c)[0], cut)
            sig2 = np.diag(Sub).max() / (2 * c)
            nmax = int(min(6, max(3, np.ceil(5 * np.sqrt(sig2)))))
            point = {"g2": c, "I_ED": I_ed, "S_ED": S_ed, "dSdg2_ED": dS_ed,
                     "excluded_prob": excl,
                     "identity_ratio": dS_ed / (-c * I_ed) if I_ed > 0 else None,
                     "I_continuum_m_law": m / (2 * c * c)}
            try:
                cfg = enumerate_hyperplane(nb, nmax)
                pm, T = model_distribution(Q, c, cfg)
                Tmean = float((pm * T).sum())
                VarT = float((pm * T * T).sum() - Tmean ** 2)
                Sm = float(-(pm[pm > 0] * np.log(pm[pm > 0])).sum())
                point.update({"TV_ED_vs_model": tv_distance(d0, cfg, pm),
                              "I_model": VarT, "S_model": Sm,
                              "nmax_model": nmax})
                # statistic correlation: T_weak vs T_strong = sum n^2
                Ts = (cfg.astype(float) ** 2).sum(axis=1)
                w = pm
                def corr(a, b, w):
                    am = (w * a).sum(); bm = (w * b).sum()
                    va = (w * (a - am) ** 2).sum()
                    vb = (w * (b - bm) ** 2).sum()
                    cv = (w * (a - am) * (b - bm)).sum()
                    return cv / np.sqrt(va * vb) if va > 0 and vb > 0 else None
                point["corr_Tweak_Tstrong_model"] = corr(T, Ts, w)
            except MemoryError:
                point["model"] = "enumeration too large"
            entry["points"].append(point)
        # exponential-family rank tests over windows
        mats = [dist_dict(load_run(Lx, Ly, Hmax, c)[0], cut) for c in centers]
        for name, sel in [("all", list(range(len(centers)))),
                          ("weak", list(range(min(3, len(centers))))),
                          ("strong", list(range(max(0, len(centers) - 3),
                                                len(centers))))]:
            r, ncfg = rank_test([mats[i] for i in sel])
            entry["rank_test_" + name] = {"s2_over_s1": r, "nconfigs": ncfg}
        # strong-coupling PT check: pattern with one excited cut plaquette
        entry["strong_coupling_check"] = strong_check(Lx, Ly, Hmax, centers,
                                                      cut)
        out["cuts"][cut] = entry
    # E-E covariance check at weakest center (A1)
    Sub, Q, m, _ = model_for_cut(Lx, Ly, cuts_for(Lx, Ly)["A1"])
    d0, _ = load_run(Lx, Ly, Hmax, centers[0])
    C_ed = d0["EEcov_A1"]
    C_model = Sub / (2 * centers[0])
    out["EEcov_check_A1_g%.2f" % centers[0]] = {
        "max_abs_diff": float(np.abs(C_ed - C_model).max()),
        "max_abs_model": float(np.abs(C_model).max())}
    return out


def strong_check(Lx, Ly, Hmax, centers, cut):
    """p(config)/p(0) vs PT prediction a^2 = 1/(16 g^8) for configs produced
    by a single plaquette flip touching the cut (those have sum n^2 = 2 and
    correspond to two cut links of one plaquette)."""
    checks = []
    for c in centers:
        if c < 2.5:
            continue
        d0 = dist_dict(load_run(Lx, Ly, Hmax, c)[0], cut)
        p0 = max(d0.values())
        # collect configs with sum n^2 == 2
        tot2 = [(k, v) for k, v in d0.items()
                if sum(x * x for x in k) == 2]
        if not tot2:
            continue
        # first-order PT: amplitude a = (hop)/(DeltaE) = (1/(2g2))/(2g2)
        # = 1/(4 g^4); leading sector probability ratio = a^2 = 1/(16 g^8).
        pred = 1.0 / (16.0 * c ** 4)  # c = g^2, so c^4 = g^8
        best = max(v for k, v in tot2)
        checks.append({"g2": c, "p_ratio_max_sumn2eq2": best / p0,
                       "PT_prediction": pred,
                       "ratio_to_PT": (best / p0) / pred})
    return checks


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return
    cmd = sys.argv[1]
    if cmd == "grid":
        done = 0
        for t in task_list():
            tag = tag_of(*t)
            ex = os.path.exists(os.path.join(OUTDIR, "run_%s.npz" % tag))
            done += ex
            print(("DONE " if ex else "TODO ") + tag)
        print("%d/%d complete" % (done, len(task_list())))
    elif cmd == "run":
        Lx, Ly, Hmax = int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
        g2 = float(sys.argv[5])
        budget = float(sys.argv[6]) if len(sys.argv) > 6 else 33.0
        do_run(Lx, Ly, Hmax, g2, budget)
    elif cmd == "auto":
        budget = float(sys.argv[2]) if len(sys.argv) > 2 else 38.0
        cmd_auto(budget)
    elif cmd == "analyze":
        cmd_analyze()
    else:
        print("unknown command")


if __name__ == "__main__":
    main()
