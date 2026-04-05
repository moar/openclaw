# Research Notes

- Focus on Portuguese content-publishing websites in these fixed categories only: Business, Tech, Lifestyle, Travel, Finance, Cooking, Sports.
- Prefer official website contact/about/ficha técnica pages for email capture.
- If only a contact form exists, leave contact_email blank and set has_email=no.
- Track contact_method as one of: email, form, both, unknown.
- Skip sites that are clearly blocked, broken, or directory-style junk instead of trying to bypass protections.
- DuckDuckGo search was intermittently bot-challenged during this run, so direct verification of known Portuguese publisher domains remains the fallback.
- If a dedicated contact/about page is missing or blocked but the official homepage clearly exposes a relevant mailto link in site navigation/footer, that homepage-level email can be used; avoid scraping emails that only appear inside article bodies or third-party embeds.
- When a site exposes multiple valid emails, prefer a general editorial/commercial inbox over personal addresses for outreach seeding.
- Current bottlenecks: repeated search challenges, SAPO rate-limiting on some sections, several Portuguese media sites sitting behind Cloudflare/JS gates, and some contact details exposed only via images or obfuscated anti-spam widgets. In those cases, keep only verifiable rows and use unknown/form instead of guessing an email.
- Additional working pattern: when search is degraded, use established Portuguese publisher families and append stable topic/category URLs only if the URL resolves cleanly and is not already present in the CSV. Skip category URLs that collapse into a single article, image asset, or hard 403 wall.
- New practical shortcut: when official contact pages use Cloudflare email obfuscation, decode only the site-owned data-cfemail values from the publisher’s own contact/ficha-técnica pages to recover verifiable editorial/commercial inboxes. If no suitable outreach inbox is exposed, prefer form/unknown rather than using privacy/subscriber addresses.
