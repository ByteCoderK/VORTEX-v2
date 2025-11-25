import requests


def logic():
    while True:
        query = input("You: ")
        res = requests.post("https://vortex-v2.onrender.com/ask", json={"query": query})
        #print("RAW:", res.text)  
        data = res.json()
        #print("DEBUG:", data)  # Add this line to see raw response
        
        if "response" in data:
            api_res = "VORTEX:", data["response"]
            return {"response": data["response"]}
        else:
            print("VORTEX: Error",data.get("details","Unknown error"))        


if __name__ == '__main__':
    logic()
