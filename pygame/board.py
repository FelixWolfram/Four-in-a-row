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
        # Überprüfen auf Unentschieden
        if all(row == -1 for row in next_free_row):
            return 3  # draw

        # check for row, columns and diagonals
        for r in range(len(board)):
            for c in range(len(board[0])):
                if board[r][c] != 0:  # only check fields that are not empty
                    # horizontal
                    if c <= len(board[0]) - 4 and all(board[r][c] == board[r][c + i] for i in range(4)):
                        return -1 if board[r][c] == 1 else 1

                    # vertical
                    if r <= len(board) - 4 and all(board[r][c] == board[r + i][c] for i in range(4)):
                        return -1 if board[r][c] == 1 else 1

                    # diagonal from top left to bottom right
                    if r <= len(board) - 4 and c <= len(board[0]) - 4 and all(board[r][c] == board[r + i][c + i] for i in range(4)):
                        return -1 if board[r][c] == 1 else 1

                    # diagonal from top right to bottom left
                    if r >= 3 and c <= len(board[0]) - 4 and all(board[r][c] == board[r - i][c + i] for i in range(4)):
                        return -1 if board[r][c] == 1 else 1

        return 0  # Kein Gewinner


    def draw(self, win):
        win.blit(self.board_img, (0, self.header_size))