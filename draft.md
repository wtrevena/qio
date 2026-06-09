# Quantum Information Ontology: A Framework for Emergent Spacetime and Gauge Structure with an Analysis of Coupling-Entanglement Correspondence

**W. [Author]**

*University of Florida (PhD, Industrial and Systems Engineering)*

April 2026

*Acknowledgment: Portions of this manuscript were developed with the assistance of Claude (Anthropic), an AI language model, which contributed to literature synthesis, mathematical exposition, and drafting. Consistent with COPE authorship guidelines, the AI system is acknowledged as a tool rather than listed as a coauthor.*

---

## Abstract

Two largely independent research programs suggest that quantum information plays a foundational role in physics. The emergent-spacetime program (Jacobson, AdS/CFT, Ryu-Takayanagi, holographic quantum error correction) connects entanglement to spacetime geometry. The division-algebraic program (Günaydin-Gürsey, Dixon, Furey, Todorov, Szangolies) connects the normed division algebras — and specifically the octonions — to the gauge group and matter content of the Standard Model. We propose a speculative framework, the Quantum Information Ontology (QIO), that treats these as aspects of a single underlying structure, with the Szangolies construction (connecting three-qubit entanglement to SU(3) × SU(2) × U(1)/Z₆ via octonionic Hopf fibrations) as a bridge between them. We review both programs with explicit epistemic labeling. We formulate a pre-specified conjecture mapping gauge coupling hierarchies to vacuum entanglement entropy under a logarithmic map, and we prove analytically that this conjecture is underconstrained: the observed Standard Model coupling hierarchy at M_Z lies inside the image of the one-qubit marginal polytope under the binary entropy map, so unconstrained three-qubit states contain continuous families of entropy triples reproducing the hierarchy. We further compute that the log-inverse-coupling gap ratio r_SM(μ) varies by approximately 24% between M_Z and 10⁶ GeV under one-loop Standard Model running, and becomes singular near the α₁-α₂ crossing, establishing that a scale-independent entropy triple cannot simultaneously match couplings at all scales under the logarithmic map. These results establish that coupling-entropy matching alone cannot constitute evidence for the QIO; additional algebraic constraints selecting the vacuum state are necessary, and the coupling-entropy relationship must either hold at a privileged UV scale or involve scale-dependent entanglement flow. We characterize what such constraints would need to provide, specify a computational program to test whether algebraically motivated states intersect the coupling-matching manifold, and identify holdout observables that could elevate the test from a baseline consistency check to genuine evidence. The QIO is presented as a research program, not a completed theory. We do not claim to derive the Standard Model, resolve quantum gravity, or solve the cosmological constant problem.

---

## 1. Introduction

Two largely independent research programs have converged on the idea that quantum information plays a foundational role in physics.

The first, rooted in quantum gravity, begins with Bekenstein's discovery (1973) that black hole entropy scales with horizon area and proceeds through the holographic principle, AdS/CFT, the Ryu-Takayanagi formula, holographic quantum error correction, and Jacobson's thermodynamic derivation of Einstein's equations. These results suggest that spacetime geometry may be emergent from quantum entanglement.

The second, rooted in algebraic particle physics, begins with Günaydin and Gürsey's identification (1973) of SU(3) color within the octonions and proceeds through Dixon's division-algebraic model, Furey's division-algebraic construction of gauge symmetries with correct fermion representations, Todorov's octonionic Clifford algebra approach, and Szangolies's recent connection of this program to qubit entanglement via Hopf fibrations. These results suggest that the internal symmetries of the Standard Model arise naturally from the octonions.

These programs have developed largely in isolation, though some researchers work across quantum information, holography, and algebraic particle physics. The Szangolies construction (2025) provides a concrete bridge: it shows that the Standard Model gauge group appears as a residual symmetry of a three-qubit octonionic Hopf fibration upon dimensional reduction, explicitly connecting gauge structure to quantum entanglement.

