WHITE = 1
BLACK = 2
actual_color = WHITE


class Pawn:
    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color

        self.char = "P"

        if self.color == WHITE:
            self.direction = 1
            self.start_row = 1
        else:
            self.direction = -1
            self.start_row = 6

    def set_position(self, row, col):
        self.row = row
        self.col = col

    def can_move(self, row, col, f, b_a_l, w_a_l):
        if (self.row + self.direction == row) or \
                (self.row == self.start_row and self.row + 2 * self.direction == row):
            if 0 <= col <= 7 and 0 <= row <= 7:
                if f[row][col] and col != self.col:
                    return True
                elif not f[row][col] and col == self.col:
                    return True
        return False

    def can_eat(self, row, col, f):
        if 0 <= col <= 7 and 0 <= row <= 7:
            if row == self.row + self.direction and (col == self.col - 1 or col == self.col + 1):
                return True
        return False



class Knight(Pawn):
    def __init__(self, row, col, color):
        super().__init__(row, col, color)
        self.char = "N"

    def can_move(self, row, col, f, b_a_l, w_a_l):
        a = abs(row - self.row)
        b = abs(col - self.col)
        if ((a == 1 and b == 2) or (b == 1 and a == 2)) and \
                0 <= col <= 7 and 0 <= row <= 7:
            return True
        return False


class Queen(Pawn):
    def __init__(self, row, col, color):
        super().__init__(row, col, color)
        self.char = "Q"

    def can_move(self, row, col, f, b_a_l, w_a_l):
        a = abs(row - self.row)
        b = abs(col - self.col)
        if self.char == "Q" or self.char == "B":
            if a == b:
                if 0 <= col <= 7 and 0 <= row <= 7:
                    x = []
                    if row > self.row:
                        for i in range(row - 1, self.row, -1):
                            x.append([i, 0])
                    elif self.row > row:
                        for i in range(row + 1, self.row, 1):
                            x.append([i, 0])

                    if col > self.col:
                        k = 0
                        for j in range(col - 1, self.col, -1):
                            x[k][1] = j
                            k += 1
                    elif col < self.col:

                        k = 0
                        for j in range(col + 1, self.col, 1):
                            x[k][1] = j
                            k += 1
                    for el in x:
                        if f[el[0]][el[1]]:
                            return False
                    if row >= 0 and col >= 0:
                        if row < 8 and col < 8:
                            return True
                ##return False
        if self.char == "Q" or self.char == "R":
            if a == 0 and b != 0:
                if 0 <= col <= 7 and 0 <= row <= 7:
                    if col > self.col:
                        for i in range(col - 1, self.col, -1):
                            if f[row][i]:
                                return False
                    if col < self.col:
                        for i in range(col + 1, self.col, 1):
                            if f[row][i]:
                                return False
                    return True

            if b == 0 and a != 0:
                if 0 <= col <= 7 and 0 <= row <= 7:
                    if row > self.row:
                        for i in range(row - 1, self.row, -1):
                            if f[i][col]:
                                return False
                    if row < self.row:
                        for i in range(row + 1, self.row, 1):
                            if f[i][col]:
                                return False
                    return True
        return False


class Bishop(Queen):
    def __init__(self, row, col, color):
        super().__init__(row, col, color)
        self.char = "B"


class Rook(Queen):
    def __init__(self, row, col, color):
        super().__init__(row, col, color)
        self.char = "R"
        self.can_do_rook_step = True


class King(Pawn):
    def __init__(self, row, col, color):
        super().__init__(row, col, color)
        self.char = "K"
        self.can_do_rook_step = True

    def can_move(self, row, col, f, b_a_l, w_a_l):
        if not ((self.color == WHITE and ([self.row, self.col] in b_a_l or [row, col] in b_a_l)) or (self.color == BLACK and ([self.row, self.col] in w_a_l or [row, col] in w_a_l))):
            a = abs(row - self.row)
            b = abs(col - self.col)
            if (a <= 1 and b <= 1 and (0 <= col <= 7 and 0 <= row <= 7)) or (a == 0 and b == 2 and self.can_do_rook_step):
                return True
        return False


