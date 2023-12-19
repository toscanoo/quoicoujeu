"""jeu à deux : le quoicoujeu"""


import pygame
import numpy as np

pygame.init()
pygame.display.set_caption("plato")


class Game:
    def __init__(self):
        self.width = 1000
        self.height = 600

    def draw_square(self, position, color, size):
        rect2 = pygame.Rect(position[0] - size / 2, position[1] - size / 2, size, size)
        pygame.draw.rect(self.screen, color, rect2)
        pygame.display.update()

    def init_screen(self):
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.screen.fill((0, 0, 0))


class player1:
    def __init__(self):
        self.color = (250, 255, 255)
        self.pos = [100, 100]
        self.speed = 10
        self.rot_speed = 10
        self.angle = 0
        self.lsight = 20
        self.color_sight = (255, 0, 255)
        self.size_sight = 5
        self.size = 20

    def move(self, step):
        self.pos = [self.pos[0] + step[0], self.pos[1] + step[1]]

    def display_sight(self):
        xsight = self.pos[0] + self.lsight * np.cos(self.angle)
        ysight = self.pos[1] + self.lsight * np.sin(self.angle)
        game.draw_square([xsight, ysight], self.color_sight, self.size_sight)

    def display(self):
        game.draw_square(self.pos, self.color, self.size)


class Shoot:
    def __init__(self, player):
        self.color = (255, 0, 0)
        self.pos = player1


game = Game()
clock = pygame.time.Clock()
player1 = player1()
game.init_screen()

while True:
    clock.tick(30)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                pygame.quit()
            if (
                pygame.key.get_pressed()[pygame.K_LEFT] == 1
            ):  # ajouter condition bord de map
                X = -1
            if pygame.key.get_pressed()[pygame.K_RIGHT] == 1:
                X = 1
            if pygame.key.get_pressed()[pygame.K_UP] == 1:
                Y = -1
            if pygame.key.get_pressed()[pygame.K_DOWN] == 1:
                Y = 1

    player1.move([X * player1.speed, Y * player1.speed])
    game.init_screen()
    player1.display()
    player1.display_sight()
    pygame.display.update()
