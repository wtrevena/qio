"""Fock-space machinery for the one-generation chiral model, exploiting the
species tensor factorization

    F = F_Q (x) F_L (x) F_u (x) F_d (x) F_e   (64*4*8*8*2 = 32768),

which is sign-safe because every gauge generator is an even (quadratic,
species-block-diagonal) operator and every gauge unitary is a plain tensor
product of per-species second quantizations.

Key trick for the commutant decomposition: all Casimirs commute with the
torus AND with the five species-number operators, so the whole problem
block-diagonalizes over keys (n_Q,n_L,n_u,n_d,n_e, p,q,t) -- 12916 blocks of
size <= 30 for the full space.  Within each block the matrix elements of
C2(su3), C2(su2), C3(su3) are assembled exactly from species-local small
matrices.
"""
import numpy as np

import su3 as su3mod
import model

# ---------------------------------------------------------------------------
# species layout
# ---------------------------------------------------------------------------
SP_ORDER = ['Q', 'L', 'u', 'd', 'e']           # bit ranges, low to high
SP_NMODES = dict(Q=6, L=2, u=3, d=3, e=1)
SP_DIM = {s: 1 << n for s, n in SP_NMODES.items()}
COLORED = ['Q', 'u', 'd']
DOUBLET = ['Q', 'L']

def gell_mann():
    l = np.zeros((8, 3, 3), complex)
    l[0][0, 1] = l[0][1, 0] = 1
    l[1][0, 1] = -1j; l[1][1, 0] = 1j
    l[2][0, 0] = 1; l[2][1, 1] = -1
    l[3][0, 2] = l[3][2, 0] = 1
    l[4][0, 2] = -1j; l[4][2, 0] = 1j
    l[5][1, 2] = l[5][2, 1] = 1
    l[6][1, 2] = -1j; l[6][2, 1] = 1j
    l[7] = np.diag([1, 1, -2]) / np.sqrt(3)
    return l

LAM = gell_mann()
SIG = np.array([[[0, 1], [1, 0]], [[0, -1j], [1j, 0]], [[1, 0], [0, -1]]])

def d_symbols():
    T = LAM / 2
    d = np.zeros((8, 8, 8))
    for a in range(8):
        for b in range(8):
            anti = T[a] @ T[b] + T[b] @ T[a]
            for c in range(8):
                d[a, b, c] = 2 * np.real(np.trace(anti @ T[c]))
    return d

DSYM = d_symbols()

# generators: 0..7 su3, 8..10 su2, 11 = Y (=y/6)
def gen_coeff(species, g):
    n = SP_NMODES[species]
    if g < 8:
        if species == 'Q':
            return np.kron(LAM[g] / 2, np.eye(2))
        if species in ('u', 'd'):
            return LAM[g] / 2
        return np.zeros((n, n), complex)
    if g < 11:
        a = g - 8
        if species == 'Q':
            return np.kron(np.eye(3), SIG[a] / 2)
        if species == 'L':
            return SIG[a] / 2
        return np.zeros((n, n), complex)
    yv = dict(Q=1, L=-3, u=4, d=-2, e=-6)[species]
    return (yv / 6.0) * np.eye(n, dtype=complex)

# su3 lowering ops in mode space: E_{-a1}: c0->c1, E_{-a2}: c1->c2 ; su2 J-
def lower_coeff(species, which):
    n = SP_NMODES[species]
    T = np.zeros((n, n), complex)
    if which == 'f1' and species == 'Q':
        T[2 + 0, 0 + 0] = 1; T[2 + 1, 0 + 1] = 1
    elif which == 'f1' and species in ('u', 'd'):
        T[1, 0] = 1
    elif which == 'f2' and species == 'Q':
        T[4 + 0, 2 + 0] = 1; T[4 + 1, 2 + 1] = 1
    elif which == 'f2' and species in ('u', 'd'):
        T[2, 1] = 1
    elif which == 'jm' and species == 'Q':
        for c in range(3):
            T[2 * c + 1, 2 * c] = 1
    elif which == 'jm' and species == 'L':
        T[1, 0] = 1
    return T

