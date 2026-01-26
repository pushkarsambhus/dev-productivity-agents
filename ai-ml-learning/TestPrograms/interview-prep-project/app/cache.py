"""
Cache Manager - Redis Integration
==================================

WHAT IS CACHING?
Caching stores frequently-accessed data in fast storage (RAM) to avoid:
- Expensive database queries
- Slow API calls
- Redundant computations

ANALOGY: Like keeping frequently-used tools on your desk instead of
walking to the garage every time you need them.

WHY REDIS?
Redis (Remote Dictionary Server) is an in-memory data store that's:
- FAST: All data lives in RAM (microsecond latency)
- SIMPLE: Key-value pairs, easy to use
- RICH: Supports complex data structures (lists, sets, sorted sets)
- SCALABLE: Handles millions of operations per second
- PERSISTENT: Can save data to disk for durability

REAL-WORLD USE CASES:
1. Session storage: User login sessions
2. Caching: API responses, database query results
3. Rate limiting: Track API usage per user
4. Leaderboards: Gaming, social media (sorted sets)
5. Pub/Sub: Real-time messaging, notifications
6. Job queues: Background task processing

INTERVIEW TIP - CAP Theorem:
Distributed systems can only guarantee 2 of 3:
- Consistency: All nodes see same data
- Availability: System always responds
- Partition tolerance: Works despite network failures

Redis prioritizes: Consistency + Partition Tolerance (CP)
"""

import redis
import json
import logging
from typing import Any, Optional, Dict
import os

logger = logging.getLogger(__name__)


