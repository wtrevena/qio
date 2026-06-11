#!/usr/bin/env python3
"""
weak_coupling_check.py -- Numerical verification of the weak-coupling
asymptotics derived in the appendix of paper 3:

  Z(t) = sum_R d_R^2 e^{-(t/2) C2(R)}  ~  vol(G) (2 pi t)^{-dim G / 2} e^{a t}
  S(t) = ln Z + (t/2)<C2>             ->  (dimG/2) ln(1/t) + c_G + o(1),
      c_G = ln vol(G) - (dimG/2) ln(2 pi) + dimG/2,
  with the e^{a t} factor cancelling EXACTLY in S (any Z = C t^{-d/2} e^{a t}
  gives S = ln C + d/2 - (d/2) ln t identically), and
  I(t) = Var_t(C2)/4 -> dimG/(2 t^2),  C(t) = t^2 I(t) -> dimG/2.

Closed-form constants (vol(G) in the metric in which the Laplacian eigenvalue
on irrep R equals the C2(R) used throughout, i.e. C2(j)=j(j+1) etc.):
  U(1):  vol = 2 pi               -> c = 1/2 + (1/2) ln 2pi      = 1.41893853
  SU(2): vol = 16 pi^2 (S^3, r=2) -> c = ln 16pi^2 - (3/2)ln 2pi + 3/2
                                                                 = 3.80535835
  SU(3): vol = 8 sqrt(3) (2pi)^5  -> c = ln(8 sqrt 3) + ln 2pi + 4
                                                                 = 8.46662475
The SU(2) volume is elementary (S^3 of radius 2: spec(-Lap) = l(l+2)/4 with
l = 2j gives j(j+1)); the SU(3) volume is checked here purely numerically.

Output: weak_coupling_check.json + console table. No randomness, no scipy.
"""

import json
import os

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
CUTOFF = 90.0   # relative weight e^{-90}: truncation ~ 1e-39, ample for 1e-10
SLACK = 60.0

DIM_G = {"U1": 1, "SU2": 3, "SU3": 8}

C_PRED = {
    "U1": 0.5 + 0.5 * np.log(2.0 * np.pi),
    "SU2": np.log(16.0 * np.pi**2) - 1.5 * np.log(2.0 * np.pi) + 1.5,
    "SU3": np.log(8.0 * np.sqrt(3.0)) + np.log(2.0 * np.pi) + 4.0,
}


def irrep_data(group, t):
    if group == "SU2":
        jmax = 0.5 * (np.sqrt(1.0 + 8.0 * (CUTOFF + SLACK) / t) - 1.0) + 2.0
        j = np.arange(0.0, jmax + 0.5, 0.5)
        return 2.0 * j + 1.0, j * (j + 1.0)
    if group == "U1":
        nmax = int(np.sqrt(2.0 * (CUTOFF + SLACK) / t)) + 2
        n = np.arange(-nmax, nmax + 1, dtype=float)
        return np.ones_like(n), n * n
    if group == "SU3":
        pmax = int(np.sqrt(6.0 * (CUTOFF + SLACK) / t)) + 2
        p, q = np.meshgrid(np.arange(pmax + 1, dtype=float),
                           np.arange(pmax + 1, dtype=float), indexing="ij")
        p, q = p.ravel(), q.ravel()
        d = (p + 1.0) * (q + 1.0) * (p + q + 2.0) / 2.0
        c2 = (p * p + q * q + p * q + 3.0 * p + 3.0 * q) / 3.0
        return d, c2
    raise ValueError(group)


def S_I_C(group, t):
    d, c2 = irrep_data(group, t)
    w = 2.0 * np.log(d) - 0.5 * t * c2
    wmax = w.max()
    ew = np.exp(w - wmax)
    Z = ew.sum()
    lnZ = wmax + np.log(Z)
    p = ew / Z
    m1 = float(p @ c2)
    var = float(p @ (c2 - m1) ** 2)
    S = lnZ + 0.5 * t * m1
    I = 0.25 * var
    return S, I, t * t * I


def main():
    rows = []
    t_grid = [0.001, 0.002, 0.005, 0.01, 0.02, 0.05, 0.1, 0.2]
    print(f"{'group':5s} {'t':>7s} {'S+(d/2)ln t':>12s} {'c_pred':>10s} "
          f"{'c-c_pred':>10s} {'2t^2 I/d - 1':>12s} {'C(t)':>10s}")
    for group in ["U1", "SU2", "SU3"]:
        dG = DIM_G[group]
        cpred = float(C_PRED[group])
        for t in t_grid:
            S, I, C = S_I_C(group, t)
            c_num = S + 0.5 * dG * np.log(t)
            rel_I = 2.0 * t * t * I / dG - 1.0
            rows.append({
                "group": group, "t": t,
                "c_numeric": float(c_num), "c_predicted": cpred,
                "c_deviation": float(c_num - cpred),
                "I_rel_dev_from_dG_over_2t2": float(rel_I),
                "capacity": float(C),
            })
            print(f"{group:5s} {t:7.3f} {c_num:12.8f} {cpred:10.6f} "
                  f"{c_num - cpred:10.2e} {rel_I:12.2e} {C:10.6f}")
    with open(os.path.join(HERE, "weak_coupling_check.json"), "w") as f:
        json.dump({"meta": {"date": "2026-06-10",
                            "c_formula": "c_G = ln vol(G) - (dG/2) ln 2pi + dG/2",
                            "volumes": {"U1": "2 pi", "SU2": "16 pi^2",
                                        "SU3": "8 sqrt(3) (2 pi)^5"}},
                   "rows": rows}, f, indent=1)
    print("-> weak_coupling_check.json")


if __name__ == "__main__":
    main()
# end of file (padding line against mount truncation)
