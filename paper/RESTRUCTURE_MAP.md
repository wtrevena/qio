# Paper 1 Restructure Map (June 2026)

Old section/equation/figure numbers (28-page version of `paper/main.tex`, the version cited
by `paper2/main.tex` and `paper3/main.tex` as `\cite{companion}`) mapped to the new
restructured 21-page version. Use this to fix every cross-reference in Papers 2 and 3.

## Title change (affects bibliography entries in Papers 2 and 3)

- **Old:** "Is the Standard Model Coupling Hierarchy Encoded in Three-Qubit Vacuum
  Entanglement? No-Go Results, an Exact Octonionic Vacuum, and the Surviving Hypothesis Space"
- **New:** "Is the Standard Model Coupling Hierarchy Encoded in Three-Qubit Entanglement?
  Scoped No-Go Results and an Exact Octonionic Rotor Vacuum"
- Papers 2 and 3 quote the old title in their `\bibitem{companion}` entries — update those.

## Equations (unchanged numbers for the ones Papers 2/3 cite)

| Old | Content | New |
|---|---|---|
| Eq. (1) | logarithmic map `log(alpha_i^-1) = A + B S_i` (`eq:logmap`) | **Eq. (1)** (Sec. 2.1) — unchanged |
| Eq. (2) | gap-ratio condition `r_S = r_SM` (`eq:ratio`) | **Eq. (2)** (Sec. 2.2) — unchanged |
| Eq. (3) | `r_SM = 1.817` definition (`eq:rsm`) | **Eq. (3)** (Sec. 2.2) — unchanged |
| Eq. (4) | one-loop running (`eq:running`) | **Eq. (5)** (Sec. 5.1) |
| Eq. (5) | affine flow map (`eq:flowmap`) | **Eq. (6)** (Sec. 5.2) |
| Eq. (6) | entropy flow equation (`eq:flow`) | **Eq. (7)** (Sec. 5.2) |
| — | NEW: weighted-W normalization condition (`eq:wfamily`) | **Eq. (4)** (Sec. 4.1, inside new Lemma 2) |

## Figures (unchanged)

| Old | New |
|---|---|
| Fig. 1 (a) running of r_SM(mu) | **Fig. 1 (a)** — now discussed in Sec. 5.1 (figure placed in Sec. 3) |
| Fig. 1 (b) 3-tangle genericity | **Fig. 1 (b)** — Sec. 3.1 |
| **Fig. 1 (c) weighted-W matching curve** (cited by Paper 2) | **Fig. 1 (c)** — same panel; curve now given in closed form by **Lemma 2, Sec. 4.1** |
| Fig. 2 (entropy flow) | **Fig. 2** — Sec. 5.2 |

## Sections: old -> new

