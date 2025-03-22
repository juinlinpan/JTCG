from abc import ABC, abstractmethod
import asyncio
import time
import schemas
import json

class BaseAgent(ABC):
    def __init__(self):
        self.messages = []
    
    @abstractmethod
    def reset_messages(self):
        return NotImplemented
    
    @abstractmethod
    def response(self, message: schemas.MessageCreate) -> str:
        return NotImplemented
    
    @abstractmethod
    def get_messages(self):
        return NotImplemented
    
    
class DummyAgent(BaseAgent):
    def __init__(self, active_connections=[]):
        self.messages = []
        self.cnt = 0
        self.planning_task = None
        self.has_new_messages = False  # 新增標記，標示是否有新訊息
        
    def reset_messages(self):
        self.cnt = 0
        self.messages = []
        # 取消任何正在進行的計劃任務
        if self.planning_task and not self.planning_task.done():
            self.planning_task.cancel()
        self.has_new_messages = False
        return self.messages

    async def response(self, message: schemas.MessageCreate):
        self.has_new_messages = False
        self.cnt += 1
        # 將使用者訊息加入對話歷史
        user_message = schemas.MessageContent(
            content=message.content,
            role="user"
        )
        self.messages.append(user_message)
        
        if self.cnt % 3 != 0: 
            ret = "This is a dummy response."
        else:
            ret = "OK, 我幫您安排行程"
            # 建立非同步任務但不等待它完成
            self.planning_task = asyncio.create_task(self.plan())
            
            
        ai_message = schemas.MessageContent(
            content=ret,
            role="assistant"
        )
        self.messages.append(ai_message)
        
        return ai_message
        
    async def plan(self, **kwargs):
        # 此方法模擬背景計算過程
        print("開始執行計劃任務...")
        await asyncio.sleep(5)
        plan_message = schemas.MessageContent(
            content="以下是我的行程建議:\n1. 上午9點：參觀博物館\n2. 中午12點：在附近餐廳用餐\n3. 下午2點：市區觀光\n4. 晚上6點：享用晚餐",
            role="assistant"
        )
        self.messages.append(plan_message)
        self.has_new_messages = True

    
    def get_messages(self):
        # 重置新訊息標記
        self.has_new_messages = False
        return self.messages
    
    def has_updates(self):
        """檢查是否有新的訊息需要更新"""
        return self.has_new_messages


