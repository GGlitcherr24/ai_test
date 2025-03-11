from get_access_token import get_access_token

from langchain.schema import HumanMessage, SystemMessage
from langchain_gigachat import GigaChat

chat = GigaChat(access_token=get_access_token(), verify_ssl_certs=False)

messages = [
    SystemMessage(
        content="Ты бот-программист, который работает на языке программирование Python и помогает писать код"
    )
]

while True:
    user_input = input("User: ")
    if user_input == 'stop':
        break
    messages.append(HumanMessage(content=user_input))
    res = chat(messages)
    messages.append(res)
    print("Bot: ", res.content)