# Reconstructing the Gauge Coupling from Gauge-Invariant Entanglement Statistics: The Exactly Solvable Case of Two-Dimensional Yang–Mills

> **NOTE (2026-06-10, round-2 revision): `paper3/main.tex` is the authoritative manuscript.** This markdown draft predates the round-2 revision implementing the external review's recommendations and is retained for history. The round-2 revision (in `main.tex` only) adds: formal theorem statements with explicit hypotheses (H) for the identity chain dS/dt = −(t/4)Var(C₂), I(t) = ¼Var(C₂), dS/dt = −t·I(t), and the n-cut identity; "compact connected Lie group in the standard 2d YM heat-kernel formulation" scoping with a remark on finite/disconnected groups; an explicit inversion-vs-sampling (channel (A)/(B)) distinction with the additive-counterterm convention stated prominently; a known-vs-new novelty table; finite-sample MLE bias and Wald/profile-likelihood confidence-interval analysis (new script `paper3/mle_bias_ci.py`, results `paper3/mle_bias_ci.json`); a weak-coupling asymptotics appendix with the heat-kernel constant c_G = ln vol(G) − (dim G/2)ln 2π + dim G/2 verified to machine precision (new script `paper3/weak_coupling_check.py`); a seven-point benchmark checklist; and a compressed, programmatic d = 4 discussion with one concrete proposed calculation (Fisher information of compact-U(1) edge-flux sectors across a closed entangling surface).

**William T. Trevena**

*Independent Researcher (PhD, ISE, University of Florida) — trevenaw7@gmail.com*

June 2026

*Acknowledgment: Portions of this manuscript were developed with the assistance of Claude (Anthropic), an AI language model, which contributed to literature synthesis, mathematical exposition, drafting, and the computational experiments. Every formula taken from the literature was verified against the arXiv LaTeX source of the cited paper, not from memory; the verification record is `ym2/FORMULAS.md` in the repository. All numerical claims are reproduced by the published scripts (`ym2/ym2_flux.py`, `ym2/ym2_su3.py`, deterministic seed 20260609). Consistent with COPE authorship guidelines, the AI system is acknowledged as a tool rather than listed as a coauthor.*

---

## Abstract

This is the third paper of a series. The first [P1] showed that "is the coupling hierarchy encoded in vacuum entanglement?" is ill-posed for frame-dependent entanglement; the second [P2] made the question well-posed algebraically and answered it negatively in the minimal toy, where all gauge-invariant entanglement is the classical edge (center) term. This paper presents the positive case the no-gos point to: the one setting where gauge-field entanglement is exactly computable and purely edge — two-dimensional Yang–Mills on a sphere — and where the coupling is not merely reflected in invariant entanglement data but *efficiently estimable* from it. For compact gauge group G in the Hartle–Hawking state, the boundary-flux distribution p_R(t) ∝ (dim R)² e^{−(t/2)C₂(R)}, t = g²A, is a one-parameter exponential family, which yields three exact statements: (i) dS/dt = −(t/4)Var_t(C₂) < 0 — the entanglement entropy is strictly decreasing in the coupling, so t ↦ S(t) is a bijection; (ii) the Fisher information of the flux measurement is I(t) = ¼Var_t(C₂), so entropy susceptibility and statistical reconstructability are the same function, dS/dt = −t·I(t); (iii) the capacity of entanglement is C(t) = t²I(t) → ½dim G as t → 0. Maximum-likelihood reconstruction from N flux samples saturates the Cramér–Rao bound for U(1), SU(2), and SU(3) — the gauge group of QCD: at t = 1, the coupling is recovered to 1.6% from 10³ samples and 0.5% from 10⁴. With n intervals the entropy grows linearly in n through the edge term 2n⟨ln dim R⟩, but the Fisher information does not grow at all: the flux at every cut is one global random variable, so entropy scales while information does not. We state precisely why all of this demonstrates *reflection*, not determination: the inference inverts a known one-parameter family; only the product g²A is recoverable; the edge term that carries it is contested as entanglement; and the one sharp d = 4 computation in the literature has the coupling dropping out. The open question the series leaves is whether any d = 4 analog of this d = 2 encoding exists.

---

## 1. Introduction

### 1.1. The series

This paper completes an arc that began with a question and ends with the only version of an affirmative answer we believe the current literature supports.

**Paper 1** [P1] asked whether the Standard Model coupling hierarchy is encoded in the entanglement entropies of a three-qubit vacuum state, and answered with no-go results: the static matching problem is underconstrained (any hierarchy can be matched; matching is non-evidential), and — the diagnosis that drives everything after it — the question is *ill-posed*, because gauge transformations act on fermionic modes rather than on qubit tensor factors, so the entanglement entropies in question are gauge-frame dependent ([P1], Sec. 9.3).

**Paper 2** [P2] made the question well-posed by replacing subsystem entropies with entanglement relative to the gauge-invariant operator algebra (Barnum–Knill–Ortiz–Viola; Zanardi; in the gauge-field form, Casini–Huerta–Rosabal [CHR]) and computed the answer exactly in the minimal toy. The well-posed answer was a sharper no-go: the single-copy invariant data is the charge-sector distribution alone; the quantum piece of the algebraic entropy vanishes identically for every pure state ("all edge, no bulk"); and the one static "match" of Paper 1 turned out to be pure gauge.

Both papers end at the same object from opposite sides: the *classical center/edge term* of gauge-invariant entanglement — the Shannon entropy of the boundary-flux distribution. Paper 2 showed it is the only gauge-invariant entanglement there is in the toy. The verified literature review accompanying the series showed it is the only place a gauge coupling demonstrably enters entanglement in low dimensions. The natural final question is therefore: **in the best possible case, how much of the coupling does the invariant edge data actually carry, and how efficiently can it be extracted?**

**This paper** answers that question in the one setting where it is exactly solvable: pure Yang–Mills theory in two spacetime dimensions.

