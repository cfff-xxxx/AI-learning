import os
import json
import argparse

def load_config(config_path="config.json"):
    """加载json配置文件"""
    if os.path.exists(config_path):
        with open(config_path, "r", encoding="utf-8") as f:
            return json.load(f)
    # 不存在配置文件返回默认值
    return {
        "paper_dir": "./papers",
        "keyword": "Agent",
        "enable_pdf": False
    }

def count_keyword(text: str, keyword: str):
    if not keyword:
        return 0
    return text.count(keyword)

def scan_papers(folder_path, target_keyword):
    print("=====论文批量统计开始=====\n")
    total_lines = 0
    total_words = 0
    total_key_cnt = 0

    if not os.path.exists(folder_path):
        print(f"❌ 文件夹不存在：{folder_path}")
        return

    for filename in os.listdir(folder_path):
        file_full_path = os.path.join(folder_path, filename)
        content = ""
        line_count = 0

        try:
            if filename.endswith(".txt"):
                with open(file_full_path, "r", encoding="utf-8") as f:
                    lines = f.readlines()
                    content = "".join(lines)
                    line_count = len(lines)
            else:
                continue

            word_list = content.split()
            word_list = [w for w in word_list if w.strip()]
            word_count = len(word_list)
            key_count = count_keyword(content, target_keyword)

            total_lines += line_count
            total_words += word_count
            total_key_cnt += key_count

            print(f"文件：{filename}")
            print(f"  行数：{line_count} | 分词字数：{word_count} | 关键词[{target_keyword}]出现：{key_count}\n")
        except Exception as e:
            print(f"❌ 读取失败 {filename}，错误：{e}\n")

    print("=====汇总统计=====")
    print(f"全部论文总行数：{total_lines}")
    print(f"全部论文总词数：{total_words}")
    print(f"关键词 [{target_keyword}] 总共出现：{total_key_cnt}")


if __name__ == "__main__":
    # 1.加载配置文件
    cfg = load_config()

    # 2.解析命令行参数，覆盖配置
    parser = argparse.ArgumentParser(description="论文统计 + json配置文件")
    parser.add_argument("--keyword", type=str, help="关键词（优先级高于config.json）")
    parser.add_argument("--dir", type=str, help="论文目录（优先级高于config.json）")
    args = parser.parse_args()

    # 参数覆盖逻辑
    keyword = args.keyword if args.keyword else cfg["keyword"]
    paper_dir = args.dir if args.dir else cfg["paper_dir"]

    print(f"当前使用配置：paper_dir={paper_dir}, keyword={keyword}\n")
    scan_papers(paper_dir, keyword)
