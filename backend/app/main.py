from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
import schemas
from agents.base import DummyAgent
import uvicorn


app = FastAPI(title="Travel Advisor API")

# 添加 CORS 中間件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 在生產環境中，應該設置為特定的前端域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TravelAdvisorAPI:
    def __init__(self):
        self.messages = []
        self.agent = DummyAgent()

    def reset_messages(self):
        self.messages = []

    def add_message(self, message: schemas.MessageCreate):
        self.messages.append(message)
        
        ## dummy ai response
        ai_response_str = "This is a dummy response."
        ai_message = schemas.MessageContent(
            content=ai_response_str,
            role="assistant"
        )
        return ai_message
    
    def get_messages(self):
        return self.messages

advisor = TravelAdvisorAPI()

@app.get("/messages/reset")
def reset_messages():
    return advisor.reset_messages()

@app.post("/messages", response_model=schemas.MessageContent)
def add_message(message: schemas.MessageCreate):
    return advisor.add_message(message)

@app.get("/messages/get_messages", response_model=list[schemas.MessageContent])
def get_messages():
    return advisor.get_messages()


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
