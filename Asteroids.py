import pygame
from pygame.constants import (QUIT, K_LEFT, K_RIGHT, K_UP, K_ESCAPE, K_SPACE, K_RETURN, KEYDOWN)
from random import randint
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

class Timer(object):
    def __init__(self, duration, with_start = True):
        self.duration = duration
        if with_start:
            self.next = pygame.time.get_ticks()
        else:
            self.next = pygame.time.get_ticks() + self.duration

    def is_next_stop_reached(self):
        if pygame.time.get_ticks() > self.next:
            self.next = pygame.time.get_ticks() + self.duration
            return True
        return False

    def change_duration(self, delta=10):
        self.duration += delta
        if self.duration < 0:
            self.duration = 0

class Spaceship(pygame.sprite.DirtySprite):
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
        self.shoot_force = 3
        self.dirty = 1

    def update(self,) -> None:
        if self.direction[0] != 0 or self.direction[1] != 0:
            self.rect.move_ip(self.direction)
            self.warp_to_other_side()

    def rotate_left(self):
        self.angle += 22.5
        if self.angle >= 360:
            self.angle -= 360
        self.image = pygame.transform.rotate(self.image_template, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)
        self.dirty = 1
    
    def rotate_right(self):
        self.angle -= 22.5
        if self.angle < 0:
            self.angle += 360
        self.image = pygame.transform.rotate(self.image_template, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)
        self.dirty = 1

    def accelerate(self):
        new_direction_x = self.direction[0] - math.sin(math.radians(self.angle))
        new_direction_y = self.direction[1] - math.cos(math.radians(self.angle))
        if new_direction_x <= 10 and new_direction_x >= -10:
            self.direction = (new_direction_x, self.direction[1])
        if new_direction_y <= 10 and new_direction_y >= -10:
            self.direction = (self.direction[0], new_direction_y)

    def warp_to_other_side(self):
        if self.rect.right <= 0:
            self.rect.left = Settings.window["width"]
        elif self.rect.left >= Settings.window["width"]:
            self.rect.right = 0
        if self.rect.bottom <= 0:
            self.rect.top = Settings.window["height"]
        elif self.rect.top >= Settings.window["height"]:
            self.rect.bottom = 0

    def shoot(self, bullet) -> None:
        direction_x = - self.shoot_force * math.sin(math.radians(self.angle)) + self.direction[0]
        direction_y = - self.shoot_force * math.cos(math.radians(self.angle)) + self.direction[1]
        bullet.direction = (direction_x, direction_y)
        bullet.rect.center = (self.rect.center[0], self.rect.center[1])

