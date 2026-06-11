# The Two-Ideal / Chiral Extension: Gauge-Invariant Structure of the One-Generation Standard-Model Fock Space

**Status (2026-06-10): computed, machine-verified, deterministic (seed 20260610).**
This report executes the seven tasks of the reviewer's "two-ideal extension" program
(new_review.txt, items 1-7): build the smallest honest arena on which the full
SU(3)_c x SU(2)_L x U(1)_Y acts, compute its gauge-invariant structure with the
direction_A commutant machinery (extended to 32768 dimensions by sector-by-sector
Schur analysis), and answer the three-parameter question. Every analytic
multiplicity claim is machine-verified by at least two independent methods; every
script asserts its own claims at runtime and fails loudly.

**Headline results.**

1. **The arena hosts the full SM gauge group** - the obstruction that closed Paper 2
   (SU(2)_L unrepresentable, abelian charge = Q_em not hypercharge) is lifted. The
   gauge action is anomaly-free in all five sums, and its faithful global form is
   detected by the computation itself: every one of the 250 sectors satisfies the
   Z6 congruence `y = 4(a-b) + 3(2j) mod 6`, i.e. the center labels live on the
   weight lattice of **(SU(3) x SU(2) x U(1))/Z6 - the true SM gauge group**.
2. **Commutant:** A' = (+)_{i=1}^{250} M_{m_i}, **dim A' = 57062**, center = C^250.
   Max multiplicity m = 52 (the (3,2)_{1/6} and (3bar,2)_{-1/6} sectors). 190 of
   250 sectors have m >= 2; 185 sectors have both n_i > 1 and m_i > 1, covering
   **94.8% of the Fock space** - the quantum (bulk) piece of the algebraic entropy
   is now *generically nonzero*. Paper 2's "all edge, no bulk" is a one-ideal
   artifact and dies here (computed: Haar states on the Q+L arena carry
   0.200 +- 0.024 bits of pure quantum gauge-invariant entropy).
3. **Center labels are full gauge-representation labels** (a,b; 2j; y) - all three
   factors, not one abelian charge. They are *not* chirality, *not* B, *not* L,
   *not* B-L: all of these vary inside single sectors, i.e. they are
   multiplicity-space (commutant) directions, **not superselected** by gauge
   kinematics. The 28-dimensional invariant-vector sector is a catalog of
   would-be 't Hooft vertices (udd, QLud, uude, ..., the filled sea), and the
   commutant contains explicit gauge-invariant B- and L-violating operators such
   as |vac><udd|.
4. **The one-generation QQQL 't Hooft vertex is kinematically absent**: the singlet
   count at species content (n_Q, n_L) = (3,1) is exactly **0** (Fermi statistics
   kills the color-singlet isosinglet combination when all three Q's are the same
   generation) - machine-verified.
5. **Three-parameter question: a sharp partial YES, honestly bounded.** The three
   Casimir-moment functionals F3 = <C2(su3)>, F2 = <C2(su2)>, F1 = <Y^2> are
   functionals of the invariant center data, are algebra-aligned with the three
   gauge factors, and are **independently variable** (Jacobian of (F3,F2,F1) over
   the 5-parameter product-state family has rank 3 with singular values
   3.35, 1.75, 0.70; explicit single-factor directions exhibited). This is the
   first arena in the program where the three-coupling question is *posable* and
   the invariant data has *room* for it. But: the "three" is input, not output
   (Sec. 6); nothing in the algebra selects coupling *values*; and the sector
   lattice is strongly correlated across factors (I(su3;Y) = 1.61 bits), not a
   product of three independent label sets.

---

## 1. Setup: the Hilbert space (task 1)

### 1.1 Definition

V = one generation of SM Weyl modes, 15 fermionic modes:

| species | rep | modes | y = 6Y | mode indices |
|---|---|---|---|---|
| Q | (3, 2)_{1/6} | 6 | +1 | 0-5 (color c, isospin s; index 2c+s) |
| L | (1, 2)_{-1/2} | 2 | -3 | 6-7 |
| u_R | (3, 1)_{2/3} | 3 | +4 | 8-10 |
| d_R | (3, 1)_{-1/3} | 3 | -2 | 11-13 |
| e_R | (1, 1)_{-1} | 1 | -6 | 14 |

