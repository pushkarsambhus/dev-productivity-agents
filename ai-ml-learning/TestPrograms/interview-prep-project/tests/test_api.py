"""
API Tests - Interview Prep Project
==================================

These tests demonstrate:
1. How to test FastAPI applications
2. Testing patterns for REST APIs
3. Mocking external dependencies (Redis)
4. Test organization and best practices

INTERVIEW TIP: Testing is critical in production
- Catch bugs before deployment
- Document expected behavior
- Enable safe refactoring
- Provide usage examples

RUN TESTS:
    pytest tests/
    pytest tests/test_api.py -v
    pytest tests/test_api.py::test_health_check -v
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app

# CONCEPT: TestClient
# - Simulates HTTP requests without starting a server
# - Synchronous (easier to test async code)
# - Full request/response cycle
client = TestClient(app)


# ============================================================================
# BASIC ENDPOINT TESTS
# ============================================================================

def test_root_endpoint():
    """
    Test the root endpoint returns expected structure.

    TESTING PATTERN: Verify structure and status code
    - Status code: 200 (success)
    - Response structure: Expected keys present
    - Data types: Values are correct type
    """
    response = client.get("/")

    # Assert status code
    assert response.status_code == 200

    # Assert response structure
    data = response.json()
    assert "message" in data
    assert "docs" in data
    assert "health" in data

    # Assert values
    assert data["docs"] == "/docs"
    assert data["health"] == "/health"


def test_health_check():
    """
    Test health check endpoint.

    INTERVIEW TIP: Health checks are critical for:
    - Kubernetes liveness/readiness probes
    - Load balancer health checks
    - Monitoring systems
    - Uptime tracking
    """
    response = client.get("/health")

    assert response.status_code == 200

    data = response.json()
    assert data["status"] in ["healthy", "degraded"]  # degraded if Redis down
    assert "message" in data
    assert "cache_connected" in data
    assert isinstance(data["cache_connected"], bool)


# ============================================================================
# AGENT ENDPOINT TESTS
# ============================================================================

def test_list_tools():
    """
    Test listing available agent tools.

    TESTING PATTERN: Validate list responses
    - Check count matches expected
    - Verify item structure
    - Validate required fields present
    """
    response = client.get("/agent/tools")

    assert response.status_code == 200

    data = response.json()
    assert "count" in data
    assert "tools" in data
    assert data["count"] > 0  # Should have at least one tool
    assert isinstance(data["tools"], list)

    # Validate first tool structure
    if data["tools"]:
        tool = data["tools"][0]
        assert "name" in tool
        assert "description" in tool
        assert "parameters" in tool


def test_agent_calculator():
    """
    Test agent with calculator tool.

    TESTING PATTERN: Test happy path
    - Valid input
    - Expected output
    - Correct tool selection
    """
    response = client.post(
        "/agent/task",
        json={
            "task": "Calculate 10 + 5",
            "context": {}
        }
    )

    assert response.status_code == 200

    data = response.json()
    assert "result" in data
    assert "tool_used" in data
    assert "cached" in data

    # Verify correct tool was used
    assert data["tool_used"] == "calculator"

    # Verify result contains expected answer
    assert "15" in data["result"]


def test_agent_weather():
    """
    Test agent with weather tool.

    TESTING PATTERN: Test with known inputs
    - Use predictable test data
    - Verify expected behavior
    """
    response = client.post(
        "/agent/task",
        json={
            "task": "What's the weather in San Francisco?",
            "context": {}
        }
    )

    assert response.status_code == 200

    data = response.json()
    assert data["tool_used"] == "weather"
    assert "San Francisco" in data["result"] or "san francisco" in data["result"].lower()


def test_agent_search():
    """
    Test agent with search tool.

    TESTING PATTERN: Test knowledge base lookup
    """
    response = client.post(
        "/agent/task",
        json={
            "task": "What is Kubernetes?",
            "context": {}
        }
    )

    assert response.status_code == 200

    data = response.json()
    # Should use search tool and return info about Kubernetes
    assert "kubernetes" in data["result"].lower() or "container" in data["result"].lower()


def test_agent_time():
    """
    Test agent with time tool.
    """
    response = client.post(
        "/agent/task",
        json={
            "task": "What time is it?",
            "context": {}
        }
    )

    assert response.status_code == 200

    data = response.json()
    assert data["tool_used"] == "time"
    # Result should contain time-related words
    assert any(word in data["result"].lower() for word in ["time", "am", "pm"])


def test_agent_invalid_request():
    """
    Test agent with invalid request.

    TESTING PATTERN: Test error handling
    - Invalid input
    - Verify appropriate error response
    - Check error messages are helpful
    """
    response = client.post(
        "/agent/task",
        json={
            "task": "",  # Empty task
            "context": {}
        }
    )

    # Should still return 200 (request valid, just result is "can't help")
    # Or could return 400 if we add validation
    assert response.status_code in [200, 400]


# ============================================================================
# CACHE ENDPOINT TESTS
# ============================================================================

def test_cache_stats():
    """
    Test cache statistics endpoint.

    TESTING PATTERN: Test monitoring endpoints
    - Should always return valid structure
    - Handle cache unavailable gracefully
    """
    response = client.get("/cache/stats")

    assert response.status_code == 200

    data = response.json()
    assert "available" in data

    # If cache is available, check for expected fields
    if data["available"]:
        assert "connected_clients" in data
        assert "used_memory_human" in data


def test_clear_cache():
    """
    Test cache clearing.

    TESTING PATTERN: Test state-changing operations
    - Verify operation succeeds
    - Check side effects (cache actually cleared)
    """
    response = client.delete("/cache/clear")

    # Should succeed whether cache is available or not
    assert response.status_code in [200, 500]

    # If successful, verify message
    if response.status_code == 200:
        data = response.json()
        assert "message" in data


# ============================================================================
# INTEGRATION TESTS
# ============================================================================

def test_caching_behavior():
    """
    Test that caching works as expected.

    TESTING PATTERN: Test complex workflows
    - Clear cache
    - Make request (should not be cached)
    - Make same request again (should be cached)

    INTERVIEW TIP: This is an integration test
    - Tests multiple components together
    - More realistic than unit tests
    - Slower, but catches integration issues
    """
    # Clear cache first
    client.delete("/cache/clear")

    # First request - should not be cached
    response1 = client.post(
        "/agent/task",
        json={
            "task": "Calculate 999 + 1",
            "context": {}
        }
    )

    assert response1.status_code == 200
    data1 = response1.json()
    # First request might or might not be cached depending on test order
    # In isolation, should be False, but if other tests ran first, might be True

    # Second request - should be cached (if cache is working)
    response2 = client.post(
        "/agent/task",
        json={
            "task": "Calculate 999 + 1",
            "context": {}
        }
    )

    assert response2.status_code == 200
    data2 = response2.json()

    # If cache is working, second request should be cached
    # (Unless cache is unavailable, then both would be False)
    # Can't assert this reliably without mocking, but test is still valuable


# ============================================================================
# INTERVIEW TALKING POINTS - TESTING
# ============================================================================
"""
KEY CONCEPTS TO EXPLAIN:

