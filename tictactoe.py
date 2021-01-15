# библиотека pygame
import pygame

# константы
COLORS = {
    'white': (255, 255, 255),
    'blue': (0, 0, 200),
    'red': (200, 0, 0),
    'green': (0, 255, 0),
    'yellow': (255, 255, 0),
    'X_color': (84, 84, 84),
    'O_color': (255, 255, 255)
}

WIDTH, HEIGHT = (600, 600)
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))


# Класс, необходимый для проверки ходов и победителя
class Checker:
    def __init__(self):
        self.field = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
        ]
        self.player = 1
        self.winning_line = None

    # проверка ячейки на занятость
    def is_valid_move(self, i, j):
        return self.field[i][j] == 0

    # сделать ход
    def make_move(self, i, j):
        if self.is_valid_move(i, j):
            self.field[i][j] = self.player
            self.player = (self.player % 2) + 1

    # проверка поля на победителя
    def check_for_winner(self):
        for i in range(3):
            if self.field[0][i] == self.field[1][i] == self.field[2][i] != 0:
                self.winning_line = ('column', i)
                return self.field[0][i]
        for i in range(3):
            if self.field[i][0] == self.field[i][1] == self.field[i][2] != 0:
                self.winning_line = ('row', i)
                return self.field[i][0]
        if self.field[0][0] == self.field[1][1] == self.field[2][2] != 0:
            self.winning_line = ('diagonal', 1)
            return self.field[0][0]
        if self.field[0][2] == self.field[1][1] == self.field[2][0] != 0:
            self.winning_line = ('diagonal', 2)
            return self.field[0][2]
        ch = 0
        for i in range(3):
            for j in range(3):
                if self.field[i][j] == 0:
                    ch = 1
        if not ch:
            return 'tie'


# класс-игровое поле
class Field:
    # игровые ячейки
    SQUARES = [
        [(0, 0, 200, 200), (200, 0, 200, 200), (400, 0, 200, 200)],
        [(0, 200, 200, 200), (200, 200, 200, 200), (400, 200, 200, 200)],
        [(0, 400, 200, 200), (200, 400, 200, 200), (400, 400, 200, 200)],
    ]

    def __init__(self):
        self.surface = WINDOW
        self.width = WIDTH
        self.height = HEIGHT
        self.color = COLORS['white']
        self.checker = Checker()
        self.winner = None
        self.font = 'consolas'

    # рисование игрового поля
    def draw_board(self):
        WINDOW.fill((13, 161, 146))
        x, y = 0, 0
        for line in range(3):
            x += self.width // 3
            y += self.width // 3
            pygame.draw.line(self.surface, self.color, (x, 0), (x, self.width), 3)
            pygame.draw.line(self.surface, self.color, (0, y), (self.height, y), 3)

    # получение индекса игровой ячейки
    def get_square(self):
        x, y = pygame.mouse.get_pos()
        i, j = -1, -1
        if 0 < y < 200:
            i = 0
        if 200 < y < 400:
            i = 1
        if 400 < y < 600:
            i = 2
        if 0 < x < 200:
            j = 0
        if 200 < x < 400:
            j = 1
        if 400 < x < 600:
            j = 2
        if i != -1 and j != -1:
            if self.checker.is_valid_move(i, j) and self.checker.check_for_winner() is None:
                pygame.draw.rect(self.surface, (16, 204, 184), self.SQUARES[i][j])
            return self.SQUARES[i][j], (i, j)

    # написание текста в окне
    def draw_text(self, text, size, color, x, y):
        font = pygame.font.Font(pygame.font.match_font(self.font, 1), size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        self.surface.blit(text_surface, text_rect)

    # вывод поля
    def draw_field(self):
        for i in range(3):
            for j in range(3):
                player = self.checker.field[i][j]
                if player != 0:
                    square = self.SQUARES[i][j]
                    x, y = square[0] + 100, square[1] + 100
                    if player == 1:
                        color = COLORS['X_color']
                    else:
                        color = COLORS['O_color']
                    symbol = ('X' if player == 1 else 'O')
                    self.draw_text(symbol, 120, color, x, y)

    # рисование линии, по которой игрок победил
    def draw_winning_line(self):
        if self.checker.check_for_winner() is not None and self.checker.check_for_winner() != 'tie':
            line, place = self.checker.winning_line
            end_col = (COLORS['X_color'] if self.winner == 1 else COLORS['O_color'])
            if line == 'row':
                y = (place * 200) + 100
                pygame.draw.line(self.surface, end_col, (35, y), (self.width - 35, y), 15)
            if line == 'column':
                x = (place * 200) + 100
                pygame.draw.line(self.surface, end_col, (x, 35), (x, self.height - 35), 15)
            if line == 'diagonal':
                start = (35, 35)
                end = (self.width - 35, self.height - 35)
                if place != 1:
                    start = (self.width - 35, 35)
                    end = (35, self.height - 35)
                pygame.draw.line(self.surface, end_col, start, end, 15)

    # функция для хода
    def make_move(self):
        return_val = self.get_square()
        if return_val is not None and self.checker.check_for_winner() is None:
            active_square, (i, j) = return_val
            self.checker.make_move(i, j)

    # объявление о победителе
    def winner_announcement(self):
        self.winner = self.checker.check_for_winner()
        if self.winner:
            color = COLORS['green']
            if self.winner == 'tie':
                color = COLORS['yellow']
                self.draw_text('Ничья', 30, color, 300, 255)
            else:
                symbol = ('X' if self.winner == 1 else 'O')
                self.draw_text(f"Победил {symbol}!!!", 30, color, 300, 255)
            self.draw_text('Чтобы сыграть заново нажмите ENTER', 25, color, 300, 300)
            self.draw_text('Чтобы выйти из игры нажмите ESC', 25, color, 300, 345)

    # удаление старого чекера и создание нового
    def reset(self):
        del self.checker
        self.checker = Checker()


# основной код
if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Tic Tac Toe')
    clock = pygame.time.Clock()
    field = Field()
    started = 0
    while True:
        if started:
            clock.tick(30)
        started = 1
        field.draw_board()
        field.get_square()
        field.draw_field()
        field.draw_winning_line()
        field.winner_announcement()
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and
                                             event.key == pygame.K_ESCAPE):
                pygame.quit()
                exit(0)
            if event.type == pygame.MOUSEBUTTONUP:
                field.make_move()
                field.draw_field()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                field.reset()
        pygame.display.flip()
