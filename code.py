import time
from tkinter import *
import threading
import random

ws = Tk()
ws.title("Ping pong")
ws.geometry('500x500')

canvas = Canvas(
    ws,
    height=500,
    width=500,
    bg="#EEE"
)
canvas.pack()
paddlesize = 100
p1 = canvas.create_rectangle(
    0, 0, 10, paddlesize,
    outline="#fb0",
    fill="#fb0"
)

p2 = canvas.create_rectangle(
    canvas.winfo_reqwidth()-4, 0, canvas.winfo_reqwidth() - 14, paddlesize,
    outline="#fb0",
    fill="#fb0"
)

ball = canvas.create_oval(
    10, 10, 20, 20,
    outline="#cb6",
    fill="#c57"
)

p1ScoreText = canvas.create_text(
    50,10,
    text="0",
)
p2ScoreText = canvas.create_text(
    canvas.winfo_reqwidth() - 50,10,
    text="0",
)

radius = canvas.coords(ball)[3] / 2

keypressed = {"w" : False, "s" : False, "i" : False, "k": False}
gamestate = False
bot1 = False
bot2 = False
ballDirection = 0
p1Score = 0
p2Score = 0
paddleSpeed = 0.0155
botReaction = canvas.winfo_reqwidth() * 0.5
speed = 0.002

def pressed(event):
    keypressed[event.keysym] = True

def released(event):
    keypressed[event.keysym] = False

def animate():
    #moves the paddles depending the keys are pressed or not
    x = 0
    y = 0
    while True:
        time.sleep(paddleSpeed)
        if(keypressed["w"] and bot1 is False):#moves p1 paddle up
            if(canvas.coords(p1)[1] > 0):
                y = -5
                canvas.move(p1, x, y)
        if(keypressed["s"] and bot1 is False):#moves p1 paddle down
            if(canvas.coords(p1)[3] < ws.winfo_height() - 1):
                y = 5
                canvas.move(p1, x, y)
        if(keypressed["i"] and bot2 is False):#moves p2 paddle up
            if(canvas.coords(p2)[1] > 0):
                y = -5
                canvas.move(p2, x, y)
        if(keypressed["k"] and bot2 is False):#moves p2 paddle down
            if(canvas.coords(p2)[3] < ws.winfo_height() - 1):
                y = 5
                canvas.move(p2, x, y)

def resize(event):
    #resize the window and move paddle and ball depending on size of window
    canvas.config(width=event.width, height=event.height)
    change = event.width - canvas.coords(p2)[2]
    canvas.move(p2, change, 0)
    canvas.moveto(p1ScoreText, 50, 10)
    canvas.moveto(p2ScoreText, canvas.winfo_reqwidth() - 65, 10)
    if(gamestate == False):
        canvas.moveto(ball, (canvas.winfo_reqwidth()/2) - radius, (canvas.winfo_reqheight()/2) - radius)
        canvas.moveto(p1, 0, (canvas.winfo_reqheight()/2) - paddlesize/2)
        canvas.moveto(p2, canvas.winfo_reqwidth()-15, (canvas.winfo_reqheight()/2) - paddlesize/2)

def resetPaddles():
    canvas.moveto(p1, 0, (canvas.winfo_reqheight()/2) - paddlesize/2)
    canvas.moveto(p2, canvas.winfo_reqwidth()-15, (canvas.winfo_reqheight()/2) - paddlesize/2)

def startGame(event):
    #when spacebar is hit a thread starts and begins to move the ball
    global gamestate
    gamestate = True
    t2 = threading.Thread(target=moveBall, daemon=True)
    t2.start()

