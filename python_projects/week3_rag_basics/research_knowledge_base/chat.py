from langchain_community.vectorstores import Chroma
from src.llm import generate_answer
from src.embedding import get_embedding_model
from src.qa import retrieve_documents

# 1.加载embedding模型
embedding_model = get_embedding_model()

# 2.加载已有向量数据库
db = Chroma(
    persist_directory="./data/vector_db",
    embedding_function=embedding_model
)
# 3.输入问题

query = input(
    "请输入问题："
)

# 4.检索
docs = retrieve_documents(
    db,
    query,
    k=5
)

context = ""

for doc in docs:
    context += doc.page_content + "\n"

answer = generate_answer(
    query,
    context
)

print("\n===== AI回答 =====\n")
print(answer)
