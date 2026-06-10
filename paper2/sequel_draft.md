# Gauge-Invariant Entanglement in a Minimal Fermionic Toy: The Coupling–Entropy Question Made Well-Posed — and Closed

**W. [Author]**

*University of Florida (PhD, Industrial and Systems Engineering)*

June 2026

*Acknowledgment: Portions of this manuscript were developed with the assistance of Claude (Anthropic), an AI language model, which contributed to literature synthesis, mathematical exposition, drafting, and the computational experiments. All numerical claims are asserted at runtime by the published code (`direction_A/run_direction_A.py`, deterministic seed): the script fails if any verification breaks. Consistent with COPE authorship guidelines, the AI system is acknowledged as a tool rather than listed as a coauthor.*

---

## Abstract

A companion paper [1] showed that the question "is the Standard Model coupling hierarchy encoded in three-qubit vacuum entanglement?" is ill-posed: gauge transformations of the underlying fermionic modes are not local unitaries of the Jordan–Wigner qubit factorization, so single-qubit entropies are gauge-frame dependent. This paper makes the question well-posed and answers it. We replace subsystem entropies with entanglement relative to the gauge-invariant operator algebra — the commutant of the gauge action, in the algebra-relative framework of Barnum–Knill–Ortiz–Viola and Zanardi, which is the discrete cousin of the Casini–Huerta center decomposition for gauge fields. The commutants are computed numerically and identified exactly: gauging U(3) yields the abelian algebra ℂ⁴ of charge-sector projectors; SU(3) yields M₂ ⊕ ℂ ⊕ ℂ, with the M₂ block on span{ν, e⁺}; U(1) yields M₁ ⊕ M₃ ⊕ M₃ ⊕ M₁. Findings, all machine-verified with deterministic seeds: (i) the single-copy gauge-invariant data of any pure state under U(3) is its electric-charge-sector distribution alone; (ii) for every pure state and all three algebras the quantum piece of the algebraic entropy vanishes identically — the toy's gauge-invariant entanglement is 100% classical center term, the discrete analog of the edge-mode contribution in lattice gauge theory ("all edge, no bulk"); (iii) the companion paper's one surviving static "match" — the weighted-W coupling-matching curve — is pure gauge: every state on it has S_𝒜 = 0 for all three algebras and is gauge-equivalent to a single Fock basis state, with W = G(U)|001⟩ exhibited explicitly; (iv) the algebra-canonical rotor vacuum's invariant data is exactly (1/2, 3/14, 3/14, 1/14) with p₁ = p₂, i.e. two independent invariant parameters — fewer than three couplings; (v) an exhaustive search over 60 sector-assignment × feature-map combinations finds nothing within 0.05 of r_SM = 1.8174, the best unprincipled miss being r = 2 exactly; (vi) SU(2)_L is not representable on the one-generation ideal at all — the mode gauge group is U(3) ≅ (SU(3)_c × U(1)_em)/Z₃ — so the three-coupling question was never posable in this toy. The well-posed question has a sharper negative answer than the ill-posed one it replaces. We state plainly what would have to exist for any version to survive: a two-ideal construction on which SU(2)_L acts, and a principle linking sector statistics to couplings. Neither currently exists.

---

## 1. Introduction

The companion paper [1] asked whether the Standard Model gauge coupling hierarchy is encoded in the entanglement entropies of a three-qubit vacuum state, motivated by the convergence of the emergent-spacetime and division-algebraic programs through the Szangolies construction [5]. Its answer was a battery of no-go results, capped by a diagnosis: the question is *ill-posed*. Recognizing Furey's Cl(6) construction [2, 3, 4] as the three-qubit operator algebra under the Jordan–Wigner transformation [6] makes electric charge the Hamming-weight grading of the computational basis — and exposes the obstruction that gauge transformations act on the fermionic *modes*, not on the qubit tensor factors. A color discrete Fourier transform maps a separable single-quark state, with single-qubit entropies (0, 0, 0), to the W state, with entropies (0.918, 0.918, 0.918). The program's central quantity was frame decoration.

The companion paper closed by identifying the construction of a gauge-invariant entanglement functional as the central open problem ([1], Secs. 9.3, 11.2). This paper completes that program for the minimal toy, and reports what the completed version says.

The functional is not new and we do not claim it as such: entanglement relative to a distinguished *-subalgebra of observables is the "generalized entanglement" of Barnum, Knill, Ortiz, and Viola [8], the algebra-relative subsystem notion of Zanardi [7], and — in the form most relevant here — the algebraic definition that Casini, Huerta, and Rosabal introduced for gauge fields [9], whose classical center term Donnelly identified with lattice-gauge edge modes [10]. Our contribution is to *execute* this definition exactly, end to end, in the one system where the companion paper's question lives: the eight-dimensional one-generation ideal (ν, d̄, u, e⁺) in its Jordan–Wigner three-qubit presentation, under the three natural gauge choices U(3), SU(3), and U(1). Everything is finite-dimensional, so there are no regularization choices to argue about; the commutants are computed numerically and certified, the entropies have closed forms, and every claim in this paper is asserted at runtime by the published code.

### 1.1. Contributions

1. **The gauge-invariant algebras, computed and identified exactly** (Section 4). Gauging U(3) leaves only the abelian algebra ℂ⁴ of charge-sector projectors; SU(3) leaves M₂ ⊕ ℂ ⊕ ℂ (dimension 6), the M₂ block living on span{ν, e⁺} — the ν–e⁺ coherence is gauge-invariant when only color is gauged; U(1) leaves M₁ ⊕ M₃ ⊕ M₃ ⊕ M₁ (dimension 20). Under the full U(3), the single-copy gauge-invariant data of any pure state is its charge-sector distribution and nothing else.

