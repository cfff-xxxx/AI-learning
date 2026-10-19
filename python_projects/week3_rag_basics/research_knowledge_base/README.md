# Research Knowledge Base RAG

基于 RAG（Retrieval-Augmented Generation，检索增强生成）的 AI 论文知识库。项目面向 AI 论文阅读场景，将 PDF 论文转换为可检索的文本片段，通过向量检索获取相关内容，并调用大语言模型辅助回答问题。

## 1. 项目功能

- **PDF 解析**：读取 PDF 论文并提取文本。
- **文本切分**：将长文档切分为适合检索的文本片段。
- **向量化**：使用 BGE 中文 Embedding 模型将文本转换为向量。
- **向量存储与检索**：使用 Chroma 保存和检索文本向量。
- **智能问答**：将检索到的论文内容作为上下文，调用 DeepSeek 生成回答。
- **HTTP API**：使用 FastAPI 提供接口，支持健康检查、论文上传、问答和检索。

## 2. 技术栈

- Python
- FastAPI
- LangChain
- Chroma
- HuggingFace Embeddings
- BAAI/bge-small-zh-v1.5
- DeepSeek API
- PyPDF

## 3. 项目结构

```text
research_knowledge_base/
├── main.py                 # FastAPI 服务入口
├── build_kb.py             # 构建论文知识库
├── chat.py                 # 问答相关脚本
├── requirements.txt        # Python 依赖
├── README.md               # 项目说明
└── src/
    ├── embedding.py        # Embedding 模型
    ├── llm.py              # 大语言模型调用
    ├── pdf_loader.py       # PDF 解析
    ├── text_splitter.py    # 文本切分
    ├── vector_store.py     # 向量存储与检索
    ├── qa.py               # 问答逻辑
    └── rag_service.py      # RAG 服务逻辑
```

## 4. 环境准备

建议使用 Python 虚拟环境。请在项目目录中执行以下命令。

安装依赖：

```bash
python -m pip install -r requirements.txt
```

## 5. 配置 API Key

在项目根目录创建 `.env` 文件，并配置 DeepSeek API Key：

```dotenv
OPENAI_API_KEY=你的DeepSeek_API_Key
```

项目通过 OpenAI 兼容客户端调用 DeepSeek API，因此这里的环境变量名为 `OPENAI_API_KEY`。

请勿将 `.env` 文件、真实 API Key 或其他敏感信息提交到 GitHub。

## 6. 运行服务

在项目根目录启动 FastAPI 服务：

```bash
python -m uvicorn main:app --reload
```

启动后，可以通过以下地址访问：

- 服务入口：http://127.0.0.1:8000/
- 健康检查：http://127.0.0.1:8000/health
- API 文档：http://127.0.0.1:8000/docs

请根据实际启动结果确认服务地址和接口状态。

## 7. API 接口

项目当前提供以下接口：

| 接口 | 用途 |
| --- | --- |
| `GET /` | 服务入口 |
| `GET /health` | 健康检查 |
| `POST /chat` | 基于知识库进行问答 |
| `POST /upload` | 上传论文 PDF |
| `POST /search` | 检索相关论文内容 |

可以打开 `/docs` 查看接口参数、请求格式和响应结果。

## 8. 数据与安全说明

- 论文 PDF 属于本地数据，不默认提交到 GitHub。
- Chroma 向量数据库及备份属于本地运行数据，不默认提交到 GitHub。
- `.env` 中的 API Key 不应公开。
- 首次运行时，Embedding 模型可能需要从 Hugging Face 下载。

## 9. 当前项目目标

本项目用于学习和实践 RAG 的基本流程，包括 PDF 文档处理、文本切分、Embedding、向量检索、大语言模型调用以及 FastAPI 接口封装。

后续可以进一步改进检索质量、回答的可追溯性、异常处理和项目部署能力。
