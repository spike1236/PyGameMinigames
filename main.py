import pygame

# выбор игры (главное меню)
WINDOW = pygame.display.set_mode((660, 300))
pygame.display.set_caption('Главное меню')


def RESET_WINDOW():
    WINDOW.fill((255, 255, 255))
    button_tictactoe.draw(WINDOW)
    button_snake.draw(WINDOW)
    button_tetris.draw(WINDOW)
    button_exit.draw(WINDOW)


class Button:
    def __init__(self, col_c, x, y, width, height, font_size, text=''):
        self.color = col_c
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.font_size = font_size

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height), 2)
        if self.text != '':
            text = pygame.font.Font(pygame.font.match_font('consolas', 1),
                                    self.font_size).render(self.text, True, self.color)
            win.blit(text, (self.x + (self.width / 2 - text.get_width() / 2),
                            self.y + (self.height / 2 - text.get_height() / 2)))

    def is_on(self, pos):
        if self.x < pos[0] < self.x + self.width:
            if self.y < pos[1] < self.y + self.height:
                return True
        return False


pygame.init()
button_tictactoe = Button((0, 200, 0), 20, 30, 200, 140, 15, 'Играть в крестики-нолики')
button_snake = Button((0, 200, 0), 235, 30, 180, 140, 20, 'Играть в змейку')
button_tetris = Button((0, 200, 0), 430, 30, 200, 140, 20, 'Играть в тетрис')
button_exit = Button((200, 0, 0), 280, 180, 100, 100, 20, 'Выйти')
selected = 0
while True:
    pygame.display.update()
    RESET_WINDOW()
    for EVENT in pygame.event.get():
        if EVENT.type == pygame.QUIT:
            pygame.quit()
            exit(0)
        if EVENT.type == pygame.MOUSEBUTTONUP:
            if button_tictactoe.is_on(pygame.mouse.get_pos()):
                selected = 1
                break
            if button_snake.is_on(pygame.mouse.get_pos()):
                selected = 2
                break
            if button_tetris.is_on(pygame.mouse.get_pos()):
                selected = 3
                break
            if button_exit.is_on(pygame.mouse.get_pos()):
                pygame.quit()
                exit(0)
        if EVENT.type == pygame.MOUSEMOTION:
            if button_tictactoe.is_on(pygame.mouse.get_pos()):
                button_tictactoe.color = (20, 255, 10)
            else:
                button_tictactoe.color = (0, 200, 0)
            if button_tetris.is_on(pygame.mouse.get_pos()):
                button_tetris.color = (20, 255, 10)
            else:
                button_tetris.color = (0, 200, 0)
            if button_snake.is_on(pygame.mouse.get_pos()):
                button_snake.color = (20, 255, 10)
            else:
                button_snake.color = (0, 200, 0)
            if button_exit.is_on(pygame.mouse.get_pos()):
                button_exit.color = (255, 20, 10)
            else:
                button_exit.color = (200, 0, 0)
    if selected:
        break
if selected == 1:
    # выбрана игра "крестики-нолики"
    import tictactoe
    WINDOW = pygame.display.set_mode((tictactoe.WIDTH, tictactoe.HEIGHT))
    pygame.display.set_caption('Tic Tac Toe')
    clock = pygame.time.Clock()
    field = tictactoe.Field()
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

