# Direction A: Gauge-Invariant (Algebraic) Entanglement in the Jordan-Wigner Three-Qubit Toy

> **Status (2026-06-10): superseded by `paper2/` (main.tex / sequel_draft.md).** This working
> report predates the referee round and strengthening pass; where numbers or claims differ,
> Paper 2 and its machine-checked Appendix B are authoritative.

**Goal.** Section 9.3 of the paper (`draft.md`) showed that the title question -- *is the SM coupling
hierarchy encoded in three-qubit vacuum entanglement?* -- is ill-posed: single-qubit entropies of the
Jordan-Wigner factorization are not gauge-invariant (a color DFT maps a separable quark state,
S = (0,0,0), to the W state, S = (0.918, 0.918, 0.918)). This report makes the question well-posed by
replacing subsystem entanglement with **entanglement relative to the gauge-invariant operator
algebra** (Barnum-Knill-Ortiz-Viola / Casini-Huerta), computes everything exactly in the toy, and
answers the re-posed question. The answer is a **sharp no-go** -- sharper than the ill-posedness it
replaces -- with every step machine-verified (`run_direction_A.py`, seed 20260609, results in
`results.json`).

**Headline results.**

1. The gauge-invariant algebras are computed numerically as commutants and identified exactly:
   U(3) -> abelian **C^4** (charge-sector projectors only); SU(3) -> **M2 (+) C (+) C**; U(1) ->
   **M1 (+) M3 (+) M3 (+) M1**.
2. For **every pure state**, the algebraic entanglement entropy is **purely classical (center)
   charge statistics** for all three gauge choices; the quantum piece vanishes identically
   (verified to 1.8e-15: full machinery on a 200-state subsample of the 10^4 Haar ensemble; sector-statistics consistency on all 10^4). In Casini-Huerta language: this toy is *all
   edge-mode term, no bulk term* -- a direct bridge to Direction B.
3. The rotor vacuum's gauge-invariant data is exactly **p = (1/2, 3/14, 3/14, 1/14)**, with
   S_U(3) = 1/2 + (1/2)log2(14) - (3/7)log2(3) ~ **1.724408 bits** and S_SU(3) ~ **1.413800 bits**.
   Crucially **p1 = p2 exactly**: the algebra-canonical vacuum carries only **two** independent
   invariant parameters -- fewer than three couplings.
4. The paper's one "positive" static result -- the weighted-W coupling-matching curve -- **collapses
   to pure gauge**: every point on it has S_A = 0 for all three algebras and is gauge-equivalent to a
   single Fock basis state (one quark in a rotated color frame).
5. SU(2)_L cannot be represented on this one-generation ideal at all; the toy's gauge group is at
   most U(3) ~ (SU(3)_c x U(1)_em)/Z3, so a *three*-coupling question was never available here.

---

## 1. Theory: entanglement relative to a *-algebra

### 1.1 Definition

Let A be a unital *-subalgebra of M_d(C) (closed under adjoints and products, containing 1). By the
Wedderburn-Artin theorem there is a unitary change of basis under which

    H  ~  (+)_k  C^{n_k} (x) C^{m_k},        A = (+)_k  M_{n_k}(C) (x) 1_{m_k},

