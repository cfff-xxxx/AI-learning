import os
import json
import argparse
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("paper_log.log", encoding="utf-8"),  # 日志写入文件
        logging.StreamHandler() # 控制台同时输出
    ]
)
logger = logging.getLogger(__name__)


def load_config(config_path="config.json"):
    """加载json配置文件"""
    try:
        if os.path.exists(config_path):
            with open(config_path, "r", encoding="utf-8") as f:
                cfg = json.load(f)
            logger.info(f"成功加载配置文件 {config_path}")
            return cfg
        else:
            logger.warning(f"配置文件 {config_path} 不存在，使用默认配置")
    except json.JSONDecodeError:
        logger.error(f"{config_path} JSON格式错误！")
    except Exception as e:
        logger.error(f"读取配置失败: {str(e)}")

    # 默认配置
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
    logger.info(f"开始扫描目录：{folder_path}，统计关键词：{target_keyword}")
    total_lines = 0
    total_words = 0
    total_key_cnt = 0

    if not os.path.exists(folder_path):
        logger.error(f"文件夹不存在：{folder_path}")
        return

    if not os.path.isdir(folder_path):
        logger.error(f"{folder_path}不是目录")
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
                logger.debug(f"跳过非txt文件：{filename}")
                continue

            word_list = content.split()
            word_list = [w for w in word_list if w.strip()]
            word_count = len(word_list)
            key_count = count_keyword(content, target_keyword)

            total_lines += line_count
            total_words += word_count
            total_key_cnt += key_count

            logger.info(f"【{filename}】行数:{line_count} 词数:{word_count} 关键词命中:{key_count}")

        except UnicodeDecodeError:
            logger.error(f"{filename} 文件编码错误，无法读取")
        except Exception as e:
            logger.error(f"读取文件 {filename} 异常: {str(e)}")

    logger.info("=====汇总统计=====")
    logger.info(f"全部论文总行数：{total_lines}")
    logger.info(f"全部论文总词数：{total_words}")
    logger.info(f"关键词 [{target_keyword}] 总共出现：{total_key_cnt}")


if __name__ == "__main__":
    cfg = load_config()

    parser = argparse.ArgumentParser(description="论文统计 + json配置 + logging日志")
    parser.add_argument("--keyword", type=str, help="关键词（优先级高于config.json）")
    parser.add_argument("--dir", type=str, help="论文目录（优先级高于config.json）")
    args = parser.parse_args()

    keyword = args.keyword if args.keyword else cfg["keyword"]
    paper_dir = args.dir if args.dir else cfg["paper_dir"]

    scan_papers(paper_dir, keyword)
