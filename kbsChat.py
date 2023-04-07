import apiManager
import gptAPIs
import json


def generate_api_calls(user_input):
    api_message_log = [
        apiManager.init_message,
        {"role": "user", "content": f"请对用户的提问内容: {user_input} 进行分析，生成相应的 API 调用指令"}
    ]

    # Send the conversation history to the chatbot and get its response
    response = gptAPIs.invoke_gpt(api_message_log)

    return apiManager.parse_api_calls(response)


def chat_with_gpt(message_log, user_input, api_calls):
    if len(api_calls) > 0:
        print(f"use api calls {api_calls}")
        api_response = apiManager.execute_apis(json.loads(api_calls))
        print(f"get api calls {api_response}")
        if len(api_response) > 0:
            user_input = user_input + "\n ---------\n以下是你应该参考的信息:\n" + api_response
        else:
            print("no result from api call")

    message_log.append({"role": "user", "content": user_input})
    # Send the conversation history to the chatbot and get its response
    response = gptAPIs.invoke_gpt(message_log)

    return response
