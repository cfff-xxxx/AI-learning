import os

import pdfplumber
from dotenv import load_dotenv, find_dotenv
from openai import OpenAI

_=load_dotenv(find_dotenv())
client=OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url="https://api.deepseek.com"
)

def extract_text_from_pdf(pdf_path):
    """读取 PDF 文件并提取纯文本"""
    text = ""
    # 打开 PDF 文件
    with pdfplumber.open(pdf_path) as pdf:
        # 遍历每一页，把文字拼起来
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:  # 如果这一页有文字，就加进去
                text += page_text + "\n"
    return text

def get_completion_from_messages(messages,model="deepseek-chat",temperature=0):
    response=client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
    )
    return response.choices[0].message.content


def summarize_paper(paper_text):
    # 1. 设计六段式输出的 Prompt（这是项目的灵魂）
    system_prompt = """
        你是一个学术论文分析助手。请阅读以下论文文本，按以下结构输出分析：
        1. 论文标题
        2. 研究问题：这篇论文试图解决什么问题？
        3. 核心方法：作者用了什么方法？
        4. 创新点：相比已有工作，新在哪里？
        5. 实验结果：主要实验结果是什么？
        6. 局限性：作者承认或你推断的局限是什么？

       【严格约束】
        必须使用中文回答。
        必须直接输出这六个部分，禁止说“我很乐意帮您”、“好的”等任何寒暄词。
        如果文本太短无法总结，请直接输出“文本信息不足”，禁止闲聊。
        """

    user_prompt=f"论文文本：\n{paper_text}"

    messages=[
        {"role":"system","content":system_prompt},
        {"role":"user","content":user_prompt}
    ]

    return get_completion_from_messages(messages)


if __name__ == "__main__":
    pdf_file_path = "papers/paper_1.pdf"

    print(f"正在读取 PDF：{pdf_file_path} ...")
    paper_text = extract_text_from_pdf(pdf_file_path)

    # 2. 检查一下是不是读到了空内容（万一 PDF 是扫描图片呢）
    if not paper_text.strip():
        print("⚠️ 警告：没有从 PDF 中读取到任何文字，它可能是扫描版的图片。")
    else:
        print(f"读取成功！共提取 {len(paper_text)} 个字符。")
        print("正在分析论文...\n")

        # 3. 把提取出的文字传给 summarize_paper
        result = summarize_paper(paper_text)
        print("=== 论文分析结果 ===")
        print(result)