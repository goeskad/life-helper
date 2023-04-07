import marketService

queries = [{"query": "连续3天涨幅稳定且风险较低的股票"}]
response = marketService.search_market(queries)
# response = queries[0]["query"]["ss"]

print(response)
