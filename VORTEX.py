import requests
import os

def required_env(name: str) -> str:
    value = os.getenv(name)
    if value is None or value.strip() == "":
        raise RuntimeError(f"Missing env var: {name}")
    return value
render_ask = required_env('render_ask')

def logic():
    while True:
        query = input("You: ")
        res = requests.post(render_ask, json={"query": query})
        data = res.json()

        if "response" in data:
            response_str = str(data["response"])
            print("VORTEX:", response_str)
            return {"response": response_str}
        else:
            print("VORTEX: Error", data.get("details", "Unknown error"))
if __name__ == '__main__':
    logic()