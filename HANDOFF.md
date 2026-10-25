# Conversation handoff

This is a summary of the project conversation, not a verbatim chat export. Give this file to the assistant when continuing on another computer.

## User's request
Build a private website/dashboard tracking daily BAR for today and the next seven nights (eight stay dates), refreshed daily, for these hotels:

Owned hotels:
- Hotel Don Fernando de Taos
- Hampton Inn Taos

Competitors:
- Sagebrush Inn
- Hotel Willa
- El Monte Sagrado
- Historic Taos Inn
- Taos Valley Lodge
- Super 8 Taos

User confirmed BAR means the lowest public flexible rate for one room, two adults, one night, before taxes, excluding member and prepaid offers. Currency: USD. Calendar timezone: America/Denver.

User currently checks individual hotel booking sites directly, rather than using a rate-shopping provider. Keep explanations simple and concrete.

## What happened
The GitHub repository tbag-ryker/comps was initially empty. Git read access worked. We created a Python standard-library web app and pushed the initial implementation to main, commit 9445b1b.

Implemented:
- Password login with HTTP-only session cookies and eight-hour sessions.
- Eight hotels by eight stay dates.
- Manual rate entry with availability status, source and checked timestamp.
- SQLite persistence, old-observation highlighting and CSV export.
- Distinct missing, sold-out and rate-unavailable states.
- No invented/sample hotel prices.

Verified with an isolated temporary database: unauthorized API requests are rejected, login works, eight hotels/eight dates are returned, a rate can be saved and read, and logout removes access. Python compilation passed. Browser rendering was not tested.

## Booking links supplied by user
Property-to-link mapping remains unknown. Do not guess it.

1. https://hotels.cloudbeds.com/en/reservation/RZWfvZ?currency=usd
2. https://be.synxis.com/?chain=17123&hotel=67117&adult=2&rooms=1&currency=USD
3. https://be.synxis.com/?chain=17448&hotel=44982&adult=2&rooms=1&currency=USD

The supplied SynXis links originally specified adult=1 and arrival 2026-10-25/departure 2026-10-26. The links above omit tracking/date parameters and use the user's confirmed two-adult basis. Future searches must calculate current stay dates, not reuse the old dates.

All three booking-page requests failed at the workspace egress proxy with Tunnel connection failed: 403 Forbidden. No hotel identities, rate parsing or live rates were verified.

## Cloud configuration
A configuration draft was saved with allowed custom network domains hotels.cloudbeds.com and be.synxis.com, plus startup instructions. The tool confirmed persistence and requires_publish=true. User was told to review/save in environment settings and publish. Runtime application and publication were not confirmed. Git pushes do not publish this cloud configuration or deploy the website.

## Running locally
Python 3.12+; no external dependencies. See README.md. Set DASHBOARD_PASSWORD securely to at least 16 characters, then run python app.py from the checkout. Default listener is 127.0.0.1:8000. Do not commit passwords, .env files or the rate database. Database observations and runtime sessions are not included in Git.

Each cloud task is already isolated: use the existing checkout, and do not create a worktree unless explicitly requested.

## Outstanding work
1. Get property names for the three supplied links and the remaining five booking links, or independently verify them once access works.
2. Retry booking access after network configuration changes. Investigate each booking engine's supported access and actual flexible-rate/cancellation data before implementing collectors.
3. Implement and verify live collection for eight hotels and eight single-night stays, and daily scheduling. Neither is currently implemented.
4. Configure private HTTPS hosting and access control. Current Python server is a development implementation; remote production hosting, login rate limiting and HTTPS reverse proxy are not configured.
5. Add appropriate browser and collector validation. Retain honest missing/error states when collection fails.

The website is not deployed and does not yet automatically track BAR. Manual entry works. User's overall request remains incomplete until live collection, daily refresh and private deployment are working.

## Continuing elsewhere
Clone https://github.com/tbag-ryker/comps and ask the assistant to read HANDOFF.md and README.md, inspect the current files, and continue the outstanding work. The actual ChatGPT conversation is available through the user's account history when signed into the same account; this repository file supplies project context if starting a new chat.
