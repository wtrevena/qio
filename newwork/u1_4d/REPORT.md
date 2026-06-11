# Fisher information in compact U(1) edge-flux sectors across a higher-dimensional entangling surface
## Research report (literature + structure + computation), 2026-06-10

**Question (reviewer, `new_review.txt` 438-444):** *Does the compact U(1) flux-sector
distribution across a closed entangling surface form an exponential family in 1/e^2, and how much
Fisher information about e does it carry?*

**Deliverables in this folder:** `LITERATURE.md` (verified primary-source base, with status
table), `DERIVATION.md` (analytic structural layer), `u1_chain_ed.py` + `results_chain.json`
(exact diagonalization of compact U(1) on a 2+1d plaquette strip in the dual height
representation; 87 ground states; deterministic, RNG-free Lanczos), `analyze_chain.py` +
`analysis_chain.json` + `analysis_weak_hmax3.json` (exponential-family rank tests, Fisher
information, identity tests, convergence), `u1_dipole_gas.py` + `results_dipole.json` (exact
analytic models of the two 3+1d limits). Files `ed2p1.py`, `gauss4d.py`, `u1_2d_baseline.py`,
`mc_row_*.json`, `results_2d.json`, `results_gauss*.json` predate this session (earlier sibling
session) and were neither used nor modified.

---

## 1. Verdict on the exponential-family question

**Conditionally yes -- as an asymptotic, phase-by-phase property; not as an exact identity as in
d = 2.** Precisely:

1. **d = 3+1, weak coupling (Coulomb phase, the phase relevant to "Maxwell + monopoles"):**
   the ground-state flux-sector distribution across a closed surface is, up to exponentially
   small monopole corrections, a Gauss-constrained discrete Gaussian
   p({n}) ~ exp[-(e^2/2) n.M^{-1}.n] with M a *pure-geometry* kernel (the photon does not run in
   the pure compact theory). This **is** a one-parameter exponential family; the natural
   parameter is **e^2 itself** (for electric sectors; the magnetic dual sectors have natural
   parameter ~ 1/e^2, so the reviewer's "in 1/e^2" is exactly right for the magnetic labels and
   right-up-to-reparametrization for the electric ones -- exponential-family-ness is
   parametrization invariant). The only piece of this already in the literature is the single
   constant-flux zero mode: Donnelly-Wall 1506.05792 eq. (36),
   Z_E = sum_{E in q_B Z} e^{-(1/2)Vol(B)E^2}, i.e. p(n) ~ e^{-(q_B^2 Vol(B)/2)n^2} -- verbatim
   verification in `LITERATURE.md` sec. 2.2.
2. **d = 3+1, strong coupling (confining phase):** the leading strong-coupling ground state gives
   an exact exponential family, but with **sufficient statistic T = (1/2) sum_l |n_l| (dipole
   count, the l^1 flux -- NOT the Casimir sum n^2)** and **natural parameter theta = ln(16 e^8)
   -- logarithmic in the coupling, not linear in e^2 or 1/e^2** (derivation `DERIVATION.md`
   sec. B; the analogous 2+1d coefficients verified by ED to 4 significant figures, below).
3. **Between the asymptotic regimes the family is genuinely curved** (not exponential in any
   single statistic): measured sigma3/sigma2 curvature of the log-likelihood matrix = 5e-2 over
   the full coupling range of the 2+1d model, vs 4e-4 in the strong-coupling window and 1e-15
   for the exact 2d YM control. The sufficient statistic itself crosses over from (1/2)sum|n|
   (strong) to a quadratic form (weak): the fitted statistic shape T(2) moves from 2.0 (=|n|)
   deep in strong coupling to 3.56 (close to n^2 = 4) in the weak window (hmax = 3 data).

So the 2d YM mechanism has a real but *split* 4d descendant: the exponential-family structure and
the entropy-Fisher identity survive at both ends of the coupling axis, but no single natural
parameter or sufficient statistic covers the whole axis, and the exactness that made Paper 3 a
theorem (the self-reproducing heat kernel) has no analog.

## 2. The entropy-Fisher identity

The 2d identity dS/dt = -t I(t) generalizes as a **lemma about exponential families with trivial
base measure** (DERIVATION.md, Lemma): dS/dtheta = -theta Var(T) = -theta I(theta) in the natural
parameter theta.

- **Coulomb-phase zero mode (d = 3+1):** natural parameter ~ e^2, so **dS/de^2 = -e^2 I(e^2)
  holds literally** -- the direct descendant of dS/dt = -t I(t) with t = g^2 A -> theta = e^2
  (times geometry). Verified to 3e-10 (`results_dipole.json`, module 2); Gaussian asymptotics
  **I(e^2) = 1/(2 e^4) per flux mode** verified to 1e-4 relative at all tested e^2 <= 1.
