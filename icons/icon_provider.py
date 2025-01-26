import os, sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from PyQt5.QtGui import QIcon


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath("./icons/files")

    return os.path.join(base_path, relative_path)


# static_path = "./icons/files/"


def get_icon(icon_name):
    # return QIcon(f"{static_path}{icon_name}")
    return QIcon(resource_path(icon_name))


def get_icon_path(icon_name):
    # return f"{static_path}{icon_name}"
    return resource_path(icon_name)


if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication

    app = QApplication([])
    print(get_icon("arrowRightIcon.png"))
