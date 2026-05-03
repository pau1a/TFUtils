# Technofatty Codex VPS Handoff

This document is for a new Codex session working on Technofatty. The repo is synced to GitHub at `git@github.com:pau1a/TFUtils.git`.

## Current Live Baseline

Technofatty is live at:

```text
https://technofatty.com/
```

Treat the live VPS deployment as complete baseline state, not as an unfinished setup checklist.

Current deployed shape:

- App path: `/var/www/technofatty/app`
- Virtualenv: `/var/www/technofatty/venv`
- Database: PostgreSQL database `technofatty_dev`, user `technofatty`
- WSGI entrypoint: `/var/www/technofatty/app/wsgi_prod.py`
- Static root: `/var/www/technofatty/app/staticfiles`
- Apache vhosts:
  - `/etc/apache2/sites-available/technofatty.com.conf`
  - `/etc/apache2/sites-available/technofatty.com-le-ssl.conf`
- Certbot certificate: `/etc/letsencrypt/live/technofatty.com/`
- Deployment support commit: `e7ead45 Add VPS Apache and Postgres deployment support`

Do not inspect or change the VPS deployment as if it is incomplete. Future work should preserve this Apache + mod_wsgi + Postgres baseline unless the user explicitly asks to revisit deployment architecture.

## Latest Session State

The current strategic focus is AdSense revenue. Technofatty is being shaped as an AdSense-first utility/verdict site, so new work should prioritise crawlable content depth, useful admin oversight, policy-safe pages, internal linking, and shareable tools that can earn search traffic.

Recent important changes:

- A Django superuser exists for username `paula`.
- A staff-only backend tool suite has been started under `/admin-tools/`.
- The Django admin homepage now includes a native-looking `Technofatty Tools` module, alongside the normal `Authentication and Authorization` module.
- The top-right admin-tools shortcut was removed because the tools now live inside the admin body/sidebar pattern.
- Custom admin tool pages use Django admin chrome/sidebar/context rather than the public Technofatty frontend shell.
- `/admin-tools/` is now an admin tools index, not the AdSense readiness page itself.
- `/admin-tools/adsense-readiness/` is the current live AdSense Readiness Dashboard.
- The other admin tool pages have permanent queued URLs ready to be built.
- Apache was restarted after the latest admin template changes.
- Do not install or use Node on this VPS. The user explicitly does not want Node here.

Latest verified checks after the admin-tools changes:

```bash
/var/www/technofatty/venv/bin/python manage.py check
/var/www/technofatty/venv/bin/python manage.py test
sudo apache2ctl configtest
sudo systemctl restart apache2
```

The test suite was at 10 passing tests after the latest admin work.

## Current Admin Tool Suite

The backend tool suite is staff-only and should feel like Django admin, not the public frontend.

Routes:

```text
/admin-tools/                         -> Admin Tools index
/admin-tools/adsense-readiness/       -> AdSense Readiness Dashboard
/admin-tools/content-inventory/       -> queued placeholder
/admin-tools/seo-metadata/            -> queued placeholder
/admin-tools/ymyl-safety/             -> queued placeholder
/admin-tools/internal-links/          -> queued placeholder
```

Implementation files:

```text
core/views.py
core/urls.py
core/tests.py
core/templates/admin/base_site.html
core/templates/admin/index.html
core/templates/core/admin_tools/base.html
core/templates/core/admin_tools/index.html
core/templates/core/admin_tools/readiness.html
core/templates/core/admin_tools/queued.html
```

Important behaviour:

- `admin.site.each_context(request)` is merged into admin tool contexts so the normal admin sidebar and top-right user links render correctly.
- A synthetic `Technofatty Tools` app is prepended to `available_apps` for admin tool pages so the sidebar shows all five tools like native admin rows.
- `core/templates/admin/index.html` overrides the admin homepage so `Technofatty Tools` appears as a native-looking module in the main admin dashboard.
- `core/templates/admin/base_site.html` customises the admin branding/userlinks but should not add a separate top-right admin-tools shortcut.
- The AdSense Readiness placeholder scan must read files with `encoding="utf-8", errors="replace"`; using the default encoding caused a live `UnicodeDecodeError` under Apache.

