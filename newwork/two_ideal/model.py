"""The one-generation chiral model: 15 Weyl modes carrying
SU(3)_c x SU(2)_L x U(1)_Y, and the decomposition of the fermionic Fock
space Lambda^*(V) into gauge irreps by exact highest-weight peeling.

Mode conventions (index order fixed once and for all; species contiguous):
  0..5   Q  = (3,2)_{1/6}   index = 2*c + s   (c = color 0,1,2; s = 0 up, 1 down)
  6..7   L  = (1,2)_{-1/2}  index = 6 + s
  8..10  uR = (3,1)_{2/3}
  11..13 dR = (3,1)_{-1/3}
  14     eR = (1,1)_{-1}

Weights: su3 fw-coords (p,q); su2 weight t = 2*Iz; hypercharge y = 6*Y (integer).
Color weights: c=0 -> (1,0), c=1 -> (-1,1), c=2 -> (0,-1).

Irrep label: (a, b, twoj, y).  All exact-integer bookkeeping.
"""
from fractions import Fraction
import numpy as np

import su3

COLOR_W = [(1, 0), (-1, 1), (0, -1)]


def make_modes():
    modes = []
    for c in range(3):
        for s in range(2):
            modes.append(dict(species='Q', p=COLOR_W[c][0], q=COLOR_W[c][1],
                              t=1 - 2 * s, y=1, chi=+1))
    for s in range(2):
        modes.append(dict(species='L', p=0, q=0, t=1 - 2 * s, y=-3, chi=+1))
    for c in range(3):
        modes.append(dict(species='u', p=COLOR_W[c][0], q=COLOR_W[c][1], t=0, y=4, chi=-1))
    for c in range(3):
        modes.append(dict(species='d', p=COLOR_W[c][0], q=COLOR_W[c][1], t=0, y=-2, chi=-1))
    modes.append(dict(species='e', p=0, q=0, t=0, y=-6, chi=-1))
    return modes


MODES = make_modes()
NMODES = len(MODES)
SPECIES_SLOTS = dict(Q=list(range(0, 6)), L=[6, 7], u=[8, 9, 10], d=[11, 12, 13], e=[14])


def anomaly_checks():
    """All one-generation anomaly sums, with chirality sign chi
    (left-handed +1, right-handed -1), Y = y/6.  Returns dict of exact values."""
    out = {}
    Y = lambda m: Fraction(m['y'], 6)
    out['su3^2-Y (sum over colored modes of chi*Y)'] = str(sum(
        m['chi'] * Y(m) for m in MODES if (m['p'], m['q']) != (0, 0)))
    out['su2^2-Y (sum over doublet modes of chi*Y)'] = str(sum(
        m['chi'] * Y(m) for m in MODES if m['t'] != 0))
    out['grav^2-Y (sum chi*Y)'] = str(sum(m['chi'] * Y(m) for m in MODES))
    out['Y^3 (sum chi*Y^3)'] = str(sum(m['chi'] * Y(m) ** 3 for m in MODES))
    out['Witten SU(2) (# doublets)'] = sum(1 for m in MODES if m['t'] == 1)
    out['sum_modes Y (unsigned; filled-state singlet iff 0)'] = str(sum(Y(m) for m in MODES))
    return out


# ---------------------------------------------------------------------------
# exact decomposition of Lambda^*(V_subset) by highest-weight peeling
# ---------------------------------------------------------------------------

def fock_weight_dict(slot_list):
    """{(p,q,t,y): count} over all 2^n subsets of the given mode slots.
    Also returns the per-state weight arrays for reuse."""
    n = len(slot_list)
    P = np.array([MODES[i]['p'] for i in slot_list])
    Q = np.array([MODES[i]['q'] for i in slot_list])
    T = np.array([MODES[i]['t'] for i in slot_list])
    Yv = np.array([MODES[i]['y'] for i in slot_list])
    idx = np.arange(1 << n)
    occ = (idx[:, None] >> np.arange(n)[None, :]) & 1
    tot = occ @ np.stack([P, Q, T, Yv], axis=1)        # (2^n, 4)
    d = {}
    for row in tot:
        key = (int(row[0]), int(row[1]), int(row[2]), int(row[3]))
        d[key] = d.get(key, 0) + 1
    return d, tot


def peel(weight_dict):
    """Exact highest-weight peeling of a (p,q,t,y) weight multiset under
    su3 x su2 x u1.  Returns list of dicts {a,b,twoj,y,m,dim}."""
    by_y = {}
    for (p, q, t, y), c in weight_dict.items():
        by_y.setdefault(y, {})[(p, q, t)] = c
    table = []
    for y in sorted(by_y):
        d = {k: v for k, v in by_y[y].items() if v}
        while d:
            # height function strictly positive on positive cone generators
            mu = max(d, key=lambda k: (2 * (k[0] + k[1]) + k[2], k))
            p, q, t = mu
            assert p >= 0 and q >= 0 and t >= 0, ("non-dominant maximal weight", mu, y)
            m = d[mu]
            assert m > 0
            diag3 = su3.wm(p, q)
            for (wp, wq), m3 in diag3.items():
                for wt in range(-t, t + 1, 2):
                    k = (wp, wq, wt)
                    d[k] = d.get(k, 0) - m * m3
                    assert d[k] >= 0, ("negative count", k, y, mu)
                    if d[k] == 0:
                        del d[k]
            table.append(dict(a=int(p), b=int(q), twoj=int(t), y=int(y), m=int(m),
                              dim=int(su3.weyl_dim(p, q) * (t + 1))))
    table.sort(key=lambda r: (r['y'], r['a'], r['b'], r['twoj']))
    return table