| Old | Old title | New location |
|---|---|---|
| 1 | Introduction | **Sec. 1** (compressed; contributions list -> Sec. 1.2 "Summary of Results") |
| 1.1 | Contributions | **Sec. 1.2** |
| 1.2 | Scope and Limitations | **Sec. 1.3** "Scope, Terminology, and Limitations" |
| 2 | The Division-Algebraic Program | **Sec. 1.1** (compressed ~70%; Hopf table kept) |
| 2.1 | Historical Development | **Sec. 1.1** (one paragraph) |
| 2.2 | The Three-Generation Observation | CUT (one clause survives in the Sec. 2.1 index-ambiguity remark) |
| **2.3** | **The Index Ambiguity** (cited by Paper 2) | **Sec. 2.1, "Remark (index ambiguity)"** — labeled paragraph at end of Sec. 2.1; sharpened cross-ref now points to Sec. 6.3 |
| 3 (3.1-3.8) | The Information-Spacetime Convergence | CUT (one motivational sentence with 5 citations remains in Sec. 1.1; one set-aside paragraph in Sec. 8.3) |
| 4 (4.1-4.3) | The QIO Framework | CUT (heuristic disclaimer absorbed into Sec. 1.3; open-specification list deleted; "QIO" name no longer used in the paper) |
| **5** | **The Coupling-Entropy Question** (cited by Paper 2 as "Secs. 5-6") | **Sec. 2** "The Static Conjecture and Its Underconstraint" |
| 5.1 | Motivation | **Sec. 2.1** (first half) |
| 5.2 | Pre-Specified Conjecture | **Sec. 2.1** (Conjecture statement; normalization caveat moved here and made prominent) |
| **5.3** | **Analytic Feasibility: The Underconstraint Result** (cited by Paper 2) | **Sec. 2.2** (Lemma, now "Lemma 1") **+ Sec. 2.3** (Proposition 1, feasibility/marginal polytope) |
| 5.4 | What Would Constitute Evidence | **Sec. 2.5** |
| 5.5 | Analytic Pre-Constraints | **Sec. 2.3** (merged into feasibility) |
| 5.6 | Minimality of Three Qubits | **Sec. 2.4** |
| **6** | **Computational Program: Design and Results** (cited by Paper 2 as "Secs. 5-6") | split: **Sec. 3** (genericity + controls) and **Sec. 4** (W-class + octonionic constructions) |
| **6.1** | **Experiment 1: Matching Manifold** (cited by Paper 2) | **Sec. 3.1** |
| **6.2** | **Experiment 2: Algebraically Motivated States** (cited by Paper 2; includes the weighted-W curve and the octonionic-construction table) | **Sec. 4** — weighted-W curve: **Sec. 4.1** (now analytic: **Lemma 2**); octonionic-construction table: **Sec. 4.2** |
| 6.3 | Scale Dependence of r_SM(mu) | **Sec. 5.1** |
| 6.4 | Null Controls (A-D) | **Sec. 3.2** |
| 6.5 | Implementation | **Sec. 8.4** "Reproducibility" (expanded into a standard reproducibility paragraph) |
| 7 | The Entropy-Flow Reformulation | **Sec. 5.2** "The Entropy-Flow Consistency Envelope" (relabeled explicitly as a consistency envelope, not a surviving conjecture) |
| 7.1 | The Revised Conjecture | **Sec. 5.2** (first part) |
| 7.2 | The Marginal Constraints Do Real Work | **Sec. 5.2** ("Computed feasibility constraints" block) |
| 7.3 | The Unification Corollary | **Sec. 5.3** "The Unification Corollary and the Normalization Caveat" |
| **8** | **Vacuum Selection from Algebraic Dynamics** (cited by Paper 2) | **Sec. 7** "An Exactly Solvable Symmetric Octonionic Rotor Vacuum" (reframed as a separate self-contained exact result; only place "vacuum" is used literally) |
| 8.1 | Three Levels | CUT as a framing device (Level-2 content = Sec. 7; Level-1 = Sec. 5.2; Level-3 aspiration dropped) |
| 8.2 | Computed Results: Rotor Hamiltonian (closed form) | **Sec. 7.1** (closed form + spectrum + invariants) and **Sec. 7.2** (unsigned + genericity controls) |
| 8.3 | Convention Robustness | **Sec. 7.3** |
| (8.2 last bullet) | "What this does and does not show" | **Sec. 7.4** |
| **9** | **The Jordan-Wigner Bridge** (cited by Paper 2: "construction inherited from Sec. 9") | **Sec. 6** "The Jordan-Wigner Gauge-Covariance Obstruction" |
| 9.1 | The Embedding Is Standard Mathematics | **Sec. 6.1** |
| 9.2 | Computed Consequences | **Sec. 6.2** |
| **9.3** | **Critical Caveat: Entanglement Is Gauge-Frame Dependent** (cited by Paper 2, twice) | **Sec. 6.3** |
| 10 | Connections to Open Problems | CUT to one paragraph: **Sec. 8.3** "Broader Motivations, Set Aside" |
| 10.1 | De Sitter Holography | CUT (mentioned by name only in Sec. 8.3) |
| 10.2 | The Cosmological Constant | CUT (mentioned by name only in Sec. 8.3) |
| 10.3 | Gauge Unification and the Monopole Problem | normalization point merged into **Sec. 5.3**; monopole framing CUT (named in Sec. 8.3) |
| 11 | Discussion | **Sec. 8** (rebuilt) |
| 11.1 | What Distinguishes the QIO | CUT (residue in Sec. 1.3 and Sec. 8.3) |
| **11.2** | **The Central Results** (cited by Paper 2 together with 9.3 as "the central open problem") | content distributed to **Sec. 1.2** (summary) and **Sec. 9** (Conclusion). For Paper 2's citation "(companion, Secs. 9.3, 11.2)" the correct new pointer is **"Secs. 6.3 and 9"** |
| 11.3 | Risks and Failure Modes | folded into **Sec. 8.1** (Table 1 "What is ruled out and what is not") and **Sec. 9** |
| 12 | Conclusion | **Sec. 9** |
| Note Added | (Paper 2 preview) | **Note Added** — kept, rephrased to Paper 2's current numbering (its Theorems 1-3, Lemma 4) |

