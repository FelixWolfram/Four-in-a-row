import copy

from customtkinter import *     # like this you don't have to put customtkinter. in front of all the classes and methods
from check_for_winner import check_for_winner
from enemy import Computer
from PIL import Image, ImageTk


class GUI:
    def __init__(self, master):
        self.colors = {
            "board_color" : "#527df3",
            "bg_color" : "#242424",
            "text_color" : "#b6ccfe",
            "chip_col1" : "yellow",
            "chip_col2" : "red"
        }

        self.master = master
        self.board_frame = None
        self.board_height = 6
        self.board_width = 7
        self.board = [[0 for _ in range(self.board_width)] for _ in range(self.board_height)]
        self.buttons = [[None for _ in range(self.board_width)] for _ in range(self.board_height)]
        self.button_border_width = 10   # variable for that, because it is used several times
        self.button_total_height = 0
        self.used_buttons = set()
        self.chip_label = None
        self.computer = Computer(self.board_height, self.board_width)
        self.next_free_row = {0 : self.board_height - 1, 1 : self.board_height - 1, 2 : self.board_height - 1, 3 : self.board_height - 1,
                              4 : self.board_height - 1, 5 : self.board_height - 1, 6 : self.board_height - 1}
                                # for every col, first set last used row to under the board
        self.player1 = True
        self.player_turn_label = None
        self.invalid_move_label = None
        self.create_GUI()
        self.print_player()


    def create_GUI(self):
        self.player_turn_label = CTkLabel(self.master, text="", font=("Helvetica", 30), text_color=self.colors["text_color"])
        self.player_turn_label.pack(pady=30)

        self.invalid_move_label = CTkLabel(self.master, text="", font=("Helvetica", 30), text_color=self.colors["text_color"])
        self.invalid_move_label.pack(pady=30)

        self.board_frame = CTkFrame(self.master, fg_color=self.colors["board_color"])
        self.board_frame.pack(pady=30)

        for r in range(self.board_height):
            for c in range(self.board_width):
                button = CTkButton(self.board_frame, text="", height=100, width=100, corner_radius=55,
                                   fg_color=self.colors["bg_color"], border_width=self.button_border_width, hover=False,
                                   border_color=self.colors["board_color"], command=lambda col = c: self.set_chip(col))
                self.button_total_height = button.cget("height")
                button.bind("<Enter>", lambda event, col = c: self.on_enter(col))
                button.bind("<Leave>", lambda event, col = c: self.on_leave(col))
                button.grid(row= r, column= c)
                self.buttons[r][c] = button


    def on_enter(self, c):
        for r in range(self.board_height):      # makes an effect, looking like the whole column colors on hovering
            if (r, c) not in self.used_buttons: # only if button is not already used
                if r == self.next_free_row[c]:
                    player_col = "chip_col1" if self.player1 else "chip_col2"
                    self.buttons[r][c].configure(fg_color=self.colors[player_col])


    def on_leave(self, c):
        for r in range(self.board_height):
            if (r, c) not in self.used_buttons:
                self.buttons[r][c].configure(fg_color=self.colors["bg_color"])


    def print_player(self):
        player = "1" if self.player1 else "2"
        self.player_turn_label.configure(text="It's Player " + player + " turn")


    def set_chip(self, col):
        self.invalid_move_label.configure(text="")
        if self.next_free_row[col] < 0:
            self.invalid_move_label.configure(text="Invalid Move, Row is full!")    # text if row is full
        else:
            if self.player1: chip_col = self.colors["chip_col1"]   # save color for the "chip"
            else: chip_col = self.colors["chip_col2"]

            # make an animation for the chip
            self.chip_label = CTkFrame(self.board_frame, height=80, width=80, fg_color=chip_col,
                                       corner_radius=55,)
            y_coord_chip = self.buttons[0][col].winfo_y() + self.button_border_width
            x_coord_chip = self.buttons[0][col].winfo_x() + self.button_border_width
            self.chip_label.place(x=x_coord_chip, y=y_coord_chip)
            # get button coordinates of the "next free button" in that row
            y_coord = self.buttons[self.next_free_row[col]][col].winfo_y() # next free row y-coord
            move_y = self.button_total_height / 40  # how much the label should move per recursion
            # disable all buttons, animate chip, then enable all buttons again
            self.disable_buttons()
            self.animate_chip(x_coord_chip, y_coord_chip, y_coord, move_y)
            # insert chip into the board
            self.board[self.next_free_row[col]][col] = 1 if self.player1 else 2 # enter "1" for player 1, "2" for player 2
            self.buttons[self.next_free_row[col]][col].configure(fg_color=chip_col) # change the button
            self.used_buttons.add((self.next_free_row[col], col))
            self.next_free_row[col] -= 1    # move the index for setting the fields up the board

            self.player1 = not self.player1   # change player
            self.print_player()
            if (winner := check_for_winner(self.board_height, self.board_width, self.board, self.next_free_row)) != 0:# one player won
                self.game_end(winner)
                return
            self.computer_move()


    def computer_move(self):
        # MAN KANN DIE KOMPLETTE METHODE STARK KÜRZEN, WENN MAN EINFACH EINE ABFRAGE, WELCHER SPIELER DRAN IST UNTEN BEIM
        # "COMPUTER_MOVE" (DAMIT NICHT IMMER DER COMPUTER AM ZUG IST) DAZUMACHT UND DANN DEN CHIP AN DIE METHODE
        # "SET_CHIP()" ÜBERGIBT --> ALLERDINGS IST DIE ANIMATION DANN VERBUGGT; WEIL EINFACH EIN CHIP IRGENDWO IN DER LUFT HÄNGT
        # --> GGF. KÖNNTE MAN DAS ÄNDERN INDEM MAN DEN CHIP KOMPLETT UNSICHTBAR MACHT, NACHDEM DIE ANIMATION FERTIG IST
        # --> DANN MÜSSTE NUR NOCH DAS PROBLEM GEFIXT WERDEN, DASS DER CHIP DIE FARBE WÄHREND DER ANIMATION ÄNDERT
            # --> AUF JEDEN FALL MAL SCHAUEN, OB PYTHON EINE "SLEEP" METHODE HAT (GIBTS AUF JEDEN FALL)
        if self.player1:
            chip_col = self.colors["chip_col1"]  # save color for the "chip"
        else:
            chip_col = self.colors["chip_col2"]


        # FUNKTIONIERT NOCH NICHT, WEIL:
        # DER COMPUTER SETZT DIE CHIPS IMMER NUR IN DIE ERSTE REIHE
        # AUCH DIE ENDANZEIGE STIMMT NOCH NICHT GANZ, DA NACH DEM 4. CHIP IN EINER REIHE DES SPIELERS DER COMPUTER
            # SOZUSAGEN AUCH NOCHMAL EIN CHIP SETZT UND ANGEZEIGT WIRD, DASS DER COMPUTER GEWONNEN HAT
        place_col = self.computer.computer_move(copy.deepcopy(self.board), self.player1, self.next_free_row.copy())
                                    # deepcopy, because with nested lists, the normal ".copy()" method only copies the outer list
        self.board[self.next_free_row[place_col]][place_col] = 1 if self.player1 else 2  # enter "1" for player 1, "2" for player 2
        self.buttons[self.next_free_row[place_col]][place_col].configure(fg_color=chip_col)  # change the button
        self.used_buttons.add((self.next_free_row[place_col], place_col))
        self.next_free_row[place_col] -= 1  # move the index for setting the fields up the board

        self.player1 = not self.player1
        self.print_player()

        if (winner := check_for_winner(self.board_height, self.board_width, self.board, self.next_free_row)) != 0:  # one player won
            self.game_end(winner)


    def animate_chip(self, x_coord_chip, y_coord_chip, y_coord, move_y):
        y_coord_chip += move_y
        if y_coord_chip <= y_coord:
            self.chip_label.place(x=x_coord_chip, y=y_coord_chip + self.button_border_width, anchor="nw")
            self.master.after(1,
                              lambda yc = y_coord_chip, xc = x_coord_chip, y = y_coord, move = move_y:
                                     self.animate_chip(xc, yc, y, move))
        else:
            self.enable_buttons()


    def disable_buttons(self):
        for r in range(self.board_height):
            for c in range(self.board_width):
                self.buttons[r][c].configure(command=None)

    def enable_buttons(self):
        for r in range(self.board_height):
            for c in range(self.board_width):
                self.buttons[r][c].configure(command=lambda col = c: self.set_chip(col))


    def game_end(self, index):
        player = "Player 1" if index == -1 else "Player 2"
        self.invalid_move_label.configure(text= player + " has won!", text_color="green")

        for r in range(self.board_height):
            for c in range(self.board_width):
                self.buttons[r][c].configure(state="disabled")
                self.buttons[r][c].unbind("<Enter>")



root = CTk()
root.title("4 Gewinnt")
root.geometry("900x900")
root._set_appearance_mode("dark")


main = GUI(root)

root.mainloop()


# TODO
# bot hinzufügen
# Schwierigkeitsanpassung für Bot hinzufügen --> mit Schiebregler
# design ändern
# UI für Restart, ...
    # für UI diesmal vielleicht anderer aufbau mit einem Container links davon
    # auch andere Buttons und Menus mal austesten
# runde Felder???
# warum auch immer das nötig wäre, aber ein passwortgeschützer Admin Mode :)
# Animationen für die "Chips" wenns geht
# Benutzer entscheiden lassen, welcher Spieler er sein will gegen den Computer (1 oder 2)
