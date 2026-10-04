import json
#读取json
with open("paper.json","r",encoding="utf-8")as f:
    paper_data=json.load(f)

print("===读取到的原始论文信息===")
print(paper_data)

paper_data["year"] = 2026
paper_data["keywords"].append("LLM")
paper_data["title"] = "Agentic Plan Caching for LLM"

print("\n===修改后的论文信息===")
print(paper_data)

#保存回json
with open("paper.json","w",encoding="utf-8")as f:
    json.dump(paper_data,ensure_ascii=False,indent=4)

print("\n✅ 文件保存完成！")
