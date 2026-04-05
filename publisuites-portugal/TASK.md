# Publisuites Portugal Batch Task

## Goal
Append verified Portuguese content-publishing websites to `publisuites-portugal/leads.csv` for later paid article outreach.

## Fixed categories
- Business
- Tech
- Lifestyle
- Travel
- Finance
- Cooking
- Sports

## Non-negotiable rules
- **Append-only:** never truncate, overwrite, replace, or rebuild `leads.csv`.
- **Preserve existing rows exactly:** every existing row must remain.
- **No duplicate websites:** do not add any website already present in `leads.csv`.
- **Normalize for duplicate checks:** compare URLs after normalizing scheme, trailing slash, and obvious `www.` variants so near-duplicates are skipped too.
- **No speculative rows:** only add a row when the site is a real Portuguese content publisher and the category is justified.
- **Source-backed contacts only:**
  - `contact_email` may be filled only when an official site/about/contact/ficha técnica/commercial page clearly exposes the email.
  - `has_email` may be `yes` only if a real email was found and recorded.
  - If no email is found, leave `contact_email` blank and set `has_email=no`.
  - Use `contact_method=form` only when an official form is present and no email is visible.
  - Use `contact_method=unknown` only as a last resort when the publisher is real but no contact route could be verified.
- **No fake completion:** do not pad the file with weak/duplicate rows to hit a numeric target.
- **Skip protected/inaccessible pages:** do not fight anti-bot systems.
- **Avoid duplicates:** compare against all existing `web_url` values before appending.
- **Quality first:** prefer mid-size / easier-to-approach publishers.

## Discovery method
- Use `brave_search.py` in this folder for candidate discovery when useful.
- Prefer broader Portuguese-language discovery queries and then filter candidates by relevance, country, category, and publisher quality.
- Before appending any candidate, compare against the existing CSV and skip anything already present.
- Do not rely on Google Custom Search.

## Per-run target
At the start of each run:
1. Read the existing CSV and count current leads (excluding header).
2. Append **up to 50 new clean leads**.
3. If fewer than 50 high-quality new leads can be found, stop early and explain why.
4. **Do not** change or remove any existing rows.

## Required columns
- `web_url`
- `topic`
- `contact_email`
- `has_email`
- `contact_method`

## contact_method values
- `email`
- `form`
- `both`
- `unknown`

## Output requirements
When the run finishes, report:
- start count
- number of new leads added
- final total count
- bottlenecks encountered
- suggested next focus areas
- whether any existing rows were skipped as duplicates (and how many)
