# PROJECT NOTES (Claude's internal working notes — maintained across sessions)

**Last updated:** 2026-06-10 late PM, after push to origin/main and planning update for review round 3.
**Purpose:** if a session is interrupted, resume from here. Update this file after every completed work item.

## What this project is

QIO program → deflated into a defensible three-paper series. Success mode (user-endorsed): convergence with serious physics, not survival of the original framework. The arc: Paper 1 kills the naive three-qubit coupling-entropy matching (scoped no-gos), Paper 2 makes the question gauge-invariant and closes it in the minimal toy, Paper 3 gives the one exactly-solvable positive result (2d YM coupling reconstruction from flux statistics).

## Repo layout (all under C:\Users\willi\repos\qio)

- `paper/` — **Paper 1**: main.tex (authoritative, 21pp post-restructure), main.pdf, RESTRUCTURE_MAP.md (old→new section map), arxiv_submission/ (qio_paper1.tar.gz + SUBMISSION.md, clean-room verified). Root `draft.md` = superseded markdown (header note says so).
- `paper2/` — **Paper 2**: main.tex (authoritative, 21pp, theorem-ified), main.pdf, sequel_draft.md (superseded), CRITIC_ROUND2.md, NOTES.md (referee-anticipation items).
- `paper3/` — **Paper 3**: main.tex (authoritative, 20pp), main.pdf, draft.md (superseded), CRITIC_ROUND1.md, mle_bias_ci.py/.json, weak_coupling_check.py/.json.
- `newwork/two_ideal/` — two-ideal chiral extension research (REPORT.md + scripts + JSONs). DONE, not yet a paper.
- `newwork/u1_4d/` — 4d compact U(1) flux-sector research (REPORT.md, LITERATURE.md, DERIVATION.md + scripts). DONE, not yet a paper.
- `direction_A/`, `direction_B/`, `experiments/`, `ym2/` — earlier supporting computations (direction_A/REPORT.md marked superseded by Paper 2). `experiments/verify_wfamily.py` verifies Paper 1's new Lemma 2.
- `new_review.txt` — external review (round 2) that drove the restructure. `SYNTHESIS.md` — QIO 4.0 synthesis (pre-review).

## Key technical state (as of round 2)

- **Paper 1** (21pp, 0 errors): no-go-first structure; QIO material cut ~75-80%; new Lemma 2 = analytic W-family solving r_S = r_SM exactly (verified to 10 digits); "What this does not rule out" + four-claims series tables added; new softened title "…Three-Qubit Entanglement? Scoped No-Go Results and an Exact Octonionic Rotor Vacuum"; 17 refs trimmed (31 remain); Note Added updated to Paper 2's theorem numbering; arXiv tarball rebuilt + clean-room compiled; SUBMISSION.md abstract 1918 chars.
- **Paper 2** (21pp, 0 errors): Theorems 1-3 (commutant table; all-edge-no-bulk; matching curve pure gauge), scoped SU(2)_L Lemma 4, analytic Schur Appendix B, machine-checked Appendix C, Sec 8 "Entropy Is Not the Full Invariant State", Sec 9 two-ideal proposal (framed as in-progress). Title kept ("Algebraic Entropy" already in it).
- **Paper 3** (20pp, 0 errors): formal theorems with hypotheses block (compact connected Lie G, S², HH state, v=0 convention); Thm 1 monotonicity+inversion, Thm 4 Fisher, Prop 5 capacity, Thm 6 n-cut; Sec 3.4 two-channels (inversion vs MLE); novelty table; Sec 4.3 MLE bias/CI (27 cells, b₁=κ₃/(N·Var²) matches 26/27, coverage ~0.95); App A weak-coupling asymptotics verified to ~1e-14; Sec 7 benchmark checklist; 4d compressed to one proposed calculation.
- **newwork/two_ideal** (the next real paper, likely Paper 4 or 2b): 15-mode one-generation chiral Fock space (2^15); commutant = ⊕ M_{m_i}, 250 sectors, dim 57062, max mult 52; center = full gauge-irrep labels (a,b;2j;y) with congruence y≡4(a−b)+3(2j) mod 6 → detects (SU(3)×SU(2)×U(1))/Z₆; "all edge no bulk" FAILS here (genuine quantum invariant entropy, Haar ~0.2 bits, engineered state = exactly 1 bit); three-parameter question: posable, rank-3 Jacobian for Casimir moments (F₃,F₂,F₁) on product states — but the "three" is input not output; B/L-violating invariant operators present kinematically; QQQL vertex absent by Fermi statistics. All multiplicities machine-verified 4 ways.
- **newwork/u1_4d** (candidate Paper 4 alt or merged): exponential-family verdict = conditionally yes, phase-by-phase (Coulomb: discrete Gaussian in e², up to monopole corrections; strong coupling: dipole statistic, natural param θ=ln(16e⁸); crossover genuinely curved); dS=−θI generalizes as exponential-family lemma; 4d continuum: edge info UV-divergent/center-dependent, universal coefficients coupling-blind, BUT topological zero-mode family (Donnelly–Wall 1506.05792 eq 36) is exact exponential family with finite Fisher 1/(2e⁴) per mode = the one regulator-independent 4d descendant; ED on 2+1d plaquette chain observed the crossover. Literature gap confirmed: nobody has computed p({n}) vs coupling in d≥3. Paper-4 scope that is supportable: "asymptotic exponential families + crossover obstruction + zero-mode bridge"; one new computation needed: T³ flux-winding sectors on the lattice.

