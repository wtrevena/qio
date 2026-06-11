# T^3 flux/winding sectors of compact U(1): the regulator-independent zero-mode family
## Computation record, 2026-06-11 (the "one new calculation" flagged in REPORT.md sec. 8)

**Artifacts.** `t3_flux_sectors.py` (pure numpy, deterministic, no RNG; runtime ~3 s),
`results_t3.json`. Everything quoted below is reproduced by `python3 t3_flux_sectors.py`.

**Question.** REPORT.md sec. 7 item 3 / sec. 8: put compact U(1) on T^3 x R, compute the
distribution of the global flux/winding sectors as a function of e^2, its entropy, the Fisher
information I(e^2), and check (a) exponential-family structure over the integer flux lattice,
(b) the entropy-Fisher identity in the predicted form, (c) the prior claim I = 1/(2e^4) per mode
generalized to the rank-b_2 lattice with the metric quadratic form, (d) modular/duality structure.

---

## 1. Setup and derivation (short)

Compact U(1), charge quantum q = 1, Kogut-Susskind normalization
H = (e^2/2) int E^2 + (1/(2e^2)) int B^2, on a flat 3-torus T^3 = R^3/Lambda with lattice basis
a_1, a_2, a_3, Gram matrix G_ij = a_i . a_j, volume V = sqrt(det G). **Choice of T^3 over
T^2 x interval:** T^3 is closed (no boundary conditions to choose, no boundary edge modes to
regulate), carries the maximal number b_1 = b_2 = 3 of independent topological classes, and all
sector labels are exactly superselected; an interval factor would re-introduce precisely the
contested boundary/center structure this calculation is designed to avoid.

Zero modes and their quantization (standard; DW 1506.05792 sec. 2 for the compactness logic):

- **Electric winding** n in Z^3 = H^1(T^3,Z). The Wilson-line holonomies theta_i in [0,2pi) are
  compact (large gauge transformations); their conjugate momenta - the constant-E components
  E = sum_i n_i a_i / V - therefore have integer spectrum. Energy
  E_el(n) = (e^2/(2V)) n^T G n.
- **Magnetic flux** m in Z^3 = H^2(T^3,Z): flux 2 pi m_i through the three 2-cycles (Dirac
  quantization), constant B = sum_i 2 pi m_i a_i / V, energy
  E_mag(m) = ((2pi)^2/(2 e^2 V)) m^T G m.

Both label sets commute with H and with each other; the zero modes decouple **exactly** from the
photon oscillators (free theory; B contains no holonomy zero mode, E's nonzero modes are
orthogonal to the constant mode). In the **strict ground state the labels are superselected and
the distribution is degenerate** (n = m = 0): zero entropy, zero information. The exponential
family lives on the **Gibbs / torus-Hartle-Hawking class of states** at inverse temperature beta
- the exact analog of 2d YM, where t = g^2 A also entered through a Euclidean (Hartle-Hawking)
preparation, not through the Minkowski vacuum of an infinite line. There the sector weights
factor out of the photon free energy exactly:

    p(n) = exp[-(beta e^2/(2V)) n^T G n] / Z_E,
    p(m) = exp[-(beta (2pi)^2/(2 e^2 V)) m^T G m] / Z_M.

**DW dictionary (verified as an identity of parameters, `DW_dictionary` in the json):** for a
rectangular torus (L_1, L_2, L_3), the marginal of class i is a one-dimensional discrete Gaussian
with parameter t_i = beta e^2 L_i^2 / V = e^2 Vol(B_i)/Vol(F_i), where B_i is the (x_i, tau)
2-torus and F_i the transverse T^2 - exactly q_B^2 Vol(B) of Donnelly-Wall 1506.05792 eq. (36)
with q = 1. The T^3 family is the rank-3 (= b_2) generalization of DW's single zero mode.

Only the products beta e^2 L_i^2/V are recoverable - the torus analog of "only t = g^2 A" in 2d
(reflection caveat imports unchanged).