so A acts irreducibly (with multiplicity m_k) on each block. Its commutant is
A' = (+)_k 1_{n_k} (x) M_{m_k}, and the **center** Z(A) = A ^ A' ~ C^{#blocks} is spanned by the
minimal central projections P_k.

The **reduced state of |psi> on A** is the conditional expectation E_A(|psi><psi|) -- equivalently,
the unique state w on A with w(a) = <psi|a|psi>. Concretely, with

    p_k = <psi| P_k |psi>,     rho_k = (1/p_k) Tr_{m_k}( P_k |psi><psi| P_k )   (an n_k x n_k state),

the reduced state is the block density matrix (+)_k p_k rho_k on (+)_k C^{n_k}, and the **algebraic
entanglement entropy** is its von Neumann entropy:

    S_A(psi)  =  H({p_k})  +  Sum_k p_k S(rho_k)
              =  [classical / CENTER piece]  +  [QUANTUM piece].

This is the "generalized entanglement relative to an observable algebra" of Barnum, Knill, Ortiz and
Viola [BKOV], the algebra-relative subsystem notion of Zanardi [Z], and -- crucially -- the *discrete
cousin of the Casini-Huerta algebraic definition used for gauge fields* [CHR, D]: when the algebra of
a region in a lattice gauge theory has a nontrivial center (electric or magnetic boundary operators),
the entanglement entropy acquires exactly this H({p_k}) "classical" term -- the Shannon entropy of the
boundary-flux superselection sectors, nowadays read as the **edge-mode** contribution. The center
term computed throughout this report is the same object in an 8-dimensional toy; this is the formal
connection between Direction A and Direction B.

Two consistency limits worth recording:
* If A = B(H_A) (x) 1_B is a factor (one block, trivial center), S_A = S(rho_A): the standard
  entanglement entropy is recovered, and the center piece is zero.
* If A is abelian (all n_k = 1), S_A = H({p_k}) is purely classical.

**Pitfall (machine-cross-checked in the library).** S_A is *not* the von Neumann entropy of the
d x d matrix E_A(rho); the two differ by Sum_k p_k log2 m_k, because E_A(rho) =
(+)_k p_k rho_k (x) 1_{m_k}/m_k spreads each block uniformly over its multiplicity factor.
`alg_entanglement.algebraic_entropy` computes S_A both ways and asserts agreement to 1e-8 on every
call.

### 1.2 Why this is the right gauge-invariant functional

If a compact group G acts on H by unitaries G(g), the gauge-invariant observables are exactly the
commutant A = {G(g)}'. For any g, conjugation by G(g) fixes A pointwise, so E_A(G rho G+) = E_A(rho):
**S_A is gauge-invariant by construction** -- the quantity that was frame-dependent (single-qubit
entropy) is replaced by one that provably cannot be. This is verified numerically below to ~1e-15.

**Honest scope note.** E_A(rho) captures every statistic obtainable by *single-copy measurements of
gauge-invariant observables* -- under a charge superselection rule this is all that is operationally
accessible [cf. BRS]. The *polynomial invariant ring* of the state under G is strictly larger: it
contains multi-copy invariants (computed for the rotor vacuum in Section 5, item 4) that are
constants of the G-orbit but are not functions of E_A(rho). The well-posed reformulation below is
phrased in terms of the operational (single-copy) data; the multi-copy ring is flagged as a next
step.

**References.**
* H. Barnum, E. Knill, G. Ortiz, L. Viola, *A subsystem-independent generalization of entanglement*,
  Phys. Rev. Lett. **92**, 107902 (2004). [BKOV]
* P. Zanardi, *Virtual quantum subsystems*, Phys. Rev. Lett. **87**, 077901 (2001). [Z]
* H. Casini, M. Huerta, J. A. Rosabal, *Remarks on entanglement entropy for gauge fields*,
  Phys. Rev. D **89**, 085012 (2014) -- the algebraic definition with center term. [CHR]
* W. Donnelly, *Entanglement entropy and nonabelian gauge symmetry*, Class. Quantum Grav. **31**,
  214003 (2014) -- the lattice-gauge / edge-mode reading of the center term. [D]
* S. D. Bartlett, T. Rudolph, R. W. Spekkens, Rev. Mod. Phys. **79**, 555 (2007) -- superselection
  and reference frames (single-copy operational reading). [BRS]

---

## 2. The computed gauge-invariant algebras

**Setup (inherited).** Three JW modes f1 = sm x I x I, f2 = Z x sm x I, f3 = Z x Z x sm on C^8;
computational basis = Fock basis graded by Hamming weight; weight = 3 x electric charge on the
(nu, dbar, u, e+) ideal. A mode rotation U in U(3) induces the number-conserving unitary G(U):
trivial on weight 0, fundamental U on weight 1, Lambda^2 U on weight 2, det U on weight 3. The
construction was verified to machine precision: CAR relations exact; G unitary (2e-15); homomorphism
G(U)G(V) = G(UV) (7e-16); mode-transformation property G(U) f_b+ G(U)+ = Sum_a U_{ab} f_a+ (2e-15).

**Method.** For each gauge choice, 50 Haar samples G(U_s) were drawn (seed 20260609) and the
commutant {X : [X, G(U_s)] = 0 for all s} computed as an SVD nullspace of the stacked maps
X -> (1 (x) G - G^T (x) 1)vec(X). Each basis was certified against **100 fresh samples** (max
commutator residual < 1e-13), checked to be a unital *-algebra (closure residual < 1e-14), and its
Wedderburn structure identified from the center and per-block ranks. Nothing below relies on
paper-and-pencil representation theory; the structures are read off the numerics (and then agree
with it).

| gauged group | dim A | structure (block / multiplicity / weight support) | center | invariant data of a pure state |
|---|---|---|---|---|
| **U(3)** | **4** | M1[w0] (+) M1(x)1_3[w1] (+) M1(x)1_3[w2] (+) M1[w3] -- **abelian C^4** | C^4 | (p0, p1, p2, p3): **3 real parameters** |
| **SU(3)** | **6** | **M2**(x)1_1[w0 u w3] (+) M1(x)1_3[w1] (+) M1(x)1_3[w2] | C^3 | (p1, p2) + pure qubit in the M2 block: **4 parameters** |
| **U(1)** | **20** | M1[w0] (+) **M3**[w1] (+) **M3**[w2] (+) M1[w3] | C^4 | 3 probs + two projective pure states in C^3: **11 parameters** |

**Verdicts on the expected structures (task 2):**

* **U(3): confirmed.** The four weight sectors carry the inequivalent irreps (1, U, Lambda^2 U ~
  3bar.det, det), each with multiplicity one, so the commutant is the abelian algebra of sector
  projectors. *The only single-copy gauge-invariant data of any state is its charge-sector
  distribution (p0, p1, p2, p3).*
* **SU(3): larger than U(3), as suspected -- found exactly.** Weights 0 and 3 are both SU(3)-trivial,
  so the commutant contains a full **M2 block on span{|000>, |111>} = span{nu, e+}**: when only color
  is gauged, the nu-e+ (GHZ-type) coherence is gauge-invariant data. Weight-1 (3) and weight-2 (3bar)
  remain inequivalent, contributing C (+) C. (Machine check: the M2 central projection equals the
  projector onto indices {0, 7} to 1e-9.)
* **U(1): confirmed.** G(e^{i theta} 1) = e^{i theta N}; the commutant is everything
  weight-preserving, M1(+)M3(+)M3(+)M1 (dim 20) -- the richest of the three, retaining the full
  within-sector color states.

Parameter-count sanity check for U(1): a pure state has 14 real parameters; gauging U(1) erases
exactly the 3 relative phases between the four sectors: 14 - 3 = 11. OK.

---

## 3. Algebraic entanglement entropies (task 3)

All entropies in **bits**. For every pure state and all three algebras the **quantum piece is
identically zero** -- each Wedderburn block above has n_k = 1 or m_k = 1, so the conditional block
states of a pure state are pure. (Verified: max |quantum piece| = 1.8e-15, full machinery on a 200-state subsample; sector statistics on all 10^4.)
S_A is therefore **entirely the center (classical) term** in this toy; the table reports totals.

| state | (p0, p1, p2, p3) | S_U(3) | S_SU(3) | S_U(1) | single-qubit S (gauge-VARIANT, for contrast) |
|---|---|---|---|---|---|
| **rotor vacuum** (sqrt7 e0 - iu)/sqrt14 | **(1/2, 3/14, 3/14, 1/14)** exact | **1.724408** | **1.413800** | 1.724408 | (0.5917, 0.5917, 0.5917) |
| **W** = color-uniform dbar | (0, 1, 0, 0) | **0** | **0** | **0** | (0.9183, 0.9183, 0.9183) |
| **GHZ** = (nu + e+)/sqrt2 | (1/2, 0, 0, 1/2) | **1** | **0** | 1 | (1, 1, 1) |
| **weighted-W matching state** (exp2) | (0, 1, 0, 0) | **0** | **0** | **0** | (0.9995, 0.8580, 0.7802) |
| Haar ensemble (10^4), mean +- std | -- | 1.580 +- 0.239 | 1.398 +- 0.162 | = S_U(3) | -- |

Exact closed forms (machine-checked to 1e-12):

    rotor:  S_U(3) = S_U(1) = 1/2 + (1/2) log2(14) - (3/7) log2(3) = 1.724407817863 bits
            S_SU(3) = (4/7)(log2(7) - 2) + (3/7) log2(14/3)        = 1.413799564606 bits
            SU(3) singlet-block (nu/e+) state: probability 4/7, pure,
            rho = (1/8) [[7, i sqrt7], [-i sqrt7, 1]]   (the gauge-invariant nu-e+ coherence)

Haar means cross-checked analytically: for Haar states p ~ Dirichlet(1,3,3,1), so
E[S_U(3)] = Sum_k (a_k/8)(psi(9) - psi(a_k+1))/ln 2 = 1.5767 (sampled 1.5798); merging weights {0,3}
gives Dirichlet(2,3,3) and E[S_SU(3)] = 1.3963 (sampled 1.3981). OK.

**Gauge invariance verified (the whole point).** For every named state, every algebra, and 20 random
elements of the corresponding gauge group: max |dS_A| < 3e-15 (assertion threshold 1e-9),
while the single-qubit entropies of the *same* transformed states shift by up to **0.92 bits**.
Bonus: S_SU(3) and S_U(1) are invariant under the **full** U(3) as well (G(U) normalizes the weight
decomposition; the extra U(1) phases are isospectral on the M2 block) -- also verified to 1e-15.

### 3.1 What the table says, state by state

* **The W state's entanglement is pure gauge.** We exhibit U in SU(3) (third column (1,1,1)/sqrt3)
  with G(U)|001> = |W> exactly, and verify E_A(W) = E_A(|001>) for the U(3) algebra (residual
  1e-16). The paradox of draft Section 9.3 -- separable state mapped to "entangled" W by a color
  DFT -- is resolved, not just flagged: the algebraic entropy assigns **zero to both**, because a
  single quark in a color-rotated frame is still a single quark. The 0.918 bits of "entanglement"
  the W state carries in the qubit factorization is entirely frame.
* **GHZ is one classical bit -- or nothing.** Under U(3) (which contains the electromagnetic U(1)),
  the GHZ state's invariant content is the charge distribution (1/2, 0, 0, 1/2): exactly **1 bit of
  classical charge uncertainty**, no quantum piece. Under SU(3) only, the nu-e+ coherence sits inside
  the M2 invariant block as a *pure* qubit, and S_SU(3)(GHZ) = **0**. The "maximal tripartite
  entanglement" of GHZ is, gauge-invariantly, either one classical bit (charge superselection
  applied) or no entropy at all (color-only gauging). Nothing about it is three-partite in any
  invariant sense.
