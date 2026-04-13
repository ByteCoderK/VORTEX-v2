from openai import OpenAI

# Stable, deterministic key ordering
keys = {
    "KEY_1": "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",
    "KEY_2": "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",
    "KEY_3": "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",
    "KEY_4": "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"
}

ordered_keys = [keys[k] for k in sorted(keys.keys())]


def create_client(api_key):
    try:
        return OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key
        )
    except Exception as e:
        print("Client init error:", e)
        return None


def ask_ai(query, a=None, b=None):
    if not query:
        query = input("You: ")

    for i, key in enumerate(ordered_keys):
        try:
            client = create_client(key)
            if client is None:
                continue

            completion = client.chat.completions.create(
                model="nvidia/nemotron-3-super-120b-a12b:free",
                messages=[
                    {
  "role": "system",
  "content": "You are ATLAS, an intelligent, composed, and highly capable AI assistant. Your personality is similar to JARVIS: confident yet respectful, efficient, precise, and subtly witty without being sarcastic. You give clear, concise answers and take initiative when needed. You keep a calm, professional tone at all times, like an advanced AI designed to assist its operator with mission-level reliability. You do not ramble or over-explain unless asked."
},
                    { "role": "user", "content": query }
                ],
                extra_headers={
                    "X-Title": "VORTEX",
                    "HTTP-Referer": "http://localhost"
                }
            )

            response = completion.choices[0].message.content
            return f"{response}"

        except Exception as e:
            print(f"Key {i} failed:", e)
            continue

    return "All models failed."