from fastapi import FastAPI
from pydantic import BaseModel
from router.router import route_command

app = FastAPI()

class Query(BaseModel):
    query: str

@app.post("/ask")
def ask(query: Query):
    query_text = query.query
    query_list = query_text.lower().split()

    try:
        response = route_command(query_text, query_list)
        if not response:
            response = "Sorry, I didn’t understand that."
    except Exception as e:
        response = f"Error: {str(e)}"

    return {"response": response}

@app.get("/")
def root():
    return {"message": "VORTEX API is online."}
