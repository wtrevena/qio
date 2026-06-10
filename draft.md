# Is the Standard Model Coupling Hierarchy Encoded in Three-Qubit Vacuum Entanglement? No-Go Results, an Exact Octonionic Vacuum, and the Surviving Hypothesis Space

**W. [Author]**

*University of Florida (PhD, Industrial and Systems Engineering)*

June 2026

*Acknowledgment: Portions of this manuscript were developed with the assistance of Claude (Anthropic), an AI language model, which contributed to literature synthesis, mathematical exposition, drafting, and the computational experiments. The "adversarial review" credited at several points in the text — which identified two computational errors and several overclaims corrected in this version, as well as the closed form in Section 8.2 — was performed by an independently instructed instance of the same AI system; a record of the review and the authors' response is published with the code. Consistent with COPE authorship guidelines, the AI system is acknowledged as a tool rather than listed as a coauthor.*

---

## Abstract

Our title question is motivated by emergent spacetime from entanglement and Standard Model structure from the octonions, bridged by Szangolies's three-qubit octonionic Hopf construction of the gauge group. We answer with systematic no-go results, verified with published code. The static version is underconstrained: across 10⁷ Haar-random states, the coupling-matching manifold is statistically generic, intersects the W class, and is matched equally well by random targets, four-qubit systems, and relabeled qubits. Two-qubit states cannot encode unequal couplings. Scale-independent entropies are inconsistent with renormalization-group running. Every canonical octonionic state construction tested is permutation-degenerate. An exactly solvable case sharpens the rigidity: the rotor Hamiltonian with multiplication-table-sign couplings equals i(L_u + 2R_u), u the sum of imaginary units; its unique ground state (√7 e₀ − iu)/√14 is provably convention-invariant and symmetric, with marginal spectra (1/7, 6/7) and 3-tangle equal to each squared concurrence, 8/49. Recognizing Furey's Cl(6) as the three-qubit algebra (Jordan-Wigner) yields charge as Hamming-weight grading — and an obstruction: gauge transformations are not local unitaries of the qubit factorization, so single-qubit entropies are gauge-frame dependent; the GUT normalization of α₁ adds convention-dependence. The title question is thus ill-posed as stated. What survives: gauge-invariant entanglement functionals; hierarchy from flow under an RG-consistent affine map, feasible only for |B| ≳ 126, whose one falsifiable consequence equates a symmetric boundary state with exact unification (SM asymmetry bottoms at 0.029; the MSSM reaches 0.003); and an explanation of why the algebra's canonical vacuum is symmetric. We offer a map of dead and surviving regions, not evidence for the motivating framework.

---

## 1. Introduction

Two largely independent research programs have converged on the idea that quantum information plays a foundational role in physics.

The first, rooted in quantum gravity, begins with Bekenstein's discovery (1973) that black hole entropy scales with horizon area and proceeds through the holographic principle, AdS/CFT, the Ryu-Takayanagi formula, holographic quantum error correction, and Jacobson's thermodynamic derivation of Einstein's equations. These results suggest that spacetime geometry may be emergent from quantum entanglement.

The second, rooted in algebraic particle physics, begins with Günaydin and Gürsey's identification (1973) of SU(3) color within the octonions and proceeds through Dixon's division-algebraic model, Furey's division-algebraic construction of gauge symmetries with correct fermion representations, Todorov's octonionic Clifford algebra approach, and Szangolies's recent connection of this program to qubit entanglement via Hopf fibrations. These results suggest that the internal symmetries of the Standard Model arise naturally from the octonions.

These programs have developed largely in isolation, though some researchers work across quantum information, holography, and algebraic particle physics. The Szangolies construction (2025) provides a concrete bridge: it shows that the Standard Model gauge group appears as a residual symmetry of a three-qubit octonionic Hopf fibration upon dimensional reduction, explicitly connecting gauge structure to quantum entanglement.

These programs jointly motivate a specific quantitative question, which is the subject of this paper: *is the Standard Model gauge coupling hierarchy encoded in the entanglement entropies of a three-qubit vacuum state?* The motivating framework — which we name the Quantum Information Ontology (QIO) and treat strictly as an organizing heuristic (Section 4) — would suggest yes. The body of the paper answers no, in every form of the question we can make precise: we prove the static version is underconstrained, execute the computational program testing it (Section 6), and find every result on the negative-diagnostic side. We then map what survives. Three objects bound the surviving hypothesis space: an entropy-flow form of the conjecture, the affine form consistent with renormalization-group running (Section 7); an exactly solvable octonionic vacuum-selection toy whose canonical vacuum is provably convention-invariant and symmetric (Section 8); and a Jordan–Wigner dictionary making the Furey construction's three-qubit content explicit, whose principal yield is that the program's central quantity — entanglement of the qubit factors — is not gauge-invariant (Section 9). The honest conclusion is that the title question is ill-posed until a gauge-invariant entanglement functional is specified, and we delineate exactly what such a specification must provide.

### 1.1. Contributions

1. **Synthesis.** We connect the emergent-spacetime and division-algebraic programs under a common framework, identifying the Szangolies construction as a bridge.

2. **Observation on spacetime emergence.** We note that Ryu-Takayanagi (spatial emergence) and Page-Wootters (temporal emergence) may describe two aspects of a single informational mechanism. This is suggestive, not a formal result.

3. **Division-algebra uniqueness.** The three-qubit octonionic case is the unique normed-division-algebra Hopf fibration producing the Standard Model gauge group.

4. **Analytic underconstraint result.** We prove that unconstrained three-qubit states can reproduce the observed Standard Model coupling hierarchy at M_Z under a two-parameter logarithmic map, establishing that coupling matching alone is not evidential (Section 5.3).

5. **Minimality of three qubits.** We prove that any two-qubit pure state has S₁ = S₂ identically (Schmidt decomposition), so a two-coupling version of the map is impossible, not merely underconstrained: three qubits is the smallest system on which the ansatz has any content (Section 5.6).

6. **Scale-dependence computation.** We compute that the log-inverse-coupling gap ratio r_SM(μ) varies significantly under one-loop SM running (~24% between M_Z and 10⁶ GeV) and becomes singular near the α₁-α₂ crossing (~10¹³ GeV), establishing that a scale-independent entropy triple cannot match couplings at all scales (Section 6.3). This motivates the entropy-flow reformulation of Section 7.

7. **Characterization of evidential requirements.** We specify what additional constraints would elevate coupling-entropy correspondence from a baseline check to genuine evidence (Section 5.4).

8. **Executed computational program.** We design and execute experiments testing whether algebraically motivated states from the Szangolies construction intersect the coupling-matching manifold (Section 6). Results: across 10⁷ Haar-random states, the matching manifold is statistically generic in its entanglement invariants (Requirement C fails empirically); every canonical octonionic state construction tested yields permutation-degenerate entropies, so none produces a hierarchy; and the matching manifold intersects the W-class (zero 3-tangle) sector, so coupling matching does not even fix the SLOCC class. Four null controls confirm that parameter freedom, not algebraic structure, drives matching.

9. **Entropy-flow form of the conjecture.** We construct an RG-consistent affine form of the coupling-entropy map, α_i⁻¹(μ) = A + B·S_i(μ), under which entropies run linearly in log μ with slopes proportional to one-loop beta coefficients (Section 7). The quantum-marginal (polygon) constraint forces |B| ≳ 126 — a robust bound, binding at M_Z — and the map's single falsifiable consequence is that an entanglement-symmetric boundary state is equivalent to exact coupling unification, which the Standard Model alone does not provide. We state this conditionally and flag its dependence on the abelian normalization convention.

10. **Jordan–Wigner dictionary and the gauge-covariance obstruction.** We make explicit that Furey's Cl(6) construction — three fermionic ladder operators [5, 6, 45] — is the three-qubit operator algebra under the Jordan–Wigner transformation [38], so that electric charge becomes Hamming-weight grading, the color-symmetric quark combination is the W state, and the ν + e⁺ superposition is the GHZ state (Section 9). The isomorphism itself is standard; the yield is the reading, and above all the obstruction it exposes: gauge transformations are not local unitaries of the qubit factorization, so single-qubit entanglement is gauge-frame dependent — an instance of the known relativity of entanglement to a tensor-product structure [46, 47], here with specific consequences: it renders the title question ill-posed as stated.

11. **An exactly solvable octonionic vacuum.** The rotor Hamiltonian H = Σ_{a<b} σ(a,b)·iL_aL_b, with couplings the octonion multiplication-table signs, has the closed form H = i(L_u + 2R_u) where u = Σ_a e_a (Section 8). Its unique ground state (√7 e₀ − iu)/√14 is provably convention-invariant (and confirmed so across all 128 sign gauges, all 5040 index relabelings, the opposite algebra, and right-multiplication operators) and permutation-symmetric, with exact invariants: marginal spectra (1/7, 6/7), and 3-tangle equal to each squared pairwise concurrence, 8/49. We delimit what this does and does not show: the construction is equivalent to distinguishing the direction u/√7 relative to the frame defining the qubit factorization, so the algebra alone does not select a vacuum; and the symmetric outcome extends the permutation rigidity of the canonical kinematic constructions to the dynamical level.

### 1.2. Scope and Limitations

We do not claim to derive the Standard Model, resolve quantum gravity, prove the number of fermion generations, or solve the cosmological constant problem. The QIO is presented as a research program — a framework for organizing results and generating hypotheses — not a completed theory.

---

## 2. The Division-Algebraic Program

The four normed division algebras — ℝ (dim 1), ℂ (dim 2), ℍ (dim 4), 𝕆 (dim 8) — are the only algebras over the reals admitting a multiplicative norm, by the Hurwitz theorem (1898) [1]. The first three are foundational to physics: ℝ in classical mechanics, ℂ in quantum mechanics, ℍ in spinor and Lorentz structure. Whether 𝕆 plays a comparable role has been investigated for fifty years.

