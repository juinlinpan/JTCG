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

from pydantic import BaseModel, Field
from typing import Any, List, TypedDict
from langchain_core.tools import tool
from langchain_core.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate
)   
from agents.tools import tool_box
from langgraph.prebuilt import ToolNode
from langgraph.graph import END, START, StateGraph


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

* Rundown:
1. 先跟她介紹你可以為他安排行程，與他打招呼。
2. 逐一詢問用戶，不要一次問，這樣有壓迫感。
3. 用戶可能會用不同的方式提供資訊，要會解讀成上述四個項目。
4. 一旦蒐集到四個項目，就統整用戶需求並覆誦一次，與用戶確認是否想要進一步安排行程。
5. 確認完畢後，不用回覆用戶，直接呼叫"行程安排師"進行行程安排。
6. 行程規劃師會從他的電腦回覆後下線，請繼續服務用戶
7. 用戶如果更改行程需求，則再次從 2. 開始，或可能再次呼叫"行程安排師"。

* Rules:
1. 用戶不知道"行程安排師"的存在，所以不要提及"行程安排師"。
2. 用戶確認無誤之後不要先回覆，直接呼叫"行程安排師"。
3. 全程使用繁體中文
"""

@tool
def call_planner(requirement: str):
    """
    呼叫這個函數，會將需求(requirement)傳遞給行程安排師，並等待行程安排師的回覆
    等到與用戶蒐集到足夠資訊後，使用此函數。
    回傳即是行程安排師的回覆。
    """

SYS_PLANNER = """
你是一位旅遊推薦平台的行程安排師
你的工作是負責為用戶提供旅遊住宿與周邊探索的整合解決方案。
你會收到用戶的需求，請根據此需求為用戶安排行程。

* Rules:
1. 輸出要可讀性高
"""

HUMAN_PLANNER = "需求: {requirement}"

class Graph_State(TypedDict):
    messages: List
    result: str
    notebook: str
    question: str
    searcher_messages: List

class V1Agent():
    def __init__(self, event_queue):
        self.event_queue = event_queue
        self.messages = []
        self.llm_resp = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash",
            temperature=0.5
            ).bind_tools([call_planner])
        
        self.llm_planner = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash",
            temperature=0.5
            )

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
        output = self.llm_resp.invoke(langchain_messages)
        if len(output.content) > 0:
            self.messages.append(self.convert_langchain_message_to_message(output))
            await self.event_queue.put({
                "data": json.dumps({
                    "type": "plan_completed",
                    "timestamp": time.time()
                })
            })
        else:
            print(output.tool_calls)
            requirement = output.tool_calls[0]['args']['requirement']
            ret = "收到您的需求，請稍等片刻，馬上為您安排行程"
            ai_message = schemas.MessageContent(
                content=ret,
                role="assistant"
            )
            self.messages.append(ai_message)
            
            await self.event_queue.put({
                "data": json.dumps({
                    "type": "plan_completed",
                    "timestamp": time.time()
                })
            })
            self.planning_task = asyncio.create_task(self.plan(requirement))


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
    
    
    async def plan(self, requirement: str):
        # 此方法模擬背景計算過程
        print("開始執行計劃任務...")
        
        prompt_template = ChatPromptTemplate(
            messages=[
                SystemMessagePromptTemplate.from_template(SYS_PLANNER),
                HumanMessagePromptTemplate.from_template(HUMAN_PLANNER)
            ]
        )
        prompt = prompt_template.format_prompt(requirement=requirement)
        output = self.llm_planner.invoke(prompt)
        self.messages.append(self.convert_langchain_message_to_message(output))
        
        # 發送事件通知
        await self.event_queue.put({
            "data": json.dumps({
                "type": "plan_completed",
                "timestamp": time.time()
            })
        })
        
        print("計劃任務執行完畢")
        
    
    def coordinator(self, graph_state: Graph_State):
        return graph_state
    def searcher(self, graph_state: Graph_State):
        return graph_state
    
    def continue_searching(self, graph_state: Graph_State):
        if graph_state['result'] == "":
            return "searcher"
        else:
            return END
        
    def go_tool(self, graph_state: Graph_State):
        if graph_state['searcher_messages'][-1].tool_calls:
            return "tool"
        else:
            return "coordinator"
        
    
    async def plan_v1_2(self, requirement: str):
        
        graph_state = Graph_State(
            messages=[],
            result="",
            notebook=""
        )
        
        workflow = StateGraph(graph_state)
        
        workflow.add_node("coordinator", self.coordinator)
        workflow.add_node("searcher", self.searcher)
        tool_node = ToolNode(tool_box)
        workflow.add_node("tool", tool_node)
        
        workflow.add_edge(START, "coordinator")
        workflow.add_conditional_edges("coordinator", self.continue_searching, ["searcher", END])
        workflow.add_conditional_edges("searcher", self.go_tool, ["tool", "coordinator"])
        workflow.add_edge("tool", "coordinator")
        
        app = workflow.compile()
        