import pygame
import random
import sys

pygame.init()
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
WINDOW = pygame.display.set_mode(size)
pygame.display.set_caption('Змейка')
timer = pygame.time.Clock()
font = pygame.font.SysFont('Arial', 36)


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


def draw_block(a_color, a_row, a_col):
    pygame.draw.rect(WINDOW, a_color, [block_size + a_col * block_size + margin * (a_col + 1),
                                       header_margin + block_size + a_row * block_size + margin * (a_row + 1),
                                       block_size, block_size])


if __name__ == '__main__':
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
                sys.exit()
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
            sys.exit()

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
            sys.exit()

        snake_blocks.append(new_head)
        snake_blocks.pop(0)

        pygame.display.flip()
        timer.tick(3 + snake_speed)