def char_fock(slot_list, phi1, phi2, psi, eta, conj_singlets=False):
    """chi_{Lambda^* V}(torus element) = prod_modes (1 + e^{i w.theta}).
    If conj_singlets, replace the RH singlet modes by their conjugates
    (u^c = (3bar,1)_{-2/3} etc.) -- used for the convention-independence lemma."""
    val = 1.0 + 0j
    for i in slot_list:
        m = MODES[i]
        p, q, y = m['p'], m['q'], m['y']
        if conj_singlets and m['chi'] == -1:
            p, q, y = -p, -q, -y
        val *= 1 + np.exp(1j * (p * phi1 + q * phi2 + m['t'] * psi + y * eta))
    return val


def char_table(table, phi1, phi2, psi, eta):
    """sum_i m_i chi_i at a torus element, using the INDEPENDENT Schur/Weyl
    character formulas (no Freudenthal)."""
    val = 0j
    for r in table:
        val += (r['m'] * su3.schur_char(r['a'], r['b'], phi1, phi2)
                * su3.su2_char(r['twoj'], psi) * np.exp(1j * r['y'] * eta))
    return val


def character_verification(table, slot_list, nrand=20, seed=20260610):
    """max |sum_i m_i chi_i - prod(1+e^{iw.theta})| over random torus elements."""
    rng = np.random.default_rng(seed)
    worst = 0.0
    for _ in range(nrand):
        p1, p2, ps, et = rng.uniform(0, 2 * np.pi, 4)
        lhs = char_table(table, p1, p2, ps, et)
        rhs = char_fock(slot_list, p1, p2, ps, et)
        worst = max(worst, abs(lhs - rhs))
    return float(worst)


def weyl_quadrature_sums(slot_list, N3=32, N2=32, N1=128):
    """Exact-on-grid Weyl-integration computation of
         <chi_F, chi_F> = sum_i m_i^2   (commutant dimension)
         <1, chi_F>     = m_singlet     (invariant-vector count)
    over SU(3) x SU(2) x U(1).  DFT quadrature is exact because all
    integrands are Laurent polynomials of degree < grid size per axis.
    Returns (dim_commutant, n_singlets) as integers (residuals asserted tiny).
    """
    th1 = 2 * np.pi * np.arange(N3) / N3
    ps = 2 * np.pi * np.arange(N2) / N2
    et = 2 * np.pi * np.arange(N1) / N1
    P1, P2 = np.meshgrid(th1, th1, indexing='ij')
    x1, x2, x3 = P1, P2 - P1, -P2
    z1, z2, z3 = np.exp(1j * x1), np.exp(1j * x2), np.exp(1j * x3)
    d3 = (z1 - z2) * (z1 - z3) * (z2 - z3)
    w3 = (np.abs(d3) ** 2) / 6.0
    w2 = (np.abs(np.exp(1j * ps) - np.exp(-1j * ps)) ** 2) / 2.0
    s_norm = 0.0
    s_inv = 0.0 + 0j
    for e in et:
        chi = np.ones((N3, N3, N2), complex)
        for i in slot_list:
            m = MODES[i]
            phase = np.exp(1j * (m['p'] * P1 + m['q'] * P2 + m['y'] * e))
            chi = chi * (1 + phase[:, :, None] * np.exp(1j * m['t'] * ps)[None, None, :])
        wgt = w3[:, :, None] * w2[None, None, :]
        s_norm += float(np.sum((np.abs(chi) ** 2) * wgt))
        s_inv += complex(np.sum(chi * wgt))
    s_norm /= (N3 * N3 * N2 * N1)
    s_inv /= (N3 * N3 * N2 * N1)
    dimc = int(round(s_norm))
    nsing = int(round(s_inv.real))
    assert abs(s_norm - dimc) < 1e-6, s_norm
    assert abs(s_inv - nsing) < 1e-6, s_inv
    return dimc, nsing


def z6_congruence(table):
    """Check y = 4*(a-b) + 3*t  (mod 6) for every irrep in the table.
    This is the statement that the faithful gauge group is
    (SU(3) x SU(2) x U(1)) / Z6 -- the true SM global structure."""
    return [r for r in table
            if (r['y'] - 4 * (r['a'] - r['b']) - 3 * r['twoj']) % 6 != 0]


def conjugation_symmetry(table):
    """Check m(a,b,j,y) == m(b,a,j,-y) (self-conjugacy of Lambda^* V,
    valid because det V is gauge-trivial: sum of mode hypercharges = 0)."""
    idx = {(r['a'], r['b'], r['twoj'], r['y']): r['m'] for r in table}
    bad = []
    for k, m in idx.items():
        kk = (k[1], k[0], k[2], -k[3])
        if idx.get(kk, 0) != m:
            bad.append((k, m, idx.get(kk, 0)))
    return bad
