from typing import Dict, Literal
from langchain.tools import tool
import os
from dotenv import find_dotenv, load_dotenv
from langchain_gigachat.chat_models import GigaChat
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver
import time

from menu import menu

load_dotenv(find_dotenv())

METHOD_OF_RECEIPT = Literal["Доставка", "Самовывоз"]

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

@tool
def create_order(name: str,
                 address: str,
                 phone_number: str,
                 place: METHOD_OF_RECEIPT):
    """ Создает заказ """
    print(f"Bot requested function create_order({name}, {place}, {address}, {phone_number})")
    print(f"NEW ORDER!: {name}, {place}, {address}, {phone_number}")
    return


system_prompt = "Ты бот-продавец шаурмы. Твоя задача продать шаурму, напитки, шашлык клиенту, если клиент сказал какая позиция нужна клиенту, предоставь список всех модификторов этого товара, если у этого блюда они есть(обратись к методу получения модификаторов), потом создать заказ, предварительно узнав всю необходимую информацию от клиента. Если тебе не хватает каких-то данных, запрашивай их у пользователя."

tools = [get_all_doner_names, get_modifiers_by_name, create_order]

model = GigaChat(
    model="GigaChat-Max",
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