## Quick lookup for every Paper 2 citation target

| Paper 2 cites (old) | Replace with (new) |
|---|---|
| Secs. 9.3, 11.2 | Secs. 6.3 and 9 |
| Sec. 9 (toy construction inherited) | Sec. 6 |
| Sec. 8 (rotor Hamiltonian / rotor vacuum) | Sec. 7 |
| Fig. 1c (weighted-W matching curve) | Fig. 1c (unchanged) — optionally add "Lemma 2" for the closed form |
| Secs. 5.3, 6.1-6.2 (underconstrained / generic / W-class) | Secs. 2.2-2.3, 3.1, 4 |
| Secs. 5-6 (static matching analysis) | Secs. 2-4 |
| Sec. 2.3 (index ambiguity) | Sec. 2.1, Remark (index ambiguity) |
| Sec. 6.2 (canonical octonionic constructions / weighted-W) | Sec. 4 (4.1 weighted-W; 4.2 octonionic table) |
| Sec. 6.1 (Haar genericity) | Sec. 3.1 |
| Eq. (1) | Eq. (1) (unchanged) |
| Eqs. (2)-(3) | Eqs. (2)-(3) (unchanged) |

## New material (no old counterpart)

- **Lemma 2 (Sec. 4.1):** analytic one-parameter weighted-W family solving r_S = r_SM
  exactly, with closed-form marginals, existence/uniqueness/smoothness proof, endpoints
  (W state at g->0; S1=1 at g_max = 0.082561), verified by `experiments/verify_wfamily.py`
  (new script; output `experiments/results/wfamily_verification.json`).
- **Table 1 (Sec. 8.1):** "What is ruled out and what is not."
- **Table 2 (Sec. 8.2):** the four-claims series table (Paper 1 opens the series).
- **Sec. 8.4:** standard reproducibility paragraph.

## Cut/trimmed bibliography (17 references removed; all others retained)

Removed because their supporting text (old Secs. 3, 4, 10) was cut: `hawking`, `thooft`,
`susskind95`, `jacobson`, `donoghue`, `maldacena13`, `swingle`, `almheiri`, `harlow17`,
`harlow19`, `verlinde`, `visser`, `moreva`, `favalli`, `susskind21`, `chang`, `freidel`.
Retained from the old motivational material (now one sentence in Sec. 1.1): `bekenstein`,
`maldacena`, `ryu`, `page`, `takayanagi`. All division-algebra, quantum-information, and
RG references are unchanged.

---

# Round-3 Addendum (June 2026, post-feedback revision)

Maps the **21-page round-2 version** (rows above) to the **round-3 version** (still 21 pages).
All `\label`s are unchanged; only rendered section numbers moved. Use this to fix
cross-references in Papers 2 and 3.

## Title change (round 3 — affects bibliography entries in Papers 2 and 3)

- **Old (round 2):** "Is the Standard Model Coupling Hierarchy Encoded in Three-Qubit
  Entanglement? Scoped No-Go Results and an Exact Octonionic Rotor Vacuum"
- **New (round 3):** "No-Go Results for a Three-Qubit Entropy Ansatz for Gauge-Coupling
  Hierarchies, with an Exact Octonionic Rotor Construction in an Appendix"

## Section moves: round 2 -> round 3

