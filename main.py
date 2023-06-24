from PyQt5.QtWidgets import QApplication
from mainWindow import MainWindow
import sys

if __name__ == "__main__":
    app = QApplication(sys.argv)
    clipboard = app.clipboard()
    window = MainWindow(clipboard)
    window.show()
    sys.exit(app.exec_())
