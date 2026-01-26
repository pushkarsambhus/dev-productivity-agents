# Quick Start Guide

Get up and running in 5 minutes!

## Choose Your Path

### 🚀 Fastest: Docker Compose (Recommended)

```bash
# 1. Start everything
docker-compose up --build

# 2. Open browser
http://localhost:8000/docs

# 3. Try an example request
curl -X POST http://localhost:8000/agent/task \
  -H "Content-Type: application/json" \
  -d '{"task": "Calculate 15 + 27"}'

# 4. Stop when done
docker-compose down
```

**What this does:**
- Builds Docker image for the API
- Starts Redis cache
- Starts API server
- Sets up networking between services

---

### 🐍 Local Python Development

```bash
# 1. Install Redis
brew install redis  # macOS
# or: sudo apt-get install redis  # Ubuntu
redis-server

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # or: venv\Scripts\activate on Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the API
uvicorn app.main:app --reload

# 5. Open browser
http://localhost:8000/docs
```

**When to use this:**
- Active development (auto-reload on code changes)
- Debugging with IDE
- Running tests

---

### ☸️ Kubernetes (Most Realistic)

```bash
# 1. Start Minikube (or use existing cluster)
minikube start

# 2. Build image in Minikube's Docker
eval $(minikube docker-env)
docker build -t interview-prep-api:latest .

# 3. Deploy everything
kubectl apply -f k8s/

# 4. Port forward to access
kubectl port-forward service/interview-prep-api 8000:80 -n interview-prep

# 5. Open browser
http://localhost:8000/docs

# 6. Watch it scale!
kubectl get pods -n interview-prep --watch

# 7. Clean up
kubectl delete namespace interview-prep
```

**What this demonstrates:**
- Container orchestration
- Auto-scaling
- Service discovery
- Production-like environment

---

## First Steps After Starting

### 1. Check Health

```bash
curl http://localhost:8000/health
```

Expected:
```json
{
  "status": "healthy",
  "message": "API is running",
  "cache_connected": true
}
```

### 2. Try the Agent

```bash
curl -X POST http://localhost:8000/agent/task \
  -H "Content-Type: application/json" \
  -d '{"task": "What is Kubernetes?"}'
```

### 3. See Available Tools

```bash
curl http://localhost:8000/agent/tools
```

### 4. Interactive Docs

Open http://localhost:8000/docs in your browser

- Click "Try it out" on any endpoint
- Fill in parameters
- Click "Execute"
- See response

---

## Common Issues

### Redis Connection Failed

**Symptom:** `cache_connected: false` in health check

**Solution:**
```bash
# Check if Redis is running
redis-cli ping  # Should return PONG

# Start Redis if needed
redis-server

# Or restart Docker Compose
docker-compose restart redis
```

### Port Already in Use

**Symptom:** `Address already in use: 8000`

**Solution:**
```bash
# Find what's using port 8000
lsof -i :8000

# Kill the process
kill -9 <PID>

# Or use a different port
uvicorn app.main:app --port 8001
```

### Docker Build Fails

**Symptom:** Docker build errors

**Solution:**
```bash
# Clear Docker cache and rebuild
docker-compose build --no-cache

# Or remove all and start fresh
docker-compose down -v
docker-compose up --build
```

### Kubernetes Pods Not Starting

**Symptom:** Pods stuck in `ImagePullBackOff`

**Solution:**
```bash
# Make sure image exists in Minikube
eval $(minikube docker-env)
docker images | grep interview-prep-api

# Rebuild if missing
docker build -t interview-prep-api:latest .

# Check pod logs
kubectl logs <pod-name> -n interview-prep
kubectl describe pod <pod-name> -n interview-prep
```

---

## Next Steps

1. **Read the Code**
   - Start with `app/main.py` (API endpoints)
   - Then `app/agent.py` (agent logic)
   - Finally `app/cache.py` (Redis integration)

2. **Try Example Requests**
   - Open `examples.http`
   - Run requests in VS Code (REST Client extension)
   - Or use the curl commands

3. **Run Tests**
   ```bash
   pytest tests/ -v
   ```

4. **Explore Kubernetes**
   ```bash
   # See all resources
   kubectl get all -n interview-prep

   # Watch pods scale
   kubectl get hpa -n interview-prep --watch

   # View logs
   kubectl logs -f deployment/interview-prep-api -n interview-prep
   ```

5. **Read the README**
   - Core concepts explained
   - Interview talking points
   - AWS integration
   - Production considerations

---

## Cheat Sheet

### Docker Compose

```bash
# Start
docker-compose up -d

# View logs
docker-compose logs -f

# Restart a service
docker-compose restart api

# Stop
docker-compose down

# Remove volumes too
docker-compose down -v
```

### Kubernetes

```bash
# Create resources
kubectl apply -f k8s/

# View resources
kubectl get all -n interview-prep

# View logs
kubectl logs -f deployment/interview-prep-api -n interview-prep

# Port forward
kubectl port-forward service/interview-prep-api 8000:80 -n interview-prep

# Scale manually
kubectl scale deployment/interview-prep-api --replicas=5 -n interview-prep

# Delete everything
kubectl delete namespace interview-prep
```

### Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app

# Run specific test
pytest tests/test_api.py::test_health_check -v

# Run with output
pytest -v -s
```

---

## Learning Resources

- **API Docs:** http://localhost:8000/docs (when running)
- **Main README:** Comprehensive explanations
- **Code Comments:** Every file is heavily documented
- **examples.http:** Sample requests to try

---

## Getting Help

1. Check the code comments (detailed explanations)
2. Read the README (concepts and interview tips)
3. Try the examples (examples.http)
4. Run tests to see expected behavior
5. Check logs: `docker-compose logs` or `kubectl logs`

---

**Ready to learn? Pick a path above and start exploring! 🚀**
