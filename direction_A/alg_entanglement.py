"""Algebraic (gauge-invariant) entanglement on finite-dimensional Hilbert spaces.

Direction A library. Implements, with machine verification at every step:

  * the numerical commutant of a set of unitaries
        A = {X in M_d(C) : [X, G] = 0 for all sampled G},
    found as the nullspace of the linear map X -> ([X, G_s])_s;

  * Wedderburn structure identification of a finite-dimensional *-algebra,
        A  ~=  (+)_k  M_{n_k}(C) (x) 1_{m_k},
    via the center (minimal central projections P_k) and per-block ranks;

  * the trace-preserving conditional expectation E_A (= Hilbert-Schmidt
    orthogonal projection onto span(A), which is the unique trace-preserving
    conditional expectation onto a unital *-subalgebra);

  * the algebraic entanglement entropy (BKOV / Casini-Huerta form), in bits:
        S_A(rho) = H({p_k})  +  sum_k p_k S(rho_k)
    where p_k = Tr(P_k rho) and rho_k is the n_k x n_k reduced block state
    (multiplicity factor traced out).  H({p_k}) is the CLASSICAL (center)
    piece; sum_k p_k S(rho_k) is the QUANTUM piece.

  NOTE (common pitfall, machine-cross-checked here): S_A is the von Neumann
  entropy of the block state (+)_k p_k rho_k on (+)_k C^{n_k}.  It is NOT the
  entropy of the d x d matrix E_A(rho); the two differ by sum_k p_k log2 m_k.

  * the Jordan-Wigner gauge action: for U in U(3) acting on the three
    fermionic modes f_1 = sm x I x I, f_2 = Z x sm x I, f_3 = Z x Z x sm
    (sm = [[0,1],[0,0]]), the induced number-conserving unitary G(U) on C^8:
    trivial on weight 0, fundamental U on weight 1, antisymmetric square
    Lambda^2 U on weight 2, det(U) on weight 3.

References:
  H. Barnum, E. Knill, G. Ortiz, L. Viola, PRL 92, 107902 (2004)  [BKOV]
  P. Zanardi, PRL 87, 077901 (2001)
  H. Casini, M. Huerta, J.A. Rosabal, PRD 89, 085012 (2014)  [algebraic def.,
      gauge fields, center = classical term]
  W. Donnelly, Class. Quantum Grav. 31, 214003 (2014)  [edge modes / lattice
      gauge reading of the center term]
"""
import numpy as np

# --------------------------------------------------------------------------
# linear algebra helpers
# --------------------------------------------------------------------------

def _vec(M):
    """Column-major vectorization (so vec(AXB) = (B^T kron A) vec(X))."""
    return np.asarray(M).flatten(order='F')


def _unvec(v, d):
    return np.asarray(v).reshape(d, d, order='F')


def nullspace_basis(K, tol=1e-9):
    """Orthonormal basis (as rows) of the right nullspace of K."""
    _, s, vh = np.linalg.svd(K, full_matrices=True)
    s_full = np.zeros(K.shape[1])
    s_full[:len(s)] = s
    return vh[s_full < tol].conj()


def hs_inner(A, B):
    """Hilbert-Schmidt inner product <A, B> = Tr(A^dag B)."""
    return np.trace(A.conj().T @ B)


def project_onto_span(X, basis):
    """HS-orthogonal projection of X onto span(basis), basis HS-orthonormal."""
    return sum(B * hs_inner(B, X) for B in basis)


# --------------------------------------------------------------------------
# commutant
# --------------------------------------------------------------------------

def commutant(unitaries, tol=1e-9):
    """HS-orthonormal basis of {X : [X, G] = 0 for all G in unitaries}.

    Vectorized: [X, G] = 0  <=>  (I kron G - G^T kron I) vec(X) = 0.
    Returns a list of d x d matrices (HS-orthonormal).
    """
    d = unitaries[0].shape[0]
    I = np.eye(d)
    K = np.vstack([np.kron(I, np.asarray(G, complex)) - np.kron(np.asarray(G, complex).T, I)
                   for G in unitaries])
    return [_unvec(c, d) for c in nullspace_basis(K, tol)]


def verify_star_algebra(basis, tol=1e-8):
    """Check span(basis) is a unital *-algebra. Returns max residual."""
    d = basis[0].shape[0]
    res = np.linalg.norm(project_onto_span(np.eye(d), basis) - np.eye(d))
    for A in basis:
        Ad = A.conj().T
        res = max(res, np.linalg.norm(project_onto_span(Ad, basis) - Ad))
        for B in basis:
            P = A @ B
            res = max(res, np.linalg.norm(project_onto_span(P, basis) - P))
    return float(res)