# ---------------------------------------------------------------------------
# species-local second quantization
# ---------------------------------------------------------------------------

def local_aops(n):
    """Annihilation matrices a_k on C^{2^n}, |S> = f+_{s1<...<sk}|0>, bit k = mode k."""
    d = 1 << n
    ops = []
    for k in range(n):
        A = np.zeros((d, d))
        for s in range(d):
            if (s >> k) & 1:
                sgn = (-1) ** bin(s & ((1 << k) - 1)).count('1')
                A[s ^ (1 << k), s] = sgn
        ops.append(A)
    return ops

_AOPS = {sp: local_aops(SP_NMODES[sp]) for sp in SP_ORDER}


def onebody(species, T):
    a = _AOPS[species]
    n = SP_NMODES[species]
    O = np.zeros((SP_DIM[species], SP_DIM[species]), complex)
    for i in range(n):
        for j in range(n):
            if abs(T[i, j]) > 1e-15:
                O += T[i, j] * (a[i].T @ a[j])
    return O


X = {sp: [onebody(sp, gen_coeff(sp, g)) for g in range(12)] for sp in SP_ORDER}
XLOW = {sp: {w: onebody(sp, lower_coeff(sp, w)) for w in ('f1', 'f2', 'jm')}
        for sp in SP_ORDER}


_GAMMA_STRUCT = {}

def _gamma_struct(n):
    """Per particle number k: (masks, rows) with rows[i] = sorted mode list."""
    if n not in _GAMMA_STRUCT:
        by = {}
        for s in range(1 << n):
            k = bin(s).count('1')
            by.setdefault(k, ([], []))
            by[k][0].append(s)
            by[k][1].append([j for j in range(n) if (s >> j) & 1])
        _GAMMA_STRUCT[n] = {k: (np.array(v[0]), np.array(v[1], dtype=int))
                            for k, v in by.items() if k > 0}
    return _GAMMA_STRUCT[n]


def gamma_species(species, U):
    """Second quantization Lambda^*(U): Gamma[T,S] = det(U[rows(T), cols(S)]),
    vectorized via stacked determinants."""
    n = SP_NMODES[species]
    d = 1 << n
    G = np.zeros((d, d), complex)
    G[0, 0] = 1.0
    for k, (masks, rows) in _gamma_struct(n).items():
        A = U[rows[:, None, :, None], rows[None, :, None, :]]   # (m,m,k,k)
        G[np.ix_(masks, masks)] = np.linalg.det(A)
    return G

# ---------------------------------------------------------------------------
# arenas
# ---------------------------------------------------------------------------

class Arena:
    def __init__(self, species):
        self.species = list(species)
        assert self.species == [s for s in SP_ORDER if s in species]
        self.nmodes = sum(SP_NMODES[s] for s in self.species)
        self.dim = 1 << self.nmodes
        self.offs = {}
        off = 0
        for s in self.species:
            self.offs[s] = off
            off += SP_NMODES[s]
        self.shape = tuple(SP_DIM[s] for s in reversed(self.species))

    def sp_index(self, idx, sp):
        return (idx >> self.offs[sp]) & (SP_DIM[sp] - 1)

    def apply_sp_op(self, psi, sp, M):
        t = psi.reshape(self.shape)
        ax = len(self.species) - 1 - self.species.index(sp)
        t = np.tensordot(M, t, axes=([1], [ax]))
        t = np.moveaxis(t, 0, ax)
        return t.reshape(-1)

    def apply_onebody(self, psi, g):
        out = np.zeros_like(psi)
        for sp in self.species:
            if np.abs(X[sp][g]).max() > 1e-14:
                out += self.apply_sp_op(psi, sp, X[sp][g])
        return out

    def apply_lowering(self, psi, w):
        out = np.zeros_like(psi)
        for sp in self.species:
            if np.abs(XLOW[sp][w]).max() > 1e-14:
                out += self.apply_sp_op(psi, sp, XLOW[sp][w])
        return out

    def apply_gamma(self, psi, U3, U2, theta):
        out = psi
        for sp in self.species:
            U = mode_unitary(sp, U3, U2, theta)
            out = self.apply_sp_op(out, sp, gamma_species(sp, U))
        return out

    def weights(self):
        idx = np.arange(self.dim)
        slots = []
        for s in self.species:
            slots += model.SPECIES_SLOTS[s]
        occ = (idx[:, None] >> np.arange(self.nmodes)[None, :]) & 1
        P = occ @ np.array([model.MODES[i]['p'] for i in slots])
        Q = occ @ np.array([model.MODES[i]['q'] for i in slots])
        T = occ @ np.array([model.MODES[i]['t'] for i in slots])
        Y = occ @ np.array([model.MODES[i]['y'] for i in slots])
        ns = {}
        for s in self.species:
            o = self.offs[s]
            ns[s] = occ[:, o:o + SP_NMODES[s]].sum(1)
        return P, Q, T, Y, ns


