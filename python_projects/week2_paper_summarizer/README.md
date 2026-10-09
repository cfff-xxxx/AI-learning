# Paper Summarizer (论文智能总结工具)

输入一篇学术论文的 PDF，自动输出结构化的六段式分析。

## 🎯 核心功能
- 读取本地 PDF 文件，提取纯文本 (pdfplumber)
- 调用 DeepSeek API，通过定制 System Prompt 约束输出格式
- 输出：论文标题、研究问题、核心方法、创新点、实验结果、局限性

## ⚙️ 如何运行
1. `pip install -r requirements.txt`（记得在文件夹里生成 requirements.txt）
2. 在根目录配置 `.env` 文件，填入 `OPENAI_API_KEY`
3. `python paper_summarizer.py`

## 🧠 工程与测试思考
- **输入校验**：处理了 PDF 可能包含图片（无文字层）的异常情况
- **Token 限制**：遇到了长文本（11万字）的上下文窗口边界，为后续学习 RAG 打下基础
- **质量评估**：配合 `evaluation.py`，使用另一个大模型（考官）对总结的准确性进行断言