### 1.2. The honest thesis

Our thesis has a positive half and a deflationary half, and we state both up front.

*Positive.* In 2d Yang–Mills on a sphere (Hartle–Hawking state, compact group G), the gauge-invariant entanglement data of an interval — the distribution p_R(t) of the boundary electric flux, and the entanglement entropy S(t) built from it — determines the dimensionless coupling t = g²A **exactly and efficiently**: S(t) is strictly decreasing (an identity, not a numerical observation), so the map t ↦ S is a bijection; and an observer who measures the flux N times can estimate t with the smallest variance allowed by statistics, saturating the Cramér–Rao bound, because the flux distribution is an exponential family in the coupling. This includes G = SU(3): in the d = 2 world, the gauge coupling of the strong interaction is reconstructible from gauge-invariant entanglement statistics, and more efficiently than for smaller groups.

*Deflationary.* This demonstrates **reflection, not determination**. The inference presupposes the theory — the group, the state preparation, the known one-parameter family p_R(t) — and recovers the value of a parameter the family was already known to depend on. It does not show that the coupling is *constituted by* entanglement, nor that any of this survives to d = 4, where the only sharp computation of a coupling-sensitive entanglement coefficient finds it independent of the coupling's value [CHMP]. Section 5 makes the deflation precise; Section 6 prices out what d = 3 and d = 4 would require.

The series, in one line: Papers 1–2 eliminated the frame-dependent encodings; this paper exhibits, and quantifies to the statistical limit, the invariant encoding that actually exists in d = 2.

### 1.3. Contributions

Each contribution carries an epistemic label, as throughout the series. "Literature-verified" means checked against the arXiv LaTeX source of the cited paper (record: `ym2/FORMULAS.md`). "Derived" means proven here from literature-verified formulas (the proofs are short and given in full). "Computed" means machine-verified by the published deterministic scripts.

1. **Monotonicity theorem** (derived; computed to stated residuals). For any compact G, the interval entanglement entropy of the Hartle–Hawking state obeys dS/dt = −(t/4)Var_t(C₂) < 0 on t ∈ (0,∞); hence t ↦ S(t) is a smooth bijection (0,∞) → (0,∞) and the coupling is recoverable from the exact entropy. Numerical inversion recovers t to ≤ 9×10⁻¹⁴ across three groups (Sec. 3.2).

2. **Fisher-information identity and Cramér–Rao saturation** (derived; computed). The flux distribution is a one-parameter exponential family with sufficient statistic C₂(R); its Fisher information is I(t) = ¼Var_t(C₂), so dS/dt = −t·I(t): the entropy's sensitivity to the coupling *is* (t times) the statistical information the flux carries about the coupling. Maximum-likelihood estimation from N flux samples saturates the Cramér–Rao bound for U(1), SU(2), SU(3) (Sec. 4).

3. **SU(3) — the QCD group** (computed; new in this paper). The analysis extends to SU(3) with irreps (p,q), dim = (p+1)(q+1)(p+q+2)/2, C₂ = (p²+q²+pq+3p+3q)/3 (convention verified, Sec. 2.3). At t = 1 the coupling is recovered to 1.6% from 10³ samples, 0.5% from 10⁴, at Cramér–Rao efficiency ~1.0. Reconstruction *improves* with group size: I(t) → dim(G)/(2t²) at weak coupling, so the larger the gauge group, the more information each flux sample carries (Sec. 4.3).

4. **Capacity of entanglement** (derived; computed). C(t) ≡ Var(−ln ρ) = t²I(t), with C(t) → ½dim G as t → 0 (verified to 10⁻⁶ at t = 0.05 for all three groups). We found no prior computation of the capacity of entanglement in 2d Yang–Mills (search record in the companion notes); the concept is due to Yao–Qi [YQ10] and was developed in QFT by de Boer–Järvelä–Keski-Vakkuri [dBJK18] (Sec. 3.4).

