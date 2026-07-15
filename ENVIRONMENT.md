# Environment Configuration

This file documents the required environment variables for the AI Kubernetes Agent.

## Backend (.env file)

```
# OpenRouter API Configuration
OPENROUTER_API_KEY=your_openrouter_api_key_here
OPENROUTER_MODEL=openai/gpt-4-turbo

# Kubernetes Configuration
KUBECONFIG_PATH=/path/to/kubeconfig

# Frontend URL (for CORS)
CORS_ORIGINS=["http://localhost:3000"]
```

### Getting Your API Key

1. Sign up for an OpenRouter account at https://openrouter.ai
2. Navigate to API Keys in your dashboard
3. Create a new API key and copy it
4. Set the `OPENROUTER_API_KEY` environment variable

### Kubernetes Configuration

- `KUBECONFIG_PATH`: Path to your kubeconfig file (typically `~/.kube/config`)
- Default: Uses kubectl from system PATH

## Frontend (.env.local file)

```
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
```

### Configuration Details

- `NEXT_PUBLIC_API_BASE_URL`: Backend API endpoint
- Default: `http://localhost:8000`
- For production: Update to your backend domain

## Quick Start

1. Copy the environment variables above to `.env` in the backend directory
2. Update values with your API keys and paths
3. Run `docker-compose up` to start the application
4. Navigate to `http://localhost:3000` in your browser

## Development

For local development:

```bash
# Backend
cd backend
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows
pip install -r requirements.txt
python main.py

# Frontend (in another terminal)
cd frontend
npm install
npm run dev
```