def max_commutator_residual(basis, unitaries):
    """max_s max_i || [B_i, G_s] ||_F  -- certifies commutant on fresh samples."""
    r = 0.0
    for G in unitaries:
        for B in basis:
            r = max(r, np.linalg.norm(B @ G - G @ B))
    return float(r)


# --------------------------------------------------------------------------
# Wedderburn structure
# --------------------------------------------------------------------------

def algebra_structure(basis, tol=1e-7, seed=0):
    """Identify A ~= (+)_k M_{n_k} (x) 1_{m_k} from an HS-orthonormal basis.

    Returns dict with keys:
      'basis'      : the input basis (HS-orthonormal),
      'center_dim' : dim of the center,
      'blocks'     : list of dicts {P, n, m, dim, weights} sorted by support;
                     P = minimal central projection, dim = rank(P) = n*m.
    """
    d = basis[0].shape[0]
    nb = len(basis)
    # ---- center: X = sum_j c_j B_j with [X, B_i] = 0 for all i ----
    cols = []
    for Bj in basis:
        cols.append(np.concatenate([_vec(Bj @ Bi - Bi @ Bj) for Bi in basis]))
    K = np.array(cols).T            # (nb*d^2, nb)
    cvecs = nullspace_basis(K, tol)
    center = [sum(c[j] * basis[j] for j in range(nb)) for c in cvecs]
    zdim = len(center)
    # ---- minimal central projections from a random Hermitian central element
    rng = np.random.default_rng(seed)
    clusters = None
    for _ in range(50):
        coef = rng.standard_normal(zdim) + 1j * rng.standard_normal(zdim)
        Zel = sum(c * C for c, C in zip(coef, center))
        Zel = Zel + Zel.conj().T
        w, V = np.linalg.eigh(Zel)
        spread = (w[-1] - w[0]) + 1.0
        groups, cur = [], [0]
        for i in range(1, d):
            if w[i] - w[i - 1] > 1e-6 * spread:
                groups.append(cur)
                cur = []
            cur.append(i)
        groups.append(cur)
        if len(groups) == zdim:
            clusters = [(V[:, idx], idx) for idx in groups]
            break
    if clusters is None:
        raise RuntimeError("could not separate central spectrum into "
                           f"{zdim} clusters")
    blocks = []
    for Vk, _ in clusters:
        P = Vk @ Vk.conj().T
        dk = int(round(np.trace(P).real))
        # rank of {P B P : B in basis} = n_k^2
        M = np.array([_vec(P @ B @ P) for B in basis])
        s = np.linalg.svd(M, compute_uv=False)
        rank = int((s > tol).sum())
        nk = int(round(np.sqrt(rank)))
        if nk * nk != rank or dk % nk != 0:
            raise RuntimeError(f"block structure inconsistent: rank={rank}, dk={dk}")
        mk = dk // nk
        # weight content of the block support (diagnostic, 3-qubit specific)
        wts = sorted({bin(i).count('1') for i in range(d)
                      if abs(P[i, i]) > 1e-9}) if d == 8 else None
        blocks.append(dict(P=P, n=nk, m=mk, dim=dk, weights=wts))
    blocks.sort(key=lambda b: (min(b['weights']) if b['weights'] else 0))
    return dict(basis=basis, center_dim=zdim, blocks=blocks)


def structure_string(struct):
    """e.g. 'M2(x)1_1 (+) M1(x)1_3 (+) M1(x)1_3' with weight labels."""
    parts = []
    for b in struct['blocks']:
        parts.append(f"M{b['n']}(x)1_{b['m']}[weights {b['weights']}]")
    return " (+) ".join(parts)


# --------------------------------------------------------------------------
# conditional expectation and algebraic entropy
# --------------------------------------------------------------------------

def cond_expectation(rho, basis):
    """Trace-preserving conditional expectation = HS projection onto span(A)."""
    return project_onto_span(rho, basis)


