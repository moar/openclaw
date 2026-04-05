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
- Treat rows with `unknown` contact_method as candidates for later manual cleanup.
