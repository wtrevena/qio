# Coupling reconstruction from gauge-invariant entanglement statistics: the exactly solvable case

**Companion artifacts.** `FORMULAS.md` (formulas + citations, each verified
against the arXiv LaTeX source), `ym2_flux.py` (deterministic, seed 20260609),
`fig_ym2.png/.pdf`, `results.json`. All numbers quoted below are reproduced by
`python3 ym2_flux.py`.

---

## 1. Setting and verified formulas

Two-dimensional pure Yang–Mills theory with compact gauge group G is the one
setting where the relation between the gauge coupling and gauge-invariant
entanglement data is exactly solvable, because (i) the theory has no propagating
degrees of freedom, (ii) the heat-kernel solution gives every amplitude in closed
form [Migdal 1975; Rusakov 1990; Witten 1991; Cordes–Moore–Ramgoolam,
hep-th/9411210], and (iii) the entanglement entropy of an interval is *entirely*
the classical edge/center term of Donnelly's decomposition — the third
("nonlocal correlations") term of [D11, eq. (threeterms)] vanishes identically.

The state is the Hartle–Hawking (sphere/disk) state on a spatial circle, the
setting of [D14, §3]: Euclidean dS₂ is a round 2-sphere of area A; the
wavefunction prepared by the hemisphere path integral is
ψ(R) ∝ d_R e^{−(g²A_disk/2)C₂(R)} [D14, eq. (hartlehawking)]. Cutting the circle
into an interval and its complement, the reduced density matrix is block-diagonal
in the boundary irrep ("electric flux") R, with each block maximally mixed over
the d_R × d_R edge space [D14, §2.2]. With the single dimensionless parameter

  **t ≡ g²A**  (A = total sphere area; in 2d, g² has dimension 1/area),

the two formulas everything below rests on are (citations and verbatim source
strings in `FORMULAS.md`):

  **Flux distribution** [D14, eq. (pr)]:
  p_R(t) = d_R² e^{−(t/2)C₂(R)} / Z(t),  Z(t) = Σ_R d_R² e^{−(t/2)C₂(R)}   (1)

  **Entanglement entropy, one interval (two cut points)**
  [D14, eq. (YM2entropy); independently by Euclidean replica trick,
  Gromov–Santos [GS14, eq. (answ)] with χ=2, l=1]:
  S(t) = −Σ_R p_R ln p_R + 2 Σ_R p_R ln d_R               (2)

For SU(2): R = j ∈ {0, ½, 1, …}, d_j = 2j+1, C₂ = j(j+1). For compact U(1):
R = n ∈ ℤ, d_n = 1, C₂ = n², and (2) is pure Shannon entropy [D14, eq. (Su1)].

Two convention points, documented in `FORMULAS.md` §3: (a) [GS14] use a Casimir
normalization that differs from [D14] by a factor of 2 for SU(2) (C₂ = (m²−1)/2 =
2j(j+1)); any rescaling C₂ → κC₂ is the reparametrization t → κt and changes
nothing structural — we adopt C₂(j) = j(j+1). (b) S carries a t-*independent*
additive ambiguity (the local counterterm 2lv of [GS14]; the measure/bare-action
constant footnoted in [D14]; the center-choice ambiguity of Casini–Huerta–Rosabal,
arXiv:1312.1183). We fix v = 0 (trivial flux sector nondegenerate, S → 0 as
t → ∞). The distribution p_R(t) and all t-derivatives of S are ambiguity-free,
and the reconstruction below uses only those.

Note that (1) is exactly the schematic p(R) ∝ (dim term) × e^{−g²·A·C₂(R)·const}
anticipated in the companion literature review (direction_B/LITERATURE_REVIEW.md,
items 3 and 6.3), now made precise: the dim term is d_R², the constant is ½.

## 2. Monotonicity and invertibility: S determines t

Eq. (1) is a one-parameter exponential family with natural parameter −t/2 and
sufficient statistic C₂(R). Writing ⟨·⟩, Var for moments under p_R(t), three
lines of algebra (derived in `FORMULAS.md` §4, verified numerically to 10⁻¹⁵ /
10⁻³ in `results.json`) give

  S(t) = ln Z(t) + (t/2)⟨C₂⟩,
  **dS/dt = −(t/4)·Var_t(C₂) < 0 for all t > 0.**          (3)

Var_t(C₂) > 0 for every finite t (full support on irreps with distinct Casimirs),
and Z(t) is analytic on (0,∞). Hence:

> **Proposition.** For G = SU(2) and G = U(1) (and any compact G), the map
> t ↦ S(t) is smooth and strictly decreasing on (0,∞), with S → ∞ as t → 0⁺ and
> S → 0 as t → ∞. It is therefore a bijection (0,∞) → (0,∞): the dimensionless
> coupling t = g²A is exactly recoverable from the entanglement entropy.

