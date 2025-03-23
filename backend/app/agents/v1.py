import asyncio
import time
import schemas
import json
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import (
    AIMessage,
    HumanMessage,
    SystemMessage,
    ToolMessage,
)
os.environ['GOOGLE_API_KEY'] = 'AIzaSyC8lJWeRoheKe6QBReAfRbhiried6EqChc'


SYS_RESP = """
你是一位旅遊推薦平台的客服人員
你的工作是負責詢問用戶的旅遊需求，再交由"行程安排師"進行行程安排。

* Execution steps:
1. 在數輪對話中引導用戶提供:
    - 目的地
    - 旅遊日期
    - 人數
    - 預算
2. 用戶提供齊全後，將用戶需求交由"行程安排師"進行行程安排
"""

SYS_PLAN = """
你是一位旅遊推薦平台的行程安排師
你的工作是負責為用戶提供旅遊住宿與周邊探索的整合解決方案
"""


class V1Agent():
    def __init__(self, event_queue):
        self.event_queue = event_queue
        self.messages = []
        self.llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0.5)

    def reset_messages(self):
        self.messages = []
        return self.messages

    async def response(self, message: schemas.MessageCreate):
        # 將使用者訊息加入對話歷史
        user_message = schemas.MessageContent(
            content=message.content,
            role="user"
        )
        self.messages.append(user_message)
        langchain_messages = [SystemMessage(content=SYS_RESP)]
        langchain_messages += [self.convert_message_to_langchain_message(msg) for msg in self.messages]
        output = self.llm.invoke(langchain_messages)
        self.messages.append(self.convert_langchain_message_to_message(output))

        await self.event_queue.put({
            "data": json.dumps({
                "type": "plan_completed",
                "timestamp": time.time()
            })
        })
        
    def convert_message_to_langchain_message(self, msg):
        if msg.role == "assistant":
            langchain_message = AIMessage(content=msg.content)
        else:
            langchain_message = HumanMessage(content=msg.content)
        return langchain_message
    
    def convert_langchain_message_to_message(self, langchain_msg):
        role = 'assistant' if langchain_msg.type == 'ai' else 'user'
        message = schemas.MessageContent(
            content=langchain_msg.content,
            role=role
        )
        return message
    
    def get_messages(self):
        return self.messages
    
    
    
    