2. **All edge, no bulk** (Section 5). For every pure state and all three algebras, the quantum piece of the algebraic entanglement entropy vanishes identically — a two-line consequence of the block structure, verified numerically to 1.8 × 10⁻¹⁵. The toy's entire gauge-invariant entanglement is the classical center term, the discrete analog of the edge-mode contribution in lattice gauge theory. As a corollary we derive S_U(1) = S_U(3) for every pure state, despite the U(1)-invariant algebra being five times larger.

3. **The headline: the companion paper's surviving "match" is pure gauge** (Section 5.4). Every point of the weighted-W coupling-matching curve — the one static construction in [1] that reproduced r_SM = 1.8174 — has S_𝒜 = 0 for all three invariant algebras and is gauge-equivalent to a single Fock basis state: one quark in a rotated color frame. We exhibit U ∈ SU(3) with G(U)|001⟩ = |W⟩ exactly. The static coupling-matching analysis of [1], Secs. 5–6, was matching frame artifacts.

4. **The well-posed question, answered** (Section 6). The gauge-invariant reformulation of the coupling-entropy question is stated and answered in the negative for four independent, machine-verified reasons: the invariant sectors are charge sectors, not gauge sectors; the algebra-canonical rotor vacuum carries exactly two independent invariant parameters, p = (1/2, 3/14, 3/14, 1/14) with p₁ = p₂; exhaustive search over sector-to-coupling assignments misses r_SM (best unprincipled miss: r = 2 exactly, flagged as numerology bait); and SU(2)_L admits no representation on the one-generation ideal, so a three-coupling question cannot even be posed.

5. **The bridge to the edge-mode literature, stated with its contested status on the surface** (Section 7.2). The center term computed throughout is the same object, in an 8-dimensional toy, as the classical flux-sector term of lattice gauge theory [9, 10] and the edge-mode reading of Kabat's contact term [11, 12, 13] — and we record honestly, following Casini–Huerta–Magán–Pontello [14], that the physical status of that term is itself contested in the continuum.

### 1.2. Scope

This paper is about an eight-dimensional toy. Nothing here bears on continuum gauge theory except by structural analogy, and the analogy's load-bearing limit is stated where it is used. The no-go results are exact within the toy and claim nothing beyond it; their value, if any, is that they close the minimal case cleanly and locate exactly what a non-minimal case would need.

---

## 2. The Toy and Its Gauge Action

**Status: construction inherited from [1], Sec. 9; machine-verified here to stated residuals.**

The arena is ℂ⁸ = ℂ² ⊗ ℂ² ⊗ ℂ² with three Jordan–Wigner fermionic modes

    f₁ = σ⁻ ⊗ I ⊗ I,    f₂ = Z ⊗ σ⁻ ⊗ I,    f₃ = Z ⊗ Z ⊗ σ⁻,

satisfying the canonical anticommutation relations exactly (residual 0.0 in our run). The computational basis is the Fock basis, graded by Hamming weight, and the weight is three times the electric charge on Furey's one-generation ideal [2, 3, 4]: ν at weight 0, the d̄ color triplet at weight 1, the u triplet at weight 2, e⁺ at weight 3, with Q = N/3 for N the number operator.

A mode rotation U ∈ U(3), f_b† ↦ Σ_a U_{ab} f_a†, induces the number-conserving unitary G(U) on ℂ⁸ acting blockwise on the weight sectors:

    weight 0: 1,    weight 1: U,    weight 2: Λ²U,    weight 3: det U,

with G(e^{iθ}1) = e^{iθN} on the U(1) subgroup. The construction was verified to machine precision: G unitary (residual 2.4 × 10⁻¹⁵), homomorphism G(U)G(V) = G(UV) (6.8 × 10⁻¹⁶), and the mode-transformation property G(U) f_b† G(U)† = Σ_a U_{ab} f_a† (1.9 × 10⁻¹⁵).

Three gauge choices are considered, each physically motivated: the full **U(3)** (color and electromagnetism together — the largest group of number-conserving mode rotations); **SU(3)** alone (gauge color, leave charge ungauged); and **U(1)** alone (charge superselection without color gauging). The group U(3) ≅ (SU(3)_c × U(1)_em)/Z₃ is the toy's entire mode gauge group; Section 6.5 explains why SU(2)_L is not on this list and cannot be.

---

## 3. Entanglement Relative to a *-Algebra

### 3.1. Definition

Let 𝒜 be a unital *-subalgebra of M_d(ℂ). By the Wedderburn–Artin theorem there is a unitary change of basis under which

    H ≅ ⊕_k ℂ^{n_k} ⊗ ℂ^{m_k},        𝒜 = ⊕_k M_{n_k}(ℂ) ⊗ 1_{m_k},

