# Setup Guide - AI Kubernetes Agent

Complete step-by-step guide for getting the AI Kubernetes Agent running.

## Prerequisites

Before you begin, ensure you have:

- **Docker & Docker Compose** — Download from https://www.docker.com/products/docker-desktop
- **Kubernetes Cluster** — Any accessible cluster (minikube, kind, EKS, AKS, GKE, etc.)
- **kubectl CLI** — Installed and configured to access your cluster
- **OpenRouter API Key** — Free tier available at https://openrouter.ai

## Step-by-Step Installation

### 1. Get Your OpenRouter API Key

1. Visit https://openrouter.ai
2. Create a free account
3. Navigate to the **API Keys** section
4. Create a new key and copy it (you'll need it in step 4)

### 2. Verify Kubernetes Access

```bash
# Test that kubectl works
kubectl get nodes

# Test that you can access pods
kubectl get pods --all-namespaces
```

If these commands fail, fix your kubeconfig before continuing.

### 3. Clone the Project

```bash
git clone <repository-url>
cd AI_Kubernetes_Agent
```

### 4. Configure Backend (.env)

Create a `.env` file in the `backend` directory:

```bash
# Navigate to backend directory
cd backend

# Copy the example
cp .env.example .env

# Edit with your values
# On Mac/Linux: nano .env
# On Windows: code .env or use your favorite editor
```

**Edit the .env file with:**

```
OPENROUTER_API_KEY=paste_your_api_key_here
OPENROUTER_MODEL=openai/gpt-4-turbo
KUBECONFIG_PATH=~/.kube/config
CORS_ORIGINS=["http://localhost:3000"]
```

**Important:** Replace `paste_your_api_key_here` with your actual OpenRouter API key!

### 5. Configure Frontend (.env.local)

```bash
# Navigate to frontend directory
cd ../frontend

# Create .env.local
cat > .env.local << EOF
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
EOF
```

Or on Windows, create `.env.local` with the content:
```
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
```

### 6. Start the Application

```bash
# From project root
docker compose up --build
```

Wait for both services to start. You should see:
```
backend-1   | Application startup complete
frontend-1  | ▲ Next.js [version]
frontend-1  | - Local: http://localhost:3000
```

### 7. Access the Application

Open your browser to: **http://localhost:3000**

You should see:
- A header: "AI Kubernetes Agent"
- An "Investigate Cluster" button
- Progress tracking panel
- Investigation history panel

## Verify Everything Works

### Test 1: Health Check

```bash
curl http://localhost:8000/health
```

Expected response:
```json
{"status": "ok", "timestamp": "2024-..."}
```

### Test 2: Run Investigation

```bash
curl -X POST http://localhost:8000/investigate
```

This will:
1. Collect pod information
2. Gather error logs
3. Analyze Kubernetes events
4. Check deployment health
5. Validate networking
6. Run AI diagnosis
7. Return results

### Test 3: Get History

```bash
curl http://localhost:8000/history
```

## Using the Dashboard

### Basic Workflow

1. **Login** (if required)
   - Enter any email/password and click login
   - Click "Investigate Cluster" to proceed

2. **Trigger Investigation**
   - Click the "Investigate Cluster" button
   - Watch the progress steps complete

3. **View Results**
   - See root cause analysis
   - Read the explanation
   - View recommended kubectl command
   - Check confidence score

4. **Review History**
   - See past investigations
   - Click to view details
   - Compare diagnoses

## Docker Compose Services

The `docker-compose.yml` defines two services:

```yaml
backend:
  - Python FastAPI application
  - Runs on port 8000
  - Handles Kubernetes investigation
  - Connects to OpenRouter API
  
frontend:
  - Next.js React application
  - Runs on port 3000
  - Provides web UI
  - Depends on backend service
```

## Common Issues & Solutions

### "Cannot connect to backend"

**Symptom:** Frontend shows connection error

**Solution:**
```bash
# Check backend is running
docker compose logs backend

# Verify ports are open
curl http://localhost:8000/health

# Restart if needed
docker compose restart backend
```

### "OpenRouter API key invalid"

**Symptom:** Backend logs show authentication error

**Solution:**
1. Double-check your API key is correct
2. Verify it's in the `.env` file without extra spaces
3. Restart backend: `docker compose restart backend`

### "kubectl not found"

**Symptom:** Backend fails to collect pod information

**Solution:**
```bash
# Verify kubectl is installed
kubectl version

# Check kubeconfig path
echo $KUBECONFIG
# or on Windows: echo %KUBECONFIG%

# Update KUBECONFIG_PATH in .env if needed
```

### "Kubernetes connection refused"

**Symptom:** Backend cannot access cluster

**Solution:**
```bash
# Test kubectl access
kubectl get nodes

# If this fails, fix your kubeconfig first
# Then update KUBECONFIG_PATH in backend/.env
```

## Development Mode

To run locally without Docker:

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows
pip install -r requirements.txt
python main.py
```

Runs on http://localhost:8000

### Frontend (in another terminal)

```bash
cd frontend
npm install
npm run dev
```

Runs on http://localhost:3000

## Stopping the Application

```bash
# Stop and remove containers
docker compose down

# Stop and remove volumes (data)
docker compose down -v

# Just stop without removing
docker compose stop
```

## Viewing Logs

```bash
# View all logs
docker compose logs

# View backend only
docker compose logs backend

# View frontend only
docker compose logs frontend

# Follow logs in real-time
docker compose logs -f

# Last 50 lines
docker compose logs --tail 50
```

## Next Steps

- Review [ENVIRONMENT.md](ENVIRONMENT.md) for advanced configuration
- Check [README.md](README.md) for architecture overview
- Explore the API documentation at http://localhost:8000/docs
- Try investigating different namespaces
- Modify prompts in `backend/ai/prompt_builder.py`

## Support

If you encounter issues:

1. Check the troubleshooting section above
2. Review Docker logs: `docker compose logs`
3. Verify all prerequisites are installed
4. Ensure kubeconfig and API key are valid
5. Open an issue with error details

Good luck! 🚀