if selected == 2:
    # выбрана игра "змейка"
    import random
    # константы
    block_size = 20
    header_margin = 80
    frame_color = (0, 255, 200)
    white_color = (255, 255, 255)
    blue_color = (200, 255, 255)
    apple_color = (255, 0, 0)
    snake_color = (0, 155, 0)
    header_color = (0, 200, 150)
    blocks_number = 20
    margin = 1
    size = [block_size * blocks_number + 2 * block_size + margin * blocks_number,
            block_size * blocks_number + 2 * block_size + margin * blocks_number + header_margin]

    # основной код игры
    class SnakeBlock:
        def __init__(self, x, y):
            self.x = x
            self.y = y

        def is_inside(self):
            return 0 <= self.x < blocks_number and 0 <= self.y < blocks_number

        def __eq__(self, other):
            return isinstance(other, SnakeBlock) and self.x == other.x and self.y == other.y


    def get_empty_block():
        x = random.randint(0, blocks_number - 1)
        y = random.randint(0, blocks_number - 1)
        empty_block = SnakeBlock(x, y)
        while empty_block in snake_blocks:
            empty_block.x = random.randint(0, blocks_number - 1)
            empty_block.y = random.randint(0, blocks_number - 1)
        return empty_block


    def draw_block(sel2_color, sel2_row, sel2_col):
        pygame.draw.rect(WINDOW, sel2_color, [block_size + sel2_col * block_size + margin * (sel2_col + 1),
                                              header_margin + block_size + sel2_row * block_size +
                                              margin * (sel2_row + 1), block_size, block_size])
    WINDOW = pygame.display.set_mode(size)
    pygame.display.set_caption('Змейка')
    timer = pygame.time.Clock()
    font = pygame.font.SysFont('Arial', 36)
    snake_blocks = [SnakeBlock(9, 8), SnakeBlock(9, 9), SnakeBlock(9, 10)]
    apple = get_empty_block()
    d_row = buf_row = 0
    d_col = buf_col = 1
    total = 0
    snake_speed = 1

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(0)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and d_col != 0:
                    buf_row = -1
                    buf_col = 0
                elif event.key == pygame.K_DOWN and d_col != 0:
                    buf_row = 1
                    buf_col = 0
                elif event.key == pygame.K_LEFT and d_row != 0:
                    buf_row = 0
                    buf_col = -1
                elif event.key == pygame.K_RIGHT and d_row != 0:
                    buf_row = 0
                    buf_col = 1

        WINDOW.fill(frame_color)
        pygame.draw.rect(WINDOW, header_color, [0, 0, size[0], header_margin])
        for row in range(blocks_number):
            for col in range(blocks_number):
                if (row + col) % 2 == 0:
                    color = blue_color
                else:
                    color = white_color
                draw_block(color, row, col)

        text_total = font.render("СЧЁТ: {}".format(total), False, white_color)
        text_speed = font.render("СКОРОСТЬ: {}".format(snake_speed), False, apple_color)
        WINDOW.blit(text_total, (block_size, block_size))
        WINDOW.blit(text_speed, (blocks_number * block_size / 2, block_size))

        head = snake_blocks[-1]
        if not head.is_inside():
            pygame.quit()
            exit(0)

        draw_block(apple_color, apple.x, apple.y)
        for block in snake_blocks:
            draw_block(snake_color, block.x, block.y)

        if apple == head:
            total += 1
            snake_speed = total // 5 + 1
            snake_blocks.append(apple)
            apple = get_empty_block()
        d_row = buf_row
        d_col = buf_col
        new_head = SnakeBlock(head.x + d_row, head.y + d_col)
        if new_head in snake_blocks:
            pygame.quit()
            exit(0)
        snake_blocks.append(new_head)
        snake_blocks.pop(0)
        pygame.display.flip()
        timer.tick(3 + snake_speed)