class Board:
    def __init__(self):
        self.field = []
        self.black_eaten = []
        self.white_eaten = []

        self.black_atack_list = []
        self.white_atack_list = []

        for row in range(8):
            self.field.append([None] * 8)
        # пешки
        for i in range(8):
            self.field[1][i] = Pawn(1, i, WHITE)
            self.field[6][i] = Pawn(6, i, BLACK)
        # ладьи
        self.field[7][0] = Rook(7, 0, BLACK)
        self.field[7][7] = Rook(7, 7, BLACK)
        self.field[0][0] = Rook(0, 0, WHITE)
        self.field[0][7] = Rook(0, 7, WHITE)
        # слоны
        self.field[7][2] = Bishop(7, 2, BLACK)
        self.field[7][5] = Bishop(7, 5, BLACK)
        self.field[0][2] = Bishop(0, 2, WHITE)
        self.field[0][5] = Bishop(0, 5, WHITE)
        # кони
        self.field[7][1] = Knight(7, 1, BLACK)
        self.field[7][6] = Knight(7, 6, BLACK)
        self.field[0][1] = Knight(0, 1, WHITE)
        self.field[0][6] = Knight(0, 6, WHITE)
        # ферзи
        self.field[7][3] = Queen(7, 3, BLACK)
        self.field[0][3] = Queen(0, 3, WHITE)
        # короли
        self.field[7][4] = King(7, 4, BLACK)
        self.field[0][4] = King(0, 4, WHITE)

    def current_player_color(self):
        return self.color

    def cell(self, row, col):
        piece = self.field[row][col]
        if piece is None:
            return '  '
        color = piece.color
        c = 'w' if color == WHITE else 'b'
        return c + piece.char

    def move_piece(self, row, col, row1, col1):
        if not (0 <= row <= 7 and 0 <= col <= 7) or not (0 <= row1 <= 7 and 0 <= col1 <= 7):
            return False
        if row == row1 and col == col1:
            return False
        piece = self.field[row][col]
        if piece.color != actual_color:
            return False
        if not piece:
            return False
        if not self.field[row][col].can_move(row1, col1, self.field, self.black_atack_list, self.white_atack_list):
            return False
        if self.field[row][col].can_move(row1, col1, self.field, self.black_atack_list, self.white_atack_list):
            if self.field[row1][col1]:
                if self.field[row1][col1].color == actual_color:
                    return False
        if self.field[row1][col1]:
            if self.field[row1][col1].color != actual_color:
                if actual_color == WHITE:
                    self.black_eaten.append(self.field[row1][col1].__class__.__name__)
                else:
                    self.white_eaten.append(self.field[row1][col1].__class__.__name__)

        """Странный код рокировки, который очень плохо написан, но должен работать"""
        if piece.char == "K":
            if piece.can_do_rook_step:
                if col1 == 6:
                    if self.field[row][7].char == "R" and self.field[row][7].can_do_rook_step and self.field[row][5] == None and self.field[row][6] == None:
                        if piece.color == WHITE and not [0, 5] in self.black_atack_list and not [0, 6] in self.black_atack_list:
                            self.field[row][7].set_position(0, 5)
                            self.field[row][5] = self.field[row][7]
                            self.field[row][7] = None
                        elif piece.color == BLACK and not [7, 5] in self.white_atack_list and not [7, 6] in self.white_atack_list:
                            self.field[row][7].set_position(7, 5)
                            self.field[row][5] = self.field[row][7]
                            self.field[row][7] = None
                        else:
                            return False
                    else:
                        return False
                if col == 2:
                    if self.field[row][0].char == "R" and self.field[row][0].can_do_rook_step and self.field[row][3] == None and self.field[row][2] == None and self.field[row][1] == None:
                        if piece.color == WHITE and not [0, 3] in self.black_atack_list and not [0, 2] in self.black_atack_list and not [0, 1] in self.black_atack_list:
                            self.field[row][0].set_position(0, 3)
                            self.field[row][3] = self.field[row][0]
                            self.field[row][0] = None
                        elif self.color == BLACK and not [7, 3] in self.white_atack_list and not [7, 2] in self.white_atack_list and not [7, 1] in self.white_atack_list:
                            self.field[row][0].set_position(7, 3)
                            self.field[row][3] = self.field[row][0]
                            self.field[row][0] = None
                        else:
                            return False
                    else:
                        return False

        self.field[row][col] = None
        self.field[row1][col1] = piece
        self.field[row1][col1].set_position(row1, col1)

        if self.field[row1][col1].char == "K" or self.field[row1][col1].char == "R":
            self.field[row1][col1].can_do_rook_step = False
        return True


