import os, sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import json

from PyQt5.QtCore import QDir

if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication
    from scripts.custom_widgets import NoteFilesViewer


static_path = "./data"
notes_path = "./data/notes"


def get_json_data(name):
    with open(f"{static_path}{name}", "r", encoding="utf-8") as file:
        return json.load(file)


def get_note(absolute_path):
    assert os.path.isfile(absolute_path), "Its's not a file"
    with open(absolute_path, "r", encoding="utf-8") as file:
        return json.load(file)


def save_note(absolute_path, data):
    with open(absolute_path, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    app = QApplication([])
    abs_notes_path = QDir().currentPath()
    print(os.path.join(QDir().currentPath(), "data", "notes"))
    win = NoteFilesViewer(os.path.join(QDir().currentPath(), "data", "notes"))
    win.show()
    app.exec_()
