# 🚀 AgentHive SaaS Platform

A complete multi-agent AI SaaS platform with 5 specialist agents, premium UI, subscription billing, and 24/7 automation.

## 🏗️ Architecture

```
┌─────────────────┐     HTTPS/API     ┌──────────────────┐
│   Vercel        │ ────────────────▶ │   Render         │
│  (Frontend)     │                   │   (Backend)      │
│   Next.js       │                   │   FastAPI        │
│                 │                   │   SQLite/Postgres│
└─────────────────┘                   └──────────────────┘
```

## 📁 Project Structure

```
agenthive/
├── app/                          # Next.js App Router (Frontend for Vercel)
│   ├── layout.tsx
│   ├── page.tsx                  # Landing page
│   ├── globals.css
│   ├── login/page.tsx
│   ├── signup/page.tsx
│   ├── dashboard/page.tsx
│   ├── pricing/page.tsx
│   └── agents/page.tsx
├── app/                          # FastAPI Backend (Python - for Render)
│   ├── main.py
│   ├── models.py
│   ├── auth.py
│   ├── billing.py
│   ├── agents/__init__.py
│   └── websocket.py
├── requirements.txt              # Python dependencies
├── package.json                  # Node.js dependencies
├── next.config.js                # Next.js config
├── vercel.json                   # Vercel deployment config
├── Dockerfile                    # Docker deployment
├── Procfile                      # Heroku/Render deployment
├── .env.example                  # Environment variables template
└── README.md
```

## 🤖 5 Agent Team

| Agent | Role |
|-------|------|
| 🧠 Head Agent | Orchestrates tasks & coordinates specialists |
| 🔍 Trend Scout | Finds trending products from internet/e-commerce |
| 💰 Analyst | Revenue, traffic & KPI analysis |
| 🎬 Creative Studio | Ad copy, video scripts, UGC content |
| 📱 Social Media Manager | Posts, comments, DM replies, traffic management |

## 🚀 Quick Start

### 1. Clone & Install

```bash
git clone https://github.com/zaid34586/agenthive.git
cd agenthive
```

### 2. Backend (Python/FastAPI) - Deploy on Render

1. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```

2. Fill in your `.env`:
   ```
   DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@db.xxx.supabase.co:5432/postgres
   JWT_SECRET=your-secret-key
   PORT=8000
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run locally:
   ```bash
   python run.py
   ```

5. Deploy to Render.com (recommended for backend)

### 3. Frontend (Next.js) - Deploy on Vercel

1. Install dependencies:
   ```bash
   npm install
   ```

2. Create `.env.local`:
   ```
   NEXT_PUBLIC_API_URL=https://your-backend.onrender.com
   ```

3. Run locally:
   ```bash
   npm run dev
   ```

4. Deploy to Vercel:
   ```bash
   npx vercel
   ```

## 💰 Pricing Tiers

| Plan | Price | Features |
|------|-------|----------|
| Starter | $0/month | 5 tasks/month, Head Agent + Trend Scout |
| Pro | $499/month | 50 tasks/month, All 5 agents, Creative Studio |
| Business | $1,499/month | Unlimited tasks, All agents + priority, White-label |

## 🔐 Environment Variables

### Backend (.env)
```
DATABASE_URL=postgresql://...
JWT_SECRET=your-secret-key
DEEPSEEK_API_KEY=...
GROQ_API_KEY=...
OPENAI_API_KEY=...
RAZORPAY_KEY_ID=...
RAZORPAY_KEY_SECRET=...
PORT=8000
```

### Frontend (.env.local)
```
NEXT_PUBLIC_API_URL=https://your-backend-url.com
```

## 📊 Database (Supabase)

6 tables created:
- `users` - User accounts & auth
- `subscriptions` - Subscription plans & billing
- `tasks` - Agent tasks & results
- `payments` - Payment records
- `usage_logs` - API usage tracking
- `agent_logs` - Individual agent activity logs

## 🌐 Deployment

### Option A: Vercel (Frontend) + Render (Backend) - RECOMMENDED

1. **Frontend on Vercel:**
   - Connect GitHub repo to Vercel
   - Add `NEXT_PUBLIC_API_URL` env var pointing to Render backend
   - Deploy

2. **Backend on Render:**
   - Connect GitHub repo to Render
   - Set build command: `pip install -r requirements.txt`
   - Set start command: `python run.py`
   - Add all `.env` variables
   - Deploy

### Option B: Single VPS

```bash
# Install dependencies
pip install -r requirements.txt
npm install

# Build frontend
npm run build

# Run backend
python run.py

# Run frontend (or serve built files)
npm start
```

## 🛡️ Security

- JWT-based authentication
- Password hashing with bcrypt
- Rate limiting ready
- CORS configured
- SQL injection protected (SQLAlchemy ORM)

## 📞 Support

For issues, create a GitHub issue in the repository.

---

**AgentHive** - Build your AI agent empire today. 🚀
