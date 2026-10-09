from openai import OpenAI
import os
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())
# 关键：加上 base_url 指向国内 API
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url="https://api.deepseek.com"
                )

def get_completion_from_messages(messages, model="deepseek-chat", temperature=0):
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
    )
    return response.choices[0].message.content

def run_translator():
    # 初始化上下文（这一步是 OrderBot 最核心的灵魂）
    context = [{'role': 'system', 'content': """
你是一个严格的翻译官。无论用户说什么，你只回复对应的英文翻译，不要加任何解释，不要闲聊，不要问候。请记住你要把用户发给你的东西翻译成英文即可
"""}]

    print("翻译官已上线！输入 'quit' 或 'exit' 退出。\n")

    # 循环收集信息
    while True:
        user_input = input("你: ")
        if user_input.lower() in ['quit', 'exit']:
            print("结束翻译。")
            break

        context.append({'role': 'user', 'content': user_input})
        response = get_completion_from_messages(context)
        context.append({'role': 'assistant', 'content': response})
        print(f"翻译官: {response}\n")



if __name__ == "__main__":
    run_translator()