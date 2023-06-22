from PyQt5.QtWidgets import QListWidget
from spreadsheetEditor import SpreadsheetEditor
import os

class SelectableList(QListWidget):
    def __init__(self, file_handler, editor):
        super().__init__()
        self.file_handler = file_handler
        self.editor = editor
        self.itemClicked.connect(self.loadFile)
        self.last_item = None

    def updateList(self):
        self.clear()
        files = self.file_handler.getFiles()
        for file in files:
            self.addItem(file)

    def loadFile(self, item):
        # Save current changes
        # current_file = self.currentItem().text() if self.currentItem() else None
        # if self.last_item:
        #     df = self.editor.getDataFrame()
        #     filename = os.path.join(self.file_handler.localization_folder_path, self.last_item)
        #     print(filename)
        #     self.file_handler.saveData(filename, df)

        # Load new file
        filename = os.path.join(self.file_handler.localization_folder_path, item.text())
        df = self.file_handler.loadFile(filename)
        self.editor.update(df)
        self.last_item = item.text()