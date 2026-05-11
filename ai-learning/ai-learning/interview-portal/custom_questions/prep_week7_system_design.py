"""
Coding Interview Prep — Week 7: System Design
=============================================
Covers: How the Internet Works, SQL vs NoSQL, Scaling & Load Balancing,
        Caching (Redis), URL Shortener, Notification System, CAP Theorem
"""

NAME        = "Week 7: System Design"
DESCRIPTION = "Databases, caching, scaling, CAP theorem, URL shortener, notification systems"
ICON        = "🏗️"

CONCEPTS = [
    {
        "title": "System Design Framework",
        "explanation": """System design interviews test your ability to design large-scale systems. Use this framework every time:

**Step 1 — Clarify requirements (5 min)**
- Functional: what does the system DO?
- Non-functional: scale, latency, availability, consistency

**Step 2 — Estimate scale (2 min)**
- Users: DAU, requests/sec
- Storage: data size × users × time
- Bandwidth: request size × requests/sec

**Step 3 — High-level design**
- Client → Load Balancer → App Servers → Cache → Database
- Draw boxes and arrows first, explain as you go

**Step 4 — Deep dive**
- Pick the hardest component and explain it in detail
- Database schema, API design, caching strategy

**Step 5 — Identify bottlenecks**
- Single points of failure, hot spots, scaling limits

**Key numbers to memorize:**
| | Value |
|--|--|
| 1 million requests/day | ~12 requests/sec |
| 1 billion requests/day | ~12,000 requests/sec |
| 1 KB × 1M users | 1 GB |
| SSD read | ~0.1ms |
| Network round trip | ~100ms |""",
        "gotchas": [
            "Always clarify requirements before designing — interviewers want to see you ask.",
            "Back-of-envelope math matters — estimate scale before choosing SQL vs NoSQL.",
            "Availability = uptime %. 99.99% = 52 min downtime/year.",
        ],
        "videos": [
            {"title": "System Design Interview Framework (Gaurav Sen)", "url": "https://www.youtube.com/watch?v=xpDnVSmNFX0", "source": "YouTube"},
            {"title": "System Design Fundamentals (ByteByteGo)", "url": "https://www.youtube.com/watch?v=i53Gi_K3o7I", "source": "YouTube"},
            {"title": "System Design Interview Course (Udemy — Frank Kane)", "url": "https://www.udemy.com/course/system-design-interview-prep/", "source": "Udemy"},
        ],
    },
    {
        "title": "Databases, Caching & Scaling",
        "explanation": """**SQL vs NoSQL:**
- SQL (Postgres, MySQL): ACID, joins, complex queries, relational data
- NoSQL (MongoDB, DynamoDB, Cassandra): flexible schema, horizontal scale, high write throughput

**Indexing:** B-tree index turns O(n) scan → O(log n). Trade-off: faster reads, slower writes.

**Caching (Redis/Memcached):**
```
Client → App Server → Cache (Redis) → Database
                    ↗ cache hit (fast)
                    ↘ cache miss → DB → update cache
```
- Cache-aside (lazy loading): app checks cache, loads from DB on miss
- Write-through: write to cache AND DB simultaneously
- TTL: time-to-live — auto-expire stale data
- LRU eviction: remove least recently used when cache is full

**Scaling:**
- Vertical (scale up): bigger machine — simple, has ceiling
- Horizontal (scale out): more machines — needs load balancer, stateless services
- Database sharding: split data across multiple DB instances by shard key
- Read replicas: route reads to replicas, writes to primary

**CAP Theorem:** In a distributed system, pick 2:
- Consistency: all nodes see same data
- Availability: every request gets a response
- Partition tolerance: works despite network failures

Since P is unavoidable, choose: **CP** (banks, strong consistency) or **AP** (social feeds, eventual consistency).""",
        "gotchas": [
            "CAP: you always have P. The real choice is C vs A during a partition.",
            "Cache invalidation is hard — stale data is a real problem. Design TTL carefully.",
            "Sharding key choice is critical — bad keys cause hot spots (uneven load).",
        ],
        "videos": [
            {"title": "CAP Theorem (ByteByteGo)", "url": "https://www.youtube.com/watch?v=RTA13VPqM7g", "source": "YouTube"},
            {"title": "Database Scaling (Gaurav Sen)", "url": "https://www.youtube.com/watch?v=kKjm4ehYiMs", "source": "YouTube"},
            {"title": "Caching Strategies (ByteByteGo)", "url": "https://www.youtube.com/watch?v=6FyXURRVmR0", "source": "YouTube"},
            {"title": "System Design Interview Course (Udemy)", "url": "https://www.udemy.com/course/system-design-interview-prep/", "source": "Udemy"},
        ],
    },
]

