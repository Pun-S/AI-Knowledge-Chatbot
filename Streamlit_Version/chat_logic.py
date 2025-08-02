import os
from embeddings_store import search
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key=os.environ.get('HF_TOKEN'),
)

completion = client.chat.completions.create(
    model="HuggingFaceH4/zephyr-7b-beta:featherless-ai",
    messages=[
        {
            "role": "user",
            "content": "What is the capital of France?"
        }
    ],
)

def ask_bot(query):
    relevant_chunks = search(query)
    context = "\n".join(relevant_chunks)
    prompt = f"Answer based only on the context below:\n{context}\n\nQuestion: {query}"
    
    completion = client.chat.completions.create(
        model="HuggingFaceH4/zephyr-7b-beta:featherless-ai",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
    )

    try:
        return completion.choices[0].message
    except Exception:
        return "Error: Could not get a valid response from the model."