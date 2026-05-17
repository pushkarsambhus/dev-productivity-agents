import os
import anthropic

_client = None


def _get_client() -> anthropic.Anthropic:
    global _client
    if _client is None:
        api_key = os.environ.get("ANTHROPIC_API_KEY")
        if not api_key:
            raise EnvironmentError("ANTHROPIC_API_KEY environment variable not set.")
        _client = anthropic.Anthropic(api_key=api_key)
    return _client


def _call(system: str, user: str, max_tokens: int = 2048) -> str:
    client = _get_client()
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=max_tokens,
        system=system,
        messages=[{"role": "user", "content": user}],
    )
    return response.content[0].text.strip()


def summarize_email(email: dict) -> str:
    system = (
        "You are an assistant that summarizes emails concisely. "
        "Give a 2-3 sentence summary: who sent it, what they want or are saying, "
        "and any action required. Be direct."
    )
    user = (
        f"From: {email['from']}\n"
        f"Subject: {email['subject']}\n"
        f"Date: {email['date']}\n\n"
        f"{email['body']}"
    )
    return _call(system, user, max_tokens=300)


def summarize_inbox(emails: list[dict]) -> str:
    system = (
        "You are an assistant that summarizes an email inbox. "
        "Give a brief overview: how many emails, the main topics or senders, "
        "and highlight anything that looks urgent or needs a reply. "
        "Use bullet points. Be concise."
    )
    lines = []
    for i, e in enumerate(emails, 1):
        lines.append(f"{i}. From: {e['from']} | Subject: {e['subject']} | {e['snippet']}")
    user = "\n".join(lines)
    return _call(system, user, max_tokens=500)


def draft_reply(email: dict, thread: list[dict], instruction: str = "") -> str:
    system = (
        "You are an AI assistant writing email replies on behalf of the user. "
        "Write in a professional yet natural tone. Match the formality of the original email. "
        "Do not include a subject line. Do not add placeholders like [Your Name] — "
        "end naturally. Output only the reply body text, nothing else."
    )
    thread_text = ""
    for msg in thread:
        thread_text += f"\n--- From: {msg['from']} ({msg['date']}) ---\n{msg['body']}\n"

    user_instruction = f"\nAdditional instruction: {instruction}" if instruction else ""
    user = (
        f"Email thread:\n{thread_text}\n"
        f"The most recent email is from: {email['from']}\n"
        f"Subject: {email['subject']}\n"
        f"Write a reply to the most recent email in the thread.{user_instruction}"
    )
    return _call(system, user, max_tokens=800)


def compose_email(to: str, intent: str, context: str = "") -> tuple[str, str]:
    """Returns (subject, body)."""
    system = (
        "You are an AI assistant composing emails on behalf of the user. "
        "Write professionally and naturally. "
        "Output exactly two sections separated by a blank line: "
        "first line is the subject (no 'Subject:' prefix), then a blank line, then the body. "
        "Do not include any other text or labels."
    )
    ctx = f"\nAdditional context: {context}" if context else ""
    user = f"To: {to}\nWhat I want to communicate: {intent}{ctx}\n\nWrite the email."
    raw = _call(system, user, max_tokens=800)

    lines = raw.split("\n", 1)
    subject = lines[0].strip()
    body = lines[1].strip() if len(lines) > 1 else ""
    return subject, body


def suggest_action(email: dict) -> str:
    system = (
        "You are an inbox assistant. Given an email, suggest the most appropriate action: "
        "reply, archive, forward, or no action needed. "
        "Give a one-line suggestion and a brief reason."
    )
    user = (
        f"From: {email['from']}\n"
        f"Subject: {email['subject']}\n\n"
        f"{email['body'][:1000]}"
    )
    return _call(system, user, max_tokens=150)
