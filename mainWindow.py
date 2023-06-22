from PyQt5.QtWidgets import QMainWindow, QMenu, QAction, QFileDialog, QMessageBox, QSplitter
from PyQt5.QtCore import Qt
from fileHandler import FileHandler
from spreadsheetEditor import SpreadsheetEditor
from selectableList import SelectableList

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.file_handler = FileHandler()
        self.initUI()

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

    # def saveAllToFile(self):
    #     self.file_handler.saveAllToFile()
