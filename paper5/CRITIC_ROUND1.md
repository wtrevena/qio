# Paper 5 adversarial self-critic, round 1 (2026-06-11)

Reviewer stance adopted: hostile referee with access to the repo JSONs and the primary sources.
Every number in the draft was rechecked against the artifact that produces it; every literature
claim against `newwork/u1_4d/LITERATURE.md` (primary-source verified 2026-06-10) or a fresh
fetch. Verdicts: P0 = wrong/misleading, must fix; P1 = weakens the paper, fix; P2 = cosmetic.

## P0 (found: 1; fixed: 1)

1. **Theorem 1 hypothesis referenced the lattice Hamiltonian (eq. KS) but the exact zero-mode
   factorization is a continuum-compact-Maxwell fact.** On the lattice, the compact theory
   contains monopoles and the integer link-flux Hilbert space does not split exactly into
   (zero modes) x (oscillators); exactness as stated would be false-by-reference. FIXED:
   theorem restated for the compact Maxwell theory (circle-valued gauge field, the setting of
   Donnelly-Wall 1506.05792); Sec. 6 setup now says explicitly that the lattice theory reduces
   to it in the Coulomb phase up to e^{-S_mono}, and caveat (4) already covered the confining
   side. No numerical claim was affected (the scripts compute the continuum zero-mode family).

## P1 (found: 7; fixed: 7)

1. Theorem 1(c) limit was stated "as all t_i -> 0" but t_i is defined only for rectangular
   tori. FIXED: condition restated as beta e^2 lambda_max(G)/V -> 0, with the rectangular case
   as the special case.
2. b1/b2 conflation: electric windings live in H^1, fluxes through 2-cycles in H^2; the draft
   wrote "the b2 = 3 electric winding labels" in the abstract. FIXED: abstract now says "three
   global electric winding labels"; Sec. 6 adds the Poincare-duality sentence fixing b2 as the
   notation for the common rank.
3. Overfull hbox 74.7pt: the sigma3/sigma2 display inside the quote environment. FIXED:
   converted to prose.
4. Overfull hbox 33.4pt: inline DW eq. (36) formula. FIXED: displayed.
5. Overfull hbox 40.3pt: appendix file list line. FIXED: rewording allows the break.
6. Minor overfulls 8.5pt / 10.6pt (definition paragraph; continuum intro). FIXED: rewordings.
7. I_tot used in Theorem 1(d) without definition. FIXED: defined inline (I_E + I_M).

## P2 (found: 3; fixed: 3)

1. hyperref "Token not allowed in PDF string" warnings from math in section titles and \ref in
   the appendix title. FIXED: \texorpdfstring on the three affected titles + explicit pdftitle/
   pdfauthor in hypersetup.
2. Bibliography titles added beyond the prior verified record were re-verified against primary
   sources this session: arXiv:1512.06182 = Casini-Huerta, "Entanglement entropy of a Maxwell
   field on the sphere," PRD 93, 105031 (2016) [INSPIRE record fetched]; arXiv:1510.07455 =
   Soni-Trivedi, "Aspects of Entanglement Entropy for Gauge Theories," JHEP 01 (2016) 136
   [arXiv abstract page fetched]. Both as cited; no change needed beyond confirmation.
3. "Gauss-constrained to total flux zero through closed contractible Sigma" -- left as is
   (correct: no enclosed charge), noted for a future style pass.

## Number audit (all pass)

| Claim in draft | Source artifact | Value there | Verdict |
|---|---|---|---|
| dipole identity relres <= 1.1e-6 | results_dipole.json | max 1.04e-6 (e2=12) | OK |
| p_dip 1.2e-2 / I_th 2.4e-2 at e2=1.5; 1.0e-4 / 2.0e-4 at e2=5 | results_dipole.json | 1.205e-2/2.35e-2; 1.0e-4/2.0e-4 | OK |
| naive ratio = theta/4: 1.099...3.178 | results_dipole.json | matches to 3 decimals, 6 couplings | OK |
| ED slope -4.002, intercept 0.689 (ln2=0.693), p1/2c2=0.9999 | analysis_chain.json | -4.00196, 0.68917, 0.99985 | OK |
| ED identity relres <= 1e-3 for e2 >= 2.5; ~40% at e2=1 | analysis_chain.json | 9.99e-4/2.96e-4/3.48e-4; 0.379 | OK |
| ED naive ratio 1.079/1.558/1.965 vs theta/4 1.087/1.559/1.965 | analysis_chain.json | exact match | OK |
| rank sigma3/sigma2: 5.1e-2 / 3.8e-4 / 3.9-5.1e-2 / 1.4e-15 | analysis_chain.json + analysis_weak_hmax3.json | 5.147e-2 / 3.82e-4 / 3.92e-2 & 5.05e-2 / 1.35e-15 | OK |
| T(2): 2.23 -> 3.56 | analysis_chain.json / analysis_weak_hmax3.json | 2.2320 / 3.5596 | OK |
| theta = 1.17 e2 - 0.12, R2 = 0.989 (hmax=3) | analysis_weak_hmax3.json | slope 1.1651, intercept -0.117 (recomputed), R2 0.98898 | OK |
| hmax non-convergence at e2=0.3: theta 0.487/0.310/0.268 | REPORT.md sec. 5 (from run logs) + analysis_weak_hmax3.json (0.268 at hmax3) | consistent | OK |
| N-dependence <= 2e-5 in S (N=7 vs 6) | analysis_chain.json convergence | 1.99e-5 | OK |
| Lanczos residuals <= 2e-13; dims to 7^6 | REPORT.md sec. 5 | as stated | OK |
| T3 rank sigma3/sigma2: 6.1e-14 / 2.2e-14 / 1.6e-13 | results_t3.json A | 6.095e-14 / 2.160e-14 / 1.561e-13 | OK |
| T3 identity relres <= 7.5e-10 | results_t3.json B | max 7.484e-10 | OK |
| 2e4*I/b2 = 1 to <= 2e-12 for e2 <= 0.8 (3 metrics) | results_t3.json C | max dev 1.5e-10? no: <= 1.51e-10 at aniso e2=0.8; below 0.8: <= 4e-16; at e2=0.8 aniso 1.0000000001508 | see note |
| entropy asymptote <= 2e-15 at e2 <= 0.4 | results_t3.json C | max 1.78e-15 | OK |
| crossover curve peak ~1.53 near t~5 | results_t3.json curve | 1.5286 (t=5), 1.5269 (t=5.5) | OK |
| aniso e2=12 per-mode 1.002/1.311/0.656 | results_t3.json C | 1.0022/1.3108/0.6560 | OK |
| Poisson identity <= 1.2e-15 | results_t3.json D | max |dI/I| 1.17e-15 | OK |
| S_tot duality diff = 0.0 (4 pairs) | results_t3.json D | 0.0 | OK |
| self-dual: dS=0 (1e-10 floor), I_tot=0.10998, -e2 I=-0.691 | results_t3.json D | 0.0 / 0.109983 / -0.6910 | OK |
| joint ratio +1.000 -> 0 -> -1.000 | results_t3.json D | 1.0000000004 / -0.0 / -0.99999999949 | OK |
| joint rank sigma3=3.005, s4/s3=9.5e-12; control sigma3=1.4e-10 | results_t3.json D | 3.00505 / 9.52e-12 / 1.397e-10 | OK |

