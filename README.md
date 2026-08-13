# CRM — 3-5 User AI-Powered CRM

Custom CRM built for small presales/sales teams: FastAPI + MySQL backend,
React + Vite + Tailwind frontend, Claude API for deal summaries, next-step
suggestions, and BANT qualification scoring.

## Stack
- **Backend:** FastAPI, SQLAlchemy, MySQL (via PyMySQL), JWT auth
- **AI:** Anthropic Claude API (claude-sonnet-4-6)
- **Frontend:** React, Vite, TypeScript, Tailwind CSS
- **Hosting:** Railway (backend + MySQL), Vercel (frontend)

## Project structure
```
crm-app/
  backend/
    app/
      main.py           # FastAPI app entrypoint
      database.py        # SQLAlchemy engine/session
      models.py           # 6 tables: users, companies, contacts, deals, activities, qualifications
      schemas.py          # Pydantic request/response models
      auth.py              # JWT auth + password hashing
      ai.py                 # Claude API calls (summarize, next-steps, qualify)
      routers/
        auth.py
        companies.py
        contacts.py
        deals.py
        activities.py
        ai_endpoints.py
    seed.py               # Creates initial user accounts
    requirements.txt
    .env.example
  frontend/
    src/
      pages/
        Login.tsx
        Deals.tsx          # Kanban pipeline view
        DealDetail.tsx      # Activity log + AI panel
      lib/api.ts             # API client
      App.tsx
      main.tsx
    package.json
    .env.example
```

## Setup — Backend

1. Create a MySQL database on Railway (New Project → Add MySQL plugin), copy the connection string.
2. `cd backend`
3. `python -m venv venv && source venv/bin/activate` (Windows: `venv\Scripts\activate`)
4. `pip install -r requirements.txt`
5. `cp .env.example .env` and fill in:
   - `DATABASE_URL` — from Railway's MySQL "Connect" tab, format: `mysql+pymysql://user:pass@host:port/railway`
   - `ANTHROPIC_API_KEY` — from console.anthropic.com
   - `SECRET_KEY` — any long random string
6. Run the seed script to create your first users: `python seed.py`
   - Default accounts: `admin@example.com` / `changeme123` (and two rep accounts) — **change these passwords immediately**
7. Start the server: `uvicorn app.main:app --reload`
8. Visit `http://localhost:8000/docs` for interactive API docs (Swagger)

## Setup — Frontend

1. `cd frontend`
2. `npm install`
3. `cp .env.example .env` and set `VITE_API_URL` to your backend URL
4. `npm run dev`
5. Visit `http://localhost:5173`, log in with a seeded account

## Deploying

**Backend (Railway):**
1. Push this repo to GitHub
2. On Railway: New Project → Deploy from GitHub → select `backend` as root directory
3. Add the same environment variables from `.env.example` in Railway's dashboard
4. Railway auto-detects Python and runs `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   (you may need to add a `Procfile` or set the start command manually in Railway settings)

**Frontend (Vercel):**
1. New Project → import the GitHub repo → set root directory to `frontend`
2. Add `VITE_API_URL` env var pointing to your deployed Railway backend URL
3. Deploy

## Data model

Six tables: `users`, `companies`, `contacts`, `deals`, `activities`, `qualifications`.
Qualification is tracked as its own table (one row per BANT criterion per deal)
rather than fixed columns, so new criteria can be added later without a schema change.

## AI endpoints

- `POST /deals/{id}/summarize` — rolls up all activity notes into a deal brief
- `POST /deals/{id}/next-steps` — suggests top 3 next actions
- `POST /deals/{id}/qualify` — assesses BANT criteria from activity history, saves results
- Activities are auto-summarized on creation (`ai_summary` field)

## Security notes before going live

- Change all seeded passwords immediately
- Rotate `SECRET_KEY` and never commit `.env` (already gitignored)
- Restrict `FRONTEND_ORIGINS` to your actual deployed frontend URL
- Consider Alembic for schema migrations instead of `create_all` once in production
