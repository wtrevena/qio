"""Theorem-level regression tests for the qio repository.

Each test re-checks, cheaply, a claim that one of the manuscripts states as a
theorem, lemma, identity, or convention.  The tests are deliberately much
lighter than the full reproduction scripts (see README.md for those); the
whole suite needs only python3 + numpy and runs in well under a minute.

Coverage:
  * CAR relations and the U(3) gauge action of the Jordan-Wigner toy
    (Papers 1-2; direction_A/alg_entanglement.py).
  * Commutant dimensions 4 / 6 / 20 for U(3) / SU(3) / U(1) (Paper 2).
  * BKOV entropy decomposition: the quantum piece vanishes identically for
    pure states of the 8-dimensional one-ideal toy ("all edge, no bulk",
    Paper 2).
  * The weighted-W matching-family identity r_S(g) = 1.8174 (Paper 1,
    Lemma 2; same logic as experiments/verify_wfamily.py), plus the stored
    Experiment 2 grid solutions.
  * 2d Yang-Mills identities dS/dt = -(t/4) Var(C2) and I(t) = Var(C2)/4,
    checked by finite differences for U(1) and SU(2) at t = 1 (Paper 3).
  * SU(3) quadratic-Casimir convention C2(fund) = 4/3 (Papers 3-4).
  * Two-ideal arena headline numbers (250 sectors, dim A' = 57062,
    28 invariant vectors) re-derived from the stored decomposition table
    (Paper 4; newwork/two_ideal/rep_checks.json -- stored JSON only, the
    32768-dimensional scripts are not rerun here).

Run from the repository root:

    python -m pytest tests/ -q      # preferred
    python tests/run_tests.py       # fallback when pytest is unavailable
"""
import json
import math
import os
import sys
from fractions import Fraction

import numpy as np

# ---------------------------------------------------------------------------
# Path setup (duplicated from conftest.py so this module also works under the
# fallback runner and under direct `python tests/test_theorems.py`).
# ---------------------------------------------------------------------------
TESTS_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(TESTS_DIR)
for _sub in ("direction_A", os.path.join("newwork", "two_ideal")):
    _p = os.path.join(REPO_ROOT, _sub)
    if _p not in sys.path:
        sys.path.insert(0, _p)

import alg_entanglement as ae  # noqa: E402  (direction_A, numpy-only)
import su3                     # noqa: E402  (newwork/two_ideal, exact integers)

SEED = 20260611
R_TARGET = 1.8174  # entropy-gap-ratio target r_SM used throughout Paper 1

# Cache for the (mildly) expensive commutant structures, shared across tests.
_CACHE = {}


def _commutant_structure(key, sampler, n_samples=32):
    if key not in _CACHE:
        rng = np.random.default_rng(SEED)
        gens = [ae.gauge_unitary(sampler(rng)) for _ in range(n_samples)]
        basis = ae.commutant(gens)
        struct = ae.algebra_structure(basis, seed=0)
        _CACHE[key] = (basis, struct)
    return _CACHE[key]


def _u3_struct():
    return _commutant_structure("U3", lambda rng: ae.haar_unitary(3, rng))


def _su3_struct():
    return _commutant_structure("SU3", lambda rng: ae.haar_su(3, rng))


def _u1_struct():
    return _commutant_structure(
        "U1",
        lambda rng: np.exp(1j * rng.uniform(0.0, 2.0 * np.pi)) * np.eye(3))


# ---------------------------------------------------------------------------
# 1. CAR relations (Papers 1-2)
# ---------------------------------------------------------------------------
def test_car_relations():
    """Jordan-Wigner modes satisfy {f_i, f_j^dag} = delta_ij, {f_i, f_j} = 0."""
    F = ae.jw_modes()
    I8 = np.eye(8)
    res = 0.0
    for i in range(3):
        for j in range(3):
            res = max(res, np.linalg.norm(
                F[i] @ F[j].conj().T + F[j].conj().T @ F[i] - I8 * (i == j)))
            res = max(res, np.linalg.norm(F[i] @ F[j] + F[j] @ F[i]))
    assert res < 1e-12


