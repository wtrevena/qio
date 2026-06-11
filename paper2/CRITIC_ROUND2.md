# CRITIC ROUND 2 — adversarial referee pass on the compiled paper2/main.pdf

Date: 2026-06-10. Referee instructed to know the series plan (Paper 1 no-go /
Paper 2 well-posed closure / Paper 3 positive YM2 case) and to attack the
compiled LaTeX paper (17 pp., 0 errors), not the markdown draft. Source
computations rerun in the sandbox: `run_direction_A.py` and `strengthen.py`
both exit 0 with every runtime assertion passing (scipy was shimmed with a
pure-NumPy `digamma`/`expm`/pivoted-QR/`brentq`; the only residuals that moved
were the shim's own `expm` round-off — all paper numbers reproduced).

Verdict up front: **no result-level errors found.** Every theorem checks
against its proof; every number in the paper was re-derived from
`direction_A/results.json` / `strengthen_results.json` or recomputed
independently (including the rotor closed forms and both Dirichlet means by
hand-rolled digamma sums). Findings below are presentation- and
bridging-level.

---

## P0 — blockers

None.

- Compile: 0 errors, 0 undefined references/citations, 17 pages.
- Theorem audit: Proposition 1 (every block has n_k = 1 or m_k = 1 in all
  three computed block structures — confirmed against `results.json`
  `commutants.*.blocks`), Corollary 2 (centers coincide: both U(3) and U(1)
  commutants have the four weight projectors as center — confirmed),
  Lemma B.1 (dim 10, centralizer span{1,N}, Bogoliubov dim 16 — all
  re-executed), Lemma B.2 (sandwich logic sound: exhibited exactly-commuting
  elements give the lower bound; the sample commutant contains the true
  commutant, giving the upper bound; 4/6/20 = 4/6/20), Lemma B.3 (rerun:
  r_Y = 1.043286, best miss 0.25332, GUT cross-check 0.18256 — all match).
- Number audit (recomputed, not just diffed): S_U(3) = 1/2 + (1/2)log2 14 −
  (3/7)log2 3 = 1.724408 ✓; S_SU(3) = (4/7)(log2 7 − 2) + (3/7)log2(14/3) =
  1.413800 ✓; M2-block state (1/8)[[7, i√7],[−i√7, 1]] with block prob 4/7 ✓
  (conditional probabilities (1/2)/(4/7) = 7/8, (1/14)/(4/7) = 1/8, off-diag
  (7/4)/√28 = √7/8 ✓); E[S_U(3)] = 1.576660, E[S_SU(3)] = 1.396323 via
  ψ(9), ψ(4), ψ(3), ψ(2) ✓; (1/2 − 3/14)/(3/14 − 1/14) = 2 ✓; best-miss
  r = log2 3/log2(7/3) = 1.296607, |r − 1.043286| = 0.2533 ✓; 14 − 3 = 11
  U(1) parameters ✓; |v̄0 v3 (v1∧v2)̄| = (1/√28)(1/14) = √7/196 ✓.
- Abstract/intro overclaim check: every abstract claim (i)–(vi) maps to a
  machine-verified section; scope limited to the toy in Sec. 1.2 and 7.5;
  the contested status of the edge term is flagged *inside the abstract
  slogan itself*. No overclaim found.

## P1 — should fix (all fixed in this pass; see dispositions)

1. **Eq. (1) underbrace inverted in the LaTeX conversion.** The display
   rendered the *prose labels* as math content with the formulas as
   subscripts ("[classical / CENTER piece]" braced over H({p_k})), inverting
   the draft's intent and reading oddly in print.
   **FIXED:** braces now sit under the math, labels beneath:
   `\underbrace{H(\{p_k\})}_{classical (center) piece} + \underbrace{\sum_k p_k S(\rho_k)}_{quantum piece}`.

2. **PDG reference listed but never cited.** `\bibitem{pdg}` appeared in the
   bibliography with no in-text citation (the markdown draft had the same
   dangling [18]). A numbered, uncited reference invites a referee question
   about where the coupling inputs come from.
   **FIXED:** Appendix B.3's machine-checks paragraph now cites
   \cite{companion, pdg} for the α inputs.

3. **Bibliography widest-label argument said {19} with 20 entries.**
   Harmless at this width but technically wrong.
   **FIXED:** {20}.

4. **Bridge to Paper 3 was citation-less (NOTES item 12).** The
   reflection-vs-determination paragraph (Sec. 7.2) — the paragraph that
   sets up Paper 3 — ended with "a companion paper in preparation develops
   the positive (reflection) case exactly" with no reference entry, and the
   2d-YM recoverability claim was pinned to Donnelly CQG 31 (2014) alone,
   though the lattice decomposition S = H({p_R}) + Σ p_R(...) originates in
   Donnelly PRD 85, 085004 (2012).
   **FIXED:** added \bibitem{donnelly12} (PRD 85, 085004, arXiv:1109.0036),
   cited alongside donnelly14 at the three lattice-form/2d-YM points; added
   \bibitem{ym2companion} with Paper 3's actual title ("Reconstructing the
   Gauge Coupling from Gauge-Invariant Entanglement Statistics: The Exactly
   Solvable Case of Two-Dimensional Yang–Mills") and cited it at the end of
   the paragraph. Wording kept honest: the cited companion shows the
   coupling is "not only reflected but efficiently estimable" — which is
   exactly Paper 3's Cramér–Rao result, no more. The paragraph still does
   NOT promise determination in d = 4; checked against paper3/draft.md's own
   deflationary framing (reflection presupposes the known exponential family
   p_R(g²A)) — the two papers' framings agree verbatim in substance.

5. **sequel_draft.md out of sync with the mandated byline and with fixes
   2/4.** The markdown still carried the old author block
   (william.todd.trevena@gmail.com, "Industrial and Systems Engineering"),
   while the compiled paper uses the series byline (Independent Researcher
   (PhD, ISE, University of Florida), trevenaw7@gmail.com).
   **FIXED:** sequel_draft.md author block synced; Sec. 7.2 sentence and
   references [19] (Donnelly 2012) and [20] (Paper 3) added to the markdown.

## P2 — nice to have / explicitly scoped out

1. **Residual overfull boxes:** three, all ≤ 2.4 pt (Sec. 4 table 0.7 pt,
   soni bibitem 2.4 pt, B.1 paragraph 0.3 pt) — invisible at print
   resolution. Left as is.
2. **"One U(3) gauge orbit point" (Sec. 5.4)** is slightly compressed
   phrasing for "contained in a single U(3) orbit"; meaning is unambiguous
   from the surrounding sentence. Left as is (draft wording, intentionally
   preserved).
3. **Conditional expectation (Sec. 3.1)** is only qualified as
   trace-preserving in Appendix A. A measure-theory pedant might want the
   qualifier at first use; the "unique state ω on 𝒜 with ω(a) = ⟨ψ|a|ψ⟩"
   clause already pins it down uniquely. Left as is.
4. **[1] and [20] lack arXiv IDs/DOIs** — impossible until the companion
   papers are posted (NOTES items 12/13). USER DECISION: fill in at posting
   time, in both main.tex and sequel_draft.md.
5. **REPORT.md remains behind the paper** (NOTES item 14: the "66" count,
   Haar-subsample phrasing, no mention of strengthen.py). Repo hygiene, not
   a paper defect. USER DECISION: sync or mark superseded.
6. **Appendix B.1 exponentiation residuals quoted (< 3e-15)** are from the
   published scipy run; the sandbox rerun with a Taylor-series expm shim
   gave 9.9e-15 — attributable to the shim, not the lemma. No action; noted
   so nobody mistakes a future shimmed rerun for a regression.

## NOTES.md referee-anticipation items — verified disposition in the compiled paper

| item | status in main.tex |
|---|---|
| 1 (60 vs 66) | 60 used throughout; 72 → 60 derivation in Sec. 6.4 and B.3; rerun confirms. CLOSED |
| 2 (edge-term status) | abstract caveat present; Sec. 7.2 imports CHMP dispute + 3-part defense + "threatens only the consolation prize". CLOSED |
| 3 (Corollary 2 proof) | center identity re-checked against results.json block weight supports. CLOSED |
| 4 (Haar 200-subsample phrasing) | precise phrasing carried into Sec. 5.1 and App. A verbatim. CLOSED |
| 5 (refs 16/17/5) | re-pointed entries carried exactly as the verification dossier prescribes. CLOSED |
| 6 (SU(2)_L machine check) | Appendix B.1 in full, status line upgraded in Sec. 6.5. CLOSED |
| 7 (α_Y rerun) | Appendix B.3 + Secs. 6.4/7.5 cite it. CLOSED |
| 8 (5 points + support argument) | "(five)" explicit; SU(3)-transitivity one-line proof in Sec. 5.4; cross-paper note after the Sec. 5.2 table. CLOSED |
| 9 (1.3σ Haar gap) | "consistent with N = 10⁴ fluctuations" retained; arithmetic re-verified (SE ≈ 0.0024). CLOSED |
| 10 (title/author block) | title kept; author block now the series byline per instruction (supersedes the "sync to Paper 1's old form" disposition). CLOSED |
| 11 (Ghosh–Soni–Trivedi 1501.02593) | verified against arXiv on 2026-06-10: title, authors, and the non-distillability sentence in the abstract all match. CLOSED |
| 12 (Donnelly 2012 + Paper 3 ref) | both added (P1 fix 4). CLOSED |
| 13 ([1] arXiv ID) | pending posting — user decision (P2.4). OPEN by necessity |
| 14 (REPORT.md sync) | repo hygiene — user decision (P2.5). OPEN by choice |
| 15 (M2 residual sync) | App. A distinguishes assertion threshold (1e-9) from measured residual (≤ 3.3e-15); consistent with dossier. CLOSED |

## Cross-paper consistency checks

- Notation: r_S, r_SM = 1.8174, GUT-normalized α1 = (5/3)α_Y, weighted-W
  family a|001⟩ + b|010⟩ + c|100⟩, rotor vacuum (√7 e0 − iu)/√14, marginal
  spectra and Hamming-weight grading — all match Paper 1's main.tex symbols
  and values. Paper 1 internal pointers cited from Paper 2 ([1] Eq. 1,
  Eqs. 2–3, Secs. 2.3/5.3/6.1–6.2/8/9.3/11.2, Fig. 1c, Experiment 1
  tolerance 0.01 vs Sec.-6.2 tolerance 0.05) were each checked against
  paper/main.tex: all exist and say what Paper 2 claims they say.
- The Sec. 5.2 cross-paper note (examples[0] vs curve midpoint, grid
  indices 0 vs 21 of 43) matches strengthen_results.json exactly.
- Paper 1's "Note Added" promises precisely what Paper 2 delivers (curve
  pure gauge, W = G(U)|001⟩, charge-sector reduction, SU(2)_L absent) — no
  drift between the two.
- Bridge to Paper 3: Paper 2 claims only "reflection … developed exactly"
  + efficient estimability; Paper 3's abstract claims monotonicity, Fisher
  identity, CR saturation, and its own deflation. No overpromise in either
  direction.

## Most serious finding

The most serious finding of the pass is the cluster fixed as P1.4: the one
paragraph whose job is to connect this paper to the rest of the series (the
reflection-vs-determination paragraph) cited neither the originating 2d-YM
lattice paper nor the companion paper that delivers the positive case. As of
this round both citations exist and the wording matches what Paper 3 actually
proves. Everything else found was cosmetic.
