# Wave 2 trust and uncertainty analysis

## Direct evidence

- Lack of trust is an adoption barrier for 9/14, including 4/5 additions.
- Trust inputs are CI/test evidence 8/14; version information, history, and explanation 7/14 each; original links 6/14; missing-evidence indication and related issue/PR 5/14 each.
- Traceability mean is 4.07/5; 10/14 rate it 4 or 5.
- Output preferences are likely answer plus explicit uncertainty 4/14, confidence score 3/14, explicit UNKNOWN 3/14, and non-reliance 4/14.
- Among additions, two prefer explicit UNKNOWN, two would not rely on automation, and one prefers confidence. No addition chose likely-answer-plus-uncertainty.
- False positives are a barrier for 5/14 and review burden for 4/14.

## Interpretation

Wave 2 strengthens alignment with explicit missingness and also strengthens automation skepticism. It does not establish one preferred user interface. Confidence scores, explicit UNKNOWN, tentative guidance, and refusal to rely are distinct positions and must not be merged into a single “uncertainty preference.”

PULSE must preserve:

- `UNKNOWN != NO`;
- missing evidence is not negative evidence;
- confidence cannot upgrade an unsupported finding;
- a declaration is not installed-version or compatibility proof;
- a candidate is not an accepted incident;
- human review is not automatically useful at every volume.

A future task-based study may compare unchanged UNKNOWN findings with separately labeled analyst hypotheses or confidence aids. It must test comprehension, calibration, evidence navigation, and whether the aid changes action. Wave 2 does not authorize probabilistic findings.

## Boundary

No respondent inspected a PULSE evidence chain or used the product to make a decision. These are preference and problem signals, not implementation validation.
