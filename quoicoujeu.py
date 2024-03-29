"""jeu à deux : le quoicoujeu"""

import pygame
import numpy as np


pygame.init()
pygame.display.set_caption("plato")


class Game:
    def __init__(self):
        self.width = 1000
        self.height = 600
        self.dict_bullets = {}
        self.index_bullets = 0
        self.todel = []
        self.framerate = 50

    def draw_square(self, position, color, size):
        rect2 = pygame.Rect(position[0] - size / 2, position[1] - size / 2, size, size)
        pygame.draw.rect(self.screen, color, rect2)
        pygame.display.update()

    def init_screen(self):
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.screen.fill((0, 0, 0))

    def verif_dist(self, pos1, pos2, dist):
        x1 = pos1[0]
        y1 = pos1[1]
        x2 = pos2[0]
        y2 = pos2[1]
        return np.abs(x1 - x2) < dist and np.abs(y1 - y2) < dist


class Player:
    def __init__(self, dict_features):
        self.name = dict_features["name"]
        self.color = dict_features["color"]
        self.pos = dict_features["spawn"]
        self.speed = 400 / game.framerate
        self.rot_speed = 500 / game.framerate * 0.015
        self.angle = dict_features["init_angle"]
        self.lsight = 40
        self.color_sight = (255, 0, 255)
        self.size_sight = 5
        self.size = 20
        self.horaire = 0
        self.antihoraire = 0
        self.dict_bindings = dict_features
        del self.dict_bindings["name"]
        del self.dict_bindings["color"]
        del self.dict_bindings["spawn"]
        self.XL = 0
        self.XR = 0
        self.YU = 0
        self.tick = 0
        self.YD = 0
        self.alive = True

    def rotation(self):  # horaire booléen true pour sens horaire, sinon false
        self.angle = self.angle + (self.horaire + self.antihoraire) * self.rot_speed

    def move(self):
        step = [(self.XL + self.XR) * self.speed, (self.YU + self.YD) * self.speed]
        self.pos = [self.pos[0] + step[0], self.pos[1] + step[1]]

    def display_sight(self):
        xsight = self.pos[0] + self.lsight * np.cos(self.angle)
        ysight = self.pos[1] + self.lsight * np.sin(self.angle)
        game.draw_square([xsight, ysight], self.color_sight, self.size_sight)

    def display(self):
        game.draw_square(self.pos, self.color, self.size)
        self.move()
        game.draw_square(self.pos, self.color, self.size)

    def shoot(self):
        game.index_bullets += 1
        game.dict_bullets[game.index_bullets] = Bullet(self, game.index_bullets)

    def is_dead(self, bullet):
        dist = bullet.size / 2 + self.size / 2

        if game.verif_dist(bullet.pos, self.pos, dist):
            self.alive = False


class Bullet:
    def __init__(self, player, index):
        self.color = (255, 0, 0)
        self.angle = player.angle
        self.speed = 450 / game.framerate
        self.pos = [
            player.pos[0] + 40 * np.cos(self.angle),
            player.pos[1] + 40 * np.sin(self.angle),
        ]

        self.size = 15
        self.index = index

    def move(self):
        self.pos = [
            self.pos[0] + self.speed * np.cos(self.angle),
            self.pos[1] + self.speed * np.sin(self.angle),
        ]

    def verif_visible(self):
        if (
            self.pos[0] < 0
            or self.pos[0] > 1000
            or self.pos[1] < 0
            or self.pos[1] > 600
        ):
            game.todel.append(self.index)

    def display(self):
        game.draw_square(self.pos, self.color, self.size)

    def kill(self):
        del game.dict_bullets[self.index]


game = Game()
clock = pygame.time.Clock()

features1 = {
    "up": pygame.K_UP,
    "down": pygame.K_DOWN,
    "left": pygame.K_LEFT,
    "right": pygame.K_RIGHT,
    "rotate_left": pygame.K_k,
    "rotate_right": pygame.K_m,
    "shoot": pygame.K_o,
    "name": "right player",
    "spawn": [900, 500],
    "color": (250, 250, 0),
    "init_angle": np.pi,
}

features2 = {
    "up": pygame.K_z,
    "down": pygame.K_s,
    "left": pygame.K_q,
    "right": pygame.K_d,
    "rotate_left": pygame.K_f,
    "rotate_right": pygame.K_h,
    "shoot": pygame.K_SPACE,
    "name": "left player",
    "spawn": [100, 100],
    "color": (100, 100, 255),
    "init_angle": 0,
}

player1 = Player(features1)
player2 = Player(features2)
game.init_screen()

while player1.alive and player2.alive:
    clock.tick(game.framerate)
    game.init_screen()
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            for player in [player1, player2]:
                if event.key == (player.dict_bindings["left"]):
                    player.XL = -1
                if event.key == (player.dict_bindings["right"]):
                    player.XR = 1
                if event.key == (player.dict_bindings["up"]):
                    player.YU = -1
                if event.key == (player.dict_bindings["down"]):
                    player.YD = 1
                if event.key == (player.dict_bindings["rotate_left"]):
                    player.horaire = 1
                if event.key == (player.dict_bindings["rotate_right"]):
                    player.antihoraire = -1
                if event.key == (player.dict_bindings["shoot"]):
                    player.shoot()

        if event.type == pygame.KEYUP:
            for player in [player1, player2]:
                if event.key == (player.dict_bindings["left"]):
                    player.XL = 0
                if event.key == (player.dict_bindings["right"]):
                    player.XR = 0
                if event.key == (player.dict_bindings["up"]):
                    player.YU = 0
                if event.key == (player.dict_bindings["down"]):
                    player.YD = 0
                if event.key == (player.dict_bindings["rotate_left"]):
                    player.horaire = 0
                if event.key == (player.dict_bindings["rotate_right"]):
                    player.antihoraire = 0

    for player in [player1, player2]:
        if player.pos[0] < 0:
            player.XL = 0
        if player.pos[0] > 1000:
            player.XR = 0
        if player.pos[1] < 0:
            player.YU = 0
        if player.pos[1] > 600:
            player.YD = 0

        player.rotation()
        player.display()
        player.display_sight()

    for bullet_index in game.dict_bullets:
        game.dict_bullets[bullet_index].display()
        game.dict_bullets[bullet_index].move()
        game.dict_bullets[bullet_index].verif_visible()

    for bullet_index in game.dict_bullets:
        for player in [player1, player2]:
            player.is_dead(game.dict_bullets[bullet_index])
            if not player.alive:
                print(str(player.name) + " lost")

    for index in game.todel:
        # if index in gamoeo.dict_bullets:
        game.dict_bullets[index].kill()
    game.todel = []

    pygame.display.flip()

pygame.time.wait(3000)
pygame.quit()
