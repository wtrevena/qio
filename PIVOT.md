# QIO 2.0: The Entropy-Flow Reformulation, a Dynamics Proposal, and the Jordan–Wigner Bridge

Date: 2026-06-09. Code: `experiments/exp{3,4,5}_*.py`; results in
`experiments/results/exp{3,4,5}_results.json`, Figure 2.

## 1. The revised conjecture (replaces the static log map of Sec 5.2)

**Conjecture (Entropy-Flow Map).** There exist constants A, B (B < 0) and a
one-parameter family of three-qubit pure states |Ω(μ)⟩ such that

    α_i⁻¹(μ) = A + B · S_i(μ),    dS_i/d log μ = −b_i / (2πB)

with the qubit-gauge assignment fixed by the Szangolies construction. The
entropies run linearly in log μ with slopes proportional to the one-loop beta
coefficients.

Why this is better than the static log map: (i) it is RG-consistent at all
scales *by construction* — the scale-dependence failure of Sec 6.3 dissolves;
(ii) it has a conceptual basis rather than a curve-fitting one: b_i count
degrees of freedom charged under each gauge factor, and entanglement entropy
in critical systems runs logarithmically with scale with coefficients that
count degrees of freedom (entropic c-functions, c/a-theorems). The slogan:
*coupling running and entanglement running are the same bookkeeping.* This
connects to entanglement renormalization (MERA), which is already the
framework's bridge to holography (Swingle).

Honesty clause: the map is still a reparametrization of measured couplings.
Its content lives in three places: the quantum-marginal feasibility
constraints (Sec 2 below — now nontrivial because they must hold at *every*
scale), the boundary condition at the symmetric point (Sec 3), and the
counting interpretation of the slopes (open).

## 2. Computed: the marginal constraints now do real work (Exp 3)

For the trajectory S_i(μ) to be realizable by pure three-qubit states at all
μ ∈ [M_Z, M_Planck], (A, B) must satisfy S ∈ [0,1]³ plus the
Higuchi–Sudbery–Szulc polygon inequality at every scale. Results:

- The box constraint alone requires |B| ≥ ~51. **The polygon inequality cuts
  91% of the box-allowed region** and forces |B| ≳ 126, A ≳ 106.
- Consequence: all three vacuum entropies are confined to a mid-band
  (roughly 0.37–0.77 at the representative point) at *every* scale — the
  framework forbids the vacuum from approaching either separability or
  maximal entanglement anywhere between M_Z and M_Planck. The slopes are
  small: |dS/d log μ| ~ 0.004–0.009 per e-fold.
- Structural feature: the entropy ordering *inverts* in the UV. At M_Z,
  S₁ > S₂ > S₃ (SU(3) most entangled); above the crossings
  (9.7×10¹², 2.4×10¹⁴, 1.05×10¹⁷ GeV), U(1) is most entangled.

## 3. Computed: the unification corollary (Exp 3)

Exact entanglement symmetry S₁ = S₂ = S₃ is equivalent to exact coupling
unification. Define the entanglement asymmetry ΔS(μ) = coupling spread /|B|:

- **SM:** most symmetric at μ* = 2.4×10¹⁴ GeV with ΔS ≈ 0.029 — it never
  symmetrizes (Fig 2c: the asymmetry bottoms out and rises again).
- **MSSM (1 TeV threshold):** ΔS cusps to ≈ 0.003 at 1.4×10¹⁶ GeV — an
  order of magnitude closer to symmetric.

If the framework demands an exactly symmetric UV boundary condition, it
*requires* coupling unification and therefore predicts BSM matter content.
This is a falsifiable commitment inherited honestly: the framework dies with
unification, and the SM alone does not unify.

## 4. Computed: a candidate dynamics (Exp 4)

The gap named in the draft — "no principle selects the vacuum's
entanglement" — now has a concrete candidate at three levels.

**Level 1 (kinematic):** the entropy-flow equation above. RG-consistent but
not yet explanatory.

**Level 2 (variational/algebraic): vacuum = ground state of a Hamiltonian
canonically built from the octonion algebra.** The left-multiplication
operators L_i = L_{e_i} satisfy the Clifford relation L_iL_j + L_jL_i =
−2δ_ij (machine-verified), so iL_i are Hermitian on ℂ⁸ = three qubits.
Findings:

- Linear Hamiltonians Σc_i(iL_i) have spectrum ±|c| with 4-fold degenerate
  ground spaces for *every* c — the Clifford structure forbids linear
  dynamics from selecting a vacuum.
