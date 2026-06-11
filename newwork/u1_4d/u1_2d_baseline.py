#!/usr/bin/env python3
"""
Baseline: compact U(1) in 2d (the G = U(1) case of the YM2 result).

Flux distribution across a cut of the spatial circle, Hartle-Hawking state:
    p_n(t) = exp(-(t/2) n^2) / Z(t),   n in Z,   t = g^2 A.
This is the exactly known 2d anchor (Donnelly arXiv:1406.7304, eq. (pr) with
d_n = 1, C2 = n^2).  Everything the 4d computation is tested against:

  (i)  one-parameter exponential family, natural parameter theta = t/2,
       sufficient statistic T = n^2  (base measure uniform on Z);
  (ii) Fisher information I(t) = (1/4) Var_t(n^2);
  (iii) identity dS/dt = -t I(t)  (S = Shannon entropy of p, all edge);
  (iv) weak coupling: I(t) -> 1/(2 t^2)  == m/(2 theta'^2) with m = 1
       independent flux degree of freedom -- the "m law" that the 4d
       computation generalizes to m = (boundary links) - 1.

Deterministic; no RNG needed. Writes results_2d.json.
"""
import json
import math

NMAX_START = 40


def dist(t):
    """Return (ns, ps) for p_n ∝ exp(-t n^2 / 2), truncated adaptively."""
    nmax = NMAX_START
    while True:
        # relative weight at the edge
        if t * nmax * nmax / 2.0 > 750.0:
            break
        nmax *= 2
    ns = list(range(-nmax, nmax + 1))
    ws = [math.exp(-(t / 2.0) * n * n) for n in ns]
    Z = sum(ws)
    return ns, [w / Z for w in ws]


def moments(t):
    ns, ps = dist(t)
    m1 = sum(p * n * n for n, p in zip(ns, ps))
    m2 = sum(p * (n * n) ** 2 for n, p in zip(ns, ps))
    S = -sum(p * math.log(p) for p in ps if p > 0.0)
    return m1, m2 - m1 * m1, S


def main():
    out = {"description": "2d compact U(1) baseline: p_n = exp(-t n^2/2)/Z",
           "convention": "t = g^2 A; theta = t/2; T = n^2; I(t) = Var(n^2)/4",
           "grid": []}
    # grid of t values
    # t up to ~20 (same range as ym2/); beyond that S < 1e-9 and central
    # differences are pure roundoff noise
    ts = [0.05 * (1.25 ** k) for k in range(27)]
    max_id_resid = 0.0
    max_weak_resid = 0.0
    for t in ts:
        m1, var, S = moments(t)
        I_t = var / 4.0
        # identity check dS/dt = -t I(t) by central differences
        eps = 1e-5 * t
        _, _, Sp = moments(t + eps)
        _, _, Sm = moments(t - eps)
        dSdt = (Sp - Sm) / (2 * eps)
        resid = abs(dSdt + t * I_t) / max(abs(dSdt), 1e-30)
        max_id_resid = max(max_id_resid, resid)
        weak = I_t * 2 * t * t  # -> 1 as t -> 0  (m = 1 law)
        if t <= 0.2:
            max_weak_resid = max(max_weak_resid, abs(weak - 1.0))
        out["grid"].append({"t": t, "S": S, "I": I_t, "dSdt_fd": dSdt,
                            "identity_resid_rel": resid,
                            "I_times_2t2": weak})
    out["max_identity_residual_rel"] = max_id_resid
    out["max_weak_coupling_residual_t_le_0.2"] = max_weak_resid
    # assertions (claims of the report)
    assert max_id_resid < 1e-6, max_id_resid
    assert max_weak_resid < 0.05, max_weak_resid
    # I never scales with number of cuts in 2d: single global flux variable
    # (analytic; see paper3 Sec 3.5 -- restated here for the comparison table)
    out["fisher_area_scaling_2d"] = "I independent of number of cuts (one global flux variable); m = 1"
    with open("results_2d.json", "w") as f:
        json.dump(out, f, indent=1)
    msg = "2d baseline OK: max identity resid %.2e," % max_id_resid
    msg += " weak-coupling law resid %.2e" % max_weak_resid
    print(msg)


if __name__ == "__main__":
    main()
