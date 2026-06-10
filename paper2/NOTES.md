# NOTES — items needing author attention before submission

Bullet-level issues noticed while drafting `sequel_draft.md` (2026-06-09). Ordered
roughly by how hard a referee will push. **Updated 2026-06-09 after the adversarial
referee pass and the verification dossier (`VERIFICATIONS.md`,
`direction_A/strengthen.py` / `strengthen_results.json`): items 1–10 below carry
one-line dispositions; new items 11–15 follow.**

1. **60 vs 66 assignment-count discrepancy (data inconsistency — must resolve).**
   `direction_A/results.json` records `n_assignments_tested: 60`; `direction_A/REPORT.md`
   (Sec. 4.5) says "66 finite assignments," and the same "66" propagated into planning
   notes. The code (`run_direction_A.py`, step 5c) enumerates 3 feature maps × 24 ordered
   triples = 72 and skips zero denominators; p₁ = p₂ kills 4 per feature map → 60. The
   draft uses 60 (the machine number). REPORT.md should be corrected, or the source of
   "66" explained.
   **RESOLVED (closed by review):** 60 confirmed as the machine number; the draft already
   used it, and the independent zoo reimplementation (Appendix B.3) re-derives 72 → 60.

2. **The center term's physical status is the paper's weakest joint.** Sec. 7.2 imports
   the CHMP critique honestly (classical term drops out of mutual information, is
   non-distillable), and argues the no-go only gets stronger under the strict reading.
   A referee may still ask: if the *only* gauge-invariant entanglement in the toy is the
   contested piece, why call it entanglement at all? The BRS single-copy/superselection
   defense is in place, but consider whether the abstract's "all edge, no bulk" slogan
   should carry an explicit qualifier.
   **HANDLED:** abstract slogan now qualified once ("with the caveat … contested [14]");
   reflection-vs-determination paragraph added at the end of Sec. 7.2 (Donnelly 2d YM =
   reflection via a dynamics-supplied family; this paper's no-go = determination), which
   pre-empts the referee question and frames the planned Paper 3.

3. **Corollary 2 (S_U(1) = S_U(3)) proof is new in this draft.** REPORT.md reports the
   equality as observed/machine-verified; the shared-center + Prop.-1 derivation was
   written for this paper and has not been independently checked. It is elementary
   (both commutants have the four weight projectors as center; every block has n_k = 1
   or m_k = 1) but deserves one more pair of eyes.
   **RESOLVED (closed by review):** derivation checked in the adversarial pass; no change
   needed.

4. **Scope of the "verified to 1.8e-15 over 10⁴ Haar states" claim.** The full block
   machinery was run on a 200-state subsample (plus named states); the remaining 9,800
   used a fast sector formula cross-checked to 2.0e-15 on that subsample. REPORT.md's
   phrasing slightly overstates this; the draft states it precisely (Sec. 5.1, App. A).
   Make sure REPORT.md and the paper stay consistent if either is edited.
   **RESOLVED (closed by review):** draft phrasing confirmed precise; REPORT.md sync
   remains a repo-hygiene task, not a paper issue.

5. **References [16] and [17] are cited by arXiv ID without verified titles.** I was not
   confident of the exact titles/venues for Soni–Trivedi 1608.00353 and
   Moitra–Soni–Trivedi 1811.06986 and left descriptive parentheticals instead. Verify
   titles, journals, and that 1608.00353 (not 1510.07455) is the right Soni–Trivedi
   paper for the non-distillability claim, per direction_B/LITERATURE_REVIEW.md. Also
   [1] needs a real arXiv number/DOI once the companion paper is posted, and [5]
   (Szangolies) has an arXiv ID (2512.17328) inherited from draft.md that should be
   double-checked — the number looks anomalous for a 2025 Entropy paper.
   **RESOLVED — but the suspicion was half-wrong:** [5] (Szangolies, arXiv:2512.17328)
   is *correct* as written (December-2025 arXiv posting of the mid-2025 Entropy article).
   The real error was [16]: the non-distillability result lives in **1510.07455**
   ("Aspects of Entanglement Entropy for Gauge Theories," JHEP 01 (2016) 136), not
   1608.00353; [16] re-pointed accordingly, with 1608.00353 retained only for the
   (3+1)-d free U(1) case under its correct title (JHEP 02 (2017) 101). [17] metadata
   filled (Moitra–Soni–Trivedi, "Entanglement Entropy, Relative Entropy and Duality,"
   JHEP 08 (2019) 059). [1] filled with the companion paper's full title and author;
   arXiv/DOI still pending posting (see item 13).

6. **SU(2)_L obstruction is structural argument, not computation.** Sec. 6.5 is labeled
   as such, but the claims "the mode gauge group is exactly U(3)" and "Furey's SU(2)_L
   acts between ideals" rest on representation-theoretic reasoning and on Furey's
   construction, respectively — neither is asserted by the code. A referee could ask for
   a machine check that no SU(2) subgroup of U(8) both normalizes the construction and
   acts as a gauge symmetry; consider whether a short lemma (number-conserving
   Bogoliubov group of 3 modes = U(3)) can be made rigorous in an appendix.
   **RESOLVED:** done exactly as suggested. New Appendix B.1 (machine-checked via
   `strengthen.py`): generator space dim 10 = dim u(3) + 1 (SVD gap 1.1e-15 vs 1.0),
   every generator exponentiates to e^{iφ}G(U) (residuals < 3e-15), group-level converse
   with no extra components (Schur step validated by mode-algebra dim 64), SU(3)
   centralizer = span{1, N} (dim 2, abelian), Bogoliubov enlargement to dim 16 entirely
   grading-violating. Sec. 6.5 status line upgraded.

7. **Convention-dependence of the r-zoo target.** r_SM = 1.8174 inherits the GUT
   normalization α₁ = (5/3)α_Y from the parent paper. The draft flags this (Sec. 7.5)
   and notes the structural reasons are normalization-independent, but re-running the
   60-assignment zoo under α_Y normalization would cost nothing and pre-empt the
   objection. (Expected: still no match; p₁ = p₂ degeneracy is unaffected.)
   **RESOLVED:** rerun done (Appendix B.3): α_Y⁻¹ = 98.33, target r_Y = 1.0433, still
   no match within 0.05 (or 0.01); best miss 0.2533 at r = log₂3/log₂(7/3) = 1.2966 —
   *worse* than the GUT miss 0.1826. Secs. 6.4 and 7.5 updated to cite it.

8. **Weighted-W collapse: 5 numerical points + exact support argument.** The numerical
   check covers only the 5 stored exp2 curve points; the "entire curve" claim rests on
   the (exact) observation that the family lies in the weight-1 sector. The draft
   phrases this carefully (Sec. 5.4); keep that phrasing if edited. Also note the
   matching-state single-qubit entropies quoted (0.9995, 0.8580, 0.7802) are exp2
   example[0], which differs from the example quoted in draft.md Fig. 1c
   (0.978, 0.895, 0.849) — different points on the same curve; worth a footnote if
   anyone diffs the two papers.
   **RESOLVED:** Sec. 5.4 now states "(five)" stored points explicitly and adds the
   one-line whole-curve proof (SU(3) transitive on the unit sphere of ℂ³ ⇒ every unit
   weight-1 amplitude vector is the third column of some U ∈ SU(3) ⇒ state = G(U)|001⟩;
   the points are confirmation, not the proof). Cross-paper footnote added after the
   Sec. 5.2 table: Paper 2's triple = examples[0] (grid index 0); Paper 1 Fig. 1c's
   triple = `weighted_W_example` (grid index 21, curve midpoint); both verified
   weight-1-supported and pure gauge (`strengthen.py`, dossier Sec. 4).

9. **Haar mean discrepancy is ~1.3σ, fine but unexplained in REPORT.** Sampled S_U(3)
   mean 1.5798 vs analytic 1.5767 with std 0.2391 over N = 10⁴ gives SE ≈ 0.0024, so the
   gap is ≈ 1.3σ — unremarkable, and the draft says "consistent with fluctuations."
   If a referee asks, that's the arithmetic.
   **RESOLVED (closed by review):** arithmetic confirmed; draft phrasing stands.

10. **Title and framing.** I changed the working title's back half to "…The
    Coupling–Entropy Question Made Well-Posed — and Closed." Alternatives kept the
    original "…and Its Answer." Also: the draft deliberately mirrors the parent's
    acknowledgment block and epistemic-status labels; if the parent's author block
    changes (name, affiliation), update both.
    **HANDLED:** author block synced to Paper 1's final form (William T. Trevena,
    Independent researcher (PhD, Industrial and Systems Engineering, University of
    Florida), with email); acknowledgment updated to name both code files. Title left
    as-is.

