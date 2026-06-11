# arXiv Submission Package — Paper 3

## Package

`qio_paper3.tar.gz` — upload this file directly on the arXiv submission page.

Contents (verified self-contained; clean-room compile from the tarball: 0 errors, 0 undefined references, 22 pages, zero Type 3 fonts):

| File | Purpose |
|---|---|
| `main.tex` | Complete manuscript (series-wired version, June 2026: companion bibliography entries carry the final titles). Bibliography embedded as `thebibliography`; no `.bbl`/`.bib` needed. |
| `fig_ym2.png` | Figure 1 (U(1)/SU(2) entropy, Fisher information, inversion, MLE demo). |
| `fig_su3.png` | Figure 2 (SU(3) extension and n-interval analysis). |

No custom style files (standard `article` class with geometry, fontenc/lmodern, amsmath, amssymb, graphicx, hyperref). arXiv AutoTeX runs pdflatex; PNG figures are handled natively.

## Title

Fisher Information and Coupling Reconstruction from Edge-Sector Statistics in Two-Dimensional Yang--Mills

## Abstract (plain text, 1,914 characters — within arXiv's 1,920 limit)

The edge-sector distribution of two-dimensional Yang-Mills theory is an exponential family; therefore its entropy derivative, its Fisher information, and the sensitivity of coupling estimation are exactly linked. For a compact connected Lie gauge group G in the heat-kernel formulation on a sphere, the Hartle-Hawking state assigns to the boundary electric flux R at an entangling cut the probability p_R(t) proportional to (dim R)^2 exp(-(t/2)C_2(R)), t = g^2 A -- a one-parameter exponential family with sufficient statistic the quadratic Casimir. The formulas are known (Donnelly; Gromov-Santos); our contribution is the estimation-theoretic reading of them, stated as theorems, plus the explicit SU(3)/capacity/n-interval analysis. Three exact statements: (i) dS/dt = -(t/4)Var_t(C_2) < 0; (ii) the Fisher information of the flux measurement is I(t) = (1/4)Var_t(C_2) and equals the quantum Fisher information, so dS/dt = -t I(t): entropy susceptibility and statistical reconstructability are the same function of the coupling; (iii) the capacity of entanglement is C(t) = t^2 I(t) -> (1/2) dim G as t -> 0, and S(t) = (1/2) dim G ln(1/t) + c_G + o(1). An observer sampling the boundary flux N times estimates t at the Cramer-Rao limit: for U(1), SU(2), and SU(3) the coupling is recovered to 1.6% from 10^3 samples and 0.5% from 10^4 at t = 1. With n intervals the entropy grows linearly in n through the edge term, but the Fisher information does not grow at all: the flux at every cut is one global random variable. We state precisely why this is reconstruction within a presupposed theory, not determination of the coupling by entanglement: the inference inverts a known one-parameter family; only g^2 A is recoverable; the edge term carrying the signal is contested as entanglement; and no claim is made about four-dimensional QCD. We close with a checklist for future "coupling from entanglement" claims.

(arXiv metadata accepts UTF-8; if any character is rejected, replace with inline TeX. The TeX abstract in `main.tex` is the authoritative full version.)

## Category

**Primary: hep-th** (High Energy Physics – Theory).

Justification: the subject is entanglement entropy and edge modes in two-dimensional Yang–Mills theory — a hep-th core topic, building directly on Donnelly, Gromov–Santos, Casini–Huerta–Rosabal, Donnelly–Wall, and the 2d YM exact-solvability literature (Migdal, Rusakov, Witten). The new content (exact entropy/Fisher identities for the flux-sector family, capacity of entanglement, n-interval scaling) lives in that literature's home category.

**Suggested cross-lists:**
- **quant-ph**: the estimation-theoretic core — Fisher information, quantum Fisher information, Cramér–Rao saturation, MLE bias — is quantum-information methodology, and the paper's companion papers sit in quant-ph.
- **math-ph**: the results are exact identities for heat-kernel exponential families over the unitary dual of a compact group, with explicit hypotheses and proofs.

Avoid hep-lat (no lattice computation here — the theory is exactly solved) and hep-ph (no phenomenology).

## License

Recommended: arXiv's default non-exclusive license to distribute ("arXiv.org perpetual, non-exclusive license") — most journal-compatible; see the discussion in `paper/arxiv_submission/SUBMISSION.md`, which applies unchanged.

## Companion arXiv IDs — fill at announcement time

The bibliography cites three companion manuscripts (`\bibitem{P1}` = Paper 1, `\bibitem{P2}` = Paper 2, `\bibitem{u1fourd}` = Paper 5) as "companion paper/manuscript (2026)" without identifiers. When the companions receive arXiv identifiers at announcement, update these entries and cross-link the IDs in the Comments field.

## Practical submission checklist

- Upload `qio_paper3.tar.gz` as-is; verify the AutoTeX PDF preview is 22 pages with both figures rendered.
- Metadata: paste title and abstract from this file; author "William T. Trevena".
- Comments field suggestion: "22 pages, 2 figures. Companion to [Paper 1/2 arXiv IDs]. Code and raw outputs at [repository URL]."
- Endorsement: first submission to hep-th may require endorsement; the guidance in `paper/arxiv_submission/SUBMISSION.md` applies, with hep-th authors (e.g. in the 2d YM entanglement literature) as natural endorsers.
