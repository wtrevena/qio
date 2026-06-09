"""Shared library for QIO computational experiments.

Conventions:
  - Three-qubit pure states psi in C^2 x C^2 x C^2, amplitudes a_{ijk},
    flattened index = 4i + 2j + k (qubit 1 = leftmost factor).
  - Qubit-gauge assignment (Szangolies): qubit 1 <-> SU(3), qubit 2 <-> SU(2),
    qubit 3 <-> U(1). Entropy ordering requirement: S1 > S2 > S3.
  - r_S = (S1 - S2) / (S2 - S3); SM target r_SM(M_Z) = 1.8174.
"""
import numpy as np

# ---------- Standard Model target ----------
ALPHA = np.array([0.1179, 0.03374, 0.01695])  # alpha_3, alpha_2, alpha_1 at M_Z (PDG 2022)
LOGINV = np.log(1.0 / ALPHA)
R_SM = (LOGINV[0] - LOGINV[1]) / (LOGINV[1] - LOGINV[2])  # = 1.8174

# ---------- State generation ----------
def haar_states(n, nq=3, rng=None):
    """n Haar-random pure states on nq qubits, shape (n, 2**nq)."""
    rng = rng or np.random.default_rng()
    d = 2 ** nq
    z = rng.standard_normal((n, d)) + 1j * rng.standard_normal((n, d))
    return z / np.linalg.norm(z, axis=1, keepdims=True)

# ---------- Entropies ----------
def _h(p):
    """Shannon entropy (base 2) of eigenvalue array along last axis."""
    p = np.clip(p.real, 1e-15, 1.0)
    return -(p * np.log2(p)).sum(axis=-1)

def single_qubit_entropies(psi, nq=3):
    """Von Neumann entropies of each single-qubit marginal. psi: (n, 2**nq).
    Returns (n, nq) array, column k = entropy of qubit k+1."""
    n = psi.shape[0]
    t = psi.reshape((n,) + (2,) * nq)
    out = np.empty((n, nq))
    for k in range(nq):
        # move qubit k to front, flatten rest
        perm = (0, k + 1) + tuple(i for i in range(1, nq + 1) if i != k + 1)
        m = np.transpose(t, perm).reshape(n, 2, 2 ** (nq - 1))
        rho = np.einsum('nia,nja->nij', m, m.conj())
        ev = np.linalg.eigvalsh(rho)
        out[:, k] = _h(ev)
    return out

def gap_ratio(S):
    """r_S = (S1-S2)/(S2-S3) for (n,3) entropy array."""
    return (S[:, 0] - S[:, 1]) / (S[:, 1] - S[:, 2])

# ---------- Binary entropy inverse ----------
def h2(x):
    x = np.clip(x, 1e-15, 1 - 1e-15)
    return -(x * np.log2(x) + (1 - x) * np.log2(1 - x))

def h2inv(S):
    """Inverse of binary entropy on [0, 1/2] (scalar or array, bisection)."""
    S = np.atleast_1d(np.asarray(S, float))
    lo, hi = np.zeros_like(S), np.full_like(S, 0.5)
    for _ in range(80):
        mid = 0.5 * (lo + hi)
        m = h2(mid) < S
        lo[m] = mid[m]
        hi[~m] = mid[~m]
    r = 0.5 * (lo + hi)
    return r if r.size > 1 else float(r[0])

# ---------- Entanglement invariants (3 qubits) ----------
def three_tangle(psi):
    """tau_3 = 4 |Det(psi)| (Cayley hyperdeterminant). psi: (n, 8)."""
    a = psi  # a[:, 4i+2j+k]
    a000, a001, a010, a011, a100, a101, a110, a111 = (a[:, i] for i in range(8))
    d1 = (a000 * a111) ** 2 + (a001 * a110) ** 2 + (a010 * a101) ** 2 + (a100 * a011) ** 2
    d2 = (a000 * a111 * a011 * a100 + a000 * a111 * a101 * a010
          + a000 * a111 * a110 * a001 + a011 * a100 * a101 * a010
          + a011 * a100 * a110 * a001 + a101 * a010 * a110 * a001)
    d3 = a000 * a110 * a101 * a011 + a111 * a001 * a010 * a100
    det = d1 - 2 * d2 + 4 * d3
    return 4 * np.abs(det)

_SY = np.array([[0, -1j], [1j, 0]])
_SYY = np.kron(_SY, _SY)

def concurrence_pairs(psi):
    """Wootters concurrences C12, C13, C23 for each 3-qubit pure state.
    psi: (n, 8). Returns (n, 3). Loop-based; use on modest n."""
    n = psi.shape[0]
    out = np.empty((n, 3))
    t = psi.reshape(n, 2, 2, 2)
    pairs = [((0, 1), 2), ((0, 2), 1), ((1, 2), 0)]
    for col, (keep, tr) in enumerate(pairs):
        axes = (1 + keep[0], 1 + keep[1], 1 + tr)
        m = np.transpose(t, (0,) + axes).reshape(n, 4, 2)
        rho = np.einsum('nia,nja->nij', m, m.conj())
        rt = rho @ _SYY @ rho.conj() @ _SYY
        ev = np.linalg.eigvals(rt)
        s = np.sqrt(np.clip(np.sort(ev.real, axis=1)[:, ::-1], 0, None))
        out[:, col] = np.maximum(0, s[:, 0] - s[:, 1] - s[:, 2] - s[:, 3])
    return out

def matching_filter(S, target=R_SM, tol=0.01):
    """Boolean mask: ordered S1>S2>S3 and |r_S - target| < tol."""
    ordered = (S[:, 0] > S[:, 1]) & (S[:, 1] > S[:, 2])
    r = np.full(S.shape[0], np.nan)
    r[ordered] = gap_ratio(S[ordered])
    return ordered & (np.abs(r - target) < tol), r
