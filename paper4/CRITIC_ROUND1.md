# Paper 4 — Adversarial Self-Critic, Round 1

Scope: `paper4/main.tex` (the two-ideal/chiral extension paper). Method: every quantitative
claim in the draft was checked against the source JSONs
(`newwork/two_ideal/{rep_checks,results_full,results_crosscheck,decomposition_full}.json`),
all three generating scripts were rerun from scratch in a clean sandbox
(`run_rep.py` 1.0 s, `run_full.py` 16.4 s, `run_crosscheck.py` 3.6 s — **all asserts passed**,
seed 20260610), and every proof sketch was re-derived by hand. Findings are graded
P0 (must fix: wrong/misleading), P1 (should fix: weakens or risks misreading), P2 (polish).

## P0 — found and fixed

1. **Theorem/proposition numbering skipped 6.** The draft ran Lemma 1, Theorem 2,
   Proposition 3, Theorem 4, Proposition 5, then jumped to "Proposition 7" (QQQL) —
   there was no item 6. Renumbered QQQL to **Proposition 6** (3 occurrences:
   contributions list, Section 7 statement, Appendix A.2 back-reference). FIXED.

2. **"Central finite difference" was wrong.** `run_full.py` line 61 uses a one-sided
   (forward) difference for the generator-consistency check, which is why the residual
   is O(eps) = 4.5e-7 at eps = 1e-6. The draft said "central finite difference," which
   would imply an O(eps^2) residual and make 4.5e-7 look anomalously bad. Rephrased to
   "one-sided finite difference ... the residual is O(eps) as expected." FIXED.

3. **Stray empty `\section*{}` before the bibliography** produced a blank heading. Removed. FIXED.

## P1 — found and fixed

4. **Kernel-converse argument in Proposition 3 was loose.** The draft argued faithfulness
   of the Z6 quotient from "the realized labels generate the quotient weight lattice,"
   which is true but indirect. Replaced with the airtight one-liner: Λ¹V ⊂ F, so
   ker Γ = ker(mode rep), and triviality on the five species forces membership in ⟨ζ⟩
   (the standard one-generation computation). FIXED.

5. **Hyperref bookmark warnings** from math in two appendix section titles
   ($Q$, $\mathbb{Z}_6$). Added `\texorpdfstring`. FIXED.

6. **Abstract phrasing** "the global form with the Standard Model's matter content" →
   "the global form selected by the Standard Model's matter content." FIXED.

7. **Product-family formula** used `\bigotimes ... |0⟩`, which abuses notation (the
   factors are creation-operator polynomials, not states). Changed to an ordered
   product Π_modes (cos θ + sin θ f†)|0⟩, matching `fock.product_state`. FIXED.

