from fastapi import FastAPI

app = FastAPI()

@app.post("/ask")
def ask(query: dict):
    return {"response": "This is VORTEX test response"}