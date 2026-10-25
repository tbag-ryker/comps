# Taos Rate Desk
Private rate observation dashboard for two owned hotels and six competitors. Python 3.12+, no external dependencies.

## Run
Set `DASHBOARD_PASSWORD` securely to a password of at least 16 characters, then run `python app.py` from this directory. Default bind: 127.0.0.1:8000. SQLite observations persist in `rates.sqlite3`; override with `RATES_DB`. Dates follow America/Denver.

For remote use, deploy behind an HTTPS reverse proxy and access control (for example an identity-aware proxy), set `COOKIE_SECURE=1`, and keep the Python service private. Production hosting and login rate limiting are not configured here. Sessions expire after eight hours and reset on server restart.

## Rates
Today plus seven nights. Default comparison is USD, one room, two adults, one night, lowest public flexible BAR before taxes, excluding member and prepaid offers. Verify cancellation terms and room eligibility at the source before recording a rate. Missing, sold-out, and unavailable observations are distinct. Previous-day observations are marked amber. Manual entry and CSV export work; live collection and scheduled daily updates require a licensed provider or approved booking integration and are not yet connected. No sample rates are presented as real prices.

Source and collection timestamp are stored for each observation. Saving replaces that hotel's observation for the stay date; historical audit trails are not implemented.
