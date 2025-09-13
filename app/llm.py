import os
def enrich_suggestions(log_text: str, base_suggestions: list[str]) -> list[str] | None:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return None
    return base_suggestions + ["Correlate errors with last successful build diff"]