## 2. Results: (a)-(d) all hold

**(a) Exponential family over the integer flux lattice - exact, every metric tested.**
p(n) prop exp(-e^2 R(n)) with natural parameter e^2 itself and sufficient statistic
R(n) = (beta/2V) n^T G n. SVD rank test of {ln p(.; e^2_j)} over 12-point coupling grids
(`A_rank_tests_electric`): sigma3/sigma2 = 6.1e-14 (cubic L=4), 2.2e-14 (anisotropic 2x3x5),
1.6e-13 (sheared metric, Gram [[4,2,0],[2,5,2],[0,2,5]], V=8) - machine-zero curvature, vs
5.1e-2 for the full-range 2+1d ED family (analysis_chain.json). No theta-function corrections to
the *family structure*: the corrections deform Z and the moments, not the exponential form.

**(b) Entropy-Fisher identity in the predicted form.** Since the natural parameter is linear in
e^2 and the base measure is trivial (h = 1 on Z^3), the Lemma of DERIVATION.md gives
dS/de^2 = -e^2 I(e^2) **literally** (the direct descendant of dS/dt = -t I(t)). Verified by
central differences at e^2 = 0.05 ... 12 on all three metrics: worst relative residual 7.5e-10
(`B_entropy_fisher_identity`; the residual is the finite-difference floor).

**(c) Fisher information: finite, and the leading term is *metric-blind*.**
I(e^2) = Var(R), computed exactly from theta sums:

- Per mode: I_i(e^2) = (c_i/2)^2 Var(n_i^2), c_i = beta L_i^2/V; Gaussian (small t_i = c_i e^2)
  asymptote **I_i -> 1/(2e^4)** - confirms the prior claim (results_dipole.json module 2) and
  the e2 <= 1 numbers there.
- Rank-b_2 generalization: for **any** Gram matrix G, Var((beta/2V) n^T G n) ->
  (1/2)(2/(2e^2))^2 tr[(G G^-1)^2-structure] = **b_2/(2e^4) = 3/(2e^4)**: the metric drops out of
  the leading term entirely (Gaussian trace identity; numerically `C_fisher_and_entropy`:
  I * 2e^4/3 = 1 to <= 2e-12 for e^2 <= 0.8 on cubic, anisotropic, and sheared metrics).
- Geometry enters only the quantization corrections, through the per-mode parameters
  t_i = beta e^2 L_i^2/V. The whole correction is one universal curve
  2e^4 I_mode = (t^2/2) Var_t(n^2) (`C_per_mode_crossover_curve`): = 1 to machine precision for
  t <= 0.5, single peak ~= 1.53 near t ~= 5, then ~ (t^2/2) e^{-t/2} freeze-out collapse.
  Anisotropic torus at e^2 = 12 (t = 1.6/3.6/10): per-mode 2e^4 I = 1.002 / 1.311 / 0.656 -
  staggered freeze-out, long directions first.
- Entropy: S -> (b_2/2)[ln(2pi/(beta e^2)) + 1] + (1/2) ln V as e^2 -> 0 - also shape-blind
  (only the volume enters; det G = V^2 cancels the mode-shape dependence). Verified to <= 2e-15
  at e^2 <= 0.4 on all three metrics. Per-mode constant (1/2) + (1/2) ln(2pi) is the U(1)
  heat-kernel constant c_U(1) of Paper 3's appendix - the same number, because the per-class
  marginal IS the U(1) 2d-YM family.
- Finiteness: I(e^2) <= b_2/(2e^4) (1 + bounded correction) for all e^2 > 0; both S and I -> 0
  exponentially as e^2 -> infinity (electric freeze-out), like t -> infinity in 2d YM. b_2 = 3
  modes total: **finite, cutoff-independent, area-independent** - this is the entire point.

