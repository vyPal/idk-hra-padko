import os
import json
import keyboard
from colorama import init
from colorama import Fore, Back, Style
import sys
import time
import random
from multiprocessing import Process, Value

init( autoreset = True)

main_script = None
other_scripts = {}
maps = {}
il = {}

try:
    with open("./main.vgs") as f:
        main_script = json.loads(f.read())
        f.close()
except:
    print("ERROR: File './main.vgs' was not found.")

def scriptLoaded(id):
    if id == "main":
        return True
    else:
        if id in other_scripts:
            return True
        else:
            return False

def mapLoaded(id):
    if id in maps:
        return True
    else:
        return False

def ilLoaded(id):
    if id in il:
        return True
    else:
        return False

def sceneExists(id):
    if id.startswith("main:"):
        if main_script[id[5:]]:
            return True
        else:
            return False
    else:
        id2 = id.split(":")
        if other_scripts[id2[0]][id2[1]]:
            return True
        else:
            return False

def loadScript(id):
    try:
        with open("./"+id+".vgs") as f:
            other_scripts[id] = json.loads(f.read())
            f.close()
    except:
        print("ERROR: File './"+id+".vgs' was not found.")

def loadMap(id):
    try:
        with open("./"+id+".vgm") as f:
            maps[id] = f.read().split("\n")
            f.close()
    except:
        print("ERROR: File './"+id+".vgm' was not found.")

def loadIl(id):
    try:
        with open("./"+id+".vgi") as f:
            temp = f.read()
            temp = temp.replace(" ",Back.BLACK+" "+Back.BLACK)
            temp = temp.replace("R",Back.RED+" "+Back.BLACK)
            temp = temp.replace("G",Back.GREEN+" "+Back.BLACK)
            temp = temp.replace("B",Back.BLUE+" "+Back.BLACK)
            temp = temp.replace("C",Back.CYAN+" "+Back.BLACK)
            temp = temp.replace("M",Back.MAGENTA+" "+Back.BLACK)
            temp = temp.replace("Y",Back.YELLOW+" "+Back.BLACK)
            temp = temp.replace("W",Back.WHITE+" "+Back.BLACK)
            il[id] = temp.split("\n")
            f.close()
    except:
        print("ERROR: File './"+id+".vgi' was not found.")

def script(id):
    if id == "main":
        return main_script
    else:
        if not scriptLoaded(id):
            loadScript(id)
        return other_scripts[id]

def gameMap(id):
    if not mapLoaded(id):
        loadMap(id)
        return maps[id]
    else:
        return maps[id]

def illustration(id):
    if not ilLoaded(id):
        loadIl(id)
        return il[id]
    else:
        return il[id]

def scene(id):
    return script(id[0:4])[id[5:]]

def execScene(id):
    sceneToExec = scene(id)

def move (y, x):
    sys.stdout.write("\033[%d;%dH" % (y, x))

def size_border():
    os.system('cls' if os.name == 'nt' else 'clear')
    width = script("main")["konzole"]["sloupce"]
    height = script("main")["konzole"]["řádky"]
    text = script("main")["konzole"]["zpráva_o_velikosti"]
    text_input = script("main")["konzole"]["input"]
    if len(text)>(width-4):
        stext=text.split(" ")
        #print(stext)
        ntext=""
        for i in range(0,int(len(text)/(width-8)+1)):
            ntext+=" ".join(stext[int(len(stext)/int(len(text)/(width-8)+1)*i):int((len(stext)/int(len(text)/(width-8)+1)*i)+len(stext)/int(len(text)/(width-8)+1))]).center(width)
            if i != int(len(text)/(width-8)+1):
                ntext += "\n"
        
        move((height/2)-int(len(text)/(width-8)+1)/4, 0)
        sys.stdout.write(ntext+"\n")
        move((height/2)-int(len(text)/(width-8)+1)/4+2, 0)
        sys.stdout.write((Back.WHITE+Fore.BLACK+"<"+text_input+">"+Style.RESET_ALL).center(width+len(Back.WHITE+Fore.BLACK+Style.RESET_ALL))+"\n")
    else:
        move(height/2-1, 0)
        sys.stdout.write(text.center(width)+"\n")
        move(height/2+1, 0)
        sys.stdout.write((Back.WHITE+Fore.BLACK+"<"+text_input+">"+Style.RESET_ALL).center(width+len(Back.WHITE+Fore.BLACK+Style.RESET_ALL))+"\n")
    for i in range(0,width+1):
        move(0, i)
        sys.stdout.write(Back.WHITE+" "+"\n"+Back.BLACK)
        move(height, i)
        sys.stdout.write(Back.WHITE+" "+"\n"+Back.BLACK)
    for i in range(0,height+1):
        move(i,0)
        sys.stdout.write(Back.WHITE+" "+"\n"+Back.BLACK)
        move(i, width)
        sys.stdout.write(Back.WHITE+" "+"\n"+Back.BLACK)
    keyboard.wait("space")

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def border():
    width = script("main")["konzole"]["sloupce"]
    height = script("main")["konzole"]["řádky"]
    for i in range(0,width+1):
        move(0, i)
        sys.stdout.write(Back.WHITE+" "+"\n"+Back.BLACK)
        move(height, i)
        sys.stdout.write(Back.WHITE+" "+"\n"+Back.BLACK)
    for i in range(0,height+1):
        move(i,0)
        sys.stdout.write(Back.WHITE+" "+"\n"+Back.BLACK)
        move(i, width)
        sys.stdout.write(Back.WHITE+" "+"\n"+Back.BLACK)

