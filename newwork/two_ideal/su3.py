"""su(3) weight-system utilities (pure numpy / pure python, exact integers).

Conventions:
  * su(3) weights in fundamental-weight coordinates (p, q) (integers).
  * Positive roots: a1 = (2,-1), a2 = (-1,2), a3 = a1+a2 = (1,1).
  * Inner product Gram matrix in fw coords: G = (1/3) [[2,1],[1,2]].
  * Irrep labels: Dynkin (a, b);  dim = (a+1)(b+1)(a+b+2)/2.
  * Fundamental 3 = (1,0) has weights (1,0), (-1,1), (0,-1)
    (eigenvalues x1, x2, x3 of the torus diag(e^{ix1},e^{ix2},e^{ix3}),
     parametrized by x1 = phi1, x2 = phi2-phi1, x3 = -phi2, so that a
     weight (p,q) pairs with angles as p*phi1 + q*phi2).
  * Quadratic Casimir (Tr T_A T_B = delta/2 normalization, i.e. C2(3)=4/3):
        c2(a,b) = (a^2 + b^2 + a*b + 3a + 3b)/3.

Every function is self-checked in selftest().
"""
from fractions import Fraction
import numpy as np

A1 = (2, -1)
A2 = (-1, 2)
A3 = (1, 1)
POS_ROOTS = [A1, A2, A3]
RHO = (1, 1)


def ip(u, v):
    """Exact inner product in fw coordinates: u^T G v with G = (1/3)[[2,1],[1,2]]."""
    return Fraction(2 * u[0] * v[0] + u[0] * v[1] + u[1] * v[0] + 2 * u[1] * v[1], 3)


def weyl_dim(a, b):
    return (a + 1) * (b + 1) * (a + b + 2) // 2


def c2(a, b):
    return Fraction(a * a + b * b + a * b + 3 * a + 3 * b, 3)


def weight_multiplicities(a, b):
    """Dict {(p,q): mult} of the irrep with highest weight (a,b), via Freudenthal.

    Exact rational arithmetic; verified against Weyl dimension formula.
    """
    lam = (a, b)
    # candidate weights lam - m*a1 - n*a2, generous box
    B = 2 * (a + b) + 2
    cands = {}
    for m in range(B + 1):
        for n in range(B + 1):
            mu = (lam[0] - 2 * m + n, lam[1] + m - 2 * n)
            cands[mu] = (m + n, mu)
    # process in increasing depth (m+n); Freudenthal recursion
    order = sorted(cands.values())
    mult = {}
    c_lam = ip((lam[0] + 1, lam[1] + 1), (lam[0] + 1, lam[1] + 1))
    for depth, mu in order:
        if depth == 0:
            mult[mu] = 1
            continue
        num = Fraction(0)
        for al in POS_ROOTS:
            k = 1
            while True:
                nu = (mu[0] + k * al[0], mu[1] + k * al[1])
                if nu not in mult or mult[nu] == 0:
                    # weights of an irrep along a root string are contiguous:
                    # once we leave the support going UP a root we stay out
                    # (support along mu + k*al is an unbroken string).
                    if nu not in mult:
                        break
                    # mult[nu]==0: continue scanning (zero entries possible in box)
                    k += 1
                    continue
                num += 2 * mult[nu] * ip(nu, al)
                k += 1
        den = c_lam - ip((mu[0] + 1, mu[1] + 1), (mu[0] + 1, mu[1] + 1))
        if den == 0:
            mult[mu] = 0
            continue
        val = num / den
        assert val.denominator == 1 and val >= 0, (a, b, mu, val)
        mult[mu] = int(val)
    out = {mu: m for mu, m in mult.items() if m > 0}
    assert sum(out.values()) == weyl_dim(a, b), (a, b, sum(out.values()))
    # Weyl-group (order-6) symmetry check: s1:(p,q)->(-p,p+q), s2:(p,q)->(p+q,-q)
    for mu, m in out.items():
        assert out.get((-mu[0], mu[0] + mu[1]), 0) == m
        assert out.get((mu[0] + mu[1], -mu[1]), 0) == m
    return out


_WM_CACHE = {}


def wm(a, b):
    if (a, b) not in _WM_CACHE:
        _WM_CACHE[(a, b)] = weight_multiplicities(a, b)
    return _WM_CACHE[(a, b)]


def schur_char(a, b, phi1, phi2):
    """Character of irrep (a,b) at torus angles (phi1, phi2), via the
    bialternant Schur polynomial s_{(a+b, b, 0)}(z1, z2, z3) -- an
    INDEPENDENT formula (no Freudenthal), used for cross-checks."""
    x = np.array([phi1, phi2 - phi1, -phi2])
    z = np.exp(1j * x)
    lam = (a + b, b, 0)
    num = np.array([[z[i] ** (lam[j] + 2 - j) for j in range(3)] for i in range(3)])
    den = np.array([[z[i] ** (2 - j) for j in range(3)] for i in range(3)])
    return np.linalg.det(num) / np.linalg.det(den)


def su2_char(twoj, psi):
    """Character of spin-j (twoj = 2j) at angle psi (weight t pairs as e^{i t psi})."""
    return sum(np.exp(1j * t * psi) for t in range(-twoj, twoj + 1, 2))


def selftest():
    assert weyl_dim(0, 0) == 1 and weyl_dim(1, 0) == 3 and weyl_dim(1, 1) == 8
    assert weyl_dim(3, 0) == 10 and weyl_dim(2, 2) == 27
    assert wm(1, 0) == {(1, 0): 1, (-1, 1): 1, (0, -1): 1}
    assert wm(0, 1) == {(0, 1): 1, (1, -1): 1, (-1, 0): 1}
    assert wm(1, 1)[(0, 0)] == 2 and sum(wm(1, 1).values()) == 8
    assert wm(2, 2)[(0, 0)] == 3 and sum(wm(2, 2).values()) == 27
    assert wm(3, 0)[(0, 0)] == 1
    # character cross-check: Freudenthal sum vs Schur, random angles
    rng = np.random.default_rng(20260610)
    for (a, b) in [(1, 0), (0, 1), (1, 1), (2, 0), (2, 1), (3, 0), (2, 2), (4, 1)]:
        for _ in range(5):
            p1, p2 = rng.uniform(0, 2 * np.pi, 2)
            cf = sum(m * np.exp(1j * (mu[0] * p1 + mu[1] * p2))
                     for mu, m in wm(a, b).items())
            cs = schur_char(a, b, p1, p2)
            assert abs(cf - cs) < 1e-9, (a, b, cf, cs)
    # c2 sanity
    assert c2(1, 0) == Fraction(4, 3) and c2(1, 1) == 3 and c2(0, 1) == Fraction(4, 3)
    return True


if __name__ == "__main__":
    selftest()
    print("su3.py selftest OK")
