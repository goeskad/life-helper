import os
import time
from fastapi import FastAPI, Request, status, Header, File, HTTPException, Depends, Body, UploadFile
from fastapi.responses import StreamingResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.staticfiles import StaticFiles
# from starlette.responses import StreamingResponse
import asyncio
from typing import Generator, AsyncGenerator, Optional

from pydantic import BaseModel
import kbsChat
import financialAssistant
import marketService

from bs4 import BeautifulSoup

app = FastAPI()
app.mount("/views", StaticFiles(directory="views"), name="static")


init_promote = "你将担任某个软件系统的客服助理。用户会问你一些使用此软件系统时遇到的问题。用户给你的提问中将包含一些关于此系统的知识，你需要根据这些知识来回答用户的提问。"
system_message = {"role": "system", "content": init_promote}


class KBSInput(BaseModel):
    text: str


class MessageInput(BaseModel):
    text: str


@app.post("/getKbsQuestions")
async def kbs_endpoint(input: KBSInput):
    user_input = input.text

    kbs_queries = kbsChat.generate_api_calls(user_input)
    return kbs_queries


@app.post("/chat")
async def chat_endpoint(hexin_v: Optional[str] = Header(None), input: MessageInput=None):
    user_input = input.text

    message_log = [
        financialAssistant.system_message
    ]

    if hexin_v is not None:
        marketService.market_token = hexin_v

    output_queue = asyncio.Queue()
    asyncio.create_task(kbsChat.chat_with_gpt(message_log, user_input, output_queue))
    response = StreamingResponse(
        content=generate_content(output_queue),
        status_code=status.HTTP_200_OK,
        media_type="text/html"
    )
    return response


@app.post("/stest")
async def stream_response(hexin_v: Optional[str] = Header(None), input: MessageInput=None):
    print('check v' + hexin_v)
    file_like = get_data_from_file('README.md')
    output_queue = asyncio.Queue()
    asyncio.create_task(processor(output_queue))
    response = StreamingResponse(
        content=generate_content(output_queue),
        status_code=status.HTTP_200_OK,
        media_type="text/html",
        background=True
    )
    return response


@app.post("/wtest")
async def wechat(request: Request):
    # 获取POST请求中的xml数据
    xml_data = await request.body()

    print("received wechat message")
    print(xml_data)

    # 处理xml数据
    soup = BeautifulSoup(xml_data, 'xml')
    to_user_name = soup.find("FromUserName").text
    from_user_name = soup.find("ToUserName").text
    create_time = str(int(time.time()))
    print(f"create time {create_time}")

    # 构造回复消息
    output_xml = """
<xml>
  <ToUserName><![CDATA[{to_user_name}]]></ToUserName>
  <FromUserName><![CDATA[{from_user_name}]]></FromUserName>
  <CreateTime>{create_time}</CreateTime>
  <MsgType><![CDATA[text]]></MsgType>
  <Content><![CDATA[你好大哥]]></Content>
</xml>
"""

    output_xml = output_xml.format(to_user_name, from_user_name, create_time)
    print(f"return message {output_xml}")
    return output_xml


@app.get("/wtest")
async def wechat(request: Request, signature: str, timestamp: str, nonce: str, echostr: str):
    # 处理xml数据
    print(f"received token verify message {signature}, {timestamp}, {nonce}, {echostr}")

    return int(echostr)


async def processor(output_queue):
    for i in range(10):
        await output_queue.put("output" + str(i) + ". ")
        await asyncio.sleep(0.1)

    await output_queue.put(ag())


def ag():
    for i in range(10):
        yield "another" + str(i)


async def generate_content(output_queue):
    while True:
        content = await output_queue.get()
        if isinstance(content, str):
            print(content)
            yield content
        else:
            for data in content:
                yield data
            break


def get_data_from_file(file_path: str) -> Generator:
    with open(file=file_path, mode="rb") as file_like:
        while True:
            content = file_like.read(50)
            if len(content) == 0:
                break
            else:
                yield content
                time.sleep(0.2)


def start():
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
