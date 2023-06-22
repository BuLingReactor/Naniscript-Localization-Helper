from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem
import pandas as pd
import os

class SpreadsheetEditor(QTableWidget):
    def __init__(self, df=pd.DataFrame(), file_handler=None, selectable_list=None):
        super().__init__()
        self.df = df
        self.file_handler = file_handler
        self.selectable_list = selectable_list
        self.initUI()
        self.cellChanged.connect(self.saveChanges)

    def saveChanges(self):
        current_item = self.selectable_list.currentItem()
        if current_item:
            current_file = os.path.join(self.file_handler.localization_folder_path, current_item.text())
            df = self.getDataFrame()
            self.file_handler.saveData(current_file, df)

    def initUI(self):
        self.setColumnCount(len(self.df.columns))
        self.setRowCount(len(self.df.index))
        self.setHorizontalHeaderLabels(self.df.columns)
        for i in range(len(self.df.index)):
            for j in range(len(self.df.columns)):
                self.setItem(i, j, QTableWidgetItem(str(self.df.iat[i, j])))

    def update(self, df):
        self.clear()
        self.df = df
        self.initUI()

    def getDataFrame(self):
        data = []
        for i in range(self.rowCount()):
            row = []
            for j in range(self.columnCount()):
                item = self.item(i, j)
                row.append(item.text() if item else '')
            data.append(row)
        return pd.DataFrame(data, columns=['ID', 'Speaker/Command', 'Original Text', 'Translated Text'])