Hilbert space: the fermionic Fock space F = Lambda^*(V), dim 2^15 = 32768, graded
by the five species numbers and the gauge weights. No nu_R (15 modes, not 16); the
corollary for 16 modes is exact and trivial: Lambda^*(V + (1,1)_0) =
Lambda^*(V) (x) C^2 with trivial G-action on C^2 - every multiplicity doubles,
the sector list is unchanged, and nothing below changes qualitatively.

### 1.2 Deviation from Furey's literal two-ideal construction, and why

Furey realizes one generation on a pair of minimal left ideals of
C (x) O = M_8(C), with SU(3)_c x U(1)_em acting within ideals and SU(2)_L (in the
C (x) H (x) O extension) acting on the quaternionic factor *between* chiral
ideals. We do **not** reproduce the division-algebra scaffolding. We build the
*representation-theoretically faithful minimal carrier*: a fermionic Fock space
over exactly the SM gauge representation content of one generation, with both the
doublet ("left ideal") and singlet ("right ideal") sectors present. Reasons:

1. The commutant/center computation depends only on the unitary G-module structure
   of the Hilbert space, not on which algebra it is an ideal of. Any construction
   carrying the same rep content (including Furey's) has the same commutant table.
2. **Convention-independence lemma (machine-verified):** the alternative
   convention with right-handed singlets conjugated to left-handed antiparticle
   modes (u^c = (3bar,1)_{-2/3}, d^c = (3bar,1)_{+1/3}, e^c = (1,1)_{+1}) yields a
   G-isomorphic Fock space: Lambda^k(W*) = Lambda^{n-k}(W) (x) (det W)*, and the
   det-twists cancel across u,d,e precisely because the singlet-sector
   hypercharges sum to zero. Verified as a character identity at 50 random torus
   elements, max deviation 3.1e-12 (`rep_checks.json`). The "particle modes vs
   two conjugate ideals" choice is immaterial.
3. What Paper 2's Lemma 4 actually required was an arena containing the chiral
   doublet pairs (nu_L with e_L, u_L with d_L) and a hypercharge (not Q_em)
   abelian action. This arena contains both; SU(2)_L acts within Q and within L,
   exactly where the one-ideal toy had no room for it.

The "two-ideal" content of the name survives as the doublet/singlet (left/right
ideal) split of the mode set, which is also precisely the chirality grading.

### 1.3 Anomaly bookkeeping (task 2)

With chirality sign chi (+1 for Q, L; -1 for u_R, d_R, e_R), all machine-checked
exactly (Fractions, `rep_checks.json`):

    [SU(3)]^2 U(1):  sum over colored modes of chi*Y          = 0
    [SU(2)]^2 U(1):  sum over doublet modes of chi*Y          = 0
    [grav]^2 U(1):   sum chi*Y                                = 0
    [U(1)]^3:        sum chi*Y^3                              = 0
    Witten:          # SU(2) doublets = 4 (even)              OK
    sum_modes Y (unsigned) = 0   <=>  the filled state is a gauge singlet.

The last line is a structural echo: the *fully filled Fock state is
gauge-invariant iff the unsigned hypercharge sum vanishes* - which for this
matter content it does. Anomaly-free matter content is what makes the "Dirac
sea" a singlet and (Sec. 4) puts it in the same superselection sector as the
vacuum.

### 1.4 The gauge action

G = SU(3) x SU(2) x U(1) acts by mode unitaries U(g) = block-diag over species
(U3 (x) U2 e^{i theta/6} on Q, U2 e^{-i theta/2} on L, U3 e^{2i theta/3} on u, ...),
second-quantized to Gamma(g) = (x)_species Lambda^*(U_s) - a plain tensor product,
sign-safe because all blocks are even operators. Machine checks
(`results_full.json`): Lie-algebra closure residual 8.7e-17, homomorphism
Gamma(g1)Gamma(g2) = Gamma(g1g2) to 4.6e-15, generator consistency
d/d eps Gamma(e^{i eps T}) = i F_T to 4.5e-07 (finite difference, eps = 1e-6).
The kernel of the action is the SM Z6, as the sector congruence confirms.

---

## 2. Method: sector-by-sector Schur, with five independent verifications

Dense 32768^2 SVD commutant methods are impossible here; we computed the
commutant *analytically via Schur* and verified it numerically *blockwise*:

* **(M1) Exact highest-weight peeling** (`run_rep.py`): the 32768 basis weights
  (p,q,t,y) are peeled against Freudenthal weight diagrams (exact integer
  arithmetic; the peeling terminating with the multiset exactly exhausted is
  itself a proof, given the weight diagrams). Output: the 250-row table
  m_i, (a,b,2j,y)_i in `decomposition_full.json`.
* **(M2) Character identity**: sum_i m_i chi_i(g) == det(1 + U(g)) at 20 random
  torus elements, with chi_i from Weyl/Schur bialternant formulas (independent of
  Freudenthal). Max error 2.6e-12.
* **(M3) Exact Weyl-integration quadrature** on a 32x32x32x128 torus grid (DFT
  exactness: all integrands are Laurent polynomials of degree < grid size):
  <chi_F, chi_F> = sum m_i^2 = 57062 and <1, chi_F> = 28 reproduce the peeling
  exactly.
* **(M4) Full Fock-space Casimir spectroscopy** (`run_full.py` + `fock.py`): the
  problem block-diagonalizes over 12916 keys (n_Q,n_L,n_u,n_d,n_e,p,q,t), max
  block size 30. In every block the matrices of C2(su3), C2(su2) (and, where su3
  conjugate pairs collide, the cubic Casimir C3 = d_ABC F_A F_B F_C) are
  assembled exactly from species-local operators and diagonalized; every
  eigenvalue cluster is matched to an irrep; the aggregated counts reproduce
  **every m_i x (weight multiplicity) for all 250 sectors and all weights**
  (asserted, not sampled). The C3 term-list assembly is itself verified against
  a brute-force dense construction (residual 2.2e-15) and [C3, su3] = 0
  (4.4e-16).
* **(M5) direction_A pipeline cross-check** (`run_crosscheck.py`): on the 64-dim
  Q-only arena the structure-agnostic commutant (memory-light eigencluster
  variant of the SVD nullspace; certified on 60 fresh Haar samples, residual
  4.3e-14; *-algebra closure 7.2e-15) finds exactly the predicted **abelian
  C^10** with block dimensions [1,1,4,6,6,6,6,9,9,16] - matching the analytic
  table block for block. On the 256-dim Q+L arena the full Wedderburn
  decomposition (including aligned multiplicity bases built by canonical
  lowering words, global orthonormality 8.9e-16) realizes every M_{m_i}
  explicitly.

Gauge invariance of all reported invariant data was verified directly:
max |dp_i| over random gauge transformations = 2.9e-15 (full space),
and on Q+L the full data (p_i, multiplicity-state spectra, S) shifts by < 5e-15.

---

## 3. The commutant and center (tasks 3-4)

### 3.1 Full 15-mode arena (the headline table)

| quantity | value |
|---|---|
| # sectors (center dim) | **250** |
| dim commutant sum m_i^2 | **57062** |
| sum m_i n_i | 32768 (= dim F, check) |
| max multiplicity | **52**, at (3,2)_{1/6} and (3bar,2)_{-1/6} |
| sectors with m_i = 1 | 60 |
| sectors with m_i >= 2 | 190 |
| sectors with n_i > 1 AND m_i > 1 | **185**, carrying 94.8% of dim F |
| invariant vectors (singlet multiplicity) | **28** |
| y-range of sectors | -18 ... +18 (all 37 values) |
| distinct su3 labels / su2 labels | 15 / 5 (2j = 0..4) |
| realized label triples vs product set | **250 of 15 x 5 x 37 = 2775** |

Largest sectors by multiplicity: (3bar,2)_{-1/6} and (3,2)_{1/6} (m=52, n=6);
(8,2)_{+1/2} and (8,2)_{-1/2} (m=50, n=16); (8,1)_0 (m=42, n=8); full table in
`decomposition_full.json`.

Contrast with Paper 2's one-ideal table (U(3): abelian C^4, center = charge
sectors): the commutant is now massively nonabelian, and for the first time in
this program the generic pure state has a **nonzero quantum piece** - the
algebraic entropy is no longer purely the classical center term. Computed on the
Q+L arena (where the full machinery runs exactly): Haar states have
S_center = 4.526 +- 0.056 bits and S_quantum = 0.200 +- 0.024 bits (minimum over
300 samples 0.128: *generically* nonzero, never zero in the ensemble). "All edge,
no bulk" was a one-ideal accident.

