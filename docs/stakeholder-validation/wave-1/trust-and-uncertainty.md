# Wave 1 trust and uncertainty analysis

## Direct response evidence

- Trust prerequisites were distributed across CI/test evidence 5/9, dependency-version information 5/9, historical state 5/9, explanation 4/9, original links 3/9, missing-evidence indication 3/9, related PRs/commits 3/9 each, human review 2/9, and confidence level 1/9.
- Traceability importance was mean 4.11/5 and median 4/5; 7/9 rated it 4 or 5.
- Lack of trust was a barrier for 5/9, false positives for 4/9, and excessive human review for 3/9.
- Insufficient-evidence output preferences were 4/9 likely answer plus explicit uncertainty, 2/9 confidence score, 2/9 no reliance on automation, and 1/9 explicit UNKNOWN.

## Analyst interpretation

Wave 1 aligns strongly with PULSE’s explicit provenance and evidence-qualification approach. It also supports keeping missingness visible. It does **not** uniformly prefer the current strict UNKNOWN presentation: five respondents explicitly want uncertainty or UNKNOWN visible, but four of those also want a tentative answer. Two prefer a confidence score, which can signal uncertainty but is not equivalent to UNKNOWN. Two would not rely on automated conclusions at all.

PULSE must preserve these semantic boundaries:

- `UNKNOWN != NO`;
- missing evidence is not negative evidence;
- a dependency declaration is not installed-version or compatibility proof;
- an automated candidate is not an accepted incident;
- a confidence score cannot upgrade an unsupported finding.

A future presentation experiment may show an explicitly labeled analyst hypothesis beside an unchanged UNKNOWN finding. That would require separate governance, calibration, and comprehension testing. Wave 1 does not authorize probabilistic findings or relaxed bounded-NO prerequisites.

## Alignment limits

The survey indicates respondent preferences; it does not prove that PULSE’s implementation is understandable or correct. No respondent inspected a PULSE evidence chain, reproduced a finding, or made a real decision with the product. Provenance is therefore preference-aligned, while usability and decision reliance remain unvalidated.
