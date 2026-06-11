# arXiv Submission Package — Paper 5

## Package

`qio_paper5.tar.gz` — upload this file directly on the arXiv submission page.

Contents (verified self-contained; clean-room compile from the tarball: 0 errors, 0 undefined references, 13 pages, zero Type 3 fonts):

| File | Purpose |
|---|---|
| `main.tex` | Complete manuscript. Bibliography embedded as `thebibliography`; no `.bbl`/`.bib` needed. No figures. |

No custom style files (standard `article` class with geometry, fontenc/lmodern, amsmath, amssymb, graphicx, hyperref). arXiv AutoTeX runs pdflatex.

## Title

Fisher Information in Compact U(1) Flux Sectors: Asymptotic Exponential Families, a Crossover Obstruction, and a Topological Zero-Mode Bridge to Four Dimensions

## Abstract (plain text, 1,915 characters — within arXiv's 1,920 limit)

In two-dimensional Yang-Mills theory the boundary-flux distribution of the Hartle-Hawking state is a one-parameter exponential family in the coupling, and the sector entropy obeys dS/dt = -t I(t) with I the Fisher information of the flux measurement. We ask how much of that structure survives for compact U(1) gauge theory above two dimensions, where the electric flux through an entangling surface is a field of integers rather than one global label. Three results, each scoped to its regime. (i) Strong coupling (lattice, d = 3+1, leading order in 1/e^4): the ground-state flux distribution across a flat cut is an exponential family whose sufficient statistic is the dipole count -- not the quadratic Casimir -- with natural parameter logarithmic in the coupling; dS/dtheta = -theta I(theta) holds exactly at this order, and the information is extensive in the cut area. (ii) Globally in the coupling the family is curved: an exact-diagonalization rank test in the 2+1d dual-height representation shows that no single natural parameter or sufficient statistic covers the coupling axis. (iii) On a spatial 3-torus the topological winding sectors yield the one regulator-independent descendant of the 2d mechanism: in the Gibbs class of states the three global electric winding labels form an exact exponential family in e^2 over the integer flux lattice; dS/de^2 = -e^2 I(e^2) holds to the 10^-9 finite-difference floor; and the Fisher information is finite with metric-independent leading term b_2/(2e^4). Poisson resummation exchanges this family with its magnetic dual; on the self-dual torus S(e^2) = S(4 pi^2/e^2) exactly, and at e^2 = 2 pi one finds dS/de^2 = 0 with I > 0: the crossover obstruction in miniature. None of this is determination of the coupling by entanglement: the carrier is the contested, non-distillable center/edge sector, and every trace of e in the statistics is a compactness effect.

(arXiv metadata accepts UTF-8; if any character is rejected, replace with inline TeX. The TeX abstract in `main.tex` is the authoritative full version.)

## Category

**Primary: hep-th** (High Energy Physics – Theory).

Justification: the subject is entanglement entropy, edge modes, and topological flux sectors in compact U(1) gauge theory — directly continuous with the Donnelly–Wall, Casini–Huerta, and Soni–Trivedi literature, with electric–magnetic duality and the torus zero-mode sector as the central objects. It is the d > 2 sequel to Paper 3 (hep-th).

**Suggested cross-lists:**
- **hep-lat**: the strong-coupling result is a lattice Hamiltonian strong-coupling expansion, and the curvature obstruction comes from exact diagonalization of the 2+1d lattice theory in the dual-height representation (Kogut–Susskind formulation throughout).
- **quant-ph**: the organizing tools — exponential families, sufficient statistics, Fisher information, entropy–information identities — are the quantum-estimation methodology shared with the companion papers.

Avoid hep-ph (no phenomenology) and cond-mat (the height/dipole machinery is borrowed, not the subject).

## License

Recommended: arXiv's default non-exclusive license to distribute ("arXiv.org perpetual, non-exclusive license") — most journal-compatible; see the discussion in `paper/arxiv_submission/SUBMISSION.md`, which applies unchanged.

## Companion arXiv IDs — fill at announcement time

The bibliography cites one companion manuscript (`\bibitem{P3}` = Paper 3) as "companion paper (2026)" without an identifier. When Paper 3 receives its arXiv identifier at announcement, update that entry and cross-link the ID in the Comments field. Suggested order: submit after Paper 3, whose results it builds on.

## Practical submission checklist

- Upload `qio_paper5.tar.gz` as-is; verify the AutoTeX PDF preview is 13 pages.
- Metadata: paste title and abstract from this file; author "William T. Trevena".
- Comments field suggestion: "13 pages. Companion to [Paper 3 arXiv ID]. Code and raw outputs at [repository URL]."
- Endorsement: see the first-time-submitter guidance in `paper/arxiv_submission/SUBMISSION.md`; hep-th/hep-lat authors in the U(1) edge-mode literature are natural endorsers.