- Commuting quadratic triples (105 pairings) give discrete vacua, almost all
  with degenerate entropy pairs — symmetric, no hierarchy.
- **[CORRECTED 2026-06-09 after Experiment 6.]** The initially reported
  hierarchical vacuum S = (0.630, 0.543, 0.430) was an artifact: Exp 4
  originally built (iL_a)(iL_b) = −L_aL_b, an antisymmetric (non-Hermitian)
  matrix, and `eigh` silently used its lower triangle. The correct
  Hermitian rotor Hamiltonian H = Σ_{a<b} σ(a,b) · iL_aL_b selects a
  **unique vacuum that is permutation-SYMMETRIC with exact invariants:**
  marginal spectra (1/7, 6/7) on every qubit (S = h₂(1/7) ≈ 0.5917),
  τ₃ = 8/49, all pairwise concurrences 2√2/7, so every CKW monogamy channel
  equals exactly 8/49 — perfectly balanced bipartite/tripartite
  entanglement. Spectrum {±3√7, ±√7(×3)}. The vacuum is the octonion
  (√7 e₀ − i Σ ±e_a)/√14. **Robustness (Exp 6): the sorted triple is
  IDENTICAL across all 128 sign gauges, all 5040 index relabelings
  (GL(3,2) subgroup included), 2000 random combined transformations, the
  opposite algebra, right-multiplication, and −H.** The unsigned-coupling
  control |σ| = 1 gives a SEPARABLE vacuum: the multiplication-table signs
  are what generate the entanglement.
- Reinterpretation: the algebra selects a *symmetric* entangled vacuum —
  exactly what the unification corollary wants as a UV boundary state
  (and its entropy 0.5917 sits inside the marginal-constraint mid-band).
  Hierarchy is a property of the flow, not the vacuum. Statics from
  algebra; hierarchy from RG.
- Generic random so(7) rotor Hamiltonians (corrected): unique vacua, 16.4%
  ordered, 0.9% land in the matching window, mean S ≈ 0.75 — the
  σ-structured choice occupies a distinguished symmetric position.

**Level 3 (aspirational):** identify the flow parameter of Level 1 with a
coarse-graining (MERA-like) flow whose fixed-point Hamiltonian is Level 2's.
Open.

## 5. Computed: the Jordan–Wigner bridge (Exp 5) — the Szangolies–Furey embedding exists

The draft (Sec 6.2) called the embedding of Furey's Cl(6) structures into
ℂ²⊗ℂ²⊗ℂ² "an open mathematical problem." It isn't: **Furey's Cl(6) is
generated by 3 fermionic ladder operators, Cl(6) ≅ M₈(ℂ) is exactly the
operator algebra of three qubits, and the Jordan–Wigner transformation is the
canonical isomorphism** (CAR relations machine-verified). Consequences
computed:

- Furey's minimal-left-ideal basis (one generation: ν, d̄×3, u×3, e⁺) maps to
  the 3-qubit computational basis graded by Hamming weight, with electric
  charge = weight/3. Charge quantization = integer grading of the qubit
  basis.
- The color-symmetric quark combination is the **W state**; the ν + e⁺
  superposition is the **GHZ state** (maximal charge-superselection
  violation). The SLOCC classes acquire particle-physics meaning.
- **Critical caveat discovered:** color rotations act on modes, not qubit
  factors — a color DFT maps a separable quark state to a (0.92, 0.92, 0.92)
  entangled one. Gauge transformations are NOT local unitaries of the qubit
  factorization, so entanglement in this frame is gauge-frame dependent. Any
  physical coupling-entropy correspondence must therefore be built from
  gauge-invariant entanglement functionals, or include an algebraic
  gauge-fixing of the tensor factorization. This sharpens (and partially
  explains) both the index ambiguity of Sec 2.3 and the Control D null.

## 6. What this changes

The paper's negative results stand and are strengthened. What changes is the
forward direction: replace "find constraints that make static matching
evidential" with three concrete, partially-computed research objects — the
entropy-flow map with its marginal-polytope bounds and unification corollary,
the σ-structured rotor Hamiltonian as a vacuum-selection mechanism, and the
Jordan–Wigner dictionary with its gauge-covariance problem. Each is
falsifiable or checkable; none requires believing the ontology.

Suggested disposition: keep the current paper's scope (negative results +
program), add the entropy-flow reformulation and the JW bridge as new
sections (they directly repair Sec 6.3's failure and resolve Sec 6.2's open
problem), and flag the rotor-Hamiltonian vacuum as preliminary pending the
convention-robustness check. The ontology language should be demoted to an
"information-first heuristic" throughout.
