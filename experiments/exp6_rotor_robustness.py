"""Experiment 6: convention-robustness of the rotor-Hamiltonian vacuum.

The candidate selection principle (Exp 4) is: vacuum = ground state of
H = sum_{a<b} sigma(a,b) iL_aL_b, with sigma the octonion multiplication-table
signs. The entropy triple S = (0.630, 0.543, 0.430) was computed in ONE
convention. Here we redo the entire canonical construction under:

  1. all 128 basis sign gauges e_a -> s_a e_a,
  2. all 5040 index relabelings e_a -> e_{pi(a)} (with the XOR-linear
     GL(3,2) subgroup of 168 tracked separately),
  3. 2000 random combined (sign, permutation) transformations,
  4. the opposite algebra, right-multiplication operators, unsigned
     couplings, and the -H (ceiling state) variant.

Question: is the sorted vacuum entropy triple a convention-independent
invariant, an orbit of a few values, or convention-dependent noise?
"""
import json
from itertools import permutations
import numpy as np
import qio_lib as q

# ---- base multiplication table (Cayley-Dickson) ----
def cd_mult(x, y, n):
    if n == 0:
        return np.array([x[0] * y[0]])
    h = len(x) // 2
    a, b, c, d = x[:h], x[h:], y[:h], y[h:]
    conj = lambda z: np.concatenate(([z[0]], -z[1:]))
    return np.concatenate([cd_mult(a, c, n-1) - cd_mult(conj(d), b, n-1),
                           cd_mult(d, a, n-1) + cd_mult(b, conj(c), n-1)])

E = np.eye(8)
SIG = np.zeros((8, 8))
for a in range(8):
    for b in range(8):
        SIG[a, b] = cd_mult(E[a], E[b], 3)[a ^ b]
XOR = np.array([[a ^ b for b in range(8)] for a in range(8)])

def build_H(cidx, sgn, right=False):
    """Canonical rotor H from a table (cidx = product index, sgn = sign)."""
    Ls = np.zeros((8, 8, 8))
    for a in range(8):
        Ls[a][cidx[a], np.arange(8)] = sgn[a]
    if right:  # right-multiplication operators R_a[c(b,a), b] = sgn(b,a)
        Ls = np.zeros((8, 8, 8))
        for a in range(8):
            Ls[a][cidx[:, a], np.arange(8)] = sgn[:, a]
    H = np.zeros((8, 8), complex)
    for a in range(1, 8):
        for b in range(a + 1, 8):
            H += sgn[a, b] * 1j * (Ls[a] @ Ls[b])
    return H

def vacuum(H):
    w, v = np.linalg.eigh(H)
    deg = int((w < w[0] + 1e-9).sum())
    psi = v[:, :1].T.copy()
    S = q.single_qubit_entropies(psi)[0]
    return deg, np.sort(S)[::-1], float(q.three_tangle(psi)[0])

def record(tag, deg, S, tau, store):
    key = tuple(np.round(S, 4))
    store.setdefault(key, []).append(tag)
    return dict(tag=tag, deg=deg, S=[float(x) for x in S], tau3=round(tau, 4))

out, orbits = {}, {}

# ---- baseline ----
deg0, S0, tau0 = vacuum(build_H(XOR, SIG))
print(f"baseline: deg={deg0} S={S0.round(4)} tau3={tau0:.4f}")
out['baseline'] = dict(deg=deg0, S=[float(x) for x in S0], tau3=tau0)

# ---- 1. sign gauges ----
triples = {}
degs = []
for bits in range(128):
    s = np.ones(8)
    for i in range(7):
        if (bits >> i) & 1:
            s[i + 1] = -1
    sgn = SIG * s[:, None] * s[None, :] * s[XOR]
    deg, S, tau = vacuum(build_H(XOR, sgn))
    degs.append(deg)
    triples.setdefault(tuple(np.round(S, 4)), 0)
    triples[tuple(np.round(S, 4))] += 1
out['sign_gauges'] = dict(n=128, degeneracies=sorted(set(degs)),
                          distinct_sorted_triples={str(k): v for k, v in triples.items()})
print(f"sign gauges: {len(triples)} distinct sorted triples, degs {sorted(set(degs))}")

# ---- 2. index relabelings ----
triples_p, triples_gl = {}, {}
degs_p = []
n_gl = 0
for pi in permutations(range(1, 8)):
    p = np.array([0] + list(pi))
    pinv = np.argsort(p)
    cidx = pinv[XOR[p][:, p]]                    # c(a,b) = pinv[p[a]^p[b]]
    sgn = SIG[p][:, p]
    deg, S, tau = vacuum(build_H(cidx, sgn))
    degs_p.append(deg)
    key = tuple(np.round(S, 4))
    triples_p[key] = triples_p.get(key, 0) + 1
    if np.array_equal(p[XOR], XOR[p][:, p].T * 0 + p[XOR]) and \
       all(p[a ^ b] == p[a] ^ p[b] for a in range(8) for b in range(8)):
        n_gl += 1
        triples_gl[key] = triples_gl.get(key, 0) + 1
out['permutations'] = dict(n=5040, n_GL32=n_gl, degeneracies=sorted(set(degs_p)),
                           n_distinct_triples=len(triples_p),
                           triples_top=sorted(((v, str(k)) for k, v in triples_p.items()),
                                              reverse=True)[:8],
                           GL32_triples={str(k): v for k, v in triples_gl.items()})
print(f"permutations: {len(triples_p)} distinct triples over 5040 "
      f"(GL(3,2) subgroup n={n_gl}: {len(triples_gl)} distinct)")

# ---- 3. random combined transformations ----
rng = np.random.default_rng(5)
triples_c = {}
for _ in range(2000):
    p = np.array([0] + list(rng.permutation(np.arange(1, 8))))
    pinv = np.argsort(p)
    s = np.where(rng.random(8) < 0.5, -1.0, 1.0); s[0] = 1
    cidx = pinv[XOR[p][:, p]]
    sgn = SIG[p][:, p] * s[:, None] * s[None, :] * s[cidx]
    deg, S, tau = vacuum(build_H(cidx, sgn))
    key = tuple(np.round(S, 4))
    triples_c[key] = triples_c.get(key, 0) + 1
out['combined_random'] = dict(n=2000, n_distinct_triples=len(triples_c),
                              triples_top=sorted(((v, str(k)) for k, v in triples_c.items()),
                                                 reverse=True)[:8])
print(f"combined random: {len(triples_c)} distinct triples over 2000")

# ---- 4. structural variants ----
variants = {}
deg, S, tau = vacuum(build_H(XOR, SIG.T))            # opposite algebra
variants['opposite_algebra'] = dict(deg=deg, S=[float(x) for x in S], tau3=round(tau, 4))
deg, S, tau = vacuum(build_H(XOR, SIG, right=True))  # right multiplications
variants['right_mult'] = dict(deg=deg, S=[float(x) for x in S], tau3=round(tau, 4))
deg, S, tau = vacuum(build_H(XOR, np.abs(SIG)))      # unsigned couplings
variants['unsigned_J'] = dict(deg=deg, S=[float(x) for x in S], tau3=round(tau, 4))
deg, S, tau = vacuum(-build_H(XOR, SIG))             # ceiling state
variants['minus_H'] = dict(deg=deg, S=[float(x) for x in S], tau3=round(tau, 4))
out['variants'] = variants
for k, v in variants.items():
    print(f"{k:18s} deg={v['deg']} S={np.round(v['S'],4)} tau3={v['tau3']}")

with open('results/exp6_results.json', 'w') as f:
    json.dump(out, f, indent=2)
print("Saved results/exp6_results.json")