**(d) Modular / electric-magnetic structure - exact.**
- Poisson resummation Z_E(alpha; G) = (2pi/alpha)^{3/2} (det G)^{-1/2} Z_E(4pi^2/alpha; G^{-1}),
  alpha = beta e^2/V: verified to machine precision by evaluating S, I, lnZ through both
  representations on the sheared metric (`poisson_identity_sheared`: dlnZ <= 4.4e-16, dI/I <=
  1.2e-15). Weak and strong coupling are exchanged; the dual quadratic form is the dual-lattice
  Gram matrix G^{-1}.
- On the cubic torus with beta = L the electric and magnetic per-mode parameters are t_E = e^2
  and t_M = 4pi^2/e^2, so the magnetic family is *exactly* the Poisson dual of the electric one:
  **S_tot(e^2) = S_tot(4pi^2/e^2)** verified to 0.0 (double precision) at 4 coupling pairs;
  self-dual point e^2 = 2pi.
- **The self-dual point separates entropy from information:** dS_tot/de^2 = 0 there (exactly, by
  duality; finite differences give 0 to the 1e-10 floor) while I_tot = I_E + I_M = 0.10998 > 0
  (-e^2 I_tot = -0.691). The identity dS = -e^2 I fails for the joint family: the ratio
  dS/de^2 / (-e^2 I_tot) runs 1.000 (e^2 = 0.3) -> 0.961 (2.0) -> 0.608 (pi) -> 0 (2pi) ->
  -0.555 (12) -> -1.000 (60) (`joint_identity_ratio`).
- Reason, made exact by the rank test: the **joint** (n, m) family is p prop
  exp[-theta_E T_E - theta_M T_M] with (theta_E, theta_M) = (e^2, 4pi^2/e^2) - a **curved**
  one-parameter path (hyperbola) in a rank-2 exponential family. Joint rank test
  (`joint_rank_test`): sigma3 = 3.005 = O(1) with sigma4/sigma3 = 9.5e-12 (rank exactly 3);
  electric-only control on the identical grid: sigma3 = 1.4e-10. So even in the purely
  topological sector, electric and magnetic labels *jointly* reproduce in miniature the
  crossover/curvature obstruction seen in the bulk flux data (REPORT.md sec. 1.3) - while each
  marginal alone is an exact one-parameter exponential family at all couplings.

## 3. One-paragraph summary for the paper

On T^3 the compact-U(1) topological sector distribution in the Gibbs/Hartle-Hawking family is an
exact one-parameter exponential family in e^2 over the rank-b_2 = 3 integer flux lattice, with
sufficient statistic the metric quadratic form (beta/2V) n^T G n; the 2d-YM identity
dS/de^2 = -e^2 I(e^2) holds verbatim (residual <= 7.5e-10); the Fisher information is finite and
regulator-independent with metric-blind leading term I = b_2/(2e^4) (per-mode 1/(2e^4), confirming
the prior claim), geometry entering only through a universal per-mode freeze-out curve and
exponentially small theta corrections; Poisson duality exchanges the electric family with the
magnetic one (natural parameter prop 1/e^2), making S_tot exactly symmetric under
e^2 -> 4pi^2/e^2 on the self-dual torus - and at the self-dual point the joint
electric-magnetic family exhibits dS = 0 with I > 0, the sharpest possible demonstration that
the joint family is curved (rank 3) even though each marginal is exactly straight (rank 2).

## 4. Caveats (carried into the paper)

1. The family lives on the Gibbs/HH class of states, not the strict T^3 vacuum (where the labels
   are superselected and the distribution is a point mass). Identical in kind to 2d YM's t = g^2 A.
2. Only the dimensionless combinations beta e^2 L_i^2/V are estimable.
3. e^2-dependence exists only because of compactness (integer n); noncompact R gauge theory has
   no normalizable zero-mode ground state at all (DW 1506.05792) and no flux quantization unit.
4. This is the free compact theory: 4d monopole corrections (Coulomb phase, exponentially small
   in 1/e^2) and charged matter are not included; in the confining phase (e^2 > e^2_c ~ 1) the
   electric description changes and the zero-mode statement should be dualized.
