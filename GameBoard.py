# -*- coding: utf-8 -*-
# @Time    : 2018/12/31 14:31
# @Author  : ZLM
# @FileName: GameBoard.py

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from board import Board, Direction
from qblock import Qblock


# GameBoard: 游戏主界面类(board面板 + Score QLabel + Button)
class GameBoard(QWidget):
    def __init__(self, parent=None):
        super(GameBoard, self).__init__(parent)
        # 游戏状态数据
        self._game_over = False
        self._game_win = False
        self.record = 0
        # create the board with 4*4 blocks
        self.board = Board(4)
        # qBlockBoard 用于存放 Qblock 方块对象
        self.qBlockBoard = [[None] * self.board.get_dimension for i in range(self.board.get_dimension)]

        self.init_gui()
        self.start_game()

    # Qblock对象只需要创建一次，后续更新时只用改变方格里的数字
    def init_draw_board(self):
        board_layout = QGridLayout()
        for i in range(self.board.get_dimension):
            for j in range(self.board.get_dimension):
                self.qBlockBoard[i][j] = Qblock(None)
                board_layout.addWidget(self.qBlockBoard[i][j], i, j)
                self.qBlockBoard[i][j].draw()
        self.main_layout.addLayout(board_layout)

    # 2019_1_30 add
    def init_gui(self):
        # set window size and overall layout
        self.resize(600, 450)
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

        # score, record, restart button
        self.hbox_layout = QHBoxLayout()
        self.scoreLabel = QLabel(("SCORE: %s" % self.board.score))
        self.scoreLabel.setStyleSheet("QLabel { color: rgb(0,0,255); font: 16pt; }")
        self.scoreLabel.setFixedSize(180, 30)
        self.hbox_layout.addWidget(self.scoreLabel, Qt.AlignLeft)

        self.recordLabel = QLabel(("RECORD: %s" % self.record))
        self.recordLabel.setStyleSheet("QLabel { color: rgb(0,0,255); font: 16pt; }")
        self.recordLabel.setFixedSize(180, 30)
        self.hbox_layout.addWidget(self.recordLabel, Qt.AlignLeft)

        self.restartButton = QPushButton('Restart')
        self.restartButton.setStyleSheet("QPushButton { background: rgb(204,192,179); \
                    font: 15pt; }")
        self.restartButton.setFixedSize(100, 30)
        self.restartButton.clicked.connect(self.start_game)

        # 没有这一行代码, 方向键是用于设置button焦点, 导致方块无法移动
        self.restartButton.setFocusPolicy(Qt.NoFocus)
        self.hbox_layout.addWidget(self.restartButton, Qt.AlignLeft)
        self.main_layout.addLayout(self.hbox_layout)

        # background-color of the game board
        self.setStyleSheet("GameBoard { background: rgb(187,173,160) }")
        self.init_draw_board()

    def display_board(self):
        for i in range(self.board.get_dimension):
            for j in range(self.board.get_dimension):
                # 从board中取出当前矩阵中存放的数字
                self.qBlockBoard[i][j].value = self.board.get_block(i, j)
                self.qBlockBoard[i][j].draw()

    # game_over: reserve current score, update the record
    def game_over(self):
        if self.record > self.board.score:
            self.record = self.board.score
            try:
                with open("record.txt", "w") as fp:
                    fp.write(str(self.record))
            except IOError as err:
                print(err)
        reply = QMessageBox.question(self, "Game Over", "Game over, Restart?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        if reply == QMessageBox.Yes:
            self.start_game()
        else:
            self.close()

    # 重写了Widget的keyPressEvent函数，用于响应用户按键输入
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Up:
            self.move_block(Direction.Up)
            print("Key->Up")
        elif event.key() == Qt.Key_Left:
            self.move_block(Direction.Left)
            print("Key->Left")
        elif event.key() == Qt.Key_Right:
            self.move_block(Direction.Right)
            print("Key->Right")
        elif event.key() == Qt.Key_Down:
            self.move_block(Direction.Down)
            print("Key->Down")

    # move blocks
    def move_block(self, direction):
        self.board.move_num(direction)

        # judge game states
        if not self.board.move_possible():
            self._game_over = True

        self.update_state()

    # update game state: nums, score
    def update_state(self):
        if self._game_over:  # 游戏结束：弹出game over窗口
            print("Game Over!")
            self.game_over()
        elif self._game_win:
            print("You Win!")
            # game win information
            QMessageBox.information(self, 'WIN', 'You get 2048! \n Continue?')

        self.scoreLabel.setText(("SCORE: %s" % self.board.score))
        self.display_board()

    def start_game(self):
        self.board.board_reset()
        self.board.score = 0
        self.scoreLabel.setText(("SCORE: %s" % self.board.score))
        # read score.txt 2019_1_30
        try:
            with open("record.txt") as fp:
                self.record = int(fp.read())
        except (IOError, ValueError) as err:
            print("read record error: %s" % err)
            self.record = 0
        self.board.add_rand_block()
        self.board.add_rand_block()
        self.display_board()

    # Respond to close event
    def closeEvent(self, QCloseEvent):
        res = QMessageBox.question(self, 'close', "close game?",
                                   QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if res == QMessageBox.Yes:
            QCloseEvent.accept()
            if self.record >= self.board.score:
                self.record = self.board.score
                try:
                    with open('record.txt', 'w') as fp:
                        fp.write(str(self.record))
                except IOError as err:
                    print(err)
        else:
            QCloseEvent.ignore()
