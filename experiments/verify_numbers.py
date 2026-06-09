"""Verify every numerical claim in draft.md (Sections 5.1, 5.3, 6.3)."""
import numpy as np

# --- Sec 5.1 couplings at M_Z (PDG 2022) ---
a3, a2, a1 = 0.1179, 0.03374, 0.01695
inv = np.array([1/a3, 1/a2, 1/a1])
L = np.log(inv)
r_SM = (L[0]-L[1])/(L[1]-L[2])
print(f"alpha_i^-1(M_Z) = {inv.round(3)}")
print(f"log(alpha_i^-1) = {L.round(3)}  (paper: 2.138, 3.389, 4.078)")
print(f"r_SM(M_Z) = {r_SM:.4f}  (paper: 1.817)")

# --- Sec 5.3 example triple ---
def h2(x):
    x = np.clip(x, 1e-300, 1)
    y = 1-x
    return -(x*np.log2(x) + y*np.log2(np.clip(y,1e-300,1)))
from scipy.optimize import brentq
def h2inv(S):  # smaller eigenvalue in [0, 1/2]
    if S >= 1: return 0.5
    if S <= 0: return 0.0
    return brentq(lambda lam: h2(lam)-S, 1e-12, 0.5)
S = np.array([0.875, 0.730, 0.650])
rS = (S[0]-S[1])/(S[1]-S[2])
lam = np.array([h2inv(s) for s in S])
print(f"\nExample triple S = {S}, r_S = {rS:.4f} (paper: ~1.817)")
print(f"lambda = {lam.round(4)}  (paper: 0.295, 0.204, 0.167)")
print(f"polygon: lam_max={lam.max():.3f} <= sum others={lam.sum()-lam.max():.3f} ? {lam.max() <= lam.sum()-lam.max()}")

# --- Sec 6.3 one-loop running ---
MZ = 91.1876
b = np.array([-7.0, -19/6, 41/10])  # b3, b2, b1
inv_MZ = inv  # [a3^-1, a2^-1, a1^-1]
print("\nmu(GeV)   a3^-1    a2^-1    a1^-1    r_SM")
for mu in [10, MZ, 1e3, 1e6, 1e9, 1e12, 1e13]:
    t = np.log(mu/MZ)
    invs = inv_MZ - b/(2*np.pi)*t
    Lm = np.log(invs)
    r = (Lm[0]-Lm[1])/(Lm[1]-Lm[2])
    print(f"{mu:9.3g} {invs[0]:8.2f} {invs[1]:8.2f} {invs[2]:8.2f} {r:9.3f}")

# variation MZ -> 1e6
t6 = np.log(1e6/MZ)
invs6 = inv_MZ - b/(2*np.pi)*t6
L6 = np.log(invs6)
r6 = (L6[0]-L6[1])/(L6[1]-L6[2])
print(f"\nvariation MZ->1e6: {(r_SM-r6)/r_SM*100:.1f}%  (paper: ~24%)")

# alpha1-alpha2 crossing scale
tc = (inv_MZ[2]-inv_MZ[1]) * 2*np.pi / (b[2]-b[1])
print(f"a1-a2 crossing: mu = {MZ*np.exp(tc):.3g} GeV (paper: ~1e13)")

# cross-check alpha2, alpha1 from PDG primary inputs
aem_inv, s2w = 127.951, 0.23122  # MSbar at MZ
a2_chk = (1/aem_inv)/s2w
a1_chk = (5/3)*(1/aem_inv)/(1-s2w)
print(f"\ncross-check: a2 = {a2_chk:.5f} (paper 0.03374), a1 = {a1_chk:.5f} (paper 0.01695)")