This is "reconstruction" in the weakest, information-theoretic sense —
invertibility of a known one-parameter family — but it is *exact*, with no
non-monotonic region anywhere: numerically, on t ∈ [0.05, 20] (400-point grid),
dS/dt stays below −6.2×10⁻³ (SU(2)) and −4.5×10⁻⁴ (U(1)), and the numerical
derivative matches (3) to better than 0.3% everywhere (finite-difference error).
We also checked the Shannon-only piece H(t) = S − 2⟨ln d⟩, which is *not*
manifestly monotonic (dH/dt = −(t/4)Var(C₂) + Cov(ln d, C₂), a competition):
numerically it too is strictly decreasing on the full grid for SU(2)
(max dH/dt = −5.1×10⁻³), so no honesty caveat is needed here — but only the full
S has the analytic proof. Practical inversion (given exact S, root-find t)
recovers t to ≤ 9×10⁻¹⁴ at six test points per group (`results.json`,
`entropy_inversion_demo`).

Two susceptibility identities tie this to physical language (derived, §4 of
`FORMULAS.md`): the Fisher information of the family (1) is I(t) = ¼Var_t(C₂)
— the flux susceptibility — and the capacity of entanglement is
C(t) = Var(−ln ρ) = t²I(t), so

  dS/dt = −t·I(t) = −C(t)/t.

The entropy's sensitivity to the coupling *is* (t times) the Fisher information
of the flux distribution; statistical reconstructability and entanglement
susceptibility are literally the same function. Numerically C(t) → dim(G)/2 as
t → 0 (1.5000 for SU(2), 0.5000 for U(1) at t ≲ 1), i.e. S ≃ (dim G/2)ln(1/t) +
const at weak coupling — consistent with the weak-coupling scaling of [GS14] and
formally the same ½·dim(G)·log(coupling) structure as Radičević's d=3 universal
term [R15].

## 3. Statistical reconstruction: MLE against the Cramér–Rao bound

The operational version: an observer who can only measure the gauge-invariant
flux observable at the cut (the Casimir of the boundary electric field — in 2d YM
this is the *only* local gauge-invariant observable [D14, §3]) draws N i.i.d.
samples R₁…R_N from p_R(t*) and estimates t. Because (1) is an exponential
family, the MLE is moment matching — solve ⟨C₂⟩_t = N⁻¹Σᵢ C₂(Rᵢ), which has a
unique root since ⟨C₂⟩_t is strictly decreasing — and the Cramér–Rao bound is
Var(t̂) ≥ 1/(N·I(t*)) = 4/(N·Var_{t*}(C₂)).

Demo (`ym2_flux.py`, seed 20260609; M = 400 independent batches per point;
t* ∈ {0.5, 1, 2, 4}; N ∈ {30, …, 30000}). Headline numbers at t* = 1:

| group | N | RMSE(t̂) | CRB √(1/NI) | RMSE/CRB |
|---|---|---|---|---|
| SU(2) | 10² | 0.0800 | 0.0816 | 0.98 |
| SU(2) | 10³ | 0.0250 | 0.0258 | 0.97 |
| SU(2) | 10⁴ | 0.0082 | 0.0082 | 1.00 |
| U(1) | 10³ | 0.0472 | 0.0447 | 1.05 |
| U(1) | 10⁴ | 0.0141 | 0.0141 | 1.00 |

So the coupling is recovered to ~2.5% from 10³ flux samples and ~0.8% from 10⁴
(SU(2), t* = 1), with the error falling as N^{−1/2} along the CR line (fig.
panel c). Across all 8 (group, t*) combinations, Var(t̂)/CRB at N = 3×10⁴ lies in
[0.93, 1.08] — saturation of the Cramér–Rao bound within Monte-Carlo resolution
(±~7% for 400 trials), as guaranteed by asymptotic efficiency of the MLE. Bias is
O(1/N) and negligible (|bias| < 10⁻³ at N = 3×10⁴). One pathological batch in
22,400 (U(1), t* = 4, N = 30: all samples in the trivial sector, MLE at the
bracket edge) is recorded in `results.json` (`n_clamped`).

## 4. Scope: what this does and does not show

Honesty requires deflating this result to its actual size.

1. **It is d = 2.** There are no propagating gluons; the entire entropy is the
   edge/center term (the third term of [D11, eq. (threeterms)] vanishes). The
   solvability that makes the theorem exact is precisely the feature that makes
   the model unrepresentative of d = 4.
2. **The physical status of that term is contested.** The edge term is
   non-distillable and drops out of mutual information and relative entropy in
   the continuum limit [Moitra–Soni–Trivedi, arXiv:1811.06986; Soni–Trivedi,
   arXiv:1608.00353], and it depends on the choice of center/boundary algebra
   [Casini–Huerta–Rosabal, arXiv:1312.1183]. Casini–Huerta–Magán–Pontello
   [arXiv:1911.00529] argue that in d = 4 Maxwell theory the analogous edge
   contribution is a regularization-dependent assignment and that the physical
   (anomaly-restoring) effect comes from charged vacuum fluctuations — and is
   *independent of the coupling's value*. So one cannot read the present result
   as evidence that "couplings live in entanglement entropy" in general: in the
   one sharp d = 4 computation, the coupling drops out.
