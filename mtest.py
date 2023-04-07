
import requests
import json

JSON_AS_ASCII=False

def send_request(url, token, queries):
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json; charset=utf-8"
    }

    response = requests.post(url, headers=headers, json=queries)

    if response.status_code == 200:
        response_data = response.json()
        new_results = []
        for result in response_data["results"]:
            query = result["query"]
            max_score_result = max(result["results"], key=lambda x: x["score"])

            new_result = {
                "query": query,
                "result": max_score_result["text"]
            }
            new_results.append(new_result)

        # 将处理后的结果输出为JSON格式
        output_data = {"results": new_results}
        output_json = json.dumps(output_data, ensure_ascii=False, indent=4)

        return output_json
    else:
        return f"Error: {response.status_code}"

def main():
    query_url = "https://lobster-app-r4gai.ondigitalocean.app/query"
    query_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkxlbyBYIiwiaWF0IjoxNTE2MjM5MDIyfQ.rcrsxozB5v-H7RgsScXOTzG-xgagmeH870_fC2re0iA"

    json_text = "{\"queries\": [{\"query\": \"在软件系统中如何找到供应商名称更改的选项\"}]}"
    queries = json.loads(json_text)
    query_response = send_request(query_url, query_token, queries)
    print(f"Find query response: {query_response}")


# Call the main function if this file is executed directly (not imported as a module)
if __name__ == "__main__":
    main()