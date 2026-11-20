# AgentHive — Production Deployment Plan

## Current Status
- ✅ Frontend (Next.js) deployed on Vercel: `https://agenthive-lilac.vercel.app`
- ✅ Code pushed to GitHub: `https://github.com/zaid34586/agenthive`
- ❌ Backend (FastAPI) — only running locally, NOT deployed
- ❌ Database — using local SQLite (`data.db`), not Supabase
- ❌ `NEXT_PUBLIC_API_URL` — not connected to a live backend

## Goal
Make AgentHive fully production-ready: frontend + backend + database all live and connected.

---

## Step-by-Step Plan

### Step 1: Verify Backend Runs Locally
- Run `python run.py` locally
- Confirm it starts on port 8000
- Test `/health` endpoint returns `{"status": "ok"}`

### Step 2: Create Production `.env` File
Create `.env` in project root with these values:
```
DATABASE_URL=postgresql://postgres:PASSWORD@db.PROJECT.supabase.co:5432/postgres
JWT_SECRET=your-super-secret-random-key-32-chars-min
ACCESS_TOKEN_EXPIRE_MINUTES=1440
DEEPSEEK_API_KEY=
GROQ_API_KEY=
OPENAI_API_KEY=
RAZORPAY_KEY_ID=your-razorpay-key-id
RAZORPAY_KEY_SECRET=your-razorpay-key-secret
NEXT_PUBLIC_API_URL=https://your-backend-url.onrender.com
NEXT_PUBLIC_SITE_URL=https://agenthive-lilac.vercel.app
PORT=8000
HOST=0.0.0.0
```

### Step 3: Choose Backend Hosting
**Recommended: Render.com** (free tier, easy FastAPI deployment)
Alternative: Railway.app, Fly.io

### Step 4: Deploy Backend to Render
1. Connect GitHub repo `zaid34586/agenthive` to Render
2. Create a new **Web Service**
3. Build command: `pip install -r requirements.txt`
4. Start command: `python run.py`
5. Add environment variables from `.env`
6. Deploy — get backend URL (e.g., `https://agenthive-api.onrender.com`)

### Step 5: Set Up Supabase Database
1. Create a project at `https://supabase.com`
2. Get the PostgreSQL connection string
3. Add it as `DATABASE_URL` in Render environment variables
4. The backend will auto-create tables via `init_db()` on startup

### Step 6: Connect Frontend to Backend
1. In Vercel project settings, add/update Environment Variable:
   - `NEXT_PUBLIC_API_URL` = `https://your-backend-url.onrender.com`
2. Redeploy frontend on Vercel

### Step 7: Test Full Flow
1. Open `https://agenthive-lilac.vercel.app`
2. Sign up a new account
3. Login
4. Create a task from dashboard
5. Verify task appears in dashboard
6. Check pricing page and payment flow

### Step 8: Fix Issues & Polish
- Fix any CORS errors between frontend and backend
- Fix any database connection errors
- Disable Vercel Deployment Protection (if needed for public access)

---

## Files Already Ready for Deployment
- `requirements.txt` — all Python dependencies listed
- `Procfile` — `web: python run.py`
- `Dockerfile` — container config
- `vercel.json` — frontend deployment config
- `app/main.py` — FastAPI app with health check at `/health`
- `app/models.py` — SQLModel with auto table creation

---

## Testing Checklist
- [ ] Backend `/health` returns OK
- [ ] Backend `/api/agents/status` returns 5 agents
- [ ] Frontend loads without errors
- [ ] User signup works
- [ ] User login works
- [ ] Dashboard loads after login
- [ ] Task creation works
- [ ] Database tables created in Supabase