def opponent(color):
    if color == WHITE:
        return BLACK
    return WHITE


def print_board(board):  # Распечатать доску в текстовом виде (см. скриншот)
    out_string = ""
    out_string += '     +----+----+----+----+----+----+----+----+\n'
    for row in range(7, -1, -1):
        out_string += f" {row}   "
        for col in range(8):
            out_string += f"| {board.cell(row, col)} "
        out_string += "|\n"
        out_string += '     +----+----+----+----+----+----+----+----+\n'
    out_string += "        "
    for col in range(8):
        out_string += f'{col}    '
    print(out_string)


def chess_action():  #
    global actual_color
    # Создаём шахматную доску
    board = Board()
    # Цикл ввода команд игроков
    game_stoped = False
    while not game_stoped:
        # Выводим положение фигур на доске
        print_board(board)
        """Механика битых болей была введена для ограничения возможностей короля и упрощения постановки мата"""
        # Мы перебираем все клетки существующего перед ходом поля
        board.white_atack_list = []
        board.black_atack_list = []
        for i in range(8):
            for j in range(8):
                # И рассматриваем их, если они представляют собой фигуры
                point = board.field[i][j]
                if point:
                    # После чего записываем в соответсттвующие списки все битые поля
                    if point.color == WHITE:
                        for i1 in range(8):
                            for j1 in range(8):
                                # При помощи метода can_move или can_eat
                                if point.char == "P":
                                    if point.can_eat(i1, j1, board.field) and [i1, j1] not in board.white_atack_list:
                                        board.white_atack_list.append([i1, j1])
                                else:
                                    if point.can_move(i1, j1, board.field, board.black_atack_list, board.white_atack_list) and [i1, j1] not in board.white_atack_list:
                                        board.white_atack_list.append([i1, j1])
                    elif point.color == BLACK:
                        for i1 in range(8):
                            for j1 in range(8):
                                if point.char == "P":
                                    if point.can_eat(i1, j1, board.field) and [i1, j1] not in board.black_atack_list:
                                        board.black_atack_list.append([i1, j1])
                                else:
                                    if point.can_move(i1, j1, board.field, board.black_atack_list, board.white_atack_list) and [i1, j1] not in board.black_atack_list:
                                        board.black_atack_list.append([i1, j1])

        print(board.white_atack_list)
        print(board.black_atack_list)

        # Подсказка по командам
        print('Команды:')
        print('    exit                               -- выход')
        print('    move <row> <col> <row1> <col1>     -- ход из клетки (row, col)')
        print('                                          в клетку (row1, col1)')
        # Выводим приглашение игроку нужного цвета
        if actual_color == WHITE:
            print('Ход белых:')
        else:
            print('Ход черных:')
        command = input()
        if command == 'exit':
            break
        move_type, row, col, row1, col1 = command.split()
        row, col, row1, col1 = int(row), int(col), int(row1), int(col1)

        if board.move_piece(row, col, row1, col1):
            print('Ход успешен')
            print(f"Потери белых: {board.white_eaten}")
            print(f"Потери чёрных: {board.black_eaten}")
            actual_color = opponent(actual_color)
        else:
            print('Координаты некорректы! Попробуйте другой ход!')


chess_action()
