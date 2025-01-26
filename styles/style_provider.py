import os, sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scripts.utils import getAllPaths, parse_file


if __name__ == "__main__":
    style_paths = getAllPaths("./styles/qss")
    style_data = []
    for style_path in style_paths:
        with open(style_path, "r", encoding="utf-8") as file:
            style_data.append(parse_file(style_path))
    style_data = "\n".join(style_data)
    with open("./styles/style_data.py", "w", encoding="utf-8") as file:
        file.write(f"app_style = '''{style_data}'''")
