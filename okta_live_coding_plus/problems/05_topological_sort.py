from collections import Counter
import json
import re
from collections import defaultdict
from datetime import datetime, timedelta

def frequent_users(logs):
    counts = Counter(log["user"] for log in logs)
    return [user for user, count in counts.items() if count > 3]

def extract_user_data(api_responses):
    results = []
    for response in api_responses:
        try:
            data = json.loads(response)
            if data.get("status") == "active" and "@" in data.get("email", ""):
                results.append({"id": data["user_id"], "email": data["email"].lower()})
        except:
            continue
    return results



def prepare_documents_for_rag(document, chunk_size=200):
    text = re.sub(r'\s+', ' ', document).strip()
    sentences = re.split(r'[.!?]+', text)
    
    chunks, current = [], []
    for s in sentences:
        if sum(len(x) for x in current) + len(s) > chunk_size and current:
            chunks.append(' '.join(current))
            current = [s]
        else:
            current.append(s)
    
    if current:
        chunks.append(' '.join(current))
    return chunks

   

class RateLimiter:
    def __init__(self, max_calls, seconds):
        self.max_calls = max_calls
        self.window = timedelta(seconds=seconds)
        self.calls = defaultdict(list)
    
    def allow_request(self, user_id):
        now = datetime.now()
        cutoff = now - self.window
        self.calls[user_id] = [t for t in self.calls[user_id] if t > cutoff]
        
        if len(self.calls[user_id]) < self.max_calls:
            self.calls[user_id].append(now)
            return True
        return False

if __name__ == "__main__":
    # Example logs with repeated users; test frequent_users function
    """
    logs = [
        {"user": "Alice", "action": "login"},
        {"user": "Bob", "action": "login"},
        {"user": "Alice", "action": "logout"},
        {"user": "Charlie", "action": "login"},
        {"user": "Bob", "action": "logout"},
        {"user": "Alice", "action": "view"},
        {"user": "Alice", "action": "update"},
    ]
    print(frequent_users(logs))  # Should print ['Alice'] because Alice appears > 3 times
    """

    """api_responses = [
        '{"user_id": 1, "email": "alice@example.com", "status": "active"}',
        '{"user_id": 2, "email": "bob@example.com", "status": "inactive"}',
        '{"user_id": 1, "email": "alice@example.com", "status": "active"}',
        '{"user_id": 3, "email": "charlie@example.com", "status": "active"}',
    ]
    print(extract_user_data(api_responses))"""

    # Demo: prepare_documents_for_rag
    document = (
        "This is a test document. It contains some sentences. "
        "This is another sentence. This is a third sentence. "
        "Sometimes we need to split long paragraphs into chunks that fit model limits. "
        "We try not to break sentences so the chunks stay readable."
    )
    """
    print("\nChunks with chunk_size=80:")
    chunks_small = prepare_documents_for_rag(document, chunk_size=80)
    for i, c in enumerate(chunks_small, 1):
        print(f"{i}. ({len(c)} chars) {c}")

    print("\nChunks with chunk_size=200:")
    chunks_large = prepare_documents_for_rag(document, chunk_size=200)
    for i, c in enumerate(chunks_large, 1):
        print(f"{i}. ({len(c)} chars) {c}")

    # Demo: a single sentence longer than the limit becomes its own chunk (can exceed limit)
    very_long_sentence = (
        "ThisIsASingleVeryLongSentenceWithoutSpacesThatExceedsTheLimitSignificantlySoItCannotBeSplit "
        "and it continues even further to ensure the character count is well beyond a small chunk size."
    )
    print("\nSingle long sentence with chunk_size=60:")
    chunks_over = prepare_documents_for_rag(very_long_sentence + ".", chunk_size=60)
    for i, c in enumerate(chunks_over, 1):
        print(f"{i}. ({len(c)} chars) {c}")
    """

    # Demo: RateLimiter
    limiter = RateLimiter(max_calls=5, seconds=1)
    print(limiter.allow_request("user1"))  # True
    print(limiter.allow_request("user1"))  # True
    print(limiter.allow_request("user1"))  # True
    print(limiter.allow_request("user1"))  # True
    print(limiter.allow_request("user1"))  # False
    print(limiter.allow_request("user1"))  # True
    print(limiter.allow_request("user1"))  # True
    print(limiter.allow_request("user1"))  # True
    print(limiter.allow_request("user1"))  # True