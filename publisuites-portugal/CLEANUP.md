# Publisuites Portugal CSV Cleanup

## Goal
Improve the quality of `publisuites-portugal/leads.csv` without changing the append-only sourcing workflow.

## Objectives
- Review rows with `contact_method=unknown` first.
- Try to verify a real official contact page or contact email for those publishers.
- If a row cannot be verified, keep it but flag it as a later manual-review candidate in notes.
- Do not remove good rows.
- Do not overwrite the CSV.

## Priority rules
1. Fix rows with known official contact routes but missing email/form metadata.
2. Verify `contact_method=form` rows to see if an email is also available on official pages.
3. Leave clearly valid rows alone.
4. If a site is inaccessible or bot-protected, skip it.

## Output
- Cleaned metadata where a better official contact route can be confirmed.
- A short summary of what was improved and what still needs manual review.
