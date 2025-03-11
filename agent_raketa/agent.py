from typing import Dict
from langchain.tools import tool
import os
from dotenv import find_dotenv, load_dotenv
from langchain_gigachat.chat_models import GigaChat
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver
import time
import asyncio
import aiohttp

from menu import menu
from get_access_token3 import get_access_token
import logging
import httpx

load_dotenv(find_dotenv())

@tool
def get_all_doner_names() -> str:
    """ Возвращает название всех шаурм через запятую """

    print(f"Bot requested function get_all_doner_names")
    return ", ".join([stuff["name"] for stuff in menu])

@tool
def get_modifiers_by_name(name: str) -> Dict:
    """ Возращает все модификаторы по названию шаурмы """

    print(f"Bot requested function get_modifiers_by_name({name})")
    for stuff in menu:
        if stuff["name"] == name.strip():
            return stuff

    return {"error": "Позиции с таким названием не существует"}

system_prompt = "Ты бот-продавец шаурмы. Твоя задача продать шаурму, напитки, шашлык клиенту, получив от него заказ. Если тебе не хватает каких-то данных, запрашивай их у пользователя."

tools = [get_all_doner_names, get_modifiers_by_name]

model = GigaChat(
    model="GigaChat-Pro",
    verify_ssl_certs=False,
    timeout=600,
)

agent = create_react_agent(model=model,
                           tools=tools,
                           checkpointer=MemorySaver(),
                           state_modifier=system_prompt)

def chat(thread_id: str):
    config = {"configurable": {"thread_id": thread_id}}
    while(True):
        print(agent)
        rq = input("\nHuman: ")
        print("User: ", rq)
        if rq == "stop":
            break
        resp = agent.invoke({"messages": [("user", rq)]}, config=config)
        print("Assistant: ", resp["messages"][-1].content)
        time.sleep(1) # For notebook capability

chat("123")