We propose a speculative framework — the Quantum Information Ontology (QIO) — treating these programs as aspects of a unified picture. We then investigate a specific quantitative question: whether the gauge coupling hierarchy is encoded in the entanglement entropy of the vacuum state. We prove analytically that the naive version of this conjecture is underconstrained, and we characterize what additional structure is needed for it to become evidential.

### 1.1. Contributions

1. **Synthesis.** We connect the emergent-spacetime and division-algebraic programs under a common framework, identifying the Szangolies construction as a bridge.

2. **Observation on spacetime emergence.** We note that Ryu-Takayanagi (spatial emergence) and Page-Wootters (temporal emergence) may describe two aspects of a single informational mechanism. This is suggestive, not a formal result.

3. **Division-algebra uniqueness.** The three-qubit octonionic case is the unique normed-division-algebra Hopf fibration producing the Standard Model gauge group.

4. **Analytic underconstraint result.** We prove that unconstrained three-qubit states can reproduce the observed Standard Model coupling hierarchy at M_Z under a two-parameter logarithmic map, establishing that coupling matching alone is not evidential (Section 5.3).

5. **Scale-dependence computation.** We compute that the log-inverse-coupling gap ratio r_SM(μ) varies significantly under one-loop SM running (~24% between M_Z and 10⁶ GeV) and becomes singular near the α₁-α₂ crossing (~10¹³ GeV). We note that hypothetical exact UV coupling unification would correspond to symmetric entanglement S₁ = S₂ = S₃, though one-loop SM running does not produce exact three-coupling unification (Section 5.4).

6. **Characterization of evidential requirements.** We specify what additional constraints would elevate coupling-entropy correspondence from a baseline check to genuine evidence (Section 5.5).

7. **Computational program.** We design experiments testing whether algebraically motivated states from the Szangolies construction intersect the coupling-matching manifold.

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

### 2.2. The Three-Generation Observation

Three appearances of "three" in this program deserve attention: Furey's Cl(6) mirrors three generations [5]; Dixon's T accommodates three families [4]; Szangolies requires three qubits [9]. Whether these reflect a single mechanism remains open. Szangolies produces the gauge group but does not derive matter representations or demonstrate that qubit tensor factors map to generations. Furey produces representations mirroring three generations but within a different algebraic framework. The mathematical relationship between these constructions is an important open problem.

We note this coincidence as motivation without claiming it constitutes an explanation.

### 2.3. The Index Ambiguity

In the Szangolies construction, the three tensor factors of ℂ² ⊗ ℂ² ⊗ ℂ² are associated with gauge group structure (the octonionic decomposition produces SU(3) × SU(2) × U(1)/Z₆). If one additionally associates these factors with fermion generations, a framework is needed in which the same structure simultaneously encodes both gauge and flavor information. Such a framework does not currently exist in complete form. This ambiguity affects the coupling-entanglement conjecture in Section 5, where we treat the three qubit factors as corresponding to gauge sectors, consistent with the Szangolies construction.

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

Page and Wootters (1983) [27] showed time can emerge from entanglement in a globally static quantum state (H|Ψ⟩ = 0). Moreva et al. (2013) [28] experimentally illustrated this in an entangled photon system. Favalli et al. (2024) [29] extended to 3+1 dimensions, recovering Schwarzschild time dilation.

---

## 4. The QIO Framework

### 4.1. Organizing Conjecture

**Quantum Information Ontology (QIO):** Quantum information is the fundamental ontological substrate of physical reality. Spacetime geometry, gravitational dynamics, and gauge symmetries are emergent phenomena arising from the entanglement structure of an underlying quantum system.

This is an organizing conjecture — a framework for connecting results and generating hypotheses — not a derived conclusion.

### 4.2. Definitions and Open Specifications

Any complete realization of the QIO would require specifying the following objects. We state them here to make explicit what the framework currently leaves undefined:

