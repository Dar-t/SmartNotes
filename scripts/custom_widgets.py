from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QPushButton,
    QListWidget,
    QListWidgetItem,
    QTreeView,
    QFileSystemModel,
    QFileIconProvider,
    QStyledItemDelegate,
)
from PyQt5.QtCore import (
    Qt,
    QFileInfo,
    QDir,
    QModelIndex,
    QItemSelection,
    QItemSelectionModel,
    QRect,
)
from PyQt5.QtGui import QIcon
import os, sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from icons.icon_provider import get_icon, get_icon_path


class MainWindow(QWidget):
    EXIT_CODE_REBOOT = -123456789

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def closeEvent(self, event):
        for window in QApplication.topLevelWidgets():
            window.close()


class NormalButton(QPushButton):
    def __init__(self, text: str | None, parent: QWidget | None = None):
        super().__init__(text, parent)
        self.setProperty("className", "normalBtn")
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.classList = []

    def addClass(self, className):
        self.classList.append(className)
        self.setProperty("className", " ".join(["normalBtn", *self.classList]))

    def removeClass(self, className):
        self.classList.remove()
        self.setProperty("className", " ".join(["normalBtn", *self.classList]))


class MiniButton(QPushButton):
    def __init__(
        self,
        icon: QIcon | None = None,
        text: str | None = None,
        parent: QWidget | None = None,
    ):
        super().__init__(icon, text, parent)
        self.setProperty("className", "miniBtn")
        self.setCursor(Qt.CursorShape.PointingHandCursor)

    def addClass(self, className):
        self.classList.append(className)
        self.setProperty("className", " ".join(["miniBtn", *self.classList]))

    def removeClass(self, className):
        self.classList.remove()
        self.setProperty("className", " ".join(["normalBtn", *self.classList]))


class ListViewer(QListWidget):
    def __init__(self, selection_icon: QIcon | None, parent: QWidget | None = None):
        super().__init__(parent)
        self.selection_icon = selection_icon
        self.__selected_option = ""

    def select_option(self, item: QListWidgetItem | None):
        if self.selection_icon:
            self.findItems(self.__selected_option, Qt.MatchFlag.MatchExactly)[
                0
            ].setData(Qt.ItemDataRole.DecorationRole, None)
            if item:
                item.setIcon(self.selection_icon)


class CustomIconProvider(QFileIconProvider):
    def icon(self, fileInfo):
        if fileInfo.isDir():
            icon = get_icon("folderIcon")
            icon.addFile(get_icon_path("folderOpenIcon"), state=icon.On)
            return icon
        else:
            if fileInfo.completeSuffix() == "note.json":
                return get_icon("noteIcon")
        return QFileIconProvider.icon(self, fileInfo)


class NameDelegate(QStyledItemDelegate):
    def initStyleOption(self, option, index):
        super().initStyleOption(option, index)
        if isinstance(index.model(), QFileSystemModel):
            if (
                index.model().fileInfo(index).isFile()
                and index.model().fileInfo(index).completeSuffix() == "note.json"
            ):
                option.text = index.model().fileInfo(index).baseName()

    def setEditorData(self, editor, index):
        if isinstance(index.model(), QFileSystemModel):
            if (
                index.model().fileInfo(index).isFile()
                and index.model().fileInfo(index).completeSuffix() == "note.json"
            ):
                editor.setText(index.model().fileInfo(index).baseName())
            else:
                super().setEditorData(editor, index)

    def setModelData(self, editor, model, index):
        if isinstance(model, QFileSystemModel):
            fi = model.fileInfo(index)
            if not model.isDir(index):
                model.setData(index, editor.text() + "." + fi.completeSuffix())
            else:
                model.setData(index, editor.text())


class NoteFilesViewer(QTreeView):
    initial_filters = ["*.note.json"]

    def __init__(
        self,
        path,
        parent: QWidget | None = None,
    ):
        super().__init__(parent)
        model = QFileSystemModel()
        model.setNameFilters(NoteFilesViewer.initial_filters)
        model.setNameFilterDisables(False)
        model.setIconProvider(CustomIconProvider())
        model.setOptions(QFileSystemModel.Option.DontUseCustomDirectoryIcons)
        model.setReadOnly(False)
        self.setItemDelegate(NameDelegate())
        self.setModel(model)
        self.setRootIndex(model.setRootPath(path))
        self.setAnimated(False)
        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        for index in range(1, self.model().columnCount()):
            self.setColumnHidden(index, True)
        self.header().hide()
        self.setExpandsOnDoubleClick(False)
        self.setRootIsDecorated(False)
        self.clicked.connect(self.expand_on_click)
        self.setIndentation(10)
        self.setEditTriggers(self.EditTrigger.NoEditTriggers)

    def model(self) -> QFileSystemModel:
        return super().model()

    def expand_on_click(self, index):
        self.setExpanded(index, not self.isExpanded(index))

    def mousePressEvent(self, event):
        if not self.indexAt(event.pos()).isValid():
            self.selectionModel().clear()
        super().mousePressEvent(event)