### 3.2 Q-only and Q+L sub-arenas (cross-check arenas)

* **Q only (64-dim):** 10 sectors, all m = 1 - commutant **abelian C^10**
  (skew duality: Lambda^k(C3 (x) C2) is multiplicity-free). Verified numerically
  end-to-end with the direction_A pipeline.
* **Q+L (256-dim):** 31 sectors, dim A' = 46, five sectors with m = 2:
  (1,1)_0 [vacuum + filled], (3,2)_{1/6}, (3bar,2)_{-1/6}, (3,3)_{-1/3},
  (3bar,3)_{+1/3}. The (3,2)_{1/6} M_2 block mixes a single quark (k=1) with a
  QQQQL composite (k=5): a Delta B = 1, Delta L = 1, Delta(B-L) = 0 coherence
  that is fully gauge-invariant data.

---

## 4. What the center labels ARE (task 5)

**The center labels are complete gauge-representation labels (a, b; 2j; y) - and
nothing else.** Concretely:

1. **All three gauge factors appear in the labels**, including the full su3 rep
   type (a,b) (not merely triality) and the full isospin j (not merely a charge).
   This is the qualitative upgrade from Paper 2, where the center was the level
   set of one abelian operator (electric charge). The sector lattice is
   4-integer-valued - note: **rank of G (2+1+1), not number of factors (3)**.
