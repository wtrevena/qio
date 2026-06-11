# arXiv Submission Package — Paper 4

## Package

`qio_paper4.tar.gz` — upload this file directly on the arXiv submission page.

Contents (verified self-contained; clean-room compile from the tarball: 0 errors, 0 undefined references, 16 pages, zero Type 3 fonts):

| File | Purpose |
|---|---|
| `main.tex` | Complete manuscript. Bibliography embedded as `thebibliography`; no `.bbl`/`.bib` needed. No figures. |

No custom style files (standard `article` class with geometry, fontenc/lmodern, amsmath, amssymb, graphicx, hyperref). arXiv AutoTeX runs pdflatex.

## Title

Room for Three Couplings, and Only the Room: The Gauge-Invariant Algebra of a One-Generation Chiral Fock Space

## Abstract (plain text, 1,913 characters — within arXiv's 1,920 limit)

A companion paper computed the gauge-invariant algebras of an eight-dimensional one-generation fermionic toy and found the three-coupling question could not even be posed there: no SU(2)_L acts, and the invariant data of any pure state is its electric-charge distribution. This paper constructs the smallest arena on which the question is posable: the 2^15-dimensional fermionic Fock space over the fifteen Weyl modes of one Standard-Model generation (Q, L, u_R, d_R, e_R), on which the full gauge group acts with all anomaly sums vanishing. The commutant of the gauge action is derived by exact highest-weight methods and confirmed by four independent computations: 250 Wedderburn blocks, total dimension 57062, center C^250, maximal multiplicity 52, and a 28-dimensional space of invariant vectors. Four structural results. (i) The center labels are complete gauge-representation data for all three factors, satisfying y = 4(a-b)+3(2j) mod 6: the sector lattice is the weight lattice of (SU(3)xSU(2)xU(1))/Z_6, the global form selected by the matter content. Chirality, B, L, and B-L are not center labels, and the invariant algebra contains explicit B- and L-violating operators. (ii) The one-ideal theorem "all edge, no bulk" does not extend here: 185 of 250 sectors can carry quantum (non-center) invariant entropy, Haar states on the Q+L sub-arena carry 0.20 bits of it on average, and an explicit state achieves exactly 1 bit. (iii) Once posable, the three-coupling question receives a precise kinematic answer: the Casimir moments are functionals of the invariant center data, aligned one-to-one with the gauge factors, and independently tunable (rank-3 Jacobian). (iv) And that is all: nothing kinematic selects coupling values. The arena supplies room for three couplings, and only the room -- where a coupling is recovered (as in 2d Yang-Mills) it comes from a dynamical family of sector distributions.

(arXiv metadata accepts UTF-8; if any character is rejected, replace with inline TeX. The TeX abstract in `main.tex` is the authoritative full version.)

## Category

**Primary: quant-ph** (Quantum Physics).

Justification: like Paper 2, whose program it completes, the technical content is operator-algebra quantum information — commutants of unitary group representations on a fermionic Fock space, Wedderburn/Schur decompositions, superselection structure, and algebra-relative entanglement (including the first nonzero quantum invariant entropy in the series). The Standard-Model representation content fixes the arena but no phenomenology is proposed.

**Suggested cross-list: hep-th** — the Z_6 global-form result (sector lattice = weight lattice of (SU(3)×SU(2)×U(1))/Z_6, cf. Tong's line-operator analysis), the anomaly bookkeeping, and the B/L-violating invariant operators are hep-th audience material.

Avoid hep-ph: kinematic structure only, no phenomenological claims.

## License

Recommended: arXiv's default non-exclusive license to distribute ("arXiv.org perpetual, non-exclusive license") — most journal-compatible; see the discussion in `paper/arxiv_submission/SUBMISSION.md`, which applies unchanged.

## Companion arXiv IDs — fill at announcement time

The bibliography cites three companion manuscripts (`\bibitem{p1}` = Paper 1, `\bibitem{p2}` = Paper 2, `\bibitem{ym2}` = Paper 3) as "companion paper (2026)" without identifiers. When the companions receive arXiv identifiers at announcement, update these entries and cross-link the IDs in the Comments field. Suggested order: submit after Papers 1–2, which it cites by section.

## Practical submission checklist

- Upload `qio_paper4.tar.gz` as-is; verify the AutoTeX PDF preview is 16 pages.
- Metadata: paste title and abstract from this file; author "William T. Trevena".
- Comments field suggestion: "16 pages. Companion to [Paper 1/2/3 arXiv IDs]. Code and raw outputs at [repository URL]."
- Endorsement: see the first-time-submitter guidance in `paper/arxiv_submission/SUBMISSION.md`.