- **Fundamental Hilbert space H.** The quantum system from which spacetime, gravity, and gauge structure emerge. Its dimension, factorization structure, and relationship to the Szangolies three-qubit space are unspecified. In the coupling-entropy conjecture (Section 5), we work within H = ℂ² ⊗ ℂ² ⊗ ℂ² as a minimal model, without claiming this is the full fundamental space.
- **Vacuum state |Ω⟩.** The specific state in H whose entanglement structure determines physical observables. Identifying |Ω⟩ from first principles requires a selection rule or dynamical principle that the current framework does not provide.
- **Physical observables.** The operators on H whose expectation values correspond to measurable quantities (coupling constants, masses, mixing angles). The coupling-entropy conjecture (Section 5) proposes that von Neumann entropies of reduced density matrices map to coupling constants, but does not derive this from a Hamiltonian or Lagrangian.
- **Gauge map.** The map from the entanglement structure of |Ω⟩ to the gauge group SU(3) × SU(2) × U(1)/Z₆. The Szangolies construction [9] provides this via the octonionic Hopf fibration, but the full dictionary between entanglement properties and gauge dynamics is not yet established.
- **Spacetime reconstruction.** The map from entanglement entropy to spatial metric. Within AdS/CFT, this is given by the Ryu-Takayanagi formula [17]. Its extension to general spacetimes is conjectural.
- **Time reconstruction.** The mechanism by which temporal evolution emerges. The Page-Wootters mechanism [27] provides a candidate but requires specifying the clock subsystem.
- **Dynamics.** No Hamiltonian, Lagrangian, or equation of motion is provided by the current framework. This is the most significant gap.

These gaps are not hidden; they define the open problems of the QIO research program.

### 4.3. Claims with Confidence Levels

**High confidence:** Information content of gravitational systems is holographic. Einstein's equations are derivable from information-theoretic assumptions. Within AdS/CFT, spatial geometry is determined by entanglement entropy.

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

Moreover, even fixing the one-qubit reduced spectra does not generally determine the three-qubit state up to local unitaries. For generic interior points of the three-qubit marginal polytope, additional local-unitary-inequivalent states share the same one-qubit spectra [cf. Sawicki, Walter, and Kuś on the Kirwan polytope]. Thus, the entropy triple is a very coarse invariant, further reinforcing that coupling matching alone cannot identify a physical vacuum.

The unconstrained existence version of the conjecture is falsified only if the target entropy ratio lies outside the feasible region — which it does not. Therefore, the meaningful test must be strengthened: after imposing independently motivated algebraic constraints on |Ω⟩, the conjecture is falsified if no algebraically allowed state produces the observed coupling hierarchy within stated tolerance.

### 5.4. What Would Constitute Evidence

The underconstraint result (Section 5.3) establishes that coupling-entropy matching alone is not evidential. Evidence for a physical coupling-entanglement correspondence requires one or more of the following:

**Requirement A (Algebraic selection).** The vacuum state |Ω⟩ must not be arbitrary. It must be selected from the Szangolies construction, or from three-qubit representatives obtained via a yet-to-be-defined embedding of Furey's Clifford-algebraic structures, or from another independently motivated geometric or algebraic condition. If such a constrained state automatically produces the correct entropy gap ratio (Eq. 2), without fitting, that would be a non-trivial result.

**Requirement B (Holdout predictions).** If the state is selected by coupling matching, it must successfully predict independent observables not used in fitting:
- The Weinberg angle θ_W
- The GUT-scale coupling convergence energy
- Qualitative CKM or PMNS structure
- A specific entanglement class (GHZ-type vs. W-type)
- A simple or notable value of the 3-tangle τ₃
- Non-generic local unitary invariants

**Requirement C (Non-genericity).** The coupling-matching states must occupy a distinguished, measure-zero or algebraically special subset of the three-qubit state space. If the matching manifold intersects a known special locus (e.g., the GHZ orbit, the W orbit, a maximal entanglement surface), this would suggest the coupling hierarchy is connected to entanglement structure rather than being an artifact of parametric freedom.

