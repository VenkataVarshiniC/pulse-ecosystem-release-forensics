# Pilot privacy protocol

## Anonymous identity

Use only `T01`, `T02`, and `T03`. Do not map these IDs to Wave 1/Wave 2 respondent IDs in the repository.

## Never commit

- names, email addresses, phone numbers, usernames, or contact records;
- employer, team, customer, or client identity;
- private repository, package, incident, ticket, or system details;
- credentials, tokens, connection strings, or access instructions;
- audio, video, screen recordings, transcripts, or scheduling metadata;
- timestamps precise enough to identify a participant when not analytically necessary;
- identifiable verbatim free text.

## Local handling

If consented recordings or raw notes exist outside the repository, store them only in an approved local ignored location with access restricted to the study owner. Do not place them under tracked paths. Record retention and deletion decisions outside the committed analysis.

## Committed result handling

Commit only coded task outcomes, sanitized evidence references, and short de-identified statements. If identity cannot be ruled out, paraphrase and label the entry `ANALYST_PARAPHRASE`. Record session date at day grain only if needed. Never infer employer, seniority, or authority from a job title alone.

If private information is disclosed during a session, stop that line of discussion, omit it from study notes, and record only `PRIVATE_DETAIL_WITHHELD` if the omission affects interpretation.
