import sys
import random
from enum import Enum
from collections import namedtuple
import pygame
from pygame.constants import K_a, K_d, K_s, K_w
from const import *


class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4


Point = namedtuple('Point', ['x', 'y'])


class Game:
    """
    This class is creates a snake game

    Attributes:
    _screen
    _lenght
    _is_recenlty_eating
    _head.x
    _head.y
    _direction
    _snake
    """

    def __init__(self):
        self._screen = pygame.display.set_mode(SIZE)

        # Snake
        self._lenght = 2
        self._is_recenlty_eating = False
        self._head = Point(200,200)
        self._direction = Direction.RIGHT
        self._snake = [
            self._head, Point(self._head.x-BLOCK_SIZE, self._head.y),
            Point(self._head.x - (2 * BLOCK_SIZE), self._head.y)  
        ]
        self.is_move_done = False

        # Fruit
        self.fruit = None
        self.random_frut()

        # Points
        self.score = 0

    def game_loop(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit(0)
                elif (
                    event.type == pygame.KEYDOWN
                    and event.key == K_w
                    and self._direction != Direction.DOWN
                    and self.is_move_done == False
                ):
                    self._direction = Direction.UP
                    self.is_move_done = True
                elif (
                    event.type == pygame.KEYDOWN
                    and event.key == K_s
                    and self._direction != Direction.UP
                    and self.is_move_done == False
                ):
                    self._direction = Direction.DOWN
                    self.is_move_done = True
                elif (
                    event.type == pygame.KEYDOWN
                    and event.key == K_a
                    and self._direction != Direction.RIGHT
                    and self.is_move_done == False
                ):
                    self._direction = Direction.LEFT
                    self.is_move_done = True
                elif (
                    event.type == pygame.KEYDOWN
                    and event.key == K_d
                    and self._direction != Direction.LEFT
                    and self.is_move_done == False
                ):
                    self._direction = Direction.RIGHT
                    self.is_move_done = True

            self.is_move_done = False
            self.eating()
            self.sterring()
            game_over = self.is_game_over()
            pygame.time.delay(100)

            self._screen.fill((0, 0, 0))
            self.draw_fruit()
            self.draw_walls()
            self.draw()
            pygame.display.flip()

            if game_over:
                print("Score: ", self.score)
                break

    def eating(self) -> None:
        if self._head.x == self.fruit[0] and self._head.y == self.fruit[1]:
            self._lenght += 1
            self.score += 1
            self._is_recenlty_eating = True
            self.random_frut()

    # Stering
    def sterring(self) -> None:
        x = self._head.x
        y = self._head.y
        if self._direction == Direction.RIGHT:
            x += 20
        if self._direction == Direction.LEFT:
            x -= 20
        if self._direction == Direction.UP:
            y -= 20
        if self._direction == Direction.DOWN:
            y += 20

        if self._is_recenlty_eating is False:
            self._snake.pop(0)
        else:
            self._is_recenlty_eating = False
        self._head = Point(x, y)
        self._snake.append(self._head)
        

    def is_game_over(self) -> bool:
        return bool(
            self.score == 10
            or self._head.x == 0
            or self._head.x == 1180
            or self._head.y == 0
            or self._head.y == 680
            or self._snake[0] in self._snake[1:]
        )

    def random_frut(self) -> None:
        self.fruit = [20 * random.randint(2, 58), 20 * random.randint(2, 33)]

    def draw(self) -> None:
        for element in self._snake:
            pygame.draw.rect(
                self._screen,
                SNAKE_COLOR,
                pygame.Rect(element[0], element[1], BLOCK_SIZE, BLOCK_SIZE),
            )

    def draw_fruit(self) -> None:
        pygame.draw.rect(
            self._screen,
            FRUIT_COLOR,
            pygame.Rect(self.fruit[0], self.fruit[1], BLOCK_SIZE, BLOCK_SIZE),
        )

    def draw_walls(self) -> None:
        pygame.draw.rect(self._screen, WALL_COLOR, pygame.Rect(0, 0, 1200, 20))
        pygame.draw.rect(self._screen, WALL_COLOR, pygame.Rect(0, 680, 1200, 20))
        pygame.draw.rect(self._screen, WALL_COLOR, pygame.Rect(0, 20, 20, 660))
        pygame.draw.rect(self._screen, WALL_COLOR, pygame.Rect(1180, 20, 20, 660))


def main():
    pygame.init()
    game = Game()
    game.game_loop()


if __name__ == "__main__":
    main()