def test_gauge_action_is_a_representation():
    """G(U) is unitary and G(U)G(V) = G(UV) (number-conserving gauge action)."""
    rng = np.random.default_rng(SEED)
    I8 = np.eye(8)
    for _ in range(5):
        U, V = ae.haar_unitary(3, rng), ae.haar_unitary(3, rng)
        GU, GV = ae.gauge_unitary(U), ae.gauge_unitary(V)
        assert np.linalg.norm(GU @ GU.conj().T - I8) < 1e-10
        assert np.linalg.norm(GU @ GV - ae.gauge_unitary(U @ V)) < 1e-10


# ---------------------------------------------------------------------------
# 2. Commutant dimensions 4 / 6 / 20 (Paper 2, Theorem-level structure)
# ---------------------------------------------------------------------------
def test_commutant_dimension_u3():
    """U(3) gauge action: commutant = C^4 (abelian; charge projectors only)."""
    basis, struct = _u3_struct()
    assert len(basis) == 4
    assert struct["center_dim"] == 4
    assert all(b["n"] == 1 for b in struct["blocks"])
    assert sorted(b["m"] for b in struct["blocks"]) == [1, 1, 3, 3]


def test_commutant_dimension_su3():
    """SU(3) gauge action: commutant = M2 (+) C (+) C (dimension 6)."""
    basis, struct = _su3_struct()
    assert len(basis) == 6
    assert struct["center_dim"] == 3
    assert sorted((b["n"], b["m"]) for b in struct["blocks"]) == \
        [(1, 3), (1, 3), (2, 1)]


def test_commutant_dimension_u1():
    """U(1) gauge action: commutant = M1 (+) M3 (+) M3 (+) M1 (dimension 20)."""
    basis, struct = _u1_struct()
    assert len(basis) == 20
    assert struct["center_dim"] == 4
    assert sorted((b["n"], b["m"]) for b in struct["blocks"]) == \
        [(1, 1), (1, 1), (3, 1), (3, 1)]


# ---------------------------------------------------------------------------
# 3. Entropy decomposition: all edge, no bulk in the 8-dim toy (Paper 2)
# ---------------------------------------------------------------------------
def test_entropy_decomposition_quantum_piece_vanishes():
    """For Haar pure states of the one-ideal toy, the BKOV quantum piece is 0.

    The U(3)-invariant algebra is abelian (C^4), so S_alg(psi) = H({p_k})
    exactly: the gauge-invariant entanglement is purely classical (center /
    edge) data.  This is the structural fact behind Paper 2's no-go.
    """
    _, struct = _u3_struct()
    rng = np.random.default_rng(SEED + 1)
    for _ in range(20):
        psi = rng.normal(size=8) + 1j * rng.normal(size=8)
        psi /= np.linalg.norm(psi)
        ent = ae.algebraic_entropy(psi, struct)
        assert abs(ent["quantum"]) < 1e-9
        assert abs(ent["total"] - ent["center"]) < 1e-9
        # center piece = Shannon entropy of the 4 charge-sector probabilities
        assert abs(ent["center"] - ae.shannon_bits(np.array(ent["p"]))) < 1e-9


# ---------------------------------------------------------------------------
# 4. Weighted-W matching family: r_S(g) = 1.8174 (Paper 1, Lemma 2)
# ---------------------------------------------------------------------------
def _h2(x):
    """Binary entropy in bits."""
    if x <= 0.0 or x >= 1.0:
        return 0.0
    return float(-x * math.log2(x) - (1.0 - x) * math.log2(1.0 - x))


