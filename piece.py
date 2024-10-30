import arcade
from config import SQUARE_SIZE

show_crown = lambda piece: arcade.draw_rectangle_filled(
    center_x=piece.col * SQUARE_SIZE + SQUARE_SIZE / 2,
    center_y=piece.row * SQUARE_SIZE + SQUARE_SIZE / 2,
    width=20,
    height=10,
    color=arcade.color.GOLD,
)
hide_crown = lambda piece: arcade.draw_rectangle_filled(
    center_x=piece.col * SQUARE_SIZE + SQUARE_SIZE / 2,
    center_y=piece.row * SQUARE_SIZE + SQUARE_SIZE / 2,
    width=20,
    height=10,
    color=arcade.color.RED if piece.symbol == "R" else arcade.color.WHITE,
)


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

    def change_size(self, mouse_pos: tuple, turno: str):
        if self.collides_with_point(mouse_pos) and self.symbol == turno:
            self.scale = 1.1
        else:
            self.scale = 1

    def __repr__(self):
        return self.symbol
