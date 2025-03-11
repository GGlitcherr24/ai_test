import getpass
from io import BytesIO
from PIL import Image
from dotenv import find_dotenv, load_dotenv
from langchain_gigachat.chat_models import GigaChat
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from base64 import b64decode
from IPython import display
import os

from get_access_token import get_access_token

load_dotenv()

llm = GigaChat(
    access_token=get_access_token(),
    model='GigaChat-Pro',
    timeout=6000,
    verify_ssl_certs=False
)

llm = llm.bind_tools(tools=[], tool_choice='auto')

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """ Ты - гейм дизайнер для мобильных игр. Делаешь в 2D стиле, но не в пиксельном"""
        ),
        MessagesPlaceholder("history", optional=True),
        ("user", """{topic}""")
    ]
)

generate_image_chain = prompt | llm

prompt_input = input("Что сгенерировать?: ")
response = generate_image_chain.invoke({"topic": prompt_input})
image_uuid = response.additional_kwargs.get("image_uuid")
image = llm.get_file(image_uuid)
description = response.additional_kwargs["postfix_message"]
try:
    image_bytes = b64decode(image.content)
    image_stream = BytesIO(image_bytes)
    img = Image.open(image_stream)
    filename = "image.png"
    img.save(filename)
except Exception as e:
    print(f"Error processing or saving image: {e}")
# display.HTML(
#     f'<img src="data:image/png;base64,{llm.get_file(image_uuid).content}" width="300" /><br><p>{description}</p>'
# )
# print(f'<img src="data:image/png;base64,{llm.get_file(image_uuid).content}" width="300" /><br><p>{description}</p>')
