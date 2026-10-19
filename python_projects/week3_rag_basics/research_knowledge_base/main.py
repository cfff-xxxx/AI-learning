import hashlib
import json
from fastapi import FastAPI, HTTPException, UploadFile, File
from openai import APIStatusError
from pydantic import BaseModel,Field
from pathlib import Path
from uuid import uuid4
from src.rag_service import add_pdf_to_knowledge_base, answer_question
from src.rag_service import search_knowledge_base

BASE_DIR = Path(__file__).resolve().parent
PAPERS_DIR = BASE_DIR / "papers"
HASH_INDEX_PATH = BASE_DIR / "data" / "uploaded_hashes.json"
PAPERS_DIR.mkdir(parents=True, exist_ok=True)

MAX_FILE_SIZE = 20 * 1024 * 1024  # 20 MB

app=FastAPI(
    title="Research Knowledge Base",
    description="科研论文知识库 API",
    version="1.0.0"
)
#Pydantic 请求体模型
class ChatRequest(BaseModel):
    question:str=Field(
        min_length=1,
        description="需要向论文知识库提问的问题"
    )

@app.get("/")
def root():
    return {
        "message": "Research Knowledge Base is running!"
    }

@app.get("/health")
def health_check():
    return {
        "status":"ok"
    }


@app.post("/chat")
def chat(request: ChatRequest):
    try:
        result = answer_question(request.question)
        return result

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

    except FileNotFoundError:
        raise HTTPException(
            status_code=500,
            detail="找不到向量数据库，请先构建知识库"
        )

    except APIStatusError as e:
        if e.status_code == 402:
            raise HTTPException(
                status_code=503,
                detail="大模型 API 账户余额不足或额度不可用，请检查 API 平台余额"
            )

        raise HTTPException(
            status_code=502,
            detail=f"大模型 API 调用失败，状态码：{e.status_code}"
        )


def load_uploaded_hashes():
    """读取已上传文件的指纹记录。"""
    if not HASH_INDEX_PATH.exists():
        return {}

    try:
        return json.loads(
            HASH_INDEX_PATH.read_text(encoding="utf-8")
        )
    except (json.JSONDecodeError, OSError):
        raise HTTPException(
            status_code=500,
            detail="上传记录文件损坏或无法读取"
        )


def save_uploaded_hashes(hashes):
    """保存已上传文件的指纹记录。"""
    HASH_INDEX_PATH.parent.mkdir(parents=True, exist_ok=True)
    HASH_INDEX_PATH.write_text(
        json.dumps(hashes, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )

@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    # 只允许 PDF 文件
    if not file.filename or not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="请上传 PDF 文件"
        )

    # 生成安全且不重复的文件名，避免覆盖已有论文
    safe_filename = f"{uuid4().hex}.pdf"
    save_path = PAPERS_DIR / safe_filename

    try:

        content = await file.read(MAX_FILE_SIZE + 1)

        if len(content) > MAX_FILE_SIZE:
            raise HTTPException(
                status_code=413,
                detail="PDF 文件不能超过 20 MB"
            )

        # 简单检查 PDF 文件头
        if not content.startswith(b"%PDF-"):
            raise HTTPException(
                status_code=400,
                detail="文件内容不是有效的 PDF 格式"
            )
        file_hash = hashlib.sha256(content).hexdigest()
        uploaded_hashes = load_uploaded_hashes()

        if file_hash in uploaded_hashes:
            raise HTTPException(
                status_code=409,
                detail="这份 PDF 已经上传过了，无需重复入库"
            )

        save_path.write_bytes(content)

        result = add_pdf_to_knowledge_base(str(save_path))
        uploaded_hashes[file_hash] = {
            "filename": safe_filename
        }
        save_uploaded_hashes(uploaded_hashes)

        return {
            "message": "论文上传并加入知识库成功",
            **result
        }

    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        # 失败时清理刚保存的文件，避免留下未入库的文件
        save_path.unlink(missing_ok=True)
        raise HTTPException(
            status_code=500,
            detail=f"处理 PDF 失败：{e}"
        )
    finally:
        await file.close()

class SearchRequest(BaseModel):
    question: str


@app.post("/search")
def search(request: SearchRequest):
    try:
        results = search_knowledge_base(request.question, k=5)
        return {
            "question": request.question,
            "results": results
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
