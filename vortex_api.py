from core.NeuralCore import *
from router.router import route_command
from fastapi import FastAPI
from fastapi import Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import asyncio
import httpx
import os
import logging
from pathlib import Path

url = os.getenv("render_url")

app = FastAPI()
LOG_PATH = Path("vortex_debug.log")
LOG_PATH.touch(exist_ok=True)

logger = logging.getLogger("vortex")
logger.setLevel(logging.INFO)

if not logger.handlers:
    formatter = logging.Formatter(
        "[%(asctime)s] %(levelname)s %(name)s: %(message)s"
    )

    file_handler = logging.FileHandler(LOG_PATH, encoding="utf-8")
    file_handler.setFormatter(formatter)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

@app.get("/ping")
@app.post("/ping")
def ping():
    logger.info("Health check received on /ping")
    return {"status": "alive"}

async def keep_awake():
    if not url:
        logger.warning("render_url is not set. Skipping keep-awake task.")
        return

    async with httpx.AsyncClient() as client:
        while True:
            try:
                await client.get(url)
                logger.info("Keep-alive ping sent.")
            except Exception:
                logger.exception("Keep-alive ping failed.")
            await asyncio.sleep(840)  # 15 minutes


@app.on_event("startup")
async def startup_event():
    logger.info("VORTEX API startup complete.")
    asyncio.create_task(keep_awake())

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
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
    logger.info("Client connected to /stream_logs")
    return StreamingResponse(
        log_streamer(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.exception("Unhandled exception on %s", request.url.path)
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error"},
    )

@app.post("/ask")
def ask(payload: Query):
    logger.info("Received /ask query: %s", payload.query)

    response = route_command(payload.query, payload.query.lower())
    RawOutput = response
    if RawOutput is None:
        logger.warning("route_command returned None for query=%s", payload.query)
        FinalOutput = ""
        return {"ATLAS": FinalOutput}

    if isinstance(RawOutput, str):
        logger.info("Returning string response from /ask")
        return {"ATLAS": RawOutput}
    try:
        items = list(RawOutput)
    except TypeError:
        FinalOutput = str(RawOutput)
    else:
        FinalOutput = " ".join(str(item) for item in items if item is not None)
    logger.info("Returning normalized response from /ask")
    return {"ATLAS": FinalOutput}
