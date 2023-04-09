import json
import apiManager
import gptAPIs
import asyncio

api_analysis_promote = '''
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

init_api_message = {"role": "system", "content": api_analysis_promote}

api_search_output_message = "为了回答您的问题，我首先将查询以下数据: \n"
user_input_prefix = "我查询到了一些有用的数据, 请参考它们来回答我的问题:\n"

init_promote = """我希望你担任投资理财助理，并想出创造性的方法来管理财务。
在为客户制定财务计划时，您需要考虑预算、投资策略和风险管理，以帮助他们实现利润最大化。
客户在向你提问时，通常将附加上实时金融指标数据以及一些股票基金等证券市场数据给你做参考，你将根据这些参考数据来回答用户提问。
"""
system_message = {"role": "system", "content": init_promote}


async def write_output(output_queue: asyncio.Queue, text):
    await output_queue.put(text)
    await asyncio.sleep(0.001)


async def prepare_user_input(user_input, output_queue):
    user_prompt = f"\n Human: 请对用户的提问内容: {user_input} 进行分析，生成相应的 API 调用指令"
    api_prompt = api_analysis_promote + user_prompt
    await write_output(output_queue, "准备开始分析\n")
    # await asyncio.sleep(0.001)
    api_calls = apiManager.generate_api_calls(api_prompt)
    await write_output(output_queue, "问题分析已完成，请稍后...\n")
    # await asyncio.sleep(0.001)
    if len(api_calls) > 0:
        formatted_api_calls = apiManager.format_api_calls(api_calls)
        await write_output(output_queue, f"{api_search_output_message}{formatted_api_calls}请稍后...\n")
        print(f"use api calls {api_calls}")
        api_response = apiManager.execute_apis(json.loads(api_calls))
        await write_output(output_queue, "\n已完成查询，准备回答您的问题，请稍后...\n\n")
        print(f"get api response {api_response}")
        return f'{user_input_prefix} {api_response}\n我的问题是"""\n{user_input}"""\n'
    else:
        await write_output(output_queue, "您的问题无需查询数据，接下来我将回答您的问题，请稍后...")
    return user_input