if selected == 3:
    # выбрана игра "тетрис"
    import random
    import pygame

    # константы
    s_width = 800
    s_height = 700
    p_width = 300
    p_height = 600
    block_size = 30

    top_left_x = (s_width - p_width) // 2
    top_left_y = s_height - p_height

    # фигуры
    Tshape = [['.....',
               '..0..',
               '.000.',
               '.....',
               '.....'],
              ['.....',
               '..0..',
               '..00.',
               '..0..',
               '.....'],
              ['.....',
               '.....',
               '.000.',
               '..0..',
               '.....'],
              ['.....',
               '..0..',
               '.00..',
               '..0..',
               '.....']]

    Zshape = [['.....',
               '.....',
               '.00..',
               '..00.',
               '.....'],
              ['.....',
               '..0..',
               '.00..',
               '.0...',
               '.....']]

    Ishape = [['..0..',
               '..0..',
               '..0..',
               '..0..',
               '.....'],
              ['.....',
               '0000.',
               '.....',
               '.....',
               '.....']]

    Oshape = [['.....',
               '.....',
               '.00..',
               '.00..',
               '.....']]

    Sshape = [['.....',
               '.....',
               '..00.',
               '.00..',
               '.....'],
              ['.....',
               '..0..',
               '..00.',
               '...0.',
               '.....']]

    Lshape = [['.....',
               '...0.',
               '.000.',
               '.....',
               '.....'],
              ['.....',
               '..0..',
               '..0..',
               '..00.',
               '.....'],
              ['.....',
               '.....',
               '.000.',
               '.0...',
               '.....'],
              ['.....',
               '.00..',
               '..0..',
               '..0..',
               '.....']]

    Jshape = [['.....',
               '.0...',
               '.000.',
               '.....',
               '.....'],
              ['.....',
               '..00.',
               '..0..',
               '..0..',
               '.....'],
              ['.....',
               '.....',
               '.000.',
               '...0.',
               '.....'],
              ['.....',
               '..0..',
               '..0..',
               '.00..',
               '.....']]

    shapes = [Sshape, Zshape, Ishape, Oshape, Jshape, Lshape, Tshape]
    shape_colors = [(0, 255, 0), (255, 0, 0), (0, 255, 255), (255, 255, 0), (255, 165, 0), (0, 0, 255), (128, 0, 128)]

    # индексы 0 - 6 описывают фигуру

    # основной код
    class Piece:
        def __init__(self, x, y, shape):
            self.x = x
            self.y = y
            self.shape = shape
            self.color = shape_colors[shapes.index(shape)]
            self.rotation = 0


    def create_grid(locked_pos=None):  # *
        if locked_pos is None:
            locked_pos = {}
        grid = [[(0, 0, 0) for _ in range(10)] for _ in range(20)]

        for i in range(len(grid)):
            for j in range(len(grid[i])):
                if (j, i) in locked_pos:
                    c = locked_pos[(j, i)]
                    grid[i][j] = c
        return grid


    def convert_shape_format(shape):
        positions = []
        form = shape.shape[shape.rotation % len(shape.shape)]

        for i, line in enumerate(form):
            for j, column in enumerate(list(line)):
                if column == '0':
                    positions.append((shape.x + j, shape.y + i))

        for i, pos in enumerate(positions):
            positions[i] = (pos[0] - 2, pos[1] - 4)

        return positions


    def valid_space(shape, grid):
        accepted_pos = [[(j, i) for j in range(10) if grid[i][j] == (0, 0, 0)] for i in range(20)]
        accepted_pos = [j for sub in accepted_pos for j in sub]

        formatted = convert_shape_format(shape)

        for pos in formatted:
            if pos not in accepted_pos:
                if pos[1] > -1:
                    return False
        return True


    def check_lost(positions):
        for pos in positions:
            x, y = pos
            if y < 1:
                return True

        return False


    def get_shape():
        return Piece(5, 0, random.choice(shapes))


    def draw_text_middle(surface, text, s_size, c_color):
        label = pygame.font.SysFont("comicsans", s_size, bold=True).render(text, True, c_color)
        surface.blit(label, (top_left_x + p_width / 2 - (label.get_width() / 2),
                             top_left_y + p_height / 2 - label.get_height() / 2))


    def draw_grid(surface, grid):
        sx = top_left_x
        sy = top_left_y

        for i in range(len(grid)):
            pygame.draw.line(surface, (128, 128, 128), (sx, sy + i * block_size), (sx + p_width, sy + i * block_size))
            for j in range(len(grid[i])):
                pygame.draw.line(surface, (128, 128, 128), (sx + j * block_size, sy),
                                 (sx + j * block_size, sy + p_height))


    def clear_rows(grid, locked):
        inc = 0
        ind = -1
        for i in range(len(grid) - 1, -1, -1):
            if (0, 0, 0) not in grid[i]:
                inc += 1
                ind = i
                for j in range(len(grid[i])):
                    try:
                        del locked[(j, i)]
                    except Exception as error:
                        continue

        if inc > 0:
            for key in sorted(list(locked), key=lambda lam: lam[1])[::-1]:
                x, y = key
                if y < ind:
                    newKey = (x, y + inc)
                    locked[newKey] = locked.pop(key)
        return inc


    def draw_next_shape(shape, surface):
        label = pygame.font.SysFont('comicsans', 30).render('Следующая фигура', True, (255, 255, 255))
        sx = top_left_x + p_width + 50
        sy = top_left_y + p_height // 2 - 100
        form = shape.shape[shape.rotation % len(shape.shape)]

        for i, line in enumerate(form):
            for j, column in enumerate(list(line)):
                if column == '0':
                    pygame.draw.rect(surface, shape.color,
                                     (sx + j * block_size, sy + i * block_size, block_size, block_size), 0)

        surface.blit(label, (sx - 30, sy - 30))


    def update_score(d_score):
        score = max_score()

        with open('scores.txt', 'w') as f:
            if int(score) > d_score:
                f.write(str(score))
            else:
                f.write(str(d_score))


    def max_score():
        with open('scores.txt', 'r') as f:
            lines = f.readlines()
            score = lines[0].strip()

        return score


    def draw_window(surface, grid, score=0, last_score=0):
        surface.fill((0, 0, 0))

        pygame.font.init()
        label = pygame.font.SysFont('comicsans', 60).render('Tetris', True, (255, 255, 255))

        surface.blit(label, (top_left_x + p_width / 2 - (label.get_width() / 2), 30))

        # current score
        label = pygame.font.SysFont('comicsans', 30).render('Счет: ' + str(score), True, (255, 255, 255))

        sx = top_left_x + p_width + 50
        sy = top_left_y + p_height / 2 - 100

        surface.blit(label, (sx + 20, sy + 160))
        # last score
        label = pygame.font.SysFont('comicsans', 30).render('Рекорд: ' + str(last_score), True, (255, 255, 255))

        sx = top_left_x - 200
        sy = top_left_y + 200

        surface.blit(label, (sx + 20, sy + 160))

        for i in range(len(grid)):
            for j in range(len(grid[i])):
                pygame.draw.rect(surface, grid[i][j],
                                 (top_left_x + j * block_size, top_left_y + i * block_size, block_size, block_size), 0)

        pygame.draw.rect(surface, (255, 0, 0), (top_left_x, top_left_y, p_width, p_height), 5)

        draw_grid(surface, grid)


    def main():  # *
        last_score = max_score()
        locked_positions = {}

        change_piece = False
        run = True
        current_piece = get_shape()
        next_piece = get_shape()
        clock_main = pygame.time.Clock()
        fall_time = 0
        fall_speed = 0.27
        level_time = 0
        score = 0

        while run:
            grid = create_grid(locked_positions)
            fall_time += clock_main.get_rawtime()
            level_time += clock_main.get_rawtime()
            clock_main.tick()

            if level_time / 1000 > 5:
                level_time = 0
                if level_time > 0.12:
                    level_time -= 0.005

            if fall_time / 1000 > fall_speed:
                fall_time = 0
                current_piece.y += 1
                if not (valid_space(current_piece, grid)) and current_piece.y > 0:
                    current_piece.y -= 1
                    change_piece = True

            for event_ in pygame.event.get():
                if event_.type == pygame.QUIT:
                    run = False
                    pygame.display.quit()
                    exit(0)

                if event_.type == pygame.KEYDOWN:
                    if event_.key == pygame.K_LEFT:
                        current_piece.x -= 1
                        if not (valid_space(current_piece, grid)):
                            current_piece.x += 1
                    if event_.key == pygame.K_RIGHT:
                        current_piece.x += 1
                        if not (valid_space(current_piece, grid)):
                            current_piece.x -= 1
                    if event_.key == pygame.K_DOWN:
                        current_piece.y += 1
                        if not (valid_space(current_piece, grid)):
                            current_piece.y -= 1
                    if event_.key == pygame.K_UP:
                        current_piece.rotation += 1
                        if not (valid_space(current_piece, grid)):
                            current_piece.rotation -= 1

            shape_pos = convert_shape_format(current_piece)

            for i in range(len(shape_pos)):
                x, y = shape_pos[i]
                if y > -1:
                    grid[y][x] = current_piece.color

            if change_piece:
                for pos in shape_pos:
                    p = (pos[0], pos[1])
                    locked_positions[p] = current_piece.color
                current_piece = next_piece
                next_piece = get_shape()
                change_piece = False
                score += clear_rows(grid, locked_positions) * 10

            draw_window(WINDOW, grid, score, int(last_score))
            draw_next_shape(next_piece, WINDOW)
            pygame.display.update()

            if check_lost(locked_positions):
                draw_text_middle(WINDOW, "Вы проиграли!", 80, (255, 255, 255))
                pygame.display.update()
                pygame.time.delay(1500)
                run = False
                update_score(score)


    def main_menu():
        run = True
        while run:
            WINDOW.fill((0, 0, 0))
            draw_text_middle(WINDOW, 'Нажмите любую кнопку для игры', 60, (255, 255, 255))
            pygame.display.update()
            for event_3 in pygame.event.get():
                if event_3.type == pygame.QUIT:
                    run = False
                if event_3.type == pygame.KEYDOWN:
                    main()

        pygame.display.quit()


    WINDOW = pygame.display.set_mode((s_width, s_height))
    pygame.display.set_caption('Tetris')
    main_menu()
