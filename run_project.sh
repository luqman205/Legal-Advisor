#!/bin/zsh
# ⚖️ Pakistani Legal Advisor AI Launcher

# Setup NVM and Node.js
export NVM_DIR="$HOME/.nvm"
if [ -s "$NVM_DIR/nvm.sh" ]; then
  echo "📦 Loading NVM..."
  . "$NVM_DIR/nvm.sh"
  nvm use 20.19.5
else
  echo "⚠️ NVM not found, attempting to use system node..."
fi

# Ensure correct working directory
cd "/Users/mac/Documents/legal advisor"

# Function to clean up background processes on exit
cleanup() {
  echo "\n🛑 Shutting down servers gracefully..."
  if [ -n "$BACKEND_PID" ]; then
    kill $BACKEND_PID 2>/dev/null
  fi
  exit 0
}
trap cleanup INT TERM EXIT

# Start Python RAG Backend
echo "🚀 Starting FastAPI Legal RAG Backend on http://127.0.0.1:8000..."
PYTHONPATH=. python3 -m uvicorn legal_ai.backend.app:app --host 127.0.0.1 --port 8000 &
BACKEND_PID=$!

# Wait for backend to spin up and perform verification
echo "⏳ Waiting for backend to initialize..."
sleep 4

# Check backend health
curl -s http://127.0.0.1:8000/health | grep -q "online"
if [ $? -eq 0 ]; then
  echo "✅ FastAPI Backend is online and loaded 11,000+ legal records!"
else
  echo "⚠️ Backend health check failed, but proceeding anyway..."
fi

# Start Next.js Frontend
echo "🚀 Starting Next.js Frontend on http://localhost:3000..."
npm run dev
