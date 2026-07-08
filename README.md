# ChessCoach (LexiTutor)

A personal game-coaching booking platform built with Django. Clients can browse coaching services, book sessions, pay securely via Paystack, and manage their bookings — all through a clean, custom-designed interface.

**Live site:** [lechesscoach.onrender.com](https://lechesscoach.onrender.com)

## About

ChessCoach lets a solo coach (1800–1900 rated in chess) offer paid coaching sessions across six games: Chess, Sudoku, Scramble, Checkers, Whot, and Ludo. Originally built as a backend web development coursework project (SEN 310), it's designed to also function as a real, ongoing business.

## Features

- **Custom authentication** — signup/login with a custom user model (unique email + phone number), strong password validation
- **Dynamic pricing engine** — tiered base prices per game, lead-time booking discounts (up to 20%), and overtime surcharges calculated automatically
- **Smart scheduling** — 6-hour slot blocking to prevent double-booking, max 4 sessions/day per client, rolling 1-year booking window
- **Paystack payment integration** — secure hosted checkout with server-side payment verification (never trusts client-side redirects alone)
- **Booking management** — clients can view booking history and retry failed/pending payments without needing to track booking IDs
- **Post-payment contact widget** — WhatsApp and email quick-contact options appear after a successful payment
- **Responsive, custom-designed UI** — no CSS framework; hand-built design system with a navy/red color scheme

## Tech Stack

- **Backend:** Django 6.0.6, Python 3.14
- **Database:** SQLite (development)
- **Payments:** Paystack (redirect flow)
- **Frontend:** Django templates, vanilla CSS and JavaScript (no framework)
- **Hosting:** Render (free tier), with WhiteNoise for static file serving
- **Config:** python-decouple for environment variable management

## Environment Variables

This project reads secrets from environment variables rather than hardcoding them. Create a `.env` file in the project root with:

```
SECRET_KEY=your-django-secret-key
DEBUG=True
PAYSTACK_PUBLIC_KEY=your-paystack-public-key
PAYSTACK_SECRET_KEY=your-paystack-secret-key
```

`.env` is gitignored and should never be committed.

## Local Setup

```bash
git clone https://github.com/Alexis-Cell-Cloud/LexiTutorChessCoachingApp.git
cd LexiTutorChessCoachingApp
python -m venv env
source env/Scripts/activate   # Windows (Git Bash)
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## Deployment

Deployed on Render using:
- **Build command:** `./build.sh` (installs dependencies, collects static files, runs migrations)
- **Start command:** `gunicorn config.wsgi`

Environment variables are set directly in the Render dashboard rather than via `.env`.

## Roadmap

- [ ] `session_mode` field (physical/online) with conditional address logic
- [ ] Automated cleanup of stale pending bookings (cron/Celery)
- [ ] Streak/recurring booking support
- [ ] Dedicated "About" page
- [ ] Switch to Paystack live keys once business verification is complete

## Author

Built by Alexis, a Nigerian computer science student, as both a coursework project and the foundation of a real coaching business.