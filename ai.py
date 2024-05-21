from openai import OpenAI
import os
import httpx
def chatgpt(inp):
    HTTP_PROXY = "http://127.0.0.1:8082"
    client = OpenAI(
    http_client=httpx.Client(
          proxies=HTTP_PROXY,
          transport=httpx.HTTPTransport(local_address="0.0.0.0"),
      ),
      api_key=os.environ.get("OPENAI_API_KEY"),
      base_url="https://aihubmix.com/v1"
    )
    completion = client.chat.completions.create(
      model="gpt-3.5-turbo",
      messages=[
      {"role": "user","content": inp,}
      ]
    )
    return completion.choices[0].message.content
#print(chatgpt("请问什么是强化学习"))