class Bullet(pygame.sprite.DirtySprite):
    def __init__(self) -> None:
        super().__init__()
        self.width = 20
        self.height = 5
        self.image = pygame.image.load(Settings.imagepath("bullet.png")).convert()
        self.image = pygame.transform.scale(self.image, (self.width, self.height)).convert()
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.center = (Settings.window['width'] // 2, Settings.window['height'] // 2)
        self.direction = (0, 0)
        self.timer = Timer(5000, False)

    def update(self) -> None:
        if self.direction[0] != 0 or self.direction[1] != 0:
            self.rect.move_ip(self.direction)
            self.dirty = 1
        if self.timer.is_next_stop_reached():
            self.kill()


class Asteroid(pygame.sprite.DirtySprite):
    def __init__(self, start_x, start_y, speed_h, speed_v) -> None:
        super().__init__()
        self.width = 90
        self.height = 80
        self.image = pygame.image.load(Settings.imagepath("asteroid_big.png")).convert()
        self.image = pygame.transform.scale(self.image, (self.width, self.height)).convert()
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.center = (start_x, start_y)
        self.direction = (speed_h, speed_v)
        self.margin = 20

    def update(self,) -> None:
        if self.direction[0] != 0 or self.direction[1] != 0:
            self.rect.move_ip(self.direction)
            self.warp_to_other_side()

    def warp_to_other_side(self):
        if self.rect.right <= 0:
            self.rect.left = Settings.window["width"]
        elif self.rect.left >= Settings.window["width"]:
            self.rect.right = 0
        if self.rect.bottom <= 0:
            self.rect.top = Settings.window["height"]
        elif self.rect.top >= Settings.window["height"]:
            self.rect.bottom = 0

class Asteroid_normal(Asteroid):
    def __init__(self, start_x, start_y, speed_h, speed_v) -> None:
        super().__init__(start_x, start_y, speed_h, speed_v)
        self.width = 60
        self.height = 60
        self.image = pygame.image.load(Settings.imagepath("asteroid_normal.png")).convert()
        self.image = pygame.transform.scale(self.image, (self.width, self.height)).convert()
        self.image = pygame.transform.scale(self.image, (self.width, self.height)).convert()
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.center = (start_x, start_y)

class Asteroid_small(Asteroid):
    def __init__(self, start_x, start_y, speed_h, speed_v) -> None:
        super().__init__(start_x, start_y, speed_h, speed_v)
        self.width = 30
        self.height = 30
        self.image = pygame.image.load(Settings.imagepath("asteroid_small.png")).convert()
        self.image = pygame.transform.scale(self.image, (self.width, self.height)).convert()
        self.image = pygame.transform.scale(self.image, (self.width, self.height)).convert()
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.center = (start_x, start_y)

class Game(object):
    def __init__(self):
        super().__init__()
        os.environ['SDL_VIDEO_WINDOW_POS'] = "10, 50"
        pygame.init()
        self.screen = pygame.display.set_mode(Settings.dim())
        pygame.display.set_caption(Settings.title)
        self.clock = pygame.time.Clock()
        self.spaceship = pygame.sprite.GroupSingle(Spaceship())
        self.bullets = pygame.sprite.LayeredDirty()
        self.asteroids = pygame.sprite.LayeredDirty()
        self.background_image = pygame.image.load(Settings.imagepath("background.png")).convert()
        self.background_image = pygame.transform.scale(self.background_image, (Settings.window["width"], Settings.window["height"])).convert()
        self.max_asteroids = 5
        self.asteroids_spawntimer = Timer(3000, True)
        #self.bullets.clear(self.screen, self.background_image)
        self.running = False
    

    def run(self) -> None:
        self.running = True
        while self.running:
            if self.asteroids_spawntimer.is_next_stop_reached():
                self.spawn_asteroid()
            self.clock.tick(Settings.fps)
            self.update()
            self.watch_for_events()
            self.draw()
        pygame.quit()

    def shoot(self) -> None:
        if len(self.bullets) < 10:
            bullet = Bullet()
            self.spaceship.sprite.shoot(bullet)
            self.bullets.add(bullet)

    def spawn_asteroid(self) -> None:
        if len(self.asteroids) < self.max_asteroids:
            for i in range(0, 100):
                rand_x = randint(0, Settings.window['width'])
                rand_y = randint(0, Settings.window['height'])
                rand_speed_h = randint(0, 2)
                rand_speed_v = randint(0, 2)
                asteroid_types = [Asteroid(rand_x, rand_y, rand_speed_h, rand_speed_v), Asteroid_normal(rand_x, rand_y, rand_speed_h, rand_speed_v), Asteroid_small(rand_x, rand_y, rand_speed_h, rand_speed_v)]
                new_asteroid = asteroid_types[randint(0, 2)]
                collision = pygame.sprite.spritecollideany(new_asteroid, self.spaceship, collided=pygame.sprite.collide_mask)
                right_wall = new_asteroid.rect.right >= Settings.window['width'] - new_asteroid.margin
                bottom_wall = new_asteroid.rect.bottom >= Settings.window['height'] - new_asteroid.margin
                left_wall = new_asteroid.rect.left <= new_asteroid.margin
                top_wall = new_asteroid.rect.top <= new_asteroid.margin
                if not collision and not right_wall and not bottom_wall and not left_wall and not top_wall:
                    self.asteroids.add(new_asteroid)
                    break

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
                elif event.key == K_RETURN or event.key == K_SPACE:
                    self.shoot()

    def update(self) -> None:
        self.spaceship.sprite.update()
        self.bullets.update()
        self.asteroids.update()

    def draw(self) -> None:
        self.screen.blit(self.background_image, (0, 0))
        self.spaceship.draw(self.screen)
        self.bullets.draw(self.screen)
        self.asteroids.draw(self.screen)
        pygame.display.flip()

if __name__ == '__main__':
    game = Game()
    game.run()