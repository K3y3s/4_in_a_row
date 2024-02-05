from collections import namedtuple
from enum import Enum

import numpy as np

from score import score_left_right, score_down_or_up

# Number of Columns on the Board.
# columns = configuration.columns
# Number of Rows on the Board.
# rows = configuration.rows
# Number of Checkers "in a row" needed to win.
# inarow = configuration.inarow
configuration = namedtuple('Configuration', ['columns', 'rows', 'inarow'])

# The current serialized Board (rows x columns).
# board = observation.board
# Which player the agent is playing as (1 or 2).
# mark = observation.mark
observation = namedtuple('Observation', ['board', 'mark'])


class Score(Enum):
    Lost = -1
    Tie = 0
    Win = 1


def convert_to_arr(board: list, columns: int, rows: int) -> np.array:
    return np.reshape(np.array(board), [rows, columns])


def update_board_score(board: np.array, column_numb: int, player_nb: str, rows: int, inarow: int) -> tuple:
    arr = board

    # from the last row to the first one
    for row_numb in range(rows - 1, -1, -1):
        if arr[row_numb, column_numb] == "0":
            arr[row_numb, column_numb] = player_nb
            score = evaluate_score(arr, row_numb, column_numb, inarow, player_nb)
            if score:
                return 1, player_nb, list(arr.flatten())

            for c in range(arr.shape[0]):
                if arr[0, c] == "0":
                    return arr, None, None

            return 0, None, board


def update_board(board: list, column_numb: int, player_nb: str, columns: int, rows: int, inarow: int) -> tuple:
    arr = convert_to_arr(board, columns, rows)
    score, player_nb, board = update_board_score(arr, column_numb, player_nb, rows, inarow)
    if isinstance(score, int):
        return Score(score).name, player_nb, board
    else:
        return list(score.flatten()), player_nb, board

def show_board(board: list, columns: int, rows: int) -> None:
    print(convert_to_arr(board, columns, rows))


def evaluate_score(arr: np.array, row_number: int, column_number: int, inarow: int, player_nb: str) -> bool | int:

    score = score_left_right(arr, column_number, row_number, player_nb, inarow)

    if score == inarow:
         return score

    ## down
    down, left_down, right_down = score_down_or_up(arr, column_number, row_number, player_nb, inarow, 1)
    if down == inarow, left

    ## up
    up, left_up, right_up = score_down_or_up(arr, column_number, row_number, player_nb, inarow, -1)

    if left_down + right_up - 1 >= inarow or left_up + right_down - 1 >= inarow:
        return 1

    return 0


if __name__ == '__main__':
    cols = 3
    rows = 3
    inarow = 2

    board = ["0"] * cols * rows
    board, _, _ = update_board(board, cols - 2, "1", cols, rows, inarow)
    board = update_board(board, cols - 2, "1", cols, rows, inarow)
    print('Should win 1')
    print(board)

    board = ["0"] * cols * rows
    board, _, _ = update_board(board, cols - 2, "1", cols, rows, inarow)
    board = update_board(board, cols - 1, "1", cols, rows, inarow)
    print('Should win 1')
    print(board)

    board = ["0"] * cols * rows
    board, _, _ = update_board(board, cols - 1, "1", cols, rows, inarow)
    board = update_board(board, cols - 2, "1", cols, rows, inarow)
    print('Should win 1')
    print(board)

    board = ["0"] * cols * rows
    board, _, _ = update_board(board, cols - 2, "1", cols, rows, inarow)
    board, _, _ = update_board(board, cols - 1, "2", cols, rows, inarow)
    board = update_board(board, cols - 1, "1", cols, rows, inarow)
    print('Should win 1')
    print(board)

    board = ["0"] * cols * rows
    board, _, _ = update_board(board, cols - 3, "1", cols, rows, inarow)
    board, _, _ = update_board(board, cols - 3, "2", cols, rows, inarow)
    board = update_board(board, cols - 3, "2", cols, rows, inarow)
    print('Should win 2')
    print(board)

    board = ["0"] * cols * rows
    board, _, _ = update_board(board, cols - 3, "1", cols, rows, inarow)
    board, _, _ = update_board(board, cols - 3, "2", cols, rows, inarow)
    board = update_board(board, cols - 3, "2", cols, rows, inarow)
    print('Should win 2')
    print(board)

    board = ["0"] * cols * rows
    board, _, _ = update_board(board, cols - 3, "1", cols, rows, 6)
    board, _, _ = update_board(board, cols - 3, "1", cols, rows, 6)
    board, _, _ = update_board(board, cols - 3, "1", cols, rows, 6)
    board = update_board(board, cols - 3, "1", cols, rows, 6)
    print('Should lost 1')
    print(board)

    board = ["0"] * cols * rows
    board, _, _ = update_board(board, cols - 3, "1", cols, rows, 3)
    board, _, _ = update_board(board, cols - 3, "2", cols, rows, 3)
    board, _, _ = update_board(board, cols - 3, "2", cols, rows, 3)
    board, _, _ = update_board(board, cols - 2, "2", cols, rows, 3)
    board, _, _ = update_board(board, cols - 2, "1", cols, rows, 3)
    board, _, _ = update_board(board, cols - 2, "2", cols, rows, 3)
    board, _, _ = update_board(board, cols - 1, "2", cols, rows, 3)
    board, _, _ = update_board(board, cols - 1, "2", cols, rows, 3)
    board = update_board(board, cols - 1, "1", cols, rows, 3)
    print('Should win 1')
    print(board)

    cols = 2
    rows = 2
    board = ["0"] * cols * rows
    board, _, _ = update_board(board, cols - 2, "1", cols, rows, 6)
    board, _, _ = update_board(board, cols - 2, "1", cols, rows, 6)
    board, _, _ = update_board(board, cols - 1, "1", cols, rows, 6)
    board = update_board(board, cols - 1, "1", cols, rows, 6)
    print('Should Tie')
    print(board)

    cols = 5
    rows = 5
    board = ["0"] * cols * rows
    board, _, _ = update_board(board, 1, "1", cols, rows, 4)
    board, _, _ = update_board(board, 0, "2", cols, rows, 4)
    board, _, _ = update_board(board, 2, "1", cols, rows, 4)
    board, _, _ = update_board(board, 2, "2", cols, rows, 4)
    board, _, _ = update_board(board, 0, "1", cols, rows, 4)
    board, _, _ = update_board(board, 4, "2", cols, rows, 4)
    board, _, _ = update_board(board, 3, "1", cols, rows, 4)
    board, _, _ = update_board(board, 4, "2", cols, rows, 4)
    board, _, _ = update_board(board, 2, "1", cols, rows, 4)
    board, _, _ = update_board(board, 1, "2", cols, rows, 4)
    board, _, _ = update_board(board, 1, "1", cols, rows, 4)
    board = update_board(board, 3, "2", cols, rows, 4)
    print('Should win 2')
    # show_board(board, cols, rows)
    print(board)

    cols = 5
    rows = 5
    board = ["0"] * cols * rows
    board, _, _ = update_board(board, 0, "2", cols, rows, 3)
    board, _, _ = update_board(board, 1, "1", cols, rows, 3)
    board, _, _ = update_board(board, 2, "1", cols, rows, 3)
    board, _, _ = update_board(board, 2, "1", cols, rows, 3)
    board, _, _ = update_board(board, 2, "2", cols, rows, 3)
    board = update_board(board, 1, "2", cols, rows, 3)
    print('Should win 2')
    # show_board(board, cols, rows)
    print(board)
