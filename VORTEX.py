import requests

def logic():
    while True:
        query = input("You: ")
        res = requests.post("https://vortex-v2-7.onrender.com", json={"query": query})
        try:
            data = res.json()
            print("DEBUG:", data)  # Add this line to see raw response
            print("VORTEX:", data["response"])
        except Exception as e:
            print("❌ Failed to parse response:", e)
            print("Raw:", res.text)


if __name__ == '__main__':
    logic()
