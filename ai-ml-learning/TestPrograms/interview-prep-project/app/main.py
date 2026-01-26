"""
FastAPI Application - REST API Fundamentals
===========================================

This file demonstrates core REST API concepts:
- Routes: URL patterns that map to functions
- Endpoints: Specific URLs that handle requests (GET, POST, etc.)
- Request/Response: How data flows in and out
- Error Handling: Managing failures gracefully

INTERVIEW TIP: REST APIs use HTTP methods to perform CRUD operations:
- GET: Read data (safe, no side effects)
- POST: Create new resources
- PUT: Update existing resources
- DELETE: Remove resources
"""

from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
import logging

# Import our custom agent and caching modules
from app.agent import SimpleAgent
from app.cache import CacheManager

# Configure logging for debugging and monitoring
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI application
# CONCEPT: FastAPI is a modern web framework that provides:
# - Automatic API documentation (Swagger UI)
# - Data validation using Python type hints
# - Async support for better performance
app = FastAPI(
    title="Interview Prep API",
    description="A learning project demonstrating REST APIs, Agents, and K8s",
    version="1.0.0"
)

# Initialize the agent and cache manager
# CONCEPT: Dependency injection - we create these once and reuse them
agent = SimpleAgent()
cache = CacheManager()


# ============================================================================
# REQUEST/RESPONSE MODELS
# ============================================================================
# CONCEPT: Pydantic models define the "shape" of data
# - Automatic validation: FastAPI checks incoming data matches the model
# - Type safety: Catches errors before they reach your business logic
# - Auto-documentation: Models appear in API docs


class TaskRequest(BaseModel):
    """
    Defines what data we expect when someone asks the agent to do something.

    INTERVIEW TIP: Using models instead of raw dicts provides:
    1. Validation: Ensures data is correct before processing
    2. Documentation: Auto-generates API docs
    3. IDE support: Autocomplete and type checking
    """
    task: str = Field(
        ...,  # ... means required
        description="The task to perform",
        example="What's the weather in San Francisco?"
    )
    context: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Additional context for the task",
        example={"user_id": "123", "preferences": {"units": "celsius"}}
    )


class TaskResponse(BaseModel):
    """Response from the agent after processing a task."""
    result: str = Field(description="The agent's response")
    tool_used: Optional[str] = Field(
        default=None,
        description="Which tool the agent decided to use"
    )
    cached: bool = Field(
        default=False,
        description="Whether this result came from cache"
    )


class HealthResponse(BaseModel):
    """Health check response."""
    status: str
    message: str
    cache_connected: bool


# ============================================================================
# API ENDPOINTS
# ============================================================================


