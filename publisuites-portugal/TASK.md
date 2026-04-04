# Publisuites Portugal Batch Task

## Goal
Expand `publisuites-portugal/leads.csv` with Portuguese content-publishing websites suitable for later paid article outreach.

## Fixed categories
- Business
- Tech
- Lifestyle
- Travel
- Finance
- Cooking
- Sports

## Constraints
- Prefer mid-size / easier-to-approach publishers.
- Continue from the existing CSV; never replace it.
- Avoid duplicates against all existing rows.
- Prefer official contact/about/ficha-tecnica/commercial pages for email confirmation.
- Skip bot-protected or inaccessible pages instead of fighting anti-bot systems.
- Update `notes.md` if methodology changes or bottlenecks appear.

## Discovery method
- Use `brave_search.py` in this folder for candidate discovery when useful.
- Prefer broader Portuguese-language discovery queries and then filter candidates by relevance, country, category, and publisher quality.
- Do not rely on Google Custom Search.

## Per-run target
At the start of each run:
1. Read the existing CSV and count current leads (excluding header).
2. Set `target_total = start_count + 50`.
3. Keep researching and appending clean new rows until one of these happens:
   - `target_total` is reached, or
   - a hard runtime/tool/access blocker prevents further high-quality additions.
4. If you stop before reaching `target_total`, clearly report the shortfall and why.

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
