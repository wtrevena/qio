# arXiv Submission Package — Paper 1

## Package

`qio_paper1.tar.gz` — upload this file directly on the arXiv submission page.

Contents (verified self-contained; compiles from scratch with 0 errors, 28 pages):

| File | Purpose |
|---|---|
| `main.tex` | Complete manuscript. The bibliography is embedded as a `thebibliography` environment, so no `.bbl` or `.bib` file is needed. |
| `fig1_experiments.pdf` | Figure 1 (Section 6 computational experiments) |
| `fig2_entropy_flow.pdf` | Figure 2 (Section 7 entropy flow) |

No custom style files are used (standard `article` class with geometry, amsmath, amssymb, graphicx, hyperref — all in every TeX Live, including arXiv's). arXiv will run pdflatex automatically (AutoTeX); the figures are PDF, which pdflatex handles natively.

## Title

Is the Standard Model Coupling Hierarchy Encoded in Three-Qubit Vacuum Entanglement? No-Go Results, an Exact Octonionic Vacuum, and the Surviving Hypothesis Space

## Abstract (plain text, 1,897 characters — within arXiv's 1,920 limit)

Our title question is motivated by emergent spacetime from entanglement and Standard Model structure from the octonions, bridged by Szangolies's three-qubit octonionic Hopf construction of the gauge group. We answer with systematic no-go results, verified with published code. The static version is underconstrained: across 10⁷ Haar-random states, the coupling-matching manifold is statistically generic, intersects the W class, and is matched equally well by random targets, four-qubit systems, and relabeled qubits. Two-qubit states cannot encode unequal couplings. Scale-independent entropies are inconsistent with renormalization-group running. Every canonical octonionic state construction tested is permutation-degenerate. An exactly solvable case sharpens the rigidity: the rotor Hamiltonian with multiplication-table-sign couplings equals i(L_u + 2R_u), u the sum of imaginary units; its unique ground state (√7 e₀ − iu)/√14 is provably convention-invariant and symmetric, with marginal spectra (1/7, 6/7) and 3-tangle equal to each squared concurrence, 8/49. Recognizing Furey's Cl(6) as the three-qubit algebra (Jordan-Wigner) yields charge as Hamming-weight grading — and an obstruction: gauge transformations are not local unitaries of the qubit factorization, so single-qubit entropies are gauge-frame dependent; the GUT normalization of α₁ adds convention-dependence. The title question is thus ill-posed as stated. What survives: gauge-invariant entanglement functionals; hierarchy from flow under an RG-consistent affine map, feasible only for |B| ≳ 126, whose one falsifiable consequence equates a symmetric boundary state with exact unification (SM asymmetry bottoms at 0.029; the MSSM reaches 0.003); and an explanation of why the algebra's canonical vacuum is symmetric. We offer a map of dead and surviving regions, not evidence for the motivating framework.

(arXiv's metadata fields accept UTF-8; if any Unicode character is rejected, replace with inline TeX, e.g. `$10^7$`, `$(\sqrt{7}\,e_0 - iu)/\sqrt{14}$`, `$\gtrsim$`.)

## Category

**Primary: quant-ph** (Quantum Physics).

Justification: the paper's core technical content is three-qubit entanglement theory — Haar-random state statistics, SLOCC/W-class geometry, single-qubit entropy polytopes, the 3-tangle, Jordan–Wigner factorizations, and algebra-relative (gauge-invariant) entanglement. The particle-physics content (coupling constants, RG running) is the *target* of the matching question, not new phenomenology; no new particle-physics predictions are made. This also matches where the closest prior work sits (Szangolies's qubit-entanglement/gauge-symmetry paper, the black-hole/qubit correspondence literature).

**Suggested cross-lists:**
- **hep-th** (High Energy Physics – Theory): the division-algebra/Cl(6) gauge-structure content, the emergent-spacetime framing, and the unification boundary-condition result are hep-th audience material.
- **math-ph** (Mathematical Physics), optional second cross-list: the exact octonionic rotor spectrum, the convention-invariance proof, and the Clifford-algebra dictionary are rigorous mathematical-physics results.

Avoid hep-ph as primary or cross-list: the paper deliberately makes no phenomenological claims.

## License

**Recommended: arXiv's non-exclusive license to distribute** (the default, "arXiv.org perpetual, non-exclusive license").

Reasoning: it is the most journal-compatible choice — many journals object to CC BY on preprints of submitted work, and this minimal license keeps every later publication option open. Choose **CC BY 4.0** instead only if you are certain you want maximal reuse rights granted to readers and your target journal permits it (e.g., you plan to submit only to fully open-access venues). Do not choose CC BY-NC-* or CC BY-SA (journal-incompatible) or public domain (irrevocable).

## Endorsement — what to expect as a first-time submitter

arXiv requires that first-time submitters to most categories, including **quant-ph**, be *endorsed* by an established arXiv author. As an independent researcher with a non-physics institutional email, you should expect the endorsement step to be triggered. What happens and what to do:

1. **Create your arXiv account first** (with trevenaw7@gmail.com), then start a submission to quant-ph. If endorsement is needed, the system tells you immediately and gives you a **6-character endorsement code** and a link you can send to a potential endorser.
2. **Who can endorse:** anyone who has authored a threshold number of arXiv papers in quant-ph in the recent past (arXiv shows "Which of these authors can endorse?" on every abstract page — look for the endorsement link at the bottom of any quant-ph paper's abstract page).
3. **Whom to ask:** the natural endorsers are researchers whose work this paper engages directly — e.g., authors in the division-algebra program (Furey, Todorov, Szangolies) or quantum-information researchers you have corresponded with. Send a short, specific email: the endorsement code, the paper PDF, a 2–3 sentence summary, and a sentence on why you are contacting them specifically. Endorsement asks only "is this a serious, on-topic scientific submission?", not refereeing — say so, since many people don't know that.
4. **Expect some friction:** endorsers are not obligated to respond; plan to ask 2–3 people, one at a time, and allow a week each. Cold requests succeed more often when the paper visibly engages the endorser's own work, which is true here for several candidates.
5. **Alternatives if endorsement stalls:** none within arXiv (arXiv staff do not endorse on request), but you can post to a preprint server without endorsement (e.g., Preprints.org, OSF) in the meantime. Do not submit to a less-gated arXiv category just to get in — cross-category dumping risks moderation holds.
6. **Moderation note:** independent-researcher submissions touching "Standard Model from octonions" territory get moderator attention. This paper's framing (rigorous no-go results, published code, explicit anti-numerology controls) is exactly what moderators look for in serious work; nevertheless, expect possible delay of a few days and possibly a reclassification suggestion. The "Note Added" referencing a companion paper in preparation is fine and standard.

## Practical submission checklist

- Upload `qio_paper1.tar.gz` as-is; arXiv unpacks and runs AutoTeX (pdflatex). Verify the generated PDF preview is 28 pages with both figures rendered.
- Metadata: paste title and abstract from this file; author "William T. Trevena"; no report number; MSC/ACM classes not needed.
- Journal-ref / DOI: leave blank (preprint).
- Comments field suggestion: "28 pages, 2 figures. Code and raw outputs at [repository URL]. Companion paper to follow." — fill in the actual code repository URL before submitting, since the manuscript states the code is published.