@app.get("/", response_model=Dict[str, str])
async def root():
    """
    Root endpoint - the entry point of your API.

    CONCEPT: Health check endpoints are standard in production:
    - Kubernetes uses them to know if your app is running
    - Load balancers use them to route traffic
    - Monitoring systems check them for uptime

    INTERVIEW TIP: In AWS, ELB (Elastic Load Balancer) pings health endpoints
    to determine which instances are healthy.
    """
    return {
        "message": "Welcome to the Interview Prep API",
        "docs": "/docs",  # FastAPI auto-generates interactive documentation
        "health": "/health"
    }


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Health check endpoint for monitoring and orchestration.

    REAL-WORLD USE: In Kubernetes, this is used for:
    - Liveness probe: Is the app running?
    - Readiness probe: Is the app ready to serve traffic?

    In AWS ECS/EKS, health checks determine:
    - Whether to restart containers
    - Whether to route traffic to this instance
    """
    cache_status = cache.ping()

    return HealthResponse(
        status="healthy" if cache_status else "degraded",
        message="API is running",
        cache_connected=cache_status
    )


@app.post("/agent/task", response_model=TaskResponse)
async def execute_agent_task(request: TaskRequest):
    """
    Main agent endpoint - demonstrates how AI agents work.

    CONCEPT: An agent is different from a regular API because it:
    1. Analyzes the request to understand intent
    2. Decides which tool(s) to use
    3. Executes the appropriate function
    4. Returns a natural response

    INTERVIEW TIP: This is similar to how ChatGPT function calling works:
    - User sends a message
    - AI determines if it needs to call a function
    - Function executes and returns data
    - AI formats the response naturally

    CACHING: We cache results to avoid redundant work:
    - Faster response times
    - Reduced computational cost
    - Better user experience
    """
    try:
        logger.info(f"Received task: {request.task}")

        # Check cache first (common pattern in production)
        cache_key = f"task:{request.task}"
        cached_result = cache.get(cache_key)

        if cached_result:
            logger.info("Cache hit - returning cached result")
            return TaskResponse(
                result=cached_result["result"],
                tool_used=cached_result.get("tool_used"),
                cached=True
            )

        # Execute the task using the agent
        result = agent.execute(request.task, request.context)

        # Cache the result for future requests
        cache.set(cache_key, result, ttl=300)  # Cache for 5 minutes

        return TaskResponse(
            result=result["result"],
            tool_used=result.get("tool_used"),
            cached=False
        )

    except Exception as e:
        logger.error(f"Error processing task: {str(e)}")
        # CONCEPT: Proper error handling is critical
        # - Never expose internal errors to users
        # - Log details for debugging
        # - Return user-friendly messages
        raise HTTPException(
            status_code=500,
            detail=f"Failed to process task: {str(e)}"
        )


@app.get("/agent/tools")
async def list_available_tools():
    """
    List all available tools the agent can use.

    CONCEPT: Transparency in agent systems - users should know what's possible.

    INTERVIEW TIP: In production agent systems (like LangChain or AutoGPT):
    - Tools are registered in a tool registry
    - Each tool has a description for the AI to understand when to use it
    - Tools can be dynamically added or removed
    """
    tools = agent.get_available_tools()
    return {
        "count": len(tools),
        "tools": tools
    }


@app.get("/cache/stats")
async def get_cache_stats():
    """
    Get cache statistics.

    REAL-WORLD USE: In production, you'd monitor:
    - Cache hit rate (higher is better)
    - Memory usage
    - Eviction rate

    INTERVIEW TIP: Redis is often used in AWS with ElastiCache:
    - Managed Redis service
    - Automatic failover
    - Multi-AZ replication
    """
    stats = cache.get_stats()
    return stats


@app.delete("/cache/clear")
async def clear_cache():
    """
    Clear the entire cache.

    USE CASE: Useful for:
    - Forcing fresh data after updates
    - Testing
    - Resolving cache inconsistencies
    """
    try:
        cache.clear()
        return {"message": "Cache cleared successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to clear cache: {str(e)}"
        )


# ============================================================================
# STARTUP AND SHUTDOWN EVENTS
# ============================================================================


@app.on_event("startup")
async def startup_event():
    """
    Runs when the application starts.

    CONCEPT: Lifecycle hooks let you:
    - Initialize connections (databases, caches)
    - Load models or data
    - Start background tasks

    KUBERNETES TIP: This runs when the pod starts, before it receives traffic.
    """
    logger.info("Starting up the application...")
    cache.connect()
    logger.info("Application ready to serve requests")


@app.on_event("shutdown")
async def shutdown_event():
    """
    Runs when the application shuts down.

    CONCEPT: Graceful shutdown - clean up resources:
    - Close database connections
    - Finish in-flight requests
    - Save state if needed

    KUBERNETES TIP: K8s sends SIGTERM, waits for graceful shutdown,
    then sends SIGKILL if the app doesn't stop.
    """
    logger.info("Shutting down the application...")
    cache.disconnect()
    logger.info("Application shutdown complete")


# ============================================================================
# INTERVIEW TALKING POINTS
# ============================================================================
"""
KEY CONCEPTS TO EXPLAIN:

1. REST API Architecture:
   - Stateless: Each request contains all needed information
   - Resource-based: URLs represent resources (/users/123)
   - Standard HTTP methods: GET, POST, PUT, DELETE
   - Status codes: 200 OK, 404 Not Found, 500 Server Error

2. Why FastAPI?:
   - Type hints enable automatic validation
   - Async support for handling many concurrent requests
   - Auto-generated OpenAPI docs
   - Production-ready (used by Netflix, Uber)

3. Caching Strategy:
   - Check cache before expensive operations
   - Set appropriate TTL (Time To Live)
   - Cache invalidation is hard - be conservative

4. Error Handling:
   - Never expose stack traces to users
   - Log errors for debugging
   - Return meaningful HTTP status codes
   - Provide actionable error messages

5. Agent vs API:
   - API: Fixed endpoints, deterministic responses
   - Agent: Interprets intent, chooses tools dynamically
   - Agent adds flexibility but complexity

6. Production Considerations:
   - Authentication/Authorization (not shown for simplicity)
   - Rate limiting
   - Monitoring and logging
   - Graceful degradation (app works if cache is down)
"""
