import pygame
from board import Board
from help import Info


class Game:
    def __init__(self):
        self.win = pygame.display.set_mode((Info.WIN_WIDTH, Info.WIN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.colors = {
            "bg" : (36, 36, 36),
            "board" : (82, 125, 243),
            "text" : (182, 204, 254),
            "chip1" : (255, 255, 0),
            "chip2" : (255, 0, 0)
        }
        self.header_size = 80
        self.board = Board(self.header_size)


    def mainloop(self):
        run = True
        while run:
            self.clock.tick(Info.FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    return

            self.redraw_window()


    def redraw_window(self):
        self.win.fill(self.colors["bg"])
        pygame.draw.rect(self.win, (255, 0, 0), (100, 100, 50, 50))
        self.board.draw(self.win)

        pygame.display.update()



pygame.init()
pygame.display.set_caption("4 in a row")

game = Game()
game.mainloop()