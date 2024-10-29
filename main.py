import arcade

from config import SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, SQUARE_SIZE
from board import Board
from piece import Piece


class MyGame(arcade.Window):

    def __init__(self, width, height, title):
        super().__init__(width, height, title, center_window=True)

        arcade.set_background_color(arcade.color.BLACK)

        # If you have sprite lists, you should create them here,
        # and set them to None
        self.selection = True
        self.selected_piece = None

    def setup(self):
        """Set up the game variables. Call to re-start the game."""
        # Create your sprites and sprite lists here
        self.board = Board()

        # print(self.board.get_piece(0, 0))

    def on_draw(self):
        # This command should happen before we start drawing. It will clear
        # the screen to the background color, and erase what we drew last frame.
        # Call draw() on all your sprite lists below
        self.clear()
        self.board.draw_squares()

        # tirar pieces
        for piece in self.board.death_pieces:
            if isinstance(piece, Piece):
                piece.kill()
                self.board.death_pieces.remove(piece)

        for piece in self.board.all_pieces:
            piece.draw()

            if piece.is_king:
                arcade.draw_rectangle_filled(
                    center_x=piece.col * SQUARE_SIZE + SQUARE_SIZE / 2,
                    center_y=piece.row * SQUARE_SIZE + SQUARE_SIZE / 2,
                    width=20,
                    height=10,
                    color=arcade.color.GOLD,
                )

        if not self.selection:
            self.board.draw_guides(self.selected_piece)

    def on_mouse_release(self, x, y, button, modifiers):
        row, col = self.board.get_row_col_from_mouse(x, y)

        if self.selection:
            p_aux = self.board.get_piece(row, col)
            if (
                isinstance(p_aux, Piece)
                and self.board.get_valid_moves(p_aux)
                and p_aux.symbol == self.board.current_turn
            ):
                self.selection = False
                p_aux.is_selected = True
                self.selected_piece = p_aux

                print("==+==+==+==+==+==+==+==+==+==+==+==+==")
                print(f"selected_piece:  {self.selected_piece}")
                print("dir: ", self.selected_piece.dir)
                print(f"selection: {self.selection}")
                print("valid moves: ", self.board.get_valid_moves(self.selected_piece))

        elif isinstance(self.selected_piece, Piece):
            self.board.move_piece(self.selected_piece, row, col)
            # if not self.board.has_kill_moves:
            self.selection = True
            self.selected_piece.is_selected = False
            self.selected_piece = None

    def on_mouse_motion(self, x, y, dx, dy):
        for piece in self.board.all_pieces:
            piece.change_size((x, y))


game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
game.setup()
game.run()
