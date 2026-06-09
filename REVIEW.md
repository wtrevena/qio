# Referee-Style Assessment of draft.md and arXiv Roadmap

Date: 2026-06-09. Companion: `experiments/RESULTS.md` (all Section 6
experiments now executed).

## Grading

**Intellectual honesty and epistemic hygiene: A.** The explicit status labels
in Section 3, the confidence tiers in 4.3, the pre-specified conjecture, and
the prominence given to negative results are well above the norm for
speculative-framework papers. This is the draft's strongest asset; preserve it.

**Technical correctness: A.** Every number was recomputed and verified
exactly: r_SM = 1.8174, the RG table, the crossing scale, the polygon-
inequality example, the PDG cross-checks. The Underconstraint Lemma proof is
correct. The Higuchi–Sudbery–Szulc citation is the right
necessary-and-sufficient result.

**Novelty: B.** The synthesis framing (QIO) is not new as a sentiment ("it
from qubit" + octonions both exist), but the coupling-entropy conjecture with
its underconstraint analysis, the r_SM(μ) scale-dependence computation, and
the use of the marginal polytope to prove feasibility are concrete and, to my
knowledge, not in the literature. The negative results are the publishable
core.

**Completeness: was C+, now B+.** The biggest weakness was that Section 6
described experiments never run. They have now been executed (see
`experiments/RESULTS.md`): all outcomes confirm and sharpen the paper's
thesis, and two new analytic facts emerged (two-qubit impossibility via
Schmidt; permutation rigidity of canonical octonionic states).

**References: A−.** Spot-checked and real. Fixes needed: ref [35] first
author is J.-C. Chang (not Y.-X. Liu); add arXiv:2512.17328 to ref [9];
ref [16] is conventionally cited as Adv. Theor. Math. Phys. 2, 231 (1998).

**arXiv readiness: C.** Markdown, placeholder author block ("W. [Author]"),
no figures, no code link. See roadmap.

## What the experiments change in the paper

1. Rewrite Section 6 as completed results (proposal → findings): match rate
   2.7×10⁻⁴ at N = 10⁷; matching manifold statistically generic in τ₃
   (KS 0.031 vs ordered Haar controls); Requirement C fails for
   unconstrained states — now measured, not just argued.
2. Add Experiment 2 table: every canonical octonionic state map
   (multiplication-table sign maps, Fano incidence, quaternionic lines,
   preferred-complex-direction states — generated convention-independently
   via Cayley–Dickson) yields permutation-degenerate entropies, so none can
   produce a hierarchy. This sharpens Requirement A: the selection principle
   must break more symmetry than any canonical construction does.
3. Add: the matching manifold intersects the W-class (τ₃ = 0) — explicit
   weighted-W curve — so coupling matching does not even fix the SLOCC class.
4. Add Control B analytic result: two-qubit pure states have S₁ = S₂
   identically, so the two-coupling map is impossible; three qubits is the
   minimal case where the ansatz has content. (Strengthens the
   division-algebra motivation in a small but real way.)
5. Add Controls A, C, D numbers (SM target generic among random targets,
   z = −0.92; four-qubit matches at comparable rate; all label permutations
   equivalent).
6. Add Figure 1 (results/fig1_experiments.pdf): (a) r_SM(μ) running with
   pole, (b) τ₃ matched-vs-control histograms, (c) weighted-W matching curve.
7. Update abstract + contributions to claim the completed computational
   program.

## Roadmap to arXiv (suggested order)

1. **Integrate results into draft.md** (items above) — content freeze.
2. **Convert to LaTeX** (RevTeX 4.2 or plain article; arXiv requires TeX for
   full-text papers). Real author name + affiliation; the AI-assistance
   acknowledgment already complies with arXiv policy and should stay.
3. **Reproducibility:** keep `experiments/` in a public GitHub repo; cite the
   repo (or a Zenodo DOI) in the paper. The code already has fixed seeds.
4. **Category strategy:** quant-ph is the best primary fit (the technical
   results are quantum-information theorems/computations); hep-th
   cross-list. Note: new submitters need endorsement for these categories;
   moderators sometimes reclassify speculative-framework papers to
   physics.gen-ph — the completed computational program and verified math are
   the best defense. Consider asking Szangolies or another cited author for
   endorsement/comments; sending a polite pre-post note to Szangolies and
   Furey could also catch errors and earn goodwill.
5. **Optional strengtheners (parallel, not blocking):**
   - Two-loop RG check that r_SM(μ) conclusions are stable (they will be;
     one paragraph).
   - Kempe invariant / full LU-invariant set on the matched sample
     (completes "all local unitary invariants" promised in 6.1).
   - A short proposition formalizing the permutation-rigidity observation:
     any state invariant under a transitive subgroup of qubit permutations
     has S₁ = S₂ = S₃, hence r_S undefined — with the canonical octonionic
     maps as instances.
6. **Title/abstract pass:** current title is long; consider leading with the
   sharp result, e.g. "Coupling-entropy matching in three-qubit models is
   underconstrained: an analysis of the octonionic route to Standard Model
   structure."

## Risks to acknowledge before posting

- The paper's positive content is a framework + negative results; some
  readers will ask "what is predicted?" The Sec 5.4 requirements and the
  executed controls are the answer — keep them prominent.
- The index ambiguity (Sec 2.3) and Control D together mean the qubit-gauge
  assignment is presently conventional; the draft says this honestly, keep it.
- PDG values are from the 2022 Review; optionally refresh to the current
  edition (changes are in the 4th decimal and do not affect r_SM at quoted
  precision).
