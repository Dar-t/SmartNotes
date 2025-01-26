import os
from PyQt5.QtCore import Qt, QDir
from PyQt5.QtWidgets import QFileDialog, QMessageBox
import json.scanner
import pathlib

HOME = os.path.join(pathlib.Path.home(), "Downloads")


def import_notes(location):
    save_path = QFileDialog.getOpenFileName(
        directory=HOME,
        filter="Notepack (*.notepack.json)",
        initialFilter="Notepack (*.notepack.json)",
    )
    if save_path[0]:
        try:
            with open(save_path[0], "r", encoding="utf-8") as file:
                notes_to_import = json.load(file)
            for notepath in notes_to_import.keys():
                if len(notepath.split("/")) > 1:
                    os.makedirs(
                        os.path.join(location, *notepath.split("/")[:-1]), exist_ok=True
                    )
                with open(
                    os.path.join(location + notepath + ".note.json"),
                    "w",
                    encoding="utf-8",
                ) as file:
                    json.dump(
                        notes_to_import[notepath], file, ensure_ascii=False, indent=4
                    )
        except Exception as e:
            QMessageBox.critical(
                None,
                "Ошибка импорта",
                f"Не удалось прочитать файл! \n{e}",
                QMessageBox.StandardButton.Ok,
            )
