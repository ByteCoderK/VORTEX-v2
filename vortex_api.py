from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from router.router import route_command
from commands.NeuralCore import*

app = FastAPI()

# Add CORS middleware - allow all origins (you can restrict if you want)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins - you can restrict to your domain here
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Query(BaseModel):
    query: str

@app.post("/ask")
def ask(payload: Query):
    response = route_command(payload.query, payload.query.lower())
    RawOutput=response
    FinalOutput = " ".join(
    try:
        [str(item) for item in RawOutput if item is not None]
    except Exception as E:
        print(f'ERROR <<< ',E)
)
    return {"ATLAS": FinalOutput}