def moveBall():
    #ball movement
    global ballDirection, p1Score, p2Score, speed
    x = random.choice([1,-1, 1, -1, 1, -1])
    y = random.uniform(-0.8, 0.8)
    while True:
        time.sleep(speed)
        p1Middle = canvas.coords(p1)[1] + (paddlesize/2)#coordinates of middle of paddle of p1
        p2Middle = canvas.coords(p2)[1] + (paddlesize/2)#coordinates of middle of paddle of p2
        middleOfBall = canvas.coords(ball)[1] + radius#coordinates of middle of ball
        canvas.move(ball, x, y)
        if canvas.coords(ball)[1] < 0:
            #if it hits the top of the window
            y = y*-1
        elif canvas.coords(ball)[3] > canvas.winfo_reqheight():
            #if it hits the bottom of the window
            y = y*-1
        elif canvas.coords(ball)[0] < 10 and (canvas.coords(ball)[1] > canvas.coords(p1)[1] - (radius * 2)) and (canvas.coords(ball)[1] < canvas.coords(p1)[3] + (radius * 2)):
            #if it hits the left paddle
            x = x*-1
            if middleOfBall < p1Middle:
                #if it hits above the middle of the paddle
                y = -1.5 * ((p1Middle - middleOfBall) / (p1Middle - canvas.coords(p1)[1]))
            if middleOfBall > p1Middle:
                #if it hits below the middle of the paddle
                y = 1.5 * ((p1Middle - middleOfBall) / (p1Middle - canvas.coords(p1)[3]))
        elif canvas.coords(ball)[2] > canvas.winfo_reqwidth() - 14 and (canvas.coords(ball)[1] > canvas.coords(p2)[1] - (radius * 2)) and (canvas.coords(ball)[1] < canvas.coords(p2)[3] + (radius * 2)):
            #if it hits the right paddle
            x = x*-1
            if middleOfBall < p2Middle:
                #if it hits above the middle of the paddle
                if(p2Middle - canvas.coords(p1)[1] != 0):
                    y = 1.5 * ((p2Middle - middleOfBall) / (p2Middle - canvas.coords(p1)[1]))
                else:
                    y = 1.5 * 0.1
            if middleOfBall > p2Middle:
                #if it hits below the middle of the paddle
                if(p2Middle - canvas.coords(p1)[1] != 0):
                    y = -1.5 * ((p2Middle - middleOfBall) / (p2Middle - canvas.coords(p1)[1]))
                else:
                    y = -1.5 * 0.1
        elif canvas.coords(ball)[0] < 10:
            #if the ball goes beyond the left of the window
            canvas.moveto(ball, (canvas.winfo_reqwidth()/2) - radius, (canvas.winfo_reqheight()/2) - radius)
            p2Score = p2Score + 1
            canvas.itemconfigure(p2ScoreText, text=p2Score)
            y = random.uniform(-0.8, 0.8)
            x = 1
            resetPaddles()
        elif canvas.coords(ball)[2] > canvas.winfo_reqwidth() - 14:
            #if the ball goes beyond the right of the window
            canvas.moveto(ball, (canvas.winfo_reqwidth()/2) - radius, (canvas.winfo_reqheight()/2) - radius)
            p1Score = p1Score + 1
            canvas.itemconfigure(p1ScoreText, text=p1Score)
            y = random.uniform(-0.8, 0.8)
            x = -1
            resetPaddles()
        ballDirection = x#track which direction the ball is going

def togglep1bot(event):#if the h key is pressed, the bot for p2 turns on and off
    global bot1
    if bot1 is False:
        bot1 = True
        t4 = threading.Thread(target=movep1bot, daemon=True)
        t4.start()
        print("p1 bot is on")
    else:
        bot1 = False
        print("p1 bot is off")

def togglep2bot(event):#if the h key is pressed, the bot for p2 turns on and off
    global bot2
    if bot2 is False:
        bot2 = True
        t3 = threading.Thread(target=movep2bot, daemon=True)
        t3.start()
        print("p2 bot is on")
    else:
        bot2 = False
        print("p2 bot is off")

def movep1bot():
    global ballDirection
    x = 0
    y = 0
    while True and bot1 is True:
        time.sleep(paddleSpeed)
        p1Middle = canvas.coords(p1)[1] + (paddlesize/2)
        middleOfBall = canvas.coords(ball)[1] + radius#coordinates of middle of ball
        if(canvas.coords(ball)[0] < ((canvas.winfo_reqwidth() / 3) + botReaction) and ballDirection < 0):
            #the bot tracks the ball when the ball crosses to their half of the screen
            if(middleOfBall < p1Middle - 10):
                #if the ball is above them move up
                if(canvas.coords(p1)[1] > 0):
                    y = -5
                    canvas.move(p1, x, y)
            elif(middleOfBall > p1Middle + 10):
                #if the ball is below them move down
                if(canvas.coords(p1)[3] < ws.winfo_height() - 1):
                    y = 5
                    canvas.move(p1, x, y)
            else:
                #dont move if the ball is moving away from them
                y = 0

def movep2bot():
    global ballDirection
    x = 0
    y = 0
    while True and bot2 is True:
        time.sleep(paddleSpeed)
        p2Middle = canvas.coords(p2)[1] + (paddlesize/2)
        middleOfBall = canvas.coords(ball)[1] + radius#coordinates of middle of ball
        if(canvas.coords(ball)[0] > ((canvas.winfo_reqwidth() / 3) - botReaction) and ballDirection > 0):
            #the bot tracks the ball when the ball crosses to their half of the screen
            if(middleOfBall < p2Middle - 10):
                #if the ball is above them move up
                if(canvas.coords(p2)[1] > 0):
                    y = -5
                    canvas.move(p2, x, y)
            elif(middleOfBall > p2Middle + 10):
                #if the ball is below them move down
                if(canvas.coords(p2)[3] < ws.winfo_height() - 1):
                    y = 5
                    canvas.move(p2, x, y)
            else:
                #dont move if the ball is moving away from them
                y = 0

ws.bind("<Configure>", resize)
ws.bind('<space>', startGame)
ws.bind('h', togglep2bot)
ws.bind('g', togglep1bot)

for keys in ["w", "s", "i", "k"]:
    ws.bind(keys, pressed)
    ws.bind("<KeyRelease>", released)

t1 = threading.Thread(target=animate, daemon=True)
t1.start()

ws.mainloop()