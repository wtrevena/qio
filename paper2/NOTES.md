# NOTES — items needing author attention before submission

Bullet-level issues noticed while drafting `sequel_draft.md` (2026-06-09). Ordered
roughly by how hard a referee will push.

1. **60 vs 66 assignment-count discrepancy (data inconsistency — must resolve).**
   `direction_A/results.json` records `n_assignments_tested: 60`; `direction_A/REPORT.md`
   (Sec. 4.5) says "66 finite assignments," and the same "66" propagated into planning
   notes. The code (`run_direction_A.py`, step 5c) enumerates 3 feature maps × 24 ordered
   triples = 72 and skips zero denominators; p₁ = p₂ kills 4 per feature map → 60. The
   draft uses 60 (the machine number). REPORT.md should be corrected, or the source of
   "66" explained.

2. **The center term's physical status is the paper's weakest joint.** Sec. 7.2 imports
   the CHMP critique honestly (classical term drops out of mutual information, is
   non-distillable), and argues the no-go only gets stronger under the strict reading.
   A referee may still ask: if the *only* gauge-invariant entanglement in the toy is the
   contested piece, why call it entanglement at all? The BRS single-copy/superselection
   defense is in place, but consider whether the abstract's "all edge, no bulk" slogan
   should carry an explicit qualifier.

3. **Corollary 2 (S_U(1) = S_U(3)) proof is new in this draft.** REPORT.md reports the
   equality as observed/machine-verified; the shared-center + Prop.-1 derivation was
   written for this paper and has not been independently checked. It is elementary
   (both commutants have the four weight projectors as center; every block has n_k = 1
   or m_k = 1) but deserves one more pair of eyes.

4. **Scope of the "verified to 1.8e-15 over 10⁴ Haar states" claim.** The full block
   machinery was run on a 200-state subsample (plus named states); the remaining 9,800
   used a fast sector formula cross-checked to 2.0e-15 on that subsample. REPORT.md's
   phrasing slightly overstates this; the draft states it precisely (Sec. 5.1, App. A).
   Make sure REPORT.md and the paper stay consistent if either is edited.

5. **References [16] and [17] are cited by arXiv ID without verified titles.** I was not
   confident of the exact titles/venues for Soni–Trivedi 1608.00353 and
   Moitra–Soni–Trivedi 1811.06986 and left descriptive parentheticals instead. Verify
   titles, journals, and that 1608.00353 (not 1510.07455) is the right Soni–Trivedi
   paper for the non-distillability claim, per direction_B/LITERATURE_REVIEW.md. Also
   [1] needs a real arXiv number/DOI once the companion paper is posted, and [5]
   (Szangolies) has an arXiv ID (2512.17328) inherited from draft.md that should be
   double-checked — the number looks anomalous for a 2025 Entropy paper.

6. **SU(2)_L obstruction is structural argument, not computation.** Sec. 6.5 is labeled
   as such, but the claims "the mode gauge group is exactly U(3)" and "Furey's SU(2)_L
   acts between ideals" rest on representation-theoretic reasoning and on Furey's
   construction, respectively — neither is asserted by the code. A referee could ask for
   a machine check that no SU(2) subgroup of U(8) both normalizes the construction and
   acts as a gauge symmetry; consider whether a short lemma (number-conserving
   Bogoliubov group of 3 modes = U(3)) can be made rigorous in an appendix.

7. **Convention-dependence of the r-zoo target.** r_SM = 1.8174 inherits the GUT
   normalization α₁ = (5/3)α_Y from the parent paper. The draft flags this (Sec. 7.5)
   and notes the structural reasons are normalization-independent, but re-running the
   60-assignment zoo under α_Y normalization would cost nothing and pre-empt the
   objection. (Expected: still no match; p₁ = p₂ degeneracy is unaffected.)

8. **Weighted-W collapse: 5 numerical points + exact support argument.** The numerical
   check covers only the 5 stored exp2 curve points; the "entire curve" claim rests on
   the (exact) observation that the family lies in the weight-1 sector. The draft
   phrases this carefully (Sec. 5.4); keep that phrasing if edited. Also note the
   matching-state single-qubit entropies quoted (0.9995, 0.8580, 0.7802) are exp2
   example[0], which differs from the example quoted in draft.md Fig. 1c
   (0.978, 0.895, 0.849) — different points on the same curve; worth a footnote if
   anyone diffs the two papers.

9. **Haar mean discrepancy is ~1.3σ, fine but unexplained in REPORT.** Sampled S_U(3)
   mean 1.5798 vs analytic 1.5767 with std 0.2391 over N = 10⁴ gives SE ≈ 0.0024, so the
   gap is ≈ 1.3σ — unremarkable, and the draft says "consistent with fluctuations."
   If a referee asks, that's the arithmetic.

10. **Title and framing.** I changed the working title's back half to "…The
    Coupling–Entropy Question Made Well-Posed — and Closed." Alternatives kept the
    original "…and Its Answer." Also: the draft deliberately mirrors the parent's
    acknowledgment block and epistemic-status labels; if the parent's author block
    changes (name, affiliation), update both.
