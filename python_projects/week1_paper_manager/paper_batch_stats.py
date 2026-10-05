import os
import argparse
from PyPDF2 import PdfReader

def extract_text_from_pdf(file_path):
    """读取pdf提取文本"""
    text = ""
    reader = PdfReader(file_path)
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text
    return text

def count_keyword(text: str, keyword: str):
    # 简单关键词计数
    if not keyword:
        return 0
    return text.lower().count(keyword.lower())

def scan_papers(folder_path, target_keyword="agent"):
    print("=====论文批量统计开始=====\n")
    total_lines = 0
    total_words = 0
    total_keyword_cnt = 0

    if not os.path.exists(folder_path):
        print(f"❌ 文件夹不存在：{folder_path}")
        return

    # 遍历目录下所有文件
    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            file_full_path = os.path.join(folder_path, filename)
            try:
                with open(file_full_path, "r", encoding="utf-8") as f:
                    lines = f.readlines()
                    content = "".join(lines)
                    # 统计行数
                    line_cnt = len(lines)
                    # 简单按空白分割算字数
                    word_list = content.split()
                    word_cnt = len(word_list)
                    kw_cnt = count_keyword(content, target_keyword)

                    total_lines += line_cnt
                    total_words += word_cnt
                    total_keyword_cnt += kw_cnt
                    print(f"文件：{filename}")
                    print(f"  行数：{line_cnt} | 字数：{word_cnt} | 关键词[{target_keyword}]出现：{kw_cnt}\n")
            except UnicodeDecodeError:
                print(f"❌ {filename} 编码错误，不是utf-8文本，跳过")
            except Exception as e:
                print(f"❌ 读取 {filename} 出错：{e}")
    print("=====汇总统计=====")
    print(f"全部论文总行数：{total_lines}")
    print(f"全部论文总词数：{total_words}")
    print(f"关键词 [{target_keyword}] 总共出现：{total_keyword_cnt}")

if __name__ == "__main__":
    parser=argparse.ArgumentParser(description="论文文本批量统计工具")
    parser.add_argument("--keyword",type=str,default="agent",help="要统计的目标关键词")
    parser.add_argument("--dir",type=str,default="./papers",help="存放论文txt的文件夹路径")
    #解析命令行参数
    args=parser.parse_args()
    scan_papers(folder_path=args.dir, target_keyword=args.keyword)
