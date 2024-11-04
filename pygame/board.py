import pygame
from help import Info


class Board:
    def __init__(self):
        self.header_size = Info.WIN_HEIGHT // 6.7
        self.border_width = Info.WIN_HEIGHT // 40
        self.radius = Info.WIN_HEIGHT // 18
        self.cell_size = None
        self.board_rect = None
        self.board_img = self.create_board_img()
        self.board = [[0 for _ in range(Info.cols)] for _ in range(Info.rows)]
        self.next_free_row = {i : Info.rows - 1 for i in range(Info.cols)}


    def create_board_img(self):
        self.cell_size = (Info.WIN_HEIGHT - self.header_size) / Info.rows - (self.border_width / Info.rows)  
        self.board_surface = pygame.Surface((Info.WIN_WIDTH, Info.WIN_HEIGHT - self.header_size), pygame.SRCALPHA)   # width and height of the surface
        self.board_surface.fill((Info.colors["bg"]))
        self.board_rect = pygame.Rect(0, 0, self.cell_size * Info.cols + 2 * self.border_width, self.cell_size * Info.rows + 2 * self.border_width)
        self.board_rect.center = self.board_surface.get_rect().center
        pygame.draw.rect(self.board_surface, Info.colors["board"], self.board_rect, border_radius=40)

        for row in range(Info.rows):
            for col in range(Info.cols):
                position = (col * self.cell_size + self.border_width + self.board_rect.x + self.cell_size / 2, row * self.cell_size + self.border_width + self.board_rect.y + self.cell_size / 2)
                pygame.draw.circle(self.board_surface, (0, 0, 0, 0), position, self.radius)  # transparent circles (RGBA: (0, 0, 0, 0))
        return self.board_surface
    

    def insert_chip(self, player1, col):
        if self.next_free_row[col] > -1:
            row = self.next_free_row[col]
            self.board[row][col] = 1 if player1 else 2
            self.next_free_row[col] -= 1
            return row
        return -1   # if the row is full, don't insert the chip
    

    def check_for_winner(self, next_free_row, board):
        draw = True
        for c in range(Info.cols):  # check for draw --> no fields left
            if next_free_row[c] > -1:  # if not all check_for_free pointers are "over" the board --> game not ended
                draw = False
                break
        if draw:
            return 3    # 3 for draw

        # check rows
        for r in range(Info.rows):
            count = [0, 0]  # first number for player1, second for player2
            for c in range(Info.cols):
                if (player_won := self.loop_over_board(r, c, count, board)) != 0:    # player_won = 0 if the first player won, 1 if the second player won
                    return player_won

        # check columns
        for c in range(Info.cols):
            count = [0, 0]
            for r in range(Info.rows):
                if (player_won := self.loop_over_board(r, c, count, board)) != 0:
                    return player_won

        # check diagonals -> there is probably a better way to do this
        for r in range(Info.rows - 3):
            count = [0, 0]
            for c in range(Info.cols):  # we don't have to check the last 3 rows/columns, because there can't be 4 chips diagonally
                if r + c < Info.rows:
                    if (player_won := self.loop_over_board(r + c, c, count, board)) != 0:
                        return player_won
        for r in range(Info.rows - 1, 2, -1):
            count = [0, 0]
            for c in range(Info.cols):
                if r - c > -1:
                    if (player_won := self.loop_over_board(r - c, c, count, board)) != 0:
                        return player_won
        for r in range(Info.cols - 3):
            count = [0, 0]
            for c in range(Info.rows):
                if r + c < Info.cols:
                    if (player_won := self.loop_over_board(c, r + c, count, board)) != 0:
                        return player_won
        for r in range(Info.cols - 1, 2, -1):
            count = [0, 0]
            for c in range(Info.rows):
                if r - c > -1:
                    if (player_won := self.loop_over_board(c, r - c, count, board)) != 0:
                        return player_won
        # two rows are still in blind spots by the four diagonal checks
        if board[5][3] == board[4][4] == board[3][5] == board[2][6] != 0:
            return -1 if board[4][4] == 1 else 1
        if board[5][2] == board[4][3] == board[3][4] == board[2][5] != 0 or \
           board[4][3] == board[3][4] == board[2][5] == board[1][6] != 0:
            return -1 if board[3][4] == 1 else 1
        return 0


    def loop_over_board(self, r, c, count, board): # incrementing the count if adjacent chips are the same
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


    def draw(self, win):
        win.blit(self.board_img, (0, self.header_size))