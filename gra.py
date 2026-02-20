#Copyright (c) 2026 Fff2468

#Ta gra jest własnością autora. 
#Nie wolno kopiować, rozpowszechniać ani używać gry w celach komercyjnych bez zgody autora.

#Wszystkie prawa zastrzeżone.

#game

import threading
import sys

def excepthook(args):
    # ignorujemy ValueError związane z signal w macOS
    if isinstance(args.exc_value, ValueError) and "signal only works in main thread" in str(args.exc_value):
        pass
    else:
        sys.__excepthook__(args.exc_type, args.exc_value, args.exc_traceback)

threading.excepthook = excepthook

import turtle
import random
import arcade
import sys
import os
import json
import tkinter as tk
from tkinter import simpledialog, messagebox

BASE_DIR = os.path.expanduser("~/gamekwadrat")
os.makedirs(BASE_DIR, exist_ok=True)
LOGIN_FILE = os.path.join(BASE_DIR, "login.json")

def save_login(username, password):
    with open(LOGIN_FILE, "w") as f:
        json.dump({"username": username, "password": password}, f)

def register_account(root):
    messagebox.showinfo("Rejestracja", "Nie znaleziono konta. Utwórz konto.", parent=root)
    username = simpledialog.askstring("Rejestracja", "Podaj nazwę użytkownika:", parent=root)
    password = simpledialog.askstring("Rejestracja", "Podaj hasło:", show="*", parent=root)
    save_login(username, password)
    return username, password

def login_account():
    root = tk.Tk()
    root.title("Logowanie")
    
    # ważne: root musi być widoczny do działania askstring
    root.geometry("200x100+500+300")
    root.update()  # odświeżenie okna
    
    if not os.path.exists(LOGIN_FILE):
        user, pwd = register_account(root)
        root.destroy()
        return user, pwd

    with open(LOGIN_FILE, "r") as f:
        data = json.load(f)
        saved_user = data.get("username")
        saved_pass = data.get("password")

    logged_in = False
    while not logged_in:
        username = simpledialog.askstring("Logowanie", "Podaj nazwę użytkownika:", parent=root)
        password = simpledialog.askstring("Logowanie", "Podaj hasło:", show="*", parent=root)

        if username == saved_user and password == saved_pass:
            messagebox.showinfo("Sukces", "Zalogowano pomyślnie!", parent=root)
            logged_in = True
        else:
            messagebox.showerror("Błąd", "Niepoprawny login lub hasło. Spróbuj ponownie.", parent=root)

    root.destroy()
    return username, password

# --------- START LOGOWANIA ---------
user, pwd = login_account()
print(f"Zalogowano: {user}")

# Teraz uruchamiasz Turtle/Arcade dopiero po zakończeniu logowania



BASE_DIR = os.path.expanduser("~/gamekwadrat")  # folder gry
os.makedirs(BASE_DIR, exist_ok=True)            # tworzy folder jeśli go nie ma

SAVE_FILE = os.path.join(BASE_DIR, "score.json")  # plik score w folderze gry

def save_score(score):
    with open(SAVE_FILE, "w") as f:
        json.dump({"score": score}, f)

def load_score():
    try:
        with open(SAVE_FILE, "r") as f:
            data = json.load(f)
            return data.get("score", 0)
    except FileNotFoundError:
        return 0

muzyka_player = None

lives = 3
points = 0  # licznik punktów
score = load_score()
level = 1
max_poziom = 4
ile_trzeba_do_mety = 150
game_active = True
teleport = False

ASE_DIR = os.path.dirname(os.path.abspath(__file__))
SOUNDS_DIR = os.path.join(BASE_DIR, "sounds")

# wczytywanie muzyki
muzyka2 = arcade.load_sound(os.path.join(SOUNDS_DIR, "coin.wav"))
muzyka = arcade.load_sound(os.path.join(SOUNDS_DIR, "gameover.wav"))
muzyka3 = arcade.load_sound(os.path.join(SOUNDS_DIR, "I_Win.wav"))
muzyka_w_tle = arcade.load_sound(os.path.join(SOUNDS_DIR, "zone1.wav"))

# Szybkie rysowanie
screen = turtle.Screen()
screen.bgcolor("black")
screen.title("Jumping Square")

napisFelix = turtle.Turtle()

napisFelix.showturtle()
napisFelix.goto(0, 60)
napisFelix.penup()
napisFelix.color("blue")
napisFelix.write("by Felix", align="center", font=("Arial", 30, "bold"))

run = turtle.Turtle()

