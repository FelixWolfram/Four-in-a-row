# check for win or draw --> 1 = player1 has won; -1 = player2 has won; 0 = draw
def check_for_winner(board_height, board_width, board, next_free_row):
    draw = True
    for c in range(board_width):  # check for draw --> no fields left
        if next_free_row[c] > -1:  # if not all check_for_free pointers are "over" the board --> game not ended
            draw = False
            break
    if draw:
        return 0

    # no draw, check whether one player has a connect four
    # check rows
    for r in range(board_height):
        count = [0, 0]  # first number for player1, second for player2
        for c in range(board_width):
            if (player_won := loop_over_board(r, c, count, board)) != 0:    # player_won = 0 if the first player won, 1 if the second player won
                return player_won

    # check columns
    for c in range(board_width):
        count = [0, 0]
        for r in range(board_height):
            if (player_won := loop_over_board(r, c, count, board)) != 0:
                return player_won

    # check diagonals
    for r in range(board_height - 3):
        count = [0, 0]
        for c in range(board_width):  # we don't have to check the last 3 rows/columns, because there can't be 4 chips diagonally
            if r + c < board_height:
                if (player_won := loop_over_board(r + c, c, count, board)) != 0:
                    return player_won
    for r in range(board_height - 1, 2, -1):
        count = [0, 0]
        for c in range(board_width):
            if r - c > -1:
                if (player_won := loop_over_board(r - c, c, count, board)) != 0:
                    return player_won
    for r in range(board_width - 3):
        count = [0, 0]
        for c in range(board_height):
            if r + c < board_width:
                if (player_won := loop_over_board(c, r + c, count, board)) != 0:
                    return player_won
    for r in range(board_width - 1, 2, -1):
        count = [0, 0]
        for c in range(board_height):
            if r - c > -1:
                if (player_won := loop_over_board(c, r - c, count, board)) != 0:
                    return player_won
    # two rows are still in blind spots by the four diagonal checks
    if board[5][3] == board[4][4] == board[3][5] == board[2][6] != 0:
        return -1 if board[4][4] == 1 else 1
    if board[5][2] == board[4][3] == board[3][4] == board[2][5] != 0 or \
       board[4][3] == board[3][4] == board[2][5] == board[1][6] != 0:
       return -1 if board[3][4] == 1 else 1
    return 0

def loop_over_board(r, c, count, board):
    if board[r][c] == 1:
        count[0] += 1
        count[1] = 0
    elif board[r][c] == 2:
        count[0] = 0
        count[1] += 1
    else:  # if a 0 was found
        count[0] = 0
        count[1] = 0
    if 4 in count:
        if count.index(4) == 0:  # index = 0 if the first player won, 1 if the second player won
            return -1   # -1, if player1 won
        else:
            return 1    # 1, if player2 won
    return 0
