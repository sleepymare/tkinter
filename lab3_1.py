from tkinter import *
from time import *
from random import *

tk = Tk()
c = Canvas(tk, width=500, height=500, background='black')
c.pack()


total_drops = 150
raindrop = [0 for _ in range(total_drops)]
rainX = [randint(0, 500) for _ in range(total_drops)]
rainY = [randint(-200, 0) for _ in range(total_drops)]

rainSpeed = []
rainLength = []


for i in range(total_drops):
    length = randint(10, 20)
    rainLength.append(length)
    rainSpeed.append(10 + length / 2)

while 1:
    for i in range(total_drops):
        raindrop[i] = c.create_line(rainX[i], rainY[i], rainX[i], rainY[i] + rainLength[i], fill='turquoise')
        rainY[i] += rainSpeed[i]
        if rainY[i] > 800 - rainLength[i]:
            rainY[i] = -rainLength[i]

    c.update()
    sleep(0.025)
    for i in range(total_drops):
        c.delete(raindrop[i])