with commutant 𝒜′ = ⊕_k 1_{n_k} ⊗ M_{m_k} and center Z(𝒜) = 𝒜 ∩ 𝒜′ ≅ ℂ^{#blocks}, spanned by the minimal central projections P_k. The reduced state of |ψ⟩ on 𝒜 is the conditional expectation E_𝒜(|ψ⟩⟨ψ|) — equivalently, the unique state ω on 𝒜 with ω(a) = ⟨ψ|a|ψ⟩. Writing

    p_k = ⟨ψ|P_k|ψ⟩,    ρ_k = (1/p_k) Tr_{m_k}(P_k |ψ⟩⟨ψ| P_k),

the **algebraic entanglement entropy** is

    S_𝒜(ψ) = H({p_k}) + Σ_k p_k S(ρ_k)
            = [classical / CENTER piece] + [QUANTUM piece],     ... (1)

in bits throughout. This is the generalized entanglement of [8], the algebra-relative notion of [7], and — crucially — the discrete cousin of the Casini–Huerta–Rosabal definition for gauge fields [9]: when the algebra of a region in a lattice gauge theory has a nontrivial center (boundary electric fluxes), the entropy acquires exactly the H({p_k}) term — the Shannon entropy of the boundary-flux superselection sectors, nowadays read as the edge-mode contribution [10]. The center term computed throughout this paper is the same object in an 8-dimensional toy.

Two consistency limits: if 𝒜 = B(H_A) ⊗ 1_B is a factor, S_𝒜 = S(ρ_A) and the center piece is zero — the standard entanglement entropy is recovered; if 𝒜 is abelian (all n_k = 1), S_𝒜 = H({p_k}) is purely classical.

**Pitfall (machine-cross-checked on every call).** S_𝒜 is *not* the von Neumann entropy of the d × d matrix E_𝒜(ρ); the two differ by Σ_k p_k log₂ m_k, because E_𝒜(ρ) spreads each block uniformly over its multiplicity factor. The library computes S_𝒜 both ways and asserts agreement to 10⁻⁸.

### 3.2. Why This Is the Right Gauge-Invariant Functional

If a compact group acts on H by unitaries G(g), the gauge-invariant observables are exactly the commutant 𝒜 = {G(g)}′. Conjugation by any G(g) fixes 𝒜 pointwise, so E_𝒜(GρG†) = E_𝒜(ρ): **S_𝒜 is gauge-invariant by construction.** The quantity that was frame-dependent in [1] — single-qubit entropy — is replaced by one that provably cannot be. (Verified numerically below to ~10⁻¹⁵, alongside the O(1) shifts of the single-qubit entropies under the same transformations.)

**Honest scope note.** E_𝒜(ρ) captures every statistic obtainable by *single-copy measurements of gauge-invariant observables* — under a charge superselection rule this is all that is operationally accessible [15]. The polynomial invariant ring of the state under G is strictly larger: it contains multi-copy invariants (computed for the rotor vacuum in Section 7.4) that are constants of the G-orbit but not functions of E_𝒜(ρ). The well-posed question of Section 6 is phrased in terms of the operational single-copy data; the multi-copy ring is flagged as the remaining unexplored invariant content, not silently absorbed.

---

## 4. The Gauge-Invariant Algebras

**Status: computed (seed 20260609; `direction_A/results.json`).**

**Method.** For each gauge choice, 50 Haar samples G(U_s) were drawn and the commutant {X : [X, G(U_s)] = 0 ∀s} computed as the SVD nullspace of the stacked maps X ↦ (1 ⊗ G − Gᵀ ⊗ 1)vec(X). Each basis was certified against 100 fresh samples (maximum commutator residual < 1.2 × 10⁻¹⁵), checked to be a unital *-algebra (closure residual < 1.3 × 10⁻¹⁵), and its Wedderburn structure read off from the center and per-block ranks. Nothing below relies on paper-and-pencil representation theory; the structures are extracted from the numerics, and then agree with it.

| gauged group | dim 𝒜 | structure (block [weight support]) | center | invariant data of a pure state |
|---|---|---|---|---|
| **U(3)** | **4** | M₁[w0] ⊕ M₁⊗1₃[w1] ⊕ M₁⊗1₃[w2] ⊕ M₁[w3] — abelian ℂ⁴ | ℂ⁴ | (p₀, p₁, p₂, p₃): **3 real parameters** |
| **SU(3)** | **6** | **M₂**⊗1₁[w0 ∪ w3] ⊕ M₁⊗1₃[w1] ⊕ M₁⊗1₃[w2] | ℂ³ | (p₁, p₂) + pure qubit in the M₂ block: **4 parameters** |
| **U(1)** | **20** | M₁[w0] ⊕ **M₃**[w1] ⊕ **M₃**[w2] ⊕ M₁[w3] | ℂ⁴ | 3 probabilities + two projective pure states in ℂ³: **11 parameters** |

Readings, in turn:

* **U(3): the commutant is abelian.** The four weight sectors carry the inequivalent irreps (1, U, Λ²U, det U), each with multiplicity one, so the invariant algebra is the sector projectors and nothing more. *The only single-copy gauge-invariant data of any state is its charge-sector distribution (p₀, p₁, p₂, p₃).* This is the precise, gauge-invariant version of [1]'s "index ambiguity" (Sec. 2.3 there): there is no gauge-covariant tensor factorization because there are no gauge-invariant subsystems at all — only charge sectors.

* **SU(3): the ν–e⁺ coherence survives.** Weights 0 and 3 are both SU(3)-trivial, so the commutant contains a full M₂ block on span{|000⟩, |111⟩} = span{ν, e⁺} (machine check: the M₂ central projection equals the projector onto indices {0, 7} to 10⁻⁹). When only color is gauged, the GHZ-type ν–e⁺ coherence is gauge-invariant data. Weights 1 and 2 (the 3 and 3̄) remain inequivalent and contribute ℂ ⊕ ℂ.

* **U(1): everything weight-preserving.** G(e^{iθ}1) = e^{iθN}, so the commutant is M₁ ⊕ M₃ ⊕ M₃ ⊕ M₁ (dimension 20) — the richest of the three, retaining the full within-sector color states. Parameter-count sanity check: a pure state in ℂ⁸ has 14 real parameters; gauging U(1) erases exactly the 3 relative phases between the four sectors: 14 − 3 = 11. ✓

So under U(3) the invariant data has exactly 3 real parameters — naive room for one per coupling. Section 6 is about why that room cannot be used.

---

## 5. Gauge-Invariant Entanglement of the Named States

**Status: computed; closed forms machine-checked to 10⁻¹².**

### 5.1. The Quantum Piece Vanishes Identically

**Proposition 1.** For every pure state |ψ⟩ ∈ ℂ⁸ and each of the three algebras above, the quantum piece of Eq. (1) vanishes: S_𝒜(ψ) = H({p_k}).

*Proof.* Every Wedderburn block of all three algebras has n_k = 1 or m_k = 1. If n_k = 1, then ρ_k is a 1 × 1 state and S(ρ_k) = 0 trivially. If m_k = 1, the multiplicity factor is trivial, so P_k|ψ⟩ is a vector in the block and ρ_k = P_k|ψ⟩⟨ψ|P_k / p_k is a rank-one projector: S(ρ_k) = 0. ∎

(Numerical confirmation: maximum |quantum piece| = 1.8 × 10⁻¹⁵ over the named states and a 200-state subsample of the 10⁴-state Haar ensemble run through the full block machinery; the remaining ensemble states were evaluated with a sector formula that agrees with the full machinery to 2.0 × 10⁻¹⁵ on that subsample.)

In Casini–Huerta language: for pure states, this toy is *all edge-mode term, no bulk term*. Any claim that "vacuum entanglement encodes couplings" in this framework is therefore, gauge-invariantly, a claim about classical charge statistics. Section 7.2 develops this bridge; here we note the scope limit on the surface: Proposition 1 is a statement about *pure* states. For mixed states the SU(3) and U(1) algebras can acquire nonzero quantum pieces (the U(3) entropy stays classical for all states because the algebra is abelian); and the first system in this program where a nonzero quantum piece could appear for pure states needs blocks with both n_k, m_k > 1 — e.g. regional subalgebras, or the two-ideal extension of Section 7.3.

**Corollary 2 (S_U(1) = S_U(3) for every pure state).** The U(1) and U(3) commutants have the same center — the four weight projectors. By Proposition 1, both entropies equal H(p₀, p₁, p₂, p₃). ∎

This holds even though the U(1)-invariant algebra is five times larger: gauging the extra SU(3) changes *which states are distinguishable* (the U(1) data distinguishes W from |001⟩; the U(3) data does not) but not the entropy. Entropy is a very lossy summary of E_𝒜(ρ) — a deflation worth keeping in view whenever a single number is asked to carry structural weight.

### 5.2. The Table

All entropies in bits; sector probabilities exact rationals (machine-checked against the numerics to 10⁻¹⁰). The rightmost column shows the gauge-*variant* single-qubit entropies for contrast.

| state | (p₀, p₁, p₂, p₃) | S_U(3) | S_SU(3) | S_U(1) | single-qubit S (gauge-variant) |
|---|---|---|---|---|---|
| **rotor vacuum** (√7 e₀ − iu)/√14 | **(1/2, 3/14, 3/14, 1/14)** exact | **1.724408** | **1.413800** | 1.724408 | (0.5917, 0.5917, 0.5917) |
| **W** = color-uniform d̄ | (0, 1, 0, 0) | **0** | **0** | **0** | (0.9183, 0.9183, 0.9183) |
| **GHZ** = (ν + e⁺)/√2 | (1/2, 0, 0, 1/2) | **1** | **0** | 1 | (1, 1, 1) |
| **weighted-W matching state** ([1], Fig. 1c curve) | (0, 1, 0, 0) | **0** | **0** | **0** | (0.9995, 0.8580, 0.7802) |
| Haar ensemble (10⁴), mean ± std | — | 1.580 ± 0.239 | 1.398 ± 0.162 | = S_U(3) | — |

Exact closed forms for the rotor vacuum (machine-checked to 10⁻¹²):

    S_U(3) = S_U(1) = 1/2 + (1/2) log₂ 14 − (3/7) log₂ 3 = 1.724407817863 bits
    S_SU(3) = (4/7)(log₂ 7 − 2) + (3/7) log₂ (14/3)      = 1.413799564606 bits

and the SU(3)-invariant qubit in the M₂ (ν/e⁺) block is pure, with block probability 4/7 and state ρ = (1/8)[[7, i√7], [−i√7, 1]] — the gauge-invariant ν–e⁺ coherence.

**Gauge invariance verified (the whole point).** For every named state, every algebra, and 20 random elements of the corresponding gauge group: max |ΔS_𝒜| < 3 × 10⁻¹⁵ (assertion threshold 10⁻⁹), while the single-qubit entropies of the *same* transformed states shift by up to 0.9226 bits. Bonus, also verified to ~10⁻¹⁵: S_SU(3) and S_U(1) are invariant under the *full* U(3) — G(U) normalizes the weight decomposition, and the extra U(1) phases are isospectral on the M₂ block.

### 5.3. State by State

**The W state's entanglement is pure gauge.** We exhibit U ∈ SU(3) (third column (1,1,1)/√3) with G(U)|001⟩ = |W⟩ exactly (construction residual 0.0), and verify E_𝒜(W) = E_𝒜(|001⟩) for the U(3) algebra (residual 2.6 × 10⁻¹⁶). The paradox that opened the well-posedness diagnosis in [1], Sec. 9.3 — a separable quark state mapped to the "entangled" W by a color DFT — is here resolved rather than flagged: the algebraic entropy assigns **zero to both**, because a single quark in a color-rotated frame is still a single quark. The 0.918 bits the W state carries in the qubit factorization is entirely frame.

**GHZ is one classical bit — or nothing.** Under U(3), which contains the electromagnetic U(1), the GHZ state's invariant content is the charge distribution (1/2, 0, 0, 1/2): exactly one bit of classical charge uncertainty, no quantum piece. Under SU(3) only, the ν–e⁺ coherence sits inside the M₂ invariant block as a *pure* qubit, and S_SU(3)(GHZ) = 0. The "maximal tripartite entanglement" of GHZ is, gauge-invariantly, either one classical bit (charge superselection imposed) or no entropy at all (color-only gauging). Nothing about it is three-partite in any invariant sense. The toy cleanly separates color gauging from charge superselection here: the ν–e⁺ coherence is physical data if and only if the abelian factor is not gauged.

**The rotor vacuum** — the unique ground state of the companion paper's algebra-canonical Hamiltonian H = i(L_u + 2R_u) ([1], Sec. 8) — is the only state in the list with nontrivial invariant data, and that data is two numbers (Section 6.3). Its invariant entropy, 1.724 bits, is comfortably *generic*: the Haar mean is 1.580 ± 0.239. Gauge-invariantly, the canonical vacuum is not even unusually entangled.

### 5.4. The Headline: the Coupling-Matching Curve Collapses to Pure Gauge

The companion paper's only surviving static "match" was the weighted-W family: a continuous curve of states a|001⟩ + b|010⟩ + c|100⟩ reproducing the Standard Model log-inverse-coupling gap ratio r_SM = 1.8174 exactly under the two-parameter affine ansatz ([1], Secs. 5.3, 6.2, Fig. 1c). Every state on that curve is a weight-1 state. Its invariant data is therefore p = (0, 1, 0, 0), identical to that of the Fock state |001⟩, and

    S_𝒜 = 0 on the entire curve, for all three algebras

(verified on all stored curve points; max |S_𝒜| = 1.9 × 10⁻¹⁵ — and exact by the support argument, since the conclusion depends only on the curve lying inside the weight-1 sector). The entire matching curve is one U(3) gauge orbit point: gauge-equivalent to a single d̄ quark in a rotated color frame. *The static coupling-matching analysis of [1], Secs. 5–6, was matching gauge artifacts.* The companion paper diagnosed its title question as ill-posed; the well-posed functional goes further and evaluates the would-be evidence at exactly zero.

### 5.5. Haar Ensemble and Analytic Cross-Check

Over 10⁴ Haar-random pure states: S_U(3) has mean 1.5798, std 0.2391, range [0.4103, 1.9984]; S_SU(3) has mean 1.3981, std 0.1617, range [0.4066, 1.5849]. These match the analytic values: for Haar states the sector probabilities are Dirichlet-distributed with parameters the sector dimensions, p ~ Dir(1, 3, 3, 1), giving E[S_U(3)] = 1.5767 via digamma sums; merging the SU(3)-trivial weights {0, 3} gives Dir(2, 3, 3) and E[S_SU(3)] = 1.3963. Sampled-vs-analytic discrepancies (0.003, 0.002) are consistent with N = 10⁴ fluctuations.

---

## 6. The Well-Posed Question and Its Answer

### 6.1. The Reformulation

> **Well-posed question.** Let 𝒜 be the commutant of the gauge action on the one-generation ideal. Does there exist a *natural* map from the single-copy gauge-invariant data E_𝒜(|Ω⟩⟨Ω|) of an algebra-selected vacuum |Ω⟩ to the three Standard Model couplings (α₃, α₂, α₁) — "natural" meaning the assignment of invariant parameters to gauge factors is dictated by the algebra, not chosen by hand?

This is well-posed where the title question of [1] was not: E_𝒜 is gauge-invariant by construction (verified to 10⁻¹⁵), and "how many independent parameters are available" is now a theorem rather than a frame choice. Under U(3) the invariant data has exactly 3 real parameters — so there is naive room, one per coupling. The answer is nevertheless no, for four independent reasons, each machine-verified.

### 6.2. Reason 1: the Sectors Are Charge Sectors, Not Gauge Sectors

The center of the U(3)-invariant algebra is spanned by the projectors onto eigenspaces of the *single operator* N (electric charge Q = N/3). The four labels {0, 1/3, 2/3, 1} are values of one U(1) quantum number. The SU(3) factor contributes no additional center label — weights 1 and 2 carry the 3 and 3̄, but that is representation *type*, not a continuous parameter — and there are four sectors for three would-be couplings. A map (p₁, p₂, p₃) → (α₃, α₂, α₁) requires a bijection {charge sectors} → {gauge factors} that nothing in the algebra provides: the invariant data simply does not factorize along gauge factors. This is the companion paper's "index ambiguity" ([1], Sec. 2.3) promoted from labeling worry to structural fact.

### 6.3. Reason 2: the Algebra-Canonical Vacuum Has Only Two Parameters

The rotor vacuum's invariant data is exactly

    p = (1/2, 3/14, 3/14, 1/14),    with p₁ = p₂ exactly,

because the vacuum (√7 e₀ − iu)/√14 has uniform |amplitude|² = 1/14 on all seven imaginary units, forcing p_k proportional to the sector dimension on weights 1–3 (machine check: |p₁ − p₂| < 10⁻¹⁶; the rationals certified against the floats to 10⁻¹⁰). The canonical vacuum therefore carries **two independent invariant parameters — fewer than three couplings.** The permutation degeneracy that killed every hierarchical reading in the frame-dependent analysis ([1], Secs. 6.2, 8) *survives gauge-invariantization* as an exact sector degeneracy. The obstruction was never the frame; it is the algebra's symmetry.

### 6.4. Reason 3: No Assignment Reproduces the Hierarchy Anyway

Even granting an unprincipled sector-to-coupling assignment, the numbers refuse. We tested every ordered assignment of three distinct charge sectors to the three couplings under three feature maps (p_k, log₂ p_k, −p_k log₂ p_k) — 3 × 24 = 72 combinations, of which 60 yield a finite gap ratio (the p₁ = p₂ degeneracy renders 12 indeterminate) — against the inherited two-parameter affine ansatz, i.e. demanding r = (x_a − x_b)/(x_b − x_c) equal r_SM = 1.8174 ([1], Eqs. 2–3; GUT-normalized α₁, a convention this target inherits). Result: **none lands within the companion paper's widened tolerance 0.05** (let alone the 0.01 of its Experiment 1); the best miss is

    r = 2 exactly    (feature p, descending sectors (0, 1, 3) or (0, 2, 3)),  distance 0.1826.

We flag this near-miss explicitly so nobody rediscovers it as a "signal": r = 2 versus 1.8174 is a 10% coincidence of small fractions — (1/2 − 3/14)/(3/14 − 1/14) = 2 — reachable only through assignments that, absurdly, put the *neutrino* sector and the *positron* sector on two different gauge couplings while skipping one of the two exactly degenerate quark sectors. Assignments using both quark sectors give r ∈ {0, −1, ±∞}, degenerate by p₁ = p₂. This is numerology bait, not structure.

### 6.5. Reason 4: SU(2)_L Is Not in the Toy at All

**Status: structural argument, not a numerical experiment; recorded with its reasons.**

The mode-rotation (number-conserving Bogoliubov) gauge group of three Jordan–Wigner modes is exactly U(3) ≅ (SU(3)_c × U(1)_em)/Z₃ — there is no room for an independent SU(2) acting on the color modes. More physically, the ideal (ν, d̄_i, u_i, e⁺) contains no weak-isospin doublet pair: ν_L pairs with e⁻_L (absent — the ideal contains e⁺), u_L with d_L (absent — the ideal contains d̄). Weak raising and lowering operators would map this ideal into a *different* ideal; in Furey's full construction SU(2)_L acts on the quaternionic factor of ℂ ⊗ ℍ ⊗ 𝕆 — between ideals, never within one [3]. And the toy's abelian charge is electromagnetic Q = N/3, not hypercharge: SU(2)_L does not commute with Q, so any implementation would have to move states between Hamming-weight sectors, and the only weight-0/weight-3 pair, (ν, e⁺), is not a doublet.

Consequently *the three-coupling question cannot even be posed gauge-covariantly on a single generation ideal*: at most two gauge factors (SU(3)_c, U(1)_em) act, and their joint invariant data is the charge distribution. The companion paper asked whether three couplings are encoded in this system; the gauge-covariant accounting says the system never had three couplings' worth of symmetry to begin with.

### 6.6. Verdict: More Constrained, Not Less

The ill-posed version of the question was *underconstrained*: a 14-real-parameter state space, a guaranteed-nonempty one-parameter matching manifold, statistically generic matches, W-class realizations ([1], Secs. 5.3, 6.1–6.2). The well-posed version is drastically *more* constrained:

* the invariant state space shrinks from 14 parameters to 3 (U(3));
* the entire weighted-W matching mechanism is annihilated — S_𝒜 = 0 on the whole curve;
* the algebra-selected vacuum's data is fixed and degenerate: two parameters, p₁ = p₂;
* no natural sector → factor map exists, and the exhaustive unnatural ones miss r_SM;
* one of the three couplings has no corresponding symmetry in the toy at all.

> **Answer to the re-posed question: no — and now provably, not just diagnostically.** The gauge-invariant entanglement data of a single pure state in this toy is its electric-charge statistics. Charge statistics has no natural three-fold structure aligned with the three gauge factors; the canonical vacuum's statistics are two-parameter degenerate; and SU(2)_L is absent from the construction. The coupling hierarchy is not, and cannot be, encoded in the gauge-invariant entanglement of a single pure state of this toy.

---

## 7. Discussion

### 7.1. The No-Go Ladder

Across the two papers, the coupling-entropy question has now descended a complete ladder, each rung sharper than the last:

1. **Frame-dependent** ([1], Secs. 5–6): the static matching analysis succeeded too easily — matching was statistically generic, null controls matched equally well, and the one algebraically flavored success (the weighted-W curve) survived.
2. **Ill-posed** ([1], Sec. 9.3): the quantity being matched, single-qubit entropy of the Jordan–Wigner factorization, is not gauge-invariant. Diagnosis, not yet answer.
3. **Well-posed** (this paper, Secs. 3–4): replace subsystem entropy by entanglement relative to the gauge-invariant algebra. The question now has a definite, frame-independent content: three real parameters under U(3).
4. **Still no** (this paper, Sec. 6): the well-posed question has a negative answer for four independent structural reasons — and it retroactively evaluates the rung-1 evidence at exactly zero (Sec. 5.4).

The pattern is worth stating because it is the opposite of the usual fear about no-go results: making the question well-posed did not rescue a positive answer that ill-posedness had been obscuring; it converted a diagnostic "the question is meaningless" into a computed "the question is meaningful and the answer is no."

### 7.2. All Edge, No Bulk: the Bridge to the Continuum — With Its Dispute Included

For pure states in this toy, the algebraic entanglement entropy is 100% center term (Proposition 1) — the discrete analog of the statement that a lattice-gauge entanglement entropy is carried by the classical boundary-flux (edge-mode) distribution. The lineage of that object in the continuum is well documented: Kabat's contact term in the conical entropy of gauge fields [11]; the Donnelly–Wall edge-mode program, which interpreted it as the Shannon entropy of normal-flux sectors [12, 13]; Donnelly's lattice form, S = H({p_R}) + Σ p_R(...), of which Eq. (1) is the abstract finite-dimensional version [10]; and the Casini–Huerta–Rosabal algebra-with-center formulation that our definition discretizes directly [9]. The toy realizes this structure in its most extreme form: all edge, no bulk. Any future claim that vacuum entanglement encodes couplings in this framework is therefore, gauge-invariantly, a claim about precisely the object that literature studies as edge modes.

Honesty requires importing the dispute along with the structure. Casini, Huerta, Magán, and Pontello [14] argue that in the continuum the center/edge term is an artifact of the algebra (equivalently regularization) choice: local continuum algebras need not have centers, the classical term drops out of mutual information and relative entropy, and related work shows it is not distillable [16, 17]. On that view, the quantity this paper computes wholesale — H({p_k}) — is exactly the piece of "entanglement entropy" whose physical status is contested. Three things can be said in the toy's defense, none of them a refutation. First, in the toy the algebra is not a regularization choice: given the gauge group, the commutant is canonical — the ambiguity that worries [14] reappears here only as the (physically meaningful) choice of *which group to gauge*, and we computed all three. Second, under a charge superselection rule the center term has a clean single-copy operational reading [15]: it is the Shannon entropy of the charge measurement that superselected observers can actually perform. Third, and cutting the other way: if one adopts the strict Casini–Huerta–Magán–Pontello standard — only mutual-information-like quantities are physical — then the toy's gauge-invariant entanglement is not merely classical but arguably *empty*, and the no-go of Section 6 becomes if anything stronger. The dispute does not threaten our negative conclusion; it threatens only the consolation prize.

### 7.3. What Two Ideals Would Change

The single most direct continuation is the two-ideal extension: build the 16-dimensional two-ideal space (or the full Cl(6) Fock space with Furey's left/right ideal pair), implement SU(2)_L as the ideal-mixing quaternionic action, and recompute the commutant of the full S(U(3) × U(2))-type action with the same machinery. That construction would be the first in this program on which a three-coupling question is even posable gauge-covariantly. The questions it must answer are exactly the ones the one-ideal no-go quantifies: does the center acquire a natural *threefold* structure aligned with gauge factors, or does the charge-sector obstruction of Section 6.2 persist? And do blocks with both n_k, m_k > 1 appear, so that a nonzero quantum piece — genuine gauge-invariant quantum entanglement, "bulk" — exists for pure states at all? We make no prediction beyond noting that every symmetry-based degeneracy found so far has survived each previous upgrade of the formalism.

### 7.4. Beyond Single Copies: the Remaining Invariant Content

The no-go of Section 6 governs single-copy gauge-invariant data — everything measurable under the superselection rule. The full polynomial invariant ring of a state under G(U(3)) is strictly larger, and for the rotor vacuum its low-degree elements are nonzero and exactly computable: with v₁, v₂ the weight-1 and weight-2 component vectors,

    |v₁ ∧ v₂| = 1/14 exactly,
    |v̄₃ · (v₁ ∧ v₂)| = 14^{−3/2} ≈ 0.019090,
    |v̄₀ v₃ (v₁ ∧ v₂)̄ | = √7/196 ≈ 0.013499,

all verified gauge-invariant to 5.6 × 10⁻¹⁷ under random G(U). These are not functions of (p₀, …, p₃): they are constants of the gauge orbit invisible to E_𝒜. The single-copy no-go therefore does not automatically extend to the full invariant ring — though it does extend to anything operationally accessible under superselection, and we know of no principle that would route three coupling constants through multi-copy invariants while bypassing every single-copy observable. Characterizing the full U(3) invariant ring on ℂ⁸ (generator count via Jacobian rank at generic points) is concrete, undone work.

### 7.5. Limitations

The obvious one bears repeating: this is an 8-dimensional toy with no dynamics, no scale, and (Sec. 6.5) at most two gauge factors. The no-go results are exact but local to the construction; they constrain the minimal three-qubit literalism of the companion paper's program, not gauge theory. The flow version of the question — whether any RG-consistent trajectory on the sector simplex, with the rotor vacuum's (1/2, 3/14, 3/14, 1/14) as boundary data, can reproduce one-loop running — remains open, though Section 6.2 makes the expected outcome plain: the simplex has no natural three-coupling structure either. Finally, the r_SM = 1.8174 target inherits the GUT normalization α₁ = (5/3)α_Y from [1]; the exhaustive-search miss of Section 6.4 is in that sense convention-dependent, but the structural reasons (Secs. 6.2, 6.3, 6.5) are not — p₁ = p₂ does not care how the abelian coupling is normalized.

---

## 8. Conclusion

The companion paper ended by declaring the coupling-entropy question ill-posed until a gauge-invariant entanglement functional was specified, and named that specification the program's central open problem. This paper specified the functional — the standard algebraic one, executed exactly — and the completed program closes the question rather than reopening it. The well-posed question has a sharper negative answer than the ill-posed one: the gauge-invariant entanglement of any pure state of the minimal fermionic toy is its electric-charge statistics, entirely classical ("all edge, no bulk"); the algebra-canonical vacuum carries two independent invariant parameters, not three; the one positive-seeming static result of the companion paper is revealed to be a single quark in a rotated color frame, with invariant entropy exactly zero; and the weak gauge factor was never representable on the construction in the first place.

For any version of the coupling-entropy correspondence to survive, two things would need to exist, neither of which currently does. First, a richer arena: a two-ideal (or larger) construction on which SU(2)_L acts, so that a three-coupling question is gauge-covariantly posable at all — and on which one can then check whether the invariant center acquires a natural threefold structure aligned with gauge factors, or whether the charge-sector obstruction found here persists. Second, a principle: an algebra-dictated, not hand-chosen, map from gauge-invariant sector statistics to coupling constants, presumably with scale dependence built in. Absent both, the conclusion of the minimal case stands as computed: there is nothing in the gauge-invariant entanglement of this toy for the Standard Model couplings to be encoded in. We offer the closed case, the machinery (which applies unchanged to any finite-dimensional gauge action), and the precise specification of what a successor construction must provide.

---

## References

[1] W. [Author], "Is the Standard Model Coupling Hierarchy Encoded in Three-Qubit Vacuum Entanglement? No-Go Results, an Exact Octonionic Vacuum, and the Surviving Hypothesis Space," companion paper (2026). Code and data: `experiments/` directory of the same repository.

[2] C. Furey, "Generations: three prints, in colour," JHEP 2014, 046 (2014).

[3] C. Furey, "SU(3)_C × SU(2)_L × U(1)_Y (× U(1)_X) as a symmetry of division algebraic ladder operators," Eur. Phys. J. C 78, 375 (2018).

[4] O.C. Stoica, "Leptons, quarks, and gauge from the complex Clifford algebra Cl(6)," Adv. Appl. Clifford Algebras 28, 52 (2018); arXiv:1702.04336.

[5] J. Szangolies, "The Standard Model Symmetry and Qubit Entanglement," Entropy 27(6), 569 (2025); arXiv:2512.17328.

[6] P. Jordan and E. Wigner, "Über das Paulische Äquivalenzverbot," Z. Phys. 47, 631 (1928).

[7] P. Zanardi, "Virtual quantum subsystems," Phys. Rev. Lett. 87, 077901 (2001).

[8] H. Barnum, E. Knill, G. Ortiz, and L. Viola, "A subsystem-independent generalization of entanglement," Phys. Rev. Lett. 92, 107902 (2004).

[9] H. Casini, M. Huerta, and J.A. Rosabal, "Remarks on entanglement entropy for gauge fields," Phys. Rev. D 89, 085012 (2014); arXiv:1312.1183.

[10] W. Donnelly, "Entanglement entropy and nonabelian gauge symmetry," Class. Quantum Grav. 31, 214003 (2014); arXiv:1406.7304.

[11] D. Kabat, "Black hole entropy and entropy of entanglement," Nucl. Phys. B 453, 281 (1995); arXiv:hep-th/9503016.

[12] W. Donnelly and A.C. Wall, "Entanglement entropy of electromagnetic edge modes," Phys. Rev. Lett. 114, 111603 (2015); arXiv:1412.1895.

[13] W. Donnelly and A.C. Wall, "Geometric entropy and edge modes of the electromagnetic field," Phys. Rev. D 94, 104053 (2016); arXiv:1506.05792.

[14] H. Casini, M. Huerta, J.M. Magán, and D. Pontello, "Logarithmic coefficient of the entanglement entropy of a Maxwell field," Phys. Rev. D 101, 065020 (2020); arXiv:1911.00529.

[15] S.D. Bartlett, T. Rudolph, and R.W. Spekkens, "Reference frames, superselection rules, and quantum information," Rev. Mod. Phys. 79, 555 (2007).

[16] R.M. Soni and S.P. Trivedi, arXiv:1608.00353 (entanglement in gauge theories; non-distillability of the classical edge term).

[17] U. Moitra, R.M. Soni, and S.P. Trivedi, arXiv:1811.06986 (the classical term does not contribute to relative entropy or mutual information in the continuum limit).

[18] Particle Data Group, "Review of Particle Physics," Prog. Theor. Exp. Phys. 2022, 083C01 (2022) — coupling values entering r_SM = 1.8174 via [1], Eqs. (2)–(3).

---

## Appendix A. Reproducibility

**Code.** All computations in this paper are produced by two files in the repository's `direction_A/` directory:

* `alg_entanglement.py` — library: numerical commutant (SVD nullspace of the stacked commutator maps), Wedderburn structure identification (center, minimal central projections, per-block ranks), trace-preserving conditional expectation, algebraic entropy with the built-in cross-check S_𝒜 = S(E_𝒜(ρ)) − Σ_k p_k log₂ m_k asserted to 10⁻⁸ on every call, Jordan–Wigner modes, the G(U) construction, and Haar samplers.
* `run_direction_A.py` — every computation reported here, in order; fixed seed 20260609; every claim asserted at runtime, so the script fails if any verification breaks; writes `results.json`.

Run: `python run_direction_A.py` (≈ 6 s; NumPy + SciPy only). The script reads `../experiments/results/exp2_results.json` (published with [1]) for the weighted-W matching-curve amplitudes tested in Section 5.4.

**Sampling protocol.** Commutants: 50 Haar generator samples per gauge group, certified against 100 fresh samples (max commutator residual < 1.2 × 10⁻¹⁵) and checked for unital *-closure (< 1.3 × 10⁻¹⁵). Gauge invariance: 20 random gauge elements per state per group (assertion threshold 10⁻⁹; observed < 3 × 10⁻¹⁵). Haar ensemble: 10⁴ states, with a 200-state subsample run through the full block machinery (fast-formula agreement 2.0 × 10⁻¹⁵; max |quantum piece| 1.8 × 10⁻¹⁵) and analytic Dirichlet cross-checks of the means asserted to 0.01.

**Exact rationals.** Sector probabilities reported as fractions (1/2, 3/14, 3/14, 1/14, etc.) are produced by `Fraction(x).limit_denominator(10⁴)` and asserted to agree with the floating-point values to 10⁻¹⁰; the closed-form entropies are asserted against the numerics to 10⁻¹²; |v₁ ∧ v₂| = 1/14 is asserted to 10⁻¹². The statement p₁ = p₂ is exact by construction (uniform |amplitude|² = 1/14 on the seven imaginary units forces p_k ∝ sector dimension on weights 1–3) and machine-checked to < 10⁻¹⁶.

**Construction residuals** (this run): CAR relations 0.0; G(U) unitarity 2.4 × 10⁻¹⁵; homomorphism 6.8 × 10⁻¹⁶; mode-transformation property 1.9 × 10⁻¹⁵; W = G(U)|001⟩ construction 0.0, with E_𝒜 reduction agreement 2.6 × 10⁻¹⁶; M₂-block support identification 10⁻⁹.
