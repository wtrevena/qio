"""Experiment 2: algebraically motivated state families (Sec 6.2).

Families: GHZ(theta), W, weighted-W, octonion-structure states (several
inequivalent maps built from the Cayley-Dickson multiplication table /
Fano-plane data), and quaternionic-subalgebra states.

Question: does any family reach r_S = 1.8174 without fitting?
"""
import json
import numpy as np
from scipy.optimize import brentq
import qio_lib as q

results = {}

# ---------- Octonion multiplication table via Cayley-Dickson ----------
# Quaternions as pairs of complexes, octonions as pairs of quaternions.
def cd_mult(x, y, n):
    """Multiply in 2^n-dim Cayley-Dickson algebra; x, y real arrays len 2^n."""
    if n == 0:
        return np.array([x[0] * y[0]])
    h = len(x) // 2
    a, b = x[:h], x[h:]
    c, d = y[:h], y[h:]
    conj = lambda z: np.concatenate(([z[0]], -z[1:]))
    return np.concatenate([
        cd_mult(a, c, n - 1) - cd_mult(conj(d), b, n - 1),
        cd_mult(d, a, n - 1) + cd_mult(b, conj(c), n - 1)])

E = np.eye(8)
SIGMA = np.zeros((8, 8))      # e_a e_b = SIGMA[a,b] e_{a XOR b}
for a in range(8):
    for b in range(8):
        prod = cd_mult(E[a], E[b], 3)
        c = int(np.argmax(np.abs(prod)))
        assert c == a ^ b
        SIGMA[a, b] = prod[c]

def analyze(name, psi, note=""):
    psi = np.asarray(psi, complex).reshape(1, 8)
    psi = psi / np.linalg.norm(psi)
    S = q.single_qubit_entropies(psi)[0]
    tau = float(q.three_tangle(psi)[0])
    if S[0] > S[1] > S[2] and abs(S[1] - S[2]) > 1e-12:
        r = float((S[0] - S[1]) / (S[1] - S[2]))
    else:
        r = None  # undefined or wrong ordering
    results[name] = dict(S=[float(s) for s in S], tau3=tau, r_S=r, note=note)
    print(f"{name:34s} S={np.round(S,4)} tau3={tau:.4f} r_S={r}")

# ---------- 1. GHZ family ----------
for th in [np.pi / 8, np.pi / 6, np.pi / 4]:
    psi = np.zeros(8, complex); psi[0] = np.cos(th); psi[7] = np.sin(th)
    analyze(f"GHZ(theta={th:.3f})", psi, "S1=S2=S3 always -> r_S undefined")

# ---------- 2. W state ----------
psi = np.zeros(8, complex); psi[1] = psi[2] = psi[4] = 3 ** -0.5
analyze("W", psi, "permutation symmetric -> r_S undefined")

# ---------- 3. Weighted-W family: does it intersect the matching manifold? ----
# |psi> = a|001> + b|010> + c|100>;  S1=h2(c^2), S2=h2(b^2), S3=h2(a^2).
# Constraints: a^2+b^2+c^2=1, r_S = R_SM. Solve: parametrize by S3, then S2 free?
# Strategy: scan S2 in (S3, 1); S1 = S2 + R*(S2-S3); feasibility: weights sum to 1.
def weight(S):  # smallest-eigenvalue branch
    return q.h2inv(S)

def family_residual(S3, S2):
    S1 = S2 + q.R_SM * (S2 - S3)
    if S1 >= 1:
        return None
    w1, w2, w3 = weight(S1), weight(S2), weight(S3)  # = c^2, b^2, a^2
    return w1 + w2 + w3 - 1.0

