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

    def can_move(self, row, col, f):
        if (self.row + self.direction == row) or \
                (self.row == self.start_row and self.row + 2 * self.direction == row):
            if 0 <= col <= 7 and 0 <= row <= 7 and row > self.row:
                if f[row][col] and col != self.col:
                    return True
                elif not f[row][col] and col == self.col:
                    return True
        return False


class Knight(Pawn):
    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color
        self.char = "N"

    def can_move(self, row, col, f):
        a = abs(row - self.row)
        b = abs(col - self.col)
        if ((a == 1 and b == 2) or (b == 1 and a == 2)) and \
                0 <= col <= 7 and 0 <= row <= 7 and row > self.row:
            return True
        return False


class Queen(Pawn):
    def __init__(self, row, col, color):
        super().__init__(row, col, color)
        self.char = "Q"

    def can_move(self, row, col, f):
        a = abs(row - self.row)
        b = abs(col - self.col)
        if a == b:
            if 0 <= col <= 7 and 0 <= row <= 7 and row > self.row:
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
            return False

        if a == 0 and b != 0:
            if 0 <= col <= 7 and 0 <= row <= 7 and row > self.row:
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
            if 0 <= col <= 7 and 0 <= row <= 7 and row > self.row:
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


class King(Pawn):
    def __init__(self, row, col, color):
        super().__init__(row, col, color)
        self.char = "K"

    def can_move(self, row, col, f):
        a = abs(row - self.row)
        b = abs(col - self.col)
        if a <= 1 and b <= 1 and \
                (0 <= col <= 7 and 0 <= row <= 7 and row > self.row):
            return True
        return False


class Board:
    def __init__(self):
        self.field = []
        self.black_eaten = []
        self.white_eaten = []
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
        if not self.field[row][col].can_move(row1, col1, self.field):
            return False
        if self.field[row][col].can_move(row1, col1, self.field):
            if self.field[row1][col1]:
                if self.field[row1][col1].color == actual_color:
                    return False
        if self.field[row1][col1]:
            if self.field[row1][col1].color != actual_color:
                if actual_color == WHITE:
                    self.black_eaten.append(self.field[row1][col1].__class__.__name__)
                else:
                    self.white_eaten.append(self.field[row1][col1].__class__.__name__)
        self.field[row][col] = None
        self.field[row1][col1] = piece
        piece.set_position(row1, col1)
        return True

    def is_under_attack(self, row, col, color):
        solutin_list = []
        for elem in self.field:
            for el in elem:
                if el:
                    if el.color() == color:
                        solutin_list.append(el.can_move(row, col))
        if any(solutin_list):
            return True
        return False


def opponent(color):
    if color == WHITE:
        return BLACK
    return WHITE


def print_board(board):  # Распечатать доску в текстовом виде (см. скриншот)
    print('     +----+----+----+----+----+----+----+----+')
    for row in range(7, -1, -1):
        print(' ', row, end='  ')
        for col in range(8):
            print('|', board.cell(row, col), end=' ')
        print('|')
        print('     +----+----+----+----+----+----+----+----+')
    print(end='        ')
    for col in range(8):
        print(col, end='    ')
    print()


def main():
    global actual_color
    # Создаём шахматную доску
    board = Board()
    # Цикл ввода команд игроков
    game_stoped = False
    while not game_stoped:
        # Выводим положение фигур на доске
        print_board(board)
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


main()