8. **Layout**: five overfull hboxes (worst 97.8 pt — the named-states table; 89.4 pt —
   the reproducibility paragraph's unbreakable `decomposition_{full,Q,QL}.json`).
   Fixed by: footnotesize + tabcolsep 4pt + splitting the two-arena table into two
   tabulars; `decomposition_*.json` phrasing; `\sloppy` on the abstract,
   acknowledgment, reproducibility, and two inline-math theorem statements.
   Final build: **zero overfull hboxes**. FIXED.

## P2 — noted, deliberately not changed

9. `\\` in `\title` triggers one harmless hyperref "Token not allowed in PDF string"
   warning (same behavior as Paper 2's title). Cosmetic; bookmarks unaffected.
10. Theorem 2 cites `decomposition_full.json` inside the theorem statement for the
    multiplicity list. Unusual in a journal, but consistent with series practice and
    the 250-row table cannot be printed in full.
11. The uniform-product functional values are printed as exact rationals (31/8, 9/4, 5/6);
    the JSON floats agree to 6e-15 but the script does not assert the rational identity.
    Kept, flagged here. (The Haar trace values (4, 3/2, 5/6) were re-derived analytically
    during this pass: Tr C2(su3)/D = 8 · (1/4) · 4 · (1/2) = 4; Tr C2(su2)/D = 3/2;
    Tr Y²/D = (1/4)ΣY² = 5/6. They are exact.)

## Number-by-number verification record (all PASS)

| claim in paper | source | value | status |
|---|---|---|---|
| 250 sectors, dim A = 57062, 28 singlets, max m = 52 | rep_checks/full + rerun stdout | identical | PASS |
| 60 sectors m=1; 190 m≥2; 185 with n,m>1 = 94.8% (0.94824) | results_full | identical | PASS |
| largest sectors (3,2)±, m=52,n=6; (8,2)±, m=50,n=16; (8,1)0, m=42,n=8 | results_full.structure | identical | PASS |
| anomaly sums 0,0,0,0; ΣY=0; 4 doublets | rep_checks.anomalies (exact Fractions) | identical | PASS |
| closure 8.7e-17; homomorphism 4.6e-15; generator 4.5e-7 | results_full | identical | PASS |
| char identity 2.6e-12 (20 torus pts); Weyl grid 32³×128 → 57062, 28 | rep_checks + model.py source | identical | PASS |
| convention lemma 3.1e-12 (50 torus pts) | rep_checks | 3.0695e-12 | PASS |
| Z6 congruence y ≡ 4(a−b)+3(2j) mod 6: 0 violations; mode-level check | rep_checks + hand check of all 5 species | identical | PASS |
| 12916 blocks ≤ 30; 25356 block entries; C3 checks 2.2e-15, 4.4e-16 | fock.py header, results_full, results_crosscheck | identical | PASS |
| Q-only C^10, dims [1,1,4,6,6,6,6,9,9,16]; residuals 4.3e-14 / 7.2e-15 / 2.5e-16 | results_crosscheck.FQ | identical | PASS |
| skew-duality dims for the 10 partitions in the 3×2 box | hand re-derivation | sum = 64, dims match | PASS |
| Q+L: 31 sectors, dim 46, five m=2 sectors (labels checked) | rep_checks.QL + results_crosscheck | identical | PASS |
| engineered state: center < 5e-16, quantum = 1.0000; twirl 0.9981 (4000 MC) | results_crosscheck | identical | PASS |
| QL Haar: 4.526±0.056 / 0.200±0.024 / min 0.128 (300 states) | results_crosscheck.QL_haar | identical | PASS |
| QL uniform: 4.2799 / 0.1722 / 4.4521 | results_crosscheck | identical | PASS |
| full uniform 7.1643; generic 6.4576; Haar 7.183±0.007; mean-p gap 9.3e-5 | results_full | identical | PASS |
| F(uniform) = (31/8, 9/4, 5/6); F(θ0) = (3.160, 2.147, 0.556); Haar (4.000,1.499,0.834) | results_full | identical | PASS |
| functional cross-check ≤ 1.2e-14 | results_full (1.15e-14, 2.7e-15) | PASS |
| Jacobian matrix entries, sv (3.35, 1.75, 0.70), rank 3 | results_full.three_parameter_test | identical to 3 decimals | PASS |
| zero pattern (θ_L → F2,F1 only; θ_u,θ_d → F3,F1; θ_e → F1; θ_Q → all) | Jacobian columns | confirmed | PASS |
| F3-only direction dθ ∝ (−0.02,−0.05,−0.23,+0.20,−0.08); off-target < 1e-6 asserted | results_full | identical | PASS |
| MI: I(su3;Y)=1.61, I(su2;Y)=1.00, I(su3;su2)=0.07 bits (Haar measure) | results_full.label_mutual_information | 1.609/1.002/0.073 | PASS |
| 250 of 2775 = 15×5×37 label triples; y ∈ {−18..18} all 37; 2j = 0..4 | rep_checks.sector_lattice | identical | PASS |
| PH covariance 7.6e-17; 121 pairs, 54 degenerate, 67 split, gap 7.6e-3; 134 distinct p; Haar-mean gap 1.2e-2 | results_full | identical | PASS |
| singlet catalog rows (udd k3 B1L0; QLud; uude; LLuud k5 B1L2; u³d³e k7 B2L1; Q⁶d³ k9 B3L0; filled k15 B4L3); 28 total; complement-closed; B−L ∈ {−2..3} | results_full.singlet_spectroscopy | identical (incl. complement pairing spot-checks) | PASS |
| QQQL count = 0 at (3,1,0,0,0); j=3/2 obstruction | results_full + hand proof via skew duality | PASS |
| gauge invariance: dp 2.9e-15 (full); QL dp/dspec 2.7e-15, dS 4.6e-15 | results_full / results_crosscheck | identical | PASS |

## Build status

- `pdflatex` (two passes): **0 errors**, 0 overfull hboxes, 16 pages.
- `pdffonts`: **all embedded Type 1 (Latin Modern + AMS), no Type 3**.
- Compile performed on a byte-identical fresh-name copy (`build4.tex`, MD5
  `ff72f1c9...` matched across the Windows and sandbox sides before compiling).

## Style-law compliance (revision feedback, cross-paper items 1–5)

- "machine-verified" phrasing: absent; replaced by "the scripts assert / checked
  numerically / verified at runtime" throughout.
- Notation table early: Table 1 (three entropies + symbol glossary) in Sec. 1.3.
- Contested edge-term status: prominent in Table 1, Sec. 5.1, and Discussion 8.2,
  in both directions (center piece contested; no distillation claim for quantum piece).
- Series self-reference: no "Paper N" phrasing; companions cited as references with
  one-sentence context; paper is self-contained (definitions restated in Sec. 3.1).
- Scoped claims: "room, not values" language enforced in abstract, Sec. 1.3, Sec. 6.3,
  Sec. 8.3; "all edge no bulk" failure framed as scope, not contradiction (Sec. 5.1, 8.2).
- Underscores: all `\_`-escaped inside `\texttt`; renders correctly.

## Citation note

`\cite{p2}` title was re-checked against `paper2/main.tex` at the end of this round
(see final report); `\cite{ym2}` uses Paper 3's current retitled form ("Fisher
Information and Coupling Reconstruction from Edge-Sector Statistics in Two-Dimensional
Yang--Mills"); `\cite{p1}` uses Paper 1's current title.