Next recommended task:

> Build `/admin-tools/content-inventory/` into the real Content Inventory admin page.

That page should show every live and queued instrument, category, sitemap presence, guide/internal-link status, disclaimers, metadata/content strength signals, and direct public/admin links. Build it in the same Django-admin style, not with public frontend styling.

## Forward Plan Snapshot

Timestamp: `2026-05-03 12:15 UTC`

This plan is intentionally time-sensitive and may become stale quickly. Treat it as the best known forward direction at the timestamp above, not as a permanent roadmap.

1. Build `/admin-tools/content-inventory/` into the real Content Inventory page.
2. Build `/admin-tools/seo-metadata/` into an SEO metadata audit.
3. Build `/admin-tools/ymyl-safety/` into a health/YMYL safety audit.
4. Build `/admin-tools/internal-links/` into an internal linking audit.
5. Use those backend tools to identify thin pages, missing metadata, weak disclaimers, and poor link coverage.
6. Improve weak public pages and verdict engines based on the audit findings.
7. Verify Search Console setup and submit `https://technofatty.com/sitemap.xml` if not already done.
8. Prepare the AdSense application once the content and policy checks look credible.
9. Replace the `ads.txt` placeholder with the real Google publisher line after AdSense provides it.
10. Later, when the site is closer to launch/scale, do the final production-hardening pass.

## Project Purpose

Technofatty is a Django-based utility/verdict-engine website with the brand line:

> Questions, awkwardly answered.

The site started as a practical calculator portfolio, but the stronger direction is now broader than calculators. It should become a collection of fast, shareable instruments and verdict cards for awkward modern questions: money, home, time, social behaviour, internet nonsense, purchases, family phone rules, and similar everyday friction.

The current product direction is:

> Technofatty turns modern social nonsense into verdict cards.

The result format matters. Strong instruments should produce a score, a label, a verdict, a useful next action, and copy that people might screenshot or send to someone.

## Repo Structure

Current top-level structure:

```text
manage.py
requirements.txt
config/
core/
static/
docs/
```

Important files:

```text
config/settings.py
config/urls.py
config/wsgi.py
config/asgi.py
core/views.py
core/urls.py
core/tests.py
core/templates/core/base.html
core/templates/core/home.html
core/templates/core/calculator_detail.html
core/templates/core/calculators_index.html
core/templates/core/category_detail.html
core/templates/core/ask_podge.html
core/templates/core/about.html
core/templates/core/contact.html
core/templates/core/guide_detail.html
core/templates/core/legal.html
core/templates/core/404.html
core/templates/admin/base_site.html
core/templates/admin/index.html
core/templates/core/admin_tools/base.html
core/templates/core/admin_tools/index.html
core/templates/core/admin_tools/readiness.html
core/templates/core/admin_tools/queued.html
static/css/site.css
static/js/calculator.js
static/img/podge.svg
static/img/logo-mark.svg
static/img/favicon.svg
```

## Current Django Architecture

This is a simple Django 5.2 app.

- Project package: `config`
- Main app: `core`
- URL entrypoint: `config/urls.py`
- App routes: `core/urls.py`
- Main page/data registry: `core/views.py`
- Shared instrument template: `core/templates/core/calculator_detail.html`
- Frontend scoring and live result logic: `static/js/calculator.js`
- Site styling: `static/css/site.css`
- Staff/admin tooling templates: `core/templates/admin/` and `core/templates/core/admin_tools/`
- Tests: `core/tests.py`

The application is registry-driven. `core/views.py` contains `TOOL_REGISTRY`, category data, guide data, question prompts, and house-special entries. `calculator_detail` looks up the current tool by slug and renders the shared detail template. The template switches on `tool.calculator_type` to render the correct form. `static/js/calculator.js` switches on the same calculator type and computes the live verdict/result.

There are no database-backed content models yet. `core/models.py` is currently empty apart from the generated app scaffold. Most content is static Python dictionaries in `core/views.py`.

