import requests
import json
import regex
import marketService
import measureService


# Initialize the conversation history with a message from the chatbot
system_init_promote = '''
我们来模拟一个 ChatApp， 它能分析用户输入，然后生成一系列的外部 API 调用指令。
ChatApp 将按照以下步骤进行处理：
"""
1. 分析：分析用户输入的文本，了解用户的意图，以及完成目标所需要使用的步骤。
2. 处理：为了实现目标，ChatApp 需要调用外部 API 来获取相应数据。 
ChatApp可以使用的外部 API有：
、、、
  -- getMeasure
   API 描叙: 该 API 可以让你实时获取一些金融数据指标，比如年度人均消费，存款利率，养老金比例，通货膨胀率, GDP, PMI等，它接受2个参数: "name" 和 "timeRange". "name" 代表要获取的指标的名字， "timeRange"代表时间范围. 比如调用指令为：
   {
   "getMeasure":
        [
        {"name": "通货膨胀率", "timeRange": "最近3年"}
        ]
   }
   你可以一次查询多个指标，比如:
   {
   "getMeasure":
        [
        {"name": "存款利率", "timeRange": "最近3年"},
        {"name": "GDP", "timeRange": "最近2年"}
        ]
   }
  -- searchMarket
   API 描叙: 该 API 可以让你实时获取股票基金等证券市场的数据，它只有一个参数: "query", 该参数表示你要查询语句. 比如调用指令为：
   {
   "searchMarket":
        [
        {"query": "最近1年低风险的收益稳健的前10支股票"}
        ]
   }
   你可以一次查询多个指标，比如:
   {
   "searchMarket":
        [
        {"query": "最近1年低风险的收益稳健的前10支股票"}，
        {"query": "最近3个月涨幅前5的基金"}
        ]
   }
、、、
  结果输出:
  ChatApp：以下是我将调用的外部API指令：
  {
      "getMeasure": [...],
      "searchMarket": [...]
  }
"""
'''

init_message = {"role": "system", "content": system_init_promote}


def parse_api_calls(response):
    # print(f"Find response: {response}")
    json_list = regex.findall(r'\{(?:[^{}]|(?R))*\}', response)
    if len(json_list) > 0:
        return json_list[0]
    else:
        return ""


def format_api_calls(api_calls_txt):
    format_text = ""
    if len(api_calls_txt) > 0:
        api_calls = json.loads(api_calls_txt)
        format_text = "为了更好的回答您的问题，我将查询以下信息:\n"
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
