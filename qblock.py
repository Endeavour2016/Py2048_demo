# -*- coding: utf-8 -*-
# @Time    : 2018/12/31 13:08
# @Author  : ZLM
# @FileName: qblock.py
# @Qblock: 每一个方块视为一个对象，相应的类定义为Qblock

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

"""
Qblock 类
    _value: 方块上显示的数字
    getValue(): 获取数字
"""


class Qblock(QLabel):
    def __init__(self, value=None):
        super(Qblock, self).__init__()
        self._value = value  # 方块数字初始值为 None
        # 当前方块对象中的内容设置居中
        self.setAlignment(Qt.AlignCenter)
    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, v):
        self._value = v

    # 绘制当前方块的背景
    def draw(self):
        if self._value is None:
            self.setText('')
            self.setStyleSheet("Qblock { background: rgb(204,192,179); border-radius: 10px; }")
        else:
            self.setText(str(self._value))  # 设置方块上显示的数字
            # 每种数字对应不同的背景颜色
            if self._value == 2:
                self.setStyleSheet("Qblock { background: rgb(238,228,216); color: rgb(119,110,101); \
                    font: bold; border-radius: 10px; font: 40pt; }")
            elif self._value == 4:
                self.setStyleSheet("Qblock { background: rgb(250,252,174); color: rgb(119,110,101); \
                    font: bold; border-radius: 10px; font: 40pt; }")  # 237,224,200
            elif self._value == 8:
                self.setStyleSheet("Qblock { background: rgb(242,177,121); color: rgb(255,255,255); \
                    font: bold; border-radius: 10px; font: 40pt; }")
            elif self._value == 16:
                self.setStyleSheet("Qblock { background: rgb(245,150,100); color: rgb(255,255,255); \
                    font: bold; border-radius: 10px; font: 40pt; }")
            elif self._value == 32:
                self.setStyleSheet("Qblock { background: rgb(245,125,95); color: rgb(255,255,255); \
                    font: bold; border-radius: 10px; font: 40pt; }")
            elif self._value == 64:
                self.setStyleSheet("Qblock { background: rgb(245,95,60); color: rgb(255,255,255); \
                    font: bold; border-radius: 10px; font: 40pt; }")
            elif self._value == 128:
                self.setStyleSheet("Qblock { background: rgb(237,207,114); color: rgb(255,255,255);\
                    font: bold; border-radius: 10px; font: 40pt; }")
            elif self._value == 256:
                self.setStyleSheet("Qblock { background: rgb(237,204,97); color: rgb(255,255,255); \
                    font: bold; border-radius: 10px; font: 40pt; }")

            # 当达到512以后，开始提供阴影效果
            elif self._value == 512:
                dse = QGraphicsDropShadowEffect()
                dse.setColor(QColor.yellow)
                dse.setBlurRadius(20)
                dse.setOffset(-1)
                self.setGraphicsEffect(dse)
                self.setStyleSheet("Qblock { background: rgb(237,204,97); color: rgb(255,255,255); \
                    font: bold; border-radius: 10px; font: 40pt; }")
            elif self._value == 1024:
                dse = QGraphicsDropShadowEffect()
                dse.setColor(QColor.yellow)
                dse.setBlurRadius(30)
                dse.setOffset(-1)
                self.setGraphicsEffect(dse)
                self.setStyleSheet("Qblock { background: rgb(237,204,97); color: rgb(255,255,255); \
                    font: bold; border-radius: 10px; font: 40pt; }")
            elif self._value == 2048:
                dse = QGraphicsDropShadowEffect()
                dse.setColor(QColor.yellow)
                dse.setBlurRadius(40)
                dse.setOffset(-1)
                self.setGraphicsEffect(dse)
                self.setStyleSheet("Qblock { background: rgb(237,204,97); color: rgb(255,255,255); \
                    font: bold; border-radius: 10px; font: 40pt; }")
            else:
                self.setStyleSheet("Qblock { background: rgb(238,228,218); color: rgb(119,110,101); \
                    font: bold; border-radius: 10px; font: 40pt; }")
# end class Qblock
