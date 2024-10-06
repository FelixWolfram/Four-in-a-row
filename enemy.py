from check_for_winner import check_for_winner


class Computer:
    def __init__(self, board_height, board_width):
        self.board_height = board_height
        self.board_height = board_height
        self.board_width = board_width
        self.memo = {}
        self.recursion_depth = 0
        self.max_recursion_depth = 4

    # OPTIMIERUNGEN, DIE VORGENOMMEN WERDEN MÜSSEN:
                    # ES KANN NICHT DER GANZE BAUM BERECHNET WERDEN, DESHALB MIT MEMOIZATION ARBEITEN
    # NUR BIS Z.B. TIEFE 5 BERECHNEN, NICHT DEN KOMPLETTEN BAUM
        # (--> ÜBER TIEFE 5 (WENN ES NOCH KEIN KLARES ERGEBNIS GIBT) EINFACH 0 (DRAW) ZURÜCKGEBEN) --> GEHT BISHER EIGENTLICH

    # ES KÖNNTEN AKTUELL PROBLEME GEGEGEN ENDE MIT VOLLEM BOARD AUFTAUCHEN, WEIL:
    # WENN SO WEIT BERECHENT WIRD, DASS ES EIN VOLLES BOARD GIBT, WIRD NICHTS MEHR IN DIE LISTE EINGETRAGEN
    # --> ES KÖNNTE EIN ERROR GEBEN, DA VERSUCHT WIRD MIN() AUF EINE LEERE LISTE ANZUWENDEN

    # AUßERDEM: MUSS SCHNELLER WERDEN UND GIBT IMMER NOCH MANCHMAL PROBLEME, DASS IN EINE VOLLE LISTE GESETZT WIRD
    # UND ES GIBT EINE FALSCHE LÖSUNG BEI DEM AKTUELL EINGETRAGENEN BOARD (VIELLEICHT AUCH NUR WEGEN EINER ZU KLEINEN RECURSION DEPTH)
    def computer_move(self, board, player1, nfrs):  # nfrs = next free rows
        col_results = []
        self.recursion_depth = 0
        for col in nfrs:
            if nfrs[col] > -1:  # if row is not full, insert a chip
                board[nfrs[col]][col] = 1 if player1 else 2  # enter "1" for player 1, "2" for player 2
                nfrs[col] -= 1

                winner = check_for_winner(self.board_height, self.board_width, board, nfrs)
                if winner != 0:
                    nfrs[col] += 1
                    board[nfrs[col]][col] = 0  # reset move

                    col_results.append((winner, col))
                else:
                    self.recursion_depth += 1
                    winner_for_path = self.evaluate_board(board, not player1, nfrs)
                    self.recursion_depth -= 1

                    col_results.append((winner_for_path, col))

                    nfrs[col] += 1
                    board[nfrs[col]][col] = 0   # reset move

        if player1: # get min
            result = min(col_results, key=lambda x: x[0]) # get the lowest item, get the index (column) and return it
        else:       # get max
            result = max(col_results, key=lambda x: x[0])
        return result[1]


    def evaluate_board(self, board, player1, nfrs):     # player1 wants to get min, player2 wants to get max
        if self.recursion_depth > self.max_recursion_depth:   # only evaluate the next 10 moves to make a guess which could be the best move
            return 0
        col_results = []    # stores tuple of the result with the column belonging to it
        for col in nfrs:
            # try to insert a chip in every row that is not already full
            if nfrs[col] > -1:  # if column is not full
                board[nfrs[col]][col] = 1 if player1 else 2  # enter "1" for player 1, "2" for player 2
                nfrs[col] -= 1

                winner = check_for_winner(self.board_height, self.board_width, board, nfrs) # check if a player won
                if winner != 0:
                    nfrs[col] += 1
                    board[nfrs[col]][col] = 0  # reset move

                    col_results.append((winner, col))
                else:
                    self.recursion_depth += 1
                    winner_for_path = self.evaluate_board(board, not player1, nfrs)
                    self.recursion_depth -= 1

                    col_results.append((winner_for_path, col))

                    nfrs[col] += 1
                    board[nfrs[col]][col] = 0  # reset move
        if player1: # get min
            # get the lowest item --> x is one tuple, the min-function then compares after the first element of the tuple
            result = min(col_results, key=lambda x: x[0])
        else:       # get max
            result = max(col_results, key=lambda x: x[0]) # get the highest item
        return result[0]



if __name__ == "__main__":   # only executed when run as a script
    board = [[   2,     0,    0,    0,    0,    0,    0],
             [   2,     0,    2,    0,    0,    0,    0],
             [   1,     2,    1,    0,    0,    0,    0],
             [   2,     2,    1,    1,    0,    0,    0],
             [   2,     1,    1,    1,    2,    1,    0],
             [   2,     1,    2,    1,    1,    1,    2]]
    nfrs =   {0: -1, 1: 1, 2: 0, 3: 2, 4: 3, 5: 3, 6: 4}
    computer = Computer(6, 7)
    solution = computer.computer_move(board, False, nfrs)
    print("best col:", solution)


#    board = [[   2,     0,    0,    0,    0,    0,    0],
#             [   2,     0,    0,    0,    0,    0,    0],
#             [   1,     0,    0,    0,    0,    2,    2],
#             [   2,     0,    0,    0,    0,    1,    1],
#             [   2,     0,    0,    0,    0,    1,    1],
#             [   2,     0,    0,    1,    2,    1,    1]]
#    nfrs =   {0: -1, 1: 5, 2: 5, 3: 4, 4: 4, 5: 1, 6: 1}
