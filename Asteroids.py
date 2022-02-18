import pygame
from pygame.constants import (QUIT, K_LEFT, K_RIGHT, K_UP, K_ESCAPE, KEYDOWN)
import os
import math

class Settings(object):
    window = {'width': 800, 'height':500}
    fps = 60
    title = "Asteroids"
    path = {}
    path['file'] = os.path.dirname(os.path.abspath(__file__))
    path['image'] = os.path.join(path['file'], "images")

    @staticmethod
    def dim():
        return (Settings.window['width'], Settings.window['height'])

    @staticmethod
    def filepath(name):
        return os.path.join(Settings.path['file'], name)

    @staticmethod
    def imagepath(name):
        return os.path.join(Settings.path['image'], name)

class Spaceship(pygame.sprite.Sprite):
    def __init__(self) -> None:
        super().__init__()
        self.width = 60
        self.height = 60
        self.angle = 0
        self.image = pygame.image.load(Settings.imagepath("spaceship0.png")).convert()
        self.image_template = pygame.transform.scale(self.image, (self.width, self.height)).convert()
        self.image = self.image_template
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.center = (Settings.window['width'] // 2, Settings.window['height'] // 2)
        self.center_original = self.rect.center
        self.direction = (0, 0)

    def update(self,) -> None:
        self.rect.move_ip(self.direction)
        self.warp_to_other_side()

    def rotate_left(self):
        self.angle += 22.5
        if self.angle >= 360:
            self.angle -= 360
        self.image = pygame.transform.rotate(self.image_template, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)
    
    def rotate_right(self):
        self.angle -= 22.5
        if self.angle < 0:
            self.angle += 360
        self.image = pygame.transform.rotate(self.image_template, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)

    def accelerate(self):
        new_direction_x = self.direction[0] - math.sin(math.radians(self.angle))
        new_direction_y = self.direction[1] - math.cos(math.radians(self.angle))
        if new_direction_x <= 10 and new_direction_x >= -10:
            self.direction = (new_direction_x, self.direction[1])
        if new_direction_y <= 10 and new_direction_y >= -10:
            self.direction = (self.direction[0], new_direction_y)
        print(self.direction)

    def warp_to_other_side(self):
        if self.rect.right <= 0:
            self.rect.left = Settings.window["width"]
        elif self.rect.left >= Settings.window["width"]:
            self.rect.right = 0
        if self.rect.bottom <= 0:
            self.rect.top = Settings.window["height"]
        elif self.rect.top >= Settings.window["height"]:
            self.rect.bottom = 0

class Game(object):
    def __init__(self):
        super().__init__()
        os.environ['SDL_VIDEO_WINDOW_POS'] = "10, 50"
        pygame.init()
        self.screen = pygame.display.set_mode(Settings.dim())
        pygame.display.set_caption(Settings.title)
        self.clock = pygame.time.Clock()
        self.spaceship = pygame.sprite.GroupSingle(Spaceship())
        self.running = False

    def run(self) -> None:
        self.running = True
        while self.running:
            self.clock.tick(Settings.fps)
            self.update()
            self.watch_for_events()
            self.draw()
        pygame.quit()

    def watch_for_events(self) -> None:
        for event in pygame.event.get():
            if event.type == QUIT:
                self.running = False
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.running = False
                elif event.key == K_LEFT:
                    self.spaceship.sprite.rotate_left()
                elif event.key == K_RIGHT:
                    self.spaceship.sprite.rotate_right()
                elif event.key == K_UP:
                    self.spaceship.sprite.accelerate()

    def update(self) -> None:
        self.spaceship.sprite.update()

    def draw(self) -> None:
        self.screen.fill((0, 0, 50))
        self.spaceship.draw(self.screen)
        pygame.display.flip()

if __name__ == '__main__':
    game = Game()
    game.run()