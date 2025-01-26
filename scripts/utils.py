import os.path
from datetime import datetime
from PyQt5.QtWidgets import QWidget


def getAllPaths(directory):
    path_list = []
    for dirpath, _, filenames in os.walk(directory):
        for f in filenames:
            path_list.append(os.path.join(dirpath, f))
    return path_list


def timestring_get():
    date = datetime.now()
    return (
        f"{date.year}/{date.month}/{date.day} {date.hour}:{date.minute}:{date.second}"
    )


def parse_file(path):
    try:
        with open(path, "r", encoding="utf-8") as file:
            return file.read()
    except:
        pass


def show_or_focus(widget: QWidget):
    if not widget.isVisible():
        widget.show()
    else:
        widget.raise_()
        widget.activateWindow()


def timestring_parse(date):
    return datetime.strptime(date, "%Y/%m/%d %H:%M:%S")