run.hideturtle()
run.penup()
run.goto(0, -10)
run.color("green")
run.write("Press Space", align="center", font=("Arial", 50, "bold"))

screen.tracer(0, 0)  # wyłącza animacje, będzie szybciej

def game_run(): 
    global muzyka_player, kwadraty, przeszkody, monety, meta
    
    run.clear()
    napisFelix.clear()
    napisFelix.hideturtle()

    screen.update()

    screen.onkey(None, "space")

    muzyka_player4 = arcade.play_sound(muzyka_w_tle)
    
    monety = []
    
    hud = turtle.Turtle()
    hud.hideturtle()
    hud.penup()
    hud.color("white")
    hud.goto(-300, 250)
    hud.write(f"Lives: {lives}   Onions: {points}   Score: {score}", font=("Arial", 20, "normal"))
    
    def update_hud():
        hud.clear()
        hud.goto(-300, 250)
        hud.write(f"Lives: {lives}   Onions: {points}   Score: {score}", font=("Arial", 20, "normal"))
    
    # plansza: 1 = platforma, 0 = pusty
    platforma = [
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,'x',0,0,0,1],
        [0,0,0,'o',0,0,0,0,0,0,0,'x',0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,'x'],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,'o',0,0,0,1],
        [0,0,0,0,'x',0,0,0,0,0,0,'o',0,0,0,1,0,0,0,0,0,0,1,1,1,1,0,1,0,1,1,1,1,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,1,1,1,1,1,1,1],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,'o',1,1,1,1,1,1,1],
        [0,0,'x',0,0,0,0,0,0,0,0,0,0,0,'o',0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,1,1,1,1],
        [1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,0,0,0,0,0,1,1,1,0,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,'f'],
        [1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,'x',1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
        [1,'x',1,0,0,0,0,0,1,1,1,1,1,0,0,0,0,0,0,0,1],
        [0,0,0,0,0,0,0,0,0,'x',0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,'o',0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
        [0,'o',0,0,'o',0,0,0,0,0,0,0,0,0,'o',0,0,0,0,0,0,0,0,0,'o',0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,'x',0,0,0,1,1,1,1,0,1,0,1,1,1,1,0,0,0,0,0,0,0,0,0,0,1],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,1,1,1,1,1,1,1,0,'x',0,0,0,0,0,0,1],
        [0,0,0,0,'x',0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,0,1,1,1,1,1,1,1,0,0,0,0,0,0,1],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,1,1,1,1,0,0,0,0,'o',0,1],
        [1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,0,0,0,0,0,1,1,1,0,1,1,1,1,1,1,1,1,1,1,0,0,0,0,1,0,0,0,0,0,0,0,0,'o',0,0,0,0,0,0,0,0,'o','o','o'],
        [1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
        [1,1,1,0,0,0,0,0,1,1,1,1,1,0,0,0,0,0,0,0,1]
    ]
    
    # rozmiar kwadratu
    kwadrat = 20
    
    # lista wszystkich kwadratów
    kwadraty = []
    
    # rysowanie platform
    kwadraty = []
    przeszkody = []
    
    meta = None 
    
    for y, row in enumerate(platforma):
        for x, val in enumerate(row):
            if val == 1:
                k = turtle.Turtle()
                k.shape("square")
                k.color("white")
                k.penup()
                k.speed(0)
                k.goto(x*kwadrat, -y*kwadrat)
                kwadraty.append(k)
            elif val == 'x':
                o = turtle.Turtle()
                o.shape("triangle")      # trujkąt
                o.color("grey")        # szare
                o.penup()
                o.speed(0)
                o.setheading(0)  # domyślnie w prawo
                o.tilt(90)       # obracamy o 90° w prawo, żeby kolce wyglądały "do góry
                o.goto(x*kwadrat, -y*kwadrat)
                przeszkody.append(o)
                
            elif val == 'o':
                # moneta
                m = turtle.Turtle()
                m.shape("circle")
                m.color("yellow")
                m.penup()
                m.speed(0)
                m.goto(x*kwadrat, -y*kwadrat)
                monety.append(m)       
            
            elif val == 'f':
                meta = turtle.Turtle()
                meta.shape("square")
                meta.color("blue")
                meta.shapesize(stretch_wid=2, stretch_len=1)  # np. większy prostokąt
                meta.penup()
                meta.goto(x*kwadrat, -y*kwadrat)   
                meta.showturtle()
    
    screen.update()
    
    # gracz
    gracz = turtle.Turtle()
    gracz.shape("square")
    gracz.color("blue")
    gracz.penup()
    gracz.speed(0)
    gracz.goto(100, 0)
    gracz.dy = 0  # prędkość w pionie
    
    def lose_life():
        global lives, game_active, muzyka_player
    
        lives -= 1
    
        hud.clear()
        hud.write(f"Lives: {lives}   Onions: {points}   Score: {score}", font=("Arial", 20, "normal"))
    
        if lives == 0 or lives < 0:
            hud.goto(0, 0)
            hud.write("GAME OVER", align="center", font=("Arial", 50, "bold"))
            game_active = False
            gracz.hideturtle()
            muzyka_player = arcade.play_sound(muzyka)   
            return
    
        # cofnięcie gracza na start
        gracz.goto(0, 100)
        gracz.dy = 0
        
    def wygrana():
        global game_active
        
        komunikat = turtle.Turtle()
        komunikat.hideturtle()
        komunikat.color("green")
        komunikat.penup()
        game_active = False
        gracz.hideturtle()
        komunikat.goto(0, 0)
        komunikat.write("You Win!!!", align="center", font=("Arial", 50, "bold")) 
        muzyka_player3 = arcade.play_sound(muzyka3)
        
    def przejdz_do_nastepnego_poziomu():
        global kwadraty, przeszkody, monety, meta, platforma, level, teleport, ile_trzeba_do_mety
    
        # usuń stare elementy
        for k in kwadraty:
            k.hideturtle()
            
        for o in przeszkody:
            o.hideturtle()
            
        for m in monety:
            m.hideturtle()
            
        if meta:
            meta.hideturtle()
    
        kwadraty = []
        przeszkody = []
        monety = []
        meta = None
        
        # zmień zawartość platforma w zależności od poziomu
        if level == 2:
       
            platforma = [
                [0,0,0,0,0,0,0,0,0,0,0,'f'],
                [0,0,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,'o',0,0,0,0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,'o','o','o','o','o','o','o'],
                [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,'o','o','o','o','o','o','o'],
                [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1],
                [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,'o','o','o','o','o','o','o'],
                [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1],
                [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1],
                [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1],
                [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,0,0,1,1,1,1,1,1,1,1,1,0,0,0,00,0,0,0,0],
                [0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,'o',0,0,0,'o','o',0,0,0,0,1],
                [0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,'x',0,0,0,0,0,0,'o','o',0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,'o','o','o','o','o',0,'o'],
                [0,0,0,0,0,0,0,1,'x','x','x','x','x',0,0,0,0,0,0,0,0,0,0,'o','o',0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,'x',1],
                [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
                
            ]
            
            gracz.goto(50, 100)
            gracz.dy = 0
            ile_trzeba_do_mety = 500
            
            teleport = True  # oznacza, że gracz został teleportowany
            
        elif level == 3:
            gracz.goto(50, 100)
            gracz.dy = 0
            ile_trzeba_do_mety = 820
            
            platforma = [
                [0,'f',0,0,0,0,'o','o',0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,'o'],
                [0,1,1,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,'o'],
                [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,'o','o','o','o','o','o','o','o','o'],
                [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,0,1,1,1,1],
                [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,'x','o','o','o','x','o','o','o','o','o','x','x','x',1,1,1,'o','o','o','o',1],
                [1,1,1,1,1,1,1,1,1,1,1,'o','o',1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                ['o','o','o','o','o',0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                [1,1,1,1,1,1,1,1,1,1,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
            
            ]
        
        elif level == 4:
            gracz.goto(50, 100)
            gracz.dy = 0
            ile_trzeba_do_mety = 990
            
            platforma = [
                
                ['f','o','o','o','o'],
                [1,1,1,0,0,0,0,1,0,0],
                [0,0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,'x','o','x'],
                [0,0,0,0,0,0,1,1,1,1],
                [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,'o'],
                [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                ['x','o','x',0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                [1,1,0,0,1,1,1,1,1,1,1,0,0,0,1,0,0,0,1],
                ['o','o','o','o','o','o','o','o','o','o',0,0,0,0,0,0,0,0,0,0,0,0],
                [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
            
            ]       
    
        gracz.dy = 0
        
        for y, row in enumerate(platforma):
            for x, val in enumerate(row):
                if val == 1:
                    k = turtle.Turtle()
                    k.shape("square")
                    k.color("white")
                    k.penup()
                    k.speed(0)
                    k.goto(x*kwadrat, -y*kwadrat)
                    kwadraty.append(k)
    
                elif val == 'x':
                    o = turtle.Turtle()
                    o.shape("triangle")
                    o.color("grey")
                    o.penup()
                    o.speed(0)
                    o.setheading(0)  # domyślnie w prawo
                    o.tilt(90)       # obracamy o 90° w prawo, żeby kolce wyglądały "do góry
                    o.goto(x*kwadrat, -y*kwadrat)
                    przeszkody.append(o)
    
                elif val == 'o':
                    m = turtle.Turtle()
                    m.shape("circle")
                    m.color("yellow")
                    m.penup()
                    m.speed(0)
                    m.goto(x*kwadrat, -y*kwadrat)
                    monety.append(m)
    
                elif val == 'f':
                    meta = turtle.Turtle()
                    meta.shape("square")
                    meta.color("blue")
                    meta.shapesize(stretch_wid=2, stretch_len=1)
                    meta.penup()
                    meta.goto(x*kwadrat, -y*kwadrat)
    
     # i tu analogicznie rysujesz mapę jak wcześniej    
    def move_left():
        step = 20
        # sprawdzamy kolizję tylko z platformami i przeszkodami
        for k in kwadraty + przeszkody:
            if abs((k.xcor() + step) - gracz.xcor()) < kwadrat and abs(k.ycor() - gracz.ycor()) < kwadrat:
                return  # nie ruszamy się w lewo, bo byłaby kolizja
        # przesuwamy mapę w prawo (gracz stoi w miejscu)
        for k in kwadraty + przeszkody + monety + ([meta] if meta else []):
            k.setx(k.xcor() + step)
        screen.update()
    
    def move_right():
        step = 20
        for k in kwadraty + przeszkody:
            if abs((k.xcor() - step) - gracz.xcor()) < kwadrat and abs(k.ycor() - gracz.ycor()) < kwadrat:
                return  # blokujemy ruch w prawo
        for k in kwadraty + przeszkody + monety + ([meta] if meta else []):
            k.setx(k.xcor() - step)
        screen.update()
    
    # skok tylko z podłoża
    
    def jump():
        podloze = False
        for k in kwadraty:
            if abs(k.xcor() - gracz.xcor()) < kwadrat:
                # jeśli gracz stoi lub lekko nad platformą
                if 0 <= gracz.ycor() - (k.ycor() + kwadrat) <= 10:
                    podloze = True
                    break
        if podloze:
           gracz.dy = 15
    # grawitacja
    def gravity():
        global points, level, game_active, teleport, score, muzyka_player  # dodajemy global, żeby móc zwiększać punkty
            
        if not game_active:
            return
        
        if teleport:
            teleport = False
            gracz.sety(gracz.ycor())
    
        gracz.dy -= 1
        gracz.sety(gracz.ycor() + gracz.dy)
    
        # kolizja z platformą (tylko kwadraty!)
        for k in kwadraty:
            if abs(k.xcor() - gracz.xcor()) < kwadrat:
                if gracz.dy <= 0:  # spada w dół
                # jeśli gracz wleciał w platformę lub jest na niej
                    if k.ycor() <= gracz.ycor() <= k.ycor() + kwadrat:
                        gracz.sety(k.ycor() + kwadrat)
                        gracz.dy = 0
                        break
                    
        for o in przeszkody:
            if abs(o.xcor() - gracz.xcor()) < kwadrat and abs(o.ycor() - gracz.ycor()) < kwadrat:
                lose_life()
                break
            
        for m in monety:
            if abs(m.xcor() - gracz.xcor()) < kwadrat and abs(m.ycor() - gracz.ycor()) < kwadrat:
                points += 10
                score += 10
                save_score(score)
                update_hud()
                m.hideturtle()           # znika wizualnie
                monety.remove(m)         # usuwa z listy, żeby nie liczyło się dalej
                muzyka_player = arcade.play_sound(muzyka2)   
                break
        # zamiast kwadrat/2 używamy kwadrat
        if meta and abs(gracz.xcor() - meta.xcor()) < kwadrat and abs(gracz.ycor() - meta.ycor()) < kwadrat and points >= ile_trzeba_do_mety:
            if level >= max_poziom:
                wygrana()
                return
            else:
                level += 1
                score += 100
                save_score(score)
                update_hud()
                gracz.dy = 0
                
                przejdz_do_nastepnego_poziomu()
    
        screen.update()
        screen.ontimer(gravity, 50)
    
    screen.listen()
    screen.onkey(move_left, "Left")
    screen.onkey(move_right, "Right")
    screen.onkey(jump, "z")
    
    gravity()
    screen.mainloop()

screen.listen()
screen.onkey(game_run, "space")
screen.mainloop()