## Verdict Engine Interaction Rule

Verdict engines and gauges should not calculate a first result from arbitrary demo values. This applies to current and future social, behavioural, purchase, AI, internet, and awkward-life instruments.

Use this pattern:

- start with blank user-controlled inputs
- render the result panel in a neutral waiting state
- require the main button press for the first verdict
- after the first successful verdict, allow edits to live-update the result
- reset returns the tool to blank inputs, neutral result state, and no live updates until the next button press

Straight practical calculators may still use harmless example defaults and immediate live updates where that makes the arithmetic easier to understand. Examples include percentage change, VAT, room area, and days between dates.

## Share Copy Rule

Every copied result should work as a shareable Technofatty artifact, not as raw UI text. It must include the result, enough context to understand it, and a link back to the current tool so other people can get their own result.

The generic share builder in `static/js/calculator.js` should:

- prefer explicit result fields when present: `shareTitle`, `shareMetric`, `shareWhy`, and `shareNext`
- fall back gracefully to `headline`, signal labels/values, `summary`, and `detail`
- normalize punctuation so copied text does not produce doubled full stops
- use the page canonical URL when available, with `window.location.href` as fallback
- format verdict engines as `Technofatty verdict`
- format practical calculators as `Technofatty result`

Future verdict engines should define `shareNext` whenever possible, because a useful next action makes the copied verdict more sendable and more likely to bring someone back to the tool.

## Calculators And Verdict Engines Added So Far

Live instrument slugs currently covered by tests:

```text
percentage-change-calculator
vat-calculator
room-area-calculator
days-between-dates
should-i-send-that-message-gauge
main-character-risk-calculator
subscription-shame-index
vaguepost-decoder
parent-phone-hypocrisy-meter
fake-fan-detector
parental-phone-treaty-generator
fancy-version-justification-engine
future-embarrassment-gauge
sale-suspicion-gauge
astroturf-detector
algorithm-tax-calculator
ai-emotional-dependency-gauge
should-i-be-proud-of-this-plate
```

Notable verdict-style instruments:

- `Should I Send That Message Gauge`
- `Main Character Risk Calculator`
- `Subscription Shame Index`
- `Vaguepost Decoder`
- `Parent Phone Hypocrisy Meter`
- `Fake Fan Detector`
- `Parental Phone Treaty Generator`
- `Fancy Version Justification Engine`
- `Future Embarrassment Gauge`
- `Sale Suspicion Gauge`
- `Astroturf Detector`
- `Algorithm Tax Calculator`
- `AI Emotional Dependency Gauge`
- `Should I Be Proud Of This Plate?`

Template-ready placeholders also exist in the registry:

- `Recipe Scaling Instrument`
- `Water Intake Gauge`

Current queued backend/admin tools:

- `Content Inventory`
- `SEO Metadata Audit`
- `Health/YMYL Safety`
- `Internal Links`

## Exact Files Changed During Site Build

Created/changed project files:

```text
.gitignore
manage.py
requirements.txt
config/__init__.py
config/asgi.py
config/settings.py
config/urls.py
config/wsgi.py
core/__init__.py
core/admin.py
core/apps.py
core/migrations/__init__.py
core/models.py
core/tests.py
core/urls.py
core/views.py
core/templates/core/404.html
core/templates/core/about.html
core/templates/core/ask_podge.html
core/templates/core/base.html
core/templates/core/calculator_detail.html
core/templates/core/calculators_index.html
core/templates/core/category_detail.html
core/templates/core/contact.html
core/templates/core/guide_detail.html
core/templates/core/home.html
core/templates/core/legal.html
core/templates/admin/base_site.html
core/templates/admin/index.html
core/templates/core/admin_tools/base.html
core/templates/core/admin_tools/index.html
core/templates/core/admin_tools/readiness.html
core/templates/core/admin_tools/queued.html
static/css/site.css
static/img/favicon.svg
static/img/logo-mark.svg
static/img/podge.svg
static/js/calculator.js
docs/codex-handoff.md
docs/deployment-runbook.md
docs/adsense-readiness-audit.md
docs/backend-readiness-audit.md
```

