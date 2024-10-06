from check_for_winner import check_for_winner


class Computer:
    def __init__(self, board_height, board_width):
        self.board_height = board_height
        self.board_height = board_height
        self.board_width = board_width
        self.memo = {}

    # OPTIMIERUNGEN, DIE VORGENOMMEN WERDEN MÜSSEN:
                    # ES KANN NICHT DER GANZE BAUM BERECHNET WERDEN, DESHALB MIT MEMOIZATION ARBEITEN
    # NUR BIS Z.B. TIEFE 5 BERECHNEN, NICHT DEN KOMPLETTEN BAUM
        # (--> ÜBER TIEFE 5 (WENN ES NOCH KEIN KLARES ERGEBNIS GIBT) EINFACH 0 (DRAW) ZURÜCKGEBEN) --> GEHT BISHER EIGENTLICH
    # PROBLEM AKTUELL: FALSCHE ERGEBNISSE WERDEN ZURÜCKGEGEBEN
    # --> MÖGLICHKEIT ZUR LÖSUNG: INPUT MIT BOARD MIT 3 GLEICHEN CHIPS IN EINER REIHE --> DANN "DENKPROZESS" BEOBACHTEN
    def computer_move(self, board, player1, nfrs):  # nfrs = next free rows
        max_winner = 0
        col_if_draw = 0
        # first loop has to be separate and can't be in the recursion, because we need to store some extra data
        for col in nfrs:
            if nfrs[col] > -1:  # if row is not full, insert a chip
                board[nfrs[col]][col] = 1 if player1 else 2  # enter "1" for player 1, "2" for player 2
                nfrs[col] -= 1

                winner = check_for_winner(self.board_height, self.board_width, board, nfrs)
                if (winner == -1 and player1) or (winner == 1 and not player1): # if the computer has already won with that move
                    nfrs[col] += 1
                    board[nfrs[col]][col] = 0  # reset move
                    return col

                winner_for_path = self.evaluate_board(board, not player1, nfrs)

                nfrs[col] += 1
                board[nfrs[col]][col] = 0   # reset move

                if col_if_draw == -1 and winner_for_path == 0: # there is apparently at least one path which ends in a draw --> save path
                    col_if_draw = col
                if player1:
                    if min(winner_for_path, max_winner) == -1:  # we found a configuration where player1 has won
                        return col
                else:
                    if max(winner_for_path, max_winner) == 1:  # we found a configuration where player2 has won
                        return col
        return col_if_draw    # draw


    def evaluate_board(self, board, player1, nfrs):     # player1 wants to get min, player2 wants to get max
        result_if_not_won = 1 if player1 else -1     # result is set to "loosing" first, if a draw is found, then it's set to draw
        for col in nfrs:
            # try to insert a chip in every row that is not already full
            if nfrs[col] > -1:  # if row is not full
                board[nfrs[col]][col] = 1 if player1 else 2  # enter "1" for player 1, "2" for player 2
                nfrs[col] -= 1

                if str(board) in self.memo:
                    return self.memo[str(board)]

                if (winner := check_for_winner(self.board_height, self.board_width, board, nfrs)) != 0:
                    nfrs[col] += 1
                    board[nfrs[col]][col] = 0  # reset move

                    if player1 and winner == -1:
                        return -1   # no need to keep evaluating
                    elif not player1 and winner == 1:
                        return 1
                    else:
                        continue # if someone won, don't place more chips in this configuration, try another chip
                else:
                    winner_for_path = self.evaluate_board(board, not player1, nfrs)
                    self.memo[str(board)] = winner_for_path # insert the result for the path into the dict

                    nfrs[col] += 1
                    board[nfrs[col]][col] = 0  # reset move

                    if player1 and winner_for_path == -1:
                            return -1   # no need to keep evaluating
                    elif not player1 and winner_for_path == 1:
                            return 1
                    elif winner_for_path == 0:
                        result_if_not_won = 0
        # when no column has empty spaces, winner_for_path is just "0"(draw) and that is returned
        return result_if_not_won





if __name__ == "__main__":   # only executed when run as a script
    pass
