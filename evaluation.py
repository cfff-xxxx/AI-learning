from openai import OpenAI
import os
from dotenv import load_dotenv, find_dotenv

# 1. 初始化配置，读取你之前的 .env 文件
_ = load_dotenv(find_dotenv())
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url="https://api.deepseek.com"
)


# 2. 基础函数（就是你之前 chatbot.py 里写的）
def get_completion_from_messages(messages, model="deepseek-chat", temperature=0):
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
    )
    return response.choices[0].message.content


# 3. 考生系统（被测对象）：这里故意返回一个错误的回答
def get_candidate_answer(question):
    messages = [
        {"role": "system", "content": "你是一个知识渊博的问答助手，请简洁地回答用户的问题。"},
        {"role": "user", "content": question}
    ]
    return get_completion_from_messages(messages)


# 4. 考官系统（裁判）
def get_judge_evaluation(question, candidate_answer, standard_answer):
    system_prompt = """
    你是一个严格的考官，请评估学生的回答是否正确。
    你将收到：问题、标准答案、学生回答。
    请判断学生的回答是否与标准答案一致（即使表达不同，只要事实正确即可）。
    如果正确，只输出“正确”。
    如果错误，输出“错误，原因：xxx”。
    """

    user_prompt = f"""
    问题：{question}
    标准答案：{standard_answer}
    学生回答：{candidate_answer}
    """

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]

    # 这里调用大模型去批改卷子
    return get_completion_from_messages(messages)


# 5. 主运行流程
if __name__ == "__main__":
    print("=== 进入 AI 自动化评估系统 ===\n")

    # 1. 出题人（你）输入考题和标准答案
    question = input("请输入考题（例如：法国的首都是哪里？）: ")
    standard_answer = input("请输入标准答案（例如：法国的首都是巴黎）: ")

    print("\n--- 第一步：考生（大模型）现场作答 ---")
    candidate_answer = get_candidate_answer(question)
    print(f"考生回答：{candidate_answer}\n")

    print("--- 第二步：考官（大模型）现场批改 ---")
    result = get_judge_evaluation(question, candidate_answer, standard_answer)
    print(f"考官评判：{result}")