# find matching curve: for a grid of S3, solve for S2
curve = []
for S3 in np.linspace(0.30, 0.95, 200):
    f = lambda S2: family_residual(S3, S2) if family_residual(S3, S2) is not None else 10.
    lo, hi = S3 + 1e-6, min(0.999, S3 + (1 - S3) / (1 + q.R_SM) + (1 - S3))
    grid = np.linspace(lo, min(0.999, S3 + (0.999 - S3)), 400)
    vals = []
    for s2 in grid:
        rres = family_residual(S3, s2)
        vals.append(np.nan if rres is None else rres)
    vals = np.array(vals)
    sign = np.sign(vals)
    idx = np.where(np.diff(sign[~np.isnan(vals)]) != 0)[0]
    g = grid[~np.isnan(vals)]
    v = vals[~np.isnan(vals)]
    for i in np.where(np.diff(np.sign(v)) != 0)[0]:
        s2 = brentq(lambda x: family_residual(S3, x), g[i], g[i + 1])
        S1 = s2 + q.R_SM * (s2 - S3)
        w1, w2, w3 = weight(S1), weight(s2), weight(S3)
        curve.append((S3, s2, S1, w3, w2, w1))

curve = np.array(curve)
results['weighted_W'] = dict(
    intersects=bool(len(curve) > 0),
    n_solutions_on_grid=int(len(curve)),
    note="tau3=0 for all weighted-W states; solutions = matching manifold "
         "intersects the W-class (zero 3-tangle) sector",
    examples=[dict(S3=float(c[0]), S2=float(c[1]), S1=float(c[2]),
                   a2=float(c[3]), b2=float(c[4]), c2=float(c[5]))
              for c in curve[::max(1, len(curve)//5)][:5]])
print(f"weighted-W matching curve: {len(curve)} grid solutions; "
      f"intersects matching manifold: {len(curve) > 0}")
if len(curve):
    c0 = curve[len(curve)//2]
    psi = np.zeros(8, complex)
    psi[1], psi[2], psi[4] = np.sqrt(c0[3]), np.sqrt(c0[4]), np.sqrt(c0[5])
    analyze("weighted_W_example", psi, "explicit matching W-class state")

# ---------- 4. Octonion-structure states ----------
# Map A: sign-row state  psi_c ∝ sum_a sigma(a, a XOR c)  (multiplication-table
#        row sums routed to product index)
amp = np.array([SIGMA[np.arange(8), np.arange(8) ^ c].sum() for c in range(8)])
analyze("oct_A_sign_rowsum", amp, "sigma row-sum map")

# Map B: diagonal-phase state  psi_a ∝ sigma(a, a)
analyze("oct_B_diag", SIGMA[np.arange(8), np.arange(8)], "sigma(a,a) = -1 except a=0")

# Map C: Fano incidence state: uniform over the 7 imaginary units
amp = np.ones(8, complex); amp[0] = 0
analyze("oct_C_imaginary_uniform", amp, "uniform over e_1..e_7")

# Map C': include identity
analyze("oct_C2_all_units_uniform", np.ones(8, complex), "uniform over e_0..e_7")

# Map D: quaternionic subalgebra states: uniform over {e_0, e_i, e_j, e_k},
# for each Fano line {i,j,k} (XOR-closed triples)
lines = [(a, b, a ^ b) for a in range(1, 8) for b in range(a + 1, 8) if (a ^ b) > b]
for (i, j, k) in lines:
    amp = np.zeros(8, complex); amp[[0, i, j, k]] = 0.5
    analyze(f"oct_D_quat_line_{i}{j}{k}", amp, "quaternionic subalgebra state")

# Map E: structure-constant tri-linear state: psi_{ijk} from sigma on the
# Fano line bits: amplitude at index a = number of ordered pairs (b,c),
# b XOR c = a, weighted by sigma(b,c)  (full convolution of signs)
amp = np.array([sum(SIGMA[b, b ^ a] for b in range(8)) for a in range(8)], complex)
analyze("oct_E_sign_convolution", amp, "same as map A by construction")

# Map F: Szangolies preferred-complex-direction states (e_0 + i e_l)/sqrt2
for l in range(1, 8):
    amp = np.zeros(8, complex); amp[0] = 1; amp[l] = 1j
    analyze(f"oct_F_complexdir_e{l}", amp, "preferred complex direction")

with open('results/exp2_results.json', 'w') as f:
    json.dump(results, f, indent=2)
print("\nSaved results/exp2_results.json")
