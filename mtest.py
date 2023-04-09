import openai
import os
import time
import inspect
import gptAPIs

# Replace 'your_api_key_here' with your actual API key
openai.api_key = os.environ.get("OPENAI_API_KEY")

init_message = [{"role": "system", "content": "you are a AI helper"}, {"role": "user", "content": "根据最新的存款利率，我的50万存款应该拿出多少来购买哪些稳健的股票，使我的年收益可以达到5%？"}]


def chat_with_gpt_stream(prompt, model="gpt-3.5-turbo", max_tokens=500):
    print("ready to go:")
    start_time = time.time()
    # Create the completion request
    # response = openai.ChatCompletion.create(
    #     model=model,
    #     messages=init_message,
    #     max_tokens=max_tokens,
    #     n=1,
    #     stop=None,
    #     temperature=0.5,
    #     stream=True,
    # )

    response = gptAPIs.invoke_gpt(init_message, use_stream=True)

    chunk_time = time.time() - start_time
    print(chunk_time)
    print(inspect.isgenerator(response))
    # for choice in response.choices:
    #     if "text" in choice:
    #         print(choice.text)
    # for chunk in response:
    #     delta = chunk['choices'][0]['delta']
    #     if 'content' in delta:
    #         print(delta['content'], end='')
    for chunk in response:
        if chunk:
            print(chunk, end='')


user_prompt = "请告诉我关于太阳系的一些基本信息。"

chat_with_gpt_stream(user_prompt)
