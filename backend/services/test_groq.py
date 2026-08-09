import os

from dotenv import load_dotenv
from groq import Groq


load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise RuntimeError("GROQ_API_KEY was not found in .env")


client = Groq(api_key=api_key)


response = client.chat.completions.create(
    model="llama-3.1-8b-instant",
    messages=[
        {
            "role": "system",
            "content": (
                "You are a technical interviewer. "
                "Ask concise, challenging technical questions."
            )
        },
        {
            "role": "user",
            "content": (
                "Ask me one interview question about "
                "Retrieval-Augmented Generation."
            )
        }
    ],
)

print("\n===== GROQ RESPONSE =====\n")
print(response.choices[0].message.content)

