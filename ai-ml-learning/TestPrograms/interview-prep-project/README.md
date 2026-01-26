# Interview Prep Project: API, Agents, Kubernetes & Cloud

A comprehensive learning project that demonstrates foundational concepts in modern software engineering, designed for technical interview preparation. This project covers REST APIs, AI agents, containerization, Kubernetes orchestration, and cloud deployment patterns.

## Table of Contents

- [Project Overview](#project-overview)
- [Core Concepts](#core-concepts)
- [Architecture](#architecture)
- [Quick Start](#quick-start)
- [Detailed Explanations](#detailed-explanations)
- [Interview Talking Points](#interview-talking-points)
- [AWS & Cloud Integration](#aws--cloud-integration)
- [Production Considerations](#production-considerations)

---

## Project Overview

This project demonstrates how modern applications are built, packaged, and deployed. It's structured to help you:

1. **Understand** core concepts through well-commented code
2. **Run** everything locally to see it in action
3. **Explain** confidently in technical interviews
4. **Scale** mentally from local dev to production systems

### What's Included

- **REST API** (FastAPI): Modern Python web framework with automatic documentation
- **Agent System**: Demonstrates tool-calling and decision-making logic
- **Redis Cache**: In-memory data store for performance optimization
- **Docker**: Containerization for consistent deployments
- **Kubernetes**: Container orchestration for production-scale deployments
- **Cloud Patterns**: How this maps to AWS services (EKS, ElastiCache, ALB)

### Technology Stack

| Component | Technology | Why? |
|-----------|-----------|------|
| API Framework | FastAPI | Modern, fast, automatic validation & docs |
| Language | Python 3.11 | Popular, readable, great for interviews |
| Cache | Redis | Industry-standard, fast, simple |
| Containerization | Docker | Standard for packaging applications |
| Orchestration | Kubernetes | De facto standard for container management |
| Server | Uvicorn | ASGI server for FastAPI |

---

## Core Concepts

### 1. REST API

**What is it?**
REST (Representational State Transfer) is an architectural style for designing networked applications. It uses standard HTTP methods to perform operations on resources.

**Key Principles:**
- **Stateless**: Each request contains all necessary information
- **Resource-based**: URLs represent resources (`/users/123`)
- **Standard methods**: GET (read), POST (create), PUT (update), DELETE (delete)
- **Status codes**: 200 (success), 404 (not found), 500 (error)

**Why REST?**
- Simple and widely understood
- Works with any client (web, mobile, IoT)
- Stateless nature enables easy scaling
- HTTP caching can be leveraged

**In This Project:**
```python
# Example endpoints:
GET  /health              # Check if API is running
POST /agent/task          # Send a task to the agent
GET  /agent/tools         # List available tools
GET  /cache/stats         # View cache statistics
```

### 2. AI Agents

**What is an Agent?**
An agent is a system that autonomously decides which actions to take to accomplish a goal. Unlike a traditional API where you call specific endpoints, you tell an agent what you want, and it figures out how to do it.

**Agent vs API:**
| Aspect | Traditional API | Agent |
|--------|----------------|-------|
| Interface | Fixed endpoints | Natural language |
| Logic | Deterministic | Decision-making |
| Routing | Client chooses | Agent chooses |
| Flexibility | Low | High |

**How Agents Work:**
```
1. Receive task: "What's the weather in SF?"
2. Analyze intent: Weather information needed
3. Select tool: Weather API tool
4. Execute tool: Call weather function with "SF"
5. Format response: "The weather in San Francisco is sunny, 68°F"
```

**Real-World Examples:**
- ChatGPT function calling
- GitHub Copilot
- Virtual assistants (Alexa, Siri)
- Customer service bots

**In This Project:**
Our simplified agent uses pattern matching instead of LLMs to demonstrate the concept:
- Calculator: Mathematical operations
- Weather: Weather information (mocked)
- Search: Knowledge base lookup
- Time: Current date/time

### 3. Caching with Redis

**What is Caching?**
Storing frequently-accessed data in fast storage (RAM) to avoid slow operations like database queries or API calls.

**Why Redis?**
- **Speed**: All data in RAM (microsecond latency)
- **Simple**: Key-value pairs, easy to use
- **Rich**: Lists, sets, sorted sets, streams
- **Reliable**: Used by Twitter, GitHub, Stack Overflow

**Caching Strategy (Cache-Aside):**
```
1. Check cache for data
2. If found (cache hit): Return immediately
3. If not found (cache miss):
   a. Fetch from source (database, API)
   b. Store in cache for next time
   c. Return data
```

**Key Concepts:**
- **TTL (Time To Live)**: How long data stays cached
- **Hit Rate**: % of requests served from cache (higher is better)
- **Eviction**: Removing data when cache is full (LRU, LFU)

**When to Cache:**
- Expensive database queries
- External API responses
- Computed results
- Session data

### 4. Docker (Containerization)

**What is Docker?**
Docker packages your application and all its dependencies into a container that runs consistently anywhere.

**Container vs Virtual Machine:**
| Aspect | Container | Virtual Machine |
|--------|-----------|----------------|
| Size | MBs | GBs |
| Startup | Seconds | Minutes |
| Isolation | Process-level | Hardware-level |
| Efficiency | High | Lower |

**Dockerfile Stages:**
```dockerfile
# Stage 1: Builder (compile, install dependencies)
FROM python:3.11-slim as builder
# ... install build tools, dependencies

# Stage 2: Runtime (only what's needed to run)
FROM python:3.11-slim
# ... copy from builder, run as non-root
```

**Benefits:**
- **Consistency**: "Works on my machine" → "Works everywhere"
- **Isolation**: Apps don't interfere with each other
- **Portability**: Same container runs anywhere
- **Efficiency**: Share OS kernel, lightweight

### 5. Kubernetes (Orchestration)

**What is Kubernetes?**
Kubernetes (K8s) is a container orchestration platform that automates deployment, scaling, and management of containerized applications.

**Why Kubernetes?**
- **Auto-scaling**: Adjust replicas based on load
- **Self-healing**: Restart failed containers
- **Load balancing**: Distribute traffic across pods
- **Rolling updates**: Deploy without downtime
- **Service discovery**: Apps find each other automatically

**Core Components:**

| Component | Purpose | Analogy |
|-----------|---------|---------|
| Pod | Runs containers | A server |
| Deployment | Manages pods | Ensures you have right number of servers |
| Service | Network endpoint | Load balancer |
| ConfigMap | Configuration | Config files |
| Ingress | External access | Reverse proxy |
| HPA | Auto-scaling | Adding servers based on traffic |

**Architecture:**
```
Internet
  ↓
Ingress (nginx)
  ↓
Service (load balancer)
  ↓
Pods (replicas: 2-10)
  ↓
Containers (API, agent logic)
  ↓
Redis (cache)
```

---

## Architecture

### System Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                         Internet                            │
└────────────────────────┬────────────────────────────────────┘
                         │
                    ┌────▼─────┐
                    │ Ingress  │ (nginx / AWS ALB)
                    │  :443    │
                    └────┬─────┘
                         │
            ┌────────────┴────────────┐
            │                         │
       ┌────▼─────┐             ┌────▼─────┐
       │   API    │             │   API    │
       │   Pod    │◄───────────►│   Pod    │
       │  :8000   │             │  :8000   │
       └────┬─────┘             └────┬─────┘
            │                         │
            └────────────┬────────────┘
                         │
                    ┌────▼─────┐
                    │  Redis   │
                    │  :6379   │
                    └──────────┘
```

### Request Flow

1. **Client** makes HTTP request to `api.example.com/agent/task`
2. **Ingress** receives request, terminates SSL, routes to API service
3. **Service** load-balances to one of the API pods
4. **API Pod** receives request:
   - Checks Redis cache for previous result
   - If cache hit: Return immediately
   - If cache miss: Execute agent logic
5. **Agent** analyzes task, selects tool, executes
6. **Response** is cached in Redis and returned to client

### Data Flow

```
┌─────────┐     POST /agent/task      ┌─────────────┐
│ Client  │ ────────────────────────► │     API     │
└─────────┘                            └──────┬──────┘
                                              │
                                    Check cache for result
                                              │
                                         ┌────▼─────┐
                                         │  Redis   │
                                         └────┬─────┘
                                              │
                                    Cache miss? Execute agent
                                              │
                                    ┌─────────▼─────────┐
                                    │  Agent (analyze)  │
                                    │   Select tool     │
                                    │  Execute tool     │
                                    └─────────┬─────────┘
                                              │
                                    Store result in cache
                                              │
                                         ┌────▼─────┐
                                         │  Redis   │
                                         └──────────┘
```

---

## Quick Start

### Option 1: Local Python (Simplest)

**Requirements:**
- Python 3.11+
- Redis server

```bash
# 1. Install Redis (macOS)
brew install redis
brew services start redis

# 2. Install Python dependencies
pip install -r requirements.txt

# 3. Run the API
uvicorn app.main:app --reload

# 4. Access the API
# - API: http://localhost:8000
# - Docs: http://localhost:8000/docs
# - Health: http://localhost:8000/health
```

### Option 2: Docker Compose (Recommended)

**Requirements:**
- Docker Desktop

```bash
# 1. Start all services (API + Redis)
docker-compose up --build

# 2. Access the API
# - API: http://localhost:8000
# - Docs: http://localhost:8000/docs

# 3. View logs
docker-compose logs -f api

# 4. Stop services
docker-compose down
```

### Option 3: Kubernetes (Most Realistic)

**Requirements:**
- Kubernetes cluster (Minikube, Kind, or cloud provider)
- kubectl CLI

```bash
# 1. Start local cluster (Minikube)
minikube start

# 2. Build Docker image
eval $(minikube docker-env)  # Use Minikube's Docker
docker build -t interview-prep-api:latest .

# 3. Deploy to Kubernetes
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/redis-deployment.yaml
kubectl apply -f k8s/api-deployment.yaml
kubectl apply -f k8s/hpa.yaml

# 4. Access the API
kubectl port-forward service/interview-prep-api 8000:80 -n interview-prep

# 5. View resources
kubectl get all -n interview-prep

# 6. View logs
kubectl logs -f deployment/interview-prep-api -n interview-prep

# 7. Clean up
kubectl delete namespace interview-prep
```

---

## Detailed Explanations

### REST API Endpoints

#### `GET /health`
**Purpose:** Health check endpoint
**Use Case:** Kubernetes liveness/readiness probes, monitoring
**Response:**
```json
{
  "status": "healthy",
  "message": "API is running",
  "cache_connected": true
}
```

#### `POST /agent/task`
**Purpose:** Send a task to the agent
**Request:**
```json
{
  "task": "Calculate 15 + 27",
  "context": {
    "user_id": "123"
  }
}
```
**Response:**
```json
{
  "result": "The result is: 42",
  "tool_used": "calculator",
  "cached": false
}
```

#### `GET /agent/tools`
**Purpose:** List available tools
**Response:**
```json
{
  "count": 4,
  "tools": [
    {
      "name": "calculator",
      "description": "Performs mathematical calculations",
      "parameters": ["expression"]
    },
    ...
  ]
}
```

### Agent System

**How It Works:**

1. **Intent Recognition**: Analyze task to understand what user wants
   ```python
   if any(word in task_lower for word in ["calculate", "compute", "math"]):
       selected_tool = "calculator"
   ```

2. **Parameter Extraction**: Extract relevant data from task
   ```python
   match = re.search(r'[\d\s\+\-\*/\(\)\.]+', task)
   if match:
       params["expression"] = match.group().strip()
   ```

3. **Tool Execution**: Call the appropriate tool
   ```python
   result = tool.execute(**params)
   ```

4. **Response Formatting**: Return user-friendly response
   ```python
   return {
       "result": result,
       "tool_used": selected_tool
   }
   ```

**Production Agents:**
In real-world systems (ChatGPT, Copilot), steps 1-2 use Large Language Models:
```python
# Pseudo-code for LLM-powered agent
response = openai.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": task}],
    tools=available_tools  # LLM chooses which tool to call
)
```

### Caching Strategy

**Cache Key Design:**
```python
cache_key = f"task:{request.task}"
# Examples:
# task:Calculate 5 + 3
# task:What's the weather in NYC?
```

**TTL Selection:**
```python
cache.set(cache_key, result, ttl=300)  # 5 minutes
```

**Choosing TTL:**
- Rapidly changing data: 5-60 seconds
- Stable data: 5-15 minutes
- Static content: Hours or no expiration

**Hit Rate Optimization:**
1. Cache frequently-accessed data
2. Set appropriate TTL (balance freshness vs hits)
3. Monitor hit rate (aim for >80%)
4. Invalidate on updates

---

## Interview Talking Points

### REST API

**Q: What is REST?**
> REST is an architectural style for APIs that uses HTTP methods (GET, POST, PUT, DELETE) to perform operations on resources. It's stateless, meaning each request contains all necessary information, and uses standard HTTP status codes.

**Q: Why use FastAPI over Flask/Django?**
> FastAPI provides automatic request validation using type hints, generates interactive API documentation (Swagger), has async support for better performance, and is one of the fastest Python frameworks. It's production-ready and used by companies like Netflix and Uber.

**Q: How would you version an API?**
> Common approaches: URL versioning (`/api/v1/users`), header versioning (`Accept: application/vnd.api.v2+json`), or query parameter (`/users?version=2`). URL versioning is most explicit and widely used.

### Agent Systems

**Q: What's the difference between an API and an agent?**
> A traditional API has fixed endpoints that the client must know and call specifically. An agent receives a natural language request, understands the intent, decides which tool(s) to use, and handles the complexity internally. It's more flexible but adds latency and complexity.

**Q: How do LLM agents decide which tool to use?**
> Modern agents pass tool descriptions to an LLM along with the user's request. The LLM analyzes both and returns a function call with parameters. The system then executes that function. This is called "function calling" or "tool use" in systems like ChatGPT and Claude.

**Q: What are the challenges with agent systems?**
> Reliability (LLMs can make mistakes), latency (multiple LLM calls), cost (API fees), security (sandboxing tool execution), and debugging (hard to trace reasoning). Production systems need fallbacks, monitoring, and human-in-the-loop for critical operations.

### Caching

**Q: Why use Redis instead of in-memory caching?**
> In-memory caching (like Python dictionaries) only works in a single process. With multiple application instances (common in production), each has its own cache, reducing hit rate. Redis is shared across all instances, providing a centralized cache. It also persists across restarts and supports advanced data structures.

**Q: What's the CAP theorem?**
> CAP states distributed systems can only guarantee 2 of 3: Consistency (all nodes see same data), Availability (always responds), Partition tolerance (works despite network failures). Redis prioritizes Consistency and Partition tolerance.

**Q: Cache invalidation strategies?**
> 1) TTL-based (automatic expiration), 2) Active invalidation (clear cache when data updates), 3) Versioning (include version in cache key), 4) Tagging (group related cache entries). Cache invalidation is notoriously difficult - keep it simple when possible.

### Docker

**Q: How is Docker different from a VM?**
> VMs virtualize hardware and run a full OS (slow startup, GBs of size). Containers share the host OS kernel and virtualize at the OS level (fast startup, MBs of size). Containers are more efficient but provide less isolation than VMs.

**Q: Explain multi-stage builds.**
> Multi-stage builds use multiple FROM statements. Early stages compile code and install build dependencies. The final stage copies only what's needed to run. This produces smaller, more secure images by excluding build tools from the production image.

**Q: Security best practices for containers?**
> Run as non-root user, use official base images, scan for vulnerabilities, minimize layers, don't store secrets in images, use read-only filesystems where possible, set resource limits, and keep images updated.

### Kubernetes

**Q: What problem does Kubernetes solve?**
> Kubernetes automates deployment, scaling, and management of containerized applications. It handles service discovery, load balancing, self-healing (restarts failed containers), rolling updates, auto-scaling, and resource allocation across a cluster of machines.

**Q: Explain Pod, Deployment, Service.**
> - Pod: Smallest unit, runs one or more containers
> - Deployment: Manages desired state (how many pods, which version)
> - Service: Stable network endpoint for accessing pods (pods are ephemeral, services are stable)

**Q: How does service discovery work?**
> Kubernetes provides internal DNS. Services get DNS names like `<service>.<namespace>.svc.cluster.local`. Pods can use service names directly (e.g., `redis` resolves to the Redis service). When a request is made, it's load-balanced to healthy pods matching the service's selector.

**Q: Liveness vs Readiness probes?**
> - Liveness: Is the container alive? If fails, K8s restarts it. Use for deadlocks, unrecoverable errors.
> - Readiness: Is the container ready for traffic? If fails, K8s removes from service endpoints (no restart). Use for temporary issues like warming up or waiting for dependencies.

**Q: How does HPA work?**
> Horizontal Pod Autoscaler monitors metrics (CPU, memory, custom) every 15s. It calculates desired replicas: `ceil(currentReplicas * currentMetric / targetMetric)`. If different from current, it updates the Deployment's replica count, which creates/deletes pods.

---

## AWS & Cloud Integration

### How This Project Maps to AWS

| Local Component | AWS Service | Purpose |
|----------------|-------------|---------|
| Kubernetes | EKS (Elastic Kubernetes Service) | Managed Kubernetes |
| Docker Registry | ECR (Elastic Container Registry) | Store Docker images |
| Redis | ElastiCache for Redis | Managed Redis |
| Ingress | ALB (Application Load Balancer) | External access, SSL |
| Persistent Storage | EBS (Elastic Block Store) | Pod volumes |
| ConfigMap/Secret | Systems Manager Parameter Store | Configuration |
| Monitoring | CloudWatch | Logs, metrics, alarms |
| DNS | Route 53 | Domain management |

### Production Architecture on AWS

```
Route 53 (DNS)
  ↓
CloudFront (CDN, optional)
  ↓
WAF (Web Application Firewall)
  ↓
ALB (Application Load Balancer)
  ↓
EKS Cluster
  ├── API Pods (Auto-scaling 2-10)
  ├── Redis (ElastiCache)
  └── Monitoring (CloudWatch)
  ↓
RDS (Database, if needed)
```

### AWS EKS Deployment Steps

```bash
# 1. Create EKS cluster
eksctl create cluster \
  --name interview-prep \
  --region us-east-1 \
  --nodegroup-name standard-workers \
  --node-type t3.medium \
  --nodes 3

# 2. Build and push image to ECR
aws ecr create-repository --repository-name interview-prep-api
docker tag interview-prep-api:latest <account>.dkr.ecr.us-east-1.amazonaws.com/interview-prep-api:latest
docker push <account>.dkr.ecr.us-east-1.amazonaws.com/interview-prep-api:latest

# 3. Update image in k8s/api-deployment.yaml to use ECR image

# 4. Install AWS Load Balancer Controller
helm install aws-load-balancer-controller eks/aws-load-balancer-controller \
  -n kube-system \
  --set clusterName=interview-prep

# 5. Deploy application
kubectl apply -f k8s/

# 6. Ingress creates ALB automatically (check with: kubectl get ingress)
```

### AWS Services Explained

**EKS (Elastic Kubernetes Service):**
- Managed Kubernetes control plane
- AWS handles master nodes, etcd, API server
- You manage worker nodes (or use Fargate for serverless)
- Integrates with AWS services (IAM, VPC, CloudWatch)

**ElastiCache for Redis:**
- Managed Redis service
- Automatic failover with Multi-AZ
- Automated backups
- Scaling (add read replicas)
- No server management

**ALB (Application Load Balancer):**
- Layer 7 (HTTP/HTTPS) load balancer
- Path-based and host-based routing
- SSL/TLS termination (use ACM for free certs)
- Integrates with WAF for security
- Auto-scaling

**CloudWatch:**
- Centralized logging (container logs)
- Metrics (CPU, memory, custom metrics)
- Alarms (alert on thresholds)
- Dashboards (visualize metrics)

---

## Production Considerations

### What's Missing (Intentionally Simplified)

This is a learning project. Production systems need:

#### 1. Authentication & Authorization
```python
# Add to FastAPI
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.post("/agent/task")
async def execute_task(token: str = Depends(oauth2_scheme)):
    # Verify token, check permissions
    ...
```

#### 2. Rate Limiting
```python
from slowapi import Limiter

limiter = Limiter(key_func=get_remote_address)

@app.post("/agent/task")
@limiter.limit("100/minute")
async def execute_task():
    ...
```

#### 3. Monitoring & Observability
- Structured logging (JSON logs)
- Distributed tracing (Jaeger, AWS X-Ray)
- Metrics (Prometheus, CloudWatch)
- Error tracking (Sentry)

#### 4. Database
```python
# Add PostgreSQL for persistent data
from sqlalchemy import create_engine

engine = create_engine("postgresql://user:pass@host/db")
```

#### 5. Message Queue
```python
# For asynchronous tasks
from celery import Celery

app = Celery('tasks', broker='redis://localhost:6379')

@app.task
def process_task(task_id):
    # Long-running task
    ...
```

#### 6. CI/CD Pipeline

```yaml
# .github/workflows/deploy.yml
name: Deploy
on:
  push:
    branches: [main]
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Build and push Docker image
      - name: Deploy to EKS
```

#### 7. Security Enhancements
- Secrets management (AWS Secrets Manager, Vault)
- Network policies (restrict pod-to-pod traffic)
- Pod security policies
- Image scanning (Trivy, Clair)
- RBAC (Role-Based Access Control)

#### 8. Data Persistence
- PersistentVolumes for stateful data
- Regular backups
- Disaster recovery plan

#### 9. High Availability
- Multi-region deployment
- Database replication
- Redis Sentinel/Cluster
- Circuit breakers

### Scaling Considerations

**Traffic Growth:**
```
1-10 users:     Single instance, local Redis
10-1000 users:  2-3 instances, shared Redis
1000+ users:    Auto-scaling (HPA), Redis cluster
10000+ users:   Multiple regions, CDN, read replicas
```

**Cost Optimization:**
- Use Spot Instances for non-critical workloads
- Right-size resources (start small, scale up)
- Scale down during off-hours
- Use S3 for static assets (cheaper than serving from API)
- Monitor and optimize database queries

---

## Testing

### Manual Testing

```bash
# Health check
curl http://localhost:8000/health

# Execute agent task
curl -X POST http://localhost:8000/agent/task \
  -H "Content-Type: application/json" \
  -d '{
    "task": "Calculate 15 + 27",
    "context": {}
  }'

# List tools
curl http://localhost:8000/agent/tools

# Cache stats
curl http://localhost:8000/cache/stats

# Clear cache
curl -X DELETE http://localhost:8000/cache/clear
```

### Automated Tests

```python
# tests/test_api.py
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_agent_calculator():
    response = client.post("/agent/task", json={
        "task": "Calculate 10 + 5"
    })
    assert response.status_code == 200
    assert "15" in response.json()["result"]
    assert response.json()["tool_used"] == "calculator"
```

Run tests:
```bash
pytest tests/
```

---

## Learning Resources

### Books
- "Designing Data-Intensive Applications" by Martin Kleppmann
- "Kubernetes in Action" by Marko Lukša
- "Building Microservices" by Sam Newman

### Online
- FastAPI Documentation: https://fastapi.tiangolo.com
- Kubernetes Docs: https://kubernetes.io/docs
- Redis Documentation: https://redis.io/docs
- AWS EKS Workshop: https://www.eksworkshop.com

### Practice
- LeetCode (algorithms)
- System Design Primer: https://github.com/donnemartin/system-design-primer
- AWS Free Tier: https://aws.amazon.com/free

---

## Interview Questions to Prepare

### Architecture
- Design a URL shortener
- Design Instagram
- Design a rate limiter
- How would you scale this API to 1M users?

### Kubernetes
- How do you deploy without downtime?
- What happens if a node fails?
- How do you handle secrets?
- Explain the pod lifecycle

### System Design
- What are the tradeoffs of microservices vs monolith?
- How do you ensure data consistency?
- Explain CAP theorem with examples
- How do you handle cascading failures?

---

## Next Steps

After mastering this project:

1. **Add Real LLM Integration**: Use OpenAI or Anthropic API for actual agent intelligence
2. **Implement Database**: Add PostgreSQL for persistent data
3. **Build Frontend**: React/Vue.js interface
4. **Add Observability**: Prometheus + Grafana for monitoring
5. **Multi-Region**: Deploy to multiple AWS regions
6. **Load Testing**: Use k6 or Locust to test at scale

---

## License

MIT License - feel free to use for learning and interviews!

## Contributing

This is a learning project, but improvements are welcome! Focus on:
- Better explanations
- More interview questions
- Additional deployment targets (GCP, Azure)
- Real-world examples

---

**Built for interview preparation. Good luck! 🚀**