QUESTIONS = [

    # ══════════════════════════════════════════════════════════════════
    # INTERNET / HTTP
    # ══════════════════════════════════════════════════════════════════
    {
        "type": "mcq",
        "difficulty": "easy",
        "topic": "HTTP & Internet Basics",
        "question": (
            "What is the difference between HTTP status codes 401 and 403?"
        ),
        "options": [
            "A) 401 = server error, 403 = client error",
            "B) 401 = Unauthorized (not authenticated), 403 = Forbidden (authenticated but not allowed)",
            "C) 401 = rate limited, 403 = not found",
            "D) They are interchangeable — both mean access denied",
        ],
        "correct_answer": "B) 401 = Unauthorized (not authenticated), 403 = Forbidden (authenticated but not allowed)",
        "explanation": (
            "401 Unauthorized: the request lacks valid authentication credentials. "
            "The client should provide credentials (login first). "
            "403 Forbidden: the server understood the request, the user IS authenticated, "
            "but they don't have permission. Logging in won't help. "
            "Common interview question for backend/API roles. "
            "Other important codes: 200 OK, 201 Created, 400 Bad Request, 404 Not Found, 500 Internal Server Error."
        ),
        "remember": "401 = not logged in. 403 = logged in but no permission. 404 = not found. 500 = server bug.",
    },

    # ══════════════════════════════════════════════════════════════════
    # DATABASES
    # ══════════════════════════════════════════════════════════════════
    {
        "type": "mcq",
        "difficulty": "easy",
        "topic": "SQL vs NoSQL",
        "question": (
            "When would you choose a NoSQL database (like MongoDB or DynamoDB) over a relational SQL database?"
        ),
        "options": [
            "A) When you need ACID transactions and complex joins",
            "B) When data has a flexible or frequently changing schema, or you need horizontal scaling at massive volume",
            "C) When you need strong consistency above all else",
            "D) NoSQL is always faster — choose it by default",
        ],
        "correct_answer": "B) When data has a flexible or frequently changing schema, or you need horizontal scaling at massive volume",
        "explanation": (
            "NoSQL shines for: flexible/dynamic schemas (user-generated content), "
            "horizontal scaling across many machines, very high write throughput, "
            "denormalized data access patterns. "
            "SQL shines for: relational data with joins, ACID transactions (financial systems), "
            "complex queries, strong consistency requirements. "
            "In interviews, always justify your database choice with trade-offs — never 'always use X'."
        ),
        "remember": "NoSQL = flexible schema, horizontal scale, high throughput. SQL = ACID, joins, complex queries. Trade-off, not winner.",
    },
    {
        "type": "mcq",
        "difficulty": "medium",
        "topic": "Database Indexing",
        "question": (
            "A table has 10 million rows. A query 'SELECT * FROM orders WHERE customer_id = 123' is slow. "
            "What is the most effective fix?"
        ),
        "options": [
            "A) Add more RAM to the database server",
            "B) Add an index on the customer_id column",
            "C) Rewrite the query using a JOIN",
            "D) Switch to a NoSQL database",
        ],
        "correct_answer": "B) Add an index on the customer_id column",
        "explanation": (
            "Without an index, the database does a full table scan (O(n)) — reading all 10M rows. "
            "An index on customer_id creates a B-tree structure allowing O(log n) lookup. "
            "Indexes trade write speed (index must be updated) and storage for read speed. "
            "This is one of the most common performance questions in backend interviews. "
            "Know the trade-off: indexes speed up reads but slow down writes."
        ),
        "remember": "Index = B-tree lookup O(log n) vs full scan O(n). Trade-off: faster reads, slower writes, more storage.",
    },

    # ══════════════════════════════════════════════════════════════════
    # CACHING
    # ══════════════════════════════════════════════════════════════════
    {
        "type": "mcq",
        "difficulty": "medium",
        "topic": "Caching & Redis",
        "question": (
            "What is a cache eviction policy, and what does LRU (Least Recently Used) do?"
        ),
        "options": [
            "A) LRU evicts the most recently accessed item to keep popular items",
            "B) LRU evicts the item that was least recently accessed — assuming it's least likely to be needed again",
            "C) LRU is a database replication strategy, not a cache policy",
            "D) LRU evicts the item with the lowest value",
        ],
        "correct_answer": "B) LRU evicts the item that was least recently accessed — assuming it's least likely to be needed again",
        "explanation": (
            "When a cache is full and a new item needs to be stored, the eviction policy decides what to remove. "
            "LRU removes the item that hasn't been accessed for the longest time. "
            "Intuition: if you haven't used something recently, you probably won't need it soon. "
            "Other policies: LFU (Least Frequently Used), FIFO, TTL (time-to-live). "
            "Redis supports multiple eviction policies. LRU is the most commonly asked in interviews."
        ),
        "remember": "LRU evicts the least recently accessed item. Cache full → remove oldest-accessed. Redis, Memcached use LRU.",
    },
    {
        "type": "mcq",
        "difficulty": "medium",
        "topic": "Scaling",
        "question": (
            "What is the difference between horizontal scaling (scale out) and vertical scaling (scale up)?"
        ),
        "options": [
            "A) Horizontal = add more CPU/RAM to one machine. Vertical = add more machines",
            "B) Horizontal = add more machines. Vertical = add more CPU/RAM to one machine",
            "C) They are the same — just different terms for the same concept",
            "D) Horizontal scaling only applies to databases, vertical to web servers",
        ],
        "correct_answer": "B) Horizontal = add more machines. Vertical = add more CPU/RAM to one machine",
        "explanation": (
            "Vertical scaling (scale up): bigger machine — more CPU, RAM, faster disk. Simple but has a ceiling. "
            "Horizontal scaling (scale out): more machines — distribute load. No hard ceiling but requires "
            "stateless services, load balancing, and distributed systems coordination. "
            "Modern systems prefer horizontal scaling for web tier (stateless) and "
            "vertical for databases initially, then sharding for horizontal. "
            "This is fundamental system design vocabulary — know it cold."
        ),
        "remember": "Scale UP = bigger machine. Scale OUT = more machines. Horizontal preferred for web tier (stateless).",
    },

    # ══════════════════════════════════════════════════════════════════
    # CAP THEOREM
    # ══════════════════════════════════════════════════════════════════
    {
        "type": "mcq",
        "difficulty": "hard",
        "topic": "CAP Theorem",
        "question": (
            "According to the CAP theorem, in the presence of a network partition (P), "
            "a distributed system must choose between which two properties?"
        ),
        "options": [
            "A) Consistency and Availability",
            "B) Consistency and Performance",
            "C) Availability and Durability",
            "D) Consistency and Scalability",
        ],
        "correct_answer": "A) Consistency and Availability",
        "explanation": (
            "CAP: Consistency (all nodes see the same data), Availability (every request gets a response), "
            "Partition tolerance (system works despite network failures between nodes). "
            "Network partitions are unavoidable in distributed systems, so P is always assumed. "
            "The real choice: CP (consistent but may reject requests during partition — HBase, ZooKeeper) "
            "vs AP (available but may return stale data — Cassandra, DynamoDB). "
            "Always follow up with: what are the business requirements? Financial transactions need CP."
        ),
        "remember": "CAP: P is given. Choose CP (consistent, may timeout) or AP (available, may be stale). Match to business need.",
    },

    # ══════════════════════════════════════════════════════════════════
    # URL SHORTENER DESIGN
    # ══════════════════════════════════════════════════════════════════
    {
        "type": "mcq",
        "difficulty": "hard",
        "topic": "System Design — URL Shortener",
        "question": (
            "You're designing a URL shortener (like bit.ly). "
            "Which approach best generates unique short codes at scale?"
        ),
        "options": [
            "A) Auto-increment integer ID encoded to Base62",
            "B) MD5 hash of the long URL, take first 7 characters",
            "C) Random UUID for each URL",
            "D) Sequential alphabetic strings (aa, ab, ac...)",
        ],
        "correct_answer": "A) Auto-increment integer ID encoded to Base62",
        "explanation": (
            "Base62 (0-9, a-z, A-Z) encoding of an auto-increment ID is the standard approach: "
            "7 characters of Base62 gives 62^7 = ~3.5 trillion unique codes. "
            "MD5 has collision risk and produces a 32-char hash that you truncate — collision probability increases. "
            "UUID is 128 bits — much longer than needed for short codes. "
            "The core design: write API generates ID, encodes to Base62, stores (short → long) in DB. "
            "Redirect API: look up short code → 301/302 redirect to long URL."
        ),
        "remember": "URL shortener = auto-increment ID → Base62 encode. 7 chars = 3.5T combos. Redirect = DB lookup + 301.",
    },
]
