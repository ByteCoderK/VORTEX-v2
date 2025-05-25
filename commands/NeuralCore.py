from openai import OpenAI

# Configure your OpenRouter client
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="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"  # Replace this with your actual API key
)


aiModels = {
    'ai_I': 'meta-llama/llama-3.3-8b-instruct:free',
    'ai_II': "qwen/qwen3-32b:free",
    'ai_III': "mistralai/devstral-small:free",
    'ai_IV': "nousresearch/deephermes-3-mistral-24b-preview:free"
}


def ask_ai(query=None,model_key='ai_I',first_call=True) -> str:
    if first_call and not query:
        query = input("You: ")
    try:
        completion = client.chat.completions.create(
            model=aiModels[model_key],
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
        response = completion.choices[0].message.content
        return f"VORTEX: {response}"
    except Exception as e:
        print(f"Error with model {model_key}: {e}")
        # Fallback logic: try next model
        model_keys = list(aiModels.keys())
        current_index = model_keys.index(model_key)
        if current_index + 1 < len(model_keys):
            next_model_key = model_keys[current_index + 1]
            ask_ai(query,next_model_key)
        else:
            return "All models failed."

ask_ai()



