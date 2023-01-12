from tkinter import *

tk = Tk()
tk.resizable(False, False)


canvas = Canvas(tk, width=600, height=600)
canvas.pack()

ball = canvas.create_oval(310, 310, 350, 350, fill='black')
speed = 4


def moveBall():
    global speed

    canvas.move(ball, 0, speed)

    (leftPos, topPos, rightPos, bottomPos) = canvas.coords(ball)
    if speed > 0:
        speed *= 1.02
    if speed < 0:
        speed /= 1.02

    if topPos <= 300 or bottomPos >= 600:
        speed = -speed

    canvas.after(30, moveBall)


canvas.after(30, moveBall)
tk.mainloop()
