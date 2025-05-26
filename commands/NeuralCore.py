from openai import OpenAI

keys = {
    'KEY_1': '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',
    'KEY_2': "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",
    'KEY_3': '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',
}


# Configure your OpenRouter client


def ask_ai(query=None,CURRENT_key=keys["KEY_1"],first_call=True) -> str:
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
            model='meta-llama/llama-3.3-8b-instruct:free',
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
        print(response + "\t---> Powered By - " + "AI_" + str(model_keys.index(CURRENT_key)))
    except Exception as e:
        # Fallback logic: try next model
        current_index = model_keys.index(CURRENT_key)
        if current_index + 1 < len(model_keys):
            next_model_key = model_keys[current_index + 1]
            return ask_ai(query, next_model_key, first_call=False)
        else:
            print(f"All models failed..",e)
ask_ai()