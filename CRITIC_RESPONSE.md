# Response to Adversarial Review (Round 1, 2026-06-09)

Referee report: independent agent, full re-derivation with independent octonion
table. Disposition of every issue. The revision also adopts a global reframing:
the paper is now titled and structured as a no-go/cartography study ("Is the
SM coupling hierarchy encoded in three-qubit vacuum entanglement?"), with the
QIO demoted to a named motivating heuristic.

## Major issues

- **M1 (unsigned-variant claim false; second Hermiticity bug).** Accepted.
  `exp6` rebuilt operators from the unsigned table → anti-Hermitian matrix →
  `eigh` garbage. Fixed: couplings +1 with true operators; result is a unique
  ENTANGLED hierarchical vacuum S ≈ (0.577, 0.472, 0.327), τ₃ ≈ 4/49
  (verified by us and by the referee independently). All "signs are
  necessary / separable" claims removed from abstract, contributions, Secs
  8.2, 11, 12; replaced by "signs necessary for the symmetric,
  convention-invariant vacuum, not for entanglement." Failure mode disclosed
  in Sec 8.2.
- **M2 (91% grid artifact; A ≳ 106 wrong).** Accepted and verified (31.7% /
  13.0% on larger grids). All "91%" and "A ≳ 106" claims removed. Only the
  robust statement remains: box |B| ≥ ~51, polygon |B| ≳ 126.5 (stable to
  grid and UV endpoint).
- **M3 (constraints bind at M_Z alone; flow adds no restrictive power).**
  Accepted and verified (feasible sets identical, 1401 = 1401, set equality).
  Sec 7.2 now states both deflations explicitly, credited to adversarial
  review. Honesty clause rewritten: the map is "the unique surviving affine
  form," not evidence.
- **M4 (closed form H = i(L_u + 2R_u); invariance provable; canonicity
  weaker).** Accepted and verified (‖H − i(L_u+2R_u)‖ = 0). Sec 8.2 now
  derives the spectrum and vacuum from the closed form; Sec 8.3 presents the
  battery as confirmation of a provable statement; the û-dependence (other
  preferred directions give separable vacua) is stated; "the algebra selects"
  weakened to "algebra plus factorization frame selects."
- **M5 (CKW balance definitional).** Accepted. All "exactly balancing the
  monogamy budget" language removed; only the equal three-way split 8/49 is
  claimed as special, attributed to permutation symmetry + marginal spectrum.
- **M6 (gauge-frame + abelian normalization undermine Secs 5–8; 7.3/10.3
  tension).** Accepted. New normalization caveat in Sec 7.3 (5/3 is a GUT
  convention; r_SM, crossings, ΔS_min all convention-dependent); interior-μ*
  awkwardness stated; Sec 10.3 rewritten to confront the tension; the
  gauge-covariance obstruction promoted to the paper's capstone (title,
  abstract, intro, conclusion). The referee's constructive remark (rotor
  boundary fixes A + 0.5917B = α*⁻¹) was checked: the referee's arithmetic
  was off (A=118, B=−126.5 ↔ α*⁻¹ = 43.15, not ≈ 25), and the relation is
  satisfiable for every α*⁻¹ ∈ [20, 50] — i.e., unconstraining. Recorded as
  such in Sec 7.3.
- **M7 (missing literature).** Accepted. Added: Borsten et al. Phys. Rep. 471
  (2009) [44] with delimitation paragraphs in Secs 2.1 and 8.2; Stoica [45]
  and softened "open problem resolved" → "standard mathematics made explicit"
  in Sec 9.1; Zanardi [46] and Barnum-Knill-Ortiz-Viola [47] in Sec 9.3;
  Harvey [48] in Sec 8.2.

## Minor issues (all fixed)

1. Mid-band corrected to ≈ 0.47–0.87. 2. Equations renumbered (4)–(6), gap
removed. 3. Sawicki-Walter-Kuś now ref [43]. 4. [29] single-author Favalli;
in-text Moreva 2014; [37] cited as PRL 134, 240001. 5. Match-rate run
provenance noted in Control C. 6. Concurrence-shift claim softened
("gap-matched control would be needed... we have not constructed one").
7. Kempe/LU invariants explicitly deferred. 8. "only 16.4% / only 0.9%"
re-phrased as consistent with chance/Haar rates. 9. Sec 6.2 non-sequitur
fixed (convention-independence attributed to Sec 8.3 + referee's independent
table). 10. exp6 docstring and GL(3,2) check fixed. 11. Sec 8.3 notes
invariance is provable; battery is a code check. 12. Sec 4.3 "high
confidence" qualified by Sec 3.4's conditional sense.

## Verified-correct items (no change needed)

All RG numbers, crossings, ΔS values, |B| bounds, rotor invariants
(spectrum, vacuum, (1/7, 6/7), 8/49, 2√2/7), weighted-W curve, Exp 1/Controls
statistics, JW/CAR/charge/color-DFT results, two-qubit minimality, polygon
example — independently reproduced by the referee from an independent
octonion table.