* **The weighted-W coupling-matching curve collapses.** Every point of the exp2 matching curve
  (the paper's only surviving static "match" of r_SM = 1.8174, Fig. 1c) is a weight-1 state, hence
  has p = (0,1,0,0) and **S_A = 0 for all three algebras** (verified for all stored curve points;
  max |S_A| < 1e-15). The entire curve is one U(3) gauge orbit point: gauge-equivalent to a single
  Fock state |001>. *The static coupling-matching analysis of Sections 5-6 was matching gauge
  artifacts.*
* **The rotor vacuum is the only state in the list with nontrivial invariant data**, and that data
  is two numbers (Section 4): p = (1/2, 3/14, 3/14, 1/14) with p1 = p2 exact.

### 3.2 The Direction-B connection, sharpened

For pure states in this toy the algebraic entanglement entropy is **100% center term** -- the
discrete analogue of the statement that a lattice-gauge entanglement entropy is carried entirely by
the classical boundary-flux (edge-mode) distribution. The toy realizes the Casini-Huerta-Donnelly
structure in its most extreme form: *all edge, no bulk*. Any future claim that "vacuum entanglement
encodes couplings" in this framework is therefore, gauge-invariantly, a claim about **classical
charge statistics** -- i.e., about precisely the object Direction B studies as edge modes. The two
directions are studying the same term of the same formula.

---

## 4. The well-posed question and its answer (task 4)

### 4.1 The reformulation

> **Well-posed question.** Let A be the commutant of the gauge action on the one-generation ideal.
> Does there exist a natural map from the single-copy gauge-invariant data E_A(|Omega><Omega|) of an
> algebra-selected vacuum |Omega> to the three SM couplings (alpha3, alpha2, alpha1) -- "natural"
> meaning the assignment of invariant parameters to gauge factors is dictated by the algebra, not
> chosen by hand?

This is well-posed: E_A is gauge-invariant by construction (verified to 1e-15), and "how many
independent parameters are available" is now a theorem, not a frame choice.

### 4.2 Parameter counting

| gauge choice | independent invariant parameters of a pure state | nature of the parameters |
|---|---|---|
| U(3) | **3** -- (p1, p2, p3) | charge-sector probabilities only |
| SU(3) | 4 -- (p1, p2) + pure nu/e+ qubit | charge probabilities + one singlet coherence |
| U(1) | 11 | charge probabilities + within-sector color states |

So there is *naive* room: under U(3) the invariant data has exactly 3 real parameters, one per
coupling. The question is whether any natural map exists. It does not, for four independent,
machine-verified reasons.

### 4.3 Reason 1: the sectors are charge sectors, not gauge sectors

The center of the U(3)-invariant algebra is spanned by the projectors onto eigenspaces of the
*single operator* N (electric charge Q = N/3). The four labels {0, 1/3, 2/3, 1} are values of **one
U(1) quantum number**; the SU(3) factor contributes no additional center label (weights 1 and 2 are
the 3 and 3bar, but that is rep *type*, not a continuous parameter), and there are four sectors for
three would-be couplings. A map (p1, p2, p3) -> (alpha3, alpha2, alpha1) requires a bijection
{charge sectors} -> {gauge factors} that nothing in the algebra provides: the invariant data simply
does not factorize along gauge factors. This is the precise, gauge-invariant version of the paper's
"index ambiguity" (draft Section 2.3) -- and it is now a structural fact rather than a labeling
worry.

### 4.4 Reason 2: the algebra-canonical vacuum has only two parameters

The rotor vacuum's invariant data is exactly

    p = (1/2, 3/14, 3/14, 1/14),    with  p1 = p2  EXACTLY  (machine: |p1 - p2| < 1e-16),

because the vacuum has uniform |amplitude|^2 = 1/14 on all seven imaginary units, forcing p_k
proportional to the sector dimension on weights 1-3. The canonical vacuum therefore carries **2
independent invariant parameters, fewer than 3 couplings**. The permutation degeneracy that killed
every hierarchical reading in the frame-dependent analysis (draft Sections 6.2, 8) *survives
gauge-invariantization* as an exact sector degeneracy. The obstruction was never the frame; it is
the algebra's symmetry.

### 4.5 Reason 3: no assignment reproduces the coupling hierarchy anyway

We tested every ordered assignment of three distinct charge sectors to the three couplings (24 per
feature map) under three feature maps (p_k, log2 p_k, -p_k log2 p_k), against the inherited
two-parameter affine ansatz, i.e. demanding the gap ratio r = (x_a - x_b)/(x_b - x_c) equal
r_SM = 1.8174 (draft Eq. 2). Result (60 non-degenerate assignments of 72 enumerated; 12 degenerate excluded — see results.json): **none lands within the paper's
widened tolerance 0.05**; the best miss is r = 2 exactly (feature p, sectors (0, 1, 3) or (0, 2, 3)
descending), at distance **0.183** -- and the assignments achieving it must, absurdly, assign the
*neutrino* sector and the *positron* sector to two different gauge couplings while skipping one of
the two (exactly degenerate) quark sectors. Assignments using both quark sectors give r in
{0, -1, +-inf} -- degenerate by p1 = p2. (The amusing near-miss r = 2 vs 1.817 is a 10% coincidence
of small fractions, reachable only through an unprincipled sector choice; we flag it so nobody
rediscovers it as a "signal.")

### 4.6 Reason 4: SU(2)_L is not in the toy at all

The mode-rotation (number-conserving Bogoliubov) gauge group of three JW modes is exactly
U(3) ~ (SU(3)_c x U(1))/Z3 -- there is no room for an independent SU(2) acting on color modes. More
physically, the ideal (nu, dbar_i, u_i, e+) contains **no weak-isospin doublet pair**: nu_L pairs
with e-_L (absent -- the ideal contains e+), u_L with d_L (absent -- the ideal contains dbar). Weak
raising/lowering operators would map this ideal into a *different* ideal; in Furey's full
construction SU(2)_L acts on the quaternionic factor of C (x) H (x) O -- between ideals, never
within one. And the toy's abelian charge is **electromagnetic Q = N/3, not hypercharge**.
Consequently *the three-coupling question cannot even be posed gauge-covariantly on a single
generation ideal*: at most two gauge factors (SU(3)_c, U(1)_em) act, and their invariant data is the
charge distribution.

### 4.7 More constrained or less? The verdict

The ill-posed version was *underconstrained*: a 14-real-parameter state space, a
guaranteed-nonempty one-parameter matching manifold, statistically generic matches, W-class
realizations (draft Sections 5.3, 6.1-6.2). The well-posed version is **drastically more
constrained**:

* the invariant state space shrinks from 14 parameters to 3 (U(3));
* the entire weighted-W matching mechanism is annihilated (S_A = 0 on the whole curve -- the
  previous "match" was frame decoration on a single quark);
* the algebra-selected vacuum's data is fixed and degenerate (2 parameters, p1 = p2);
* no natural sector->factor map exists, and the exhaustive unnatural ones miss r_SM;
* one of the three couplings has no corresponding symmetry in the toy at all.

> **Answer to the re-posed question: NO -- and now provably, not just diagnostically.** The
> gauge-invariant entanglement data of a single pure state in this toy is its electric-charge
> statistics. Charge statistics has no natural three-fold structure aligned with the three gauge
> factors; the canonical vacuum's statistics are two-parameter degenerate; and SU(2)_L is absent
> from the construction. The coupling hierarchy is not, and cannot be, encoded in the
> gauge-invariant entanglement of a single pure state of this toy.

This is the strongest form of the paper's conclusion available at this level: the well-posedness
program (draft Sections 9.3, 11.2) was completed for the toy, and the completed version *closes* the
static question rather than reopening it. What it leaves open is exactly what it quantifies: richer
state spaces (more ideals), richer data (multi-copy invariants), and flow (mu-dependence of p_k).

---

## 5. Surprises and additional exact results

1. **S_U(1) = S_U(3) for every pure state** (both equal H of the charge distribution), even though
   the U(1)-invariant algebra is 5x larger. Gauging the extra SU(3) changes *which states are
   distinguishable* (the U(1) data distinguishes W from |001>; the U(3) data does not) but not the
   entropy. Entropy is a very lossy summary of E_A.
2. **All gauge-invariant entanglement in this toy is classical.** Quantum piece = 0 for all pure
   states, all three algebras (every block has n_k = 1 or m_k = 1). The first system in this program
   where a *nonzero quantum piece* could appear needs either mixed states, or an algebra whose
   blocks have both n_k, m_k > 1 (e.g., regional subalgebras -- Direction B).
3. **SU(3)-only gauging leaves the nu-e+ coherence physical.** The M2 invariant block means the
   GHZ-type coherence is gauge-invariant data if (and only if) the abelian factor is not gauged --
   the toy cleanly separates "color confinement of entanglement" from "charge superselection."
   For the rotor vacuum that invariant qubit is rho = (1/8)[[7, i sqrt7],[-i sqrt7, 1]] with
   block probability 4/7.
4. **Beyond-E_A invariants are nonzero and exactly computable for the rotor vacuum**: the
   cross-sector invariant |v1 ^ v2| = **1/14** exactly (v1, v2 the weight-1 and weight-2 mode
   vectors), |conj(v3)(v1^v2)| = 14^{-3/2} ~ 0.01909, |conj(v0) v3 conj(v1^v2)| = sqrt7/196 ~
   0.01350 -- all verified gauge-invariant to 1e-15. The single-copy no-go of Section 4 does not
   automatically extend to the full invariant ring; it does extend to anything measurable under the
   superselection rule.
5. The rotor vacuum's invariant entropy 1.724 bits is comfortably *generic* (Haar mean 1.580 +-
   0.239): gauge-invariantly, the canonical vacuum is not even unusually entangled.

