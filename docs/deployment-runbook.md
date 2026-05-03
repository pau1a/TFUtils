# Technofatty Deployment Runbook

This runbook describes the current live Technofatty VPS deployment. Treat this deployment as the baseline unless the user explicitly asks to change the hosting shape.

## Live Site

Current live URL:

```text
https://technofatty.com/
```

Canonical redirect behaviour:

- `http://technofatty.com/` redirects to `https://technofatty.com/`.
- `http://www.technofatty.com/` redirects to `https://technofatty.com/`.
- `https://www.technofatty.com/` redirects to `https://technofatty.com/`.
- The canonical host is `technofatty.com` without `www`.

## Server Layout

Application:

```text
/var/www/technofatty/app
```

Virtualenv:

```text
/var/www/technofatty/venv
```

Database:

```text
PostgreSQL database: technofatty_dev
PostgreSQL user: technofatty
```

WSGI entrypoint:

```text
/var/www/technofatty/app/wsgi_prod.py
```

Static root:

```text
/var/www/technofatty/app/staticfiles
```

Apache vhosts:

```text
/etc/apache2/sites-available/technofatty.com.conf
/etc/apache2/sites-available/technofatty.com-le-ssl.conf
```

Certbot certificate:

```text
/etc/letsencrypt/live/technofatty.com/
```

## Django Environment

The live WSGI entrypoint loads `/var/www/technofatty/app/.env` before importing Django.

Important environment variables:

```text
DJANGO_DEBUG=1
DJANGO_SECRET_KEY=<long random secret before production>
DJANGO_ALLOWED_HOSTS=technofatty.com,www.technofatty.com
DJANGO_CSRF_TRUSTED_ORIGINS=https://technofatty.com,https://www.technofatty.com
DB_ENGINE=django.db.backends.postgresql
DB_NAME=technofatty_dev
DB_USER=technofatty
DB_PASSWORD=<server-only password>
DB_HOST=localhost
DB_PORT=5432
```

For the current internet-facing dev deployment, `DJANGO_DEBUG=1` is intentional. Before a production hardening pass, set `DJANGO_DEBUG=0`, provide `DJANGO_SECRET_KEY`, and review:

```text
DJANGO_SESSION_COOKIE_SECURE
DJANGO_CSRF_COOKIE_SECURE
DJANGO_SECURE_SSL_REDIRECT
DJANGO_SECURE_HSTS_SECONDS
DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS
DJANGO_SECURE_HSTS_PRELOAD
```

## Normal Update Procedure

From the app directory:

```bash
cd /var/www/technofatty/app
git status --short
git pull
/var/www/technofatty/venv/bin/pip install -r requirements.txt
set -a
. /var/www/technofatty/app/.env
set +a
/var/www/technofatty/venv/bin/python manage.py check
/var/www/technofatty/venv/bin/python manage.py migrate
/var/www/technofatty/venv/bin/python manage.py collectstatic --noinput
sudo apache2ctl configtest
sudo systemctl reload apache2
```

Check `git status --short` first so local or user-made changes are not overwritten accidentally. If the working tree is dirty, understand the changes before pulling or deploying.

The `set -a` block matters: the WSGI entrypoint loads `.env`, but plain `manage.py` commands do not automatically load it. Source `.env` before `check`, `migrate`, and `collectstatic` when you mean to operate against the live VPS settings and PostgreSQL database.

## Django Maintenance Commands

Run checks:

```bash
cd /var/www/technofatty/app
set -a
. /var/www/technofatty/app/.env
set +a
/var/www/technofatty/venv/bin/python manage.py check
```

Apply migrations:

```bash
cd /var/www/technofatty/app
set -a
. /var/www/technofatty/app/.env
set +a
/var/www/technofatty/venv/bin/python manage.py migrate
```

Collect static files:

```bash
cd /var/www/technofatty/app
set -a
. /var/www/technofatty/app/.env
set +a
/var/www/technofatty/venv/bin/python manage.py collectstatic --noinput
```

Deployment checklist with production-like security settings:

```bash
cd /var/www/technofatty/app
set -a
. /var/www/technofatty/app/.env
set +a
DJANGO_DEBUG=0 \
DJANGO_SECURE_SSL_REDIRECT=1 \
DJANGO_SECURE_HSTS_SECONDS=31536000 \
DJANGO_SECURE_HSTS_PRELOAD=1 \
/var/www/technofatty/venv/bin/python manage.py check --deploy
```

## Apache Commands

Validate Apache configuration:

```bash
sudo apache2ctl configtest
```

Reload Apache after a valid config test:

```bash
sudo systemctl reload apache2
```

Restart Apache only when reload is not enough:

```bash
sudo systemctl restart apache2
```

## Smoke Tests

From the VPS or any shell with network access:

```bash
curl -I http://technofatty.com/
curl -I http://www.technofatty.com/
curl -I https://technofatty.com/
curl -I https://www.technofatty.com/
```

Expected high-level behaviour:

- HTTP requests should redirect to HTTPS.
- `www` requests should redirect to non-`www`.
- `https://technofatty.com/` should return a successful response.

Useful page checks:

```bash
curl -I https://technofatty.com/
curl -I https://technofatty.com/calculators/vaguepost-decoder/
curl -I https://technofatty.com/ask-podge/
```

## Certificate Renewal

`certbot renew --dry-run` currently succeeds for `technofatty.com`.

The global dry-run currently reports an unrelated renewal failure for `loudounproud.co.uk`. Do not treat that unrelated failure as evidence that the Technofatty certificate is broken.

Technofatty certificate path:

```text
/etc/letsencrypt/live/technofatty.com/
```

## Do Not Commit

Do not commit local deployment secrets or generated runtime output:

- `.env`
- `staticfiles/`
- `db.sqlite3`
- local secrets
- database dumps containing private data

Keep secrets on the server and out of Git.
