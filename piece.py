import arcade
from config import SQUARE_SIZE


class Piece(arcade.sprite.SpriteCircle):
    def __init__(self, row, col, radius, color, symbol: str):
        super().__init__(radius=radius, color=color)
        self.symbol = symbol
        self.row = row
        self.col = col
        self.is_selected = False
        self.is_king = False
        self.dir = [1] if self.symbol == "R" else [-1]

    def move(self, row, col):
        self.row = row
        self.col = col
        self.center_y = row * SQUARE_SIZE + SQUARE_SIZE / 2
        self.center_x = col * SQUARE_SIZE + SQUARE_SIZE / 2
        self.is_selected = False

        if self.row in (0, 7):
            self.is_king = True
            print("promovido")
            self.dir = [1, -1]

        self.is_selected = False

    def change_size(self, mouse_pos: tuple):
        if self.is_selected:
            return

        if self.collides_with_point(mouse_pos):
            self.scale = 1.1
        else:
            self.scale = 1

    def __repr__(self):
        return self.symbol