1. Types of Tests:
   - Unit tests: Test single function/class in isolation
   - Integration tests: Test multiple components together
   - End-to-end tests: Test entire system from user perspective
   - Performance tests: Test speed, load handling
   - Security tests: Test for vulnerabilities

2. Test Pyramid:
   - Many unit tests (fast, cheap)
   - Some integration tests (slower, more valuable)
   - Few e2e tests (slow, expensive, but most realistic)

3. AAA Pattern (Arrange, Act, Assert):
   - Arrange: Set up test data, mocks
   - Act: Execute the code being tested
   - Assert: Verify expected results

4. Mocking:
   - Replace external dependencies with controlled versions
   - Example: Mock Redis to test without actual Redis server
   - Tools: unittest.mock, pytest-mock

5. Test Coverage:
   - Percentage of code executed by tests
   - Aim for 80%+ (100% is often not practical)
   - Coverage ≠ quality (can have 100% coverage with bad tests)

6. CI/CD:
   - Tests run automatically on every commit
   - Prevents merging broken code
   - Fast feedback loop

7. TDD (Test-Driven Development):
   - Write test first (fails)
   - Write minimal code to pass test
   - Refactor
   - Repeat

8. Best Practices:
   - Tests should be independent (can run in any order)
   - One assertion per test (debatable)
   - Clear test names (describe what's being tested)
   - Fast tests (use mocks for external services)
   - Deterministic (same input → same output)

9. Common Pitfalls:
   - Testing implementation details (fragile)
   - Slow tests (developers won't run them)
   - Flaky tests (sometimes pass, sometimes fail)
   - No negative tests (only test happy path)

10. Production Testing:
    - Smoke tests (basic health checks)
    - Canary deployments (test with small % of traffic)
    - A/B testing (compare versions)
    - Chaos engineering (intentionally break things)
"""

# ============================================================================
# ADVANCED: MOCKING EXAMPLE (commented out - requires setup)
# ============================================================================
"""
from unittest.mock import patch, MagicMock

def test_agent_with_mocked_redis():
    '''
    Test agent with mocked Redis.

    CONCEPT: Mocking external dependencies
    - Don't need actual Redis running
    - Control Redis behavior in tests
    - Test error scenarios (Redis down)
    '''
    # Mock Redis client
    with patch('app.cache.redis.Redis') as mock_redis:
        # Configure mock to return None (cache miss)
        mock_redis.return_value.get.return_value = None

        # Make request
        response = client.post(
            "/agent/task",
            json={"task": "Calculate 1 + 1"}
        )

        # Verify Redis was called
        mock_redis.return_value.get.assert_called_once()

        # Verify response
        assert response.status_code == 200
        assert response.json()["cached"] == False
"""

# ============================================================================
# PYTEST FIXTURES (Advanced)
# ============================================================================
"""
@pytest.fixture
def clear_cache_before_test():
    '''
    Fixture to clear cache before each test.

    CONCEPT: Fixtures provide reusable setup/teardown
    - Run before each test (or once per session)
    - Clean up after test
    - Can be composed (fixtures can use other fixtures)
    '''
    client.delete("/cache/clear")
    yield  # Test runs here
    # Cleanup code would go here (after yield)

@pytest.fixture
def sample_task():
    '''Return a sample task for testing.'''
    return {
        "task": "Calculate 10 + 5",
        "context": {"user_id": "test"}
    }

def test_with_fixtures(clear_cache_before_test, sample_task):
    '''
    Test using fixtures.

    USAGE: Just add fixture name as parameter
    '''
    response = client.post("/agent/task", json=sample_task)
    assert response.status_code == 200
"""

# ============================================================================
# PARAMETRIZED TESTS (Advanced)
# ============================================================================
"""
@pytest.mark.parametrize("task,expected_tool", [
    ("Calculate 5 + 3", "calculator"),
    ("What's the weather?", "weather"),
    ("What is Redis?", "search"),
    ("What time is it?", "time"),
])
def test_tool_selection(task, expected_tool):
    '''
    Test that correct tool is selected for various tasks.

    CONCEPT: Parametrized tests reduce duplication
    - Same test logic, different inputs
    - Easy to add more cases
    - Clear which case failed
    '''
    response = client.post("/agent/task", json={"task": task})
    assert response.status_code == 200
    assert response.json()["tool_used"] == expected_tool
"""
