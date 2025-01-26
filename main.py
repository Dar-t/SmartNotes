import json.tool
from PyQt5.QtCore import Qt, QModelIndex, QFileInfo, QProcess, QCoreApplication
from PyQt5.QtWidgets import (
    QAbstractItemView,
    QApplication,
    QMessageBox,
    QFileDialog,
)
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout
from PyQt5.QtWidgets import (
    QLabel,
    QLineEdit,
    QTextEdit,
    QListWidget,
)
from PyQt5.QtWidgets import QShortcut
from PyQt5.QtGui import QKeySequence
import json

import json.scanner

app = QApplication([])

from styles.style_data import app_style
from icons.icon_provider import get_icon
from scripts.utils import show_or_focus
from scripts.custom_widgets import *
from scripts.notes_imorting import import_notes
from data.data_provider import get_note
from windows.filters_win import filters_initializer
from windows.export_win import export_initializer
import os


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def restart():
    app.exit(MainWindow.EXIT_CODE_REBOOT)


def select_root_path():
    path = QFileDialog.getExistingDirectory(
        None, "Выберите папку для хранения заметок", app_state["data_path"]
    )
    if path:
        app_state["data_path"] = path
        restart()


# display data [
def display_tags(taglist):
    tags_browser.clear()
    for tag in taglist:
        tags_browser.addItem(tag)
    tags_browser.sortItems(Qt.SortOrder.AscendingOrder)


def load_note(note: QModelIndex):
    global folder_state
    save_note()
    item_info: QFileInfo = note.model().fileInfo(note)
    if item_info.isFile():
        if folder_state["current_note"]["path"] != item_info.absoluteFilePath():
            try:
                load_note_data(item_info)
                notes_editor_label.setText(folder_state["current_note"]["name"])
                notes_editor.setDisabled(False)
            except:
                QMessageBox.critical(
                    None,
                    "Ошибка при загрузке файла",
                    "Файл повреждён или пуст",
                    buttons=QMessageBox.StandardButton.Close,
                )
                tags_browser.clear()
                notes_editor.clear()
                notes_browser.setCurrentIndex(QModelIndex())
                notes_editor_label.setText("[Здесь будет имя заметки]")
                folder_state["current_note"] = {
                    "name": "",
                    "path": "",
                }
                notes_editor.setDisabled(True)


def load_note_data(item_info: QFileInfo):
    folder_state["current_note"]["path"] = item_info.absoluteFilePath()
    folder_state["current_note"]["name"] = item_info.baseName()
    note_data = get_note(folder_state["current_note"]["path"])
    notes_editor.setText(note_data.get("text", ""))
    display_tags(note_data["tags"])


# ]
# edit notes [
def save_note():
    global folder_state
    if os.path.exists(folder_state["current_note"]["path"]):
        with open(folder_state["current_note"]["path"], "w", encoding="utf-8") as file:
            taglist = [tags_browser.item(i).text() for i in range(tags_browser.count())]
            note_obj = {"text": notes_editor.toPlainText(), "tags": taglist}
            json.dump(note_obj, file, ensure_ascii=False, indent=4)


def del_item():
    if notes_browser.selectedIndexes():
        note_to_remove = notes_browser.selectedIndexes()[0]
        notes_browser.model().remove(note_to_remove)
        tags_browser.clear()
        notes_editor.clear()
        notes_browser.setCurrentIndex(QModelIndex())
        notes_editor_label.setText("[Здесь будет имя заметки]")
        folder_state["current_note"] = {
            "name": "",
            "path": "",
        }
        notes_editor.setDisabled(True)


def create_note():
    empty_data = {
        "text": "",
        "tags": [],
    }
    if notes_browser.selectedIndexes():
        selected_info = notes_browser.model().fileInfo(
            notes_browser.selectedIndexes()[0]
        )
        if selected_info.isDir() and notes_browser.isExpanded(
            notes_browser.selectedIndexes()[0]
        ):
            empty_path = selected_info.filePath()
        else:
            empty_path = selected_info.path()
    else:
        empty_path = app_state["data_path"]
    num = 1
    while os.path.exists(f"{os.path.join(empty_path, 'New note')} {num}.note.json"):
        num += 1
    empty_path = f"{os.path.join(empty_path, 'New note')} {num}.note.json"
    with open(empty_path, "w", encoding="utf-8") as file:
        json.dump(empty_data, file, indent=4, ensure_ascii=False)
    notes_browser.setCurrentIndex(notes_browser.model().index(empty_path))
    notes_browser.edit(notes_browser.model().index(empty_path))


