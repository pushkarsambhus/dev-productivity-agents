import os
from openai import OpenAI
from utils.helper_functions import get_llm_response, print_llm_response

BASE_URL = os.getenv("OPENAI_BASE_URL", "http://localhost:11434/v1")
API_KEY  = os.getenv("OPENAI_API_KEY", "ollama")

client = OpenAI(base_url=BASE_URL, api_key=API_KEY)

answer = get_llm_response(
    client,
    "Explain embeddings in 3 beginner-friendly bullets.",
    model="llama3",  # swap to "llama3.2:3b" for faster replies
    system="You are a clear, concise teacher.",
    temperature=0.2,
)
print_llm_response(answer)