3. **Reflection, not determination.** The demo shows that the value of t is
   *reflected* in gauge-invariant entanglement data — the map t ↦ p(t) is
   injective and statistically efficient to invert — for a *known* one-parameter
   family of states. It does not show that couplings are *determined by*
   entanglement in any structural sense: the inference presupposes the theory
   (group, state preparation, the family p_R(t)), and what is recovered is only
   the dimensionless product t = g²A. By area-preserving diffeomorphism
   invariance, g² and A enter all observables only through this product
   [GS14, §2], so even in this best case "the coupling" is recoverable only
   relative to a fixed fiducial area — a 2d echo of the d = 4 obstruction that
   for noncompact free Maxwell g can be removed entirely by field redefinition.
4. **Additive ambiguity.** S(t) itself carries the t-independent counterterm
   ambiguity (§1). The reconstruction is clean only because it uses
   t-*derivatives* (equivalently, the distribution p_R(t), which is unambiguous).
   An absolute "value of S" claim would not be.

## 5. Relation to the companion toy model

The companion 3-qubit toy (this repo, `experiments/`; see
direction_B/LITERATURE_REVIEW.md, final section) realizes the identical
structure in finite dimensions: for a gauge-invariant subalgebra with center,
H = ⊕_k H_A^k ⊗ H_B^k and S = H({p_k}) + Σ_k p_k S(ρ_k) [CHR, arXiv:1312.1183].
There, as here, the entire parameter dependence of the "edge" entropy sits in the
classical sector distribution p_k — the toy is also "all edge". 2d YM is the
field-theory member of the same family: k → R, p_k → p_R(t) of eq. (1), with the
bonus that p_R(t) is an exponential family in the coupling, which is what turns
qualitative parameter dependence into a quantitative reconstruction theorem with
a saturated CR bound. The CHR caveat imports unchanged in both cases: H({p_k})
depends on the choice of center; only relative/mutual-information quantities are
choice-independent, and those are exactly the quantities from which the edge term
drops out.

## 6. What the d = 3 analog would require

In d = 3 the entropy is no longer all edge: the third term of [D11] is nonzero
(propagating photon/gluon), and the boundary flux distribution becomes a
distribution over irrep assignments on the entangling *curve*, not a single
global R. Radičević's weak-coupling analysis [R15, arXiv:1509.08478] shows the
coupling still enters a universal term — (1/2)·dim(G)·log(e²r) for a region of
size r — so a d = 3 reconstruction program would need: (i) the joint distribution
of boundary fluxes at the cut (a Gaussian field at weak coupling, with
covariance ⟨E_⊥E_⊥⟩ set by e²), (ii) separation of the universal log coefficient
from the non-universal area/perimeter pieces, and (iii) a stance on the
center-choice ambiguity, which in d ≥ 3 affects the would-be sufficient
statistics themselves. None of that is exactly solvable; the present note is the
boundary case where it all collapses to one line, eq. (3).

---

### References

- [D11] W. Donnelly, *Decomposition of entanglement entropy in lattice gauge theory*, arXiv:1109.0036, PRD 85, 085004 (2012).
- [D14] W. Donnelly, *Entanglement entropy and nonabelian gauge symmetry*, arXiv:1406.7304, CQG 31 (2014) 214003.
- [GS14] A. Gromov, R. A. Santos, *Entanglement Entropy in 2D Non-abelian Pure Gauge Theory*, arXiv:1403.5035, PLB 737 (2014) 60.
- [V08] A. Velytsky, *Entanglement entropy in d+1 SU(N) gauge theory*, arXiv:0801.4111.
- [R15] Đ. Radičević, *Entanglement in Weakly Coupled Lattice Gauge Theories*, arXiv:1509.08478.
- S. Cordes, G. Moore, S. Ramgoolam, *Lectures on 2D Yang-Mills theory, equivariant cohomology and topological field theories*, arXiv:hep-th/9411210.
- H. Casini, M. Huerta, J. A. Rosabal, *Remarks on entanglement entropy for gauge fields*, arXiv:1312.1183.
- H. Casini, M. Huerta, J. M. Magán, D. Pontello, *On the logarithmic coefficient of the entanglement entropy of a Maxwell field*, arXiv:1911.00529, PRD 101, 065020.
- U. Moitra, R. M. Soni, S. P. Trivedi, *Entanglement Entropy, Relative Entropy and Duality*, arXiv:1811.06986.
- R. M. Soni, S. P. Trivedi, *Entanglement Entropy in (3+1)-d Free U(1) Gauge Theory*, arXiv:1608.00353.
- A. Blommaert, T. G. Mertens, H. Verschelde, *Edge Dynamics from the Path Integral: Maxwell and Yang-Mills*, arXiv:1804.07585.
