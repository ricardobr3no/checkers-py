import arcade

from config import SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, SQUARE_SIZE
from board import Board
from piece import Piece
from menu import Menu


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


def draw_ui():
    restart_button = arcade.gui.UIFlatButton(
        text="RESTART",
        font_size=32,
        width=100,
        height=50,
    )
    quit_button = arcade.gui.UIFlatButton(
        text="QUIT",
        font_size=32,
        width=100,
        height=50,
    )
    buttons_widget = arcade.gui.UIBoxLayout(
        x=0,
        y=0,
        children=[restart_button, arcade.gui.UISpace(height=20), quit_button],
    )
    vertical_box = arcade.gui.UIBoxLayout(
        x=SCREEN_HEIGHT + 100,
        y=300,
        children=[buttons_widget],
    )
    vertical_box.add(buttons_widget)

    @restart_button.event("on_click")
    def on_click_restart(event):
        print("restart")

    @quit_button.event("on_click")
    def on_click_quit(event):
        print("saindo...")
        arcade.close_window()

    return vertical_box


class MyGame(arcade.Window):

    def __init__(self, width, height, title):
        super().__init__(width, height, title, center_window=True)

        arcade.set_background_color(arcade.color.AMAZON)

        self.selection = True
        self.selected_piece = None
        self.setup()

    def setup(self):
        """Set up the game variables. Call to re-start the game."""
        # Create your sprites and sprite lists here
        self.board = Board()
        self.menu = Menu()

        self.selection = True
        self.selected_piece = None

    def on_draw(self):
        arcade.start_render()
        self.clear()

        self.menu.on_draw()
        self.board.draw_squares()

        # desenhar as pieces
        for piece in self.board.all_pieces:
            if piece in self.board.death_pieces:
                piece.kill()
                continue
            piece.draw()
            show_crown(piece) if piece.is_king else hide_crown(piece)

        # desenhar as guias
        if not self.selection:
            self.board.draw_guides(self.selected_piece)

    def on_mouse_release(self, x, y, button, modifiers):
        row, col = self.board.get_row_col_from_mouse(x, y)

        if col not in range(8):
            return

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

                # print("==+==+==+==+==+==+==+==+==+==+==+==+==")
                # print(f"selected_piece:  {self.selected_piece}")
                # print("dir: ", self.selected_piece.dir)
                # print(f"selection: {self.selection}")
                # print("valid moves: ", self.board.get_valid_moves(self.selected_piece))

        elif isinstance(self.selected_piece, Piece):
            self.board.move_piece(self.selected_piece, row, col)
            # if not self.board.has_kill_moves:
            self.selection = True
            self.selected_piece.is_selected = False
            self.selected_piece = None

        # verifica fim de jogo
        print("total de peças: ", self.board.total_pieces)
        self.menu.update_score(self.board.total_pieces)

        # verifica botao restart

    def on_mouse_motion(self, x, y, dx, dy):
        for piece in self.board.all_pieces:
            piece.change_size((x, y), self.board.current_turn)


game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
game.setup()
game.run()
