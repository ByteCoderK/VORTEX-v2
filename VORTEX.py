import requests

def logic():
    while True:
        query = input("You: ")
        res = requests.post("https://your-vortex-url.onrender.com/ask", json={"query": query})
        print("VORTEX:", res.json()["response"])

if __name__ == '__main__':
    logic()