The most important public instrument files are `core/views.py`, `core/templates/core/calculator_detail.html`, and `static/js/calculator.js`.

The most important backend tool files are `core/views.py`, `core/urls.py`, `core/templates/admin/index.html`, `core/templates/admin/base_site.html`, and `core/templates/core/admin_tools/`.

## Current Local Settings State

`config/settings.py` started in dev shape. The deployment support commit added the VPS-facing support needed for the live Apache/Postgres setup.

For local development, keep the project dev-friendly. For the VPS, use the established deployment files and environment expected by:

- `/var/www/technofatty/app/wsgi_prod.py`
- PostgreSQL `technofatty_dev`
- static collection into `/var/www/technofatty/app/staticfiles`

Do not treat local settings defaults as the final production hardening posture. The live deployment is internet-facing development/review, not a full production hardening pass.

## Current Deployment Baseline

Known completed deployment facts:

- The repo is synced to GitHub.
- The live domain is `https://technofatty.com/`.
- The server uses Apache, not Nginx.
- Django is served through the WSGI entrypoint at `/var/www/technofatty/app/wsgi_prod.py`.
- The app uses PostgreSQL database `technofatty_dev` with user `technofatty`.
- Static files are collected to `/var/www/technofatty/app/staticfiles` and served by Apache.
- HTTPS is in place through Certbot.
- This is still an internet-facing dev deployment, not full production yet.
- `DEBUG` can remain on temporarily until the user is ready to tighten it.
- Secrets can be revisited nearer production.
- The user wants practical cyber hygiene, but not a full production hardening pass yet.

## Decision: Apache, Not Nginx

Use Apache as the front door because that is what the VPS uses.

The current path is:

```text
Apache + mod_wsgi + Postgres + Django static files served by Apache
```

Do not switch to Nginx/Gunicorn just because many Django tutorials use that stack.

## Database Baseline

The VPS deployment uses PostgreSQL:

- Database: `technofatty_dev`
- User: `technofatty`

Keep the implementation simple. There is currently no data model beyond Django built-ins, so the migration risk is low.

## Internet-Facing Dev, Not Full Production

This deployment is intended to make the site reachable at `technofatty.com` for development/review. It is not the final production posture.

Still useful now:

- real domain routing
- Apache vhost
- Postgres
- static files served correctly
- HTTPS if available or easy to add
- firewall sanity check
- clear restart/deploy process

Acceptable temporarily:

- `DEBUG=True`
- manual deploys
- minimal monitoring
- no CI/CD
- no CDN
- no fully hardened secret management

## Deliberately Deferred Until Nearer Production

Do not spend time on these unless the user asks:

- full production hardening
- switching from Apache to Nginx
- Dockerization
- CI/CD pipeline
- CDN/object storage for static assets
- Sentry/monitoring
- advanced caching
- admin/content management system
- moving registry data into database models
- formal backup/restore automation beyond noting what should be backed up
- SEO sitemap automation
- final `DEBUG=False` hardening pass
- final secret rotation and settings split

Before public launch, revisit:

- `DEBUG=False`
- generated `SECRET_KEY` from environment
- `ALLOWED_HOSTS` for `technofatty.com` and `www.technofatty.com`
- `CSRF_TRUSTED_ORIGINS`
- HTTPS redirect settings
- secure cookies
- `STATIC_ROOT` and `collectstatic`
- Postgres backup plan
- Apache security headers
- log rotation and error logging

## Historical Pre-Deployment Checklist

This section is superseded. It records the checklist that was used before Technofatty went live. Do not treat it as current next steps.

1. SSH into the VPS.
2. Inspect Apache, Python, Postgres, and vhost state using the commands below.
3. Confirm how Apache currently serves Python.
4. Clone or update the repo from GitHub.
5. Create a venv for Technofatty.
6. Install requirements.
7. Add Postgres driver and update repo requirements.
8. Create Postgres DB/user.
9. Patch Django settings for env-driven Postgres while preserving dev-friendly `DEBUG` behaviour.
10. Add `STATIC_ROOT` so static assets can be collected.
11. Run `manage.py check`.
12. Run `manage.py migrate`.
13. Run `manage.py collectstatic`.
14. Configure Apache vhost for `technofatty.com`.
15. Confirm DNS points to the VPS.
16. Restart/reload Apache.
17. Test local server response from the VPS.
18. Test `http://technofatty.com/` externally.
19. Add HTTPS with the server's existing Certbot/Apache process if present.