def create_folder():
    if notes_browser.selectedIndexes():
        selected_info = notes_browser.model().fileInfo(
            notes_browser.selectedIndexes()[0]
        )
        if selected_info.isDir() and notes_browser.isExpanded(
            notes_browser.selectedIndexes()[0]
        ):
            empty_path = selected_info.filePath()
        else:
            empty_path = selected_info.path()
    else:
        empty_path = app_state["data_path"]
    num = 1
    while os.path.exists(f"{os.path.join(empty_path, 'New folder')} {num}"):
        num += 1
    notes_browser.model().mkdir(
        notes_browser.model().index(empty_path), f"New folder {num}"
    )
    notes_browser.setCurrentIndex(
        notes_browser.model().index(f"{os.path.join(empty_path, 'New folder')} {num}")
    )
    notes_browser.edit(
        notes_browser.model().index(f"{os.path.join(empty_path, 'New folder')} {num}")
    )


def rename_item():
    if notes_browser.selectedIndexes():
        notes_browser.edit(notes_browser.selectedIndexes()[0])


# ]
# edit note tags [
def create_tag():
    if os.path.exists(folder_state["current_note"]["path"]):
        tag = tags_input.text()
        taglist = [
            tags_browser.item(i).text().lower() for i in range(tags_browser.count())
        ]
        if tag and tag.lower() not in taglist:
            tags_browser.addItem(tag)
            tags_browser.sortItems(Qt.SortOrder.AscendingOrder)
            tags_input.clear()


def del_tag():
    tags_to_remove = tags_browser.selectedItems()
    if tags_to_remove:
        for tag in tags_to_remove:
            tags_browser.takeItem(tags_browser.row(tag))


# ]
# other [
def toggle_expanded(index: QModelIndex):
    file_info = notes_browser.model().fileInfo(index)
    if file_info.isDir():
        if notes_browser.isExpanded(index):
            folder_state["expanded"].add(file_info.filePath())
        else:
            folder_state["expanded"].discard(file_info.filePath())


