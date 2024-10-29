import arcade

from config import SCREEN_WIDTH, SCREEN_HEIGHT, SQUARE_SIZE, ROWS, COLS
from piece import Piece

from rich import print


class Board:

    def __init__(self):
        self.board = [[0 for _ in range(ROWS)] for _ in range(ROWS)]
        self.red_pieces = self.white_pieces = 12
        self.all_pieces = []
        self.death_pieces = []
        self.has_kill_moves = False
        self.all_moves = []
        self.current_turn = "W"

        self.create_board()

    def change_turn(self):
        if self.current_turn == "W":
            self.current_turn = "R"
        else:
            self.current_turn = "W"

    def draw_squares(self):
        for row in range(ROWS):
            for col in range(row % 2, COLS, 2):
                arcade.draw_rectangle_filled(
                    col * SQUARE_SIZE + SQUARE_SIZE / 2,
                    row * SQUARE_SIZE + SQUARE_SIZE / 2,
                    SQUARE_SIZE,
                    SQUARE_SIZE,
                    arcade.color.RED,
                )

    def create_board(self):
        for row in range(ROWS):
            for col in range((row - 1) % 2, COLS, 2):
                if row < 3:
                    self.board[row][col] = self.new_piece(
                        row, col, arcade.color.RED, symbol="R"
                    )
                elif row > 4:
                    self.board[row][col] = self.new_piece(
                        row, col, arcade.color.WHITE, symbol="W"
                    )
            # print(self.board[row])

    def get_piece(self, row, col):
        return self.board[row][col]

    def get_row_col_from_mouse(self, mouse_x, mouse_y) -> tuple:
        row = int(mouse_y // SQUARE_SIZE)
        col = int(mouse_x // SQUARE_SIZE)
        return row, col

    def new_piece(self, row, col, color, symbol):
        piece = Piece(row, col, 20, color, symbol)
        piece.center_y = row * SQUARE_SIZE + SQUARE_SIZE / 2
        piece.center_x = col * SQUARE_SIZE + SQUARE_SIZE / 2
        self.all_pieces.append(piece)
        return piece

    def move_piece(self, piece: Piece, row, col):
        if not isinstance(piece, Piece):
            return

        if (row, col) in self.get_valid_moves(piece):
            if not self.has_kill_moves:
                temp = self.board[row][col]
                self.board[row][col] = self.board[piece.row][piece.col]
                self.board[piece.row][piece.col] = temp
                piece.move(row, col)
            else:
                temp = self.board[row][col]
                self.board[row][col] = self.board[piece.row][piece.col]
                self.board[piece.row][piece.col] = temp

                row_center = int((row + piece.row) // 2)
                col_center = int((col + piece.col) // 2)
                enemy = self.board[row_center][col_center]
                self.death_pieces.append(enemy)
                # self.board[row_center][col_center].kill()
                self.board[row_center][col_center] = 0
                piece.move(row, col)
                self.has_kill_moves = False

            self.change_turn()

        for row in self.board:
            print(row)

    def get_valid_moves(self, piece: Piece):
        if not isinstance(piece, Piece):
            return []

        valid_moves = []
        kill_moves = []
        # self.has_kill_moves = False

        for dir in piece.dir:
            # pulo simples
            ## right
            if piece.col < 7 and (0 <= piece.row + dir <= 7):
                if self.board[piece.row + dir][piece.col + 1] == 0:
                    valid_moves.append((piece.row + dir, piece.col + 1))
            ## left
            if piece.col > 0 and (0 <= piece.row + dir <= 7):
                if self.board[piece.row + dir][piece.col - 1] == 0:
                    valid_moves.append((piece.row + dir, piece.col - 1))

            # pulo matador
            ## right
            if piece.col < 6 and (1 <= piece.row + dir <= 6):
                enemy_1 = self.board[piece.row + dir][piece.col + 1]
                if (
                    isinstance(enemy_1, Piece)
                    and enemy_1.symbol != piece.symbol
                    and self.board[piece.row + 2 * dir][piece.col + 2] == 0
                ):
                    kill_moves.append((piece.row + 2 * dir, piece.col + 2))
                    self.has_kill_moves = True
            ## left
            if piece.col > 1 and (1 <= piece.row + dir <= 6):
                enemy_2 = self.board[piece.row + dir][piece.col - 1]
                if (
                    isinstance(enemy_2, Piece)
                    and enemy_2.symbol != piece.symbol
                    and self.board[piece.row + 2 * dir][piece.col - 2] == 0
                ):
                    kill_moves.append((piece.row + 2 * dir, piece.col - 2))
                    self.has_kill_moves = True

        return kill_moves if kill_moves else valid_moves

    def get_all_moves(self):
        self.has_kill_moves = False
        self.all_moves = []

        for piece in self.all_pieces:
            if piece.symbol == self.current_turn:
                self.all_moves.extend(self.get_valid_moves(piece))
        return list(set(self.all_moves))

    def draw_guides(self, piece: Piece):
        if piece.symbol == self.current_turn and piece.is_selected:
            for move in self.get_valid_moves(piece):
                row, col = move
                arcade.draw_circle_filled(
                    col * SQUARE_SIZE + SQUARE_SIZE / 2,
                    row * SQUARE_SIZE + SQUARE_SIZE / 2,
                    10,
                    arcade.color.BLUE,
                )
