#!/usr/bin/env python3
"""
Exact diagonalization of compact U(1) gauge theory on a 1xN plaquette strip in 2+1d,
in the dual integer-height representation (see DERIVATION.md, section D).

Model: heights h_1..h_N in Z (truncated |h| <= hmax), h_0 = h_{N+1} = 0,
    H = (e^2/2) * sum_{i=0..N} (h_{i+1}-h_i)^2  - (1/(2 e^2)) * sum_i (R_i + R_i^dag),
R_i : h_i -> h_i + 1.  This is the Kogut-Susskind Hamiltonian of compact U(1) on the
strip after solving Gauss's law (E_link = height difference across the link).

Entangling cut between plaquettes k=N//2 and k+1 cuts one bulk link; its electric flux
n = h_k - h_{k+1} is the center (superselection) label. We compute the ground state by
Lanczos (deterministic start vector, no RNG), the flux-sector distribution p(n), its
Shannon entropy, the height-bipartition entanglement entropy, and store everything in
results_chain.json (merged across stages).

Stages (each designed to fit a ~45 s budget):
    python3 u1_chain_ed.py grid     # N=6, hmax=2, 25-point geometric e^2 grid [0.3, 8]
    python3 u1_chain_ed.py fisher   # triplets e^2*(1, 1+d, 1-d) at 7 couplings, d=0.01
    python3 u1_chain_ed.py conv1    # convergence: N=6, hmax=1 and hmax=3 (8 couplings)
    python3 u1_chain_ed.py conv2    # convergence: N=4 and N=7 at hmax=2 (8 couplings)

Deterministic: no random numbers anywhere (SEED kept for provenance only).
"""
import sys, json, math, os
import numpy as np

SEED = 20260610  # provenance; algorithm is RNG-free
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results_chain.json")


def build_diag(N, hmax, e2):
    """Diagonal electric energy (e2/2) sum (dh)^2 as flat vector."""
    M = 2 * hmax + 1
    hvals = np.arange(-hmax, hmax + 1, dtype=np.float64)
    shape = (M,) * N
    E = np.zeros(shape)
    # boundary terms h_1^2 and h_N^2
    E += hvals.reshape((M,) + (1,) * (N - 1)) ** 2
    E += hvals.reshape((1,) * (N - 1) + (M,)) ** 2
    for i in range(N - 1):
        a = hvals.reshape((1,) * i + (M,) + (1,) * (N - 1 - i))
        b = hvals.reshape((1,) * (i + 1) + (M,) + (1,) * (N - 2 - i))
        E += (a - b) ** 2
    return 0.5 * e2 * E.ravel(), shape


def matvec_factory(N, hmax, e2):
    diag, shape = build_diag(N, hmax, e2)
    M = 2 * hmax + 1
    t = 1.0 / (2.0 * e2)

    def mv(v):
        w = diag * v
        x = v.reshape(shape)
        y = w.reshape(shape)
        for ax in range(N):
            sl_lo = [slice(None)] * N
            sl_hi = [slice(None)] * N
            sl_lo[ax] = slice(0, M - 1)
            sl_hi[ax] = slice(1, M)
            # raising: |h+1><h|  and lowering: |h><h+1|
            y[tuple(sl_hi)] -= t * x[tuple(sl_lo)]
            y[tuple(sl_lo)] -= t * x[tuple(sl_hi)]
        return w

    return mv, diag, shape


def lanczos_ground(N, hmax, e2, m=None):
    mv, diag, shape = matvec_factory(N, hmax, e2)
    dim = diag.size
    if m is None:
        m = 200 if dim <= 70000 else 140
    m = min(m, dim)
    # deterministic start: Boltzmann-weighted vector (good overlap at all couplings)
    v = np.exp(-(diag - diag.min()))
    v /= np.linalg.norm(v)
    V = np.empty((m, dim))
    alpha = np.zeros(m)
    beta = np.zeros(m)
    V[0] = v
    w = mv(v)
    alpha[0] = v @ w
    w -= alpha[0] * v
    used = m
    for j in range(1, m):
        # full reorthogonalization (twice for stability)
        for _ in range(2):
            w -= V[:j].T @ (V[:j] @ w)
        beta[j] = np.linalg.norm(w)
        if beta[j] < 1e-13:
            used = j
            break
        V[j] = w / beta[j]
        w = mv(V[j])
        alpha[j] = V[j] @ w
        w -= alpha[j] * V[j] + beta[j] * V[j - 1]
    a, b = alpha[:used], beta[1:used]
    T = np.diag(a) + np.diag(b, 1) + np.diag(b, -1)
    evals, evecs = np.linalg.eigh(T)
    gs = V[:used].T @ evecs[:, 0]
    gs /= np.linalg.norm(gs)
    Hgs = mv(gs)
    e0 = gs @ Hgs
    resid = float(np.linalg.norm(Hgs - e0 * gs))
    return gs, float(e0), resid, shape


