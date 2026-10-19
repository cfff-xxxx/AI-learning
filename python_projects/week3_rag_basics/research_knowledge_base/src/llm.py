import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()#读取.env文件

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url="https://api.deepseek.com"
)


def generate_answer(question, context):

    prompt = f"""
你是一个专业的AI论文助手。

请根据下面提供的论文内容回答问题。

要求：
1. 只根据论文内容回答，不要编造。
2. 如果论文没有提到，请明确说明。
3. 回答时说明论文中的方法、实验或结论。

论文内容：
{context}


问题：
{question}
"""


    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {
                "role": "system",
                "content": "你是一名帮助阅读AI论文的助手。"
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )


    return response.choices[0].message.content