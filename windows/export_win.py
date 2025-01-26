import os, sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from PyQt5.QtCore import Qt, QDir, QModelIndex
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QFileDialog,
)
from scripts.custom_widgets import NoteFilesViewer, NormalButton
from icons.icon_provider import get_icon
import json.scanner
import pathlib

global selected_set
selected_set = set()
HOME = os.path.join(pathlib.Path.home(), "Downloads")


class export_initializer(QWidget):
    def __init__(
        self,
        path: str,
        parent: QWidget = None,
        flags: Qt.WindowFlags | Qt.WindowType = Qt.WindowFlags(),
    ):
        super().__init__(parent=parent, flags=flags)
        self.init_ui(path)

    def init_ui(self, path):

        select_hlayout = QHBoxLayout()
        buttons_hlayout = QHBoxLayout()
        main_vlayout = QVBoxLayout()
        items_vlayout = QVBoxLayout()
        files_vlayout = QVBoxLayout()

        self.file_view = NoteFilesViewer(path)

        self.items_list = QListWidget()

        file_label = QLabel("Список файлов")
        items_label = QLabel("Выбранные заметки")

        reset_button = NormalButton("Очистить список")
        export_button = NormalButton("Экспортировать")

        main_vlayout.addLayout(select_hlayout)
        main_vlayout.addLayout(buttons_hlayout)

        select_hlayout.addLayout(items_vlayout)
        select_hlayout.addLayout(files_vlayout)

        items_vlayout.addWidget(items_label)
        items_vlayout.addWidget(self.items_list)

        files_vlayout.addWidget(file_label)
        files_vlayout.addWidget(self.file_view)

        buttons_hlayout.addWidget(reset_button)
        buttons_hlayout.addWidget(export_button)

        reset_button.addClass("deleteBtn")

        self.items_list.itemClicked.connect(self.remove_selection)
        self.file_view.clicked.connect(self.append_selection)

        reset_button.clicked.connect(self.items_list.clear)
        export_button.clicked.connect(self.export_selected)

        self.items_list.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.items_list.setObjectName("exportSelectedList")

        self.setWindowIcon(get_icon("exporterIcon"))

        self.setLayout(main_vlayout)

    def remove_selection(self, item: QListWidgetItem):
        selected_set.discard(item.text())
        self.items_list.takeItem(self.items_list.row(item))

    def append_selection(self, item: QModelIndex):
        file_info = self.file_view.model().fileInfo(item)
        if file_info.isFile():
            selected_set.add(
                file_info.filePath()
                .replace(self.file_view.model().rootPath(), "")
                .replace(".note.json", "")
            )
            self.items_list.clear()
            self.items_list.addItems(selected_set)
            self.items_list.sortItems()
        else:
            pass

    def export_selected(self):
        save_path = QFileDialog.getSaveFileName(
            None, "", HOME, "Notepacks (*.notepack.json)"
        )
        if save_path[0]:
            root = self.file_view.model().rootPath()
            ext = ".note.json"
            export_data = {}
            for pseudopath in selected_set:
                model_index = self.file_view.model().index(root + pseudopath + ext)
                real_path = self.file_view.model().filePath(model_index)
                with open(real_path, "r", encoding="utf-8") as file:
                    export_data[pseudopath] = json.load(file)

            with open(save_path[0], "w", encoding="utf-8") as file:
                json.dump(export_data, file, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    app = QApplication([])
    win = export_initializer()
    win.show()
    app.exec()
