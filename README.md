# AI Based Smart Complaint System for Women

Production-oriented Django 5 web application that enables women to file safety complaints securely using text or voice input, assisted by an AI chatbot.

## Core Features
- Guided complaint filing with AI assistant (OpenAI `gpt-4o-mini` fallback logic included)
- Voice-to-text capture via browser Web Speech API
- Complaint evidence uploads (images/audio/docs)
- User authentication (register/login/logout)
- Staff dashboard for reviewing complaints and updating status
- Complaint status tracking with audit logs
- Async notifications with Celery (Email + optional Twilio SMS)
- Encrypted complaint description storage (Fernet)

## Tech Stack
- Backend: Django 5.x, Celery
- Frontend: HTML5, CSS3, Bootstrap 5, JavaScript
- AI: OpenAI API (fallback deterministic guidance if API key absent)
- Database: SQLite for development, PostgreSQL supported via env
- Notifications: Django email backend + Twilio SMS

## Quick Start

### 1) Setup
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

### 2) Run migrations + create admin
```bash
python manage.py migrate
python manage.py createsuperuser
```

### 3) Start app
```bash
python manage.py runserver
```

### 4) Start Celery worker (optional but recommended)
```bash
celery -A smart_complaint_system worker -l info
```

## Environment Variables
See `.env.example` for all options, including:
- Django security/runtime settings
- OpenAI API model/key
- Twilio credentials
- Celery broker/result backend
- Fernet encryption key (`ENCRYPTION_KEY`)

## Security Notes
- Complaint descriptions are encrypted before DB persistence when `ENCRYPTION_KEY` is set.
- CSRF protection, auth, and secure middleware defaults are enabled.
- Production mode (`DJANGO_DEBUG=False`) enforces secure cookies + SSL redirect.

## URL Map
- `/` - Landing page
- `/register/` - User registration
- `/login/` - User login
- `/dashboard/` - User complaint dashboard
- `/complaints/new/` - Submit complaint
- `/staff/dashboard/` - Staff management dashboard

## Production Hardening Checklist
- Configure PostgreSQL and Redis in production
- Store secrets in secure secret manager (never commit real `.env`)
- Set up HTTPS/TLS, reverse proxy (Nginx), and gunicorn/uvicorn
- Configure SMTP provider and Twilio verified numbers
- Add monitoring, centralized logging, and backup policy
