import math
import os
from pathlib import Path
from PIL import Image, ImageTk

WIDTH = 1000
HEIGHT = 600
LIVES = 3


def get_path(file_path):
    dir = os.path.dirname(Path(__file__).absolute())
    return os.path.join(dir, file_path)


class Object:
    def __init__(self, x, y, size, game, canvas, filename=None, color=None):
        self.x = x
        self.y = y
        self.size = size
        self.color = color
        self.game = game
        self.canvas = canvas
        self.img_name = filename
        if self.img_name:
            image = Image.open(self.img_name)
            image = image.resize(self.size)
            self.image = ImageTk.PhotoImage(image)
        self.id = self.draw(self.x, self.y)

    def draw(self, x, y):
        return


class StaticObject(Object):
    def __init__(self, x, y, size, game, canvas, filename=None, text=None, tag=None, anchor=None, font_obj=None,
                 color=None):
        self.text = text
        self.tag = tag
        self.anchor = anchor
        self.font = font_obj
        super().__init__(x, y, size, game, canvas, filename, color)

    def draw(self, x, y):
        if self.img_name:
            return self.canvas.create_image(self.x, self.y, image=self.image, tag=self.tag, anchor=self.anchor)
        else:
            return self.canvas.create_text(self.x, self.y, anchor=self.anchor, text=self.text,
                                           fill=self.color, font=self.font)

    def change_text(self, text):
        self.canvas.itemconfigure(self.id, text=text)


class MovingObject(Object):
    def __init__(self, x, y, angle, speed, size, game, canvas, color=None, filename=None):
        self.state = 'alive'
        self.angle = angle
        self.speed = speed
        super().__init__(x, y, size, game, canvas, filename, color)

    def draw(self, x, y):
        return self.canvas.create_rectangle(x - self.size[0], y - self.size[1],
                                            x + self.size[0], y + self.size[1], fill=self.color)

    def redraw(self):
        self.canvas.delete(self.id)
        self.id = self.draw(self.x, self.y)

    def move(self):
        dx = math.cos(math.radians(self.angle)) * self.speed
        dy = -math.sin(math.radians(self.angle)) * self.speed
        self.x += dx
        self.y += dy
        self.canvas.move(self.id, dx, dy)

    def update(self, toroidal=False, moving=True):
        if toroidal:
            if self.x < 0:
                self.x += WIDTH - 100
                self.canvas.move(self.id, WIDTH - 100, 0)
            elif self.x > WIDTH:
                self.x -= WIDTH
                self.canvas.move(self.id, -WIDTH, 0)
            elif self.y < 0:
                self.y += HEIGHT
                self.canvas.move(self.id, 0, HEIGHT - 100)
            elif self.y > HEIGHT:
                self.y -= HEIGHT
                self.canvas.move(self.id, 0, -HEIGHT)
        else:
            if self.x < 0 or self.x > WIDTH or self.y < 0 or self.y > HEIGHT:
                self.canvas.delete(self.id)
                self.state = 'destroyed'
        if moving:
            return self.move()


class Missile(MovingObject):
    def __init__(self, x, y, angle, speed, size, game, canvas, filename=None):
        super().__init__(x, y, angle, speed, size, game, canvas, filename=filename)
        image = Image.open(self.img_name)
        image = image.resize(self.size)
        self.image = ImageTk.PhotoImage(image.rotate(self.angle))
        self.redraw()

    def draw(self, x, y):
        return self.canvas.create_image(self.x, self.y, image=self.image)

    def move(self):
        destroyed = []
        super().move()
        collision = self.canvas.find_overlapping(self.x, self.y, self.x + self.size[0] - 10,
                                                 self.y + self.size[1] - 5)
        for collision_object in collision:
            if collision_object != self.id and collision_object not in self.game.no_collision_tags \
                    and collision_object != self.game.spaceship.id \
                    and collision_object not in set([rocket.id for rocket in self.game.spaceship.rockets]):
                self.canvas.delete(collision_object)

                destroyed.append(collision_object)
                self.state = 'destroyed'
                self.canvas.delete(self.id)
                self.game.score += 1
                self.game.score_box.change_text(f'Points - {self.game.score}')
                break
        return destroyed

    def rotate(self):
        self.rotate_img()

    def rotate_img(self):
        image = Image.open(self.img_name)
        image = image.resize(self.size)
        self.image = ImageTk.PhotoImage(image.rotate_img(self.angle))
        self.redraw()


