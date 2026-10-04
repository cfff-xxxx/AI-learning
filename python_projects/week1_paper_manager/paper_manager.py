import json

if __name__ == "__main__":
    try:
        # 1. 读取paper.json
        with open("paper.json", "r", encoding="utf-8") as f:
            paper_data = json.load(f)

        print("===读取到的原始论文信息===")
        print(paper_data)

        # 2. 修改内容
        paper_data["year"] = 2026
        paper_data["keywords"].append("LLM")
        paper_data["title"] = "Agentic Plan Caching for LLM"

        print("\n===修改后的论文信息===")
        print(paper_data)

        # 3. 保存回json文件
        with open("paper.json", "w", encoding="utf-8") as f:
            json.dump(paper_data, f, ensure_ascii=False, indent=4)

        print("\n✅ 文件保存完成！")

    except FileNotFoundError:
        print("❌ 错误：找不到 paper.json 文件")
    except json.JSONDecodeError:
        print("❌ 错误：json文件格式损坏，无法解析")
    except Exception as e:
        print(f"❌ 未知错误：{e}")