- **Strong coupling:** the identity holds in theta = ln(16 e^8) (verified to finite-difference
  floor, <= 1e-6), but the naive e^2-form *fails by exactly the predicted reparametrization
  factor theta/4*: measured dS/de^2 / (-e^2 I(e^2)) = 1.099, 1.386, 1.792, 2.303, 2.773, 3.178
  at e^2 = 1.5...12 vs prediction theta/4 = same numbers to 3 decimals. The same factor appears
  independently in the 2+1d ED (measured 1.079/1.558/1.965 vs theta/4 = 1.087/1.559/1.965 at
  e^2 = 2.5/4/6).

## 3. Strong-coupling Fisher result (the tractable, controlled regime)

For d = 3+1 lattice compact U(1) at strong coupling (per straddling boundary plaquette; there are
N_str = 2 N_cut of them, so everything below is **extensive in the cut area** -- the decisive
structural difference from 2d YM, where the flux was one global variable and information did not
scale):

    p_dipole = c^2 = 1/(16 e^8),    theta = ln 16 + 8 ln e,
    S_class ~ N_str * 2 c^2 (1 - ln 2c^2),
    I(theta) = N_str * 2 c^2 (1 - 2c^2),     I(e^2) = (4/e^2)^2 I(theta) ~ N_str * 2/e^12,
    dS/dtheta = -theta I(theta)   exactly at leading order.

Numbers (per plaquette): at e^2 = 1.5, p_dip = 1.2e-2, I(theta) = 2.4e-2; at e^2 = 5,
p_dip = 1.0e-4, I(theta) = 2.0e-4. Both entropy and information vanish as e^2 -> infinity
(frozen sectors), exactly like t -> infinity in 2d YM. The 2+1d ED quantitatively confirms the
whole strong-coupling picture: d ln p(1)/p(0) / d ln e^2 = -4.002 (prediction -4), intercept
0.689 (ln 2 = 0.693), p(1)/(2c^2) = 0.9999 at e^2 = 8.

## 4. Weak-coupling / continuum status (d = 3+1)

Three-tiered, and this is the honest core of the answer to "how much Fisher information about e":

1. **Lattice-regulated edge data: I_total(e^2) ~ N_modes/(2 e^4) with N_modes ~ Area/a^2 --
   divergent in the continuum limit** at fixed physical surface. Every boundary lattice cell is
   an independent (up to the Gauss constraint and the kernel's correlations) flux sample. The
   coupling is *infinitely well determined* by cutoff-scale flux data -- but that information
   lives entirely in the center/edge sector that is non-distillable (Soni-Trivedi 1510.07455,
   1608.00353), drops out of mutual/relative entropy in the continuum (Moitra-Soni-Trivedi
   1811.06986), and is center-choice dependent (Casini-Huerta-Rosabal 1312.1183).
2. **IR/topological zero modes: finite, nonzero, cutoff-independent Fisher information.** The
   Donnelly-Wall flux zero mode carries I(e^2) = 1/(2 e^4) (1 + quantization corrections) per
   closed surface/homology class. This is the d = 4 object most literally analogous to Paper 3's
   p_R(t), and the only candidate for a *physical* (regulator-independent) Fisher statement we
   can defend.
3. **Universal continuum coefficients: zero Fisher information.** The free-Maxwell log
   coefficient is e-independent (-16/45, Casini-Huerta 1512.06182), and the charge/monopole
   correction that restores the anomaly is *independent of the coupling's value* (CHMP
   1911.00529). Verified quotes in `LITERATURE.md` sec. 1, sec. 3.

Why no contradiction with "free Maxwell EE cannot depend on e": all e-dependence above is a
**compactness effect** -- integer flux quantization supplies the absolute unit that the field
redefinition E -> E/e would otherwise erase. Remove compactness and M^{-1}'s normalization is
unobservable; with n integer it is measured in flux quanta and e^2 becomes estimable. In d = 2+1
(Polyakov) there is the further wrinkle that the kernel itself runs (mass gap m(e^2) ~
e^{-const/e^2}), so even the weak-coupling family is weakly curved -- visible in our ED as
sigma3/sigma2 = 5e-2 in the weak window at hmax = 3.

## 5. What the numerics showed (all deterministic; convergence-checked)

Model: compact U(1) on a 1xN plaquette strip (2+1d), dual integer-height chain, Lanczos ED
(`u1_chain_ed.py`; dim up to 7^6 = 117649; Lanczos residuals <= 2e-13; no RNG anywhere; the
single-cut-link flux n = h_k - h_{k+1} is the center label).

