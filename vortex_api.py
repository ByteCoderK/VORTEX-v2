from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from router.router import route_command
from commands.NeuralCore import*
import asyncio
import httpx
import time 

app = FastAPI()
LOG_PATH = "vortex_debug.log"


@app.get("/ping")
def ping():
    return {"status": "alive"}

async def keep_awake():
    url = "https://vortex-v2.onrender.com/ping"
    async with httpx.AsyncClient() as client:
        while True:
            try:
                await client.get(url)
                print("Keep-alive ping sent.")
            except Exception as e:
                print(f"Keep-alive ping failed: {e}")
            await asyncio.sleep(900)  # 15 minutes


@app.on_event("startup")
async def startup_event():
    asyncio.create_task(keep_awake())

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


def log_streamer():
    with open(LOG_PATH, "r", encoding="utf-8", errors="ignore") as f:
        f.seek(0, 2)  # move to end
        while True:
            line = f.readline()
            if not line:
                time.sleep(0.2)
                continue
            yield f"data: {line}\n\n"

@app.get("/stream_logs")
def stream_logs():
    return StreamingResponse(log_streamer(), media_type="text/event-stream")

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