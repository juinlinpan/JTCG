from abc import ABC, abstractmethod
import time

class BaseAgent(ABC):
    def __init__(self):
        pass
    
    @abstractmethod
    def response(self, messages) -> str:
        return NotImplemented
    
    
class DummyAgent(BaseAgent):
    def __init__(self):
        self.cnt = 0
    def response(self, messages) -> str:
        
        self.cnt += 1
        if self.cnt < 3:
            ret = "This is a dummy response."
        else:
            ret = "OK, 我幫您安排行程"
            self.plan()
        return ret
    
    def plan(self, **kwargs):
        time.sleep(30)
        return "dummy plan: aaaaaaa"