import regex
import json

text = '大家好{"queries": [{"query": "在软件系统中如何找到供应商名称更改的选项"}], "jks": [{"mk": "he"}]} 具体的事情{"bbs": [{"bkey": "hi"}]} 怎么样'

# 使用正则表达式匹配JSON格式的文本
json_strings = regex.findall(r'\{(?:[^{}]|(?R))*\}', text)

# 提取queries和bbs部分
queries = None
bbs = None
for json_str in json_strings:
    try:
        json_obj = json.loads(json_str)
        if 'queries' in json_obj:
            queries = json_obj['queries']
        if 'bbs' in json_obj:
            bbs = json_obj['bbs']
    except json.JSONDecodeError:
        pass

print("queries:", queries)
print("bbs:", bbs)