import os
from tavily import TavilyClient

tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

def web_search(query: str, max_results: int = 5) -&gt; str:
  """جست‌وجوی وب با استفاده از موتور جست‌وجوی بهینه‌شده برای هوش مصنوعی (Tavily).

  ورودی: query: عبارت جست‌وجو max_results: حداکثر تعداد نتایج (پیش‌فرض ۵)
  """
  try:
    response = tavily_client.search(
        query=query,
        max_results=max_results,
        search_depth="basic",  # جست‌وجوی سریع
    )
    # استخراج خلاصه‌ی نتایج به صورت متن ساختاریافته
    results = []
    for r in response.get("results", []):
      results.append(
          f"Title: {r.get('title')}\nURL: {r.get('url')}\nContent:"
          f" {r.get('content')}\n---"
      )

    return (
        "\n".join(results)
        if results
        else "No relevant search results found."
    )
  except Exception as e:
    return f"Error executing web search: {str(e)}"

web_search_schema = {
    "type": "function",
    "function": {
        "name": "web_search",
        "description": (
            "Search the live web for up-to-date facts, current events, or"
            " information not in training data."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The search query string.",
                },
                "max_results": {
                    "type": "integer",
                    "description": (
                        "Number of search results to return (default 5)."
                    ),
                },
            },
            "required": ["query"],
        },
    },
}
