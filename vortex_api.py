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
    # Handle None safely and log a simple warning
    if RawOutput is None:
        q=payload.query
        print (f"route_command returned None for query={q}")
        FinalOutput = ""
        return {"ATLAS": FinalOutput}

    if isinstance(RawOutput, str):
        return {"ATLAS": RawOutput}

# Otherwise try to iterate; if not iterable, convert to str
    try:
        items = list(RawOutput)
    except TypeError:
        FinalOutput = str(RawOutput)
    else:
        FinalOutput = " ".join(str(item) for item in items if item is not None)

    return {"ATLAS": FinalOutput}