def _h2inv(y):
    """Inverse of the binary entropy on [0, 1/2] (bisection, numpy-free)."""
    lo, hi = 0.0, 0.5
    for _ in range(100):
        mid = 0.5 * (lo + hi)
        if _h2(mid) < y:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def _wfamily_state(g, r=R_TARGET):
    """Solve the Lemma-2 normalization for s(g) and build the weighted-W state."""
    def f(s):
        return _h2inv(s + r * g) + _h2inv(s) + _h2inv(s - g) - 1.0

    lo, hi = g + 1e-12, 1.0 - r * g - 1e-12
    assert f(lo) < 0.0 < f(hi)
    for _ in range(100):
        mid = 0.5 * (lo + hi)
        if f(mid) < 0.0:
            lo = mid
        else:
            hi = mid
    s = 0.5 * (lo + hi)
    c2, b2, a2 = _h2inv(s + r * g), _h2inv(s), _h2inv(s - g)
    psi = np.zeros(8)
    psi[1], psi[2], psi[4] = math.sqrt(a2), math.sqrt(b2), math.sqrt(c2)
    return psi / np.linalg.norm(psi)


def test_wfamily_identity_analytic():
    """r_S = (S1-S2)/(S2-S3) = 1.8174 exactly along the analytic family.

    Entropies are computed from reduced density matrices of the explicit
    state (partial-trace machinery), not from the closed form -- the same
    cross-check as experiments/verify_wfamily.py, on a 4-point g grid.
    """
    for g in (0.01, 0.03, 0.06, 0.08):
        psi = _wfamily_state(g)
        S1, S2, S3 = ae.single_qubit_entropies(psi)
        assert S1 > S2 > S3 > 0.0
        assert abs((S1 - S2) / (S2 - S3) - R_TARGET) < 1e-8


def test_wfamily_stored_grid_solutions():
    """Stored Experiment 2 grid solutions reproduce their S values and the ratio."""
    path = os.path.join(REPO_ROOT, "experiments", "results", "exp2_results.json")
    with open(path) as fh:
        examples = json.load(fh)["weighted_W"]["examples"]
    assert len(examples) >= 1
    for rec in examples:
        psi = np.zeros(8)
        psi[1] = math.sqrt(rec["a2"])
        psi[2] = math.sqrt(rec["b2"])
        psi[4] = math.sqrt(rec["c2"])
        psi /= np.linalg.norm(psi)
        S1, S2, S3 = ae.single_qubit_entropies(psi)
        assert abs(S1 - rec["S1"]) < 1e-9
        assert abs(S2 - rec["S2"]) < 1e-9
        assert abs(S3 - rec["S3"]) < 1e-9
        # grid solutions satisfy the identity to grid accuracy
        assert abs((S1 - S2) / (S2 - S3) - R_TARGET) < 1e-3


# ---------------------------------------------------------------------------
# 5. 2d Yang-Mills identities (Paper 3)
# ---------------------------------------------------------------------------
def _ym2_distribution(group, t):
    """Heat-kernel flux distribution p_R(t) = d_R^2 e^{-(t/2) C2(R)} / Z(t)."""
    if group == "U1":
        n = np.arange(-60, 61, dtype=float)
        d = np.ones_like(n)
        c2 = n ** 2
    elif group == "SU2":
        twoj = np.arange(0, 121, dtype=float)
        d = twoj + 1.0
        c2 = (twoj / 2.0) * (twoj / 2.0 + 1.0)
    else:
        raise ValueError(group)
    w = d ** 2 * np.exp(-(t / 2.0) * c2)
    return w / w.sum(), d, c2


def _ym2_entropy(group, t):
    """One-interval entropy S(t) = sum_R p_R [ -ln p_R + 2 ln d_R ]  (nats)."""
    p, d, _ = _ym2_distribution(group, t)
    nz = p > 0.0
    return float(np.sum(p[nz] * (-np.log(p[nz]) + 2.0 * np.log(d[nz]))))


