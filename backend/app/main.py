from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import asyncio
import schemas
from agents.base import DummyAgent
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

advisor = DummyAgent()



@app.get("/messages/reset")
def reset_messages():
    return advisor.reset_messages()

@app.post("/messages", response_model=schemas.MessageContent)
async def add_message(message: schemas.MessageCreate):
    # 改為非同步呼叫
    return await advisor.response(message)
    
@app.get("/messages/get_messages", response_model=list[schemas.MessageContent])
def get_messages():
    return advisor.get_messages()


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
