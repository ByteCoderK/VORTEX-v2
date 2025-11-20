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
                model="kwaipilot/kat-coder-pro:free",
                messages=[
                    { "role": "system", "content": "You are ATLAS, a helpful voice-controlled assistant." },
                    { "role": "user", "content": query }
                ],
                extra_headers={
                    "X-Title": "VORTEX",
                    "HTTP-Referer": "http://localhost"
                }
            )

            response = completion.choices[0].message.content
            return f"{response}\t---> Powered By - AI_{i}"

        except Exception as e:
            print(f"Key {i} failed:", e)
            continue

    return "All models failed."