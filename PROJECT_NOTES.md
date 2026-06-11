# PROJECT NOTES (Claude's internal working notes — maintained across sessions)

**Last updated:** 2026-06-10, after Paper 1 restructure (review round 2).
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

## TODO — next items (in order)

1. **[IN PROGRESS] Cross-ref reconcile after Paper 1 restructure:** paper2/main.tex has ~17 pointers to Paper 1's OLD section numbers (lines listed in Paper 2 agent report: L41, L53, L69, L160, L201, L207, L220, L224, L228, L242, L260, L268, L272, L296, L317, L318, L519) — remap via paper/RESTRUCTURE_MAP.md (9.3→6.3; 11.2→6.3+9; 5-6→2-4; 9→6; 2.3→2.1-Remark; 8→7; 6.2→4; 5.3→2.2-2.3; 6.1→3.1; Fig 1c, Eqs 1-3 unchanged). ALSO: Paper 1's TITLE changed — update its quoted title in paper2 + paper3 bibliographies (paper3 \bibitem{P1} also cites path "paper/draft.md" → point to paper/main.tex). Recompile both, 0 errors. Then commit.
2. Final read-through pass of all three PDFs (page-level sanity, cross-paper consistency).
3. User uploads Paper 1 to arXiv (package ready). After arXiv ID exists: fill placeholder refs in Paper 2 ([1] companion, [20] ym2companion) and Paper 3 ([P1]), rebuild their packages.
4. Build arXiv packages for Papers 2 and 3 (not yet done — only Paper 1 has one).
5. Decide Paper 4: two-ideal writeup vs u1_4d writeup vs both. Both REPORTs are paper-grade. Suggested: two-ideal first (it answers Paper 2's open objection; reviewer called it "the next real paper").
6. Optional per reviewer: update Papers 2/3 "in progress" mentions of the two research directions once Paper 4 decision is made (they currently claim no results — accurate but understated now).
7. Keep this file updated after every completed item.

## Commit log (this effort)

- b1f44ce series finalization round 1 (bylines, packages, critic rounds)
- e7c786b review round 2: Papers 2+3 revised, newwork/two_ideal + newwork/u1_4d research done
- (next) Paper 1 restructure + this notes file + cross-ref reconcile
