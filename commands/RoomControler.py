import requests
from fastapi import FastAPI, Request

app = FastAPI()
#
ESP8266_IP = "http://192.168.1.100"  # Replace with your actual ESP8266 IP

@app.get("/command")
async def handle_command(query: str):
    try:
        response = requests.get(f"{ESP8266_IP}/relay/on", timeout=3)
        if response.status_code == 200:
            return {"status": "Relay turned ON"}
        else:
            return {"status": "Failed to trigger relay", "code": response.status_code}
    except Exception as e:
        return {"status": "Error contacting ESP8266", "error": str(e)}
    