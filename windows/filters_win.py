import os, sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QApplication
from PyQt5.QtWidgets import (
    QWidget,
    QLabel,
    QLineEdit,
    QComboBox,
)
from scripts.custom_widgets import NormalButton, NoteFilesViewer
from icons.icon_provider import get_icon


class Filterer:
    sort_types = {
        "А-Я": {
            "index": 0,
            "order": Qt.SortOrder.AscendingOrder,
        },
        "Я-А": {
            "index": 0,
            "order": Qt.SortOrder.DescendingOrder,
        },
        "Дата создания (с новых)": {
            "index": 2,
            "order": Qt.SortOrder.AscendingOrder,
        },
        "Дата создания (со старых)": {
            "index": 2,
            "order": Qt.SortOrder.DescendingOrder,
        },
        "Дата обновления (с новых)": {
            "index": 3,
            "order": Qt.SortOrder.AscendingOrder,
        },
        "Дата обновления (со старых)": {
            "index": 3,
            "order": Qt.SortOrder.DescendingOrder,
        },
    }

    def filter_note_name(file_view: NoteFilesViewer, text):
        file_view.model().setNameFilters(["*" + text + "*"])

    filter_types = {
        "Без фильтрации": {
            "func": lambda *args: None,
            "symbol": None,
        },
        "По названию": {"func": filter_note_name, "symbol": "@"},
    }


class filters_initializer(QWidget):
    def __init__(
        self,
        file_view: NoteFilesViewer,
        label: QLabel,
        parent: QWidget = None,
        flags: Qt.WindowFlags | Qt.WindowType = Qt.WindowFlags(),
    ):
        super().__init__(parent=parent, flags=flags)
        self.file_view = file_view
        self.label = label
        self.init_ui()

    def init_ui(self):
        self.sort_combobox = QComboBox()
        self.filter_combobox = QComboBox()
        self.filters_input = QLineEdit()

        filters_apply = NormalButton("Применить фильтры")
        filters_reset = NormalButton("Сбросить фильтры")

        filter_win_vlayout = QVBoxLayout()

        filters_hlayout = QHBoxLayout()
        filters_hlayout2 = QHBoxLayout()

        filters_hlayout.addWidget(self.filters_input)

        filters_hlayout2.addWidget(filters_apply)
        filters_hlayout2.addWidget(filters_reset)

        filter_win_vlayout.addWidget(self.sort_combobox)
        filter_win_vlayout.addWidget(self.filter_combobox)
        filter_win_vlayout.addLayout(filters_hlayout)
        filter_win_vlayout.addLayout(filters_hlayout2)

        self.setLayout(filter_win_vlayout)

        filters_reset.clicked.connect(self.reset_filters)
        filters_apply.clicked.connect(self.apply_filters)

        self.setWindowIcon(get_icon("filterIcon.png"))
        self.setWindowTitle("Фильтры")

        self.filters_input.setPlaceholderText("Введите текст для фильтров...")
        self.sort_combobox.addItems(Filterer.sort_types.keys())
        self.filter_combobox.addItems(Filterer.filter_types.keys())

    def apply_filters(self):
        sorter = Filterer.sort_types[self.sort_combobox.currentText()]
        filterer = Filterer.filter_types[self.filter_combobox.currentText()]
        self.file_view.model().sort(sorter["index"], sorter["order"])
        self.label.setText(
            "Список заметок "
            + (
                f'({filterer["symbol"]}{self.filters_input.text()})'
                if filterer["symbol"]
                else ""
            )
        )
        if callable(filterer["func"]):
            filterer["func"](self.file_view, self.filters_input.text())

    def reset_filters(self):
        self.label.setText("Список заметок")
        self.file_view.model().sort(0, Qt.SortOrder.AscendingOrder)
        self.file_view.model().setNameFilters(NoteFilesViewer.initial_filters)


if __name__ == "__main__":
    app = QApplication([])
    FILTERS_WIN = filters_initializer()
    FILTERS_WIN.show()
    app.exec()
