from pygame import draw, font, Rect, Surface, SRCALPHA
from help import Info


class StartGui:
    def __init__(self):
        self.header_rect, self.pvp_rect, self.pvc_rect, self.start_surf = self.create_start_gui()
        self.pvp_hover = False
        self.pvc_hover = False


    def create_start_gui(self):
        start_font = font.SysFont("verdana", 80)
        pvp_pvc_font = font.SysFont("verdana", 110)

        surf = Surface((Info.WIN_WIDTH, Info.WIN_HEIGHT), SRCALPHA)
        surf.fill((0, 0, 0, 0))
        header_rect = Rect(0, 0, Info.WIN_WIDTH / 1.5, Info.WIN_HEIGHT / 6)
        pvp_rect = Rect(0, 0, Info.WIN_WIDTH / 3.15, Info.WIN_HEIGHT / 2.3)
        pvc_rect = Rect(0, 0, Info.WIN_WIDTH / 3.15, Info.WIN_HEIGHT / 2.3)
        header_rect.center = (surf.get_rect().center[0], surf.get_rect().center[1] - Info.WIN_HEIGHT / 4)
        pvp_rect.center = (surf.get_rect().center[0] - pvp_rect.width * 0.55, surf.get_rect().center[1] + Info.WIN_HEIGHT / 11)
        pvc_rect.center = (surf.get_rect().center[0] + pvc_rect.width * 0.55, surf.get_rect().center[1] + Info.WIN_HEIGHT / 11)

        header_txt = start_font.render("4 in a row", True, Info.colors["text"])
        pvp_txt = pvp_pvc_font.render("PvP", True, Info.colors["text"])
        pvc_txt = pvp_pvc_font.render("PvC", True, Info.colors["text"])
        header_txt_rect = header_txt.get_rect(center = header_rect.center)
        pvp_txt_rect = pvp_txt.get_rect(center = pvp_rect.center)
        pvc_txt_rect = pvc_txt.get_rect(center = pvc_rect.center)
        surf.blit(header_txt, header_txt_rect)
        surf.blit(pvp_txt, pvp_txt_rect)
        surf.blit(pvc_txt, pvc_txt_rect)
        return header_rect, pvp_rect, pvc_rect, surf
    

    def draw(self, win):
        win.fill(Info.colors["gui"])
        draw.rect(win, Info.colors["header"], self.header_rect, border_radius=40)
        draw.rect(win, Info.colors["hover" if self.pvc_hover else "board"], self.pvc_rect, border_radius=40)
        draw.rect(win, Info.colors["hover" if self.pvp_hover else "board"], self.pvp_rect, border_radius=40)
        win.blit(self.start_surf, (0, 0))