def algebraic_entropy(state, struct, tol=1e-12):
    """BKOV / Casini-Huerta algebraic entanglement entropy, in bits.

    state: pure-state vector (1d) or density matrix (2d).
    Returns dict: p (sector probabilities, ordered as struct['blocks']),
                  center  = H({p_k})              (classical piece),
                  quantum = sum_k p_k S(rho_k)    (quantum piece),
                  total   = center + quantum.
    Internally cross-checked against S(E_A(rho)) - sum_k p_k log2 m_k.
    """
    psi = np.asarray(state, complex)
    rho = np.outer(psi, psi.conj()) if psi.ndim == 1 else psi
    E = cond_expectation(rho, struct['basis'])
    ps, qs = [], []
    for blk in struct['blocks']:
        P, m = blk['P'], blk['m']
        p = float(np.real(np.trace(P @ rho)))
        p = max(p, 0.0)
        ps.append(p)
        if p < tol:
            qs.append(0.0)
            continue
        # eigenvalues of E restricted to the block: each eigenvalue of
        # (p_k/m_k) rho_k repeated m_k times
        mu = np.linalg.eigvalsh(P @ E @ P)
        mu = mu[mu > tol]
        s_block = float(-np.sum(mu * np.log2(mu)))
        qs.append(s_block + p * np.log2(p / m))   # = p_k S(rho_k)
    ps, qs = np.array(ps), np.array(qs)
    pn = ps[ps > tol]
    center = float(-np.sum(pn * np.log2(pn)))
    quantum = float(np.sum(qs))
    total = center + quantum
    # ---- independent cross-check ----
    ev = np.linalg.eigvalsh(E)
    ev = ev[ev > tol]
    alt = float(-np.sum(ev * np.log2(ev))
                - sum(p * np.log2(b['m']) for p, b in zip(ps, struct['blocks'])
                      if p > tol))
    if abs(total - alt) > 1e-8:
        raise RuntimeError(f"entropy cross-check failed: {total} vs {alt}")
    return dict(p=ps.tolist(), center=center, quantum=quantum, total=total)


# --------------------------------------------------------------------------
# Jordan-Wigner setup and the gauge action G(U)
# --------------------------------------------------------------------------

I2 = np.eye(2, dtype=complex)
Z2 = np.diag([1.0, -1.0]).astype(complex)
SM = np.array([[0, 1], [0, 0]], complex)        # sigma^-


def kron3(a, b, c):
    return np.kron(np.kron(a, b), c)


def jw_modes():
    """f_1 = sm x I x I, f_2 = Z x sm x I, f_3 = Z x Z x sm."""
    return [kron3(SM, I2, I2), kron3(Z2, SM, I2), kron3(Z2, Z2, SM)]


WEIGHT = np.array([bin(i).count('1') for i in range(8)])
W1_IDX = [4, 2, 1]                  # f_a^dag |0> for a = 1,2,3
W2_PAIRS = [(0, 1), (0, 2), (1, 2)]
W2_IDX = [6, 5, 3]                  # f_i^dag f_j^dag |0>, pairs as above


def gauge_unitary(U):
    """Fock-space (number-conserving) implementation G(U) of the mode
    rotation, with G(U) f_b^dag G(U)^dag = sum_a U[a,b] f_a^dag.

    Weight 0: 1.  Weight 1: U.  Weight 2: Lambda^2 U.  Weight 3: det U.
    U(1) subgroup: G(e^{i theta} 1) = e^{i theta N} (N = number operator).
    """
    U = np.asarray(U, complex)
    G = np.zeros((8, 8), complex)
    G[0, 0] = 1.0
    G[7, 7] = np.linalg.det(U)
    for a in range(3):
        for b in range(3):
            G[W1_IDX[a], W1_IDX[b]] = U[a, b]
    for A, (i, j) in enumerate(W2_PAIRS):
        for B, (k, l) in enumerate(W2_PAIRS):
            G[W2_IDX[A], W2_IDX[B]] = U[i, k] * U[j, l] - U[i, l] * U[j, k]
    return G


def haar_unitary(n, rng):
    """Haar-random U(n) via QR with phase fix."""
    z = rng.standard_normal((n, n)) + 1j * rng.standard_normal((n, n))
    q, r = np.linalg.qr(z)
    return q * (np.diagonal(r) / np.abs(np.diagonal(r)))


def haar_su(n, rng):
    """Haar-random SU(n): Haar U(n) divided by an n-th root of its det."""
    U = haar_unitary(n, rng)
    return U / np.linalg.det(U) ** (1.0 / n)


# --------------------------------------------------------------------------
# small utilities for the run script
# --------------------------------------------------------------------------

def single_qubit_entropies(psi):
    """Von Neumann entropies (bits) of the three single-qubit marginals."""
    t = np.asarray(psi, complex).reshape(2, 2, 2)
    out = []
    for k in range(3):
        m = np.moveaxis(t, k, 0).reshape(2, 4)
        rho = m @ m.conj().T
        ev = np.linalg.eigvalsh(rho)
        ev = ev[ev > 1e-15]
        out.append(float(-np.sum(ev * np.log2(ev))))
    return np.array(out)


def sector_probs(psi):
    """(p0, p1, p2, p3): |amplitude|^2 summed per Hamming-weight sector."""
    a2 = np.abs(np.asarray(psi, complex)) ** 2
    return np.array([a2[WEIGHT == w].sum() for w in range(4)])


def shannon_bits(p, tol=1e-15):
    p = np.asarray(p, float)
    p = p[p > tol]
    return float(-np.sum(p * np.log2(p)))
