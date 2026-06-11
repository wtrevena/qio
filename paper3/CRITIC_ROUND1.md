# Paper 3 — Adversarial Critic, Round 1 (internal)

Date: 2026-06-10. Referee instructions: full knowledge of the series plan
(SYNTHESIS.md, Papers 1–2), re-verify rather than trust. Everything below was
checked by rerunning code or refetching sources, not from memory.

## What was independently re-verified (no findings)

1. **Exact identities re-derived by hand.** (C1) S = ln Z + (t/2)⟨C₂⟩;
   (3) d⟨f⟩/dt = −½Cov(f, C₂), d ln Z/dt = −½⟨C₂⟩; (5) dS/dt = −(t/4)Var(C₂);
   (6) ∂_t ln p_R = ½(⟨C₂⟩ − C₂) ⇒ I = ¼Var(C₂); (7) dS/dt = −t·I(t);
   (8) C = t²I (−ln λ_R affine in C₂); (9) dS_n/dt = −(t/4)Var − (n−1)Cov(ln d, C₂)
   from S_n = S_1 + 2(n−1)⟨ln d⟩. All correct as printed in the draft.
2. **Full pipeline rerun from scratch in the sandbox** (scipy unavailable:
   `brentq` replaced by an independently written pure-Python Brent zeroin;
   matplotlib stubbed). `ym2_flux.py` and `ym2_su3.py` reproduce every quoted
   number to the digits shown: max dS/dt = −6.195e−3 / −4.539e−4 / −2.591e−4
   (SU2/U1/SU3); inversion ≤ 8.6e−14 (18 points); capacity 0.5/1.5/4.0 at
   t = 0.05; SU(3) RMSE {0.0080, 0.0162, 0.0318, 0.0650} at N = 10³;
   1.6%/0.48% at t* = 1; Var/CRB at N = 3×10⁴ in [0.925, 1.079] (SU2+U1) and
   [0.888, 1.073] (SU3); identity (9) worst rel. dev. 2.43e−10 (48 combos);
   n-cut demo sd/CRB_N = 0.925/0.967, sd/CRB_6N = 2.267/2.369 (√6 = 2.449);
   bias 1.41e−4 (SU3, t* = 1, N = 3×10⁴); clamps: 0 for SU(3), the single
   U(1) t* = 4, N = 30 batch as documented. Reproduction with an
   *independent* root-finder also confirms the results are not
   brentq-implementation artifacts.
3. **Donnelly [D14] transcriptions checked against the full text (ar5iv).**
   p(R) = (dim R)² e^{−2πr²q²C₂}/Z₁ (their eq. 35; = eq. (1) with t = 4πr²q²);
   S = Σ p(R)(−log p(R) + 2n log dim R) (their eqs. 18/37 = eq. (2)); the
   "independent of the number of intervals … does not change the amount of
   information" quote is verbatim (ellipsis correctly drops one sentence);
   "appears once for each of the 2n points on the boundary of A" verbatim;
   "not associated to uncertainty in gauge-invariant observables" verbatim;
   HH wavefunction ψ(R) ∝ dim R e^{−πr²q²C₂} (= d_R e^{−(t/4)C₂}).
4. **Gromov–Santos [GS14] checked against the full text.** tr ρⁿ and S with
   the 2lv counterterm (their eqs. 14–17) match (F5); e and A entering only
   as e²·A (their eq. 8) supports Sec. 5.3; SU(2) C₂ = (m²−1)/2 = 2j(j+1)
   (their eq. 22) confirms the ×2 convention note; their torus weak-coupling
   S = (3/2)ln T + … (their eq. 24) is the ½dim G·log structure quoted.
5. **Bridge sentences to Papers 1–2.** Checked against paper/main.tex
   (abstract, contribution 9) and paper2/sequel_draft.md (abstract,
   contributions 1–4): ill-posedness diagnosis, commutant/center framework
   attribution (BKOV/Zanardi/CHR), "all edge, no bulk", charge-sector
   distribution as the single-copy invariant data, and the pure-gauge
   matching-curve all accurately summarized. No overstatement found.
6. **Abstract overclaim audit.** The abstract claims estimability/recovery of
   t = g²A (defined in the same sentence), states "reflection, not
   determination" explicitly, flags the contested status of the edge term and
   the adverse d = 4 evidence. The six red lines of NOTES.md §14 are not
   crossed anywhere in the text. Title kept: "reconstructing … from …
   statistics" is the estimation claim actually proven, and Secs. 5.3–5.4
   bound it.
