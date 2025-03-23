from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from sse_starlette.sse import EventSourceResponse
from typing import List
import asyncio
import schemas
from agents.base import DummyAgent
from agents.v1 import V1Agent
import uvicorn
import time


app = FastAPI(title="Travel Advisor API")

# 添加 CORS 中間件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 在生產環境中，應該設置為特定的前端域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 建立事件隊列
event_queue = asyncio.Queue()

@app.get("/events")
async def events(request: Request):
    async def event_generator():
        try:
            while True:
                if await request.is_disconnected():
                    break
                
                # 等待事件，但設置超時以檢查連接狀態
                try:
                    event = await asyncio.wait_for(event_queue.get(), timeout=1.0)
                    yield event
                except asyncio.TimeoutError:
                    continue
                    
        except asyncio.CancelledError:
            pass
    
    return EventSourceResponse(event_generator())

# 將事件隊列傳遞給 advisor
advisor = V1Agent(event_queue)

@app.get("/messages/reset")
def reset_messages():
    return advisor.reset_messages()

@app.post("/messages")
async def add_message(message: schemas.MessageCreate):
    asyncio.create_task(advisor.response(message))
    return {"message": "Message received."}
    
@app.get("/messages/get_messages", response_model=list[schemas.MessageContent])
def get_messages():
    return advisor.get_messages()


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
