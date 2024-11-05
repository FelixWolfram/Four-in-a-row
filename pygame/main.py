import pygame
from board import Board
from minimax_pruning import Computer
from start_gui import StartGui
from help import Info
import threading
from copy import deepcopy


class Game:
    def __init__(self):
        self.win = pygame.display.set_mode((Info.WIN_WIDTH, Info.WIN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.board = Board()
        self.computer = Computer(self.board.check_for_winner)
        self.start_gui = StartGui()

        self.player1 = True
        self.chip_pos = None
        self.chip_visible = False
        self.set_chip = False

        self.in_animation = False
        self.animation_pos = None
        self.gravity = 1.08
        self.start_acceleration = 0.3
        self.acceleration = self.start_acceleration
        self.destination_cell = None
        self.chip_hover_height = 60
        self.chip_count = 0
        self.save_move_col = None
        self.game_over = False
        self.game_start = True
        self.winner = 0

        self.end_header = None
        self.computer_is_thinking = pygame.font.SysFont("verdana", 60).render("Computer is thinking...", True, Info.colors["thinking_txt"])
        self.computer_is_thinking_rect = self.computer_is_thinking.get_rect(center = (Info.WIN_WIDTH / 2, self.board.header_size / 2))
        self.game_state = None
        self.restart_rect = None
        self.game_end = False


    def mainloop(self):
        run = True
        while run:
            self.clock.tick(Info.FPS)

            if not self.in_animation:
                if winner := self.board.check_for_winner(self.board.next_free_row, self.board.board): # -1 player1 won, 1 player2 won, 3 draw
                    self.game_over = True
                    self.winner = winner
                    self.end_header = self.create_end_gui()
            if self.save_move_col is not None and not self.in_animation:
                self.chip_pos = (self.save_move_col * self.board.cell_size + self.board.border_width + self.board.board_rect.x + self.board.cell_size / 2, self.chip_hover_height)
                self.do_move(self.save_move_col)
                self.save_move_col = None
                continue                           

            mouse_x, mouse_y = pygame.mouse.get_pos()
            self.set_chip = False  
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    self.game_end = True
                    return
                if self.game_start:     # check whether the player hovers or clicks on a button
                    self.start_gui.pvp_hover = False
                    self.start_gui.pvc_hover = False
                    if self.start_gui.pvp_rect.collidepoint(mouse_x, mouse_y):
                        self.start_gui.pvp_hover = True
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            self.game_start = False
                            self.game_state = "pvp"
                    elif self.start_gui.pvc_rect.collidepoint(mouse_x, mouse_y):
                        self.start_gui.pvc_hover = True
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            self.game_start = False
                            self.game_state = "pvc"
                elif self.game_over and self.restart_rect is not None:    # check whether the player clicks on the restart button
                    if event.type == pygame.MOUSEBUTTONDOWN and self.restart_rect.collidepoint(mouse_x, mouse_y):
                        return              # starting a new game
                else:
                    if event.type == pygame.MOUSEBUTTONDOWN and not self.in_animation and not self.game_over:
                        self.set_chip = True            # set the chip if the player clicks
            
            if not self.game_over:
                if self.board.board_rect.collidepoint(mouse_x, mouse_y) and not self.in_animation and not (not self.player1 and self.game_state == "pvc"): # animate the chip hovering over the board
                    col = int((mouse_x - self.board.board_rect.x) // (self.board.board_rect.width / Info.cols))
                    self.chip_pos = (col * self.board.cell_size + self.board.border_width + self.board.board_rect.x + self.board.cell_size / 2, self.chip_hover_height)
                    self.chip_visible = True  
                    if self.set_chip:
                        if self.do_move(col) and self.game_state == "pvc":
                            threading.Thread(target=self.calculate_computer_move).start() # start to calculate the computer move instantly when the player places the chip
                else:
                    self.chip_visible = False   # if the chip is outside the field

                if self.in_animation:   # animate the chip falling down
                    if self.animation_pos[1] < self.get_y_from_row(self.destination_cell[0]):
                        self.animation_pos[1] += self.acceleration
                        self.acceleration += max(0.42, (self.gravity - 1) * self.acceleration)
                    else:   # chip reached the destination
                        self.in_animation = False
                        self.acceleration = self.start_acceleration
                        self.animation_pos = None
                        self.destination_cell = None

            self.redraw_window()


    # setting the chip when possible and swithing the player
    def do_move(self, col): 
        if (destination_row := self.board.insert_chip(self.player1, col)) == -1: # sets the chip and returns the row where the chip was inserted
            return False
        self.chip_count += 1
        self.player1 = not self.player1
        self.in_animation = True
        self.animation_pos = [self.chip_pos[0], self.chip_hover_height]
        self.destination_cell = (destination_row, col)
        self.chip_visible = False # hide the chip while in the animation
        return True
        

    def calculate_computer_move(self):
        col = self.computer.computer_move(deepcopy(self.board.board), self.player1, self.board.next_free_row, self.chip_count)
        self.save_move_col = col    # save the move -> do not do it instantly because the player-move could be still in the animation


    # calculate the y position of a row
    def get_y_from_row(self, row):
        return self.board.board_rect.y + self.board.border_width + self.board.cell_size / 2 + row * self.board.cell_size + self.board.header_size


    # calculate the x position of a column
    def get_x_from_col(self, col):
        return self.board.board_rect.x + self.board.border_width + self.board.cell_size / 2 + col * self.board.cell_size 


    def create_end_gui(self):
        end_surf = pygame.Surface((Info.WIN_WIDTH, self.board.header_size), pygame.SRCALPHA)
        end_font = pygame.font.SysFont("verdana", 60)
        end_surf.fill((0, 0, 0, 0))
        
        header_gap = self.board.cell_size * 0.75
        winner_text = "Draw!" if self.winner == 3 else f"Player {'1' if self.winner == -1 else '2'} won!" # -1 player1 won, 1 player2 won, 3 draw
        text_color = Info.colors["draw"] if self.winner == 3 else (Info.colors["chip1"] if self.winner == -1 else Info.colors["chip2"])
        end_txt = end_font.render(winner_text, 1, text_color)
        end_txt_rect = end_txt.get_rect(center = end_surf.get_rect().center)
        restart_img = pygame.image.load("assets/images/restart1.png")
        restart_img = pygame.transform.smoothscale(restart_img, (end_txt_rect.height, end_txt_rect.height))
        end_surf.blit(end_txt, end_txt_rect)
        self.restart_rect = pygame.Rect(end_txt_rect.right + header_gap, end_txt_rect.y, *restart_img.get_rect().size)
        end_surf.blit(restart_img, (end_txt_rect.right + header_gap, end_txt_rect.y))
        return end_surf


    def draw_chips(self):
        for row in range(Info.rows):
            for col in range(Info.cols):
                if (row, col) == self.destination_cell:
                    pygame.draw.circle(self.win, Info.colors["chip1" if self.board.board[row][col] == 1 else "chip2"], (self.animation_pos[0], self.animation_pos[1]), self.board.radius)
                elif self.board.board[row][col] != 0:
                    x = self.get_x_from_col(col)
                    y = self.get_y_from_row(row)
                    pygame.draw.circle(self.win, Info.colors["chip1" if self.board.board[row][col] == 1 else "chip2"], (x, y), self.board.radius) 


    def redraw_window(self):
        self.win.fill(Info.colors["bg"])
        if self.game_start:
            self.start_gui.draw(self.win)
        else:
            if self.chip_visible and not self.game_over and not self.game_start: 
                pygame.draw.circle(self.win, Info.colors["chip1" if self.player1 else "chip2"], self.chip_pos, self.board.radius)
            if (not self.player1 and self.game_state == "pvc") and not self.chip_visible and not self.in_animation:
                self.win.blit(self.computer_is_thinking, self.computer_is_thinking_rect)
            self.draw_chips()
            self.board.draw(self.win)
            if self.game_over:
                self.win.blit(self.end_header, (0, 0))

        pygame.display.update()


pygame.init()
pygame.display.set_caption("4 in a row")

game_end = False
while not game_end:
    game = Game()
    game.mainloop()
    if game.game_end:
        break
