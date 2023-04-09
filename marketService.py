import requests
import json
import numbers
from urllib.parse import quote


market_host = "http://www.iwencai.com/unifiedwap/unified-wap/v2/result/get-robot-data"
market_token = "AwrBGiEPWmT3SdbGF0vAp_3TXfup-4pTgHUC-ZRitB3oUqQlfIveZVAPUjZn"
source_value = "ths_mobile_iwencai"
version_value = "2.0"
per_page = 20
data_template = f'source={quote(source_value)}&version={quote(version_value)}&page=1%perpage={per_page}'


def is_number(s):
    if s.isdigit():
        return True

    try:
        float(s)
        return True
    except ValueError:
        pass

    return False


def send_request(url, token, query):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
        "Content-Type": "application/x-www-form-urlencoded",
        "hexin-v": token,
        "Origin": "http://www.iwencai.com"
    }

    encoded_data = f"{data_template}&question={quote(query)}"

    response = requests.post(url, data=encoded_data, headers=headers)

    return response


def process_columns(data, columns):
    for item in data.items():
        key = item[0]
        value = item[1]
        allow_column = False
        if isinstance(value, numbers.Number):
            allow_column = True
        elif isinstance(value, str):
            if is_number(value):
                allow_column = True
            elif "简称" in key or key == "code":
                allow_column = True
            else:
                allow_column = False
        if allow_column:
            columns.append(key)


def get_market_datas(response_data):
    try:
        return response_data["data"]["answer"][0]["txt"][0]["content"]["components"][1]["data"]["datas"]
    except:
        pass
    return []


def process_response(response_data):
    print(f"original market response {len(response_data)}")
    datas = get_market_datas(response_data)

    if len(datas) > 0:
        new_datas = []
        columns = []
        if len(datas) > 10:
            datas = datas[:10]

        for data in datas:
            new_data = []
            if len(columns) == 0:
                process_columns(data, columns)
            for column in columns:
                if column in data:
                    new_data.append(data[column])
                else:
                    new_data.append('unknown')
            new_datas.append(json.dumps(new_data, ensure_ascii=False))
        return {"columns": json.dumps(columns, ensure_ascii=False), "datas": new_datas}
    else:
        return {"datas": "no data"}


def search_market(queries):
    results = "证券市场数据: \n"
    for query in queries:
        question = query["query"]
        response = send_request(market_host, market_token, question)

        if response.status_code == 200:
            datas = process_response(response.json())
            results = f"{results}\n{question}:\n{json.dumps(datas, ensure_ascii=False, indent=4)}"
            if len(results) > 5000:
                break
        else:
            return f"Error: {response.status_code}"
    return results