## Historical First Commands For Initial VPS Inspection

This section is superseded. These commands were for the initial deployment inspection, not for routine future work.

Run these before changing anything:

```bash
pwd
whoami
hostname
uname -a
lsb_release -a
```

Inspect Apache:

```bash
apachectl -v
apachectl -M
apachectl -S
systemctl status apache2 --no-pager
ls -la /etc/apache2/sites-available
ls -la /etc/apache2/sites-enabled
```

Check how Python web apps may already be served:

```bash
ps aux | egrep 'apache|httpd|wsgi|uwsgi|gunicorn|daphne|uvicorn'
apachectl -M | egrep 'wsgi|proxy|ssl|headers|rewrite'
```

Inspect Python:

```bash
python3 --version
which python3
python3 -m pip --version
python3 -m venv --help
```

Inspect Postgres:

```bash
psql --version
systemctl status postgresql --no-pager
sudo -u postgres psql -c '\l'
sudo -u postgres psql -c '\du'
```

Inspect current web roots and likely deployment locations:

```bash
ls -la /var/www
ls -la /srv
find /etc/apache2/sites-enabled -maxdepth 1 -type l -print
```

Inspect DNS and network basics from the VPS:

```bash
hostname -I
curl -I http://127.0.0.1
curl -I http://technofatty.com
curl -I http://www.technofatty.com
```

Check whether Certbot is already installed:

```bash
certbot --version
ls -la /etc/letsencrypt/live
```

## Historical Apache Shape Used For Planning

This planning section is superseded by the live Apache vhosts listed in Current Live Baseline.

The original expected vhost ingredients were:

```apache
ServerName technofatty.com
ServerAlias www.technofatty.com

WSGIDaemonProcess technofatty python-home=/srv/technofatty/venv python-path=/srv/technofatty/app
WSGIProcessGroup technofatty
WSGIScriptAlias / /srv/technofatty/app/config/wsgi.py

Alias /static/ /srv/technofatty/app/staticfiles/

<Directory /srv/technofatty/app/config>
    <Files wsgi.py>
        Require all granted
    </Files>
</Directory>

<Directory /srv/technofatty/app/staticfiles>
    Require all granted
</Directory>
```

The live deployment uses `/var/www/technofatty/app`, not `/srv/technofatty/app`.

## Useful Django Commands

From `/var/www/technofatty/app` on the VPS:

```bash
/var/www/technofatty/venv/bin/python manage.py check
/var/www/technofatty/venv/bin/python manage.py migrate
/var/www/technofatty/venv/bin/python manage.py collectstatic
```

For commands that need the live Postgres environment, source `.env` first because `manage.py` does not load it by itself:

```bash
set -a
. /var/www/technofatty/app/.env
set +a
/var/www/technofatty/venv/bin/python manage.py check
```

Use the established VPS environment and `wsgi_prod.py` deployment shape when running deployment checks.

## Current Local Verification

Before this handoff, the local app had recently passed:

```bash
.venv/bin/python manage.py check
.venv/bin/python manage.py test
```

The most recent direct route checks included:

```text
/admin/ -> redirects anonymous users to login
/admin-tools/ -> redirects anonymous users to login
/admin-tools/adsense-readiness/ -> redirects anonymous users to login
```

## Cautions For The VPS Session

- Treat the live deployment as baseline.
- Do not change Apache, Postgres, Certbot, or WSGI setup unless the user asks.
- Do not assume Nginx or Gunicorn.
- Do not delete existing Apache configs.
- Avoid broad production refactors unless needed for a requested change.
- Keep deployment changes small enough that the site can be debugged with normal Apache, Django, and Postgres logs.