def observables(gs, shape, N, hmax):
    M = 2 * hmax + 1
    k = N // 2  # cut between sites k and k+1 (1-indexed: sites 1..k | k+1..N)
    psi2 = (gs ** 2).reshape(shape)
    # joint of (h_k, h_{k+1}) -> axes k-1, k (0-indexed)
    axes = tuple(i for i in range(N) if i not in (k - 1, k))
    joint = psi2.sum(axis=axes)  # shape (M, M), rows h_k, cols h_{k+1}
    # p(n), n = h_k - h_{k+1} in [-2hmax, 2hmax]
    pn = np.zeros(4 * hmax + 1)
    for a in range(M):
        for b in range(M):
            n = (a - hmax) - (b - hmax)
            pn[n + 2 * hmax] += joint[a, b]
    pn = np.maximum(pn, 0.0)
    pn /= pn.sum()
    nz = pn > 0
    shannon = float(-(pn[nz] * np.log(pn[nz])).sum())
    # bipartite EE of heights 1..k vs rest
    mat = gs.reshape(M ** k, M ** (N - k))
    s = np.linalg.svd(mat, compute_uv=False)
    lam = s ** 2
    lam = lam[lam > 1e-16]
    ee = float(-(lam * np.log(lam)).sum())
    # joint 2-cut around middle site j=k: (h_{k-1}-h_k, h_k-h_{k+1})
    axes3 = tuple(i for i in range(N) if i not in (k - 2, k - 1, k))
    j3 = psi2.sum(axis=axes3)  # (h_{k-1}, h_k, h_{k+1})
    pj = np.zeros((4 * hmax + 1, 4 * hmax + 1))
    for a in range(M):
        for b in range(M):
            for c in range(M):
                pj[a - b + 2 * hmax, b - c + 2 * hmax] += j3[a, b, c]
    pj /= pj.sum()
    return pn, shannon, ee, pj


def run_point(N, hmax, e2):
    gs, e0, resid, shape = lanczos_ground(N, hmax, e2)
    pn, shannon, ee, pj = observables(gs, shape, N, hmax)
    return {
        "N": N, "hmax": hmax, "e2": e2, "E0": e0, "lanczos_resid": resid,
        "n_range": [-2 * hmax, 2 * hmax],
        "p_n": pn.tolist(), "shannon_pn": shannon, "ee_heights": ee,
        "p_joint_2cut": pj.tolist(),
    }


def load():
    if os.path.exists(OUT):
        with open(OUT) as f:
            return json.load(f)
    return {"seed": SEED, "model": "compact U(1) strip, dual height chain", "points": []}


def save(d):
    with open(OUT, "w") as f:
        json.dump(d, f)


def grid_e2():
    return list(np.geomspace(0.3, 8.0, 25))


def main():
    stage = sys.argv[1] if len(sys.argv) > 1 else "grid"
    data = load()

    def add(N, hmax, e2, tag):
        r = run_point(N, hmax, float(e2))
        r["tag"] = tag
        data["points"] = [p for p in data["points"] if not (
            p["N"] == N and p["hmax"] == hmax and abs(p["e2"] - e2) < 1e-12 and p["tag"] == tag)]
        data["points"].append(r)
        print(f"N={N} hmax={hmax} e2={e2:.5f} E0={r['E0']:.8f} resid={r['lanczos_resid']:.2e} "
              f"S_pn={r['shannon_pn']:.6f} tag={tag}", flush=True)

    if stage == "grid":
        for e2 in grid_e2():
            add(6, 2, e2, "grid")
    elif stage == "fisher":
        d = 0.01
        for e2 in [0.4, 0.7, 1.0, 1.5, 2.5, 4.0, 6.0]:
            for f in (1.0, 1.0 + d, 1.0 - d):
                add(6, 2, e2 * f, "fisher")
    elif stage == "conv1":
        for hm in (1, 3):
            for e2 in np.geomspace(0.3, 8.0, 8):
                add(6, hm, float(e2), "conv")
    elif stage == "conv2":
        for N in (4, 7):
            for e2 in np.geomspace(0.3, 8.0, 8):
                add(N, 2, float(e2), "conv")
    else:
        raise SystemExit(f"unknown stage {stage}")
    save(data)
    print(f"saved {len(data['points'])} points -> {OUT}")


if __name__ == "__main__":
    main()
