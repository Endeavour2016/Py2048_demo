# -*- coding: utf-8 -*-
# @Time    : 2019/1/3 21:24
# @Author  : ZLM
# @FileName: testMoveUp.py
# @Software: PyCharm


# 向上移动move up
def move_up(blockMatrix):
    print("calling board.move_up")
    for col in range(4):
        # 当前列的元素从上到下开始 move up
        for row in range(0, 4):
            # 先找到当前列第一个非 None 的元素
            if blockMatrix[row][col] is not None:
                r = 0
                while r < row:
                    if blockMatrix[r][col] is None and no_block_in_col(blockMatrix, col, r, row):
                        blockMatrix[r][col] = blockMatrix[row][col]
                        blockMatrix[row][col] = None
                    elif blockMatrix[r][col] == blockMatrix[row][col] and \
                            no_block_in_col(blockMatrix, col, r, row):
                        # 合并数字, 更新计分
                        blockMatrix[r][col] += blockMatrix[row][col]
                        blockMatrix[row][col] = None
                    r += 1


# 判断当前行的 c1 列和 c2 列之间是否有方块
def no_block_in_row(blockMatrix, row, c1, c2):
    i = c1 + 1
    while i < c2:
        if blockMatrix[row][i] is not None:
            return False
        #i += 1
    else:
        return True

# 判断当前列的 r1 行和 r2 行之间是否有方块
def no_block_in_col(blockMatrix, col, r1, r2):
    i = r1 + 1
    while i < r2:
        if blockMatrix[i][col] is not None:
            return False
        #i += 1
    else:
        return True


if __name__ == "__main__":
    matrix = [[None]*4 for i in range(4)]
    matrix[0][0] = 4
    matrix[1][0] = 2
    matrix[2][0] = None
    matrix[3][0] = 4

    print(matrix)

    move_up(matrix)

    print(matrix)
