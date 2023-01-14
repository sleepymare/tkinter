import tkinter
from tkinter import *
from tkinter import font
from objects import *
import random
import time


class Game:
    def __init__(self):
        self.lives = LIVES
        self.window = Tk()
        self.window.title('Asteroids')
        self.score = 0
        self.resistance = 0.1
        self.state = 'start'
        c_font = font.Font(family='Times',
                           size=21, weight='normal', slant='italic')

        self.canvas = Canvas(self.window, width=WIDTH, height=HEIGHT)
        self.canvas.pack()

        self.background = StaticObject(0, 0, (WIDTH, HEIGHT), self, self.canvas, filename='b1.png', anchor=tkinter.NW)

        self.start_page = StaticObject(WIDTH // 2, HEIGHT // 2, (WIDTH // 2, HEIGHT // 2), self, self.canvas,
                                       filename='start.png', tag='startTag',
                                       anchor=tkinter.CENTER)

        self.score_box = StaticObject(15, 15, None, game=self, canvas=self.canvas, font_obj=c_font, color="turquoise",
                                      anchor=tkinter.NW)

        self.lives_box = StaticObject(15, 65, None, game=self, canvas=self.canvas, font_obj=c_font, color="red",
                                      anchor=tkinter.NW)

        self.canvas.tag_bind('startTag', '<ButtonPress-1>', lambda ev: self.click_to_start(ev))

        self.canvas.tag_raise(self.score_box.id)
        self.canvas.tag_raise(self.lives_box.id)
        self.canvas.tag_lower(self.background.id)
        self.set_start()
        self.no_collision_tags = {self.score_box.id, self.lives_box.id, self.background.id, self.start_page.id}
        self.spaceship = None
        self.asteroids = None

    def set_start(self):
        self.state = 'start'
        self.lives = LIVES
        self.score = 0
        self.score_box.change_text(f'Points - {self.score}')
        self.lives_box.change_text(f'Lives - {self.lives}')
        self.canvas.itemconfig(self.start_page.id, state='normal')
        self.canvas.tag_raise(self.start_page.id)

    def click_to_start(self, event):
        self.state = 'play'
        self.canvas.itemconfig(self.start_page.id, state='hidden')

    def game_loop(self):
        while True:
            if self.state == 'start':
                self.start_configuration()
            else:
                self.gameplay()

    def start_configuration(self):
        while self.state == 'start':
            self.canvas.tag_raise(self.start_page.id)
            self.canvas.tag_raise(self.score_box.id)
            self.canvas.tag_raise(self.lives_box.id)
            self.canvas.update()

    def gameplay(self):
        self.spaceship = Spaceship(WIDTH // 2, HEIGHT // 2, 0, 2.5, (150, 150), self, self.canvas,
                                   filename='spaceship.png')
        self.window.bind('<Right>', lambda event: self.spaceship.rotate())
        self.window.bind('<Left>', lambda event: self.spaceship.rotate(clockwise=False))
        self.window.bind('<Up>', lambda event: self.spaceship.move_forward())
        self.window.bind('<Escape>', lambda event: self.set_start())
        self.window.bind('<space>', lambda event: self.spaceship.shoot_missiles())

        print(self.asteroids)
        self.asteroids = set([Asteroid(random.randint(50, 750), random.randint(20, 150), random.randint(0, 360),
                                       5, (70, 70), self, self.canvas, filename='ast1.png')
                              for ast in range(7)])

        start_time = time.time()

        while self.state == 'play':
            elapsed_time = time.time() - start_time
            if elapsed_time > 2:
                for _ in range(3):
                    self.asteroids.add(Asteroid(random.randint(50, 750), random.randint(50, 100),
                                                random.randint(0, 360), 4, (70, 70),
                                                self, self.canvas, filename='ast1.png'))
                start_time = time.time()
            current_rockets = set()
            destroyed_asteroids = set()

            for rocket in self.spaceship.rockets:
                for asteroid in rocket.update():
                    destroyed_asteroids.add(asteroid)
                if rocket.state == 'alive':
                    current_rockets.add(rocket)
            self.spaceship.rockets = current_rockets

            for asteroid in self.spaceship.update():
                destroyed_asteroids.add(asteroid)

            current_asteroids = self.asteroids.copy()
            self.asteroids = set()
            for asteroid in current_asteroids:
                asteroid.update(toroidal=True)
                if asteroid.id not in destroyed_asteroids:
                    self.asteroids.add(asteroid)
            self.canvas.tag_raise(self.score_box.id)
            self.canvas.tag_raise(self.lives_box.id)
            self.canvas.update()

        for asteroid in self.asteroids:
            self.canvas.delete(asteroid.id)
        self.asteroids.clear()

        self.canvas.delete(self.spaceship.id)
        for rocket in self.spaceship.rockets:
            self.canvas.delete(rocket.id)
        self.spaceship.rockets.clear()
        self.spaceship = None


game = Game()
game.game_loop()