def test_ym2_entropy_derivative_identity():
    """dS/dt = -(t/4) Var_t(C2), by central finite differences at t = 1."""
    t, h = 1.0, 1e-4
    for group in ("U1", "SU2"):
        p, _, c2 = _ym2_distribution(group, t)
        var = float(np.sum(p * c2 ** 2) - np.sum(p * c2) ** 2)
        lhs = (_ym2_entropy(group, t + h) - _ym2_entropy(group, t - h)) / (2 * h)
        rhs = -(t / 4.0) * var
        assert rhs < 0.0
        assert abs(lhs - rhs) < 1e-6 * max(1.0, abs(rhs))


def test_ym2_fisher_information_identity():
    """I(t) = E[(d ln p / dt)^2] = Var_t(C2)/4, by finite differences at t = 1."""
    t, h = 1.0, 1e-4
    for group in ("U1", "SU2"):
        p, _, c2 = _ym2_distribution(group, t)
        pp, _, _ = _ym2_distribution(group, t + h)
        pm, _, _ = _ym2_distribution(group, t - h)
        mask = (p > 1e-30) & (pp > 0.0) & (pm > 0.0)
        score = (np.log(pp[mask]) - np.log(pm[mask])) / (2 * h)
        fisher_fd = float(np.sum(p[mask] * score ** 2))
        var = float(np.sum(p * c2 ** 2) - np.sum(p * c2) ** 2)
        assert abs(fisher_fd - var / 4.0) < 1e-6 * max(1.0, var / 4.0)


# ---------------------------------------------------------------------------
# 6. SU(3) Casimir convention (Papers 3-4)
# ---------------------------------------------------------------------------
def test_su3_casimir_convention():
    """C2(fund) = 4/3, C2(adj) = 3 in the Tr(T_a T_b) = delta_ab/2 convention.

    Uses the exact-integer su(3) module shared by the two-ideal computation;
    this is the same normalization family as C2(j) = j(j+1) for SU(2) (whose
    fundamental gives 3/4), i.e. the convention used by ym2/ym2_su3.py.
    """
    su3.selftest()
    assert su3.c2(1, 0) == Fraction(4, 3)
    assert su3.c2(0, 1) == Fraction(4, 3)
    assert su3.c2(1, 1) == 3
    assert su3.weyl_dim(1, 0) == 3
    assert su3.weyl_dim(0, 1) == 3
    assert su3.weyl_dim(1, 1) == 8


# ---------------------------------------------------------------------------
# 7. Two-ideal arena headline numbers (Paper 4) -- stored JSON only
# ---------------------------------------------------------------------------
def test_two_ideal_headline_numbers():
    """250 sectors, dim A' = 57062, 28 invariant vectors, max multiplicity 52.

    Re-derived from the stored sector table (not just read back from the
    summary fields): sum m_i dim_i = 2^15, dim A' = sum m_i^2, invariant
    vectors = multiplicity of the trivial sector (a, b; 2j; y) = (0, 0; 0; 0).
    """
    path = os.path.join(REPO_ROOT, "newwork", "two_ideal", "rep_checks.json")
    with open(path) as fh:
        full = json.load(fh)["full"]
    assert full["n_modes"] == 15
    assert full["fock_dim"] == 32768
    assert full["n_sectors"] == 250
    assert full["dim_commutant"] == 57062
    assert full["n_invariant_vectors"] == 28
    assert full["max_multiplicity"] == 52
    assert full["z6_congruence_violations"] == 0

    table = full["table"]
    assert len(table) == 250
    assert sum(r["m"] * r["dim"] for r in table) == 32768
    assert sum(r["m"] ** 2 for r in table) == 57062
    trivial = [r for r in table
               if (r["a"], r["b"], r["twoj"], r["y"]) == (0, 0, 0, 0)]
    assert len(trivial) == 1 and trivial[0]["m"] == 28
    assert max(r["m"] for r in table) == 52
