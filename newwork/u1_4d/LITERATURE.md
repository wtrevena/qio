# Compact U(1) entanglement across a closed surface in d = 3+1: verified literature base

**Scope.** This file supports the question posed by the external review (`new_review.txt`, lines
438–444): *"Does the compact U(1) flux-sector distribution across a closed entangling surface form
an exponential family in 1/e², and how much Fisher information about e does it carry?"*
Every claim below is tagged **[FETCHED 2026-06-10]** (primary source fetched and quoted today),
**[VERIFIED IN direction_B]** (verbatim-verified in `direction_B/LITERATURE_REVIEW.md`, June 2026,
against full texts; spot-rechecked here only where load-bearing), or **[STANDARD]** (pre-arXiv
theorem-grade results cited from the journals).

Search methods used today: arXiv abstract fetches; full-text extraction of the PDF of
arXiv:1506.05792 (≈88k chars, grepped for the flux-sector equations); WebSearch queries
("symmetry-resolved entanglement lattice gauge U(1) flux sector", "compact U(1) entanglement
strong coupling expansion flux sectors Coulomb phase", "Monte Carlo entanglement compact QED
monopoles", "'Fisher information' entanglement 'gauge coupling' flux sectors"). The arXiv API and
arXiv search UI returned empty through the fetch tool; WebSearch was used instead.

---

## 1. Maxwell entanglement and the anomaly mismatch (free, noncompact)

**1.1 Casini–Huerta, arXiv:1512.06182 [FETCHED 2026-06-10].** Abstract, verbatim:

> "We show the entanglement entropy of a Maxwell field is equivalent to the one of two identical
> massless scalars from which the mode of l=0 has been removed. … Using the accepted values for
> these coefficients c_log^S = −1/90 and c_log^{S_{l=0}} = 1/6 we get c_log^M = −16/45, which
> coincides with Dowker's calculation, but does not match the coefficient −31/45 in the trace
> anomaly for a Maxwell field."

Status: **computed** (operator-algebra computation, checked numerically against mutual
information of concentric spheres in the same paper). The mismatch −16/45 vs −31/45 is real for
the *free* field.

**1.2 The free-field coupling no-go [STANDARD / VERIFIED IN direction_B].** In noncompact free
Maxwell theory in d = 4 the coupling can be absorbed by field redefinition A → A/e, so no vacuum
entanglement quantity of the free theory can depend on e. Any e-dependence must enter through
(i) compactness (flux/charge quantization) or (ii) charged matter. This is stated as the central
obstruction in `direction_B/LITERATURE_REVIEW.md` §6 and is used explicitly by Donnelly–Wall
(1506.05792, see 2.3 below) as the reason the U(1)-vs-ℝ distinction is "fundamentally important."

## 2. The contact/edge term and where the coupling enters (Donnelly–Wall)

**2.1 Donnelly–Wall, arXiv:1412.1895 (PRL 114, 111603) [VERIFIED IN direction_B].** The Kabat
contact term is the Shannon/edge entropy of the normal electric field distribution,
S = ∫𝒟E⊥ p(E⊥)[−ln p(E⊥) + S(ρ_{E⊥})]; the edge piece supplies −(1/3)ln r which added to the bulk
−16/45 gives the anomaly value −31/45 (within the conical/extended-Hilbert-space framework).

**2.2 Donnelly–Wall, arXiv:1506.05792 (PRD 94, 104053) [FETCHED 2026-06-10, full PDF text].**
This is the d = 4 (general D, with 2d base B and entangling-surface fiber F) computation where the
coupling demonstrably enters. Verbatim extracts from the fetched text:

- Compactness setup: "Dirac quantization condition, ∮_Ω F ∈ 2π/q for every closed 2-surface Ω";
  and the reason compactness is essential: "while the nonzero modes of a gauge field act like
  harmonic oscillators, the zero modes of the R gauge theory act like free particles, and do not
  have a normalizable ground state. Since we are calculating the ground state entanglement
  entropy, a noncompact gauge group would lead to an infrared divergence … This problem is
  naturally cured in the U(1) gauge theory."
- KK reduction defines a 2d Maxwell theory on the base B with effective charge
  **q_B = q/√Vol(F)** ("Here we have defined q_B = q/√Vol(F), the fundamental charge of the
  two-dimensional Maxwell theory on B").
- **The electric flux-sector partition function, eq. (36) of the paper:**
  Z_E = Σ_{E ∈ q_B ℤ} exp(−½ Vol(B) E²),
  i.e. with E = q_B n, n ∈ ℤ:  **Z_E = Σ_n exp(−(q_B² Vol(B)/2) n²)** — exactly the U(1) 2d-YM
  heat-kernel form p_n ∝ e^{−(t_eff/2)n²} with **t_eff = q_B² Vol(B) = q² Vol(B)/Vol(F)**.
- Its entropic interpretation, verbatim: "When we vary the conical angle β, the volume of B is
  proportional to β, and so the first factor (36) takes the form of a canonical partition
  function. The energy levels are precisely those of the quantized electric field E on the base,
  for which the geometric entropy (1) gives the entanglement entropy [23]."
- Magnetic sector: the bundles wrapping the fiber are "quantized magnetic fields … quantized on
  the lattice (2π/q) H²(F,ℤ)", i.e. weights exp(−const·(2π/q)² m²): natural parameter ∝ 1/q².
- The contact term proper, eq. (38): Z_χ = [√(2π V_F)/q · det′(Δ_0^F)^{−1/2}]^{−χ(B)} — "the
  partition function of a scalar field localized on the entangling surface" with wrong-sign
  exponent; note **the fundamental charge q appears in its prefactor**, so even the contact
  term's finite part is q-dependent in the compact theory.

Status: **computed** (one-loop, Hartle–Hawking-type states on bifurcate-Killing-horizon
backgrounds with product geometry B × F; not a lattice ground-state computation, not arbitrary Σ).

**Reading for our question:** in the one existing d = 4 compact-U(1) entanglement computation, the
electric flux-sector distribution across the entangling surface is literally a discrete Gaussian,
p(n) ∝ exp(−(q_B² Vol(B)/2) n²) — a one-parameter exponential family whose natural parameter is
**proportional to q² (the coupling squared), not 1/q²** — and the magnetic-sector distribution is
the dual family with parameter ∝ 1/q². But it concerns only the *single global (constant) flux
mode*; the joint distribution over local flux patterns on Σ is not computed there.

**2.3 Caveat from the same paper [FETCHED]:** the edge calculation is done "only … at weak
coupling"; strong coupling is explicitly out of scope ("becomes tractable only at strong
coupling" refers to the RT/holography check discussion).

## 3. The compact-U(1)-specific e-dependence is contested as physical

**3.1 Casini–Huerta–Magán–Pontello, arXiv:1911.00529 (PRD 101, 065020) [FETCHED 2026-06-10].**
Abstract, verbatim:

> "the logarithmic term is different for a free Maxwell field and a Maxwell field interacting
> with heavy charges. This is possible because of the presence of superselection sectors in the
> IR theory. However, the correction due to the coupling with charged vacuum fluctuations, that
> restores the anomaly coefficient, is independent of the precise UV dynamics. The problem is
> invariant under electromagnetic duality, and the solution requires both the existence of
> electric charges and magnetic monopoles."

Status: **computed/argued** (real-time operator approach + four-sphere partition function
translation). For our purposes the load-bearing point (verified verbatim in direction_B from the
full text) is that the anomaly-restoring correction is **independent of the value of the
coupling** and of the charge masses — the one sharp d = 4 *universal* entanglement coefficient
involving charges forgets e. So any Fisher information about e must live in non-universal
(cutoff/edge/zero-mode) data, not in the universal log coefficient.

**3.2 Non-distillability of the carrier [VERIFIED IN direction_B].**
- Ghosh–Soni–Trivedi, arXiv:1501.02593: extended-Hilbert-space definition; "agrees with a
  particular case of the definition given by Casini, Huerta and Rosabal" (electric center) for
  U(1); the entropy "does not agree with some standard ways to measure entanglement, like the
  number of Bell pairs … by entanglement distillation."
- Soni–Trivedi, arXiv:1510.07455 [abstract FETCHED 2026-06-10]: "the entanglement entropy does
  not agree with the maximum number of Bell pairs that can be extracted by the processes of
  entanglement distillation or dilution."
- Soni–Trivedi, arXiv:1608.00353 [abstract FETCHED 2026-06-10]: for free U(1) in 3+1d, extended
  Hilbert space: "the result for the logarithmic term in the entanglement, which is universal, is
  given by the a anomaly coefficient. We also consider the extractable part … the coefficient of
  the logarithmic term for the extractable part is different … this difference is accounted for
  by a massless scalar living on the boundary."
- Moitra–Soni–Trivedi, arXiv:1811.06986: the classical/edge term "does not contribute to the
  relative entropy or the mutual information, in the continuum limit."

**3.3 Casini–Huerta–Rosabal, arXiv:1312.1183 [VERIFIED IN direction_B].** Center-choice
ambiguity: the Shannon sector term depends on the choice of center; only mutual/relative
entropies are choice-independent.

## 4. Lattice formulation: where the flux-sector distribution lives

**4.1 Donnelly, arXiv:1109.0036 [VERIFIED IN direction_B].** Three-term decomposition of lattice
gauge EE: Shannon entropy of boundary-representation distribution + Σ p_R ln dim R + nonlocal
term. For U(1): sectors = integer electric fluxes on cut links, constrained by Gauss's law.

**4.2 Soni–Trivedi 1608.00353 / 1510.07455 [FETCHED, abstracts].** Extended-Hilbert-space U(1)
lattice EE: ρ_A block-diagonal in the cut-link electric fluxes {n_e}; the center-sector
distribution appears explicitly in the definition. (In 1506.05792's lattice section, fetched:
"electric flux E_vw ∈ qℤ assigned to each oriented link … must obey Gauss' law"; "the density
matrix can be split into a direct sum of superselection sectors, each labelled by the
[boundary flux]".)

**4.3 Strong-coupling expansions of lattice EE exist but for SU(N) Euclidean replica:**
Aoki–Iritani–Nozaki–Numasawa–Shiba–Tasaki had earlier work; the directly relevant one found
today: arXiv:1503.01766 [abstract FETCHED 2026-06-10], "Strong Coupling Expansion of the
Entanglement Entropy of Yang-Mills Gauge Theories": replica EE to O(β³), "the entanglement
entropy is solely contributed by the central plaquettes enclosing the conical singularity," area
law at O(β³). No U(1) flux-sector *distribution* is extracted there, and no Fisher analysis.

**4.4 Radičević, arXiv:1509.08478 [abstract FETCHED 2026-06-10].** Verbatim: "In two spatial
dimensions, for a region of linear size r, this term equals ½ dim(G) log(e²r) and it dominates
the universal part of the entanglement entropy. Such logarithmic terms arise from the
entanglement of the softest mode in the entangling region with the environment." This is the
d = 3 statement that the coupling enters a universal EE term at weak coupling (through the
softest boundary mode, whose fluctuation width is set by e²).

**4.5 Superselection-resolved lattice studies [FETCHED 2026-06-10, abstract].**
arXiv:2401.01942 (Sela group), "Superselection-Resolved Entanglement in Lattice Gauge Theories":
"when the gauge symmetry is strictly obeyed, superselection-resolved entanglement becomes the
only distillable contribution"; finds corner-law behavior in tensor-network gauge-invariant
states. Closest modern computation of sector-resolved entanglement structure on the lattice; does
**not** compute the sector distribution as a function of the gauge coupling, and not for compact
U(1) ground states.

**4.6 Phase structure of compact U(1) lattice gauge theory [STANDARD].**
- d = 2+1: Polyakov, Nucl. Phys. B120, 429 (1977): confining at **all** couplings; mass gap and
  string tension generated by the monopole plasma; gap m ∝ exp(−const/e²) at weak coupling.
- d = 3+1: Guth, Phys. Rev. D 21, 2291 (1980); Fröhlich–Spencer, Commun. Math. Phys. 83, 411
  (1982): **theorem** — the 4d compact U(1) lattice theory has a deconfined Coulomb (free-photon)
  phase at weak coupling and a confining phase at strong coupling, separated by a transition at
  β = 1/e² ≈ 1.01 (Monte Carlo). In the Coulomb phase the photon is massless, monopoles are
  gapped, and the coupling does not run (pure gauge theory; e labels a line of fixed points up to
  a finite, computable dielectric renormalization).

## 5. What is NOT in the literature (searches of 2026-06-10 + direction_B June 2026)

1. **No paper computes the joint electric-flux-sector distribution p({n_e}) across an entangling
   surface in compact U(1) lattice gauge theory as a function of the coupling** — neither in the
   strong-coupling expansion nor by Monte Carlo nor by exact diagonalization. (1506.05792 computes
   only the constant-flux zero mode on compact B × F backgrounds; 1503.01766 computes replica EE,
   not the sector distribution; 2401.01942 computes sector-resolved entropy of tensor-network
   states, not coupling dependence.)
2. **No paper performs a Fisher-information / estimation-theoretic analysis of gauge-theory flux
   sectors in any dimension above 2** (the d = 2 case being this repo's Paper 3). The WebSearch
   for "Fisher information" + "gauge coupling" + flux sectors returns only unrelated material
   (e.g. arXiv:2407.07969 — entanglement asymmetry as Fisher information in CFT; arXiv:2601.17199
   — flux-tube tomography in (2+1)d YM, which is about string states, not vacuum coupling
   inference).
3. **No Monte Carlo computation of compact-QED entanglement in 3+1d resolved by flux sector**
   (existing lattice EE Monte Carlo: SU(2)/SU(3) c-functions, Z₂ via duality — arXiv:2404.01987,
   arXiv:2304.03311 — and 3d Z₂; nothing sector-resolved for compact U(1)).

## 6. Status table

| Claim | Status | Source |
|---|---|---|
| Free Maxwell d=4 sphere log coefficient = −16/45 ≠ anomaly −31/45 | computed (two independent methods) | 1512.06182, Dowker 1009.3854 [F] |
| Free noncompact Maxwell vacuum EE cannot depend on e | theorem-grade (field redefinition) | folklore; used in 1506.05792 [F] |
| Edge/contact term = Shannon entropy of E⊥ sectors (extended HS / electric center) | computed; framework-dependent | 1412.1895, 1109.0036, 1312.1183, 1501.02593 [V] |
| Compact U(1): electric zero-mode sector distribution = discrete Gaussian, natural parameter ∝ q² | computed (weak coupling, B×F geometry) | 1506.05792 eq. (36) [F] |
| Compact U(1): magnetic sector distribution = dual discrete Gaussian, parameter ∝ 1/q² | computed (same setting) | 1506.05792 [F] |
| Edge term non-distillable; drops from MI/relative entropy in continuum | computed/proven in stated settings | 1510.07455, 1608.00353, 1811.06986 [F/V] |
| Anomaly-restoring charge correction independent of coupling value | computed/argued | 1911.00529 [F] |
| d=3 universal term ½dim(G)log(e²r) at weak coupling | computed (lattice, weak coupling) | 1509.08478 [F] |
| 4d compact U(1): Coulomb + confining phases, transition β≈1.01 | theorem (existence) + MC (location) | Guth 1980, Fröhlich–Spencer 1982 [S] |
| 2+1d compact U(1) confines at all e; gap ∝ e^{−const/e²} | theorem-grade (dilute monopole gas) | Polyakov 1977 [S] |
| Flux-sector distribution p({n_e}) vs coupling across a surface, any lattice compact U(1) ground state | **OPEN — not in the literature** | searches §5 |
| Fisher information of flux sectors about e in d ≥ 3 | **OPEN — not in the literature** | searches §5 |

[F] = fetched today; [V] = verified verbatim in direction_B (June 2026); [S] = standard/journal.
