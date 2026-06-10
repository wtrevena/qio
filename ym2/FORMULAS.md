# YM₂ flux statistics: adopted formulas and their sources

**Purpose.** This file fixes, with primary-source citations, every formula used by
`ym2_flux.py` and quoted in `NOTE.md`. Each formula was verified against the LaTeX
source of the cited paper (downloaded from arXiv e-print on 2026-06-09), not from
memory. Where the literature uses different conventions, the discrepancy is
documented and a single convention is adopted explicitly.

Verified sources (LaTeX sources fetched and grepped):

- **[D11]** W. Donnelly, *Decomposition of entanglement entropy in lattice gauge
  theory*, arXiv:1109.0036, Phys. Rev. D 85, 085004 (2012).
- **[D14]** W. Donnelly, *Entanglement entropy and nonabelian gauge symmetry*,
  arXiv:1406.7304, Class. Quantum Grav. 31 (2014) 214003.
- **[GS14]** A. Gromov, R. A. Santos, *Entanglement Entropy in 2D Non-abelian Pure
  Gauge Theory*, arXiv:1403.5035, Phys. Lett. B 737 (2014) 60.
- Standard YM₂ solvability cited therein: A. Migdal, Sov. Phys. JETP 42, 413 (1975);
  B. Rusakov, Mod. Phys. Lett. A5 (1990) 693; E. Witten, Commun. Math. Phys. 141
  (1991) 153; S. Cordes, G. Moore, S. Ramgoolam, arXiv:hep-th/9411210 (the
  reference [D14] cites as "Cordes1994" for the heat-kernel amplitudes).
- **[V08]** A. Velytsky, *Entanglement entropy in d+1 SU(N) gauge theory*,
  arXiv:0801.4111 (the l = 1 special case of [GS14], as noted by [GS14]).
- **[R15]** Đ. Radičević, *Entanglement in Weakly Coupled Lattice Gauge Theories*,
  arXiv:1509.08478 (used only in the outlook of NOTE.md).
- **[BMV18]** A. Blommaert, T. G. Mertens, H. Verschelde, *Edge Dynamics from the
  Path Integral: Maxwell and Yang-Mills*, arXiv:1804.07585 (corroborating edge-mode
  path-integral treatment; not load-bearing here).

---

## 1. Setting

Pure Yang–Mills theory with compact gauge group G on a two-dimensional Euclidean
spacetime. The state is the **Hartle–Hawking / sphere state**: the state on a
spatial circle prepared by the Euclidean path integral over a disk (hemisphere).
In [D14] this is presented as the Hartle–Hawking vacuum of dS₂ with de Sitter
radius r (Euclidean section = round 2-sphere of area 4πr²); by area-preserving
diffeomorphism invariance only the total disk areas matter, so the same formulas
hold for any disk areas A₁ (bra side) + A₂ (ket side) = A.

The spatial circle is cut into **2n points** bounding n disjoint intervals; the
region A is the union of the n intervals. The Hilbert space of an interval is the
extended (gauge-variant-at-endpoints) space L²(G) [D14, §2.2]; the physical space
on the circle is spanned by characters, basis states |R⟩ labelled by irreps R of G.

## 2. Verified formulas

**(F1) Heat-kernel partition function** (Migdal/Rusakov/Witten; quoted as eq. for
Z in [D14], §"Replica trick", and as eq. (10) of [GS14]):

    Z(Σ) = Σ_R (dim R)^{χ(Σ)} exp[ −(q² V / 2) C₂(R) ]

with χ(Σ) the Euler characteristic, V the total area, q the gauge coupling, C₂ the
quadratic Casimir. Verbatim from the [D14] LaTeX source:
`Z = \sum_R (\dim R)^{\chi} e^{-\frac12 V q^2 C_2(R)}`.
The disk (χ = 1) amplitude with boundary holonomy U is correspondingly
Z_disk(U; A) = Σ_R (dim R) χ_R(U) exp[−(q²A/2) C₂(R)].
**Exponent convention adopted: e^{−(q²A/2)C₂(R)}, with the explicit 1/2.**

**(F2) Hartle–Hawking wavefunction** ([D14], eq. labelled `hartlehawking`;
hemisphere of area 2πr², χ = 1):

    ψ(R) ∝ (dim R) · exp[ −π r² q² C₂(R) ]    (= d_R e^{−(q² A_disk/2) C₂(R)})

