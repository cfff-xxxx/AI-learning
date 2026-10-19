from openai import embeddings

from python_projects.week3_rag_basics.research_knowledge_base.src.embedding import get_embedding_model
from python_projects.week3_rag_basics.research_knowledge_base.src.pdf_loader import load_pdf
from python_projects.week3_rag_basics.research_knowledge_base.src.text_splitter import split_documents
from python_projects.week3_rag_basics.research_knowledge_base.src.vector_store import create_vector_store

pdf_path="./papers/Efficient Agents .pdf"
docs=load_pdf(pdf_path)

print(
    "PDF页数:",
    len(docs)
)
chunks=split_documents(docs)
print(
    "切片数量:",
    len(chunks)
)

embedding_model=get_embedding_model()

db=create_vector_store(
    chunks,
    embedding_model
)

print(
"知识库创建完成!"
)