### 2.1. Historical Development

**Günaydin and Gürsey (1973)** identified the SU(3) color symmetry of quarks within the automorphism group of the octonions [2].

**Dixon (1994, 2004)** proposed that T = ℝ ⊗ ℂ ⊗ ℍ ⊗ 𝕆 encodes Standard Model structure, including a mechanism for family replication [3, 4].

**Furey (2014)** identified SU_c(3) representations in the Clifford algebra Cl(6), arising from complex octonions, that mirror the chromodynamic structure of three generations of Standard Model fermions — six triplets, six singlets, and their antiparticles [5]. Particle-antiparticle conjugation corresponds to complex conjugation.

**Furey (2018)** constructed the full Standard Model gauge group SU(3)_C × SU(2)_L × U(1)_Y (with possible additional U(1)_X) from division algebraic ladder operator symmetries for a single generation, deriving correct electric charges for all particles. Charge quantization emerges because the relevant number operator takes integer values [6].

**Todorov and Dubois-Violette (2018)** independently derived Standard Model symmetry from the exceptional Jordan algebra and octonionic Clifford algebras, identifying chiral leptons and quarks of one generation as mutually orthogonal idempotents [7, 8].

**Szangolies (2025)** connected this program to quantum information [9]. Building on Mosseri-Dandoloff [10] and Bernevig-Chen [11], Szangolies showed that entangled multi-qubit systems map to Hopf fibrations over the normed division algebras:

| Qubits | Algebra | Hopf Fibration | Residual Symmetry |
|--------|---------|----------------|-------------------|
| 1 | ℂ | S¹ → S³ → S² | U(1) |
| 2 | ℍ | S³ → S⁷ → S⁴ | SU(2) × U(1) |
| 3 | 𝕆 | S⁷ → S¹⁵ → S⁸ | SU(3) × SU(2) × U(1)/Z₆ |

The three-qubit construction admits a dimensional reduction whose residual symmetry is SU(3) × SU(2) × U(1)/Z₆, motivating an information-theoretic route to Standard Model gauge structure [9]. The Hopf maps are entanglement-sensitive: separable states produce no non-abelian gauge structure. The three-qubit octonionic case is the unique normed-division-algebra Hopf fibration producing this gauge group, because no normed division algebra exists beyond the octonions (Hurwitz [1]).

We note that the nexus of three qubits, the Cayley hyperdeterminant, the octonions, and the Fano plane is also the subject of an established and independent body of work — the black-hole/qubit correspondence [44] — in which three-qubit entanglement classification maps onto extremal black-hole solutions of supergravity. Any claim of novelty in this paper concerning three-qubit/octonion structure should be read against that literature; our use of the nexus (coupling hierarchies and vacuum selection) is, to our knowledge, distinct from its use there.

### 2.2. The Three-Generation Observation

Three appearances of "three" in this program deserve attention: Furey's Cl(6) mirrors three generations [5]; Dixon's T accommodates three families [4]; Szangolies requires three qubits [9]. Whether these reflect a single mechanism remains open. Szangolies produces the gauge group but does not derive matter representations or demonstrate that qubit tensor factors map to generations. Furey produces representations mirroring three generations but within a different algebraic framework. The mathematical relationship between these constructions is an important open problem.

We note this coincidence as motivation without claiming it constitutes an explanation.

### 2.3. The Index Ambiguity

In the Szangolies construction, the three tensor factors of ℂ² ⊗ ℂ² ⊗ ℂ² are associated with gauge group structure (the octonionic decomposition produces SU(3) × SU(2) × U(1)/Z₆). If one additionally associates these factors with fermion generations, a framework is needed in which the same structure simultaneously encodes both gauge and flavor information. Such a framework does not currently exist in complete form. This ambiguity affects the coupling-entanglement conjecture in Section 5, where we treat the three qubit factors as corresponding to gauge sectors, consistent with the Szangolies construction. The Jordan–Wigner analysis of Section 9 sharpens this ambiguity: it shows that gauge transformations need not act as local unitaries of any chosen qubit factorization, so the factorization itself is gauge-frame dependent.

It is important to note that gauge group, matter representations, generation structure, Yukawa couplings, and mixing matrices are separate physical targets. The division-algebraic program has made progress on the gauge group and (partially) matter representations. Generations, Yukawas, and mixing remain open.

---

## 3. The Information-Spacetime Convergence

We review results connecting quantum information to spacetime, with epistemic labels.

### 3.1. Bekenstein-Hawking Entropy and Holographic Principle

**Status: Established (semiclassical gravity).**

