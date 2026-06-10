# Synthesis: Directions A + B (2026-06-09)

Inputs: `direction_A/REPORT.md` + `results.json` (gauge-invariant entanglement
in the toy, computed); `direction_B/LITERATURE_REVIEW.md` + `SOURCES.md`
(edge-mode/contact-term literature, verified). Both executed by independent
subagents; both delivered adversarial-grade results.

## What Direction A established (computed, machine-verified)

The well-posed (BKOV/algebraic) version of the title question was computed in
the toy, and the answer is a no-go sharper than the ill-posedness it replaces:

1. The U(3) gauge-invariant data of any pure state is its charge-sector
   distribution (p₀, p₁, p₂, p₃) — the commutant is abelian ℂ⁴. Charge
   sectors have no natural bijection to the three gauge factors.
2. The rotor vacuum's sector distribution is exactly (1/2, 3/14, 3/14, 1/14),
   with p₁ = p₂: only two independent invariant parameters. The permutation
   rigidity survives gauge-invariantization.
3. **The paper's weighted-W coupling-matching curve is pure gauge**: every
   state on it satisfies S_𝒜 = 0 for all three invariant algebras, and
   W = G(U)|001⟩ explicitly. The static "match" matched frame artifacts.
4. SU(2)_L is not representable on the one-generation ideal (mode gauge group
   is exactly U(3) ≅ (SU(3)_c × U(1)_em)/Z₃): the three-coupling question
   was never posable in this toy.
5. Surprise with structural weight: for every pure state and all three
   invariant algebras, the quantum piece of the algebraic entropy vanishes
   identically — the gauge-invariant entanglement of the toy is 100% the
   classical center term, i.e. pure "edge mode" in the discrete
   Casini-Huerta sense. The toy's only gauge-invariant entanglement IS the
   discrete analog of the object Direction B studies.

## What Direction B established (literature, verified with quotes)

My proposed reformulation was right about the destination and wrong about how
much of the road is already paved:

- **Solid:** Susskind-Uglum → Cooperman-Luty: G_N renormalization absorbing
  the EE divergence is established. Kabat's contact term is exact as quoted.
- **Contested:** Donnelly-Wall's edge-mode statistical interpretation is
  challenged by Casini-Huerta-Magán-Pontello (1911.00529): center/edge term
  is regularization-dependent, drops out of mutual information.
- **Not in the literature (my overclaim):** "edge-mode coefficients match the
  beta function" — Donnelly-Wall's coefficients match the conformal anomaly,
  not 1/g² running; "beta function" appears zero times in their papers. No
  published "1/g² = edge-mode EE" exists. Worse, in free d=4 Maxwell the EE
  cannot depend on g at all, and CHMP's charged-matter correction is
  coupling-value-independent — direct evidence against naive identification.
  Nobody has proposed the three-SM-couplings application (novelty confirmed,
  for whatever a vacant niche is worth).
- **The defensible core:** the edge sector of gauge-field EE is the Shannon
  entropy of the normal-flux distribution — a genuine vacuum flux-fluctuation
  susceptibility that provably depends on g in d=2 (YM₂: p(R) ∝
  e^{−g²A·C₂(R)}) and d=3 (Radičević: universal ½·dim G·log(g²r) term). In
  d=4, g enters only via compactness and charged matter. The honest
  conjecture is **reconstruction, not identification**: coarse-grained flux
  statistics track g_i²(μ). Full identification ("couplings are nothing but
  entanglement") would require an induced-coupling scenario (Zee/Terazawa) —
  the gauge analog of induced gravity, which is unclaimed territory.

## The merged picture (QIO 4.0, stated honestly)

The two directions converge on one object from opposite sides: the classical
center/flux term of gauge-invariant entanglement. Direction A shows it is the
*only* gauge-invariant entanglement in the minimal toy; Direction B shows it
is the *only* place the coupling demonstrably enters entanglement in low
dimensions. The surviving program, in one sentence:

> **Vacuum flux-fluctuation statistics across an entangling surface are a
> gauge-invariant, dimension-dependent probe of g_i²(μ); the open question is
> whether, in an induced-coupling framework (the gauge analog of
> Jacobson/Sakharov), they determine the couplings rather than merely
> reflecting them.**

This is no longer the QIO. It is what the QIO turns into when every
non-surviving part is removed — which was the declared success mode.

Note the arc closed a loop: the project began with emergent gravity
(Jacobson) as motivation for an information-first view of gauge structure,
and after four pivots the surviving question is precisely the gauge analog of
Jacobson — induced couplings. The intuition was pointing at the right
neighborhood; the three-qubit literalism was the wrong vehicle.

## Consequences for the papers

1. **No-go paper (draft.md):** ship as planned. Optionally add one paragraph
   to Sec 9.3/12 noting the sequel result that the weighted-W matching curve
   is pure gauge (strengthens the ill-posedness conclusion to a computed
   triviality). The paper's claims as stated remain correct.
2. **Sequel paper (Direction A, mostly written):** "Gauge-invariant
   entanglement in a minimal fermionic toy: the well-posed coupling-entropy
   question and its answer." Content: commutant computations, exact rotor
   sector distribution, the pure-gauge collapse of the matching manifold,
   the vanishing quantum piece, SU(2)_L unrepresentability. Clean quant-ph
   paper; the two-ideal extension (to represent SU(2)_L) is its natural
   future-work section.
3. **Research program (Direction B):** the d=2/d=3 flux-susceptibility
   reconstruction is computable territory (lattice YM₂ is exactly solvable —
   a "measure g² from flux entropy" demonstration is a feasible next
   computation). The induced-coupling identification is the long-horizon
   question.

## Next steps (priority order)

1. Ship the no-go paper (author block, LaTeX, optional Sec 3/4/10
   compression, repo link).
2. Draft the Direction-A sequel from `direction_A/REPORT.md` (the
   computations are done and deterministic).
3. Computable B-test: YM₂ flux-distribution entropy vs g² — exact formulas
   exist; a short note demonstrating "coupling reconstruction from
   gauge-invariant entanglement statistics" in the one case where it is a
   theorem.
4. Two-ideal toy (two generations / doublet structure) to make SU(2)_L
   representable — the first construction in this program where a
   three-coupling question could even be posed gauge-invariantly.