2. **The labels detect the global group.** All 250 sectors satisfy
   y = 4(a-b) + 3(2j) mod 6 with zero violations: the realized lattice is the
   weight lattice of (SU(3) x SU(2) x U(1))/Z6. The kinematics knows the SM's
   global structure.
3. **The labels are NOT a product set**: 250 realized of 2775 possible triples;
   under the Haar (dimension-weighted) measure the label mutual informations are
   I(su3; Y) = 1.609 bits, I(su2; Y) = 1.002 bits, I(su3; su2) = 0.073 bits.
   The three "channels" are kinematically correlated, partly (not only) by the
   Z6 congruence.
4. **Chirality is not a center label**: e.g. the singlet sector contains both the
   vacuum (chirality content 0) and udd (pure right-handed content). Chirality
   data lives in the multiplicity spaces.
5. **B, L, B-L are not center labels** - they are commutant operators that are
   *not central*. The singlet sector alone carries B-L in {-2,...,+3}
   (machine-verified spread). Consequence, stated sharply: **gauge kinematics
   does not superselect baryon or lepton number**; |vac><udd| is a gauge-invariant
   operator (a "neutron annihilation vertex"), and the vacuum-filled coherence
   (Delta B = 4, Delta L = 3 in this 15-mode counting) is invariant data. In the
   SM, B and L conservation is accidental/dynamical; the toy renders that
   textbook statement as a computed algebraic fact: the would-be vertices sit
   inside the gauge-invariant algebra from the start.

### 4.1 Singlet spectroscopy: the 't Hooft-vertex catalog

The 28 invariant vectors resolve into **28 distinct species-number sectors, each
with multiplicity exactly 1** (a multiplicity-free catalog; full list in
`results_full.json`). Highlights (B, L per entry):

| content | k | B | L | reading |
|---|---|---|---|---|
| vacuum | 0 | 0 | 0 | - |
| u d d | 3 | 1 | 0 | the neutron-content singlet |
| Q L u d | 4 | 1 | 1 | mixed-chirality B+L vertex |
| u u d e | 4 | 1 | 1 | "hydrogen-like" all-RH singlet |
| L L u u d | 5 | 1 | 2 | - |
| u u u d d d e | 7 | 2 | 1 | - |
| Q^6 d^3 | 9 | 3 | 0 | color-saturated tri-baryon |
| filled (Q^6 L^2 u^3 d^3 e) | 15 | 4 | 3 | the anomaly-free Dirac sea |
| ... 28 total, closed under complement (k <-> 15-k) | | | |

**The QQQL singlet is absent** ((n_Q, n_L, n_u, n_d, n_e) = (3,1,0,0,0) count = 0,
asserted): with a single generation, epsilon-color antisymmetry forces the QQQ
isospin to 3/2, which cannot couple with one L to an SU(2) singlet - the famous
fact that the 't Hooft vertex needs flavor structure, here falling out of the
commutant computation as a zero.

---

## 5. Algebraic entropy and invariant data of algebra-selected states (task 6)

Algebra: the gauge-invariant algebra A' = commutant; S_{A'} = H({p_i}) +
sum_i p_i S(rho_i^mult) (BKOV / Casini-Huerta, as in direction_A). Center data on
the full space; complete data including quantum piece on Q+L (256-dim), where the
aligned-basis machinery is exact. All entries in bits.

