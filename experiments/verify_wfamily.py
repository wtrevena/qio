"""Numerical verification of the analytic weighted-W matching family (Lemma 2 of Paper 1).

For the weighted-W state psi = a|001> + b|010> + c|100> the single-qubit marginals are
diagonal, so S1 = h2(c^2), S2 = h2(b^2), S3 = h2(a^2) in closed form. Lemma 2 states
that for each gap parameter g in (0, g_max), with g_max the unique root of
    h2^{-1}(1 - r g) + h2^{-1}(1 - (1+r) g) = 1/2,
there is a unique s = s(g) in (g, 1 - r g) with
    h2^{-1}(s + r g) + h2^{-1}(s) + h2^{-1}(s - g) = 1     (normalization),
and the state with c^2 = h2^{-1}(s + r g), b^2 = h2^{-1}(s), a^2 = h2^{-1}(s - g)
satisfies r_S = (S1 - S2)/(S2 - S3) = r exactly, with tau_3 = 0 identically.

This script verifies the lemma against the same partial-trace machinery used by the
experiments (entropies computed from reduced density matrices of the explicit state,
not from the closed form), and cross-checks the curve against the stored grid solutions
of Experiment 2 (results/exp2_results.json).

Deterministic (no sampling). NumPy only. Run: python verify_wfamily.py
"""

import json
import os
import numpy as np

R_TARGET = 1.8174  # entropy-gap-ratio target r_SM used throughout the experiments


def h2(x):
    """Binary entropy (bits)."""
    if x <= 0.0 or x >= 1.0:
        return 0.0
    return float(-x * np.log2(x) - (1.0 - x) * np.log2(1.0 - x))


def bisect(f, lo, hi, iters=300):
    flo, fhi = f(lo), f(hi)
    assert flo * fhi <= 0, (lo, hi, flo, fhi)
    for _ in range(iters):
        mid = 0.5 * (lo + hi)
        fm = f(mid)
        if flo * fm <= 0:
            hi, fhi = mid, fm
        else:
            lo, flo = mid, fm
    return 0.5 * (lo + hi)


def h2inv(s):
    """Inverse of h2 on [0, 1/2]."""
    if s <= 0.0:
        return 0.0
    if s >= 1.0:
        return 0.5
    return bisect(lambda x: h2(x) - s, 1e-17, 0.5)


def g_max(r):
    return bisect(lambda g: h2inv(1 - r * g) + h2inv(1 - (1 + r) * g) - 0.5, 1e-9, 0.3)


def solve_s(g, r):
    """Unique s in (g, 1 - r g) with h2inv(s + r g) + h2inv(s) + h2inv(s - g) = 1."""
    phi = lambda s: h2inv(s + r * g) + h2inv(s) + h2inv(s - g) - 1.0
    return bisect(phi, g + 1e-13, 1 - r * g - 1e-13)


def family_weights(g, r):
    s = solve_s(g, r)
    return h2inv(s - g), h2inv(s), h2inv(s + r * g)  # a^2, b^2, c^2


def entropies_from_state(a, b, c):
    """Single-qubit entropies via partial trace of the explicit 8-dim state."""
    psi = np.zeros(8, complex)
    psi[0b001], psi[0b010], psi[0b100] = a, b, c
    T = psi.reshape(2, 2, 2)
    S = []
    for ax in range(3):
        M = np.moveaxis(T, ax, 0).reshape(2, 4)
        ev = np.linalg.eigvalsh(M @ M.conj().T)
        ev = ev[ev > 1e-15]
        S.append(float(-(ev * np.log2(ev)).sum()))
    return S


def main():
    r = R_TARGET
    gm = g_max(r)
    out = {"r_target": r, "g_max": gm, "family_checks": [], "exp2_crosschecks": []}
    print(f"g_max({r}) = {gm:.9f}")

    worst = 0.0
    for g in [0.005, 0.02, 0.04, 0.06, 0.0779, 0.082, 0.9999 * gm]:
        a2, b2, c2 = family_weights(g, r)
        S = entropies_from_state(np.sqrt(a2), np.sqrt(b2), np.sqrt(c2))
        r_S = (S[0] - S[1]) / (S[1] - S[2])
        worst = max(worst, abs(r_S - r))
        out["family_checks"].append(
            {"g": g, "a2": a2, "b2": b2, "c2": c2, "S": S, "r_S": r_S}
        )
        print(f"g={g:.7f}  (a2,b2,c2)=({a2:.7f},{b2:.7f},{c2:.7f})  "
              f"S1={S[0]:.7f}  r_S={r_S:.10f}")
    print(f"max |r_S - r| over family checks: {worst:.2e}")
    assert worst < 1e-9, "r_S deviates from target beyond tolerance"

    here = os.path.dirname(os.path.abspath(__file__))
    exp2_path = os.path.join(here, "results", "exp2_results.json")
    if os.path.exists(exp2_path):
        stored = json.load(open(exp2_path))["weighted_W"]["examples"]
        for ex in stored:
            g_ex = ex["S2"] - ex["S3"]
            a2, b2, c2 = family_weights(g_ex, r)
            diff = max(abs(a2 - ex["a2"]), abs(b2 - ex["b2"]), abs(c2 - ex["c2"]))
            out["exp2_crosschecks"].append({"g": g_ex, "max_weight_diff": diff})
            print(f"exp2 grid solution at g={g_ex:.6f}: max weight diff = {diff:.2e}")
            assert diff < 5e-6, "analytic curve does not reproduce stored grid solution"

    res_path = os.path.join(here, "results", "wfamily_verification.json")
    with open(res_path, "w") as f:
        json.dump(out, f, indent=2)
    print(f"PASS - results written to {res_path}")


if __name__ == "__main__":
    main()
