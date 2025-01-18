import random

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 10

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


# Тут опишите все классы игры.
class GameObject:
    """Квадрат"""

    def __init__(self, position=(0, 0), body_color=BOARD_BACKGROUND_COLOR):
        self.position = position
        self.body_color = body_color

    def draw(self):
        """Квадрат отрисовка"""
        pass


class Apple(GameObject):
    """Яблоко"""

    def randomize_position(self):
        """Яблоко рандом"""
        self.position = (random.randrange(0, 621, 20), random.randrange(0, 461, 20))

    def draw(self):
        """Яблоко отрисовка"""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

    def __init__(self):
        super().__init__((0, 0), APPLE_COLOR)
        self.randomize_position()


class Snake(GameObject):
    """Змея"""

    def update_direction(self):
        """Змея смена направления"""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Змея движение"""
        self.update_direction()
        if self.direction == UP:
            new_p = self.positions[0][1] - 20 if self.positions[0][1] - 20 >= 0 else 460
            self.positions = [(self.positions[0][0], new_p)] + self.positions
        elif self.direction == DOWN:
            new_p = self.positions[0][1] + 20 if self.positions[0][1] + 20 < 480 else 0
            self.positions = [(self.positions[0][0], new_p)] + self.positions
        elif self.direction == RIGHT:
            new_p = self.positions[0][0] + 20 if self.positions[0][0] + 20 < 640 else 0
            self.positions = [(new_p, self.positions[0][1])] + self.positions
        elif self.direction == LEFT:
            new_p = self.positions[0][0] - 20 if self.positions[0][0] - 20 >= 0 else 620
            self.positions = [(new_p, self.positions[0][1])] + self.positions
        self.last = self.positions[-1]
        del self.positions[-1]

    def draw(self):
        """Змея отрисовка"""
        for position in self.positions[:-1]:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def get_head_position(self):
        """Змея голова"""
        return self.positions[0]

    def reset(self):
        """Змея сброс"""
        for position in self.positions:
            r = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, r)
        self.length = 1
        self.positions = [(320, 240)]
        self.direction = RIGHT
        self.next_direction = None

    def ate_itself(self):
        """Змея самопоедание"""
        l = len(self.positions)
        if l > 1 and self.get_head_position() in self.positions[1::]:
            self.reset()

    def __init__(self):
        super().__init__((320, 240), SNAKE_COLOR)
        self.length = 1
        self.positions = [(320, 240)]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None


def handle_keys(game_object):
    """Управление"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Игра"""
    pygame.init()
    a = Apple()
    s = Snake()

    while True:
        clock.tick(SPEED)
        handle_keys(s)
        s.move()
        s.ate_itself()
        if s.get_head_position() == a.position:
            s.length += 1
            s.positions.append(s.last)
            s.last = None
            a.randomize_position()
        s.draw()
        a.draw()
        pygame.display.update()


if __name__ == '__main__':
    main()
