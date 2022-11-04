from PyQt5.QtWidgets import QLabel, QMainWindow, QApplication
from PyQt5.QtGui import QPixmap
import sys

class Second_form(QMainWindow):
    def __init__(self, args):
        super().__init__()
        self.initUI(args)

    def initUI(self, args):
        self.filename = args
        self.setGeometry(400, 100, 1000, 750)
        self.setWindowTitle('Отображение картинки')
        self.pixmap = QPixmap(self.filename)
        self.image = QLabel(self)
        self.image.resize(1000, 750)
        self.image.setPixmap(self.pixmap)


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = Second_form('test')
    form.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
