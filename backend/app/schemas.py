from pydantic import BaseModel
from enum import Enum
import datetime

class MessageRole(str, Enum):
    system = "system"
    user = "user"
    assistant = "assistant"

class MessageBase(BaseModel):
    content: str
    role: MessageRole = MessageRole.user
    
class MessageCreate(MessageBase):
    pass

class MessageContent(BaseModel):
    content: str
    role: str