class Spaceship(MovingObject):
    def __init__(self, x, y, angle, speed, size, game, canvas, filename):
        self.moving = False
        self.rockets = set()
        self.dx = 0
        self.dy = 0
        self.acceleration = 0
        super().__init__(x, y, angle, speed, size, game, canvas, filename=filename)

    def move(self):
        self.x += self.dx
        self.y += self.dy
        if abs(self.dx) < self.speed / 5 and abs(self.dy) < self.speed / 5:
            self.moving = False
        else:
            self.moving = True
        self.canvas.move(self.id, self.dx, self.dy)
        self.dx *= (1 - self.game.resistance)
        self.dy *= (1 - self.game.resistance)

    def move_forward(self):
        self.dx += math.cos(math.radians(self.angle)) * self.speed
        self.dy += -math.sin(math.radians(self.angle)) * self.speed

    def update(self, toroidal=False, moving=True):
        if self.x < 0:
            self.x += WIDTH
            self.canvas.move(self.id, WIDTH, 0)
        elif self.x > WIDTH - 10:
            self.x -= WIDTH
            self.canvas.move(self.id, -WIDTH, 0)
        elif self.y < 0:
            self.y += HEIGHT
            self.canvas.move(self.id, 0, HEIGHT)
        elif self.y > HEIGHT - 10:
            self.y -= HEIGHT
            self.canvas.move(self.id, 0, -HEIGHT)
        self.redraw()
        destroyed = []
        collision = self.canvas.find_overlapping(self.x, self.y, self.x + self.size[0] / 3, self.y + self.size[1] / 3)

        for collision_object in collision:
            if collision_object != self.id and collision_object not in self.game.no_collision_tags \
                    and collision_object not in set([rocket.id for rocket in self.rockets]):
                self.canvas.delete(collision_object)
                destroyed.append(collision_object)
                self.x = WIDTH // 2
                self.y = HEIGHT // 2
                self.redraw()
                self.state = 'destroyed'
                self.game.lives -= 1
                self.game.lives_box.change_text(f'Lives - {self.game.lives}')
                if self.game.lives <= 0:
                    self.game.set_start()

                break
        self.move()
        return destroyed

    def rotate(self, clockwise=True):
        if clockwise:
            self.angle -= 36
        else:
            self.angle += 36
        self.angle %= 360
        self.rotate_img()

    def rotate_img(self):
        image = Image.open(self.img_name)
        image = image.resize(self.size)
        self.image = ImageTk.PhotoImage(image.rotate(self.angle))
        self.redraw()

    def create_img(self, img_name):
        image = Image.open(get_path(img_name))
        image = image.resize(self.size)
        self.image = ImageTk.PhotoImage(image.rotate(self.angle))
        return self.canvas.create_image(self.x, self.y, image=self.image)

    def draw(self, x, y):
        return self.create_img(self.img_name)

    def redraw(self):
        self.canvas.delete(self.id)
        self.id = self.draw(self.x, self.y)

    def shoot_missiles(self):
        dx = math.cos(math.radians(self.angle)) * 25
        dy = -math.sin(math.radians(self.angle)) * 25
        self.rockets.add(Missile(self.x + dx, self.y + dy, self.angle, 25, (20, 20), self.game, self.canvas,
                                 filename='missile.png'))


class Asteroid(MovingObject):
    def __init__(self, x, y, angle, speed, size, game, canvas, filename):
        super().__init__(x, y, angle, speed, size, game, canvas, filename=filename)

    def draw(self, x, y):
        return self.canvas.create_image(self.x, self.y, image=self.image)