---

## 6. Next steps (concrete)

1. **Two-ideal extension (the SU(2)_L fix).** Build the 16-dimensional two-ideal space (or the full
   Cl(6) Fock space C^64 with Furey's left/right ideal pair), implement SU(2)_L as the ideal-mixing
   quaternionic action, and recompute the commutant of the full S(U(3)xU(2))-type action with the
   same machinery. Question: does the center acquire a natural *threefold* structure aligned with
   gauge factors, or does the no-go of Section 4.3 persist? This is the single most direct
   continuation.
2. **Regional algebras / edge modes (Direction B bridge).** Repeat the computation for *subsets of
   modes* (e.g., the algebra generated by gauge-invariant operators built on modes {1, 2} only),
   where blocks with n_k, m_k > 1 -- hence a nonzero quantum piece -- first appear. Compare the
   center term with the lattice-gauge edge-mode term of [CHR, D] explicitly.
3. **Characterize the full U(3) invariant ring on C^8** (the multi-copy invariants of Section 5,
   item 4): count independent generators numerically (rank of the Jacobian of the invariants at
   generic points), determine what they add beyond (p0..p3), and decide whether any physical reading
   exists given that single-copy superselected measurements cannot access them.
4. **Flow version with invariant data.** Replace the entropy triple of draft Section 7 by the sector
   distribution p_k(mu): determine whether any RG-consistent affine flow on the 3-simplex, with the
   rotor vacuum's (1/2, 3/14, 3/14, 1/14) as boundary data, can reproduce one-loop running -- or
   prove the analogous no-go (expected, by Section 4.3: the simplex flow has no natural
   three-coupling structure either).
5. **Gauge-fixed factorization alternative.** The paper's other escape route (draft Section 9.3) was
   an algebraic gauge-fixing of the tensor-product structure. Classify U(3)-orbits of JW-compatible
   factorizations and test whether any algebra-selected gauge fixing yields a hierarchical entropy
   triple for the rotor vacuum. (Expected answer: no -- in its own canonical frame the rotor vacuum
   is exactly symmetric, (0.5917)^3 -- but the classification would make that a theorem.)

---

## 7. Files and reproduction

* `alg_entanglement.py` -- library: numerical commutant, Wedderburn structure identification,
  conditional expectation, algebraic entropy (center + quantum, with built-in cross-check),
  JW modes, G(U) construction, Haar samplers.
* `run_direction_A.py` -- all computations above; fixed seed 20260609; every claim asserted at
  runtime (the script *fails* if any verification breaks); writes `results.json`.
* `results.json` -- raw outputs: verification residuals, commutant structures, per-state entropies
  and exact fractions, gauge-invariance maxima, Haar statistics with analytic cross-checks, the
  r-matching zoo, the weighted-W collapse, the SU(2)_L obstruction, and the verdict.

Run: `python run_direction_A.py` (~6 s; numpy + scipy only; reads
`../experiments/results/exp2_results.json` for the weighted-W matching amplitudes).
