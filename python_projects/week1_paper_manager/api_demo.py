import os
import json
import logging
import requests

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def send_paper_meta_to_api(json_file_path: str):
    # 读取script2输出的json
    if not os.path.exists(json_file_path):
        logger.error(f"{json_file_path}不存在，请先运行script2")
        return
    with open(json_file_path, "r", encoding="utf-8") as f:
        payload_data = json.load(f)

    url = "https://httpbin.org/post" # 公开测试post接口
    try:
        logger.info("正在把PDF解析得到的论文元数据POST发送API")
        resp = requests.post(url, json=payload_data, timeout=10)
        resp.raise_for_status()
        res_json = resp.json()
        logger.info("API返回结果：")
        logger.info(json.dumps(res_json, ensure_ascii=False, indent=2))
        # 提取API回传的我们发出去的论文数据
        sent_data = res_json["json"]
        logger.info(f"\n回传校验，我们发送的论文标题：{sent_data[0]['title']}")
    except requests.exceptions.RequestException as e:
        logger.error(f"API请求失败 {e}")

if __name__ == "__main__":
    send_paper_meta_to_api("paper_meta.json")