| Test | Result |
|---|---|
| Exponential-family rank test sigma3/sigma2 (0 = exact) | full range 5.1e-2; strong window 3.8e-4; weak window 3.9-5.1e-2; 2d YM control 1.4e-15 |
| Strong-coupling natural parameter | dtheta/d ln e^2 = 4.0020 (pred. 4); intercept 0.6892 (pred. ln 2 = 0.6931); p(1)/2c^2 = 0.9999 |
| Weak-coupling natural parameter | theta = 1.17 e^2 - 0.12, R^2 = 0.989 at hmax = 3 -- approximately linear in e^2, residual curvature genuine (finite-size kernel) |
| Sufficient-statistic crossover | fitted T(2): 2.23 (global, strong-dominated; abs-n -> 2) vs 3.56 (weak window; n^2 -> 4) |
| Identity dS/dtheta = -theta Var(T) - Cov(ln h,T) | rel. residual <= 1e-3 for e^2 >= 2.5 (with T = abs n: <= 4e-3); with T = n^2 at e^2 = 0.7: 2.6e-2 (hmax = 2) / 2.6e-1 (hmax = 3, crossover curvature is real); both fail ~40% at e^2 = 1 (maximal curvature) |
| Naive e^2-identity ratio dS/de^2/(-e^2 I) | = theta/4 to 3 decimals at strong coupling (1.079 -> 1.965 for e^2 = 2.5 -> 6); = 0.9-1.0 at weak coupling |
| Fisher information I(e^2) | smooth, finite, single-peaked: 1.87 (e^2=0.4) -> 1.08 (e^2=1) -> 3.4e-4 (e^2=6); per cut link |
| Convergence | N-dependence negligible (<= 2e-5 in S at N=7 vs 6); hmax-dependence controlled for e^2 >= 0.6, NOT converged at e^2 = 0.3 with hmax <= 3 (theta: 0.487/0.310/0.268 for hmax = 1/2/3) -- weakest-coupling numbers are qualitative |

3+1d analytic models (`u1_dipole_gas.py`): dipole-gas identity verified to <= 1e-6; zero-mode
discrete Gaussian: I(e^2) * 2 e^4 = 1.0000 and dS/de^2 = -e^2 I(e^2) to <= 5e-10.

## 6. Honest answer to the reviewer, in two sentences

The compact U(1) flux-sector distribution across a closed entangling surface is an exponential
family **asymptotically in each phase** -- in the 4d Coulomb phase it is (up to e^{-S_mono})
the Gauss-constrained discrete Gaussian with natural parameter e^2 (electric) / 1/e^2 (magnetic),
the entropy-Fisher identity dS/de^2 = -e^2 I(e^2) holds there, and the per-mode information is
1/(2 e^4) -- but **globally in the coupling the family is curved**, with the sufficient statistic
crossing from (1/2)sum|n_l| (confining phase, natural parameter ln(16 e^8)) to a quadratic form.
The Fisher information about e is **finite per lattice mode, extensive in the cut area (the d = 2
"information does not scale" pathology disappears), UV-divergent (~ Area/a^2) in the continuum
limit of the edge sector, finite and cutoff-independent only for topological zero modes, and
exactly zero in universal continuum coefficients** -- so a physically defensible Paper-4 claim
must target the zero-mode/topological family, not the area-law edge data.

## 7. What a full lattice study would require (pricing the lumber)

1. **3+1d Hamiltonian ED beyond strips:** a 2x2x2 cube with |n| <= 2 is ~1e7-1e8 states with
   Gauss projection -- feasible with sparse methods + symmetry reduction, not in this sandbox.
   Needed to see the *joint* multi-link flux distribution and its M-kernel at intermediate e^2.
2. **Euclidean Monte Carlo of 4d compact QED with flux-sector resolution:** replica/snake
   algorithms exist for EE (cf. 2304.03311-style nonequilibrium methods), but the sector
   *distribution* requires measuring the joint distribution of flux observables on the surface --
   new measurement code; the Coulomb phase (beta > 1.01) is the target; check the discrete-
   Gaussian prediction and extract M; monopole corrections near beta_c.
3. **Zero-mode program (the defensible one):** put the theory on T^3 x R, measure the
   distribution of the three global electric flux winding sectors vs e^2; compare to
   sum_n e^{-(e^2 L/2 ...)n^2}; Fisher information per zero mode; this is finite, physical, and
   directly the DW eq. (36) object. Smallest honest version of "Paper 4".
4. **Theory gap to close:** a sharp statement of how much of I(e^2) survives in *distillable* or
   relative-entropy quantities (expectation from MST/CHMP: zero in the continuum; a proof
   would make the negative half of the paper rigorous).
5. **Center-choice dependence:** repeat the strip computation with a magnetic/trivial center to
   quantify how the *amount* of Fisher information depends on the algebra choice (expected:
   strongly -- it is edge data).

## 8. Decision relevance for Paper 4

**Single most decision-relevant finding:** the 2d mechanism survives in d = 4 in exactly one
regulator-independent form -- the **topological zero-mode flux family
p(n) ~ e^{-(e^2 geom/2)n^2} (DW 1506.05792 eq. (36)), which is a bona fide exponential family
with natural parameter ~ e^2, satisfies the same entropy-Fisher identity as 2d YM, and carries
finite Fisher information 1/(2 e^4) per mode** -- while everything else (the area-extensive edge
information) is divergent, non-distillable, and center-choice dependent, and all universal
continuum coefficients are coupling-blind. A Paper 4 scoped as *"Fisher information in compact
U(1) flux sectors: exact asymptotic exponential families, the crossover obstruction, and the
zero-mode bridge to 4d"* is supportable today with the analytics + ED in this folder (plus the
T^3 zero-mode lattice check as its one new computation); a Paper 4 claiming a 4d
*local/universal* entanglement encoding of e is not supported and the evidence runs against it.
