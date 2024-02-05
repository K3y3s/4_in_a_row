from agents import agent1, agent2
from utils import observation, configuration, update_board, show_board
import time
#starting_configuration


rows = 4
columns = 4
inarow = 3

board = ["0"] * rows * columns

game_config = configuration(columns, rows, inarow)
observ1 = observation(board, "1")

while True:
    print('Player 1:')
    show_board(board, columns, rows)

    start = time.time()
    column_numb = agent1(observ1, game_config)
    end = time.time()
    print('Time:', end - start)
    board_before = board.copy()
    board, plr, board_after = update_board(board, column_numb, "1", columns, rows, inarow)
    if not isinstance(board, list):
        print(board, plr, "1")
        show_board(board_before, columns, rows)
        show_board(board_after, columns, rows)
        break
    print('Player 2:')
    observ2 = observation(board, "2")
    show_board(board, columns, rows)
    column_numb = agent2(observ2, game_config)
    board_before = board.copy()
    board, plr, board_after = update_board(board, column_numb, "2", columns, rows, inarow)
    if not isinstance(board, list):
        print(board, plr, "2")
        show_board(board_before, columns, rows)
        show_board(board_after, columns, rows)
        break
    observ1 = observation(board, "1")