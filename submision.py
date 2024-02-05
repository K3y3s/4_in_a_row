import logging
from math import inf

import numpy as np

from utils import update_board_score, convert_to_arr

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
strh = logging.StreamHandler()
strh.setLevel(logging.DEBUG)
logger.addHandler(strh)


def agent_human(observation, configuration):
    return int(input(f'Choose column number ({[i + 1 for i in range(configuration.columns)]}): ')) - 1


def agent_min_max(observation, configuration):
    def min_max(board_prev: np.array, player_nb: str, columns: int, rows: int, inarow: int, deep: int) -> tuple:

        maximum = True if player_nb == '1' else False  # False for player '2'
        score_final = -inf if maximum else inf  # inf for player '2'
        column_final = 0
        all_columns_filled = True

        logger.debug(f'{"..." * deep} Deep: {deep}')
        logger.debug(f'{"..." * deep} {board_prev}')

        scores = []
        if deep == 30:
            return 0, 0

        for column_nb in range(columns):
            logger.debug(f'{"..." * deep} Column number: {column_nb}, Player_nb: {player_nb}')

            if board_prev[0, column_nb] != '0':
                if column_nb == columns - 1 and all_columns_filled:
                    return 0, column_nb
                continue
            else:
                all_columns_filled = False

            score_board, _, _ = update_board_score(board=board_prev.copy(), column_numb=column_nb, player_nb=player_nb,
                                                   rows=rows, inarow=inarow)

            if not isinstance(score_board, int):
                score_board, _ = min_max(board_prev=score_board, player_nb='2' if player_nb == '1' else '1',
                                         columns=columns, rows=rows, inarow=inarow, deep=deep + 1)

            elif player_nb == "2":
                score_board = score_board * -1

            logger.debug(f'{"..." * deep} Player: {player_nb}, Score: {score_board}, Score_final: {score_final}')
            logger.debug(f'{"..." * deep} Maximum: {maximum}, Deep: {deep}, Column nb: {column_nb}')
            scores.append(score_board)

            if score_board > score_final if maximum else score_board < score_final:
                score_final = score_board
                column_final = column_nb

            logger.debug(f'{"..." * deep} Final score: {score_final}, Final col: {column_final}')
        logger.debug(f'{"..." * deep} Score:  {score_final}, {column_final}')
        logger.debug(f'{"..." * deep} Scores: {scores}')

        return score_final, column_final

    board = observation.board
    player_nb = observation.mark
    columns = configuration.columns
    rows = configuration.rows
    inarow = configuration.inarow
    board = convert_to_arr(board, columns, rows)

    score, column_nb = min_max(board_prev=board, player_nb=player_nb, columns=columns, rows=rows, inarow=inarow, deep=0)

    return column_nb


def agent_random(observation, configuration):
    # Number of Columns on the Board.
    columns = configuration.columns
    # Number of Rows on the Board.
    rows = configuration.rows
    # Number of Checkers "in a row" needed to win.
    inarow = configuration.inarow
    # The current serialized Board (rows x columns).
    board = observation.board
    # Which player the agent is playing as (1 or 2).
    mark = observation.mark

    # Return which column to drop a checker (action).
    from random import choice
    return choice([i for i in range(columns)])


if __name__ == '__main__':
    from utils import update_board, configuration, observation, show_board

    cols = 3
    rows = 3
    inarow = 3

    game_config = configuration(cols, rows, inarow)

    board = ["0"] * cols * rows
    # board, _, _ = update_board(board, 1, "1", cols, rows, inarow)
    # board, _, _ = update_board(board, 0, "2", cols, rows, inarow)
    # board, _, _ = update_board(board, 1, "1", cols, rows, inarow)
    # board, _, _ = update_board(board, 1, "2", cols, rows, inarow)
    # board, _, _ = update_board(board, 0, "1", cols, rows, inarow)

    cols = 4
    rows = 4
    inarow = 3

    game_config = configuration(cols, rows, inarow)

    board = ["0"] * cols * rows

    board, _, _ = update_board(board, 0, "1", cols, rows, inarow)
    board, _, _ = update_board(board, 0, "2", cols, rows, inarow)
    board, _, _ = update_board(board, 0, "1", cols, rows, inarow)
    board, _, _ = update_board(board, 0, "2", cols, rows, inarow)
    board, _, _ = update_board(board, 1, "1", cols, rows, inarow)
    board, _, _ = update_board(board, 1, "2", cols, rows, inarow)
    board, _, _ = update_board(board, 1, "1", cols, rows, inarow)

    show_board(board, cols, rows)

    observ1 = observation(board, "2")

    print(agent_min_max(observ1, game_config))