def intro():
    if "intro" in script("main"):
        ill = illustration(script("main")["intro"])
        sys.stdout.write("\n".join(ill)+"\n")
        keyboard.wait("space")


x=0
y=0
ps=1
p=""
rd=1
oldscr=[]

def renderMap(sc):
    global x
    global y
    global ps
    global p
    global rd
    global oldscr
    width = script("main")["konzole"]["sloupce"]
    height = script("main")["konzole"]["řádky"]
    #for i in range(0,ps):
    #    p+=Back.YELLOW
    #    for j in range(0,ps+1):
    #        p+=" "
    #    p+="\n"
    #clear()
    for j in range(0-rd*2, rd*2):
        for i in range(0-rd, rd):
            chars=["!", "_", "?", ".", ",", ")", "*", ">"]
            temp2=" "
            temp=Back.BLACK
            if x+i<0:
                temp=Back.CYAN
            elif x+i>len(gameMap(sc["mapa"])):
                temp=Back.CYAN
            elif y+j<0:
                temp=Back.CYAN
            elif y+j>len(gameMap(sc["mapa"])[x+i-1]):
                temp=Back.CYAN
            elif gameMap(sc["mapa"])[x+i-1][y+j-1] == "█":
                temp=Back.WHITE
            if (i==0 and j==0) or (i==0 and j==1):
                temp=Back.YELLOW
            if random.randint(0,500) == 50:
                temp2=chars[random.randint(0,len(chars)-1)]
            move(height/2+i, width/2+j)
            sys.stdout.write(temp+temp2+"\n")
    #move(height/2,width/2)
    #print(p)
    #border()

di=None
didone=False
dicycle=0
dicontdel=5
diline=0

def renderDialog(sc):
    global didone
    if "dialogy" in sc and "dialog" in sc and not didone:
        global di
        global dicycle
        global diline
        if di == None:
            di = sc["dialog"]
        dia = sc["dialogy"][di]
        odd = sc["dialogy"]["oddělovač"]
        width = script("main")["konzole"]["sloupce"]
        move(25,5)
        for i in dia["text"][0:dicycle]:
            if i=="|":
                diline+=1
                move(25+diline, 5)
            else:
                sys.stdout.write(i)
        if dicycle<len(dia["text"]):
            dicycle+=1
            diline=0
        else:
            dicycle=0
            diline=0
            didone=True
            move(25+diline+2,0)
            sys.stdout.write(odd.center(width)+"\n")
            border()

def loadFirstScene():
    if "mapa" in scene("main:start"):
        renderMap(scene("main:start"))
    else:
        sys.stdout.write("No"+"\n")

nextdia=Value('i', 0)

def dialogManager(data):
    global di
    global didone
    global dicycle
    nextdia=data.value
    while True:
        renderDialog(scene("main:start"))
        if didone:
            if nextdia == 1:
                nextdia = 0
                didone = False
                di = scene("main:start")["dialogy"][di]["next"]
        time.sleep(0.05)

diproc = Process(target=dialogManager, args=(nextdia,))

def manager():
    global x
    global y
    global diproc
    global nextdia
    #diproc.start()
    while True:
        height = script("main")["konzole"]["řádky"]
        move(height,0)
        key = keyboard.read_key()
        move(height,0)
        sys.stdout.write(Back.WHITE+Fore.WHITE+"              \n")
        move(height,0)
        if key == "right":
            if gameMap(scene("main:start")["mapa"])[x-1][y+1] != "█":
                y+=2
                renderMap(scene("main:start"))
        if key == "left":
            if gameMap(scene("main:start")["mapa"])[x-1][y-2] != "█":
                y-=2
                renderMap(scene("main:start"))
        if key == "down":
            if gameMap(scene("main:start")["mapa"])[x+1][y-2] != "█":
                x+=1
                renderMap(scene("main:start"))
        if key == "up":
            if gameMap(scene("main:start")["mapa"])[x-2][y-1] != "█":
                x-=1
                renderMap(scene("main:start"))
        if key == "space":
            nextdia.value = 1

def start():
    #intro()
    size_border()
    clear()
    border()
    global x
    global y
    global ps
    global p
    global rd
    global oldscr
    x=scene("main:start")["startx"]
    y=scene("main:start")["starty"]
    ps=scene("main:start")["player_size"]
    p=""
    rd=scene("main:mapy")["render_distance"]
    for i in range(rd*2+1):
        temp=[]
        for j in range(rd*2+1):
            temp.append("0")
        oldscr.append(temp)
    loadFirstScene()
    manager()

start()