**Full 15-mode arena:**

| state | S_center | sectors occupied | (F3, F2, F1) | notes |
|---|---|---|---|---|
| Fock vacuum | 0 | 1 (singlet) | (0, 0, 0) | S_total = 0 |
| filled sea | 0 | 1 (singlet) | (0, 0, 0) | S_total = 0; same sector as vacuum |
| (vac + filled)/sqrt2 | 0 | 1 | (0, 0, 0) | S = 0 but nontrivial invariant data: off-diagonal of the M_28 singlet block; the Delta(B+L) coherence is gauge-invariant |
| uniform product (rotor-vacuum analog) | 7.1643 | 250 | (31/8, 9/4, 5/6) | occupies every sector |
| generic product (theta = .7,.9,1.1,.5,1.3) | 6.4576 | 250 | (3.160, 2.147, 0.556) | Jacobian base point |
| Haar (200 samples) | 7.183 +- 0.007 | 250 | (4.000, 1.499, 0.834) ~ exact (4, 3/2, 5/6) | mean p_i matches m_i n_i / 32768 to 9.3e-5 |

**Q+L arena (full algebraic entropy, quantum piece exact):**

| state | center | quantum | total | notes |
|---|---|---|---|---|
| vacuum / filled / (vac+filled)/sqrt2 | 0 | 0 | 0 | invariant coherence, zero entropy |
| (vac + quark)/sqrt2 | 1 | 0 | 1 | one classical sector bit |
| engineered M2 state | 0 | **1** | 1 | **pure quantum gauge-invariant entropy** - first nonzero quantum piece in this program; p = 1 on (3,2)_{1/6}, rho_mult = I/2; MC-twirl cross-check 0.9981 vs 1.0000 |
| uniform product | 4.2799 | 0.1722 | 4.4521 | the rotor analog has a quantum piece too |
| Haar (300) | 4.526 +- 0.056 | 0.200 +- 0.024 | - | quantum piece generic (min 0.128) |