def mode_unitary(species, U3, U2, theta):
    yv = dict(Q=1, L=-3, u=4, d=-2, e=-6)[species]
    ph = np.exp(1j * theta * yv / 6.0)
    if species == 'Q':
        return ph * np.kron(U3, U2)
    if species == 'L':
        return ph * U2
    if species in ('u', 'd'):
        return ph * U3
    return ph * np.eye(1, dtype=complex)


def haar_unitary(n, rng):
    z = rng.standard_normal((n, n)) + 1j * rng.standard_normal((n, n))
    q, r = np.linalg.qr(z)
    return q * (np.diagonal(r) / np.abs(np.diagonal(r)))


def haar_su(n, rng):
    U = haar_unitary(n, rng)
    return U / np.linalg.det(U) ** (1.0 / n)


def random_gauge(rng):
    return haar_su(3, rng), haar_su(2, rng), rng.uniform(0, 12 * np.pi)

# ---------------------------------------------------------------------------
# Casimir term lists
# ---------------------------------------------------------------------------

def casimir_terms(species):
    colored = [s for s in species if s in COLORED]
    doublet = [s for s in species if s in DOUBLET]
    t3, t2 = [], []
    for s in colored:
        t3.append((1.0, {s: sum(X[s][A] @ X[s][A] for A in range(8))}))
    for i in range(len(colored)):
        for j in range(i + 1, len(colored)):
            s, sp = colored[i], colored[j]
            for A in range(8):
                t3.append((2.0, {s: X[s][A], sp: X[sp][A]}))
    for s in doublet:
        t2.append((1.0, {s: sum(X[s][8 + a] @ X[s][8 + a] for a in range(3))}))
    for i in range(len(doublet)):
        for j in range(i + 1, len(doublet)):
            s, sp = doublet[i], doublet[j]
            for a in range(3):
                t2.append((2.0, {s: X[s][8 + a], sp: X[sp][8 + a]}))
    return t3, t2


def c3_terms(species):
    colored = [s for s in species if s in COLORED]
    terms = []
    nz = [(a, b, c) for a in range(8) for b in range(8) for c in range(8)
          if abs(DSYM[a, b, c]) > 1e-12]
    for s in colored:
        M = np.zeros((SP_DIM[s], SP_DIM[s]), complex)
        for a, b, c in nz:
            M += DSYM[a, b, c] * (X[s][a] @ X[s][b] @ X[s][c])
        terms.append((1.0, {s: M}))
    for s in colored:                              # pattern (s,s,s')
        K = [sum(DSYM[a, b, c] * (X[s][a] @ X[s][b])
                 for a in range(8) for b in range(8)
                 if abs(DSYM[a, b, c]) > 1e-12) for c in range(8)]
        for sp in colored:
            if sp == s:
                continue
            for c in range(8):
                if np.abs(K[c]).max() > 1e-14 and np.abs(X[sp][c]).max() > 1e-14:
                    terms.append((3.0, {s: K[c], sp: X[sp][c]}))
    if len(colored) == 3:
        s1, s2, s3 = colored
        for a, b, c in nz:
            terms.append((6.0 * DSYM[a, b, c],
                          {s1: X[s1][a], s2: X[s2][b], s3: X[s3][c]}))
    return terms


