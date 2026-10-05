import os
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def batch_rename_pdf(folder: str):
    if not os.path.isdir(folder):
        logger.error(f"目录不存在：{folder}")
        return
    file_list = [f for f in os.listdir(folder) if f.lower().endswith(".pdf")]
    logger.info(f"找到 {len(file_list)} 个PDF待重命名")
    for idx, filename in enumerate(file_list, start=1):
        old_full = os.path.join(folder, filename)
        new_name = f"paper_{idx}.pdf"
        new_full = os.path.join(folder, new_name)
        os.rename(old_full, new_full)
        logger.info(f"{filename} → {new_name}")

if __name__ == "__main__":
    batch_rename_pdf("./papers")
