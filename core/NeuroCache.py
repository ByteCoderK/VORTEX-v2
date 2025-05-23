from openai import OpenAI
import json

MemoryCACHE = []

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="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"
)

def rememberMeProtocol(query: str) -> dict:
    try:
        completion = client.chat.completions.create(
            model="meta-llama/llama-3.3-8b-instruct:free",
            messages=[
                {
                    "role": "system",
                    "content": """Respond ONLY with pure JSON. Example outputs:
{"user_name": "John"} for names
{"country": "France"} for locations
{"preferences": ["pizza"]} for likes
{"reminders": ["Call mom"]} for tasks
{} for no data"""
                },
                {"role": "user", "content": query}
            ],
            temperature=0.0
        )
        
        # Get the raw response content
        response_text = completion.choices[0].message.content
        # Parse the JSON response
        response_data = json.loads(response_text)
        # Store in memory if not empty
        if response_data:
            MemoryCACHE.append(response_data)
        
        return response_data
        
    except json.JSONDecodeError:
        print("Received invalid JSON response")
        return {}
    except Exception as e:
        print(f"Error: {e}")
        return {}

while True:
    try:
        #query = input("You: ")
        if query.lower() in ('exit', 'quit'):
            print("Stored memories:", MemoryCACHE)
            break
            
        response = rememberMeProtocol(query)
        print("Response:", response)
        
    except KeyboardInterrupt:
        print("\nFinal memories:", MemoryCACHE)
        break