def block_matrix(terms, sp_idx, eq):
    sps = list(sp_idx.keys())
    n = len(next(iter(sp_idx.values())))
    M = np.zeros((n, n), complex)
    for coef, facs in terms:
        term = np.full((n, n), coef, complex)
        ok = True
        for sp in sps:
            if sp in facs:
                xi = sp_idx[sp]
                term = term * facs[sp][xi[:, None], xi[None, :]]
            else:
                term = term * eq[sp]
            if not np.any(term):
                ok = False
                break
        if ok:
            M += term
    return M

# ---------------------------------------------------------------------------
# full sector analysis of an arena
# ---------------------------------------------------------------------------

def c2_su3(a, b):
    return (a * a + b * b + a * b + 3 * a + 3 * b) / 3.0


def analyze_arena(arena, table):
    """Block-by-block Schur decomposition + machine verification of every
    multiplicity in `table`.  Returns dict(blocks=[{idx, vecs, irrep}], c3_val)."""
    P, Q, T, Y, ns = arena.weights()
    key_arr = np.stack([ns[s] for s in arena.species] + [P, Q, T], axis=1)
    uk, inv = np.unique(key_arr, axis=0, return_inverse=True)
    nsp = len(arena.species)

    wm_cache = {}
    def wts3(a, b):
        if (a, b) not in wm_cache:
            wm_cache[(a, b)] = su3mod.wm(a, b)
        return wm_cache[(a, b)]

    t3, t2 = casimir_terms(arena.species)
    t3c = c3_terms(arena.species)

    c3_val = {}
    blocks = []
    deferred = []
    count_per_irrep = np.zeros(len(table), dtype=int)
    count_per_irrep_wt = {}
    kappa = 1.0 / np.pi

    def cluster_evals(w, tol=1e-6):
        cl = []
        for i, val in enumerate(w):
            if cl and abs(val - cl[-1][0][-1]) < tol:
                cl[-1][0].append(val); cl[-1][1].append(i)
            else:
                cl.append(([val], [i]))
        return cl

    def record(iid, p, q, t, ncols, sel, vv):
        count_per_irrep[iid] += ncols
        count_per_irrep_wt[(iid, p, q, t)] = \
            count_per_irrep_wt.get((iid, p, q, t), 0) + ncols
        blocks.append(dict(idx=sel, vecs=vv, irrep=iid))

    member_sel = np.where(inv == 0)[0]  # placeholder to appease linters

    for bk in range(len(uk)):
        sel = np.where(inv == bk)[0]
        n_b = len(sel)
        key = uk[bk]
        p, q, t = int(key[nsp]), int(key[nsp + 1]), int(key[nsp + 2])
        y = int(Y[sel[0]])
        sp_idx = {s: arena.sp_index(sel, s) for s in arena.species}
        eq = {s: (sp_idx[s][:, None] == sp_idx[s][None, :]) for s in arena.species}
        H3 = block_matrix(t3, sp_idx, eq)
        H2 = block_matrix(t2, sp_idx, eq)
        assert np.abs(H3 - H3.conj().T).max() < 1e-10
        assert np.abs(H2 - H2.conj().T).max() < 1e-10
        cands = []
        for iid, r in enumerate(table):
            if r['y'] != y or r['twoj'] < abs(t) or (r['twoj'] - t) % 2 != 0:
                continue
            mult3 = wts3(r['a'], r['b']).get((p, q), 0)
            if mult3 == 0:
                continue
            cands.append((iid, r))
        Hc = H3 + kappa * H2
        w, V = np.linalg.eigh(Hc)
        classes = {}
        for iid, r in cands:
            ckey = (r['a'] ** 2 + r['b'] ** 2 + r['a'] * r['b']
                    + 3 * r['a'] + 3 * r['b'],
                    r['twoj'] * (r['twoj'] + 2))
            classes.setdefault(ckey, []).append(iid)
        used = np.zeros(n_b, bool)
        for ckey, memb_ids in classes.items():
            ev = ckey[0] / 3.0 + kappa * ckey[1] / 4.0
            hit = np.where(np.abs(w - ev) < 1e-6)[0]
            if len(hit) == 0:
                continue
            assert not used[hit].any()
            used[hit] = True
            vecs = V[:, hit]
            if len(memb_ids) == 1:
                iid = memb_ids[0]
                r = table[iid]
                if (p, q) == (r['a'], r['b']) and t == r['twoj'] and iid not in c3_val:
                    H3c = block_matrix(t3c, sp_idx, eq)
                    sc = np.diagonal(vecs.conj().T @ H3c @ vecs)
                    assert np.abs(sc - sc.mean()).max() < 1e-7, (key, sc)
                    c3_val[iid] = float(np.real(sc.mean()))
                record(iid, p, q, t, vecs.shape[1], sel, vecs)
                continue
            # ambiguity must be exactly an su3-conjugate pair
            labs = [(table[i]['a'], table[i]['b']) for i in memb_ids]
            assert len(memb_ids) == 2 and labs[0] == (labs[1][1], labs[1][0]), \
                (key, labs)
            H3c = block_matrix(t3c, sp_idx, eq)
            Hr = vecs.conj().T @ H3c @ vecs
            assert np.abs(Hr - Hr.conj().T).max() < 1e-9
            w3, V3 = np.linalg.eigh(Hr)
            vecs3 = vecs @ V3
            cl = cluster_evals(w3)
            if not all(mid in c3_val for mid in memb_ids):
                deferred.append((sel, p, q, t, vecs3,
                                 [(list(c[1]), float(np.mean(c[0]))) for c in cl],
                                 memb_ids))
                continue
            for vals, cols in cl:
                mval = float(np.mean(vals))
                best = min(memb_ids, key=lambda mid: abs(c3_val[mid] - mval))
                assert abs(c3_val[best] - mval) < 1e-5, (key, mval, c3_val)
                record(best, p, q, t, len(cols), sel, vecs3[:, cols])
        assert used.all(), (key, w)

    for sel, p, q, t, vecs3, clusters, memb_ids in deferred:
        for cols, mval in clusters:
            best = min(memb_ids, key=lambda mid: abs(c3_val[mid] - mval))
            assert abs(c3_val[best] - mval) < 1e-5, (p, q, t, mval)
            record(best, p, q, t, len(cols), sel, vecs3[:, cols])

    # C3 antisymmetry under conjugation, where both refs were measured
    lab2id = {(r['a'], r['b'], r['twoj'], r['y']): i for i, r in enumerate(table)}
    for iid, v in c3_val.items():
        r = table[iid]
        jid = lab2id.get((r['b'], r['a'], r['twoj'], -r['y']))
        if jid is not None and jid in c3_val:
            assert abs(c3_val[iid] + c3_val[jid]) < 1e-6, (iid, jid)

    # ---- global verification against the analytic table ----
    for iid, r in enumerate(table):
        assert count_per_irrep[iid] == r['m'] * r['dim'], \
            (iid, r, int(count_per_irrep[iid]))
        for (pp, qq), m3 in wts3(r['a'], r['b']).items():
            for tt in range(-r['twoj'], r['twoj'] + 1, 2):
                got = count_per_irrep_wt.get((iid, pp, qq, tt), 0)
                assert got == r['m'] * m3, (iid, r, pp, qq, tt, got)
    assert int(count_per_irrep.sum()) == arena.dim
    return dict(blocks=blocks, c3_val=c3_val)


def sector_probs(decomp, table, psi):
    p = np.zeros(len(table))
    for b in decomp['blocks']:
        amp = b['vecs'].conj().T @ psi[b['idx']]
        p[b['irrep']] += float(np.real(np.vdot(amp, amp)))
    return p


def product_state(arena, amps):
    """Tensor product state prod_modes (a0|0> + a1|1>), amps: species -> (a0,a1)."""
    psi = np.array([1.0 + 0j])
    for sp in arena.species:        # forward: later species end up in HIGH bits
        a0, a1 = amps[sp]
        v = np.array([a0, a1], complex)
        loc = np.array([1.0 + 0j])
        for _ in range(SP_NMODES[sp]):
            loc = np.kron(v, loc)
        psi = np.kron(loc, psi)
    return psi


def shannon(p, tol=1e-14):
    p = np.asarray(p, float)
    p = p[p > tol]
    return float(-(p * np.log2(p)).sum())