class CacheManager:
    """
    Manages caching operations using Redis.

    DESIGN PATTERNS:
    1. Singleton pattern: One cache manager for the entire app
    2. Graceful degradation: App works even if Redis is down
    3. Serialization: Convert Python objects to JSON for storage

    INTERVIEW TIP: In production, consider:
    - Connection pooling (reuse connections)
    - Retry logic (handle transient failures)
    - Circuit breaker (stop trying if Redis is down)
    - Monitoring (cache hit rate, latency)
    """

    def __init__(self):
        """
        Initialize cache manager.

        CONFIGURATION: Gets Redis connection details from environment variables.
        This is a best practice:
        - Never hardcode credentials
        - Different configs for dev/staging/prod
        - Easy to change without code updates

        KUBERNETES/DOCKER: Environment variables are set in:
        - Kubernetes ConfigMaps (non-sensitive config)
        - Kubernetes Secrets (passwords, API keys)
        - Docker Compose environment section
        """
        self.host = os.getenv("REDIS_HOST", "localhost")
        self.port = int(os.getenv("REDIS_PORT", "6379"))
        self.db = int(os.getenv("REDIS_DB", "0"))

        # Redis client (connection pool built-in)
        self.client: Optional[redis.Redis] = None

        # Track if cache is available (graceful degradation)
        self.available = False

    def connect(self):
        """
        Establish connection to Redis.

        CONCEPT: Connection pooling
        - Redis client maintains a pool of connections
        - Reuses connections instead of creating new ones
        - Improves performance and resource usage

        ERROR HANDLING: If Redis is unavailable:
        - Log the error (for debugging)
        - Set available=False (graceful degradation)
        - App continues working without cache
        """
        try:
            self.client = redis.Redis(
                host=self.host,
                port=self.port,
                db=self.db,
                decode_responses=True,  # Automatically decode bytes to strings
                socket_timeout=5,  # Don't wait forever for responses
                socket_connect_timeout=5,
                retry_on_timeout=True
            )

            # Test the connection
            self.client.ping()
            self.available = True
            logger.info(f"Connected to Redis at {self.host}:{self.port}")

        except redis.ConnectionError as e:
            logger.warning(f"Could not connect to Redis: {e}")
            logger.warning("Application will run without caching")
            self.available = False
        except Exception as e:
            logger.error(f"Unexpected error connecting to Redis: {e}")
            self.available = False

    def disconnect(self):
        """
        Close Redis connection.

        CONCEPT: Resource cleanup
        - Always close connections when shutting down
        - Prevents resource leaks
        - Important in containerized environments
        """
        if self.client:
            try:
                self.client.close()
                logger.info("Disconnected from Redis")
            except Exception as e:
                logger.error(f"Error disconnecting from Redis: {e}")
        self.available = False

    def ping(self) -> bool:
        """
        Check if Redis is available.

        USE CASE: Health checks
        - Kubernetes liveness/readiness probes
        - Monitoring systems
        - Circuit breaker pattern
        """
        if not self.client:
            return False
        try:
            return self.client.ping()
        except Exception as e:
            logger.error(f"Redis ping failed: {e}")
            self.available = False
            return False

    def get(self, key: str) -> Optional[Any]:
        """
        Get a value from cache.

        CONCEPT: Cache hit vs miss
        - Hit: Data found in cache (fast)
        - Miss: Data not in cache (need to fetch from source)

        RETURN: None if:
        - Key doesn't exist (cache miss)
        - Redis is unavailable
        - Deserialization fails

        INTERVIEW TIP: Cache hit rate is a key metric:
        - High hit rate (>80%): Cache is effective
        - Low hit rate (<50%): Review caching strategy
        """
        if not self.available or not self.client:
            return None

        try:
            value = self.client.get(key)
            if value is None:
                logger.debug(f"Cache miss: {key}")
                return None

            logger.debug(f"Cache hit: {key}")
            # Deserialize JSON string back to Python object
            return json.loads(value)

        except json.JSONDecodeError as e:
            logger.error(f"Failed to deserialize cached value for {key}: {e}")
            # Delete corrupt data
            self.delete(key)
            return None
        except Exception as e:
            logger.error(f"Error getting key {key}: {e}")
            return None

    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> bool:
        """
        Set a value in cache with optional TTL (Time To Live).

        TTL (Time To Live):
        - How long data stays in cache before expiring
        - Measured in seconds
        - Balances freshness vs performance

        CHOOSING TTL:
        - Rapidly changing data: Short TTL (seconds to minutes)
        - Stable data: Long TTL (hours to days)
        - Static data: No TTL (cache forever)

        EXAMPLES:
        - Stock prices: 5-60 seconds
        - User profiles: 5-15 minutes
        - Product catalogs: 1-24 hours
        - Static content: No expiration

        INTERVIEW TIP: Cache invalidation is one of the hardest problems
        in computer science. Strategies:
        1. TTL: Data expires automatically
        2. Active invalidation: Clear cache when data changes
        3. Versioning: Include version in cache key
        """
        if not self.available or not self.client:
            return False

        try:
            # Serialize Python object to JSON string
            value_json = json.dumps(value)

            if ttl:
                # Set with expiration
                self.client.setex(key, ttl, value_json)
                logger.debug(f"Cached {key} with TTL {ttl}s")
            else:
                # Set without expiration
                self.client.set(key, value_json)
                logger.debug(f"Cached {key} (no TTL)")

            return True

        except TypeError as e:
            logger.error(f"Value not JSON serializable for {key}: {e}")
            return False
        except Exception as e:
            logger.error(f"Error setting key {key}: {e}")
            return False

    def delete(self, key: str) -> bool:
        """
        Delete a key from cache.

        USE CASES:
        - Cache invalidation after data updates
        - Removing sensitive data
        - Clearing corrupt entries
        """
        if not self.available or not self.client:
            return False

        try:
            result = self.client.delete(key)
            logger.debug(f"Deleted {key}: {result}")
            return bool(result)
        except Exception as e:
            logger.error(f"Error deleting key {key}: {e}")
            return False

    def clear(self) -> bool:
        """
        Clear all keys in the current database.

        WARNING: Destructive operation!
        - Only use in development/testing
        - In production, be very careful
        - Consider using key patterns instead

        INTERVIEW TIP: Redis supports 16 databases (0-15)
        - Different apps can use different DBs
        - Or use key prefixes (e.g., "app1:user:123")
        """
        if not self.available or not self.client:
            return False

        try:
            self.client.flushdb()
            logger.info("Cache cleared")
            return True
        except Exception as e:
            logger.error(f"Error clearing cache: {e}")
            return False

    def get_stats(self) -> Dict[str, Any]:
        """
        Get cache statistics.

        METRICS TO MONITOR:
        - Memory usage: How much RAM Redis is using
        - Hit rate: Percentage of requests served from cache
        - Eviction rate: How often data is removed to free memory
        - Connection count: Number of clients connected

        INTERVIEW TIP: In AWS ElastiCache:
        - CloudWatch provides these metrics
        - Set alarms for high memory usage
        - Monitor evictions (might need larger instance)
        """
        if not self.available or not self.client:
            return {
                "available": False,
                "message": "Redis not connected"
            }

        try:
            info = self.client.info()
            stats = self.client.info("stats")

            return {
                "available": True,
                "connected_clients": info.get("connected_clients", 0),
                "used_memory_human": info.get("used_memory_human", "unknown"),
                "total_commands_processed": stats.get("total_commands_processed", 0),
                "keyspace_hits": stats.get("keyspace_hits", 0),
                "keyspace_misses": stats.get("keyspace_misses", 0),
                "hit_rate": self._calculate_hit_rate(
                    stats.get("keyspace_hits", 0),
                    stats.get("keyspace_misses", 0)
                )
            }
        except Exception as e:
            logger.error(f"Error getting cache stats: {e}")
            return {
                "available": False,
                "error": str(e)
            }

    def _calculate_hit_rate(self, hits: int, misses: int) -> str:
        """Calculate cache hit rate as a percentage."""
        total = hits + misses
        if total == 0:
            return "N/A (no requests yet)"
        rate = (hits / total) * 100
        return f"{rate:.2f}%"


