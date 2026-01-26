# ==============================================================================
# DOCKERFILE - Container Image Definition
# ==============================================================================
#
# WHAT IS DOCKER?
# Docker packages your application and all its dependencies into a "container"
# - Like a lightweight virtual machine
# - Runs consistently across different environments (dev, staging, prod)
# - Isolates applications from each other
# - Makes deployment predictable and repeatable
#
# ANALOGY: Docker is like a shipping container for software
# - Just as shipping containers standardized global trade
# - Docker containers standardize software deployment
#
# KEY CONCEPTS:
# - Image: A template (like a recipe)
# - Container: A running instance of an image (like a cake made from recipe)
# - Dockerfile: Instructions to build an image
# - Registry: Storage for images (Docker Hub, ECR, etc.)
#
# INTERVIEW TIP: Explain the difference:
# - Virtual Machine: Full OS, heavy (GBs), slow to start (minutes)
# - Container: Shared OS kernel, light (MBs), fast to start (seconds)
#
# ==============================================================================

# ------------------------------------------------------------------------------
# STAGE 1: Builder
# ------------------------------------------------------------------------------
# CONCEPT: Multi-stage builds
# - Separate build environment from runtime environment
# - Smaller final image (no build tools included)
# - More secure (fewer attack surfaces)
# - Faster deployments (less to download)

FROM python:3.11-slim as builder

# Set working directory
# CONCEPT: All subsequent commands run from this directory
WORKDIR /app

# Install system dependencies needed for building Python packages
# INTERVIEW TIP: Many Python packages need C compilers to install
# - gcc: C compiler
# - We use --no-install-recommends to keep image small
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (layer caching optimization)
# CONCEPT: Docker builds in layers
# - Each instruction creates a new layer
# - Layers are cached
# - If requirements.txt doesn't change, Docker reuses the cached layer
# - This makes rebuilds MUCH faster
COPY requirements.txt .

# Install Python dependencies
# CONCEPT: Using a virtual environment even in Docker
# - Keeps dependencies isolated
# - Makes it clear what's installed
# - pip --no-cache-dir: Don't store downloaded packages (saves space)
RUN pip install --no-cache-dir --user -r requirements.txt

# ------------------------------------------------------------------------------
# STAGE 2: Runtime
# ------------------------------------------------------------------------------
# CONCEPT: Start fresh with a clean base image
# - Copy only what we need from builder
# - No build tools in final image
# - Result: Smaller, more secure image

FROM python:3.11-slim

# Create a non-root user to run the application
# SECURITY BEST PRACTICE: Never run containers as root
# - If container is compromised, attacker has limited access
# - Principle of least privilege
RUN useradd -m -u 1000 appuser

WORKDIR /app

# Copy Python dependencies from builder stage
# CONCEPT: Multi-stage build - we only take what we need
COPY --from=builder /root/.local /home/appuser/.local

# Copy application code
COPY app/ ./app/

# Change ownership to non-root user
RUN chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Update PATH to include user-installed packages
ENV PATH=/home/appuser/.local/bin:$PATH

# Expose port 8000
# CONCEPT: Documentation - tells users which port the app uses
# NOTE: This doesn't actually publish the port, it's just documentation
# You still need to map ports when running: docker run -p 8000:8000
EXPOSE 8000

# Health check
# CONCEPT: Docker can periodically check if container is healthy
# - Useful for orchestration (K8s, Docker Swarm)
# - If health check fails, container can be restarted
# INTERVIEW TIP: In Kubernetes, this is replaced by liveness/readiness probes
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')"

# Command to run the application
# CONCEPT: CMD vs ENTRYPOINT
# - CMD: Can be overridden when running container
# - ENTRYPOINT: Always runs (CMD becomes arguments to it)
# - We use CMD for flexibility
#
# UVICORN: ASGI server that runs FastAPI
# - host 0.0.0.0: Listen on all network interfaces (not just localhost)
# - port 8000: Standard development port
# - In production, you might add:
#   --workers 4 (multiple worker processes)
#   --access-log (request logging)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

# ==============================================================================
# DOCKER COMMANDS CHEAT SHEET
# ==============================================================================
#
# Build the image:
#   docker build -t interview-prep-api .
#   (-t: tag/name the image)
#
# Run the container:
#   docker run -p 8000:8000 interview-prep-api
#   (-p: map host port 8000 to container port 8000)
#
# Run with environment variables:
#   docker run -p 8000:8000 -e REDIS_HOST=redis interview-prep-api
#   (-e: set environment variable)
#
# Run in background (detached):
#   docker run -d -p 8000:8000 interview-prep-api
#   (-d: detached mode)
#
# View running containers:
#   docker ps
#
# View logs:
#   docker logs <container-id>
#
# Stop container:
#   docker stop <container-id>
#
# Remove container:
#   docker rm <container-id>
#
# Remove image:
#   docker rmi interview-prep-api
#
# Execute command in running container:
#   docker exec -it <container-id> /bin/bash
#   (-it: interactive terminal)
#
# ==============================================================================
# INTERVIEW TALKING POINTS - DOCKER
# ==============================================================================
#
# 1. Why Docker?
#    - Consistency: Same environment everywhere
#    - Isolation: Apps don't interfere with each other
#    - Portability: Runs on any system with Docker
#    - Efficiency: Share OS kernel, lightweight
#
# 2. Docker vs VMs:
#    - VMs: Full OS, hardware virtualization, slow, heavy
#    - Containers: Shared kernel, OS-level virtualization, fast, light
#
# 3. Docker Architecture:
#    - Docker Client: CLI you use (docker run, docker build)
#    - Docker Daemon: Background service that manages containers
#    - Docker Registry: Stores images (Docker Hub, ECR)
#
# 4. Best Practices:
#    - Use official base images
#    - Multi-stage builds for smaller images
#    - Layer caching (copy requirements before code)
#    - Run as non-root user
#    - Use .dockerignore (like .gitignore)
#    - Pin versions (python:3.11, not python:latest)
#    - One process per container (usually)
#
# 5. Docker Compose:
#    - Tool for running multi-container applications
#    - Define services in docker-compose.yml
#    - Example: API + Redis + PostgreSQL
#    - One command to start everything: docker-compose up
#
# 6. Container Orchestration:
#    - Docker runs containers on one machine
#    - Orchestrators manage containers across many machines:
#      * Kubernetes (most popular)
#      * Docker Swarm (simpler, Docker-native)
#      * ECS (AWS-specific)
#
# 7. AWS Integration:
#    - ECR (Elastic Container Registry): Store Docker images
#    - ECS (Elastic Container Service): Run containers on AWS
#    - EKS (Elastic Kubernetes Service): Managed Kubernetes
#    - Fargate: Serverless container runtime
#
# 8. Production Considerations:
#    - Image scanning for vulnerabilities
#    - Secrets management (don't bake into image)
#    - Resource limits (CPU, memory)
#    - Logging and monitoring
#    - Image size optimization
#
# 9. Common Dockerfile Instructions:
#    - FROM: Base image
#    - RUN: Execute command during build
#    - COPY/ADD: Copy files into image
#    - WORKDIR: Set working directory
#    - ENV: Set environment variable
#    - EXPOSE: Document port
#    - CMD/ENTRYPOINT: Command to run
#    - USER: Switch user
#
# 10. Debugging Containers:
#     - docker logs: View application logs
#     - docker exec: Run commands in container
#     - docker inspect: Detailed container info
#     - docker stats: Resource usage
#
# ==============================================================================
