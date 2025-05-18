import requests

def logic():
    while True:
        query = input("You: ")
        res = requests.post("https://vortex-v2-7.onrender.com", json={"query": query})
        
        data = res.json()
        print("DEBUG:", data)  # Add this line to see raw response
        print("VORTEX:", data["response"])
        


if __name__ == '__main__':
    logic()
