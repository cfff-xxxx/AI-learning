from pathlib import Path

def create_project_dirs():
    base = Path(".")
    dirs = [
        base / "paper_notes",
        base / "python_projects",
        base / "agent_projects",
        base / "python_projects" / "week1_paper_manager"
    ]
    for d in dirs:
        d.mkdir(exist_ok=True)
        print(f"创建目录: {d.absolute()}")

if __name__ == "__main__":
    create_project_dirs()
