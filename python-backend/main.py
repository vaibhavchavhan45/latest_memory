from fastapi import FastAPI
import asyncio

from db.database import engine, Base
from db.models import VideoState
from routes.ingest_route import router as ingest_router
from routes.ask_query_route import router as ask_query_router
from routes.status_route import router as status_router
from services.video_repair.video_repair_scheduler import auto_repair_loop


Base.metadata.create_all(bind = engine)

app = FastAPI() 

app.include_router(ingest_router)
app.include_router(ask_query_router)
app.include_router(status_router)


@app.on_event("startup")
async def start_auto_repair():
    """
    Start auto-repair background task when FastAPI server starts.
    Runs forever in background, independent of user requests.
    """
    print("Starting Auto repair scheduler....")
    asyncio.create_task(auto_repair_loop())
