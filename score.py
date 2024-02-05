import numpy as np
from numpy.lib.stride_tricks import sliding_window_view


def score_left_right(arr, column_number: int, row_number: int, player_nb: str, inarow: int):
    player_left = 0
    player_right = 0
    increment = 0
    for i in range(column_number, -1, -1):
        if arr[row_number, i] == player_nb:
            player_left += 1
            if player_left == inarow:
                return player_left
        else:
            break

        increment += 1
        if increment > inarow:
            break

    increment = 0
    for i in range(column_number, arr.shape[1]):
        if arr[row_number, i] == player_nb:
            player_right += 1
            if player_right == inarow:
                return player_right
        else:
            break

        increment += 1
        if increment > inarow:
            break

    sum = player_right + player_left - 1
    if sum == inarow:
        return sum

    return False


def score_down_or_up(arr, column_number: int, row_number: int, player_nb: str, inarow: int,
                     direction: int):
    """
    :param direction: if 1 is going down, if 0 then going up  
    """""

    if direction == 1:
        for_loop_increment = 1
        ending_value = arr.shape[0]
    elif direction == -1:
        for_loop_increment = -1
        ending_value = -1

    player_vertical_down = 0
    player_vertex_left = 0
    player_vertex_right = 0
    increment = 0

    # if consecutive
    down = True
    left = True
    right = True

    for i in range(row_number, ending_value, for_loop_increment):

        ###mid
        if down and arr[i, column_number] == player_nb:
            player_vertical_down += 1
            if player_vertical_down == inarow:
                break
        else:
            down = False

        ##left
        if left and column_number - increment >= 0 and arr[i, column_number - increment] == player_nb:
            player_vertex_left += 1
            if player_vertex_left == inarow:
                break
        else:
            left = False

        # right
        if right and column_number + increment < arr.shape[1] and arr[i, column_number + increment] == player_nb:
            player_vertex_right += 1
            if player_vertex_right == inarow:
                break
        else:
            right = False

        increment += 1

        if increment > inarow:
            break

    return False, player_vertex_left, player_vertex_right


def all_win_possibilities(arr, inarow: int):

    def score_values_in_straight_line(arr, vals, inarow, indeks_arr, horizontal):
        window = sliding_window_view(arr, (1, inarow) if horizontal else (inarow, 1))

        for row_nb in range(vals.shape[0]):
            for col_nb in range(vals.shape[1]):
                vals[row_nb, col_nb] += np.count_nonzero(indeks_arr[row_nb, col_nb] == window)

        return vals

    def score_diagonals(arr, vals, inarow, indeks_arr, antidiagonal=False):
        window = sliding_window_view(arr, (inarow, inarow))

        diagonals = window.diagonal(axis1=2, axis2=3) if not antidiagonal else np.flip(window, axis=3).diagonal(axis1=3, axis2=2)

        for row_nb in range(vals.shape[0]):
            for col_nb in range(vals.shape[1]):
                vals[row_nb, col_nb] += np.count_nonzero(indeks_arr[row_nb, col_nb] == diagonals)

        return vals

    indeks_arr = np.arange(arr.size).reshape(arr.shape)
    vals = np.zeros(arr.shape)

    vals = score_values_in_straight_line(arr, vals, inarow, indeks_arr, horizontal=True)
    if arr.shape[0] == arr.shape[1]:
        vals = vals*2

    #for symetric arrays rows == cols vals2 is the same as one
    else:
        vals = score_values_in_straight_line(arr, vals, inarow, indeks_arr, horizontal=False)

    vals = score_diagonals(arr, vals, inarow, indeks_arr, antidiagonal=False)
    #in geneneral second function will give the same array but flipted
    vals = score_diagonals(arr, vals, inarow, indeks_arr, antidiagonal=True)

    return vals


def update_vals(arr_player, index_arr, arr_oponent, player_number, col_number, inarow):

    first_zero_row = arr.shape[0]
    while arr[first_zero_row, col_number] != 0 and first_zero_row > 0:
        first_zero_row -= 1

    column_left_index = col_number
    columns_right_index = col_number

    while arr[first_zero_row, column_left_index] != 0 and column_left_index > 0:
        column_left_index -= column_left_index

    while arr[first_zero_row, columns_right_index] != 0 and column_left_index < arr.shape[1]:
        column_left_index -= column_left_index


if __name__ == '__main__':
    rows_cols = 4
    arr = np.arange(rows_cols**2).reshape((rows_cols, rows_cols))
    score_arr(arr, inarow=3)
