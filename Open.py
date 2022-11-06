from PIL import Image, ImageDraw
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from random import randint, choice
from finaly_project import Ui_Dialog
from Second_form import Second_form
import sqlite3
import datetime
from PyQt5.QtWidgets import QInputDialog, QColorDialog
from PYQT_Project import Draw_maker

def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = Draw_maker()
    form.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