### 5.5. Analytic Pre-Constraints

For completeness, we record the constraints on achievable entropy triples. Each S_i ∈ [0, 1]. The triangle inequality S_i ≤ S_j + S_k holds for all tripartite pure states [32]. For sharper feasibility constraints, the smaller eigenvalues λ_i of the single-qubit reduced density matrices (obtained by solving S_i = h₂(λ_i) with λ_i ∈ [0, 1/2]) must satisfy the polygon inequality λ_i ≤ Σ_{j≠i} λ_j, which Higuchi, Sudbery, and Szulc [31] show is necessary and sufficient for compatibility with a pure n-qubit state.

The required entropy ordering is S₁ > S₂ > S₃ (stronger coupling ↔ more entanglement), with B < 0.

---

## 6. Computational Program

The underconstraint result (Section 5.3) reshapes the computational program. The goal is not to find a matching state (which is guaranteed) but to characterize the matching manifold and test whether it intersects algebraically distinguished regions of the three-qubit state space.

### 6.1. Experiment 1: Characterize the Matching Manifold

**Objective.** Map the set of three-qubit pure states satisfying r_S = 1.817 ± 0.01 and determine its entanglement properties.

**Procedure.** Generate N = 10⁷ Haar-random three-qubit states. (This large sample is not needed to find a matching state — the Underconstraint Lemma guarantees many exist. The sample size is chosen to characterize the *distribution* of entanglement invariants across the matching manifold, which requires dense coverage.) For each, compute S₁, S₂, S₃ (with qubit labels preserved per Szangolies assignment). Retain states satisfying S₁ > S₂ > S₃ and |r_S - 1.817| < 0.01.

For all retained states, compute: 3-tangle τ₃ [33], pairwise concurrences C₁₂, C₁₃, C₂₃, Cayley hyperdeterminant, SLOCC class, and all local unitary invariants.

**Output.** Distribution of entanglement invariants on the matching manifold. Determine whether the matching states differ statistically from Haar-conditioned generic states in their entanglement invariants, especially 3-tangle, pairwise concurrences, local-unitary invariants, and distance to lower-dimensional special loci such as W, biseparable, or symmetric-state families.

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

Note: Furey's Clifford-algebraic construction [5, 6] does not directly produce three-qubit quantum states. Testing Furey-motivated states requires first defining an embedding map from Cl(6) structures to ℂ² ⊗ ℂ² ⊗ ℂ², which is itself an open mathematical problem.

### 6.3. Analytic Result: Scale Dependence of r_SM(μ)

We compute r_SM(μ) across energy scales. This is not a proposed experiment — it is a completed calculation.

The one-loop RG equations, with the convention dg_i/d(log μ) = b_i g_i³/(16π²), give:

    α_i⁻¹(μ) = α_i⁻¹(M_Z) - (b_i/2π) log(μ/M_Z)     ... (5)

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

### 6.4. Null Controls

Since the underconstraint result establishes that matching is easy, the null controls should test *non-genericity* — whether the Standard Model coupling hierarchy selects algebraically special states compared to generic targets.

**Control A (Non-genericity of SM target).** For 1000 randomly sampled coupling triples (log-uniform on [0.001, 0.5], ordered), compute the corresponding entropy-gap ratios and characterize the matching manifolds. Compare the entanglement-class distributions, 3-tangle distributions, and local unitary invariant distributions against the Standard Model target. The null question is not whether random targets can be matched (they can), but whether the SM target selects a more algebraically special matching manifold than generic targets.

**Control B (Two-qubit comparison).** Two-qubit states have two single-qubit entropies, not three, so the three-coupling logarithmic map is not directly comparable. This control tests whether a two-entropy map (fitting two couplings with one free parameter, no holdout) achieves comparable matching quality, which would indicate that the three-qubit structure adds no explanatory power beyond having a third entropy variable.

