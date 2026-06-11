# Paper 3 — Referee Anticipation Notes (internal, not for submission)

Date: 2026-06-09. Companion to `paper3/draft.md`. Purpose: every objection we
expect, with our honest position and where the draft handles it. The novelty
scan (item 1) is the load-bearing section; it was done by targeted search, not
assumed.

---

## 1. Novelty scan: what here is actually new vs Donnelly / Gromov–Santos?

**The blunt answer a referee deserves: the physics formulas are entirely
Donnelly's and Gromov–Santos's. Our additions are the statistical layer and
two derivative identities. We checked whether that layer already exists; we
could not find it. Detailed accounting:**

| Item | Status | Source / search outcome |
|---|---|---|
| p_R(t) ∝ d_R² e^{−(t/2)C₂}; S = H[p] + 2n⟨ln d⟩ | **Theirs.** | [D14] eqs. (pr), (YM2entropy); [GS14] eq. (answ). Verified against LaTeX sources (`ym2/FORMULAS.md`). |
| "All edge, no bulk" in 2d YM | **Theirs.** | [D11] third term vanishes; stated in [D14]. |
| Qualitative monotonicity of S in total area | **Partially anticipated.** | Melnikov–Oliveira–Peixoto–Tenser, arXiv:2603.10171 (March 2026), abstract: path-integral states have "entanglement consistently reducing with total area." We fetched and grepped their full text: no Var(C₂) identity, no "Fisher", no "capacity", no derivative formula — their statement is qualitative/by inspection of examples, and their focus is Wilson-line defects and large-volume limits. Our Proposition 1 (exact identity + bijection for all compact G) is sharper, but the draft must NOT claim the qualitative observation as new. Handled: [MOPT26] cited at Secs. 3.4, 3.5 and in references. Consider adding an explicit sentence "the qualitative area-monotonicity for path-integral states was observed in [MOPT26]" to Sec. 3.2 if a referee asks. |
| dS/dt = −(t/4)Var_t(C₂) | **Not found anywhere; trivial to derive.** | Searches: `"variance of the Casimir" entanglement Yang-Mills`; `"Var(C_2)" 2d Yang-Mills entropy`; `entanglement entropy derivative area "Casimir" two-dimensional Yang-Mills monotonic`. Nothing. It is three lines of exponential-family algebra, so its absence from the literature is unsurprising and its presence here is "low-hanging fruit," which the draft says verbatim (Sec. 3.4). |
| Fisher information I(t) = ¼Var(C₂); CR framing; MLE reconstruction demo | **Not found.** | Searches: `"Fisher information" "2d Yang-Mills" entanglement`; `"Fisher information" "two-dimensional Yang-Mills" coupling estimation`; `gauge coupling estimation entanglement Cramér-Rao`. Returned quantum-metrology papers (e.g. arXiv:2504.13729, two-qubit coupling estimation) with no Yang–Mills contact. The framing appears to be new packaging. NOTE honestly: the *mathematics* (exponential family ⇒ MLE = moment matching ⇒ CR saturation) is textbook statistics; what is new is only the identification of the YM₂ flux family as the instance and the susceptibility identity (7). |
| QFI = classical FI remark (commuting family) | **Standard QI fact, new application.** | Textbook (Braunstein–Caves); the application sentence is ours. Adjacent literature a referee might raise: fidelity susceptibility / quantum information metric for marginal couplings (Miyaji–Takayanagi et al.) — different quantity (state-space metric of the full vacuum vs. estimation from a subregion's invariant data). If asked, add one sentence distinguishing them. |
| Capacity of entanglement C(t) = t²I(t) in YM₂ | **Concept theirs, computation ours; no prior YM₂ appearance found.** | Concept: Yao–Qi arXiv:1001.1165; QFT systematics: de Boer–Järvelä–Keski-Vakkuri arXiv:1807.07357 (PRD 99, 066012). Searches: `"capacity of entanglement" "Yang-Mills" two-dimensional`; `"capacity of entanglement" lattice gauge`; `capacity entanglement 2d Yang-Mills sphere`. Closest hits: Nandy arXiv:2106.00228 (capacity for local-operator excitations in **4d free** YM); symmetry-resolution/RG capacity papers (arXiv:2301.02117); nothing in YM₂. The small-t plateau C → ½dim G appears to be unrecorded. |
| n-interval entropy 2n⟨ln d⟩ | **Theirs.** | [D14] eq. (YM2entropy), verbatim `2n \log \dim R`; verified directly against the e-print source (grep performed 2026-06-09). [GS14] l-cut replica agrees. |
| n-cuts add no information | **Qualitatively Donnelly's; quantitatively ours.** | [D14] source, abelian section, verbatim: "the entropy is independent of the number of intervals traced out … Having access to an additional interval therefore does not change the amount of information one can acquire about the state." The draft quotes this (Sec. 3.5) — claiming the point as ours would be indefensible. Ours: the identity dS_n/dt = −(t/4)Var(C₂) − (n−1)Cov(ln d, C₂); the observation that for nonabelian G the *entropy* nevertheless grows and becomes more t-sensitive with n while information stays fixed; and the duplicated-dataset CRB demonstration. |
| SU(3) flux statistics / reconstruction | **Computation new (trivially); group data textbook.** | dim and C₂ formulas verified against standard sources (Wikipedia SU(3) CG page; arXiv:2109.12087; consistency checks (N²−1)/2N and N asserted at runtime). [V08] and [GS14] have SU(N) entropy expressions; nobody had reason to run the estimation loop. |

**Risk assessment.** The most dangerous overlap is [MOPT26] (March 2026,
same year, same theory, monotonicity language in the abstract). Mitigation:
cite prominently, characterize precisely (done), and frame our Proposition 1
as the identity/bijection statement. Second-most dangerous: someone finds
dS/dt = −(t/4)Var(C₂) as an exercise in a TQFT or matrix-model paper we did
not search (the identity is too easy to be safe). Mitigation: the draft
already calls it low-hanging fruit and stakes the contribution on the
*combination* (identity + Fisher + capacity + reconstruction + n-cuts), not on
any single line.

Search-query log (June 2026, WebSearch + arXiv full-text fetch): the queries
quoted above, plus `SU(3) quadratic Casimir (p,q) dimension formula`;
`"capacity of entanglement" Yang-Mills`; `de Boer Järvelä Keski-Vakkuri
capacity`; `1406.7304 e-print grep ("2n", "intervals", "YM2entropy")`;
`2603.10171 full-text grep ("Fisher", "capacity", "variance", "monoton")`.

## 2. "The edge term is not entanglement" (CHMP / Moitra–Soni–Trivedi)

Expected from any referee fluent in the algebraic school. Position (drafted in
Sec. 5.2): we concede the interpretation dispute and decouple the result from
it — the reconstruction consumes p_R(t), which is an unambiguous gauge-
invariant distribution regardless of whether its Shannon entropy deserves the
name "entanglement." If a referee insists, we can retitle the recovered object
"superselection-sector statistics" with zero change to any number. Do NOT let
the rebuttal drift into defending the edge term's physicality; the series'
credibility rests on not needing it.

## 3. "What does sampling p_R even mean operationally?"

Fair. N i.i.d. samples = N independent preparations of the HH sphere state,
each measured once at one cut (Sec. 4.1 says this; Sec. 3.5 explains why
multiple cuts of one preparation don't multiply N). This is the standard
idealization of any tomography statement. The d = 2 theory has no dynamics to
re-randomize the flux, so time-averaging on one preparation is NOT a
substitute — worth adding a sentence if a referee pushes (ergodicity fails
trivially: R is a constant of motion).

## 4. "Only t = g²A is recovered, so you haven't reconstructed g."

Correct, and stated three times (abstract, Sec. 5.3, conclusion). The honest
formulation: entanglement data recovers the scheme-invariant combination, and
in d = 2 that combination is g²A. A referee who wants g alone is asking for
something diffeomorphism invariance forbids; that's a feature of the analysis,
not a bug — but we must not paraphrase ourselves anywhere as "measuring g²."
Check before submission: abstract says "the coupling … efficiently estimable"
— acceptable because t is defined in the same sentence, but audit all section
heads for an unguarded "the coupling."

## 5. "Proposition 1's t → 0 limit: S → ∞ needs justification."

S(t) ~ ½dim G ln(1/t) as t → 0 is computed, and is consistent with [GS14]'s
weak-coupling analysis; the divergence is the G-orbifold/heat-kernel
small-area behavior. For U(1) it is the Gaussian-sum estimate; for SU(2)/SU(3)
the capacity plateau (computed to 10⁻⁶) is the numerical witness. If a referee
wants an analytic proof of the asymptotics, cite heat-kernel small-t
asymptotics on group manifolds (Z(t) ~ vol(G)(2π t)^{−dim G/2} e^{…}); the
draft's claim is the numerically verified plateau plus consistency with
[GS14]; consider weakening "S → ∞" in Prop. 1 to cite the standard asymptotics
explicitly. ACTION ITEM before submission: add the heat-kernel citation
(Cordes–Moore–Ramgoolam §4 has the small-area limit).

## 6. "Your monotonicity is on a grid; the proposition claims (0,∞)."

The proposition's proof is analytic (Var > 0 from full support, two distinct
Casimir values suffice; Z analytic by locally uniform convergence). The grid
numbers are verification, not the proof. The draft says this, but make sure
the wording "computed verification" cannot be read as "the evidence is
numerical." Status: Sec. 3.2 is structured proof-first; OK.

## 7. "Shannon piece H is the gauge-invariant-uncertainty term; is IT monotone?"

Anticipated and answered honestly in Sec. 3.2: dH/dt has a competition term
+Cov(ln d, C₂) and is NOT manifestly monotone; numerically it is monotone on
the grid for all three groups; only S has the proof. A referee could ask for a
proof or counterexample for H in some group; we have neither. Acceptable as an
open remark; do not promise it.

## 8. "The n-interval claim depends on the cut topology / state."

Yes — stated in Sec. 3.5 ("Setting adopted"): circle spatial slice, HH state,
contractible cuts; the single-R structure follows from the physical Hilbert
space being class functions of one holonomy. On the torus spatial slice or
with Wilson-line insertions ([MOPT26], flux-tube papers) the sector structure
is richer and the no-extra-information conclusion can fail (e.g., a Wilson
line crossing region boundaries changes which R appears at which cut). The
draft's d = 3 paragraph already notes the n-cuts no-go is a d = 2 peculiarity.
If a referee asks for the general statement: information scales with the
number of *independent* superselection labels crossing the boundary, which the
topology and matter content control — a nice forward-looking sentence, could
be added to Sec. 6.

## 9. "MLE bracket/truncation engineering."

Documented in Appendix A and in `ym2_su3.py` docstrings: e⁻⁸⁰⁰ for
curves/identities (exactly zero error in float64), e⁻¹²⁰ for the MLE loop
(< 10⁻⁵⁰ relative truncation), bracket [0.02, 120] with monotone-grid
bracketing + brentq, clamps recorded (zero clamps for SU(3) anywhere; the
single U(1) t* = 4, N = 30 pathology is in the Paper-3-adjacent base results
and documented there). Determinism: per-component RNG streams; full run and
staged runs bit-identical. Nothing hidden here.

## 10. "Why no comparison to the symmetry-resolved entanglement literature?"

The flux-block decomposition IS a charge/symmetry-resolved structure, and the
capacity of entanglement has been used as an RG/symmetry-resolution probe
(e.g. arXiv:2301.02117). We cite the capacity lineage but not the
symmetry-resolved entanglement literature (Goldstein–Sela etc.). LOW-COST
IMPROVEMENT: one sentence + two citations in Sec. 3.4 would defuse this.

## 11. "Large N?"

[DTV19] computed the entropy's 1/N expansion (Boltzmann vs Shannon split).
We work at fixed small N and make no large-N claims. If asked how I(t) scales
with N at large N: Var(C₂) is computable from their results and the
Douglas–Kazakov transition would show up as a Fisher-information spike —
genuinely interesting FUTURE WORK; do not improvise it in the rebuttal.

## 12. "Series self-citations [P1], [P2] are unpublished."

True; they are repository companions with published code. The draft labels
them "companion paper" with repo paths. For arXiv submission, post all three
simultaneously and replace repo paths with arXiv IDs.

## 13. Internal consistency checklist (verified before this note)

- [x] SU(3) conventions asserted at runtime (six irreps).
- [x] Capacity plateau = dim G/2: 0.5 / 1.5 / 4.0 at t = 0.05 (exact to ~1e-15
      for U(1), SU(2); 4.0 - O(1e-7) for SU(3) at t = 0.05).
- [x] I(t* = 1): 0.500 / 1.500 / 4.000 — matches dim G/2t² to the digits shown
      (deviation appears by t* = 4: SU(3) I = 0.2495 vs 0.25).
- [x] Table numbers in Sec. 4.2 traced to `results.json` (U(1), SU(2)) and
      `su3_results.json` (SU(3)); RMSE/CRB and var/CRB ranges quoted correctly
      ([0.93, 1.08] base, [0.89, 1.07] SU(3) at N = 3×10⁴).
- [x] n-interval identity residual 2.4×10⁻¹⁰ (48 combinations).
- [x] Fisher demo ratios 0.93/0.97 (CRB_N) and 2.27/2.37 (CRB_6N), √6 ≈ 2.449.
- [x] Donnelly verbatim quotes in Secs. 2.2, 3.5 match the e-print source
      strings grepped on 2026-06-09.
- [x] RESOLVED 2026-06-10: [BFHK24] author list pulled from arXiv: Rocco
      Amorosso, Sergey Syritsyn, Raju Venugopalan (both 2411.12818 and
      2410.00112; the latter JHEP 12 (2024) 177). Tag was wrong too —
      renamed [ASV24] in draft and main.tex (CRITIC_ROUND1.md, P1-1).
- [x] RESOLVED 2026-06-10: heat-kernel small-t asymptotics added to Sec. 3.2
      with citation [Cam90] (Camporesi, Phys. Rep. 196 (1990)) + [CMR94];
      computed witness added: S + ½dim G·ln t constant to <1e-6 on
      t ∈ [0.002, 0.2], U(1) constant = ½ + ½ln 2π to seven digits
      (CRITIC_ROUND1.md, P1-2).
- [x] RESOLVED 2026-06-10: symmetry-resolved-entanglement sentence added to
      Sec. 3.4 with [GS18] 1711.09418, [XAS18] 1804.06357, [ADKT23]
      2301.02117 (JHEP 03 (2023) 175 verified) (CRITIC_ROUND1.md, P2-6).

## 14. What we deliberately do NOT claim (rebuttal red lines)

1. Not claiming the monotonicity *observation* is new (MOPT26 have the
   qualitative version for path-integral states).
2. Not claiming any d > 2 result, positive or negative.
3. Not claiming the edge term is physical/distillable entanglement.
4. Not claiming g is measurable separately from A.
5. Not claiming the exponential-family mathematics is novel — only its
   identification with the YM₂ flux family and the resulting identities.
6. Not claiming the toy-model results of [P2] transfer to YM₂ beyond the
   structural "all edge" parallel.

If a rebuttal ever needs one of these six, the paper is wrong, not the
referee.
