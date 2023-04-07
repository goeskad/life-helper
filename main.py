from fastapi import FastAPI, Depends
from pydantic import BaseModel

import kbsChat
import marketService

app = FastAPI()


class KBSInput(BaseModel):
    text: str


class MessageInput(BaseModel):
    text: str
    kbsQueries: str
    kbsToken: str


@app.post("/getKbsQuestions")
async def kbs_endpoint(input: KBSInput):
    user_input = input.text

    kbs_queries = kbsChat.generate_api_calls(user_input)
    return kbs_queries


@app.post("/chat")
async def chat_endpoint(input: MessageInput):
    user_input = input.text
    kbs_queries = input.kbsQueries
    kbs_token = input.kbsToken

    init_promote = "你将担任某个软件系统的客服助理。用户会问你一些使用此软件系统时遇到的问题。用户给你的提问中将包含一些关于此系统的知识，你需要根据这些知识来回答用户的提问。"
    message_log = [
        {"role": "system", "content": init_promote}
    ]

    if kbs_token is not None:
        marketService.market_token = kbs_token

    response = kbsChat.chat_with_gpt(message_log, user_input, kbs_queries)

    return response


def start():
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