**Control C (Four-qubit comparison).** Four-qubit states (30 real parameters) do not correspond to a normed division algebra. This control tests whether the algebraic restriction to three qubits, rather than parameter count, selects anything special. If four-qubit matching manifolds have indistinguishable structure from three-qubit manifolds, the division-algebra motivation is weakened.

**Control D (Shuffled labels).** Test all six qubit-gauge permutations. If the Szangolies construction supplies a physically meaningful labeling of the three qubit factors, the corresponding assignment should be distinguishable from arbitrary permutations in the entanglement-invariant structure of the matching manifold. If all permutations give equivalent results, the coupling assignment has not yet acquired physical content.

### 6.5. Implementation

Python (NumPy/SciPy). Haar-random states via complex Gaussian normalization. Partial traces via tensor reshaping. Von Neumann entropy from eigenvalues of reduced density matrices. All code published for reproducibility.

---

## 7. Connections to Open Problems

The QIO suggests reframings — potentially productive changes of viewpoint — for several open problems. These are research directions, not resolutions.

### 7.1. De Sitter Holography

If spacetime universally emerges from entanglement, holography should extend beyond AdS. Recent work on static patch holography [34] and composite deformation flows [35] shows progress. De Sitter holography does not yet approach AdS/CFT-level rigor.

### 7.2. The Cosmological Constant

If the holographic principle constrains degrees of freedom to scale with area rather than volume, the QFT vacuum energy calculation overcounts. Freidel et al. (2023) [36] explored how holographic entropy bounds constrain vacuum energy, showing a technically natural result (Λ → 0 as IR scale increases). This is suggestive but does not derive the observed Λ, address radiative stability, or produce numerical predictions.

### 7.3. Gauge Unification and the Monopole Problem

Standard GUTs (SU(5), SO(10)) unify the three Standard Model gauge interactions; gravity is usually not part of these models. If the QIO/division-algebraic framework ultimately favors a direct origin of SU(3) × SU(2) × U(1) from octonionic entanglement structure — without embedding the Standard Model gauge group into a larger simply connected GUT group — then the usual monopole-producing symmetry-breaking patterns of conventional GUTs may not arise. This would reframe the monopole problem, but only if the QIO/division-algebraic framework replaces rather than supplements conventional GUT symmetry breaking. This possibility is conditional on the QIO's core posits and has not been demonstrated.

---

## 8. Discussion

### 8.1. What Distinguishes the QIO

The "It from Qubit" program [37] pursues emergent spacetime from entanglement. The division-algebraic program pursues Standard Model structure from octonions. The QIO claims these describe the same structure. Whether the Szangolies bridge between them is deep or superficial is an empirical question. The computational program in Section 6 addresses one facet of this question.

### 8.2. The Central Analytic Results

The most important technical contributions of this paper are negative. First, we prove that the naive coupling-entropy conjecture is underconstrained (Section 5.3): any two-parameter map fitting two couplings reduces the prediction of the third to a single scalar ratio that lies inside the feasible region of pure three-qubit states. Second, we compute that the log-inverse-coupling gap ratio r_SM(μ) varies substantially across energy scales (Section 6.3), establishing that a fixed entropy triple cannot match couplings at all scales under the logarithmic map.

These negative results are valuable because they precisely delineate what additional structure is needed. The underconstraint result redirects the program from numerical searching to algebraic selection of the vacuum state. The scale-dependence result suggests that if a coupling-entropy correspondence exists, it either holds at a privileged UV scale (with RG flow generating the low-energy hierarchy) or involves scale-dependent entanglement. The qualitative observation that couplings converging at high energy would correspond to more symmetric entanglement — while the low-energy hierarchy corresponds to asymmetric entanglement — remains a suggestive feature, though one-loop SM running does not produce exact three-coupling unification.

### 8.3. Risks and Failure Modes

The matching manifold may have no intersection with algebraically motivated states (Experiment 2 fails). The index ambiguity (Section 2.3) may prove fatal. The QIO may be too vague to produce testable predictions. These are acceptable outcomes — the purpose of precise conjecture is to enable definitive testing, including failure.

