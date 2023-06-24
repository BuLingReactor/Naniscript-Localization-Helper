from PyQt5.QtWidgets import QMainWindow, QMenu, QAction, QFileDialog, QMessageBox, QSplitter
from PyQt5.QtCore import Qt
from fileHandler import FileHandler
from spreadsheetEditor import SpreadsheetEditor
from selectableList import SelectableList

class MainWindow(QMainWindow):
    def __init__(self, clipboard):
        super().__init__()
        self.file_handler = FileHandler()
        self.initUI()
        self.clipboard = clipboard

    def initUI(self):
        self.createMenuBar()
        self.createMainWindow()

    def createMenuBar(self):
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('File')

        selectOriginalFolderAction = QAction('Select original text folder', self)
        selectOriginalFolderAction.triggered.connect(self.selectOriginalFolder)
        fileMenu.addAction(selectOriginalFolderAction)

        selectLocalizationFolderAction = QAction('Select localization folder', self)
        selectLocalizationFolderAction.triggered.connect(self.selectLocalizationFolder)
        fileMenu.addAction(selectLocalizationFolderAction)

        saveProgressAction = QAction('Save progress', self, shortcut='Ctrl+S')
        saveProgressAction.triggered.connect(self.saveProgress)
        fileMenu.addAction(saveProgressAction)

        loadProgressAction = QAction('Load progress', self, shortcut='Ctrl+O')
        loadProgressAction.triggered.connect(self.loadProgress)
        fileMenu.addAction(loadProgressAction)

        exportToClipboardAction = QAction('Export to clipboard', self, shortcut='Ctrl+E')
        exportToClipboardAction.triggered.connect(self.exportToClipboard)
        fileMenu.addAction(exportToClipboardAction)

        exportAllToSingleCSVAction = QAction('Export all to single CSV', self, shortcut='Ctrl+Shift+E')
        exportAllToSingleCSVAction.triggered.connect(self.exportAllToSingleCSV)
        fileMenu.addAction(exportAllToSingleCSVAction)

        exportToXlsxAction = QAction('Export all to xlsx', self, shortcut='Ctrl+X')
        exportToXlsxAction.triggered.connect(self.exportAllToXlsx)
        fileMenu.addAction(exportToXlsxAction)

        importFromCSVAction = QAction('Import from CSV', self, shortcut='Ctrl+I')
        importFromCSVAction.triggered.connect(self.importFromCSV)
        fileMenu.addAction(importFromCSVAction)


        # saveAllToFileAction = QAction('Save all to files', self, shortcut='Ctrl+Alt+S')
        # saveAllToFileAction.triggered.connect(self.saveAllToFile)
        # fileMenu.addAction(saveAllToFileAction)

    def createMainWindow(self):
        self.splitter = QSplitter(Qt.Horizontal)

        self.spreadsheet_editor = SpreadsheetEditor(file_handler=self.file_handler)
        self.selectable_list = SelectableList(self.file_handler, self.spreadsheet_editor)
        self.spreadsheet_editor.selectable_list = self.selectable_list
        self.splitter.addWidget(self.selectable_list)
        self.splitter.addWidget(self.spreadsheet_editor)

        self.setCentralWidget(self.splitter)

    def selectOriginalFolder(self):
        folder_path = QFileDialog.getExistingDirectory(self, 'Select original text folder')
        if folder_path:
            self.file_handler.setOriginalFolderPath(folder_path)
            self.selectable_list.updateList()

    def selectLocalizationFolder(self):
        folder_path = QFileDialog.getExistingDirectory(self, 'Select localization folder')
        if folder_path:
            self.file_handler.setLocalizationFolderPath(folder_path)
            self.selectable_list.updateList()

    def saveProgress(self):
        self.file_handler.saveProgress()
        self.file_handler.saveAllToFile()

    def loadProgress(self):
        self.file_handler.loadProgress()
        self.selectable_list.updateList()

    def exportToClipboard(self):
        df = self.spreadsheet_editor.getDataFrame()
        self.clipboard.setText(df.to_csv(index=False))

    def exportAllToSingleCSV(self):
        filename, _ = QFileDialog.getSaveFileName(self, 'Save File', '', 'CSV Files (*.csv)')
        if filename:
            self.file_handler.exportAllToSingleCSV(filename)

    def exportAllToXlsx(self):
        xlsxFilename, _ = QFileDialog.getSaveFileName(self, 'Save File', '', 'XLSX Files (*.xlsx)')
        if xlsxFilename:
            self.file_handler.exportAllToXlsx(xlsxFilename)

    def importFromCSV(self):
        filename, _ = QFileDialog.getOpenFileName(self, 'Save File', '', 'CSV Files (*.csv)')
        if filename:
            self.file_handler.importFromCSV(filename)

    # def saveAllToFile(self):
    #     self.file_handler.saveAllToFile()