5. **n intervals: entropy scales, information does not** (derived; computed; the qualitative point is Donnelly's [D14]). For a region of n intervals the entropy is S_n = H[p] + 2n⟨ln d⟩ [D14, eq. (YM2entropy), literature-verified], and we derive dS_n/dt = −(t/4)Var(C₂) − (n−1)Cov(ln d, C₂), strictly negative for all n in all cases computed. But the flux variables at the 2n cut points are *perfectly correlated* — one global R — so the Fisher information is exactly n-independent: more cuts give no new information about the coupling, and a numerical experiment confirms the estimator obeys the N-preparation bound, not the hypothetical 2nN-sample bound (Sec. 3.5). 2d Yang–Mills's flux is one global random variable; the edge entropy counts cut points, not information.

6. **Scope, stated as sharply as the results** (literature-verified). Everything here is d = 2 and purely the contested edge term; only the product g²A is recoverable; and the d = 4 evidence runs *against* naive extrapolation (Secs. 5–6).

---

## 2. Setting and Verified Formulas

**Status: literature-verified (sources and verbatim strings in `ym2/FORMULAS.md`).**

### 2.1. The theory and the state

Pure Yang–Mills theory with compact gauge group G in two Euclidean dimensions is exactly solvable: the heat-kernel lattice action is self-reproducing under plaquette merging, so every amplitude on every surface has a closed form as a sum over irreps [Mig75; Rus90; Wit91; CMR94]. On a closed surface Σ of area V and Euler characteristic χ,

    Z(Σ) = Σ_R (dim R)^χ exp[ −(g²V/2) C₂(R) ],

with C₂ the quadratic Casimir. The theory has no propagating degrees of freedom; by invariance under area-preserving diffeomorphisms, g² and the areas enter only through products g²·(area).

The state is the **Hartle–Hawking (sphere) state** on a spatial circle, the setting of Donnelly's nonabelian analysis [D14]: the wavefunction prepared by the path integral over a hemisphere (disk) of area A/2,

    ψ(R) ∝ (dim R) e^{−(g²A/4) C₂(R)},

expressed in the character basis |R⟩ of the physical Hilbert space (class functions of the circle holonomy). Everything depends on the single dimensionless parameter

    **t ≡ g²A**,    A = total sphere area    (g² has dimension 1/area in d = 2).

### 2.2. The two formulas

Cutting the circle into a region A of n disjoint intervals (2n cut points) and embedding into the extended Hilbert space (one copy of L²(G) per interval), the reduced density matrix is block-diagonal in the boundary irrep R ("electric flux"), with each block maximally mixed over the edge multiplicity space of dimension (dim R)^{2n} [D14]. The two formulas everything in this paper rests on are:

**(F1) Flux distribution** [D14, eq. (pr)]:

    p_R(t) = d_R² e^{−(t/2)C₂(R)} / Z(t),    Z(t) = Σ_R d_R² e^{−(t/2)C₂(R)},     (1)

where d_R = dim R. This is the probability of measuring boundary flux R at the cut — in 2d YM, the Casimir of the boundary electric field is the *only* local gauge-invariant observable [D14]. Note that p_R does not depend on n (Sec. 3.5).

**(F2) Entanglement entropy, n intervals** [D14, eq. (YM2entropy); verbatim from the source: `S = \sum_R p(R) (- \log p(R) + 2n \log \dim R)`]:

    S_n(t) = −Σ_R p_R ln p_R + 2n Σ_R p_R ln d_R = H[p(t)] + 2n⟨ln d⟩_t.     (2)

The same result follows from the Euclidean replica trick on the sphere with n cuts (Gromov–Santos [GS14, eq. (answ)], χ = 2, l = n), up to the additive counterterm discussed below. We use n = 1 except in Sec. 3.5. In the three-term decomposition of [D11], the first term of (2) is the classical (Shannon) piece, the second is the boundary log-dim piece, and the third term — distillable "nonlocal correlations" — **vanishes identically**: the entropy is entirely the edge/center term. This is the field-theory realization of the "all edge, no bulk" structure computed in the toy of [P2].

### 2.3. Group data and conventions

| G | irreps R | dim R | C₂(R) |
|---|---|---|---|
| compact U(1) | n ∈ ℤ | 1 | n² |
| SU(2) | j ∈ {0, ½, 1, …} | 2j+1 | j(j+1) |
| SU(3) | (p,q), p,q ∈ ℤ₊ | (p+1)(q+1)(p+q+2)/2 | (p²+q²+pq+3p+3q)/3 |

**SU(3) convention (verified against standard sources, June 2026).** The Dynkin-label formulas above give C₂(1,0) = 4/3 = (N²−1)/2N for the fundamental and C₂(1,1) = 3 = N for the adjoint — the normalization in which Tr(T_aT_b) = ½δ_ab in the fundamental. This is the same family as C₂(j) = j(j+1) for SU(2) (fundamental: 3/4 = (N²−1)/2N) and matches the convention of [D14]. Both formulas are asserted at runtime in `ym2_su3.py` on the low-lying irreps (1 = (0,0), 3 = (1,0), 3̄ = (0,1), 6 = (2,0), 8 = (1,1), 10 = (3,0)). Any rescaling C₂ → κC₂ — e.g., the 't Hooft-style convention of [GS14], which is 2× ours for SU(2) — is the reparametrization t → κt and changes nothing structural.

**Additive ambiguity.** S carries a t-*independent* additive ambiguity: the local counterterm 2lv of [GS14], the measure/bare-action constant footnoted in [D14], the center-choice ambiguity of [CHR]. We fix it by the extended-Hilbert-space counting (trivial flux sector nondegenerate; S → 0 as t → ∞). The distribution p_R(t) and all t-derivatives of S are ambiguity-free, and the reconstruction below uses only those.

---

## 3. Exact Results

### 3.1. Exponential-family structure

**Status: derived (elementary); the observation that drives the paper.**

Eq. (1) is a one-parameter exponential family in θ = −t/2 with sufficient statistic C₂(R) and base measure d_R². Writing ⟨·⟩, Var, Cov for moments under p(t), the standard cumulant identities give

    d⟨f(R)⟩/dt = −½ Cov_t(f, C₂)   for any statistic f,    d ln Z/dt = −½⟨C₂⟩.     (3)

Everything in Secs. 3.2–3.5 is a corollary of (3).

### 3.2. Monotonicity: S determines t

**Status: derived; computed (machine-verified residuals quoted).**

From (1), the eigenvalues of the reduced density matrix in flux sector R (n = 1) are λ_R = e^{−(t/2)C₂(R)}/Z, each d_R²-fold degenerate, so −ln λ_R = ln Z + (t/2)C₂(R) and

    S(t) = ln Z(t) + (t/2)⟨C₂⟩_t.     (4)

Differentiating with (3):

> **Proposition 1 (monotonicity).** For any compact G,
>
>     dS/dt = −½⟨C₂⟩ + ½⟨C₂⟩ + (t/2)·(−½Var_t(C₂)) = **−(t/4)·Var_t(C₂) < 0**     (5)
>
> for all t > 0, since p(t) has full support on irreps with distinct Casimirs. Z(t) is analytic on (0,∞), so S is smooth and strictly decreasing, with S → ∞ as t → 0⁺ and S → 0 as t → ∞: the map t ↦ S(t) is a bijection (0,∞) → (0,∞). The dimensionless coupling t = g²A is exactly recoverable from the entanglement entropy.

*Computed verification.* On t ∈ [0.05, 20] (400-point geometric grid): S strictly decreasing for U(1), SU(2), SU(3); the analytic derivative (5) matches finite differences to better than 0.3% (SU(2), U(1)) and 0.6% (SU(3)) everywhere on the grid (grid-stencil error), and to 2.4×10⁻¹⁰ with dedicated central differences (Sec. 3.5); max dS/dt on the grid: −6.2×10⁻³ (SU(2)), −4.5×10⁻⁴ (U(1)), −2.6×10⁻⁴ (SU(3)) — bounded away from zero. Practical inversion (given exact S, root-find t) recovers t to ≤ 9×10⁻¹⁴ at six test points per group. The Shannon-only piece H(t) = S − 2⟨ln d⟩ is *not* manifestly monotonic (dH/dt = −(t/4)Var(C₂) + Cov(ln d, C₂), a competition); numerically it is also strictly decreasing for all three groups on the grid, but only the full S has the analytic proof. We flag this honestly because H, not S, is the piece [D14] identifies with uncertainty in gauge-invariant observables.

The weak-coupling behavior is universal, and it is what justifies S → ∞ in Proposition 1: Z(t) = Σ_R d_R² e^{−(t/2)C₂(R)} is the heat kernel of the group manifold G evaluated at the identity, whose short-time behavior is the standard flat divergence Z(t) ≃ vol(G)·(2πt)^{−dim(G)/2} [Cam90; CMR94], so S ≃ ½dim(G)·ln(1/t) + const as t → 0. Computed witness: S(t) + ½dim(G)·ln t is constant to better than 10⁻⁶ over t ∈ [0.002, 0.2] for all three groups, and for U(1) the constant equals the exact heat-kernel value ½ + ½ln 2π = 1.4189385 to seven digits. This is consistent with the weak-coupling scaling of [GS14], and formally the same ½dim(G)·log(coupling) structure as Radičević's d = 3 universal term [R15].

### 3.3. Fisher information: reconstructability = susceptibility

**Status: derived; the framing we believe is new (novelty scan in `paper3/NOTES.md`).**

For the family (1), ∂_t ln p_R = ½(⟨C₂⟩ − C₂(R)), so the Fisher information of one flux measurement is

    I(t) = E[(∂_t ln p_R)²] = **¼ Var_t(C₂)**,     (6)

and the Cramér–Rao bound for any unbiased estimator of t from N i.i.d. flux samples is Var(t̂) ≥ 1/(N·I(t)) = 4/(N·Var_t(C₂)). Comparing (5) and (6):

    **dS/dt = −t·I(t).**     (7)

The entropy's sensitivity to the coupling and the statistical information the flux carries about the coupling are the same function of t, up to the factor −t. Physically, Var_t(C₂) is the flux susceptibility of the vacuum — the object the synthesis of this series identified as "the defensible core" of any coupling-from-entanglement claim. Eq. (7) says that in d = 2 the identification is exact: *entanglement susceptibility is Fisher information.*

*The flux measurement is quantum-optimal.* A referee may ask whether some other measurement on the interval extracts more information about t. No: the reduced density matrices {ρ_A(t)} are all diagonal in the same flux-block basis (eq. (1) with t-independent eigenvectors), so the family is mutually commuting, and the quantum Fisher information of ρ_A(t) equals the classical Fisher information of its eigenvalue distribution [BC94]. Within a block the state is maximally mixed with t-independent weights 1/d_R², carrying no information; the eigenvalue distribution over blocks is p_R(t). Hence QFI(t) = I(t) = ¼Var_t(C₂): the flux measurement saturates the quantum Cramér–Rao bound among all measurements on the interval's algebra, and (6) is not an artifact of a convenient measurement choice.

### 3.4. Capacity of entanglement

**Status: derived; computed. Concept from [YQ10; dBJK18]; we found no prior YM₂ appearance.**

The capacity of entanglement is the variance of the modular Hamiltonian, C(t) ≡ Var(−ln ρ_A) — the entanglement analog of heat capacity [YQ10; dBJK18]. Since −ln λ_R = ln Z + (t/2)C₂(R) is affine in C₂,

    C(t) = (t²/4)·Var_t(C₂) = **t²·I(t)**,    and    dS/dt = −C(t)/t.     (8)

In this model the capacity of entanglement *is* the Fisher information in disguise — a clean instance of the thermodynamic analogy (capacity ↔ heat capacity ↔ fluctuation ↔ information) becoming an identity. Computed: C(t) → ½dim G as t → 0⁺, equal to 0.5000, 1.5000, 4.0000 (U(1), SU(2), SU(3)) at t = 0.05 to the precision quoted in the results files; equivalently S ≃ ½dim(G) ln(1/t) at weak coupling, with the capacity plateau ending around t ~ 1 (SU(3) still 3.995 at t ≈ 3.9).

*Prior work.* Capacity of entanglement was introduced in [YQ10], studied systematically in QFT and holography in [dBJK18], and computed for local-operator excitations of 4d free Yang–Mills in [N21]. We also note the contact with the symmetry-resolved entanglement literature: the flux-block decomposition of ρ_A is precisely a charge/sector-resolved structure in the sense of [GS18; XAS18], and the capacity of entanglement has been used as a probe of RG flows and symmetry resolution in [ADKT23]; our eq. (8) is the YM₂ instance in which the sector distribution alone carries all of the t-dependence. Searches (June 2026; queries recorded in `paper3/NOTES.md`) found no prior computation in 2d Yang–Mills and no prior statement of (6)–(8) there; we flag that the entanglement entropy of YM₂ itself is thoroughly studied [GS14; D14; DTV19; MOPT26], so (8) is best read as low-hanging fruit made visible by the Fisher framing, not as a difficult result.

### 3.5. n intervals: the entropy scales, the information does not

**Status: formula (2) literature-verified; identity (9) derived; non-scaling of information derived and computed; the qualitative point is already in [D14].**

*Setting adopted (stated carefully, since the cut topology matters).* The spatial manifold is the circle in the HH sphere state; region A = n disjoint intervals, complement = n intervals, 2n cut points. The physical state is a class function of the single circle holonomy, ψ = Σ_R c_R|R⟩; iterating Donnelly's embedding map, the character state |R⟩ embeds into the 2n-interval extended Hilbert space with one d_R-dimensional index pair per cut point, all carrying the *same* R. The reduced density matrix is therefore block-diagonal in **one global flux label R** with the *n-independent* distribution p_R(t) of eq. (1), each block maximally mixed of dimension d_R^{2n}. This yields (2), whose log-dim term "appears once for each of the 2n points on the boundary of A" [D14, verbatim]. The replica computation of [GS14] on the sphere with l = n cuts gives the same t-dependence. (On higher-genus surfaces or for non-HH states the sector structure is richer [MOPT26]; we do not use those settings.)

*Entropy.* From S_n = S_1 + 2(n−1)⟨ln d⟩ and (3):

    **dS_n/dt = −(t/4)·Var_t(C₂) − (n−1)·Cov_t(ln d, C₂).**     (9)

Computed: (9) matches central finite differences to ≤ 2.4×10⁻¹⁰ relative over 48 (group, t, n) combinations (U(1), SU(2), SU(3); t ∈ {0.3, 1, 3, 8}; n ∈ {1,2,3,4}). Cov_t(ln d, C₂) > 0 on the full 400-point grid for SU(2) and SU(3) (minima 1.1×10⁻³ and 4.3×10⁻⁵ respectively) and is identically 0 for U(1) (d ≡ 1); so S_n is strictly decreasing in t for every n in all cases computed — each additional pair of cut points makes the entropy *more* coupling-sensitive, by (n−1)Cov.

*Information.* Does Fisher information scale with n — do more cuts mean more flux samples? **No.** The 2n cut-point fluxes of one prepared circle are copies of the single global R: perfectly correlated, joint distribution supported on the diagonal with weights p_R(t). The Fisher information of the joint measurement is therefore exactly I(t) = ¼Var_t(C₂), independent of n. Donnelly states the qualitative point verbatim for the abelian case [D14]: "the entropy is independent of the number of intervals traced out... Having access to an additional interval therefore does not change the amount of information one can acquire about the state." (In the nonabelian case the *entropy* does grow with n — but only through the 2n⟨ln d⟩ edge term, which [D14] notes "is not associated to uncertainty in gauge-invariant observables.")

*Computed demonstration.* M = 400 trials, each preparing N = 1000 independent circles cut into n = 3 intervals (6 cut points, 6000 flux readings, 1000 independent values). The MLE from the 6000-reading dataset is *identical* to the MLE from the 1000 unique samples (duplication leaves the sufficient statistic unchanged; verified to 10⁻¹⁴ relative, exact as estimators), and its standard deviation matches the N-preparation Cramér–Rao bound, not the hypothetical 2nN-sample bound: sd/CRB_N = 0.93 (SU(3)), 0.97 (SU(2)); sd/CRB_{2nN} = 2.27, 2.37 ≈ √6·(sd/CRB_N).

The moral is worth the sentence: **in 2d Yang–Mills, entropy counts cut points; information counts independent preparations.** The edge term 2n⟨ln d⟩ — the dominant part of S_n for large n — carries no additional information about the coupling beyond what one cut already provides. A referee who suspects that "more entanglement entropy" must mean "better reconstruction" has it exactly backwards here, and the structure of the reduced state says why: 2d YM's flux is one global random variable. (Compare the flux-tube entanglement of [ASV24], which likewise depends on the number of boundary crossings and dim R but not on lengths.)

---

## 4. Statistical Reconstruction: MLE Against the Cramér–Rao Bound

**Status: computed (deterministic seed 20260609; M = 400 independent batches per point).**

### 4.1. Protocol

The operational question: an observer who can measure only the gauge-invariant flux observable at one cut draws N i.i.d. samples R₁…R_N from p_R(t*) (N independent preparations; Sec. 3.5 is why repeated cuts of one preparation do not count) and estimates t. Because (1) is an exponential family, the MLE is moment matching — solve ⟨C₂⟩_t = N⁻¹Σᵢ C₂(Rᵢ), which has a unique root since ⟨C₂⟩_t is strictly decreasing by (3) — and asymptotic MLE theory guarantees Cramér–Rao saturation as N → ∞. The content of the demo is quantitative: *how fast*, at physically interesting t, for the groups that matter.

### 4.2. Results

At t* = 1 (M = 400 trials per cell; RMSE of t̂; CRB = √(1/N·I(t*)); ratio = RMSE/CRB):

| group | I(t*=1) | N = 10² | N = 10³ | N = 10⁴ | ratio at 10³ / 10⁴ |
|---|---|---|---|---|---|
| U(1) | 0.500 | 0.1437 | 0.0472 | 0.0141 | 1.05 / 1.00 |
| SU(2) | 1.500 | 0.0800 | 0.0250 | 0.0082 | 0.97 / 1.00 |
| SU(3) | 4.000 | 0.0490 | 0.0162 | 0.0048 | 1.03 / 0.97 |

Errors fall as N^{−1/2} along the CR line. Across all t* ∈ {0.5, 1, 2, 4} at N = 3×10⁴: Var(t̂)/CRB ∈ [0.93, 1.08] (SU(2), U(1), 8 cells) and [0.89, 1.07] (SU(3), 4 cells) — saturation within Monte-Carlo resolution (±~7% at 400 trials). Bias is O(1/N) and negligible (|bias| ≤ 1.4×10⁻⁴ at N = 3×10⁴, SU(3), t* = 1). SU(3) reconstruction at t* ∈ {0.5, 1, 2, 4} and N = 10³ achieves RMSE {0.0080, 0.0162, 0.0318, 0.0650}, i.e. 1.6% relative at t* = 1 and 10³ samples, 0.48% at 10⁴. No clamped batches occurred for SU(3) (the d_R² degeneracy pressure makes all-trivial-sector samples vanishingly rare); the single pathological batch in the whole series remains the U(1), t* = 4, N = 30 cell documented in the Paper-3 results files.

### 4.3. The QCD sentence, and why bigger groups are easier

SU(3) is the gauge group of quantum chromodynamics; the computation above is the statement that **in the d = 2 world, the strong coupling — the dimensionless g²A — is reconstructible from gauge-invariant entanglement statistics at the Cramér–Rao limit.** We confine that sentence to d = 2 with the full force of Section 5.

The group-size trend is itself informative. At weak coupling I(t) ≈ dim(G)/(2t²) (from C(t) → ½dim G and (8)): I(1) = 0.5, 1.5, 4.0 for U(1), SU(2), SU(3). Each flux sample from a larger group carries more information about the coupling, because the Casimir spectrum is richer and the d_R² degeneracy weighting spreads p_R over more, better-separated sectors. The hierarchy-minded reader of Paper 1 will note the irony: in the one solvable setting, the *non-abelian* couplings are the easy ones.

### 4.4. Inversion from the exact entropy

Independent of sampling: given the exact value of S(t*) alone (one number, no samples), root-finding on the strictly monotonic S(·) recovers t* to ≤ 9×10⁻¹⁴ at all test points t* ∈ {0.3, 0.7, 1.5, 3, 6, 12} for all three groups — the bijection of Proposition 1 in practice. We emphasize that this uses the v = 0 normalization (Sec. 2.3); an observer uncertain about the additive counterterm should use derivative or sampling data, which are ambiguity-free.

---

## 5. Scope: What This Does and Does Not Show

**Status: the deflationary half of the thesis; literature-verified where cited.**

1. **It is d = 2, and the solvability is the unrepresentativeness.** There are no propagating gluons; the entire entropy is the edge/center term (the distillable term of [D11] vanishes identically). The features that make the theorem exact — one global flux variable, no transverse physics, area-only dynamics — are precisely the features absent in d = 4. Nothing here is evidence that d = 4 couplings live in entanglement; it is the exact statement of what the best case looks like.

2. **The carrier of the signal is contested as "entanglement."** The edge term is non-distillable and drops out of mutual information and relative entropy in the continuum limit [ST16; MST18]; it depends on the choice of center/boundary algebra [CHR]; and Casini–Huerta–Magán–Pontello [CHMP] argue that in d = 4 Maxwell theory the analogous edge assignment is regularization-dependent, with the physical (anomaly-restoring) effect coming from charged vacuum fluctuations — an effect *independent of the coupling's value*. Our reconstruction reads information out of exactly the term whose physical status is the live dispute. Two mitigations, honestly weighed: (i) the flux distribution p_R(t) itself is an unambiguous, gauge-invariant object whatever one calls its Shannon entropy — the statistical reconstruction of Sec. 4 needs only p_R, not an entropy interpretation; (ii) but an operationalist who insists on distillable entanglement as the only physical entanglement will say this paper reconstructs the coupling from *superselection-sector statistics*, not from entanglement. We think that reading is defensible and the title's "entanglement statistics" should be heard with that asterisk.

3. **Only g²A is recoverable — reflection has a gauge orbit of its own.** By area-preserving diffeomorphism invariance, g² and A enter all observables only through t = g²A [GS14]; "the coupling" is recoverable only relative to a fixed fiducial area. This is the d = 2 echo of the d = 4 obstruction that for noncompact free Maxwell, g can be removed entirely by field redefinition: couplings are scheme-relative quantities, and entanglement data can at best pin down their invariant combinations.

4. **Reflection, not determination — the precise statement.** What is proven: the map t ↦ p(t) is injective (Proposition 1) and its inversion from samples is statistically efficient (Sec. 4). What is presupposed: the group G, the Hartle–Hawking preparation, and the functional form of the family (1) — i.e., the entire theory up to one number. An inference of this shape can never show that couplings *are* entanglement properties; it shows that a known theory's coupling leaves a complete, efficiently readable fingerprint in invariant data. Determination would require, at minimum, an induced-coupling framework in which 1/g² is *defined* by an entanglement functional (the gauge analog of Sakharov/Jacobson induced gravity, flagged as unclaimed territory in the series synthesis) — no such framework exists in the literature we verified.

5. **The additive ambiguity is real but quarantined.** S(t) carries the t-independent counterterm ambiguity (Sec. 2.3). All reconstruction channels used here — p_R(t), t-derivatives of S, sampled fluxes — are ambiguity-free. A claim that needed the absolute value of S would not be.

---

## 6. What d = 3 and d = 4 Would Require

**Status: literature-verified program statement; nothing here is solvable by the methods of this paper.**

**d = 3.** The entropy is no longer all edge: the distillable term of [D11] is nonzero (a propagating photon/gluon), and the boundary flux becomes a *field* on the entangling curve rather than one label. Radičević's weak-coupling analysis [R15] shows the coupling still enters a universal term, ½dim(G)·log(e²r) for a region of size r — formally the same ½dim(G)·log(coupling) structure as our weak-coupling S(t). A d = 3 reconstruction program would need: (i) the joint distribution of boundary fluxes (at weak coupling a Gaussian field with covariance ⟨E_⊥E_⊥⟩ set by e²) — note that unlike our single global R, *this* distribution genuinely has more independent components for larger boundaries, so the n-cuts no-go of Sec. 3.5 is a d = 2 peculiarity, not a general law; (ii) separation of the universal log coefficient from non-universal perimeter pieces; (iii) a stance on the center choice, which in d ≥ 3 affects the sufficient statistics themselves [CHR].

**d = 4.** Three verified facts frame the problem. (i) For noncompact free Maxwell, vacuum entanglement cannot depend on g at all (field redefinition). (ii) For compact U(1), the coupling enters through flux-sector (zero-mode) weights — a finite, topological term [DW16] — and through compactness effects on the edge partition function; this is the closest d = 4 analog of our p_R(t) and the natural first target: *the flux-sector distribution on a compact entangling surface is an exponential family in 1/e² with sufficient statistic the flux quantum number squared*, and a Fisher analysis of it would be a direct (if much weaker) descendant of Sec. 3.3. (iii) With charged matter, the one sharp computation [CHMP] finds the log-coefficient shift universal — independent of the coupling's value and of the charge masses. So in d = 4 the live possibilities are: the coupling enters only through compactness/topology (reconstructible but topological, not local), or only through scale-dependence of coarse-grained flux statistics (the "reconstruction, not identification" conjecture of the series synthesis), or not at all in any distillable quantity. Deciding among these is the open problem the series hands to whoever next enters; the d = 2 result fixes the gold standard such a program should be measured against — exponential-family structure, identity (7), CR saturation — while its own n-cuts lesson warns that gauge theories can manufacture arbitrarily much edge entropy carrying zero additional information.

---

## 7. Conclusion: The Series Closed Into a Point

Paper 1 proved that the frame-dependent version of "couplings from entanglement" is ill-posed and that its static matchings are non-evidential. Paper 2 made the question well-posed with the algebraic (commutant/center) definition and showed that in the minimal toy the well-posed answer is a sharper no-go — and that all gauge-invariant entanglement there is, is the classical edge term. This paper went to the one place where that edge term is an exactly solvable function of a gauge coupling and extracted everything it contains: the coupling is reflected *completely* (bijection), *identifiably* (one global flux variable, with no information inflation from extra cuts), and *efficiently* (Cramér–Rao saturation, for U(1), SU(2), and the QCD group SU(3), with larger groups easier). The exact identities

    dS/dt = −(t/4)Var_t(C₂) = −t·I(t) = −C(t)/t

say in one line what the series learned the long way: in d = 2, entanglement susceptibility, flux susceptibility, Fisher information, and capacity of entanglement are one function, and that function knows the coupling.

What none of this shows is determination. The inference presupposes the theory; the recovered number is the scheme-invariant product g²A; the carrier is a term whose entanglement credentials are contested; and the d = 4 evidence is, if anything, adverse. The honest summary of the series is therefore a conditional: *if* gauge couplings are encoded in vacuum entanglement in the actual world, the encoding must be of the kind exhibited here — gauge-invariant flux statistics, not frame-dependent subsystem entropies — and whether any d = 4 version of that encoding exists, beyond topological zero modes, is the open question. The no-gos cleared the ground; this paper is the one building that provably stands on it; everything taller is future work, and we have priced the lumber.

---

## Appendix A: Reproducibility

All computations are deterministic (seed 20260609) and complete in seconds on a laptop. Repository layout (paths relative to repo root):

- `ym2/FORMULAS.md` — every literature formula with citation and verbatim source string, verified against the arXiv LaTeX of [D14], [GS14], [D11] (fetched 2026-06-09); the convention discrepancies found ([GS14] Casimir ×2; additive counterterm) and resolutions.
- `ym2/ym2_flux.py` — U(1) and SU(2): curves, monotonicity, inversion, MLE/CRB demo. Output: `results.json`, `fig_ym2.png/.pdf`. Runtime ≈ 8 s.
- `ym2/ym2_su3.py` — **new for this paper.** SU(3) (convention asserted at runtime on the irreps 1, 3, 3̄, 6, 8, 10), plus the n-interval analysis for all three groups: identity (9) by central differences, and the Fisher non-scaling demonstration. Output: `su3_results.json`, `fig_su3.png/.pdf`. Runtime ≈ 3 s. Run `python3 ym2_su3.py` (no arguments) for the full pipeline; staged execution (`stage1`, `stage2:0.5,1.0`, `stage2:2.0,4.0`, `stage3`, `merge`) produces bit-identical results via per-component RNG streams `default_rng([SEED, stage, index])`.
- Truncation policy: curve/identity computations keep all irreps with relative weight > e⁻⁸⁰⁰ (truncation error exactly zero in float64); the MLE inner loop uses e⁻¹²⁰ (relative truncation < 10⁻⁵⁰, ~46 orders below Monte-Carlo noise). For SU(3) the irrep sum runs over a (p,q) grid with p,q ≤ √(6·860/t)+2.
- Headline residuals: |S_direct − S_exponential-family| ≤ 3.6×10⁻¹⁵ (SU(3), 400 grid points); identity (9) to 2.4×10⁻¹⁰ (48 combinations); inversion ≤ 9×10⁻¹⁴ (18 test points); capacity plateau ½dim G to < 10⁻⁶ at t = 0.05.

## References

**Companion papers**

- [P1] W. T. Trevena, *Is the Standard Model Coupling Hierarchy Encoded in Three-Qubit Vacuum Entanglement? No-Go Results, an Exact Octonionic Vacuum, and the Surviving Hypothesis Space*, companion paper (2026), repository `paper/draft.md`.
- [P2] W. T. Trevena, *Gauge-Invariant Entanglement in a Minimal Fermionic Toy: The Coupling–Entropy Question Made Well-Posed — and Closed*, companion paper (2026), repository `paper2/sequel_draft.md`.

**2d Yang–Mills solvability**

- [Mig75] A. A. Migdal, *Recursion equations in gauge field theories*, Sov. Phys. JETP 42, 413 (1975).
- [Rus90] B. Rusakov, *Loop averages and partition functions in U(N) gauge theory on two-dimensional manifolds*, Mod. Phys. Lett. A5, 693 (1990).
- [Wit91] E. Witten, *On quantum gauge theories in two dimensions*, Commun. Math. Phys. 141, 153 (1991).
- [CMR94] S. Cordes, G. Moore, S. Ramgoolam, *Lectures on 2D Yang–Mills theory, equivariant cohomology and topological field theories*, arXiv:hep-th/9411210.

**Entanglement in gauge theories: the formulas and their status**

- [D11] W. Donnelly, *Decomposition of entanglement entropy in lattice gauge theory*, arXiv:1109.0036, Phys. Rev. D 85, 085004 (2012).
- [D14] W. Donnelly, *Entanglement entropy and nonabelian gauge symmetry*, arXiv:1406.7304, Class. Quantum Grav. 31, 214003 (2014).
- [GS14] A. Gromov, R. A. Santos, *Entanglement entropy in 2D non-abelian pure gauge theory*, arXiv:1403.5035, Phys. Lett. B 737, 60 (2014).
- [V08] A. Velytsky, *Entanglement entropy in d+1 SU(N) gauge theory*, arXiv:0801.4111, Phys. Rev. D 77, 085021 (2008).
- [CHR] H. Casini, M. Huerta, J. A. Rosabal, *Remarks on entanglement entropy for gauge fields*, arXiv:1312.1183, Phys. Rev. D 89, 085012 (2014).
- [GST15] S. Ghosh, R. M. Soni, S. P. Trivedi, *On the entanglement entropy for gauge theories*, arXiv:1501.02593, JHEP 09 (2015) 069.
- [ST16] R. M. Soni, S. P. Trivedi, *Aspects of entanglement entropy for gauge theories* / *(3+1)-d free U(1) results*, arXiv:1608.00353, JHEP 02 (2017) 101.
- [MST18] U. Moitra, R. M. Soni, S. P. Trivedi, *Entanglement entropy, relative entropy and duality*, arXiv:1811.06986, JHEP 08 (2019) 059.
- [DW14] W. Donnelly, A. C. Wall, *Entanglement entropy of electromagnetic edge modes*, arXiv:1412.1895, Phys. Rev. Lett. 114, 111603 (2015).
- [DW16] W. Donnelly, A. C. Wall, *Geometric entropy and edge modes of the electromagnetic field*, arXiv:1506.05792, Phys. Rev. D 94, 104053 (2016).
- [CHMP] H. Casini, M. Huerta, J. M. Magán, D. Pontello, *On the logarithmic coefficient of the entanglement entropy of a Maxwell field*, arXiv:1911.00529, Phys. Rev. D 101, 065020 (2020).
- [K95] D. Kabat, *Black hole entropy and entropy of entanglement*, arXiv:hep-th/9503016, Nucl. Phys. B 453, 281 (1995).
- [R15] Đ. Radičević, *Entanglement in weakly coupled lattice gauge theories*, arXiv:1509.08478, JHEP 04 (2016) 163.
- [BMV18] A. Blommaert, T. G. Mertens, H. Verschelde, *Edge dynamics from the path integral: Maxwell and Yang–Mills*, arXiv:1804.07585, JHEP 11 (2018) 080.

**2d Yang–Mills entanglement, further**

- [DTV19] W. Donnelly, S. Timmerman, N. Valdés-Meller, *Entanglement entropy and the large N expansion of two-dimensional Yang–Mills theory*, arXiv:1911.09302, JHEP 04 (2020) 182.
- [MOPT26] D. Melnikov, J. T. Oliveira, V. Peixoto, M. Tenser, *States of 2D Yang–Mills and large-volume entanglement*, arXiv:2603.10171 (2026).
- [ASV24] R. Amorosso, S. Syritsyn, R. Venugopalan, *Entanglement entropy of a color flux tube in (1+1)D Yang–Mills theory*, arXiv:2411.12818; and *Entanglement entropy of a color flux tube in (2+1)D Yang–Mills theory*, arXiv:2410.00112, JHEP 12 (2024) 177. *(Cited for the crossing-number dependence of flux-tube entanglement.)*

**Capacity of entanglement, symmetry resolution, estimation**

- [YQ10] H. Yao, X.-L. Qi, *Entanglement entropy and entanglement spectrum of the Kitaev model*, arXiv:1001.1165, Phys. Rev. Lett. 105, 080501 (2010).
- [dBJK18] J. de Boer, J. Järvelä, E. Keski-Vakkuri, *Aspects of capacity of entanglement*, arXiv:1807.07357, Phys. Rev. D 99, 066012 (2019).
- [N21] P. Nandy, *Capacity of entanglement in local operators*, arXiv:2106.00228, JHEP 07 (2021) 019.
- [GS18] M. Goldstein, E. Sela, *Symmetry-resolved entanglement in many-body systems*, arXiv:1711.09418, Phys. Rev. Lett. 120, 200602 (2018).
- [XAS18] J. C. Xavier, F. C. Alcaraz, G. Sierra, *Equipartition of the entanglement entropy*, arXiv:1804.06357, Phys. Rev. B 98, 041106(R) (2018).
- [ADKT23] R. Arias, G. Di Giulio, E. Keski-Vakkuri, E. Tonni, *Probing RG flows, symmetry resolution and quench dynamics through the capacity of entanglement*, arXiv:2301.02117, JHEP 03 (2023) 175.
- [BC94] S. L. Braunstein, C. M. Caves, *Statistical distance and the geometry of quantum states*, Phys. Rev. Lett. 72, 3439 (1994).
- [Cam90] R. Camporesi, *Harmonic analysis and propagators on homogeneous spaces*, Phys. Rep. 196, 1 (1990). *(Short-time heat-kernel asymptotics on group manifolds.)*

**SU(3) representation data (convention check)**

- Standard sources for dim(p,q) = (p+1)(q+1)(p+q+2)/2 and C₂(p,q) = (p²+q²+pq+3p+3q)/3, e.g.: Wikipedia, *Clebsch–Gordan coefficients for SU(3)* (accessed 2026-06-09); A. B. Balantekin et al. lecture notes, *Notes on symmetries in particle physics*, arXiv:2109.12087, and standard group-theory texts (Georgi). Verified to satisfy C₂(1,0) = (N²−1)/2N and C₂(1,1) = N; asserted at runtime in `ym2_su3.py`.

**Algebra-relative entanglement (used in [P2], cited for series continuity)**

- H. Barnum, E. Knill, G. Ortiz, L. Viola, *Generalizations of entanglement based on coherent states and convex sets*, arXiv:quant-ph/0305023, Phys. Rev. A 68, 032308 (2003).
- P. Zanardi, *Virtual quantum subsystems*, arXiv:quant-ph/0103030, Phys. Rev. Lett. 87, 077901 (2001).
