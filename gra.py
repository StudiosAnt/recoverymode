import turtle
import random

lives = 3
points = 0  # licznik punktów
score = 0
level = 1
max_poziom = 4
ile_trzeba_do_mety = 150
game_active = True
teleport = False

# Szybkie rysowanie
screen = turtle.Screen()
screen.bgcolor("black")
screen.tracer(0, 0)  # wyłącza animacje, będzie szybciej
screen.title("Jumping Square Pro")

monety = []

hud = turtle.Turtle()
hud.hideturtle()
hud.penup()
hud.color("white")
hud.goto(-300, 250)
hud.write(f"Życia: {lives}", font=("Arial", 20, "normal"))

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
    global lives, game_active

    lives -= 1

    hud.clear()
    hud.write(f"Życia: {lives}", font=("Arial", 16, "normal"))

    if lives == 0 or lives < 0:
        hud.goto(0, 0)
        hud.write("GAME OVER", align="center", font=("Arial", 50, "bold"))
        game_active = False
        gracz.hideturtle()
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
    komunikat.write("WYGRAŁEŚ!", align="center", font=("Arial", 50, "bold"))    
    
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
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
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
    global points, level, game_active, teleport, score  # dodajemy global, żeby móc zwiększać punkty
        
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
            update_hud()
            m.hideturtle()           # znika wizualnie
            monety.remove(m)         # usuwa z listy, żeby nie liczyło się dalej
            break
    # zamiast kwadrat/2 używamy kwadrat
    if meta and abs(gracz.xcor() - meta.xcor()) < kwadrat and abs(gracz.ycor() - meta.ycor()) < kwadrat and points >= ile_trzeba_do_mety:
        if level >= max_poziom:
            wygrana()
            return
        else:
            level += 1
            score += 100
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