---

## New items (post-revision, 2026-06-09)

11. **Ghosh–Soni–Trivedi metadata in [16] not covered by the dossier.** The optional
    "see also" citation added to [16] — S. Ghosh, R.M. Soni, S.P. Trivedi, "On the
    Entanglement Entropy for Gauge Theories," JHEP 09 (2015) 069, arXiv:1501.02593 —
    was written from memory; VERIFICATIONS.md verified 1510.07455/1608.00353/1811.06986
    but not 1501.02593. Confirm title/venue against INSPIRE before submission (or drop
    the see-also; it is optional).

12. **Donnelly 2d Yang–Mills citation in the new Sec. 7.2 paragraph.** The
    reflection-vs-determination paragraph cites [10] (Donnelly, CQG 31, 214003) for the
    coupling-recoverability of the flux-sector distribution. If the precise 2d YM
    computation is better attributed to Donnelly, "Decomposition of entanglement entropy
    in lattice gauge theory," Phys. Rev. D 85, 085004 (2012), arXiv:1109.0036, add it as
    a separate reference. Also: "a companion paper in preparation develops the positive
    (reflection) case exactly" (Paper 3) has no reference entry yet — add one when it
    exists.

13. **[1] still needs an arXiv number/DOI** once the companion paper is posted
    (carried over from item 5; everything else in [1] is now filled).

14. **REPORT.md is now behind the paper in three places:** the "66" count (item 1), the
    Haar-subsample phrasing (item 4), and it does not mention `strengthen.py` /
    Appendix B at all. Sync or mark REPORT.md as superseded by the paper + dossier.

15. **M₂-support measured residual (≤ 3.3e-15).** App. A and Sec. 4 now distinguish the
    10⁻⁹ assertion threshold from the measured residual, with the measured figure taken
    from the verification dossier. If `run_direction_A.py`/`results.json` are
    regenerated, keep this number in sync (or have the script record it explicitly).