# ]
exit_code = MainWindow.EXIT_CODE_REBOOT
while exit_code == MainWindow.EXIT_CODE_REBOOT:
    app_state = {
        "data_path": "",
    }
    folder_state = {
        "current_note": {
            "name": "",
            "path": "",
        },
        "expanded": [
            # "path1", "path2"
        ],
    }
    state_data_path = "app_state.json"
    try:
        with open(state_data_path, "r", encoding="utf-8") as raw_data:
            app_state = json.load(raw_data)

    except Exception as e:
        with open(state_data_path, "w", encoding="utf-8") as file:
            json.dump(app_state, file, ensure_ascii=False, indent=4)

    if not os.path.exists(app_state["data_path"]):
        path = QFileDialog.getExistingDirectory(
            None, "Выберите папку для хранения заметок"
        )
        if path:
            app_state["data_path"] = path
            restart()
        else:
            QMessageBox.critical(None, "Ошибка", "Директория не выбрана")
            sys.exit()
    folder_state_path = os.path.join(app_state["data_path"], "folder_state.json")
    try:
        with open(folder_state_path, "r", encoding="utf-8") as file:
            save_state = json.load(file)
            for key in save_state.keys():
                folder_state[key] = save_state[key]
    except Exception as e:
        with open(folder_state_path, "w", encoding="utf-8") as file:
            json.dump(folder_state, file, ensure_ascii=False, indent=4)

    folder_state["expanded"] = set(folder_state["expanded"])

    # widgets -----------------------------------
    MAIN_WIN = MainWindow()

    notes_editor = QTextEdit()
    notes_editor_label = QLabel("[Здесь будет имя заметки]")

    notes_browser = NoteFilesViewer(app_state["data_path"])
    notes_browser_label = QLabel("Список заметок")

    EXPORT_WIN = export_initializer(os.path.join(app_state["data_path"] + "\\"))
    FILTERS_WIN = filters_initializer(
        file_view=notes_browser, label=notes_browser_label
    )

    notes_create = NormalButton("Создать заметку")
    notes_delete = NormalButton("Удалить элемент")
    notes_mkdir = NormalButton("Создать папку")
    notes_rename = NormalButton("Переименовать элемент")

    notes_import = MiniButton(get_icon("importIcon.png"))
    notes_export = MiniButton(get_icon("exportIcon.png"))
    open_another_folder = MiniButton(get_icon("folderOpenIcon.png"))

    tags_browser = QListWidget()
    tags_browser_label = QLabel("Список тегов заметки")
    tags_input = QLineEdit()
    tags_create = NormalButton("Добавить тег")
    tags_delete = NormalButton("Удалить тег")

    filters_open = NormalButton("Фильтры")

    # layouts -----------------------------------
    main_hlayout = QHBoxLayout()

    notes_buttons_hlayout = QHBoxLayout()
    notes_buttons_hlayout2 = QHBoxLayout()

    tags_buttons_hlayout = QHBoxLayout()
    tags_buttons_hlayout2 = QHBoxLayout()

    editor_title_hlayout = QHBoxLayout()
    editor_group_hlayout = QHBoxLayout()

    interact_vlayout = QVBoxLayout()
    editor_vlayout = QVBoxLayout()

    # links -------------------------------------
    notes_buttons_hlayout.addWidget(notes_create)
    notes_buttons_hlayout.addWidget(notes_delete)

    notes_buttons_hlayout2.addWidget(notes_mkdir)
    notes_buttons_hlayout2.addWidget(notes_rename)

    interact_vlayout.addWidget(notes_browser_label)
    interact_vlayout.addWidget(notes_browser)
    interact_vlayout.addLayout(notes_buttons_hlayout)
    interact_vlayout.addLayout(notes_buttons_hlayout2)

    tags_buttons_hlayout.addWidget(tags_create)
    tags_buttons_hlayout.addWidget(tags_delete)

    tags_buttons_hlayout2.addWidget(filters_open)

    interact_vlayout.addWidget(tags_browser_label)
    interact_vlayout.addWidget(tags_browser)
    interact_vlayout.addWidget(tags_input)
    interact_vlayout.addLayout(tags_buttons_hlayout)
    interact_vlayout.addLayout(tags_buttons_hlayout2)

    editor_group_hlayout.addWidget(open_another_folder)
    editor_group_hlayout.addWidget(notes_import)
    editor_group_hlayout.addWidget(notes_export)

    editor_title_hlayout.addWidget(notes_editor_label)
    editor_title_hlayout.addLayout(editor_group_hlayout)

    editor_vlayout.addLayout(editor_title_hlayout)
    editor_vlayout.addWidget(notes_editor)

    main_hlayout.addLayout(interact_vlayout)
    main_hlayout.addLayout(editor_vlayout)

    MAIN_WIN.setLayout(main_hlayout)

    # connects / interactions -------------------
    notes_browser.clicked.connect(load_note)
    notes_browser.clicked.connect(toggle_expanded)
    # notes_browser.model().fileRenamed.connect(prevent_file_recreating)

    notes_create.clicked.connect(create_note)
    notes_delete.clicked.connect(del_item)
    notes_mkdir.clicked.connect(create_folder)
    notes_rename.clicked.connect(rename_item)

    open_another_folder.clicked.connect(select_root_path)
    notes_import.clicked.connect(lambda: import_notes(app_state["data_path"]))
    notes_export.clicked.connect(EXPORT_WIN.show)

    tags_create.clicked.connect(create_tag)
    tags_delete.clicked.connect(del_tag)

    filters_open.clicked.connect(lambda: show_or_focus(FILTERS_WIN))

    # shortcuts ---------------------------------
    shortcut_save = QShortcut(QKeySequence("Ctrl+S"), notes_editor)
    shortcut_save.activated.connect(save_note)

    shortcut_rename = QShortcut(QKeySequence("F2"), notes_browser)
    shortcut_rename.activated.connect(rename_item)

    # style / settings --------------------------

    tags_browser.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
    tags_browser.setFocusPolicy(Qt.FocusPolicy.NoFocus)

    # widget styling [
    notes_delete.addClass("deleteBtn")
    tags_input.setContentsMargins(0, 5, 0, 0)
    tags_input.setPlaceholderText("Введите тег...")
    notes_editor.setPlaceholderText("Введите текст заметки...")
    notes_editor_label.setContentsMargins(0, 9, 0, 0)
    # ]

    # layout styling [
    notes_buttons_hlayout.setContentsMargins(0, 5, 0, 0)
    interact_vlayout.setSpacing(6)
    editor_vlayout.setSpacing(6)
    interact_vlayout.setContentsMargins(0, 9, 0, 0)
    main_hlayout.setStretch(0, 1)
    main_hlayout.setStretch(1, 2)
    # ]

    # app styling [
    MAIN_WIN.setWindowTitle("Умные заметки")
    MAIN_WIN.resize(1000, 700)
    MAIN_WIN.setMinimumSize(600, 400)
    app.setStyle("Fusion")
    app.setStyleSheet(app_style)
    MAIN_WIN.setWindowIcon(get_icon("noteIcon.png"))
    # ]

    # run ---------------------------------------
    to_remove = []
    for path in folder_state["expanded"]:
        if os.path.exists(path):
            notes_browser.expand(notes_browser.model().index(path))
        else:
            to_remove.append(path)
    for path in to_remove:
        folder_state["expanded"].discard(path)
    if os.path.exists(folder_state["current_note"]["path"]):
        index = notes_browser.model().index(folder_state["current_note"]["path"])
        folder_state["current_note"]["path"] = ""
        notes_browser.setCurrentIndex(index)
        load_note(index)
    else:
        folder_state["current_note"] = {"path": "", "name": ""}

    notes_editor.setDisabled(True)

    MAIN_WIN.show()

    exit_code = app.exec()

    # exit --------------------------------------
    save_note()
    with open(state_data_path, "w", encoding="utf-8") as file:
        json.dump(app_state, file, ensure_ascii=False, indent=4)

    with open(folder_state_path, "w", encoding="utf-8") as file:
        folder_state["expanded"] = list(folder_state["expanded"])
        json.dump(folder_state, file, ensure_ascii=False, indent=4)