Black hole entropy scales with horizon area: S = A/(4l_P²) [12, 13]. This area-scaling contrasts with ordinary thermal entropy in local QFT, which is extensive in volume, though vacuum entanglement entropy in QFT also exhibits boundary-area divergences. The holographic principle ('t Hooft [14], Susskind [15]) generalizes: information content is bounded by boundary area in Planck units.

### 3.2. AdS/CFT Correspondence

**Status: Exact duality (vast evidence; no rigorous proof).**

Maldacena (1997) [16] established a duality between (d+1)-dimensional AdS gravity and d-dimensional boundary CFT. Bulk geometry is derived from boundary entanglement. Formulated in AdS (negative cosmological constant), not our de Sitter-like universe.

### 3.3. Ryu-Takayanagi Formula

**Status: Proven within AdS/CFT.**

Entanglement entropy of boundary region A equals the minimal bulk surface area divided by 4G_N [17]. Extended to time-dependent (HRT) and quantum-corrected (QES) settings.

### 3.4. Jacobson's Thermodynamic Derivation

**Status: Established derivation from conditional assumptions.**

Jacobson (1995) [18] derived Einstein's field equations from the Clausius relation applied to local Rindler horizons, assuming Bekenstein entropy-area proportionality. This demonstrates that Einstein's equations can be interpreted as an equation of state. It does not prove gravity is *only* emergent; as Donoghue [19] emphasizes, general relativity is also a valid low-energy effective field theory.

### 3.5. ER=EPR Conjecture

**Status: Conjecture.**

Maldacena and Susskind (2013) [20] proposed that wormholes and entanglement are the same phenomenon. Well-motivated but not established.

### 3.6. Tensor Networks and Holographic Error Correction

**Status: Structural correspondence (tensor networks as models); established within AdS/CFT (error correction).**

Swingle (2012) [21] showed MERA networks provide models of emergent bulk geometry. Almheiri, Dong, and Harlow (2015) [22] showed holographic correspondence has QEC structure. Harlow (2017) [23] showed this matches AdS/CFT bulk reconstruction. Harlow and Ooguri (2019) [24] proved that quantum gravity in AdS forbids global symmetries and requires all gauge charges to be realized.

### 3.7. Entropic Gravity

**Status: Controversial proposal.**

Verlinde (2010) [25] derived Newton's law from entropic arguments. Consistent with Jacobson's result but remains contested; see Visser (2011) [26] for challenges.

### 3.8. Page-Wootters Mechanism

**Status: Framework with experimental illustration in small systems.**

Page and Wootters (1983) [27] showed time can emerge from entanglement in a globally static quantum state (H|Ψ⟩ = 0). Moreva et al. (2014) [28] experimentally illustrated this in an entangled photon system. Favalli (2024) [29] extended to 3+1 dimensions, recovering Schwarzschild time dilation.

---

## 4. The QIO Framework

### 4.1. Organizing Conjecture

**Quantum Information Ontology (QIO):** Spacetime geometry, gravitational dynamics, and gauge symmetries are emergent phenomena arising from the entanglement structure of an underlying quantum system.

We retain the name "ontology" for continuity, but the framework is better described as an *information-first organizing heuristic*: a working assumption that treating quantum information as primary is the most productive way to organize the results reviewed here and to generate hypotheses, not a metaphysical claim we assert or require. None of the technical results in this paper — positive or negative — depends on accepting the ontological reading. This is an organizing conjecture, not a derived conclusion.

### 4.2. Definitions and Open Specifications

Any complete realization of the QIO would require specifying the following objects. We state them here to make explicit what the framework currently leaves undefined:

- **Fundamental Hilbert space H.** The quantum system from which spacetime, gravity, and gauge structure emerge. Its dimension, factorization structure, and relationship to the Szangolies three-qubit space are unspecified. In the coupling-entropy conjecture (Section 5), we work within H = ℂ² ⊗ ℂ² ⊗ ℂ² as a minimal model, without claiming this is the full fundamental space.
- **Vacuum state |Ω⟩.** The specific state in H whose entanglement structure determines physical observables. Identifying |Ω⟩ from first principles requires a selection rule or dynamical principle that the current framework does not provide. (Section 8 reports an algebra-canonical candidate whose vacuum is exactly convention-invariant.)
- **Physical observables.** The operators on H whose expectation values correspond to measurable quantities (coupling constants, masses, mixing angles). The coupling-entropy conjecture (Section 5) proposes that von Neumann entropies of reduced density matrices map to coupling constants, but does not derive this from a Hamiltonian or Lagrangian.
- **Gauge map.** The map from the entanglement structure of |Ω⟩ to the gauge group SU(3) × SU(2) × U(1)/Z₆. The Szangolies construction [9] provides this via the octonionic Hopf fibration, but the full dictionary between entanglement properties and gauge dynamics is not yet established.
- **Spacetime reconstruction.** The map from entanglement entropy to spatial metric. Within AdS/CFT, this is given by the Ryu-Takayanagi formula [17]. Its extension to general spacetimes is conjectural.
- **Time reconstruction.** The mechanism by which temporal evolution emerges. The Page-Wootters mechanism [27] provides a candidate but requires specifying the clock subsystem.
- **Dynamics.** No Hamiltonian, Lagrangian, or equation of motion is provided by the current framework. This is the most significant gap. (Section 8 proposes a candidate at three levels of ambition, with computed and convention-robust results at the second.)

These gaps are not hidden; they define the open problems of the QIO research program.

### 4.3. Claims with Confidence Levels

**High confidence:** Information content of gravitational systems is holographic. Einstein's equations are derivable from information-theoretic assumptions, in the conditional sense of Section 3.4. Within AdS/CFT, spatial geometry is determined by entanglement entropy.

**Moderate confidence:** Several results motivate treating gravity as emergent or thermodynamic rather than as a fundamental gauge interaction. Spacetime may have quantum error-correcting code structure.

**Speculative:** The graviton, if present, may be an effective quasiparticle. If gravity is emergent, QIO reinforces the standard separation between gauge unification (which already involves only three forces in SU(5), SO(10), etc.) and quantum gravity. Coupling constants may be encoded in entanglement entropy.

### 4.4. Observation: Unified Spacetime Emergence

The Ryu-Takayanagi formula describes spatial emergence from entanglement. The Page-Wootters mechanism describes temporal emergence from entanglement. If both operate within a single state satisfying H|Ψ⟩ = 0, space and time emerge from the same substrate through the same mechanism applied to different partitions. This is suggestive, not a formal result. Making it precise requires demonstrating that both can be derived as special cases of a single formalism.

---

## 5. The Coupling-Entropy Question

### 5.1. Motivation

The Szangolies construction shows that gauge structure requires entanglement (separable states produce no gauge symmetry). A natural quantitative question follows: is the *strength* of each gauge interaction related to the *degree* of entanglement supporting it?

The three gauge couplings at M_Z ≈ 91.2 GeV [30]:

    α₃ = 0.1179 ± 0.0010    (SU(3))
    α₂ = 0.03374 ± 0.00003  (SU(2))
    α₁ = 0.01695 ± 0.00002  (U(1), GUT-normalized: α₁ = (5/3)α_Y)

These are free parameters — measured, not derived from any known principle.

### 5.2. Pre-Specified Conjecture

**Conjecture (Logarithmic Coupling-Entropy Map):** There exists a three-qubit pure state |Ω⟩ ∈ ℂ² ⊗ ℂ² ⊗ ℂ² and real constants A, B such that:

    log(α_i⁻¹) = A + B · S_i     for i = 1, 2, 3     ... (1)

where S_i is the von Neumann entropy of the i-th qubit's reduced density matrix, and the qubit-gauge assignment (qubit 1 ↔ SU(3), qubit 2 ↔ SU(2), qubit 3 ↔ U(1)) is fixed by the Szangolies construction. Here "vacuum state" means the state selected in the minimal three-qubit model, not the full continuum QFT vacuum.

We use log(α_i⁻¹) because it compresses the large dynamic range among inverse couplings and converts multiplicative errors into additive errors. This is a simple first ansatz, not a unique consequence of RG theory. We fix this mapping before examining any data and do not consider alternatives.

### 5.3. Analytic Feasibility: The Underconstraint Result

We now prove that the conjecture as stated in Section 5.2 is underconstrained: unconstrained three-qubit states can reproduce the observed hierarchy without physically selecting a vacuum state. This result is central to the paper.

**Lemma (Underconstraint).** Under the two-parameter logarithmic map (Eq. 1), fitting A and B using α₃ and α₂ reduces the prediction of α₁ to a single scalar condition on the entropy triple:

    r_S ≡ (S₁ - S₂)/(S₂ - S₃) = r_SM     ... (2)

where:

    r_SM = [log(α₃⁻¹) - log(α₂⁻¹)] / [log(α₂⁻¹) - log(α₁⁻¹)]
         = (2.138 - 3.389) / (3.389 - 4.078)
         = 1.817     ... (3)

**Proof.** From Eq. (1), A + B·S₁ = log(α₃⁻¹) and A + B·S₂ = log(α₂⁻¹). Subtracting: B(S₁ - S₂) = log(α₃⁻¹) - log(α₂⁻¹). The prediction A + B·S₃ = log(α₁⁻¹) requires B(S₂ - S₃) = log(α₂⁻¹) - log(α₁⁻¹). Dividing these two equations yields Eq. (2). ∎

The condition r_S = 1.817 is a single constraint on the two-dimensional space of ordered entropy triples (S₁ > S₂ > S₃) in [0,1]³. This defines a one-parameter family (a curve) in entropy space.

**Proposition (Feasibility and underconstraint).** The observed Standard Model coupling hierarchy at M_Z is compatible with the one-qubit marginal constraints for pure three-qubit states. Consequently, the unconstrained logarithmic coupling-entropy ansatz is underconstrained and cannot by itself provide evidence for QIO.

*Example.* The entropy triple S₁ = 0.875, S₂ = 0.730, S₃ = 0.650 satisfies r_S ≈ 1.817, matching the gap ratio determined by the observed couplings. Solving S_i = h₂(λ_i) for the smaller eigenvalues of the one-qubit reduced density matrices gives approximately λ₁ = 0.295, λ₂ = 0.204, λ₃ = 0.167. These satisfy the polygon inequalities of Higuchi-Sudbery-Szulc [31]:

    λ_i ≤ Σ_{j≠i} λ_j

with strict inequality for the largest eigenvalue: 0.295 < 0.204 + 0.167 = 0.371. Therefore there exists a pure three-qubit state with these one-qubit reduced spectra. Because the inequalities are strict and h₂ is continuous and strictly increasing on [0, 1/2], nearby eigenvalue triples remain feasible. Since r_S varies continuously and nontrivially in this neighborhood, the level set r_S = r_SM locally contains a continuous one-dimensional family of compatible entropy triples. ∎

**Consequence.** The unconstrained existence of a coupling-matching three-qubit state is a necessary but not sufficient condition for the conjecture to be meaningful. The observed coupling hierarchy lies inside the image of the one-qubit marginal polytope (expressed in reduced-density-matrix eigenvalues) under the binary entropy map, and the matching manifold is a continuous family within this image. Finding such a state in a numerical search is essentially guaranteed and does not constitute evidence for the QIO.

Moreover, even fixing the one-qubit reduced spectra does not generally determine the three-qubit state up to local unitaries. For generic interior points of the three-qubit marginal polytope, additional local-unitary-inequivalent states share the same one-qubit spectra [43]. Thus, the entropy triple is a very coarse invariant, further reinforcing that coupling matching alone cannot identify a physical vacuum.

The unconstrained existence version of the conjecture is falsified only if the target entropy ratio lies outside the feasible region — which it does not. Therefore, the meaningful test must be strengthened: after imposing independently motivated algebraic constraints on |Ω⟩, the conjecture is falsified if no algebraically allowed state produces the observed coupling hierarchy within stated tolerance.

### 5.4. What Would Constitute Evidence

The underconstraint result (Section 5.3) establishes that coupling-entropy matching alone is not evidential. Evidence for a physical coupling-entanglement correspondence requires one or more of the following:

**Requirement A (Algebraic selection).** The vacuum state |Ω⟩ must not be arbitrary. It must be selected from the Szangolies construction, or from three-qubit representatives obtained via an embedding of Furey's Clifford-algebraic structures (constructed in Section 9), or from another independently motivated geometric or algebraic condition. If such a constrained state automatically produces the correct entropy gap ratio (Eq. 2), without fitting, that would be a non-trivial result. (Section 6.2 reports that no canonical octonionic construction satisfies this; Section 8 reports a dynamical candidate.)

**Requirement B (Holdout predictions).** If the state is selected by coupling matching, it must successfully predict independent observables not used in fitting:
- The Weinberg angle θ_W
- The GUT-scale coupling convergence energy
- Qualitative CKM or PMNS structure
- A specific entanglement class (GHZ-type vs. W-type)
- A simple or notable value of the 3-tangle τ₃
- Non-generic local unitary invariants

**Requirement C (Non-genericity).** The coupling-matching states must occupy a distinguished, measure-zero or algebraically special subset of the three-qubit state space. If the matching manifold intersects a known special locus (e.g., the GHZ orbit, the W orbit, a maximal entanglement surface), this would suggest the coupling hierarchy is connected to entanglement structure rather than being an artifact of parametric freedom. (Section 6.1 reports that this requirement fails empirically for unconstrained matching.)

### 5.5. Analytic Pre-Constraints

For completeness, we record the constraints on achievable entropy triples. Each S_i ∈ [0, 1]. The triangle inequality S_i ≤ S_j + S_k holds for all tripartite pure states [32]. For sharper feasibility constraints, the smaller eigenvalues λ_i of the single-qubit reduced density matrices (obtained by solving S_i = h₂(λ_i) with λ_i ∈ [0, 1/2]) must satisfy the polygon inequality λ_i ≤ Σ_{j≠i} λ_j, which Higuchi, Sudbery, and Szulc [31] show is necessary and sufficient for compatibility with a pure n-qubit state.

The required entropy ordering is S₁ > S₂ > S₃ (stronger coupling ↔ more entanglement), with B < 0.

### 5.6. Minimality of Three Qubits

A simple observation, prompted by Control B of the computational program (Section 6.4), deserves analytic statement: for any *two*-qubit pure state, the Schmidt decomposition forces the two single-qubit reduced density matrices to share the same spectrum, so S₁ = S₂ identically. (We verified this numerically as a code check: the maximum of |S₁ − S₂| over 10⁵ random two-qubit pure states is 4 × 10⁻¹⁵, i.e., machine precision.) Consequently, a two-coupling version of the logarithmic map with B ≠ 0 is *impossible*, not merely underconstrained: no two-qubit pure state can encode two unequal couplings under any map of the form of Eq. (1).

Three qubits is therefore the smallest system on which the coupling-entropy ansatz has any content at all. This is a modest but genuine strengthening of the division-algebra motivation: the octonionic (three-qubit) level of the Hopf hierarchy is not merely the level at which the Standard Model gauge group appears (Section 2.1) — it is also the first level at which a coupling hierarchy is even expressible in single-qubit entropies.

---

## 6. Computational Program: Design and Results

The underconstraint result (Section 5.3) reshapes the computational program. The goal is not to find a matching state (which is guaranteed) but to characterize the matching manifold and test whether it intersects algebraically distinguished regions of the three-qubit state space.

This program has now been executed in full. We retain the experimental design as pre-specified and report the results of each experiment in place. Every numerical claim in Sections 5 and 6.3 was independently re-verified as part of the same run (including a cross-check of the coupling inputs against PDG primary values α_em⁻¹ = 127.951, sin²θ_W = 0.23122, which reproduces α₁ to four significant figures and α₂ to within 0.2%, the residual reflecting scheme conventions). Summary plots appear in Figure 1 (`experiments/results/fig1_experiments.pdf`): panel (a) shows the running of r_SM(μ) with its pole, panel (b) the 3-tangle distributions of matched states versus controls, and panel (c) the weighted-W matching curve.

The headline is easy to state: every experiment came out on the negative/diagnostic side. The matching manifold is statistically generic; canonical octonionic constructions cannot produce a hierarchy; and the null controls show that parameter freedom, not algebraic structure, drives matching. These outcomes confirm and sharpen the paper's analytic thesis.

### 6.1. Experiment 1: Characterize the Matching Manifold

**Objective.** Map the set of three-qubit pure states satisfying r_S = 1.817 ± 0.01 and determine its entanglement properties.

**Procedure.** Generate N = 10⁷ Haar-random three-qubit states. (This large sample is not needed to find a matching state — the Underconstraint Lemma guarantees many exist. The sample size is chosen to characterize the *distribution* of entanglement invariants across the matching manifold, which requires dense coverage.) For each, compute S₁, S₂, S₃ (with qubit labels preserved per Szangolies assignment). Retain states satisfying S₁ > S₂ > S₃ and |r_S - 1.817| < 0.01.

For all retained states, compute: 3-tangle τ₃ [33], pairwise concurrences C₁₂, C₁₃, C₂₃, Cayley hyperdeterminant, SLOCC class, and all local unitary invariants.

**Output.** Distribution of entanglement invariants on the matching manifold. Determine whether the matching states differ statistically from Haar-conditioned generic states in their entanglement invariants, especially 3-tangle, pairwise concurrences, local-unitary invariants, and distance to lower-dimensional special loci such as W, biseparable, or symmetric-state families.

**Results.** Of N = 10⁷ Haar-random states, 1,666,906 had the required ordering S₁ > S₂ > S₃ (≈ 1/6, as exchange symmetry requires), and 2,666 matched |r_S − 1.8174| < 0.01 — a match rate of 2.7 × 10⁻⁴ overall (1.6 × 10⁻³ given the ordering). Matching is easy, exactly as the Underconstraint Lemma predicts.

The matching manifold is statistically generic. The 3-tangle distribution of matched states is nearly identical to that of ordering-conditioned Haar controls: Kolmogorov-Smirnov statistic D = 0.031 — a negligible effect size, despite p = 0.023 at these sample sizes; medians 0.326 versus 0.312 (Figure 1b). The fraction of states with τ₃ < 0.01 is approximately 0.1% in both populations, so the matching condition does not concentrate states near the W-class locus or any other special set. Pairwise concurrence distributions do shift relative to the ordering-conditioned controls (KS statistics up to 0.31), as expected from conditioning on entropy gaps; a gap-matched control would be needed to test whether any shift goes beyond what the conditioning forces, and we have not constructed one. Of the invariants listed in the design, τ₃ and the pairwise concurrences were computed; the Kempe invariant and higher local-unitary invariants are left to future work.

**Conclusion: Requirement C (non-genericity, Section 5.4) fails empirically for unconstrained matching.** This converts the paper's analytic underconstraint argument into a measured fact.

### 6.2. Experiment 2: Intersection with Algebraically Motivated States

**Objective.** Test whether states arising from the Szangolies construction, independently constrained by algebraic considerations, lie on or near the coupling-matching manifold.

**6.2.1. Candidate algebraic state families.**

The following families should be tested:

1. **GHZ family.** |ψ_GHZ(θ)⟩ = cos θ |000⟩ + sin θ |111⟩. This family has equal single-qubit entropies (S₁ = S₂ = S₃), so it cannot match the low-energy coupling hierarchy. It represents the symmetric-entanglement limit and serves as a reference.

2. **W state.** |ψ_W⟩ = (|001⟩ + |010⟩ + |100⟩)/√3. Also symmetric under qubit permutation (equal entropies), so it also cannot match the hierarchy directly.

3. **Weighted W family.** |ψ⟩ = a|001⟩ + b|010⟩ + c|100⟩ with |a|² + |b|² + |c|² = 1. This can generate unequal single-qubit entropies and is the simplest analytically tractable family with broken qubit-permutation symmetry. The weighted W family has τ₃ = 0, so it tests whether the matching condition can be realized in the W-type sector rather than in the generic GHZ class. Compute r_S as a function of (a, b, c) and determine whether r_S = 1.817 is achievable.

4. **Octonion-structure states.** States whose amplitudes are related to the Fano plane multiplication table of the octonions, or to coefficients appearing in specific octonionic unit products. A first task of this experiment is to define a concrete map from octonionic structure constants C_{ijk} or Fano-plane incidence data to normalized complex amplitudes a_{ijk} ∈ ℂ² ⊗ ℂ² ⊗ ℂ². Several inequivalent maps are possible (e.g., real amplitudes from signs of structure constants, or complex amplitudes from multiplication table phases), and the result should be tested for robustness across these choices.

5. **Szangolies dimensional-reduction states.** States associated with the preferred complex direction used in the dimensional reduction from the 9+1-dimensional octonionic spacetime to 3+1 dimensions. Different choices of complex structure may yield different three-qubit states; the question is whether any choice produces r_S ≈ 1.817.

**Procedure.** For each family, compute entropy triples and gap ratios r_S analytically where possible, numerically otherwise. If any algebraically motivated state satisfies |r_S - 1.817| < 0.05 without fitting, this constitutes a non-trivial result: the algebraic structure independently selects a state whose entanglement encodes the coupling hierarchy.

**6.2.2. Results.**

The octonion multiplication table was generated by Cayley–Dickson doubling and machine-verified to satisfy e_a e_b = ±e_{a⊕b}. (Convention-independence of the results below was checked separately, in the robustness battery of Section 8.3 and by independent reconstruction from a Fano-triple table in adversarial review.) The findings:

| Family | Entropies (S₁, S₂, S₃) | τ₃ | r_S = 1.8174 reachable? |
|---|---|---|---|
| GHZ(θ) | S₁ = S₂ = S₃ | 4 sin²θ cos²θ | No (r_S undefined) |
| W | (0.918, 0.918, 0.918) | 0 | No (r_S undefined) |
| Weighted W | tunable | 0 | **Yes — continuous curve** |
| Octonion sign-row / sign-convolution map | (0.811, 0.811, 0.811) | 0.25 | No |
| Octonion diagonal map σ(a,a) | (0.811, 0.811, 0.811) | 0.25 | No |
| Fano incidence (uniform over e₁…e₇) | (0.349, 0.349, 0.349) | 0.082 | No |
| Uniform over e₀…e₇ | (0, 0, 0), separable | 0 | No |
| Quaternionic-line states (all 7 Fano lines) | degenerate: (0,0,0), (1,1,0) perms, or (1,1,1) | 0 or 1 | No |
| Preferred-complex-direction (e₀ + i e_ℓ)/√2, ℓ = 1…7 | degenerate: (0,0,0), (1,1,0) perms, or (1,1,1) | 0 or 1 | No |

Two sharp results emerge:

1. **Every canonical octonionic construction tested yields permutation-degenerate entropies** — all three equal, or degenerate {0,0,0}/{1,1,0}/{1,1,1} patterns. None can produce a three-way hierarchy; r_S is undefined (0/0) on all of them. The algebra's symmetry (G₂ automorphisms, triality, the XOR-grading of the basis) is too rigid: producing a hierarchy requires symmetry breaking beyond the choice of a preferred unit. This sharpens Requirement A (Section 5.4): whatever selection principle the framework eventually supplies, it cannot be any of the obvious "canonical state" maps from octonionic structure data. (Section 8 explores a dynamical route to such symmetry breaking.)

2. **The matching manifold intersects the W-class (τ₃ = 0) sector.** The weighted-W family contains a continuous one-parameter curve of states satisfying r_S = 1.8174 exactly — an explicit example is S = (0.978, 0.895, 0.849) with τ₃ = 0 (Figure 1c; weights in `experiments/results/exp2_results.json`). Coupling matching therefore does not even discriminate between SLOCC classes: both GHZ-class and W-class realizations exist.

Note: Furey's Clifford-algebraic construction [5, 6] does not directly produce three-qubit quantum states. At the time the program was designed, defining an embedding map from Cl(6) structures to ℂ² ⊗ ℂ² ⊗ ℂ² appeared to be an open mathematical problem. It is not: the Jordan–Wigner transformation provides the canonical isomorphism, and Section 9 develops its consequences.

### 6.3. Analytic Result: Scale Dependence of r_SM(μ)

We compute r_SM(μ) across energy scales. This is not a proposed experiment — it is a completed calculation.

The one-loop RG equations, with the convention dg_i/d(log μ) = b_i g_i³/(16π²), give:

    α_i⁻¹(μ) = α_i⁻¹(M_Z) - (b_i/2π) log(μ/M_Z)     ... (4)

    (b₁, b₂, b₃) = (41/10, -19/6, -7)

We compute the log-inverse-coupling gap ratio at representative one-loop extrapolated scales:

| μ (GeV) | α₃⁻¹(μ) | α₂⁻¹(μ) | α₁⁻¹(μ) | r_SM(μ) |
|---------|----------|----------|----------|---------|
| 10      | 6.02     | 28.52    | 60.44    | 2.072   |
| 91.2 (M_Z) | 8.48 | 29.64    | 59.00    | 1.817   |
| 10³     | 11.15    | 30.85    | 57.43    | 1.637   |
| 10⁶     | 18.85    | 34.33    | 52.93    | 1.385   |
| 10⁹     | 26.54    | 37.81    | 48.42    | 1.430   |
| 10¹²    | 34.24    | 41.29    | 43.91    | 3.042   |
| 10¹³    | 36.80    | 42.45    | 42.41    | near pole |

**Result:** r_SM(μ) varies by approximately 24% between M_Z and 10⁶ GeV, and the denominator crosses zero near 10¹³ GeV where α₁⁻¹ and α₂⁻¹ cross. A fixed entropy triple (S₁, S₂, S₃) satisfying r_S = 1.817 at M_Z cannot simultaneously match the coupling hierarchy at other scales.

**Interpretation:** The logarithmic coupling-entropy map with scale-independent entropies is inconsistent with RG running. Either:

(a) The logarithmic map is the wrong ansatz and a different functional relationship holds, or

(b) The entropies themselves must run with energy scale, S_i = S_i(μ), introducing "entanglement renormalization flow" that the current framework does not specify, or

(c) The coupling-entropy correspondence holds only at a specific privileged scale (e.g., the Planck scale), with RG running accounting for the departure at lower energies.

Regarding option (c): the divergence of r_SM near 10¹³ GeV is not full gauge coupling unification — it occurs when α₁ and α₂ cross while α₃ remains distinct. The non-supersymmetric Standard Model does not produce exact three-coupling unification at one loop. Exact symmetric entanglement S₁ = S₂ = S₃ would correspond, under the logarithmic map, to exact equality of all three couplings, making the gap ratio indeterminate (0/0). Thus, the symmetric-entanglement interpretation should be treated as a property of hypothetical exact UV unification (which may require beyond-SM physics), not as something established by SM one-loop running. Nonetheless, the qualitative direction — couplings converging at high energy corresponding to entanglement symmetry becoming more equal — remains a suggestive feature of the framework.

This computation is the direct motivation for the reformulation developed in Section 7, which takes option (b) seriously: it replaces the static logarithmic map with a linear map under which the entropies run with scale, and shows that quantum-marginal constraints then acquire genuine restrictive power.

### 6.4. Null Controls

Since the underconstraint result establishes that matching is easy, the null controls should test *non-genericity* — whether the Standard Model coupling hierarchy selects algebraically special states compared to generic targets.

**Control A (Non-genericity of SM target).** For randomly sampled coupling triples (log-uniform on [0.001, 0.5], ordered), compute the corresponding entropy-gap ratios and characterize the matching manifolds. Compare the entanglement-class distributions, 3-tangle distributions, and local unitary invariant distributions against the Standard Model target. The null question is not whether random targets can be matched (they can), but whether the SM target selects a more algebraically special matching manifold than generic targets.

*Result.* It does not. Across random coupling targets, the SM-target matched states have mean τ₃ = 0.320 versus 0.337 ± 0.018 for random targets — a deviation of z = −0.92, well within statistical noise. The Standard Model coupling hierarchy is statistically indistinguishable from a random coupling target as far as its matching manifold is concerned.

**Control B (Two-qubit comparison).** Two-qubit states have two single-qubit entropies, not three, so the three-coupling logarithmic map is not directly comparable. This control tests whether a two-entropy map (fitting two couplings with one free parameter, no holdout) achieves comparable matching quality.

*Result.* The two-qubit map is not merely weaker — it is impossible. Any two-qubit pure state has S₁ = S₂ identically by the Schmidt decomposition, so no two-qubit state encodes two unequal couplings under the map with B ≠ 0. This analytic observation, which emerged from this control, is stated as a result in Section 5.6: three qubits is the minimal system on which the ansatz has any content.

**Control C (Four-qubit comparison).** Four-qubit states (30 real parameters) do not correspond to a normed division algebra. This control tests whether the algebraic restriction to three qubits, rather than parameter count, selects anything special.

*Result.* It does not. The per-triple match rate for four-qubit states is 3.4 × 10⁻⁴, versus 2.6 × 10⁻⁴ for three qubits in the same N = 10⁶ control run (the Experiment 1 run at N = 10⁷ gives 2.7 × 10⁻⁴; the difference is sampling noise), and 1.3 × 10⁻³ if any of the four ordered triples is allowed to match. Four-qubit systems match at least as easily as three-qubit systems: parameter freedom, not division-algebra structure, drives matching.

**Control D (Shuffled labels).** Test all six qubit-gauge permutations. If the Szangolies construction supplies a physically meaningful labeling of the three qubit factors, the corresponding assignment should be distinguishable from arbitrary permutations in the entanglement-invariant structure of the matching manifold.

*Result.* All six permutations match at statistically identical rates (256–292 matches per 10⁶ states), as the exchange symmetry of the Haar measure requires. The Szangolies labeling currently carries no measurable content for unconstrained states. Section 9.3 offers a structural explanation: gauge transformations are not local unitaries of the qubit factorization, so no unconstrained entanglement statistic can privilege one labeling.

### 6.5. Implementation

Python (NumPy/SciPy). Haar-random states via complex Gaussian normalization. Partial traces via tensor reshaping. Von Neumann entropy from eigenvalues of reduced density matrices. All code, fixed random seeds, and raw outputs (JSON) are published with this paper in the `experiments/` directory for reproducibility.

---

## 7. The Entropy-Flow Reformulation

### 7.1. The Revised Conjecture

The scale-dependence computation (Section 6.3) established that a fixed entropy triple cannot match the couplings at all scales under the static logarithmic map. Of the three options identified there, we now develop option (b) — scale-dependent entanglement — into a precise reformulation.

**Conjecture (Entropy-Flow Map).** There exist real constants A and B (with B < 0) and a one-parameter family of three-qubit pure states |Ω(μ)⟩ such that

    α_i⁻¹(μ) = A + B · S_i(μ)    for i = 1, 2, 3     ... (5)

with the qubit-gauge assignment fixed by the Szangolies construction as before. Substituting the one-loop running (Eq. 4) gives the flow equation

    dS_i / d log μ = −b_i / (2πB)     ... (6)

so the entropies run *linearly* in log μ, with slopes proportional to the one-loop beta coefficients.

Two features make this reformulation better than the static logarithmic map, rather than merely different. First, it is RG-consistent at all scales *by construction*: the scale-dependence failure of Section 6.3 dissolves rather than being patched. Second, it has a conceptual basis rather than a curve-fitting one. The beta coefficients b_i count the degrees of freedom charged under each gauge factor, and entanglement entropy in critical systems is known to run logarithmically with scale, with coefficients that count degrees of freedom — this is the content of the Zamolodchikov c-theorem [39] and its entropic formulation by Casini and Huerta [40]. The slogan: *coupling running and entanglement running are the same bookkeeping.* This also connects the conjecture to entanglement renormalization (MERA) [42], which is already the framework's bridge to holography via Swingle's correspondence [21].

**Honesty clause.** The entropy-flow map, like its static predecessor, is a reparametrization of measured couplings: given any running α_i⁻¹(μ) and any (A, B), Eq. (5) *defines* a trajectory S_i(μ). Its only possible content lives in three places: (i) the quantum-marginal feasibility constraints on (A, B) (Section 7.2) — though these constrain only the unobservable map parameters, not any observable; (ii) the boundary condition at the symmetric point (Section 7.3), which is the map's single falsifiable consequence; and (iii) the counting interpretation of the slopes, which remains open and is where any genuine physical content would have to reside. We present this map as the surviving affine form of the conjecture — we do not claim uniqueness among all functional forms (per-coupling constants (A_i, B_i), for instance, are equally RG-consistent and even less constrained) — and not as evidence for it.

### 7.2. The Marginal Constraints Do Real Work

**Status: Computed (Experiment 3; results in `experiments/results/exp3_results.json`).**

For the trajectory S_i(μ) to be realizable by pure three-qubit states at every μ ∈ [M_Z, M_Planck], the constants (A, B) must satisfy S_i(μ) ∈ [0, 1] together with the Higuchi-Sudbery-Szulc polygon inequality [31] at every scale. Scanning the (A, B) plane:

- The box constraint S ∈ [0,1]³ alone requires |B| ≥ ~51. Adding the polygon inequality raises this to **|B| ≳ 126.5** — a bound we verified to be robust against enlarging the scan region and against moving the UV endpoint from M_Planck down to 10¹⁶ GeV. The feasible region itself is unbounded (larger A forces proportionally larger |B|), so no statement about its "fraction" or about an upper bound on A is meaningful; the lower bound on |B| is the entire content of the constraint.

- Two honest deflations, found in adversarial review of this work and verified. First, the constraints *bind at M_Z alone*: imposing feasibility only at M_Z yields the identical feasible (A, B) set as imposing it at every scale, because the coupling spread is widest at M_Z. The flow adds no restrictive power beyond the static affine map at one scale. Second, the constraints restrict only the unobservable parameters (A, B); since the feasible set is non-empty, nothing observable is constrained here.

- At the minimal-|B| feasible point, the three vacuum entropies are confined to a mid-band (≈ 0.47–0.87) at all scales, with small slopes |dS_i/d log μ| ≈ 0.004–0.009 per e-fold.

- Structural feature (a restatement, not a prediction): the entropy ordering inverts in the UV. At M_Z, S₁ > S₂ > S₃ (SU(3) most entangled); above the pairwise coupling crossings — at 9.7 × 10¹² GeV (α₂–α₁), 2.4 × 10¹⁴ GeV (α₃–α₁), and 1.05 × 10¹⁷ GeV (α₃–α₂) — the ordering reverses and U(1) becomes the most entangled factor. This is the known one-loop crossing pattern re-expressed in entropy variables.

These results are summarized in Figure 2 (`experiments/results/fig2_entropy_flow.pdf`).

### 7.3. The Unification Corollary

Under the entropy-flow map, exact entanglement symmetry S₁ = S₂ = S₃ at some scale is *equivalent* to exact coupling unification at that scale — immediately, from Eq. (5) with B ≠ 0. This equivalence is definitional, not derived; what the map adds is only a translation of the unification question into entanglement language. Define the entanglement asymmetry ΔS(μ) as the spread of the inverse couplings divided by |B|. Computed at one loop:

- **Standard Model:** ΔS(μ) is minimized at μ* = 2.4 × 10¹⁴ GeV with ΔS ≈ 0.029 (at the minimal feasible |B|) — and it *never reaches zero*: the asymmetry bottoms out and rises again (Figure 2c). The SM vacuum, in this framework, is never symmetric at any scale. Note also that μ* is an *interior* scale: above it the couplings re-split, so a symmetric boundary condition would sit in the middle of the flow, not at its UV end — an awkwardness any symmetric-boundary reading must confront.

- **MSSM (1 TeV threshold):** ΔS cusps to ≈ 0.003 at 1.4 × 10¹⁶ GeV — an order of magnitude closer to symmetric, reflecting the well-known approximate unification of MSSM couplings [41].

The corollary, stated conditionally: **if** one demands an exactly symmetric boundary state — one natural reading of "couplings emerge from a symmetric entangled vacuum" — **then** the map requires exact coupling unification, which the Standard Model alone does not provide. This is the map's single falsifiable consequence, and it is inherited rather than novel: it restates the unification question, it does not add to it.

**Normalization caveat.** The abelian coupling enters all of these numbers in the GUT normalization α₁ = (5/3)α_Y. That factor is a convention inherited from embedding hypercharge in SU(5)-type groups; nothing in the three-qubit framework fixes it. Under a different admissible normalization, r_SM, the crossing scales, and ΔS_min all change. This interacts with Section 10.3, which entertains *avoiding* GUT embedding: without an embedding, the normalization is unfixed and three trajectories meeting at a point would be an unexplained codimension-one coincidence. The unification corollary is therefore doubly conditional — on the symmetric-boundary reading and on a normalization that only a GUT-type embedding currently motivates.

**A point of contact with Section 8.** If the symmetric boundary state is taken to be the rotor vacuum of Section 8 (entropies h₂(1/7) ≈ 0.5917), Eq. (5) at the symmetric scale fixes one linear relation between the map parameters: A + 0.5917·B = α*⁻¹. We verified that feasible (A, B) satisfying this relation exist for every unification coupling α*⁻¹ in the physically plausible range [20, 50]. The rotor boundary state is therefore *compatible* with the entropy-flow map but does not constrain it — consistent with the pattern, recurring throughout this paper, that internal consistency is cheap and constraint is what must be earned.

---

## 8. Vacuum Selection from Algebraic Dynamics

Section 4.2 identified the absence of dynamics — no principle selects the vacuum's entanglement — as the framework's most significant gap. We now report a concrete candidate, organized in three levels of ambition, together with computed results at the second level.

### 8.1. Three Levels

**Level 1 (kinematic).** The entropy-flow equation of Section 7 (Eq. 6). This is RG-consistent but not explanatory: it constrains how the vacuum's entanglement runs, not which vacuum is selected.

**Level 2 (variational/algebraic).** The vacuum is the ground state of a Hamiltonian canonically constructed from the octonion algebra itself, with no tuned parameters. This is the level at which we have computed results (Section 8.2).

**Level 3 (aspirational).** Identify the flow parameter of Level 1 with a coarse-graining (MERA-like [42]) flow whose fixed-point Hamiltonian is the Level-2 object. This would unite the kinematic and variational levels. It is entirely open.

### 8.2. Computed Results: the Octonion-Structured Rotor Hamiltonian

**Status: Computed (Experiments 4 and 6; results in `experiments/results/exp4_results.json` and `exp6_results.json`). Convention robustness verified in Section 8.3.**

The left-multiplication operators L_i = L_{e_i} of the imaginary octonion units on 𝕆 ≅ ℝ⁸ satisfy the Clifford relation L_iL_j + L_jL_i = −2δ_ij (machine-verified in our run), so the operators iL_i are Hermitian on ℂ⁸ — which is exactly the three-qubit Hilbert space. This permits Hamiltonians built canonically from the algebra. Findings:

- **Linear no-go.** Every linear Hamiltonian H = Σ c_i (iL_i) satisfies H² = |c|²·𝟙, so its spectrum is ±|c| with each level 4-fold degenerate, for *every* coupling vector c. The Clifford structure forbids linear algebra-canonical dynamics from selecting a unique vacuum; within the 4-dimensional ground manifold, entropy triples are unconstrained by the dynamics.

- **Commuting quadratic pairings.** The 105 ways of partitioning six of the seven generators into three commuting quadratic pairs give discrete vacua whose sorted entropy triples take only four values — (0, 0, 0), (0, 1, 1), (0.811, 0.811, 0.811), and (1, 1, 1) — all separable, degenerate, or permutation-symmetric. No hierarchy.

- **The rotor Hamiltonian and its closed form.** Take H = Σ_{a<b} σ(a,b) · iL_aL_b, where the couplings σ(a,b) are the octonion multiplication-table signs. Adversarial review of this work identified, and we verified to machine precision, the closed form

      H = i(L_u + 2R_u),     u = Σ_{a=1}^{7} e_a,

  where L_u and R_u are left and right multiplication by the sum of the imaginary units. Everything that follows is then provable in a few lines (and was confirmed numerically): on span{e₀, u}, since u² = −7, the operator L_u + 2R_u acts as 3M with M² = −7·𝟙 (a scaled complex structure), giving eigenvalues ±3√7; on the six-dimensional complement, R_u = −L_u and L_u² = −7·𝟙 by alternativity, giving ±√7, each threefold. The unique ground state is (√7 e₀ − iu)/√14 — half identity, half spread uniformly over the seven imaginary units — with exact invariants: each single-qubit reduced density matrix has spectrum (1/7, 6/7), so S₁ = S₂ = S₃ = h₂(1/7) ≈ 0.5917; the 3-tangle is τ₃ = 8/49; and all three pairwise concurrences equal 2√2/7. (The Coffman-Kundu-Wootters identity [33] C²₁₂ + C²₁₃ + τ₃ = 4λ₁(1−λ₁) holds for *every* pure three-qubit state; what is special here is only the equal three-way split, C²₁₂ = C²₁₃ = C²₂₃ = τ₃ = 8/49, which follows from permutation symmetry plus the marginal spectrum.)

- **What this does and does not show.** Because H = i(L_u + 2R_u), the construction is equivalent to distinguishing the unit direction û = u/√7 in the imaginary octonions, relative to the basis frame that also defines the qubit factorization. The convention-invariance of the vacuum (Section 8.3) is a provable consequence — the "sum of basis units" direction is permutation- and sign-gauge-covariant by construction — rather than an empirical discovery. And the choice of û matters: other distinguished directions give isospectral Hamiltonians i(L_û + 2R_û) whose vacua (e₀ − iû)/√2 can be *separable* — for û = e₁ this is exactly the preferred-complex-direction state found entropy-degenerate in Section 6.2. So the algebra alone does not select a vacuum; the algebra *plus the frame defining the qubit factorization* selects one. The result is best read as a clean, exactly solvable instance of the same permutation rigidity found kinematically in Section 6.2, now at the dynamical level: even the canonical dynamical construction yields a symmetric vacuum, not a hierarchy.

- **Unsigned control.** Replacing the couplings σ(a,b) by +1 while keeping the true multiplication operators yields a different Hermitian Hamiltonian whose unique ground state is entangled but *hierarchical* and convention-*dependent* (in the Cayley–Dickson convention used here: sorted entropies (0.577, 0.472, 0.327), τ₃ = 4/49 exactly; across the 128 sign gauges the sorted triple takes nine distinct values, unlike the σ-structured vacuum's single one — "unsigned" is not a basis-independent notion). The table signs are therefore necessary for the symmetric, convention-invariant vacuum — not for entanglement as such. (An earlier version of this control, like an earlier version of the main computation, suffered from passing a non-Hermitian matrix to a Hermitian eigensolver; both are corrected here, and we flag the failure mode for others automating such computations.)

- **Genericity control.** Random so(7) rotor Hamiltonians (generic antisymmetric couplings in place of σ) also have unique vacua; 16.4% produce ordered entropies S₁ > S₂ > S₃ — consistent with the 1/6 exchange-symmetry chance rate — and 0.9% land in a widened coupling-matching window (|r_S − 1.8174| < 0.05; Section 6.1 uses 0.01), consistent with the Haar-generic rate at that tolerance. Generic quadratic dynamics is generic; the σ-structured choice is distinguished only by its symmetry.

The rotor vacuum is permutation-symmetric, not hierarchical — extending the permutation rigidity of every canonical kinematic construction (Section 6.2) to the dynamical level. Within the entropy-flow picture of Section 7 a symmetric algebra-derived state is the natural candidate boundary state at a unification scale, and its entropy 0.5917 lies inside the feasible mid-band of Section 7.2 — but as Section 7.3 records, this compatibility does not constrain the map.

**Relation to prior work.** Multiplication operators on the octonions and the decomposition of so(8) into left- and right-multiplication parts are classical material [48], and the ±√7-type spectra of such operators are standard; the three-qubit/octonion/hyperdeterminant nexus is extensively developed in the black-hole/qubit correspondence [44]. We have not found this specific Hamiltonian proposed as a three-qubit vacuum selector, or this state's entanglement invariants recorded, but the ingredients are elementary and the result should be regarded as an observation assembled from standard parts, not as new mathematics.

### 8.3. Convention Robustness

**Status: Provable from the closed form; confirmed computationally (Experiment 6; `experiments/results/exp6_results.json`).**

Because H = i(L_u + 2R_u) with u the sum of the imaginary basis units, the vacuum has the same coordinate vector (√7, −i, −i, −i, −i, −i, −i, −i)/√14 in every basis convention: sign gauges e_a → s_a e_a and relabelings e_a → e_{π(a)} permute and re-sign the summands of u coherently with the basis itself. We nonetheless ran the full battery as a check on the code and the claim: all 2⁷ = 128 sign gauges; all 7! = 5040 index relabelings (the 168-element XOR-linear GL(3,2) subgroup tracked separately); 2000 random combined transformations; the opposite algebra; right-multiplication operators in place of left; and H → −H. In every case the ground state is unique with sorted entropy triple (0.5917, 0.5917, 0.5917) and τ₃ = 8/49. The invariance is exact, as the closed form requires.

---

## 9. The Jordan–Wigner Bridge Between the Furey and Szangolies Constructions

### 9.1. The Embedding Is Standard Mathematics Made Explicit

The design phase of the computational program (Section 6.2) treated the embedding of Furey's Cl(6) structures [5, 6] into ℂ² ⊗ ℂ² ⊗ ℂ² as an open problem. It is not — and we should be precise about how much of this was already in the literature. Furey's construction is explicitly built from three fermionic ladder operators [5, 6], and the minimal-left-ideal structure of Cl(6) with electric charge as one-third the number operator is developed in detail by Stoica [45]. The complex Clifford algebra Cl(6) is isomorphic to M₈(ℂ), which is exactly the full operator algebra of three qubits, and the Jordan–Wigner transformation [38] between three fermionic modes and three qubits is textbook. We machine-verified that the Jordan–Wigner images of the three ladder operators satisfy the canonical anticommutation relations exactly (Experiment 5; `experiments/results/exp5_results.json`).

The bridge between the Furey and Szangolies constructions is therefore a standard transformation, dating to 1928, that had not been put to work in this specific context. What this paper contributes is the reading of its consequences — and, principally, the obstruction it exposes (Section 9.3).

### 9.2. Computed Consequences

**Status: Computed (Experiment 5).**

- **Charge is Hamming weight.** Furey's minimal-left-ideal basis for one generation — ν, three d̄ colors, three u colors, e⁺ — maps under Jordan–Wigner to the three-qubit computational basis, graded by Hamming weight: ν at weight 0, the d̄ triplet at weight 1, the u triplet at weight 2, e⁺ at weight 3, with electric charge Q = (weight)/3. Furey's observation that charge quantization follows from the integer spectrum of a number operator [6] becomes, in qubit language, the statement that charge quantization is the integer grading of the computational basis.

- **SLOCC classes acquire particle-physics meaning.** The color-symmetric quark combination (uniform superposition over the weight-1 triplet) is precisely the **W state**, with S = (0.918, 0.918, 0.918) and τ₃ = 0. The ν + e⁺ superposition is precisely the **GHZ state** — the maximal violation of charge superselection (ΔQ = 1) maps to maximal genuine tripartite entanglement.

- Fock (particle) basis states are computational basis states: single particles carry no entanglement in this frame.

### 9.3. Critical Caveat: Entanglement Is Gauge-Frame Dependent

The same computation exposes a structural obstruction. Color rotations act on the fermionic *modes*, not on the qubit tensor factors. A discrete Fourier transform in color space — an SU(3) gauge transformation — maps a separable single-quark state, S = (0, 0, 0), to a state with S = (0.918, 0.918, 0.918). Machine check: this transformation is not a local unitary of the qubit factorization.

That entanglement is relative to a choice of tensor-product structure, and that mode rotations change it, is well documented in the quantum-information literature [46, 47]; we are not claiming the phenomenon as new. The contribution here is its specific consequence for this program:

**Gauge transformations are not local unitaries of the qubit factorization, and therefore single-qubit entanglement entropies in this frame are gauge-frame dependent.** Any physical coupling-entropy correspondence must consequently be built from gauge-invariant entanglement functionals, or must include an algebraic gauge-fixing of the tensor factorization as part of its definition. Neither has yet been constructed. Until one is, the title question of this paper is ill-posed — which is itself the sharpest result the executed program produced.

This caveat sharpens, and partially explains, two earlier findings: the index ambiguity of Section 2.3 (the tensor-factor labels were never gauge-covariantly defined) and the Control D null of Section 6.4 (no unconstrained entanglement statistic could have privileged one qubit-gauge labeling, because the labeling is not gauge-invariant in the first place). We regard identifying the right gauge-invariant entanglement functional as the central open problem this paper leaves for the coupling-entropy program.

---

## 10. Connections to Open Problems

The QIO suggests reframings — potentially productive changes of viewpoint — for several open problems. These are research directions, not resolutions.

### 10.1. De Sitter Holography

If spacetime universally emerges from entanglement, holography should extend beyond AdS. Recent work on static patch holography [34] and composite deformation flows [35] shows progress. De Sitter holography does not yet approach AdS/CFT-level rigor.

### 10.2. The Cosmological Constant

If the holographic principle constrains degrees of freedom to scale with area rather than volume, the QFT vacuum energy calculation overcounts. Freidel et al. (2023) [36] explored how holographic entropy bounds constrain vacuum energy, showing a technically natural result (Λ → 0 as IR scale increases). This is suggestive but does not derive the observed Λ, address radiative stability, or produce numerical predictions.

### 10.3. Gauge Unification and the Monopole Problem

Standard GUTs (SU(5), SO(10)) unify the three Standard Model gauge interactions; gravity is usually not part of these models. If the QIO/division-algebraic framework ultimately favors a direct origin of SU(3) × SU(2) × U(1) from octonionic entanglement structure — without embedding the Standard Model gauge group into a larger simply connected GUT group — then the usual monopole-producing symmetry-breaking patterns of conventional GUTs may not arise. This would reframe the monopole problem, but only if the QIO/division-algebraic framework replaces rather than supplements conventional GUT symmetry breaking. This possibility is conditional on the QIO's core posits and has not been demonstrated. We note the tension with Section 7.3, now sharpened by the normalization caveat recorded there: the unification corollary requires the coupling *values* to converge, and the very normalization in which they converge (α₁ = (5/3)α_Y) is motivated by GUT embedding. Without an embedding, the normalization is unfixed and three trajectories meeting at a point would be an unexplained codimension-one coincidence. A framework that wants both the unification boundary condition and no GUT group owes an independent derivation of the abelian normalization; none currently exists.

---

## 11. Discussion

### 11.1. What Distinguishes the QIO

The "It from Qubit" program [37] pursues emergent spacetime from entanglement. The division-algebraic program pursues Standard Model structure from octonions. The QIO — read as an information-first organizing heuristic (Section 4.1) — treats these as descriptions of the same structure. Whether the Szangolies bridge between them is deep or superficial is an empirical question. The computational program of Section 6, now executed, addresses one facet of this question, and the Jordan–Wigner dictionary of Section 9 makes explicit that one such link (Furey ↔ three qubits) is a standard isomorphism — though one whose entanglement consequences are gauge-frame dependent, which is the deeper finding.

### 11.2. The Central Results

The most important technical contributions of this paper remain negative, and the executed program strengthened them. First, we prove that the naive coupling-entropy conjecture is underconstrained (Section 5.3), and the executed Experiment 1 converts this from argument to measurement: across 10⁷ Haar states, the matching manifold is statistically generic in the 3-tangle and intersects the W-class, and the null controls show that parameter freedom, not algebraic structure, drives matching. Second, we prove that the two-qubit version of the map is impossible (Section 5.6), so three qubits is the minimal case with content. Third, we compute that r_SM(μ) varies substantially across scales (Section 6.3), ruling out a scale-independent entropy triple under the logarithmic map. Fourth, every canonical octonionic state construction tested is permutation-degenerate (Section 6.2): the algebra's own symmetry forbids the obvious kinematic routes to a hierarchy.

These negative results delineate precisely what additional structure is needed. The second half of the paper maps the surviving hypothesis space with three objects — each checkable, none requiring belief in the ontology, and each presented with its deflations on the surface:

1. **The entropy-flow map** (Section 7): an RG-consistent affine form of the conjecture. Its quantum-marginal feasibility requires |B| ≳ 126.5 (a robust bound, binding at M_Z alone), it constrains no observable, and its single falsifiable consequence — an entanglement-symmetric boundary state is equivalent to exact coupling unification — restates the unification question rather than adding to it, and depends on the GUT normalization of the abelian coupling.

2. **The rotor Hamiltonian** H = i(L_u + 2R_u) (Section 8): an exactly solvable vacuum-selection toy whose unique ground state is provably convention-invariant and permutation-symmetric, with exact invariants (marginal spectra (1/7, 6/7); 3-tangle equal to each squared concurrence, 8/49). It extends the permutation rigidity of the kinematic constructions to the dynamical level; the selection is by the algebra *together with* the frame defining the qubit factorization, not by the algebra alone.

3. **The Jordan–Wigner dictionary** (Section 9), which makes the Furey construction's three-qubit content explicit — charge quantization as Hamming-weight grading, the W and GHZ states acquiring particle-physics meaning — and whose principal yield is the gauge-covariance obstruction: entanglement of the qubit factorization is not gauge-invariant, so the program's central quantity is ill-posed as currently defined.

The forward direction is therefore not "develop the framework" but "solve the well-posedness problem": construct a gauge-invariant entanglement functional, or accept that the title question has no physical content.

### 11.3. Risks and Failure Modes

The executed program realized one of the previously listed failure modes: no canonical algebraically motivated state intersects the matching manifold (Section 6.2), and unconstrained matching is confirmed non-evidential. The program absorbed this outcome as designed. The convention-robustness check (Section 8.3) was passed exactly, though it revealed that the rotor vacuum is symmetric rather than hierarchical, relocating the burden of hierarchy generation entirely to the flow. Remaining risks: the gauge-frame dependence of entanglement (Section 9.3) may admit no satisfactory gauge-invariant reformulation, which would undercut the coupling-entropy program at its root; the entropy-flow map's counting interpretation may never acquire independent content, leaving it a reparametrization; no mechanism is known that produces the required entropy slopes from the rotor boundary state; and the index ambiguity (Section 2.3) may prove fatal. These are acceptable outcomes — the purpose of precise conjecture is to enable definitive testing, including failure.

---

## 12. Conclusion

We asked whether the Standard Model coupling hierarchy is encoded in three-qubit vacuum entanglement, motivated by two convergent research programs and the Szangolies bridge between them, organized under the Quantum Information Ontology read strictly as a heuristic. We formulated the conjecture precisely, executed the computational program designed to test it, and subjected every positive-seeming result to adversarial review (which found, and we corrected, two computational errors and three overclaims — all documented in the repository).

Our negative results stand and are strengthened by execution. Analytically: unconstrained three-qubit states can reproduce the observed coupling hierarchy at M_Z (underconstraint, Section 5.3); two-qubit states cannot encode unequal couplings at all (minimality, Section 5.6); and a scale-independent entropy triple cannot match couplings at all energies (Section 6.3). Empirically, across 10⁷ Haar-random states: the matching manifold is statistically generic in its entanglement invariants and intersects the W-class; every canonical octonionic state construction is permutation-degenerate and cannot produce a hierarchy; and four null controls confirm that parameter freedom, not division-algebra structure, drives matching. Coupling matching alone is not evidence — now as a measurement, not only a theorem.

The surviving hypothesis space is small and sharply bounded. A coupling-entropy correspondence, if one exists, must: (i) be built from gauge-invariant entanglement functionals, because single-qubit entropies of the Jordan–Wigner factorization are gauge-frame dependent (Section 9.3) and the abelian normalization is itself a convention (Section 7.3); (ii) generate the hierarchy by flow rather than statics, in the RG-consistent affine form of Section 7, whose only falsifiable consequence is the unification boundary condition — the Standard Model's entanglement asymmetry never reaches zero, bottoming at ≈ 0.029 near 2.4 × 10¹⁴ GeV, while the MSSM reaches ≈ 0.003 near 1.4 × 10¹⁶ GeV; and (iii) explain why the algebra's own canonical vacuum, the exactly solvable rotor ground state (√7 e₀ − iu)/√14 with marginal spectra (1/7, 6/7) and 3-tangle 8/49, is permutation-symmetric — hierarchy is nowhere to be found in the octonions' canonical structures, kinematic or dynamical.

None of these results requires believing the ontology; each is a checkable statement about three-qubit states, Clifford algebras, or renormalization-group trajectories, with code and raw outputs published. The well-defined problems this paper leaves open are the construction of a gauge-invariant entanglement functional (the well-posedness problem, which we regard as the central one), the counting interpretation of the entropy-flow slopes, and the mechanism question of whether any flow connects a symmetric boundary state to the low-energy hierarchy. A map of where the answers cannot lie is what this paper contributes; we offer it to whoever next enters this territory.

---

## References

[1] A. Hurwitz, "Über die Composition der quadratischen Formen," Nachr. Ges. Wiss. Göttingen, 309 (1898).

[2] M. Günaydin and F. Gürsey, "Quark structure and the octonions," J. Math. Phys. 14, 1651 (1973).

[3] G.M. Dixon, *Division Algebras: Octonions, Quaternions, Complex Numbers and the Algebraic Design of Physics*, Springer (1994).

[4] G.M. Dixon, "Division algebras: Family replication," J. Math. Phys. 45, 3878 (2004).

[5] C. Furey, "Generations: three prints, in colour," JHEP 2014, 046 (2014).

[6] C. Furey, "SU(3)_C × SU(2)_L × U(1)_Y (× U(1)_X) as a symmetry of division algebraic ladder operators," Eur. Phys. J. C 78, 375 (2018).

[7] I. Todorov and M. Dubois-Violette, "Deducing the symmetry of the standard model from the automorphism and structure groups of the exceptional Jordan algebra," Int. J. Mod. Phys. A 33, 1850118 (2018).

[8] I. Todorov, "Octonion internal space algebra for the Standard Model," arXiv:2206.06912 (2022).

[9] J. Szangolies, "The Standard Model Symmetry and Qubit Entanglement," Entropy 27(6), 569 (2025); arXiv:2512.17328.

[10] R. Mosseri and R. Dandoloff, "Geometry of entangled states, Bloch spheres and Hopf fibrations," J. Phys. A 34, 10243 (2001).

[11] B.A. Bernevig and H.-D. Chen, "Geometry of the three-qubit state, entanglement and division algebras," J. Phys. A 36, 8325 (2003).

[12] J.D. Bekenstein, "Black holes and entropy," Phys. Rev. D 7, 2333 (1973).

[13] S.W. Hawking, "Particle creation by black holes," Commun. Math. Phys. 43, 199 (1975).

[14] G. 't Hooft, "Dimensional reduction in quantum gravity," arXiv:gr-qc/9310026 (1993).

[15] L. Susskind, "The world as a hologram," J. Math. Phys. 36, 6377 (1995).

[16] J. Maldacena, "The large-N limit of superconformal field theories and supergravity," Adv. Theor. Math. Phys. 2, 231 (1998).

[17] S. Ryu and T. Takayanagi, "Holographic derivation of entanglement entropy from AdS/CFT," Phys. Rev. Lett. 96, 181602 (2006).

[18] T. Jacobson, "Thermodynamics of spacetime: The Einstein equation of state," Phys. Rev. Lett. 75, 1260 (1995).

[19] J.F. Donoghue, "The effective field theory treatment of quantum gravity," AIP Conf. Proc. 1483, 73 (2012).

[20] J. Maldacena and L. Susskind, "Cool horizons for entangled black holes," Fortschr. Phys. 61, 781 (2013).

[21] B. Swingle, "Entanglement renormalization and holography," Phys. Rev. D 86, 065007 (2012).

[22] A. Almheiri, X. Dong, and D. Harlow, "Bulk locality and quantum error correction in AdS/CFT," JHEP 2015, 163 (2015).

[23] D. Harlow, "The Ryu-Takayanagi formula from quantum error correction," Commun. Math. Phys. 354, 865 (2017).

[24] D. Harlow and H. Ooguri, "Constraints on symmetries from holography," Phys. Rev. Lett. 122, 191601 (2019).

[25] E. Verlinde, "On the origin of gravity and the laws of Newton," JHEP 2011, 29 (2011).

[26] M. Visser, "Conservative entropic forces," JHEP 2011, 140 (2011).

[27] D.N. Page and W.K. Wootters, "Evolution without evolution," Phys. Rev. D 27, 2885 (1983).

[28] E. Moreva et al., "Time from quantum entanglement: An experimental illustration," Phys. Rev. A 89, 052122 (2014).

[29] T. Favalli, *On the Emergence of Time and Space in Closed Quantum Systems*, Springer Theses, Springer (2024).

[30] Particle Data Group, "Review of Particle Physics," Prog. Theor. Exp. Phys. (updated regularly; coupling values used here from the 2022 edition, R.L. Workman et al., 2022, 083C01).

[31] A. Higuchi, A. Sudbery, and J. Szulc, "One-qubit reduced states of a pure many-qubit state: polygon inequalities," Phys. Rev. Lett. 90, 107902 (2003).

[32] M.A. Nielsen and I.L. Chuang, *Quantum Computation and Quantum Information*, Cambridge University Press (2000).

[33] V. Coffman, J. Kundu, and W.K. Wootters, "Distributed entanglement," Phys. Rev. A 61, 052306 (2000).

[34] L. Susskind, "De Sitter holography," arXiv:2106.03964 (2021).

[35] J.-C. Chang et al., "Toward a unified de Sitter holography," Sci. China Phys. Mech. Astron. (2026); arXiv:2511.16098.

[36] L. Freidel, J. Kowalski-Glikman, R.G. Leigh, and D. Minic, "Vacuum energy density and gravitational entropy," Phys. Rev. D 107, 126016 (2023).

[37] T. Takayanagi, "Emergent Holographic Spacetime from Quantum Information," Phys. Rev. Lett. 134, 240001 (2025); arXiv:2506.06595. See also the Simons Foundation "It from Qubit" collaboration.

[38] P. Jordan and E. Wigner, "Über das Paulische Äquivalenzverbot," Z. Phys. 47, 631 (1928).

[39] A.B. Zamolodchikov, "Irreversibility of the flux of the renormalization group in a 2D field theory," JETP Lett. 43, 730 (1986).

[40] H. Casini and M. Huerta, "A c-theorem for the entanglement entropy," J. Phys. A 40, 7031 (2007).

[41] U. Amaldi, W. de Boer, and H. Fürstenau, "Comparison of grand unified theories with electroweak and strong coupling constants measured at LEP," Phys. Lett. B 260, 447 (1991).

[42] G. Vidal, "Entanglement renormalization," Phys. Rev. Lett. 99, 220405 (2007).

[43] A. Sawicki, M. Walter, and M. Kuś, "When is a pure state of three qubits determined by its single-particle reduced density matrices?," J. Phys. A: Math. Theor. 46, 055304 (2013).

[44] L. Borsten, D. Dahanayake, M.J. Duff, H. Ebrahim, and W. Rubens, "Black holes, qubits and octonions," Phys. Rep. 471, 113 (2009).

[45] O.C. Stoica, "Leptons, quarks, and gauge from the complex Clifford algebra Cl(6)," Adv. Appl. Clifford Algebras 28, 52 (2018); arXiv:1702.04336.

[46] P. Zanardi, "Virtual quantum subsystems," Phys. Rev. Lett. 87, 077901 (2001).

[47] H. Barnum, E. Knill, G. Ortiz, and L. Viola, "A subsystem-independent generalization of entanglement," Phys. Rev. Lett. 92, 107902 (2004).

[48] F.R. Harvey, *Spinors and Calibrations*, Academic Press (1990).