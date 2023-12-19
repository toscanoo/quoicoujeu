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
        self.color = (200, 200, 200)
        self.pos = [100, 100]
        self.speed = 10
        self.rot_speed = 10
        self.angle = 0
        self.lsight = 20
        self.color_sight = (255, 0, 255)
        self.size_sight = 5
        self.size = 20

    def rotation(self, horaire):  # horaire booléen true pour sens horaire, sinon false
        if horaire:
            self.angle = self.angle + self.rot_speed
        else:
            self.angle = self.angle - self.rot_speed

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
X1L = 0
X1R = 0
Y1U = 0
Y1D = 0
R1 = False
R1S = False
while True:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                pygame.quit()
            if event.key == (pygame.K_LEFT):
                X1L = -1
            if event.key == (pygame.K_RIGHT):
                X1R = 1
            if event.key == (pygame.K_UP):
                Y1U = -1
            if event.key == (pygame.K_DOWN):
                Y1D = 1
            if event.key == (pygame.K_UP):
                Y1U = -1
            if event.key == (pygame.K_DOWN):
                Y1D = 1

        if event.type == pygame.KEYUP:
            if event.key == (pygame.K_LEFT):  # ajouter condition bord de map
                X1L = 0
            if event.key == (pygame.K_RIGHT):
                X1R = 0
            if event.key == (pygame.K_UP):
                Y1U = 0
            if event.key == (pygame.K_DOWN):
                Y1D = 0

        if player1.pos[0] < 0:
            X1L = 0
        if player1.pos[0] > 1000:
            X1R = 0
        if player1.pos[1] < 0:
            Y1U = 0
        if player1.pos[1] > 600:
            Y1D = 0

    player1.move([(X1L + X1R) * player1.speed, (Y1U + Y1D) * player1.speed])
    game.init_screen()
    player1.display()
    player1.display_sight()
    pygame.display.update()
