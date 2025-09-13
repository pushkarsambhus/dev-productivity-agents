from typing import Any, Dict, List, Optional

def print_llm_response(text: str) -> None:
    rule = "─" * min(80, max(20, len(text)))
    print(rule); print(text); print(rule)

def get_llm_response(
    client: Any,
    prompt: str,
    *,
    model: str = "llama3",
    system: Optional[str] = None,
    temperature: float = 0.3,
    max_tokens: Optional[int] = None,
    messages: Optional[List[Dict[str, str]]] = None,
) -> str:
    """OpenAI-compatible call (works with Ollama server)."""
    _messages: List[Dict[str, str]] = []
    if system:
        _messages.append({"role": "system", "content": system})
    if messages:
        _messages.extend(messages)
    else:
        _messages.append({"role": "user", "content": prompt})

    resp = client.chat.completions.create(
        model=model,
        messages=_messages,
        temperature=temperature,
        max_tokens=max_tokens,
    )
    return resp.choices[0].message.content.strip()