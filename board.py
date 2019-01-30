# -*- coding: utf-8 -*-
# @Time    : 2018/12/31 13:40
# @Author  : ZLM
# @FileName: board.py
# class board：包含数字矩阵成员和方块的移动方法

from enum import Enum
from random import randint
import copy

class Direction(Enum):
    Up = 1
    Down = 2
    Left = 3
    Right = 4

# dimension 表示面板大小(dimension * dimension)
class Board:
    def __init__(self, dimension):
        self._dimension = dimension
        self._score = 0
        # blockMatrix 仅用于存放4*4个数字
        self.blockMatrix = [[None]*self.get_dimension for j in range(self.get_dimension)]

    # 方块中数字复位,用于游戏重启
    def board_reset(self):
        for i in range(self._dimension):
            for j in range(self._dimension):
                self.blockMatrix[i][j] = None

    @property
    def get_dimension(self):
        return self._dimension

    @property
    def score(self):
        return self._score

    @score.setter
    def score(self, s):
        self._score = s

    # 返回位置(i,j)的方块数字
    def get_block(self, i, j):
        return self.blockMatrix[i][j]

    # move numbers in the blocks
    def move_num(self, direction):
        block_before_move = copy.deepcopy(self.blockMatrix)  # 移动前的数字矩阵
        if direction == Direction.Up:
            self.move_up()
        elif direction == Direction.Down:
            self.move_down()
        elif direction == Direction.Left:
            self.move_left()
        elif direction == Direction.Right:
            self.move_right()

        # 如果经过上述移动后，如果方格没有满，此时可能会生成新的随机数
        if not self.is_full():
            # 如果移动前和移动后，方块中的数字没有发生变化，说明此时沿着某个方向已经没法移动
            # 此时无需生成随机数，玩家可以改变移动方向，是游戏继续
            if self.blockMatrix != block_before_move:
                self.add_rand_block()
        # 游戏的状态函数在 gameboard.py 中定义

    # 随机产生一个位置
    def random_position(self):
        pos = []
        if self.is_full():
            pos.append(-1)
            pos.append(-1)
        else:
            i = randint(0, self._dimension-1)
            j = randint(0, self._dimension - 1)
            while self.blockMatrix[i][j] is not None:
                i = randint(0, self._dimension - 1)
                j = randint(0, self._dimension - 1)
            pos.append(i)
            pos.append(j)
        return pos

    # 随机生成一个方块
    def add_rand_block(self):
        row, col = self.random_position()
        # 75%的概率产生数字2, 25%的概率产生数字4
        if row != -1 and col != -1:
            self.blockMatrix[row][col] = 2 if randint(0, 3) < 3 else 4

    # -------------- Move Algorithm ---------------
    def can_move_right(self):
        for row in range(self._dimension):
            # 单独对每一行中的元素进行判断
            for col in range(self._dimension-2, -1, -1):
                if self.blockMatrix[row][col] is not None:
                    if self.blockMatrix[row][col+1] is None \
                            or self.blockMatrix[row][col] == self.blockMatrix[row][col+1]:
                        return True
        return False

    def can_move_left(self):
        for row in range(self._dimension):
            for col in range(1, self._dimension):
                if self.blockMatrix[row][col] is not None:
                    if self.blockMatrix[row][col - 1] is None \
                            or self.blockMatrix[row][col] == self.blockMatrix[row][col - 1]:
                        return True
        return False

    # down: 每一列都是独立的, 这里对每列元素单独进行移动
    def can_move_up(self):
        for col in range(self._dimension):
            for row in range(1, self._dimension):
                if self.blockMatrix[row][col] is not None:  # 当前数字不为None, 需要判断该列上一行数字
                    if self.blockMatrix[row-1][col] is None \
                            or self.blockMatrix[row][col] == self.blockMatrix[row-1][col]:
                        return True
        return False

    def can_move_down(self):
        for col in range(self._dimension):
            for row in range(self._dimension-2, -1, -1):
                if self.blockMatrix[row][col] is not None:
                    if self.blockMatrix[row+1][col] is None \
                            or self.blockMatrix[row][col] == self.blockMatrix[row+1][col]:
                        return True
        return False

    def move_right(self):
        print("calling board.move_right()")
        for row in range(self._dimension):
            # 移动一行中的元素
            for col in range(self._dimension-1, -1, -1):
                # 当前元素为空则跳过(先找到右边第一个非None的元素)
                if self.blockMatrix[row][col] is not None:
                    k = self._dimension-1
                    while k > col:
                        if self.blockMatrix[row][k] is None and self.no_block_in_row(row, col, k):
                            # 移动数字(这里可以添加动画效果)
                            self.blockMatrix[row][k] = self.blockMatrix[row][col]
                            self.blockMatrix[row][col] = None
                        elif self.blockMatrix[row][k] == self.blockMatrix[row][col] and \
                                self.no_block_in_row(row, col, k):
                            # 合并数字, 更新计分
                            self.blockMatrix[row][k] += self.blockMatrix[row][k]
                            self._score += self.blockMatrix[row][k]
                            self.blockMatrix[row][col] = None
                        k -= 1
                    # end while

    def move_left(self):
        print("calling board.move_left()")
        for row in range(self._dimension):
            for col in range(0, self._dimension):
                # 先找到左边第一个非 None 的元素
                if self.blockMatrix[row][col] is not None:
                    k = 0
                    while k < col:
                        if self.blockMatrix[row][k] is None and self.no_block_in_row(row, k, col):
                            self.blockMatrix[row][k] = self.blockMatrix[row][col]
                            self.blockMatrix[row][col] = None
                        elif self.blockMatrix[row][k] == self.blockMatrix[row][col] and \
                                self.no_block_in_row(row, k, col):
                            # 合并数字, 更新计分
                            self.blockMatrix[row][k] += self.blockMatrix[row][k]
                            self._score += self.blockMatrix[row][k]
                            self.blockMatrix[row][col] = None
                        k += 1

    def move_up(self):
        print("calling board.move_up()")
        for col in range(self._dimension):
            # 当前列的元素从上到下开始 move up
            for row in range(0, self._dimension):
                # 先找到当前列第一个非 None 的元素
                if self.blockMatrix[row][col] is not None:
                    r = 0
                    while r < row:
                        if self.blockMatrix[r][col] is None and self.no_block_in_col(col, r, row):
                            self.blockMatrix[r][col] = self.blockMatrix[row][col]
                            self.blockMatrix[row][col] = None
                        elif self.blockMatrix[r][col] == self.blockMatrix[row][col] and \
                                self.no_block_in_col(col, r, row):
                            # 合并数字, 更新计分
                            self.blockMatrix[r][col] += self.blockMatrix[row][col]
                            self._score += self.blockMatrix[r][col]
                            self.blockMatrix[row][col] = None
                        r += 1

    def move_down(self):
        print("calling board.move_down()")
        for col in range(self._dimension):
            # 当前列的元素从下到上开始 move down
            for row in range(self._dimension-1, -1, -1):
                if self.blockMatrix[row][col] is not None:
                    r = self._dimension-1
                    while r > row:
                        if self.blockMatrix[r][col] is None and self.no_block_in_col(col, row, r):
                            self.blockMatrix[r][col] = self.blockMatrix[row][col]
                            self.blockMatrix[row][col] = None
                        elif self.blockMatrix[r][col] == self.blockMatrix[row][col] and \
                                self.no_block_in_col(col, row, r):
                            # 合并数字, 更新计分
                            self.blockMatrix[r][col] += self.blockMatrix[row][col]
                            self._score += self.blockMatrix[r][col]
                            self.blockMatrix[row][col] = None
                        r -= 1

    # 判断当前行的 c1 列和 c2 列之间是否有方块
    def no_block_in_row(self, row, c1, c2):
        i = c1 + 1
        while i < c2:
            if self.blockMatrix[row][i] is not None:
                return False
            i += 1
        else:
            return True

    # 判断当前列的 r1 行和 r2 行之间是否有方块
    def no_block_in_col(self, col, r1, r2):
        i = r1 + 1
        while i < r2:
            if self.blockMatrix[i][col] is not None:
                return False
            i += 1
        else:
            return True
    # ------------ end the Move Algorithm -------------

    def is_full(self):
        for i in range(self._dimension):
            for j in range(self._dimension):
                if self.blockMatrix[i][j] is None:
                    return False
        return True

    # 判读方块是否能继续移动, 用于判断游戏是否结束
    def move_possible(self):
        if self.is_full():
            # check if the block could be moved
            if self.can_move_up():
                return True
            if self.can_move_down():
                return True
            if self.can_move_left():
                return True
            if self.can_move_right():
                return True
            # can not move
            return False
        else:
            return True
