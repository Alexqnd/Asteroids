import pygame
from pygame.constants import (QUIT,K_SPACE, K_LEFT, K_RIGHT, K_ESCAPE, KEYDOWN)
import os

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
    
    def rotate_left(self):
        self.angle += 22.5
        self.image = pygame.transform.rotate(self.image_template, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)

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

    def draw(self) -> None:
        self.screen.fill((0, 0, 50))
        self.spaceship.draw(self.screen)
        pygame.display.flip()

if __name__ == '__main__':
    game = Game()
    game.run()