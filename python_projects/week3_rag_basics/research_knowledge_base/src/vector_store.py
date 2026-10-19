
from langchain_community.vectorstores import Chroma


def create_vector_store(
    chunks,
    embedding_model,
    persist_directory="./data/vector_db"
):
    """创建向量数据库。用于首次构建知识库。"""
    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embedding_model,
        persist_directory=persist_directory
    )
    return vector_store


def get_vector_store(
    embedding_model,
    persist_directory="./data/vector_db"
):
    """打开已有的向量数据库。"""
    vector_store = Chroma(
        persist_directory=persist_directory,
        embedding_function=embedding_model
    )
    return vector_store