Note on the "2e4 I/b2 = 1 to <= 2e-12 for e2 <= 0.8" line: the aniso e2=0.8 entry is
1.0000000001508 (1.5e-10 deviation, a real theta correction from t=2/3, not numerics), so the
draft's "<= 2e-12" was too strong for that row. FIXED in the draft: the verification bullet now
says "to <= 2e-10 for e2 <= 0.8 (and to <= 3e-16 for e2 <= 0.4)".

## Literature audit (all pass, against LITERATURE.md quoted text or fresh fetch)

- DW 1506.05792 eq. (36) and q_B = q/sqrt(Vol F): verbatim in LITERATURE.md sec. 2.2. OK.
- DW noncompact zero-mode IR divergence quote: LITERATURE.md sec. 2.2. OK.
- CH 1512.06182: -16/45 vs -31/45, "coincides with Dowker's calculation": abstract quoted in
  LITERATURE.md sec. 1.1 and re-fetched this session. OK.
- CHMP 1911.00529: "independent of the precise UV dynamics" verbatim; coupling-value
  independence is the direction_B-verified load-bearing reading recorded in LITERATURE.md 3.1.
  Paper quotes the verbatim phrase and attributes the coupling-independence reading. OK.
- ST 1510.07455 distillation quote; MST 1811.06986 relative-entropy/MI quote; CHR center
  dependence; GST extended Hilbert space: LITERATURE.md secs. 3.2-3.3. OK.
- Guth/Froehlich-Spencer theorem + beta_c ~ 1.01 MC; Polyakov 2+1d gap: LITERATURE.md 4.6. OK.
- R15 1/2 dim(G) log(e^2 r): verbatim in LITERATURE.md 4.4. OK.
- 't Hooft 1979 torus flux sectors: standard-grade citation, used only for "labels are
  superselected" background. Acceptable.

## Scope/voice audit (style law of 20260610 feedback, lines 246-278)

- "machine-verified" appears 0 times; phrasing is "verified numerically", "reproduced by the
  published scripts". OK.
- Notation table appears in Sec. 2, before any result. OK.
- Contested-edge-term caveat: prominent (Sec. 2 framing, Sec. 7 tier 1 labeled load-bearing,
  Discussion). OK.
- Standalone: series reference reduced to one citation of [P3] for eq. (1) plus the epistemic-
  label convention; no Paper 1/2/4 references. OK.
- Underscores in file paths escaped (\_) throughout; checked compile renders them. OK.
- Scoped claims: Theorem only for the exactly-derived T3 family (continuum); strong coupling is
  a Proposition explicitly "at leading order"; the obstruction is labeled "computed" evidence,
  not a theorem. OK.

## Final build status (after all fixes)

pdflatex x2: 0 errors, 0 overfull/underfull boxes, 0 hyperref PDF-string warnings, 0 undefined
references/citations; 13 pages; pdffonts: all fonts Type 1 (lmodern), no Type 3. Paper 3 cited
under its current (retitled) name, read from `paper3/main.tex` at finalization time:
"Fisher Information and Coupling Reconstruction from Edge-Sector Statistics in Two-Dimensional
Yang-Mills".

## Remaining known limitations (disclosed in the paper, not fixable here)

- The crossover-obstruction numerics are 2+1d (strip, hmax <= 3); the 3+1d statement rests on
  the perturbative mechanism. Disclosed in Sec. 5 ("Scope of the numerics, stated plainly").
- The T3 family is a Gibbs/HH-class statement; the strict vacuum is a point mass. Disclosed
  (caveat 1) and paralleled to the 2d HH state.
- No computation of the distillable term in d >= 3. Disclosed in Sec. 2.