## Decisions on record (user)

- Byline everywhere: William T. Trevena / Independent Researcher (PhD, ISE, University of Florida) / trevenaw7@gmail.com.
- Submission order: 1 → 2 → 3 (kept against reviewer's 2→3→1 advice; arXiv, not journal-first).
- Paper 1: full restructure, NO split (rotor stays inside as section/appendix).
- New research: started both two-ideal and u1_4d (done); RG-flow model + lattice deferred as premature.
- User uploads to arXiv themselves; I prep packages. First-time submitter → endorsement needed (see paper/arxiv_submission/SUBMISSION.md).

## Operational gotchas (hard-won — do not rediscover)

- **Sandbox mount quirks:** files just edited from Windows side appear truncated (~16 bytes short) on /sessions/dreamy-cool-galileo/mnt/qio; files written from sandbox side can get NUL-padded on host. Workflow: edit via Windows-path file tools; copy to a FRESH NAME before sandbox compile (fresh names sync immediately); compile in /tmp; after sandbox writes, python-verify NUL-freeness + correct ending. The NUL bug corrupted paper/main.tex and the first tarball once — fixed.
- **Git: NEVER from sandbox** (index corrupts: "bad signature 0x00000000"; can't unlink index.lock). Use Desktop Commander (PowerShell on host). Repo-local identity already set (user.name William T. Trevena / user.email trevenaw7@gmail.com). If sandbox git ever ran by mistake: delete .git\index.lock on host, `git reset`, re-add.
- Desktop Commander processes exit after first command batch — use a new start_process per command group, `cd C:\Users\willi\repos\qio;` prefix.
- pip in sandbox: `--break-system-packages`; scipy often uninstallable → pure-NumPy shims (precedents: direction_A, paper3 scripts).
- arXiv tarball: embedded thebibliography (no .bbl needed); always clean-room compile from /tmp after rebuild; check NULs.
- Agents: don't let them run git; give each exclusive folder ownership; they should cite Paper 1 results by NAME not section number (sections changed in restructure).

## NEXT STEP (user-directed 2026-06-11, NOT yet started — do this first on resume)

**Round 4 — final pre-publication review.** Read `C:\Users\willi\repos\qio\20260611_7.54am_PST_revision_feedback.txt` (deliberately NOT yet read; content unknown). User instruction: treat it as ADVISORY feedback only — Claude applies whatever revisions Claude deems appropriate (not obligated to take every suggestion), then we wrap up and declare the series ready to publish. After applying: recompile + rebuild any touched arXiv packages (clean-room), re-run tests/run_tests.py if code touched, update this file, commit + push. Cowork task #16 tracks this. This is intended as the LAST revision round before publish-ready sign-off.

Triage discipline learned from rounds 2-3 (reuse): split feedback into (a) technical errors → always fix; (b) language/framing/scope → fix if consistent with deflationary strategy; (c) structural reorganization → weigh against user's standing decisions (separate papers, order 1→2→3→4→5, arXiv first); (d) journal-strategy advice → log in notes, don't act; (e) new-research suggestions → log as future work, don't start without user approval.

## STATUS 2026-06-11: ROUND 3 + PAPERS 4/5 + WIRING ALL COMPLETE

All five papers compiled (0 errors, Type-1 fonts only): P1 21pp "No-Go Results for a Three-Qubit Entropy Ansatz for Gauge-Coupling Hierarchies, with an Exact Octonionic Rotor Construction in an Appendix"; P2 22pp "…A Single-Copy No-Go for Coupling Encoding"; P3 22pp "Fisher Information and Coupling Reconstruction from Edge-Sector Statistics in Two-Dimensional Yang–Mills"; P4 16pp "Room for Three Couplings, and Only the Room: The Gauge-Invariant Algebra of a One-Generation Chiral Fock Space"; P5 13pp "Fisher Information in Compact U(1) Flux Sectors: …Topological Zero-Mode Bridge to Four Dimensions". All five arxiv_submission/ packages built + clean-room verified; abstracts <1920 chars; categories suggested per SUBMISSION.md files. Cross-refs fully wired (new titles everywhere, P1 round-3 section remaps applied in P2, placeholders twoideal/u1fourd filled). Repo packaged: README, requirements.txt (numpy==2.2.6, Python 3.10.12), MIT LICENSE, CITATION.cff, tests/ 12-test suite green in 1.7s (pytest-compatible; sandbox lacks pytest → tests/run_tests.py runner). T³ computation done (newwork/u1_4d/T3_RESULTS.md): exact exponential family on H¹(T³,ℤ), dS/de²=−e²I to 7.5e-10, I→b₂/(2e⁴) metric-independent, Poisson e²↔4π²/e² duality to 1.2e-15.

REMAINING (user actions + post-upload): (1) user uploads the five packages to arXiv (order 1→2→3→4→5 or batch; endorsement notes in paper/arxiv_submission/SUBMISSION.md); (2) after IDs exist: fill companion arXiv IDs in all five bibs + rebuild tarballs; (3) at submission: git tags paperN-v1-submission + Zenodo DOI (convention documented in README); (4) journal strategy ON RECORD for later: reviewer recommends P3 first (JMP/JPA/Annals/SciPost Core), P1+P2 merged for journal form, P4 likely most publishable continuation. (5) Known benign quirk: mount may serve stale tests/test_theorems.py view; Windows-side file is correct.

## PLAN OF RECORD (round 3 — completed 2026-06-11) — was: do in this order

1. **[IN PROGRESS] Review round 3** (feedback file read 2026-06-10 late PM). Triage: (a) arXiv path blessed "after cleanup"; journal advice (merge P1+P2, lead with P3, venues JMP/JPA/Annals/SciPost Core) LOGGED FOR LATER, not acted on — user's standing decision is separate papers 1→2→3. (b) P0 = repo-consistency: public repo shows two-ideal/u1_4d results while papers say "in progress" → resolved by writing Papers 4/5 + wiring pass. (c) Per-paper round-3 fixes dispatched to agents: P1 retitle (drop SM), rotor→appendix-as-control, Haar→sanity check, gauge obstruction before RG, Szangolies non-refutation sentence; P2 retitle (drop "— and Closed"), method framing, path-underscore typesetting fix, two-ideal mention update; P3 standalone-ization, exponential-family theorem first, QCD language down, MLE→appendix, nontrivial-group hypotheses, d=4 sync. All papers: notation table (3 entropy objects), "machine-verified"→normal phrasing, AI-review language→"independent verification log", Type-1 fonts (lmodern), series self-reference reduction. (d) Repo packaging agent: README w/ per-paper reproduce commands, requirements.txt, pytest theorem tests, LICENSE, CITATION.cff. Release tags + Zenodo DOI = at-submission user actions (logged).
2. **Wrap up Paper 4 (two-ideal, sequel to Paper 2).** Source: newwork/two_ideal/REPORT.md (computations done, machine-verified 4 ways). Write LaTeX in new paper4/ matching series conventions (article 11pt, embedded thebibliography, theorem style of Paper 2, standard byline), adversarial critic pass, compile 0 errors. Decision already made: two-ideal is Paper 4, separate paper, NOT folded into Paper 2 (it partially reverses Paper 2's "all edge no bulk" — sequel's job).
3. **Wrap up Paper 5 (u1_4d, note-length sequel to Paper 3).** First run the one missing computation flagged in newwork/u1_4d/REPORT.md: T³ flux-winding sectors on the lattice. Then write paper5/ at the supportable scope: asymptotic exponential families + crossover obstruction + zero-mode bridge (Donnelly–Wall 1506.05792 eq. 36 family, finite Fisher 1/(2e⁴) per mode). Critic pass, compile.
4. **Series wiring for the 5-paper batch.** Upgrade "in progress, no results claimed" mentions in Papers 1-3 to real citations of Papers 4/5 (locations verified by grep: Paper 1 discussion Sec 8.2; Paper 2 abstract + Sec 5.1 + Lemma 4 area + Sec 9 + conclusion; Paper 3 d=4 proposal paragraph ~L417). Build arXiv packages for Papers 2-5 (only Paper 1 has one). Final cross-paper consistency pass. Commit + push.
5. Strategy on record: post all five together (or 1-4 then 5); cite companions by title, fill arXiv IDs during the announcement cycle or in v2. User uploads; first-time-submitter endorsement notes in paper/arxiv_submission/SUBMISSION.md.
6. Keep this file updated after every completed item.

### Recently completed (this session)
- Cross-ref reconcile post-restructure: 15 pointers in paper2, 2 in paper3 (incl. out-of-list P2-title catch); L207 Fig-1c note reworded to Lemma 2 verification; 21pp+20pp, 0 errors, zero stale strings.
- Pushed everything to origin/main (git@github.com:wtrevena/qio.git, branch was newly created on remote, upstream now set). Verified pushed paper/main.tex blob is the clean 73,332-byte version — the 20,577 "NULs" seen via the mount were a stale-cache mirage; host+git were always clean. Lesson reinforced: NEVER trust the sandbox mount's view of repo files for verification; check via Desktop Commander/git cat-file on host.
- Task list (Cowork): #12 review feedback (pending), #13 Paper 4 (pending), #14 Paper 5 + T³ (pending), #15 series wiring + packages (pending).

## Exhaustive completion ledger (as of 2026-06-11, end of round 3)

**Papers — all compiled 0 errors, 0 undefined refs, Type-1 fonts only, byline standard:**
| Paper | Folder | Title (current) | Pages | Status |
|---|---|---|---|---|
| 1 | paper/ | No-Go Results for a Three-Qubit Entropy Ansatz for Gauge-Coupling Hierarchies, with an Exact Octonionic Rotor Construction in an Appendix | 21 | submit-ready |
| 2 | paper2/ | Gauge-Invariant Algebraic Entropy in a Minimal Fermionic Toy: A Single-Copy No-Go for Coupling Encoding | 22 | submit-ready |
| 3 | paper3/ | Fisher Information and Coupling Reconstruction from Edge-Sector Statistics in Two-Dimensional Yang–Mills | 22 | submit-ready |
| 4 | paper4/ | Room for Three Couplings, and Only the Room: The Gauge-Invariant Algebra of a One-Generation Chiral Fock Space | 16 | submit-ready |
| 5 | paper5/ | Fisher Information in Compact U(1) Flux Sectors: Asymptotic Exponential Families, a Crossover Obstruction, and a Topological Zero-Mode Bridge to Four Dimensions | 13 | submit-ready |

**Per-paper revision history:** P1: round-1 byline/package → round-2 full restructure (no-go first, QIO cut 75-80%, Lemma 2 analytic W-family, tables) → round-3 (retitle, rotor→App A as control, JW before RG, Haar compressed, Szangolies non-refutation sentence, notation table). P2: critic round (CRITIC_ROUND2.md, 0 P0) → theorem-ification (Thms 1-3 + Schur App B + scoped Lemma 4 + Secs 8/9) → round-3 (retitle single-copy, method-first framing, two-ideal consistency). P3: critic round (CRITIC_ROUND1.md) → formal theorems + bias/CI + weak-coupling App → round-3 (retitle edge-sector, exponential-family-first, MLE→App B, nontrivial-group hypotheses, QCD language removed). P4: written from newwork/two_ideal/REPORT.md, own critic round (3 P0 + 5 P1 fixed, all numbers verified vs JSONs). P5: T³ computation first (all 4 targets confirmed), then written, own critic round (1 P0 + 7 P1 fixed).

**arXiv packages (all clean-room verified from /tmp):** paper{,2,3,4,5}/arxiv_submission/qio_paperN.tar.gz + SUBMISSION.md each (abstracts 1913-1918 chars, all <1920; categories: P1 quant-ph+hep-th, P2 quant-ph+hep-th, P3 hep-th+quant-ph/math-ph, P4 quant-ph+hep-th, P5 hep-th+hep-lat/quant-ph; P3 tarball includes fig_ym2.png+fig_su3.png; P1 includes 2 outlined-font PDF figures; P2/P4/P5 tex-only).

**Cross-ref wiring (round-3 final state):** all five bibliographies carry the current titles; P2's 6 section pointers remapped to P1's round-3 numbering; P1 gained 4 companion bibitems (paper2-paper5) + neutral drafted-manuscript clauses in Sec 7.2 and Note Added; twoideal/u1fourd placeholders filled; zero "in preparation" language anywhere; READMEs say "drafted". Companion arXiv IDs are the ONLY placeholders left (filled after upload).

**Repo packaging:** README.md (per-paper one-command reproduction, all commands sandbox-verified; scipy-dependent scripts documented as such), requirements.txt (Python 3.10.12, numpy==2.2.6, matplotlib==3.10.9, scipy optional), LICENSE (MIT 2026), CITATION.cff (repo-level), tests/ (12 theorem-level tests, all green 1.7s; pytest-format + zero-dep run_tests.py runner because sandbox lacks pytest).

**Research artifacts:** newwork/two_ideal/ (commutant ⊕₂₅₀M_m dim 57062, center=(a,b;2j;y) detecting (SU(3)×SU(2)×U(1))/Z₆, all-edge-no-bulk fails, rank-3 Casimir Jacobian, 't Hooft catalog, QQQL Fermi-absent — all in P4). newwork/u1_4d/ (phase-by-phase exponential families, crossover obstruction, zero-mode bridge + T3_RESULTS.md: exact family on H¹(T³,ℤ), dS/de²=−e²I @7.5e-10, I→b₂/(2e⁴) metric-blind, Poisson duality @1.2e-15, self-dual point e²=2π — all in P5).

**External reviews processed:** new_review.txt (round 2 — full restructure driver) and 20260610.10.48_PM_PST_revision_feedback.txt (round 3 — retitles, repo-consistency P0, packaging). Round 4 file exists, unread (see NEXT STEP).

**Standing user decisions:** separate papers (no merges), order 1→2→3→4→5, arXiv first (user uploads; first-timer endorsement notes in P1's SUBMISSION.md), byline with (PhD, ISE, University of Florida), journal strategy deferred (reviewer: P3 → JMP/JPA/Annals/SciPost Core first; P1+P2 merge for journal form; P4 strongest continuation).

**Commit log:** b1f44ce round 1 → e7c786b round 2 + research → 69d2091 P1 restructure + notes → 6f4e8bc reconcile → 3051f2f plan → 6846f53 round 3 + P4/P5 + packaging → 677a29b wiring + packages (all pushed to git@github.com:wtrevena/qio.git main).
