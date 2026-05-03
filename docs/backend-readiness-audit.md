# Technofatty Backend Readiness Audit

Date: 2026-05-03

## Verdict

The backend is good enough for the current internet-facing dev deployment, but it is not perfect or fully production-hardened yet.

The main site is live, Apache/mod_wsgi is serving Django, PostgreSQL is the intended live database, HTTPS is in place, static files are served by Apache, and Django checks/tests pass. The remaining gaps are mostly production hardening and operational discipline.

## Fixed In The Latest Backend Pass

- `config/settings.py` now supports environment-driven:
  - `DJANGO_DEBUG`
  - `DJANGO_SECRET_KEY`
  - `DJANGO_ALLOWED_HOSTS`
  - `DJANGO_CSRF_TRUSTED_ORIGINS`
  - secure cookie settings
  - HTTPS redirect and HSTS settings
- `CSRF_TRUSTED_ORIGINS` is set for `technofatty.com` and `www.technofatty.com`.
- `SECURE_PROXY_SSL_HEADER` is set for Apache/proxy HTTPS awareness.
- `SESSION_COOKIE_SECURE` and `CSRF_COOKIE_SECURE` default to secure when `DJANGO_DEBUG=0`.
- `docs/deployment-runbook.md` now makes it explicit that `.env` must be sourced before `manage.py` commands when operating against live VPS settings.
- A production-like `manage.py check --deploy` passes when run with `DJANGO_DEBUG=0`, a strong temporary secret, HTTPS redirect, HSTS, and HSTS preload enabled.

## Current Known Gaps

1. `DJANGO_DEBUG=1` is still intentionally set for the current internet-facing dev deployment.

   This is acceptable for the stated current phase, but should be changed before a real production launch.

2. The fallback `SECRET_KEY` in `settings.py` is still the original development key.

   Production safety depends on setting `DJANGO_SECRET_KEY` in `.env`. Before production, generate a long random secret and set it server-side.

3. Plain `manage.py` does not automatically load `.env`.

   This is now documented in the runbook. Source `.env` before live `check`, `migrate`, and `collectstatic` commands.

4. Final secure settings are not enabled yet.

   Before production, set and verify:

   ```text
   DJANGO_DEBUG=0
   DJANGO_SECRET_KEY=<long random secret>
   DJANGO_SECURE_SSL_REDIRECT=1
   DJANGO_SECURE_HSTS_SECONDS=31536000
   DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS=1
   DJANGO_SECURE_HSTS_PRELOAD=1
   ```

5. Backup/restore is not formalised.

   PostgreSQL backup and restore procedure should be documented before the site becomes valuable.

6. Logging/monitoring is minimal.

   Apache and Django errors can be debugged with normal logs, but there is no Sentry, uptime monitor, or alerting yet.

7. No CI/CD.

   Manual deployment is fine for now, but the process depends on careful commands.

## Backend Checks Run

Current dev-mode checks:

```text
manage.py check: OK
manage.py test: OK
```

Production-like Django deployment check:

```text
DJANGO_DEBUG=0 ... manage.py check --deploy: OK
```

The production-like check used a temporary strong secret for validation only. Do not reuse that value as a real secret.

## Production Hardening Trigger

Do the final hardening pass when the site is ready to apply for ads seriously or when user traffic starts to matter.

At that point:

- set `DJANGO_DEBUG=0`
- set a real `DJANGO_SECRET_KEY`
- verify PostgreSQL credentials are real and not placeholders
- run migrations with `.env` sourced
- run `check --deploy`
- verify HTTPS redirects
- confirm secure cookies
- confirm HSTS behaviour
- document backups
- review Apache logs and error handling