# ============================================================================
# INTERVIEW TALKING POINTS - CACHING & REDIS
# ============================================================================
"""
KEY CONCEPTS TO EXPLAIN:

1. Why Cache?
   - Performance: Serve data faster (RAM vs disk/network)
   - Cost: Reduce expensive operations (DB queries, API calls)
   - Scalability: Handle more requests with same resources
   - Reliability: Serve cached data if backend is down

2. Cache Strategies:
   - Cache-Aside (Lazy Loading):
     * Check cache first
     * On miss, fetch from source and populate cache
     * What we implemented here

   - Write-Through:
     * Write to cache and database simultaneously
     * Always consistent but slower writes

   - Write-Behind (Write-Back):
     * Write to cache immediately
     * Write to database asynchronously
     * Fast but risk of data loss

3. Cache Eviction Policies:
   When cache is full, which data to remove?
   - LRU (Least Recently Used): Remove oldest accessed items
   - LFU (Least Frequently Used): Remove least popular items
   - TTL: Remove expired items
   - FIFO: Remove oldest items (by insertion time)

4. Redis Data Structures:
   - Strings: Simple key-value (what we used)
   - Hashes: Store objects/mappings
   - Lists: Ordered collections, queues
   - Sets: Unordered unique items
   - Sorted Sets: Ordered by score (leaderboards)
   - Streams: Log-like data structure

5. Redis in Production:
   - Persistence: RDB snapshots, AOF (Append-Only File)
   - Replication: Primary-replica for high availability
   - Clustering: Sharding data across nodes
   - Sentinel: Automatic failover

6. AWS Integration:
   - ElastiCache for Redis: Managed Redis service
     * Automatic backups
     * Multi-AZ replication
     * Automatic failover
     * Monitoring via CloudWatch
     * Scaling (vertical and horizontal)

   - Common pattern in AWS:
     * EC2/ECS/EKS runs your application
     * ElastiCache provides Redis cluster
     * RDS for persistent database
     * S3 for file storage

7. When NOT to Use Cache:
   - Frequently changing data (cache thrashing)
   - Data that must be 100% consistent
   - Large binary files (use CDN instead)
   - When cache miss penalty is low

8. Security Considerations:
   - Don't cache sensitive data (passwords, tokens)
   - Encrypt data in transit (TLS)
   - Network isolation (private VPC)
   - Authentication (Redis 6+ has ACLs)

9. Common Pitfalls:
   - Cache stampede: Many requests miss cache simultaneously
   - Stale data: Old cached data after updates
   - Memory overflow: Cache grows unbounded
   - Hot keys: One key gets too many requests

10. Monitoring & Debugging:
    - Cache hit rate (target >80%)
    - Memory usage (watch for near-full)
    - Evictions (data removed due to memory pressure)
    - Slow queries (use SLOWLOG)
    - Connection errors

11. Alternatives to Redis:
    - Memcached: Simpler, multi-threaded
    - DynamoDB DAX: AWS DynamoDB cache
    - Hazelcast: In-memory data grid
    - Apache Ignite: Distributed database
    - Application memory: Simplest, not shared
"""