**(F3) Flux (irrep) probability distribution** ([D14], eq. labelled `pr` and again
in the replica section: `p(R) = (\dim R)^2 e^{-2\pi r^2 q^2 C_2(R)} / Z_1`):

    p_R(t) = d_R² e^{−(t/2) C₂(R)} / Z(t),     Z(t) = Σ_R d_R² e^{−(t/2) C₂(R)}

where we define the single dimensionless control parameter

    t ≡ q² A_sphere     (in [D14]: A_sphere = 4πr², so t = 4π r² q²).

In 2d, q² has dimension 1/area, so t is dimensionless. This p_R is the probability
of measuring boundary irrep ("electric flux") R at the cut; it is the distribution
of the only local gauge-invariant observable of the theory [D14, §3].

**(F4) Entanglement entropy, n intervals (2n cut points)** ([D14], eq. labelled
`YM2entropy`, derived canonically in §2.2 and re-derived by replica trick in the
replica section; verbatim: `S = \sum_R p(R) (- \log p(R) + 2n \log \dim R)`):

    S(t) = Σ_R p_R(t) [ −log p_R(t) + 2n·log d_R ]
         = H[p(t)]  +  2n · Σ_R p_R(t) log d_R

The reduced density matrix is block diagonal in R,
ρ_A = ⊕_R p_R · (1/d_R²)·𝟙_{d_R²} ([D14], eq. for ρ: each block is maximally mixed
over the d_R ⊗ d_R edge multiplicity space, one factor d_R per cut point).
We use **n = 1** (one interval, two cut points) throughout: S = H[p] + 2⟨log d_R⟩.

**(F5) Replica-trick cross-check + additive ambiguity** ([GS14], eqs. labelled
`rhon` and `answ`): on a Riemann surface Σ with l cuts, with local-counterterm
parameter v,

    tr ρ_A^n = e^{−v l (2−2n)} · [Σ_R d_R^{nχ−2l(n−1)} e^{−λ n C₂}] / [Σ_R d_R^χ e^{−λ C₂}]^n
    S = 2lv + ln Z − ⟨ ln( d_R^{χ−2l} e^{−λ C₂(R)} ) ⟩

which for χ = 2 (sphere), l = n intervals, rearranges exactly to (F4) plus the
constant 2lv:  S = 2lv − Σ p_R ln p_R + 2l Σ p_R ln d_R, with
p_R ∝ d_R² e^{−λC₂}. So [GS14] (Euclidean replica) and [D14] (canonical,
extended Hilbert space) agree on the full t-dependence; they differ only by the
additive, t-independent counterterm 2lv. [D14] notes the same ambiguity in a
footnote (an overall constant in the degeneracy d(R) "can be absorbed into the
path integral measure, or by adding a bare Einstein-Hilbert term"; it shifts the
entropy by an additive constant). **We set v = 0**, i.e. the normalization in
which the trivial-flux sector is nondegenerate and S → 0 as t → ∞ (this is the
choice [D14] calls "nice" and is forced by the extended-Hilbert-space counting).

**(F6) General three-term decomposition** ([D11], main result, eq. labelled
`threeterms`; verbatim:
`S(\rho_A) = H(p(R_∂)) + Σ_{l∈L_∂A} ⟨ln dim(r_l)⟩ + ⟨S(ρ_A(R_∂))⟩`):

    S(ρ_A) = H[p(R_∂)]  +  Σ_{boundary links} ⟨ log dim R ⟩  +  ⟨ S(ρ_A(R_∂)) ⟩

