from core.NeuralCore import *
from router.router import route_command
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import asyncio
import httpx
import os
from pathlib import Path

url = os.getenv("render_url")
frontend_origins = os.getenv("FRONTEND_ORIGINS", "")

app = FastAPI()
LOG_PATH = Path("vortex_debug.log")

allowed_origins = [
    origin.strip()
    for origin in frontend_origins.split(",")
    if origin.strip()
]

if not allowed_origins:
    allowed_origins = [
        "http://localhost:3000",
        "http://127.0.0.1:5500",
    ]


@app.get("/ping")
@app.post("/ping")
def ping():
    return {"status": "alive"}

async def keep_awake():
    if not url:
        print("render_url is not set. Skipping keep-awake task.")
        return

    async with httpx.AsyncClient() as client:
        while True:
            try:
                await client.get(url)
                print("Keep-alive ping sent.")
            except Exception as e:
                print(f"Keep-alive ping failed: {e}")
            await asyncio.sleep(840)  # 15 minutes


@app.on_event("startup")
async def startup_event():
    asyncio.create_task(keep_awake())

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Query(BaseModel):
    query: str


async def log_streamer():
    LOG_PATH.touch(exist_ok=True)

    with LOG_PATH.open("r", encoding="utf-8", errors="ignore") as f:
        f.seek(0, 2)  # move to end
        while True:
            line = f.readline()
            if not line:
                await asyncio.sleep(0.2)
                continue
            yield f"data: {line.rstrip()}\n\n"

@app.get("/stream_logs")
def stream_logs():
    return StreamingResponse(
        log_streamer(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )

@app.post("/ask")
def ask(payload: Query):
    response = route_command(payload.query, payload.query.lower())
    RawOutput=response
    if RawOutput is None:
        q=payload.query
        print (f"route_command returned None for query={q}")
        FinalOutput = ""
        return {"ATLAS": FinalOutput}

    if isinstance(RawOutput, str):
        return {"ATLAS": RawOutput}
    try:
        items = list(RawOutput)
    except TypeError:
        FinalOutput = str(RawOutput)
    else:
        FinalOutput = " ".join(str(item) for item in items if item is not None)
    return {"ATLAS": FinalOutput}