**Particle-hole structure (the fate of Paper 2's p1 = p2).** The exact theorem
that survives is a *covariance*, not a degeneracy of the symmetric state:
p_i(psi) = p_{ibar}(K psi) for the signed (fermionic) complement map K, verified
to 7.6e-17. But the uniform product state is **not** K-invariant (K introduces
Fermi signs), so the inherited degeneracy is only partial: of 121 conjugate
sector pairs, **54 are exactly degenerate** and 67 are split (max gap 7.6e-3);
the state carries 134 distinct p-values across 250 sectors. Moreover the uniform
state is *not* the Haar-mean distribution (max |p_i - m_i n_i / 2^15| = 0.0115) -
the Paper-2 mechanism "uniform amplitudes => p proportional to sector dimension"
also fails here, because sectors are no longer single weight-classes. The
algebra-canonical symmetric state has more invariant structure in this arena,
not less.

---

## 6. The three-parameter test (task 7)

**Test as specified:** can three independent functionals of the invariant data be
varied independently by choice of state, in a way that tracks the three factors?

**Construction.** F3 = <C2(su3)>, F2 = <C2(su2)>, F1 = <Y^2>. These are exact
linear functionals of the center distribution {p_i} (each sector has sharp
Casimir values) - hence functionals of the single-copy gauge-invariant data -
and each is built from exactly one gauge factor's quadratic Casimir: the
factor alignment is algebra-dictated, not hand-chosen. (Cross-check: p-weighted
sector sums equal direct operator expectations to < 1e-8.)

**Result: YES on representability and independence.**
On the natural 5-parameter family of algebra-compatible product states
(one filling angle per species), the Jacobian d(F3,F2,F1)/d(theta_Q..theta_e) at
a generic point has **rank 3** (singular values 3.35, 1.75, 0.70), and explicit
single-factor directions exist: state deformations moving F3 alone (a u-vs-d
filling tradeoff, dtheta ~ (-.02,-.05,-.23,+.20,-.08)), F2 alone, F1 alone (all
achieved dF verified to 1e-6). The structure of the Jacobian is itself readable:
theta_L moves only (F2, F1); theta_u, theta_d move only (F3, F1); theta_e moves
only F1; theta_Q moves all three - exactly the SM charge table at work.

Both Paper-2 obstructions are confirmed lifted: the center is no longer the level
set of one abelian charge (Sec. 4), and SU(2)_L now acts with its Casimir
functional independently tunable.

**The honest negatives - why this is not "three couplings emerge":**

1. **The "three" is an input, not an output.** The natural grading of the center
   is the 4-integer gauge-irrep lattice (rank of G), and the invariant data of a
   generic state is ~249 sector probabilities plus multiplicity-block states (a
   dim-57062 algebra), not three numbers. Three appears exactly when one decides
   to summarize each gauge factor by its quadratic Casimir moment - a canonical
   *choice*, available in any theory carrying any G; it reflects the fact that we
   put SU(3) x SU(2) x U(1) in by hand. The arena finally *permits* a
   three-parameter reading; it does not *produce* one.
2. **No algebra-selected state carries three distinguished numbers.** The
   algebra-canonical states (vacuum, filled, their coherences) sit in the singlet
   sector with S = 0 and (F3,F2,F1) = (0,0,0). The symmetric (uniform) state has
   fixed values (31/8, 9/4, 5/6) with zero free parameters; the Haar ensemble
   concentrates at the trace values (4, 3/2, 5/6) with std 0.007 bits in entropy.
   Nothing selects a *point* in (F3,F2,F1)-space that could encode (g3,g2,g1);
   the map states -> (F3,F2,F1) is hugely many-to-one and there is no
   algebra-dictated section. Couplings would have to come from dynamics
   (a Hamiltonian, a flow) - exactly the conclusion of the YM2 companion line:
   reflection requires a dynamical family; kinematics supplies only the room.
3. **The three channels are kinematically entangled.** The sector lattice is not
   a product (250 of 2775 triples; I(su3;Y) = 1.61 bits under the Haar measure;
   the Z6 congruence is an exact functional dependence mod 6). Any "per-factor"
   statistic inherits cross-factor correlations from the matter content. This is
   the structural descendant of Paper 2's "no natural bijection sectors <->
   factors": the bijection now exists at the level of *Casimir functionals*, but
   the underlying sector random variable does not factorize.
4. **Degeneracies still haunt the canonical symmetric state** (54 exact conjugate
   degeneracies of 121 pairs), though - new here - they are now *partial* and
   traceable to a theorem (particle-hole covariance + the state's partial
   K-symmetry), and the u/d hypercharge asymmetry visibly breaks the rest.

**Verdict.** The two-ideal extension converts Paper 2's "the question is not
posable" into "the question is posable and the kinematic answer is: three
independent, algebra-aligned, independently-tunable functionals exist - and that
is *all* that exists." There is room for three couplings; there is no mechanism,
preferred state, or extra structure that would *determine* them. If a
three-coupling structure is ever to emerge in this program rather than be
imposed, it must come from dynamics on this arena (a gauge-invariant Hamiltonian
flow deforming {p_i}), not from the kinematic invariant data of any single state.

---

## 7. Findings (numbered)

1. **(Posability restored.)** The full SU(3)_c x SU(2)_L x U(1)_Y acts faithfully
   (mod the SM Z6) on the 15-mode one-generation Fock space; all five anomaly
   sums vanish; SU(2)_L acts within the doublet species. Lemma 4 of Paper 2 is an
   artifact of the one-ideal truncation, as that paper predicted.
2. **(Commutant.)** A' = (+) M_{m_i} over 250 sectors, dim 57062, center C^250,
   max m = 52. Verified by exact peeling + characters + Weyl quadrature + full
   blockwise Casimir spectroscopy + (on sub-arenas) the direction_A SVD pipeline.
3. **(Center labels.)** Full gauge-irrep labels (a,b;2j;y) on the Z6-constrained
   lattice of the true SM group; 4-integer-valued (rank, not #factors);
   non-product (MI up to 1.61 bits).
4. **(Not labels.)** Chirality, B, L, B-L all vary within sectors: gauge
   kinematics does not superselect them. The gauge-invariant algebra contains
   explicit B/L-violating operators; B/L conservation must be dynamical.
5. **('t Hooft catalog.)** 28 invariant vectors, multiplicity-free across 28
   species-number sectors, closed under complement; QQQL absent by Fermi
   statistics (count = 0, machine-verified); udd, QLud, uude present.
6. **(Bulk exists now.)** 185 sectors with n,m > 1 (94.8% of dim F); generic
   states carry a nonzero quantum piece (Q+L: 0.200 +- 0.024 bits; engineered
   state: exactly 1 bit of pure quantum gauge-invariant entropy, MC-twirl
   confirmed). Paper 2's "all edge, no bulk" does not survive the extension.
7. **(Canonical states are invariantly trivial.)** Vacuum, filled sea, and their
   coherences: S = 0, all functionals 0, single sector. The filled sea is a
   singlet *because* the matter content is anomaly-free (sum Y = 0).
8. **(Particle-hole.)** Exact covariance p_i(psi) = p_ibar(K psi); the uniform
   state retains only 54/121 conjugate degeneracies (max split 7.6e-3) and is
   not the Haar mean (gap 1.2e-2): Paper 2's exact p1 = p2 rigidity survives
   only as a partial, theorem-controlled remnant.
9. **(Three-parameter question.)** Posable: yes. Three algebra-aligned
   functionals independently variable: yes (rank-3 Jacobian, single-factor
   directions). Emergent three-coupling structure: **no** - the three-ness is
   the input group's factor count; no state, sector statistic, or algebraic
   datum singles out coupling values; the label lattice does not factorize.

**Single most surprising finding** (in the report's judgment): findings 4/5 - the
center of the gauge-invariant algebra washes out exactly the quantum numbers
(B, L, chirality) that organize the physics, while gauge-invariant B- and
L-violating coherences (vacuum <-> udd "neutron", quark <-> QQQQL) are present in
the kinematic invariant data from the start, and the one-generation QQQL vertex
is killed not by gauge theory but by Fermi statistics. The superselection
structure of the SM's kinematics is *purely* gauge-representation-theoretic;
everything else the SM conserves, it conserves for dynamical reasons.

---

## 8. Honest assessment and limitations

* The arena is kinematic: no Hamiltonian, no scale, no flow. Every statement
  about couplings is therefore about *room*, never about *values*. The positive
  result (rank-3 tunability) is exactly as strong as it sounds and no stronger.
* The quantum-piece computations with full multiplicity-state machinery were
  performed exactly on the 256-dim Q+L arena; on the full 32768-dim space we
  computed exact center data for all states and exact total entropies for states
  confined to n=1 or m=1 blocks (vacuum, filled, coherences). Building aligned
  multiplicity bases for all 250 sectors of the full space is implementable with
  the same lowering-word code but was not needed for any conclusion above.
* The Haar ensembles use 200 (full) / 300 (Q+L) samples; means match exact trace
  identities to ~1e-4, and no conclusion rests on ensemble tails.
* The product-state family is a natural but specific 5-parameter slice; rank 3 on
  a slice proves independence globally (it is a lower bound on attainable rank),
  but the *non*-existence claims (no preferred point) are structural arguments,
  not exhaustive searches over state space.
* We did not reproduce Furey's division-algebra construction literally; Sec. 1.2
  argues (and machine-checks the conjugation lemma) that the commutant
  conclusions are construction-independent. If one insists on the C (x) H (x) O
  scaffolding, the rep content is the same and the table transfers verbatim.

## 9. Files and reproduction

All deterministic, seed 20260610; pure numpy (no scipy). Run order:

    python3 run_rep.py          # ~1 s   decomposition_{full,Q,QL}.json, rep_checks.json
    python3 run_full.py         # ~15 s  results_full.json
    python3 run_crosscheck.py   # ~5 s   results_crosscheck.json

* `su3.py` - exact su(3) weight systems (Freudenthal), Weyl dims, Schur
  characters; self-tested.
* `model.py` - the 15 modes and weights; exact peeling; character and Weyl
  quadrature verifications; anomaly sums; Z6 and conjugation checks.
* `fock.py` - species-factorized Fock machinery: second-quantized generators,
  vectorized Gamma(g), blockwise Casimir assembly (C2's and the cubic C3 via
  collapsed term lists), the 12916-block Schur analysis, sector probabilities,
  product states.
* `run_rep.py`, `run_full.py`, `run_crosscheck.py` - as above; every claim in
  this report is asserted at runtime in one of them.
* `decomposition_full.json` - the 250-row commutant/center table (the analog of
  Paper 2's commutant table, ~60x larger center).
* `results_full.json`, `results_crosscheck.json`, `rep_checks.json` - all
  numbers quoted above.

Direction_A code is imported read-only (one memory-fix monkeypatch for d=64,
documented in `run_crosscheck.py`).
