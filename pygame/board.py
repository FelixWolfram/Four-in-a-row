from pygame import image, transform
from help import Info


class Board:
    def __init__(self, header_size):
        self.image = image.load("assets/images/board.png")
        self.header_size = header_size
        self.scale_size = (Info.WIN_HEIGHT - self.header_size) / self.image.get_height()
        self.image = transform.smoothscale(self.image, (self.image.get_width() * self.scale_size, self.image.get_height() * self.scale_size))
        self.rect = self.image.get_rect()


    def draw(self, win):
        win.blit(self.image, self.rect )