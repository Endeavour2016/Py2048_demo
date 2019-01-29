# -*- coding: utf-8 -*-
# @Time    : 2018/12/31 16:35
# @Author  : ZLM
# @FileName: game.py
# @Software: PyCharm

from PyQt5.QtWidgets import *
# from qblock import Qblock
# from board import Board, Direction
from GameBoard import GameBoard
import sys

# ------------------------------------------
if __name__ == "__main__":
    myApp = QApplication(sys.argv)
    gameBoard = GameBoard()
    gameBoard.show()
    sys.exit(myApp.exec_())