In 2d YM there are no bulk degrees of freedom, the third (distillable, "nonlocal
correlations") term vanishes identically, and (F6) reduces to (F4): the entropy is
**entirely** the edge/center term. This is the precise sense of "the EE is purely
the classical edge term" used in the companion literature review.

**(F7) Group data adopted.**
- SU(2): irreps j = 0, ½, 1, …; d_j = 2j+1; **C₂(j) = j(j+1)**.
- compact U(1): irreps n ∈ ℤ; d_n = 1; **C₂(n) = n²**. For U(1) (F4) has no
  log-dim term and S = H[p] exactly ([D14], abelian case, eq. labelled `Su1`).

## 3. Convention discrepancies found, and resolution

1. **Casimir normalization.** [GS14] use 't Hooft-normalized conventions,
   e^{−(A/2N)C₂(R)}, and for SU(2) take C₂ = (m²−1)/2 with m = 2j+1, i.e.
   C₂ = 2j(j+1) — **twice** the standard j(j+1). [D14] uses the standard
   normalization (T_tt = ½q²C₂ with C₂(j)=j(j+1)). Any rescaling C₂ → κC₂ is
   equivalent to t → κt, a smooth reparametrization that changes nothing
   structural. **Adopted: C₂(j) = j(j+1), C₂(n) = n², t ≡ q²A, weight
   e^{−(t/2)C₂}.** When comparing to [GS14] formulas substitute t → t/2 ·(their λ
   conventions) as appropriate.
2. **Additive constant.** See (F5): S is defined up to a t-independent constant
   (2lv in [GS14]; measure/bare-gravitational ambiguity footnoted in [D14];
   the same ambiguity class as in Casini–Huerta–Rosabal, arXiv:1312.1183).
   Adopted: v = 0. The distribution p_R(t) itself and all t-derivatives of S are
   ambiguity-free; the reconstruction demo uses only these.
3. **Exponent factor of 2.** Some references write e^{−g²A C₂} (absorbing the ½
   into g² or C₂). We keep the explicit ½ of (F1)–(F3), matching the [D14] source.

## 4. Exact corollaries derived here (one-line proofs from F3–F4)

These are derived, not taken from the literature; each is verified numerically in
`ym2_flux.py` against finite differences / sampling.

p_R(t) ∝ d_R² e^{−(t/2)C₂(R)} is a one-parameter **exponential family** with
natural parameter θ = −t/2 and sufficient statistic C₂(R). Writing ⟨·⟩ and Var
for moments under p(t), and λ_R = e^{−(t/2)C₂(R)}/Z for the d_R²-fold degenerate
eigenvalues of ρ_A (n = 1):

- **(C1)** S(t) = ln Z(t) + (t/2)⟨C₂⟩.   [since −ln λ_R = ln Z + (t/2)C₂(R)]
- **(C2)** d⟨C₂⟩/dt = −½ Var(C₂);  d ln Z/dt = −½⟨C₂⟩.
- **(C3) Monotonicity theorem.**  dS/dt = −(t/4)·Var_t(C₂)  < 0 for all t > 0.
  (Var_t(C₂) > 0 for every finite t because p_R(t) has full support on irreps with
  distinct Casimirs.) Z(t) is analytic on (0,∞) (locally uniformly convergent sum),
  so S is smooth and **strictly decreasing**: t ↦ S(t) is invertible on (0,∞), and
  S maps (0,∞) onto (0,∞) with S→∞ as t→0⁺ and S→0 as t→∞.
- **(C4) Fisher information.**  I(t) = E[(∂_t ln p_R)²] = ¼ Var_t(C₂).
  Cramér–Rao: any unbiased estimator of t from N i.i.d. flux samples satisfies
  Var(t̂) ≥ 1/(N·I(t)) = 4/(N·Var_t(C₂)).
- **(C5) Susceptibility identities.**  The capacity of entanglement
  C(t) ≡ Var(−ln λ) = (t²/4)Var_t(C₂) = t²·I(t),  and  dS/dt = −t·I(t) = −C(t)/t.
  So the entropy susceptibility, the flux susceptibility Var(C₂), the Fisher
  information, and the capacity of entanglement are all the same function of t up
  to factors of t.
- **(C6) MLE = moment matching.**  For exponential families the likelihood
  equation is ⟨C₂⟩_t = (1/N)Σᵢ C₂(Rᵢ); since ⟨C₂⟩_t is strictly decreasing (C2),
  the MLE t̂ is unique whenever the sample mean lies in (0, ∞), and is found by
  bisection.
- **(C7) Shannon piece.**  H(t) = S(t) − 2⟨ln d⟩, and
  dH/dt = −(t/4)Var(C₂) + Cov_t(ln d_R, C₂). The second term is positive for
  SU(2), so H alone is **not** manifestly monotonic; its behaviour is checked
  numerically and reported honestly in results.json / NOTE.md. (For U(1), d ≡ 1,
  H = S, and (C3) applies directly.)