| Round 2 | Content (label) | Round 3 |
|---|---|---|
| Sec. 3 "Haar Genericity and Null Controls" (`sec:generic`) | compressed ~50% to a supporting sanity check | **Sec. 3** "A Sampling Sanity Check: Haar Genericity and Null Controls" |
| Sec. 3.1 (`sec:exp1`) | compressed to one paragraph | **Sec. 3.1** "Haar Genericity (Experiment 1)" |
| Sec. 3.2 (`sec:controls`) | controls A-D, compressed | **Sec. 3.2** (unchanged number) |
| **Sec. 5 "RG Obstruction / Entropy-Flow Envelope"** (`sec:rg`, `sec:running`, `sec:envelope`, `sec:corollary`) | **swapped after JW**; running table cut; section shortened | **Sec. 6** (6.1, 6.2, 6.3) |
| **Sec. 6 "Jordan-Wigner Gauge-Covariance Obstruction"** (`sec:jw`, `sec:embedding`, `sec:jwconsequences`, `sec:obstruction`) | **moved before RG** (now the paper's principal result) | **Sec. 5** (5.1, 5.2, 5.3) |
| **Sec. 7 "Octonionic Rotor Vacuum"** (`sec:rotor`, `sec:closedform`, `sec:rotorcontrols`, `sec:robustness`, `sec:rotorscope`) | **moved to appendix**, reframed as a dynamical control ("even the most canonical dynamical octonionic construction produces symmetry, not hierarchy"); all content kept | **Appendix A** "An Exact Octonionic Rotor Construction as a Dynamical Control" (A.1-A.4) |
| Sec. 8 Discussion (`sec:discussion`) | | **Sec. 7** |
| Sec. 8.1 (`sec:notruledout`) | | **Sec. 7.1** |
| Sec. 8.2 "This Paper in the Series" (`sec:series`) | series table (old Table 2) **deleted**; rewritten as a short pointer paragraph | **Sec. 7.2** "Relation to Subsequent Work" |
| Sec. 8.3 (`sec:broader`) | | **Sec. 7.3** |
| Sec. 8.4 (`sec:repro`) | | **Sec. 7.4** |
| Sec. 9 Conclusion (`sec:conclusion`) | rewritten around "naive entropy observable is not gauge-invariant => map not physically meaningful"; explicit "not refuting Szangolies" scope statement added (also in Sec. 1.1) | **Sec. 8** |

Sections 1, 2, 4 keep their round-2 numbers and subsection structure.

## Quick lookup for Paper 2/3 citation targets (round 2 -> round 3)

| Cited (round 2) | Replace with (round 3) |
|---|---|
| Sec. 6.3 (gauge-frame obstruction) | **Sec. 5.3** |
| Secs. 6.3 and 9 | **Secs. 5.3 and 8** |
| Sec. 6 (JW toy construction) | **Sec. 5** |
| Sec. 7 (rotor Hamiltonian / rotor vacuum) | **Appendix A** |
| Sec. 5 / 5.1 / 5.2 / 5.3 (RG, envelope, corollary) | **Sec. 6 / 6.1 / 6.2 / 6.3** |
| Secs. 2.2-2.3, 3.1, 4 (underconstraint/generic/W-class) | unchanged |
| Eqs. (1)-(7) | **unchanged** (the JW section has no numbered equations, so the Sec. 5/6 swap does not move equation numbers) |
| Fig. 1, Fig. 2 | unchanged (figure *text outlined* in round 3 to remove Type 3 fonts; content identical) |

## Tables (round 3)

- **NEW Table 1** (`tab:notions`, Sec. 1.3): notation table distinguishing (i) subsystem
  entropy of qubits (this paper's object), (ii) algebraic entropy relative to
  gauge-invariant algebras (Paper 2's object), (iii) flux-sector/edge entropy in gauge
  theory (Paper 3's object).
- Old Table 1 (`tab:notruledout`) -> **Table 2**.
- Old Table 2 (`tab:series`, four-claims series table) -> **deleted** (content reduced to
  one paragraph in Sec. 7.2).
- The RG representative-scales table (Sec. 5.1 of round 2) -> **deleted** (key values kept
  in the Sec. 6.1 text; curve remains Fig. 1a).

## Language/packaging changes (round 3, no structural effect)

- "machine-verified" -> "verified numerically" / "the accompanying code verifies".
- "adversarial review" -> "independent verification"; acknowledgment and reproducibility
  paragraphs now say "the repository includes an independent verification log and a
  response-to-review document".
- "the series"/"Paper 2"/"Paper 3"/"companion" reduced to essential pointers
  (Sec. 7.2 + Note Added).
- Added `\usepackage[T1]{fontenc}` + `\usepackage{lmodern}`; figure text converted to
  outlines; `pdffonts` on the built PDF shows zero Type 3 fonts.
- arXiv package `arxiv_submission/qio_paper1.tar.gz` rebuilt and clean-room verified
  (0 errors, 21 pages).
