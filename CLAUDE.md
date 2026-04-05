# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

PomoTracker is a Django 4.2 Pomodoro timer web application (Python 3.11) with PostgreSQL, Redis caching, and Nginx reverse proxy. It has two interfaces: a template-rendered web app (`app/`) and a RESTful JSON API (`api/`) for mobile/CSR clients.

## Development Commands

### Docker (recommended)
```bash
docker compose -f docker-compose.yml up --build -d
docker compose exec app python manage.py migrate
# Access at http://localhost:1337
```

### Django management
```bash
python manage.py runserver 0.0.0.0:1337    # local dev server (needs local PG + Redis)
python manage.py migrate                    # apply migrations
python manage.py makemigrations             # generate migrations after model changes
python manage.py giveRewards                # custom command: monthly leaderboard rewards
```

### Environment
Dev env vars are in `PomoTracker/.dev.env` (loaded by docker-compose). Key vars: `DB_*`, `REDIS_HOST`, `DJANGO_DEBUG`, `DJANGO_ALLOWED_HOSTS`, `DJANGO_CSRF_TRUSTED_ORIGINS`.

## Architecture

### Two-app structure
- **`app/`** — Server-side rendered views (timer, profile, leaderboard, charts). Uses Django templates in `app/templates/app/`. Authentication via Django + django-allauth (Google OAuth).
- **`api/`** — Token-authenticated JSON endpoints for CRUD on pomodoros, tags, settings, and leaderboard data. Tokens are auto-generated per user in `UserSettings`.

### Key models (`app/models.py`)
- **Pomodoro** — Core entity: links user, timestamp, and tag.
- **Tag** — Categorizes pomodoros per user.
- **UserSettings** — Per-user config (theme, sounds, focus/break times, timezone, API token, profile image URL).
- **Rewards** — Gamification medals (gold/silver/bronze) and average ranking.
- **SlicePomodoros** — Utility class that filters pomodoros by time period (year/month/week/day).
- **Statistics** — Aggregation logic for averages, tag stats, leaderboard.

### Infrastructure stack
Nginx (:1337) → Gunicorn (:80) → Django → PostgreSQL (:5432) + Redis (:6379)

Config files live in `config/` (nginx.conf, postgres/, redis/, gunicorn/).

### AWS S3 integration
Profile image uploads/deletions via boto3 in `app/helpers.py`.

## CI/CD

Azure Pipelines (`azure-pipelines.yml`): builds Docker image, pushes to Docker Hub (`viodid/pomotracker`), deploys via SSH to production VM using `docker-compose.prod.yml`.

## URL structure

- Web: `/` (timer), `/<username>/` (profile), `/leaderboard`, `/charts`, `/pomodoros`, `/token`
- API: `/api/<username>/alltags`, `/api/<username>/alldates`, `/api/<username>/allpomodoros`, `/api/leaderboard`, `/api/<token>/create` (POST), `/api/<token>/<id>` (PUT/DELETE), `/api/<token>/settings` (PUT)
- Auth: `/accounts/` (django-allauth routes)

## Notes

- API GET endpoints are cached for 25 minutes via Redis.
- Sessions use signed cookies, not database-backed sessions.
- Production settings enable SSL/HSTS.
- Tests (`app/tests.py`, `api/tests.py`) are placeholder-only — no test suite exists.
