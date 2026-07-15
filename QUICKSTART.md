# 🚀 Quick Start Card

## AI Kubernetes Agent - 5-Minute Setup

### Prerequisites
- Docker & Docker Compose
- Kubernetes cluster with kubectl
- OpenRouter API key (free at https://openrouter.ai)

---

### Step 1: Get API Key
1. Visit https://openrouter.ai
2. Create account → API Keys → Create Key
3. Copy the key

---

### Step 2: Configure Backend

```bash
cd backend
cp .env.example .env
```

**Edit `backend/.env`:**
```
OPENROUTER_API_KEY=paste_your_key_here
OPENROUTER_MODEL=openai/gpt-4-turbo
KUBECONFIG_PATH=~/.kube/config
```

---

### Step 3: Configure Frontend

**Create `frontend/.env.local`:**
```
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
```

---

### Step 4: Start Application

```bash
docker compose up --build
```

Wait for: "Application startup complete"

---

### Step 5: Open Dashboard

Visit: **http://localhost:3000**

Click "Investigate Cluster" to run your first investigation!

---

## 📖 Documentation

- **[README.md](README.md)** — Features & architecture
- **[SETUP.md](SETUP.md)** — Detailed installation
- **[ENVIRONMENT.md](ENVIRONMENT.md)** — Configuration reference
- **[FRONTEND_GUIDE.md](FRONTEND_GUIDE.md)** — Component documentation
- **[IMPLEMENTATION.md](IMPLEMENTATION.md)** — Technical details
- **[INDEX.md](INDEX.md)** — Documentation index

---

## 🔍 Verify Setup

```bash
# Health check
curl http://localhost:8000/health

# API documentation
http://localhost:8000/docs

# Frontend
http://localhost:3000
```

---

## ❌ Troubleshooting

| Issue | Solution |
|-------|----------|
| Backend won't start | Check OpenRouter API key in `.env` |
| Frontend shows error | Ensure backend running on port 8000 |
| Investigation fails | Verify `kubectl get nodes` works |

See [SETUP.md](SETUP.md) for more troubleshooting.

---

## 🎯 What's Next?

1. **View Results** — Run investigation and see diagnosis
2. **Check History** — See previous analyses
3. **Explore Components** — Check [FRONTEND_GUIDE.md](FRONTEND_GUIDE.md)
4. **Extend Features** — See [IMPLEMENTATION.md](IMPLEMENTATION.md)

---

**That's it! Your AI-powered Kubernetes troubleshooting system is ready.** 🎉
