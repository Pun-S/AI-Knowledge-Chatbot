import os
import requests
from embeddings_store import search

HF_API_KEY = os.getenv("HF_API_KEY")
if not HF_API_KEY:
    raise ValueError("Missing Hugging Face API key. Set HF_API_KEY environment variable.")

HF_API_URL = "https://api-inference.huggingface.co/models/HuggingFaceH4/zephyr-7b-beta"
HF_HEADERS = {"Authorization": f"Bearer {HF_API_KEY}"}

# Store recent conversation only
conversation_history = []

MAX_HISTORY_TURNS = 3
MAX_CHARS_CONTEXT = 1500

def truncate_text(text, max_chars=MAX_CHARS_CONTEXT):
    return text[:max_chars] if len(text) > max_chars else text

def ask_bot(query):
    # Search top 3 relevant chunks
    relevant_chunks = search(query, k=3)
    context = truncate_text("\n".join(relevant_chunks))

    # Keep only the last N turns of conversation
    recent_history = conversation_history[-MAX_HISTORY_TURNS:]
    history_text = "\n".join(
        [f"User: {msg['user']}\nBot: {msg['bot']}" for msg in recent_history]
    )
    history_text = truncate_text(history_text)

    # Build prompt
    prompt = (
        f"You are a helpful assistant. Use conversation history and document context.\n\n"
        f"Conversation History:\n{history_text}\n\n"
        f"Document Context:\n{context}\n\n"
        f"Question: {query}"
    )

    payload = {
        "inputs": prompt,
        "parameters": {"max_new_tokens": 200}
    }

    response = requests.post(HF_API_URL, headers=HF_HEADERS, json=payload)

    try:
        data = response.json()
        if isinstance(data, dict) and "error" in data:
            return f"HF API Error: {data['error']}"
        answer = data[0]['generated_text']

        # Save to memory
        conversation_history.append({"user": query, "bot": answer})
        return answer
    except Exception as e:
        return f"Error: {str(e)}"

def reset_memory():
    global conversation_history
    conversation_history = []