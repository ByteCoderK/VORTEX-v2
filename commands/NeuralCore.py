from openai import OpenAI

keys = {
    'KEY_1': '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',
    'KEY_2': "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",
    'KEY_3': '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',
    'KEY_4': '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'
}
def ask_ai(query,CURRENT_key=keys["KEY_1"],first_call=True) -> str:
    model_keys = list(keys.values())
    client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=CURRENT_key
)
      # Replace this with your actual API key
    if first_call and not query:
        query = input("You: ")
    try:
        completion = client.chat.completions.create(
            model='kwaipilot/kat-coder-pro:free',
            messages=[
                {
                    "role": "system",
                    "content": "You are VORTEX, a helpful voice-controlled assistant."
                },
                {
                    "role": "user",
                    "content": query
                }
            ],
            extra_headers={
                "X-Title": "VORTEX",
                "HTTP-Referer": "http://localhost"
            },
            extra_body={}
        )
        response = completion.choices[0].message.content
        return response + "\t---> Powered By - " + "AI_" + str(model_keys.index(CURRENT_key))
    except Exception as e:
        # Fallback logic: try next model
        current_index = model_keys.index(CURRENT_key)
        if current_index + 1 < len(model_keys):
            next_model_key = model_keys[current_index + 1]
            return ask_ai(query, next_model_key, first_call=False)
        else:
            return f"All models failed..",e