---

## 9. Conclusion

We have proposed the Quantum Information Ontology as a framework connecting two convergent research programs. We have reviewed both with explicit epistemic labeling, identified the Szangolies construction as a bridge, and formulated a coupling-entropy conjecture.

Our most important results are analytic. We prove that unconstrained three-qubit states can reproduce the observed Standard Model coupling hierarchy at M_Z under the logarithmic map, establishing that coupling matching alone is not evidence. We compute that the log-inverse-coupling gap ratio varies by ~24% between M_Z and 10⁶ GeV and becomes singular near the α₁-α₂ crossing, establishing that scale-independent entanglement cannot match couplings at all energies. Together, these results sharpen the QIO research program by identifying precisely what must be provided for coupling-entropy correspondence to become evidential: algebraic selection of the vacuum state and either a privileged UV scale or a mechanism for entanglement flow.

The qualitative observation that couplings converging at high energy would correspond to more symmetric entanglement, while the low-energy hierarchy corresponds to asymmetric entanglement, suggests a productive direction — though one-loop SM running does not produce exact three-coupling unification. Testing whether division-algebraic structure independently selects a vacuum state whose entanglement encodes the coupling hierarchy requires connecting the Szangolies and Furey constructions to concrete entanglement states and computing their properties. This is a well-defined mathematical problem for future work.

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

[9] J. Szangolies, "The Standard Model Symmetry and Qubit Entanglement," Entropy 27(6), 569 (2025).

[10] R. Mosseri and R. Dandoloff, "Geometry of entangled states, Bloch spheres and Hopf fibrations," J. Phys. A 34, 10243 (2001).

[11] B.A. Bernevig and H.-D. Chen, "Geometry of the three-qubit state, entanglement and division algebras," J. Phys. A 36, 8325 (2003).

[12] J.D. Bekenstein, "Black holes and entropy," Phys. Rev. D 7, 2333 (1973).

[13] S.W. Hawking, "Particle creation by black holes," Commun. Math. Phys. 43, 199 (1975).

[14] G. 't Hooft, "Dimensional reduction in quantum gravity," arXiv:gr-qc/9310026 (1993).

[15] L. Susskind, "The world as a hologram," J. Math. Phys. 36, 6377 (1995).

[16] J. Maldacena, "The large-N limit of superconformal field theories and supergravity," Int. J. Theor. Phys. 38, 1113 (1999).

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

[29] T. Favalli et al., *On the Emergence of Time and Space in Closed Quantum Systems*, Springer (2024).

[30] Particle Data Group, "Review of Particle Physics," Prog. Theor. Exp. Phys. (updated regularly; coupling values used here from the 2022 edition, R.L. Workman et al., 2022, 083C01).

[31] A. Higuchi, A. Sudbery, and J. Szulc, "One-qubit reduced states of a pure many-qubit state: polygon inequalities," Phys. Rev. Lett. 90, 107902 (2003).

[32] M.A. Nielsen and I.L. Chuang, *Quantum Computation and Quantum Information*, Cambridge University Press (2000).

[33] V. Coffman, J. Kundu, and W.K. Wootters, "Distributed entanglement," Phys. Rev. A 61, 052306 (2000).

[34] L. Susskind, "De Sitter holography," arXiv:2106.03964 (2021).

[35] Y.-X. Liu et al., "Toward a unified de Sitter holography," Sci. China Phys. Mech. Astron. (2026); arXiv:2511.16098.

[36] L. Freidel, J. Kowalski-Glikman, R.G. Leigh, and D. Minic, "Vacuum energy density and gravitational entropy," Phys. Rev. D 107, 126016 (2023).

[37] Simons Foundation "It from Qubit" collaboration; T. Takayanagi, "Emergent Holographic Spacetime from Quantum Information," arXiv:2506.06595 (2025).