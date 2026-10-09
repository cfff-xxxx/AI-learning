import json
import os
import logging
import requests

logging.basicConfig(level=logging.INFO,format="%(asctime)s-%(levelname)s-%(message)s")
logger=logging.getLogger(__name__)

def send_paper_meta_to_api(json_file_path:str):
    if not os.path.exists(json_file_path):
        logger.error(f"{json_file_path}不存在，请先运行paper_json_stat")
        return
    with open(json_file_path,"r",encoding="utf-8")as f:
        payload_data=json.load(f)#json文件->python列表/字典对象

    url="https://httpbin.org/post"
    try:
        logger.info("正在把pdf解析得到的论文元数据post发送API")
        resp=requests.post(url,json=payload_data,timeout=10)
        resp.raise_for_status()#检查http状态码
        res_json=resp.json()#把服务器返回的内容转为python对象
        logger.info("API返回结果：")
        logger.info(json.dumps(res_json,ensure_ascii=False,indent=2))#json_dumps:把python对象->json字符串
        sent_data=res_json["json"]
        logger.info(f"\n回传校验，我们发送的论文题目：{sent_data[0]['title']}")

    except requests.exceptions.RequestException as e:
        logger.error(f"api请求失败{e}")

if __name__=="__main__":
    send_paper_meta_to_api("paper_meta.json")