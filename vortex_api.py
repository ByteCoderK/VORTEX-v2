from fastapi import FastAPI
from pydantic import BaseModel
from router.router import route_command
#
app = FastAPI()

class Query(BaseModel):
    query: str

@app.post("/ask")
def ask(payload: Query):
    response = route_command(payload.query, payload.query.lower().split())
    return {"response": response}
