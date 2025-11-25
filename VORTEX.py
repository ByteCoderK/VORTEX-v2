import requests

def logic():
    while True:
        query = input("You: ")
        res = requests.post("https://vortex-v2.onrender.com/ask", json={"query": query})
        data = res.json()

        if "response" in data:
            # Force response to be a string
            response_str = str(data["response"])
            print("VORTEX:", response_str)  # Optional console log
            return {"response": response_str}  # This is proper JSON for browsers
        else:
            print("VORTEX: Error", data.get("details", "Unknown error"))

if __name__ == '__main__':
    logic()