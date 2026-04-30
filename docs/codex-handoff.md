# Technofatty Codex VPS Handoff

This document is for a new Codex session running on the VPS. The local repo has been synced to GitHub at `git@github.com:pau1a/TFUtils.git`.

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
- Tests: `core/tests.py`

The application is registry-driven. `core/views.py` contains `TOOL_REGISTRY`, category data, guide data, question prompts, and house-special entries. `calculator_detail` looks up the current tool by slug and renders the shared detail template. The template switches on `tool.calculator_type` to render the correct form. `static/js/calculator.js` switches on the same calculator type and computes the live verdict/result.

There are no database-backed content models yet. `core/models.py` is currently empty apart from the generated app scaffold. Most content is static Python dictionaries in `core/views.py`.

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

Template-ready placeholders also exist in the registry:

- `Recipe Scaling Instrument`
- `Water Intake Gauge`

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
static/css/site.css
static/img/favicon.svg
static/img/logo-mark.svg
static/img/podge.svg
static/js/calculator.js
docs/codex-handoff.md
```

The most important implementation files are `core/views.py`, `core/templates/core/calculator_detail.html`, and `static/js/calculator.js`.

## Current Local Settings State

`config/settings.py` is still in dev shape:

- `DEBUG = True`
- `SECRET_KEY` is hardcoded
- `ALLOWED_HOSTS = ["localhost", "127.0.0.1", "testserver"]`
- database is SQLite at `BASE_DIR / "db.sqlite3"`
- `STATIC_URL = "static/"`
- `STATICFILES_DIRS = [BASE_DIR / "static"]`
- no `STATIC_ROOT` yet
- no Postgres driver dependency yet
- no Apache-specific deployment config yet

This is intentional for the current phase. Do not treat the local settings file as production-hardened.

## Current Deployment Assumptions

The next session will run on the VPS and should inspect the actual server before changing anything.

Known assumptions from the conversation:

- The repo is synced to GitHub.
- The target domain is `technofatty.com`.
- The server uses Apache, not Nginx.
- The exact Python serving mechanism is unknown and must be checked. It may be `mod_wsgi`, a reverse proxy to another app server, uWSGI, or something else.
- The app should move to Postgres.
- This is an internet-facing dev deployment, not full production yet.
- `DEBUG` can remain on temporarily until the user is ready to tighten it.
- Secrets can be revisited nearer production, but the deployment shape should make env vars easy.
- The user wants practical cyber hygiene, but not a full production hardening pass yet.

## Decision: Apache, Not Nginx

Use Apache as the front door because that is what the VPS already uses.

The likely preferred path is:

```text
Apache + mod_wsgi + Postgres + Django static files served by Apache
```

If Apache is already reverse-proxying to another Python app server, preserve the existing pattern if it is sane. Do not switch to Nginx/Gunicorn just because many Django tutorials use that stack.

## Intention To Move To Postgres

The current local project uses SQLite. The VPS deployment should move Django to Postgres.

Expected work:

- Install/verify Postgres on the VPS.
- Create a `technofatty` database.
- Create a dedicated DB user.
- Add a Postgres Python driver to the repo, likely `psycopg[binary]` or `psycopg2-binary`.
- Change Django `DATABASES` to support Postgres via environment variables.
- Run migrations against Postgres on the VPS.

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

## Exact Next Steps On The VPS

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

## First Commands To Run On The VPS

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

## Likely Apache Shape If mod_wsgi Is Available

If `apachectl -M` shows `wsgi_module`, the deployment can use `config/wsgi.py`.

Expected vhost ingredients:

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

Adjust paths after inspecting the server. Do not assume `/srv/technofatty/app` already exists.

## Useful Django Commands After Repo Is In Place

From the project directory on the VPS:

```bash
python3 -m venv .venv
.venv/bin/pip install --upgrade pip
.venv/bin/pip install -r requirements.txt
.venv/bin/python manage.py check
.venv/bin/python manage.py migrate
.venv/bin/python manage.py collectstatic
```

If settings have not yet been patched for Postgres, `migrate` will still target SQLite. Patch settings first if the intention is to verify Postgres.

## Current Local Verification

Before this handoff, the local app had recently passed:

```bash
.venv/bin/python manage.py check
.venv/bin/python manage.py test
```

The most recent direct route checks included:

```text
/calculators/vaguepost-decoder/ -> 200
/calculators/parent-phone-hypocrisy-meter/ -> 200
/ask-podge/ -> 200
```

## Cautions For The VPS Session

- Inspect before changing Apache. Existing vhosts may matter.
- Do not assume Nginx or Gunicorn.
- Do not delete existing Apache configs.
- Avoid broad production refactors unless needed to get the internet-facing dev site working.
- Keep deployment changes small enough that the site can be debugged with normal Apache, Django, and Postgres logs.