7. **[MOPT26] citation verified live** (arXiv:2603.10171, Melnikov, Oliveira,
   Peixoto, Tenser, March 2026): title, authors, and the qualitative
   area-monotonicity abstract claim are as characterized in Sec. 3.5 and the
   NOTES novelty table.
8. **SU(3) data.** dim(p,q) and C₂(p,q) formulas re-asserted at runtime in the
   rerun; C₂(1,0) = 4/3 = (N²−1)/2N, C₂(1,1) = 3 = N confirmed.

## Findings

### P0 — none

No factual, derivational, or numerical error found at claim level.

### P1 — fixed in this round

1. **[BFHK24] reference was wrong.** Tag initials match no author and the
   list "R. Amorosso, S. Syritsyn et al." silently dropped a coauthor. The
   papers (arXiv:2411.12818, arXiv:2410.00112) are by **Rocco Amorosso,
   Sergey Syritsyn, Raju Venugopalan** (verified on arXiv; (2+1)D published
   as JHEP 12 (2024) 177). Fixed: retagged [ASV24], full author list, journal
   ref added. (Resolves NOTES §13 open item 1.)
2. **Prop. 1's "S → ∞ as t → 0⁺" had no justification in the text** (NOTES §5
   action item). Fixed: added the short-time heat-kernel statement — Z(t) is
   the heat kernel of G at the identity, Z(t) ≃ vol(G)(2πt)^{−dim G/2} —
   with citation [Cam90] (Camporesi, Phys. Rep. 196 (1990)) and [CMR94], plus
   a computed witness: S(t) + ½dim G·ln t is constant to < 10⁻⁶ over
   t ∈ [0.002, 0.2] for all three groups, and for U(1) the constant equals
   the exact heat-kernel value ½ + ½ln 2π = 1.4189385 to seven digits.
   (Resolves NOTES §13 open item 2.)
3. **Unsupported computed claim:** Sec. 3.5 asserted Cov(ln d, C₂) > 0 on the
   full grid "for SU(2) and SU(3)" but only the SU(3) minimum (4.3×10⁻⁵) is
   recorded in published artifacts. Verified by direct computation: SU(2)
   minimum on the same 400-point grid is 1.1×10⁻³. Fixed: both minima now
   quoted.
4. **Byline email inconsistent with the series.** Draft had
   william.todd.trevena@gmail.com; Paper 1 (main.tex) and the series byline
   use trevenaw7@gmail.com. Fixed in draft and used in main.tex.

### P2 — fixed in this round

5. **[D14] section pointers (§2.2, §3) do not match the e-print structure**
   (ar5iv: §1.1 abelian, §1.2 nonabelian YM, §1.3 HH/de Sitter; the published
   CQG version may number differently). Fixed: section pointers removed; the
   unambiguous equation-level references (pr), (YM2entropy) retained.
6. **Missing symmetry-resolved-entanglement contact** (NOTES §10): the flux
   decomposition is a charge-resolved structure and the capacity has been
   used as a symmetry-resolution probe. Fixed: one sentence + citations
   [GS18] (Goldstein–Sela 1711.09418), [XAS18] (Xavier–Alcaraz–Sierra
   1804.06357), [ADKT23] (Arias–Di Giulio–Keski-Vakkuri–Tonni 2301.02117)
   added to Sec. 3.4. (Resolves NOTES §13 open item 3.)
7. **QFI remark uncited.** Braunstein–Caves [BC94] added to Sec. 3.3.
8. **[P1] repository path** said `draft.md`; fixed to `paper/draft.md`.
9. **Notation:** "I(t) → dim(G)/2t²" ambiguous; now dim(G)/(2t²) (two places).

### P2 — noted, not changed

10. **Rounding edge:** the SU2+U1 Var/CRB range quoted as [0.93, 1.08] has raw
    endpoints [0.9250, 1.0793]; 0.9250 → 0.93 at 2 dp is correct
    (round-half-up) but borderline. Raw minima recorded here for the record.
11. **"Determines" in Sec. 1.2** ("the invariant data determines t") is the
    information-theoretic sense (injectivity), explicitly disambiguated from
    metaphysical determination in Sec. 5.4; left as is.
12. **H(t) monotonicity** remains an honestly flagged open question (proof
    only for S); the draft promises nothing (NOTES §7) — correct as is.

## Verdict

With the P1/P2 fixes applied: the paper's claims are correct, sourced, and
reproduced; the deflationary framing is structurally enforced (every positive
claim is bound to t = g²A, d = 2, and the known-family caveat). Ready for
LaTeX conversion.
