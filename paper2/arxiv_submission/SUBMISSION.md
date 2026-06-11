# arXiv Submission Package — Paper 2

## Package

`qio_paper2.tar.gz` — upload this file directly on the arXiv submission page.

Contents (verified self-contained; clean-room compile from the tarball: 0 errors, 0 undefined references, 22 pages, zero Type 3 fonts):

| File | Purpose |
|---|---|
| `main.tex` | Complete manuscript (series-wired version, June 2026: companion bibliography entries carry the final titles; Paper 1 section pointers remapped to its round-3 numbering). The bibliography is embedded as a `thebibliography` environment, so no `.bbl` or `.bib` file is needed. No figures. |

No custom style files are used (standard `article` class with geometry, fontenc/lmodern, amsmath, amssymb, graphicx, hyperref — all in every TeX Live, including arXiv's). arXiv will run pdflatex automatically (AutoTeX).

## Title

Gauge-Invariant Algebraic Entropy in a Minimal Fermionic Toy: A Single-Copy No-Go for Coupling Encoding

## Abstract (plain text, 1,918 characters — within arXiv's 1,920 limit)

Whether an entanglement functional carries physical content in a gauged system is computable: is it invariant under the gauge action? We give a general finite-dimensional method -- compute the commutant of the unitary gauge action, identify its Wedderburn block structure, and evaluate entropy relative to that gauge-invariant algebra (the Barnum-Knill-Ortiz-Viola/Zanardi algebra-relative framework, discrete cousin of the Casini-Huerta center decomposition) -- and execute it end to end in the eight-dimensional Jordan-Wigner/Fock realization of the one-generation division-algebraic ideal, where a predecessor analysis showed gauge transformations are not local unitaries of the qubit factorization, so the question "is the Standard Model coupling hierarchy encoded in three-qubit vacuum entanglement?" was ill-posed. The commutants are derived by Schur's lemma and certified numerically: gauging U(3) leaves the abelian algebra of charge-sector projectors; SU(3) leaves M2+C+C; U(1) leaves M1+M3+M3+M1. Findings, all asserted at runtime by code: (i) the single-copy gauge-invariant data of any pure state under U(3) is its charge-sector distribution alone; (ii) for every pure state and all three algebras the quantum piece of the algebraic entropy vanishes -- all edge, no bulk; (iii) the predecessor's one surviving static "match", the weighted-W coupling-matching curve, is pure gauge: every state on it has zero invariant entropy and is gauge-equivalent to one Fock basis state; (iv) the algebra-canonical rotor vacuum carries two independent invariant parameters -- fewer than three couplings; (v) an exhaustive sector-to-coupling search misses the measured ratio; (vi) no SU(2)_L action is present in this one-ideal realization, so a two-ideal/chiral construction is required before a three-coupling question is even posable. The no-go is deliberately single-copy; the multi-copy invariant ring remains open.

(arXiv metadata accepts UTF-8; if any character is rejected, replace with inline TeX. The TeX abstract in `main.tex` is the authoritative full version; this plain-text rendering compresses notation, e.g. M2+C+C for $M_2 \oplus \mathbb{C} \oplus \mathbb{C}$.)

## Category

**Primary: quant-ph** (Quantum Physics).

Justification: the paper's technical content is finite-dimensional operator-algebra quantum information — commutants of unitary group actions, Wedderburn decompositions, algebra-relative (generalized) entanglement in the Barnum–Knill–Ortiz–Viola/Zanardi sense, superselection rules, and Jordan–Wigner fermionic encodings. The no-go theorems are entanglement-theory results; no particle-physics phenomenology is proposed.

**Suggested cross-list: hep-th** — the paper computes the discrete analog of the Casini–Huerta–Rosabal center term and engages the lattice/continuum edge-mode literature (Donnelly, Donnelly–Wall, Kabat, Casini–Huerta–Magán–Pontello) directly; the division-algebra/Cl(6) framing is also hep-th audience material. (math-ph is a defensible optional second cross-list for the Schur/Wedderburn machinery, but quant-ph + hep-th covers the readership.)

Avoid hep-ph: no phenomenological claims are made.

## License

Recommended: arXiv's default non-exclusive license to distribute ("arXiv.org perpetual, non-exclusive license") — most journal-compatible; see the discussion in `paper/arxiv_submission/SUBMISSION.md`, which applies unchanged.

## Companion arXiv IDs — fill at announcement time

The bibliography cites four companion manuscripts (`\bibitem{companion}` = Paper 1, `\bibitem{ym2companion}` = Paper 3, `\bibitem{twoideal}` = Paper 4) as "companion paper/manuscript (2026)" without identifiers. When the companions receive arXiv identifiers at announcement, update these entries (replacement or pre-announcement edit) and cross-link the IDs in the Comments field. Suggested submission order: Paper 1 first (this paper cites its section numbers), then Papers 2–5.

## Practical submission checklist

- Upload `qio_paper2.tar.gz` as-is; verify the AutoTeX PDF preview is 22 pages.
- Metadata: paste title and abstract from this file; author "William T. Trevena".
- Comments field suggestion: "22 pages, no figures. Companion to [Paper 1 arXiv ID]. Code and raw outputs at [repository URL]."
- Endorsement: see the first-time-submitter guidance in `paper/arxiv_submission/SUBMISSION.md` (applies to quant-ph submissions from this account).
