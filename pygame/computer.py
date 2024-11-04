from random import randint

class Computer:
    def __init__(self, check_for_winner):
        self.memo = {}
        self.recursion_depth = 0
        self.max_recursion_depth = None
        self.check_for_winner = check_for_winner


    def computer_move(self, board, player1, nfrs: dict, chip_nums):  # nfrs = next free rows
        # set the first chip always in the middle --> returns draw for every column anyway and middle is the best
        if chip_nums == (0 if player1 else 1):    # move 1
            return 3  # place chip in the middle

        col_results = []
        self.memo = {}
        self.recursion_depth = 0
        self.max_recursion_depth = 6 + round(chip_nums ** 2 / 120)
        for col in nfrs:
            if nfrs[col] > -1:  # if row is not full, insert a chip
                board[nfrs[col]][col] = 1 if player1 else 2  # enter "1" for player 1, "2" for player 2
                nfrs[col] -= 1

                winner = self.check_for_winner(nfrs, board)
                if winner != 0:
                    nfrs[col] += 1
                    board[nfrs[col]][col] = 0  # reset move
                    col_results.append((winner, col))
                    if player1 and winner == -1:
                        return col
                    if not player1 and winner == 1:
                        return col
                else:
                    self.recursion_depth += 1
                    winner_for_path = self.evaluate_board(board, not player1, nfrs)
                    self.recursion_depth -= 1

                    col_results.append((winner_for_path, col))

                    nfrs[col] += 1
                    board[nfrs[col]][col] = 0   # reset move
                    if player1 and winner_for_path == -1:
                        return col
                    if not player1 and winner_for_path == 1:
                        return col
        if not col_results:  # if col_results is empty (whole board is full and no winner) --> return draw and do not execute "min()"
            return 0
        if player1:  # get min
            result = min(col_results, key=lambda x: x[0])  # get the lowest item, get the index (column) and return it
        else:  # get max
            result = max(col_results, key=lambda x: x[0])
        if result[0] == 0 and col_results[0].count(0) > 1:
            col = self.get_random_col(col_results)
            return col
        return result[1]


    def evaluate_board(self, board, player1, nfrs):     # player1 wants to get min, player2 wants to get max
        if self.recursion_depth > self.max_recursion_depth:   # only evaluate the next 10 moves to make a guess which could be the best move
            return 0

        if str(board) + str(player1) in self.memo:
            solution_board = str(board) + str(player1)
            return self.memo[solution_board]
        col_results = []    # stores tuple of the result with the column belonging to it
        for col in nfrs:
            # try to insert a chip in every row that is not already full
            if nfrs[col] > -1:  # if column is not full
                board[nfrs[col]][col] = 1 if player1 else 2  # enter "1" for player 1, "2" for player 2
                nfrs[col] -= 1

                winner = self.check_for_winner(nfrs, board) # check if a player won
                if winner != 0:
                    nfrs[col] += 1
                    board[nfrs[col]][col] = 0  # reset move

                    col_results.append((winner, col))
                    if player1 and winner == -1:
                        self.save_before_return(board, player1, -1)
                        return -1
                    if not player1 and winner == 1:
                        self.save_before_return(board, player1, 1)
                        return 1
                else:
                    self.recursion_depth += 1
                    winner_for_path = self.evaluate_board(board, not player1, nfrs)
                    self.recursion_depth -= 1

                    col_results.append((winner_for_path, col))

                    nfrs[col] += 1
                    board[nfrs[col]][col] = 0  # reset move

                    if player1 and winner_for_path == -1:
                        self.save_before_return(board, player1, -1)
                        return -1
                    if not player1 and winner_for_path == 1:
                        self.save_before_return(board, player1, 1)
                        return 1
        if not col_results: # if col_results is empty (whole board is full and no winner) --> return draw and do not execute "min()"
            return 0
        if player1: # get min
            # get the lowest item --> x is one tuple, the min-function then compares after the first element of the tuple
            result = min(col_results, key=lambda x: x[0])
        else:       # get max
            result = max(col_results, key=lambda x: x[0]) # get the highest item
        self.save_before_return(board, player1, result[0])
        return result[0]


    def get_random_col(self, col_results):
        # 60% one of the middle 3, 40% one of the rest
        draw_list = [i for i in range(len(col_results)) if col_results[i][0] == 0]  # collect all moves resulting in a draw
        if 2 in draw_list or 3 in draw_list or 4 in draw_list:
            area_prob = randint(1, 10)
            if area_prob <= 6:
                return self.get_col(draw_list, [0, 1, 5, 6])
            else:
                return self.get_col(draw_list, [2, 3, 4])
        else:   # if all the middle columns are full
            return self.get_col(draw_list, [0, 1, 5, 6])


    def get_col(self, draw_list, col_limiter):
        while True:
            random_col = randint(min(draw_list), max(draw_list))
            if random_col in col_limiter:
                return random_col


    def save_before_return(self, board, player1, result):
        if str(board) + str(player1) not in self.memo:
            self.memo[str(board) + str(player1)] = result