# commands/ai.py

from openai import OpenAI

# Configure your OpenRouter client
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="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"  # Replace this with your actual API key
)

def ask_ai(query: str) -> str:
    try:
        completion = client.chat.completions.create(
            model="meta-llama/llama-3.3-8b-instruct:free",
            messages=[
                {
                    "role": "system",
                    "content": "You are VORTEX, a helpful voice-controlled assistant."
                },
                {
                    "role": "user",
                    "content": query  # <- This is how you pass the user question
                }
            ],
            extra_headers={
                "X-Title": "VORTEX",
                "HTTP-Referer": "http://localhost"  # Optional
            },
            extra_body={}
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"Sorry, I couldn't reach the AI: {str(e)}"
