import asyncio
import json
from datetime import datetime

from fastapi import APIRouter
from fastapi.responses import StreamingResponse

router = APIRouter()


@router.get("/stream")
async def stream():
    async def event_generator():
        yield f"event: ping\ndata: {json.dumps({'at': datetime.utcnow().isoformat()})}\n\n"
        await asyncio.sleep(0.1)

    return StreamingResponse(event_generator(), media_type="text/event-stream")
