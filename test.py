# -*- coding: utf-8 -*-
# @Time    : 2018/12/31 19:23
# @Author  : ZLM
# @FileName: test.py
# @Software: PyCharm

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys


# 该类的对象可以作为MainWin类的一个成员
class widgets(QWidget):
    def __init__(self, parent=None):
        super(widgets, self).__init__(parent)
        self.setWindowTitle("widgets")
        # self.setFixedSize(400, 200)

        self.box = QVBoxLayout()
        self.label = QLabel('L1')
        self.box.addWidget(self.label)
        self.setLayout(self.box)
        self.label.setStyleSheet("QLabel { color: rgb(0,102,255); font: 16pt; }")


class MainWin(QWidget):
    def __init__(self):
        super(MainWin, self).__init__()
        self.setWindowTitle("test")
        self.sub = widgets()

        label = QLabel('Main')

        # 布局
        self.box = QVBoxLayout()
        self.setLayout(self.box)
        self.box.addWidget(self.sub)
        self.box.addWidget(label)
        # QMessageBox.information(self, 'title', 'Information')

app = QApplication(sys.argv)
w = MainWin()
w.show()
sys.exit(app.exec_())
