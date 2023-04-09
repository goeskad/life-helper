import json
import regex
import gptAPIs
import marketService
import measureService


def generate_api_calls(api_prompt):
    # api_message_log = [
    #     apiManager.init_message,
    #     {"role": "user", "content": f"请对用户的提问内容: {user_input} 进行分析，生成相应的 API 调用指令"}
    # ]
    #
    # # Send the conversation history to the chatbot and get its response
    # response = gptAPIs.invoke_gpt(api_message_log)
    response = gptAPIs.invoke_gpt3(api_prompt)
    return parse_api_calls(response)


def parse_api_calls(response):
    # print(f"Find response: {response}")
    json_list = regex.findall(r'\{(?:[^{}]|(?R))*\}', response)
    if len(json_list) > 0:
        return json_list[0]
    else:
        return ""


def format_api_calls(api_calls_txt):
    if len(api_calls_txt) > 0:
        api_calls = json.loads(api_calls_txt)
        format_text = ""
        for api_call in api_calls.items():
            api_key = api_call[0]
            if api_key == "searchMarket":
                format_text += "证券市场数据:\n"
                for query in api_call[1]:
                    query_text = query.get("query")
                    if query_text is not None:
                        format_text += query_text + "\n"
            elif api_key == "getMeasure":
                format_text += "金融指标数据:\n"
                for query in api_call[1]:
                    query_text = query.get("name")
                    if query_text is not None:
                        format_text += query_text + "\n"
    else:
        format_text = "无需查询实时数据，请稍后\n"

    return format_text


def execute_apis(api_calls):
    results = []
    for api_call in api_calls.items():
        api_key = api_call[0]
        if api_key == "searchMarket":
            result = marketService.search_market(api_call[1])
            results.append(result)
        elif api_key == "getMeasure":
            result = measureService.get_measure(api_call[1])
            results.append(result)
    return '\n'.join(results)
