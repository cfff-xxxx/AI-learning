from pathlib import Path
from src.pdf_loader import load_pdf
from src.text_splitter import split_documents
from src.embedding import get_embedding_model
from src.qa import retrieve_documents
from src.llm import generate_answer
from src.vector_store import get_vector_store

BASE_DIR = Path(__file__).resolve().parent.parent
VECTOR_DB_DIR = BASE_DIR / "data" / "vector_db"

embedding_model = None
db = None


def get_db():
    """获取已有向量数据库；首次调用时初始化。"""
    global embedding_model, db

    if db is None:
        if not VECTOR_DB_DIR.exists():
            raise FileNotFoundError(
                f"找不到向量数据库：{VECTOR_DB_DIR}，请先运行 build_kb.py"
            )

        embedding_model = get_embedding_model()
        db = get_vector_store(
            embedding_model=embedding_model,
            persist_directory=str(VECTOR_DB_DIR)
        )

    return db


def add_pdf_to_knowledge_base(pdf_path: str) -> dict:
    """解析新 PDF，并将切片追加到现有向量数据库。"""

    docs = load_pdf(pdf_path)

    if not docs:
        raise ValueError("PDF 没有解析出任何页面")

    chunks = split_documents(docs)

    if not chunks:
        raise ValueError("PDF 没有提取到可用文本")

    vector_db = get_db()

    # 为每个切片补充来源信息，便于以后追踪论文来源
    for chunk in chunks:
        chunk.metadata["source"] = Path(pdf_path).name

    vector_db.add_documents(chunks)

    return {
        "filename": Path(pdf_path).name,
        "pages": len(docs),
        "chunks_added": len(chunks)
    }


def answer_question(question: str) -> dict:
    question = question.strip()

    if not question:
        raise ValueError("问题不能为空")

    vector_db = get_db()
    docs = retrieve_documents(vector_db, question, k=5)

    if not docs:
        raise ValueError("知识库中没有检索到相关内容")

    context = "\n\n".join(doc.page_content for doc in docs)
    answer = generate_answer(question, context)

    return {
        "question": question,
        "answer": answer,
        "retrieved_chunks": len(docs)
    }

def search_knowledge_base(question: str, k: int = 5) -> list:
    """只检索知识库，不调用大模型。"""
    vector_db = get_db()
    docs = retrieve_documents(vector_db, question, k=k)

    results = []

    for doc in docs:
        results.append({
            "content": doc.page_content,
            "source": doc.metadata.get("source", "未知来源")
        })

    return results
