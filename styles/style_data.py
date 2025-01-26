app_style = '''QComboBox {
    padding: 2px 5px 4px 5px;
    border: 1px solid black;
    border-radius: 5px;
    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 white, stop: 1 white);
}
QComboBox::down-arrow {
    image: url("./icons/files/arrowDownIcon.png");
    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 white, stop: 1 white);
}
QComboBox::down-arrow, QComboBox::drop-down:button {
    border: none;
    min-width: 20px;
    max-width: 20px;
}

.QLineEdit { padding: 2px 3px 4px 3px; }
.QLineEdit {
    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 white, stop: 1 white);
    color: black;
    border-radius: 5px;
    text-align: bottom;
    margin-bottom: 2px;
}
.QLineEdit, QTextEdit {
    border: 1px solid black;
}
QListWidget {
    border: 1px solid black;
}
QListWidget {
    selection-background-color: white;
    qproperty-iconSize: 10px;
}
QListWidget::item {
    padding: 5px;
    height: 14px;
}
QListWidget::item:selected:!active {
    background: #d1d1d1;
}
#exportSelectedList::item:hover {
    background: #ffffb7b7
}
*[className~="miniBtn"] {
    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 white, stop: 1 white);
    border: 1px solid #646464;
    min-width: 20px;
    max-width: 20px;
    min-height: 20px;
    max-height: 20px;
}
*[className~="normalBtn"] {
    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 white, stop: 1 white);
    color: black;
    border: 1px solid black;
    border-radius: 5px;
    text-align: bottom;
    margin-bottom: 2px;
    padding: 3px 3px 6px 3px;
    font-weight: 1000;
}
*[className~="normalBtn"][className~="deleteBtn"] {
    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #ff6d6d, stop: 1 #ff6d6d);
    color: white;
}
*[className~="normalBtn"]:disabled {
    color: #696969;
    border-color: #696969;
}
*[className~="normalBtn"][className~="deleteBtn"]:disabled {
    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #ffbcbc, stop: 1 #ffbcbc);
    color: #696969;
    border-color: #696969;
}
NoteFilesViewer {
    border: 1px solid black;
}
NoteFilesViewer::item {
    padding: 3px;
    height: 18px;
}
NoteFilesViewer::item:hover, NoteFilesViewer::branch:hover {
    background: #d1d1d1;
}
NoteFilesViewer::item:hover:selected, NoteFilesViewer::branch:hover:selected {
    background-color: #d1d1d1;
}
NoteFilesViewer::item:selected, NoteFilesViewer::branch:selected {
    background-color: #d1d1d1;
}
NoteFilesViewer::branch {
    background: palette(base);
}
NoteFilesViewer QLineEdit {
    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #d1d1d1, stop: 1 #d1d1d1);
    color: black;
    border-radius: 5px;
}'''