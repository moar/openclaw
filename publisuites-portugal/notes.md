# Research Notes

- Focus is Portugal-only content publishers suitable for paid article outreach.
- Use fixed categories only: Business, Tech, Lifestyle, Travel, Finance, Cooking, Sports.
- Prefer official contact/about/ficha técnica/commercial pages for email verification.
- If no email exists, leave it blank and set `has_email=no`.
- `contact_method=form` is allowed only when an official form is visible and no email is found.
- `contact_method=unknown` is a fallback, not a default.
- Never rebuild or overwrite the CSV; append only.
- Skip bot-protected / inaccessible pages rather than forcing extraction.
- Brave Search is the current discovery source; broader Portuguese queries work better than narrow `site:` searches.
- Discovery must be duplicate-aware: compare normalized URLs against existing `leads.csv` before appending.
- Treat rows with `unknown` contact_method as candidates for later manual cleanup.
- Separate cleanup passes may be used to improve existing rows, but they must not remove good rows or overwrite the CSV.
- Batch runs should target 50 new pages per run unless blocked; small batches are only acceptable when the task explicitly reports the shortfall and cause.
- Prefer mid-sized, independent, and regional publishers; treat major national brands as fallback inventory rather than the default target pool.
