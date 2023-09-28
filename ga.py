import curses
import threading
# import asyncio

stdscr = curses.initscr()
curses.curs_set(0)
curses.noecho()
curses.cbreak()
stdscr.keypad(True)

heroDataLatest = [20, 50, "____"]
enemyDataLatest = [4, 4, "enem"]
enemyHitboxLatest = []
enemyAlive = False
enemyHitboxDraw = False
noBullet = True
bullets = []
hitArea = []
changeInHitArea = False


def blueMoon(heroData=None):  # mapData first
    global heroDataLatest, enemyDataLatest, enemyAlive, enemyHitboxDraw, enemyHitboxLatest
    stdscr.clear()
    if heroData == None:
        heroData = heroDataLatest
    else:
        heroDataLatest = heroData

    if enemyAlive:
        y, x, txt = enemyDataLatest
        dummyA = 0
        for a in enemyDataLatest[2]:
            stdscr.addstr(y + dummyA, x, a)
            dummyA = dummyA + 1

    if enemyHitboxDraw:
        y, x, txt = enemyHitboxLatest
        stdscr.addstr(y, x, txt)

    if not noBullet:
        for muda in bullets:
            y, x, txt = muda
            stdscr.addstr(y, x, txt)

    y, x, txt = heroData
    stdscr.addstr(y, x, txt)

    stdscr.refresh()


class enems:
    packetToSend = []

    def __init__(self, hp, hpBoxes, y, x, sprite, hpXoffset=3, hpYoffset=1, frozen=[]):
        global hitArea, changeInHitArea
        self.hp = hp
        self.curHP = hp
        self.hpBoxes = hpBoxes
        self.y = y
        self.x = x
        self.frozen = frozen
        self.sprite = sprite
        self.hpYoffset = self.y - hpYoffset
        self.hpXoffset = self.x + hpXoffset
        tempest = len(max(sprite))
        tampermonkey = len(sprite)
        hitArea = [[self.x, self.x + tempest], [self.y, self.y + tampermonkey]]
        changeInHitArea = True

    def spawn(self):
        global enemyAlive, enemyHitboxDraw, enemyDataLatest, enemyHitboxLatest
        enemyAlive = True
        enemyHitboxDraw = True
        enemyDataLatest = [self.y, self.x, self.sprite]
        enemyHitboxLatest = [self.hpYoffset, self.hpXoffset, "■"*self.hpBoxes]
        blueMoon()

        if not self.frozen:
            self.updateEenemy()

    def updateEenemy(self):  # 5 line and wide
        global stoneFree
        stoneFree = True

    def enemyHitAction(self, heroDmg):
        global enemyHitboxDraw, enemyAlive, enemyHitboxLatest
        self.curHP = self.curHP - heroDmg
        if self.curHP <= 0:
            enemyHitboxDraw = False
            enemyAlive = False
        else:
            x = round((self.curHP/self.hp)*(self.hpBoxes))
            toPrint = "■"*x + "□"*(self.hpBoxes - x)
            enemyHitboxLatest = [self.hpYoffset, self.hpXoffset, toPrint]
            blueMoon()


x = 50
dio = enems(240, 20, 10, 40, ("▒▒▒▒▒▒▐███████▌", "▒▒▒▒▒▒▐░▀░▀░▀░▌",
            "▒▒▒▒▒▒▐▄▄▄▄▄▄▄▌", "▄▀▀▀█▒▐░▀▀▄▀▀░▌▒█▀▀▀▄", "▌▌▌▌▐▒▄▌░▄▄▄░▐▄▒▌▐▐▐▐"), 6, 2)
dio.spawn()


def gameUpdates():
    t = threading.Timer(0.1, gameUpdates)
    t.daemon = True
    t.start()
    global bullets, noBullet, changeInHitArea, hitArea, enemyHitboxLatest, enemyDataLatest
    if not noBullet:
        newBullets = []
        for muda in bullets:
            y, x, txt = muda
            y = y - 1
            if changeInHitArea:
                global xmin, xmax, ymin, ymax
                changeInHitArea = False
                xmin, xmax = hitArea[0]  # x
                ymin, ymax = hitArea[1]  # y

            if xmin <= x <= xmax and ymin <= y <= ymax and enemyAlive:
                dio.enemyHitAction(30)
            elif y >= 0:
                newBullets.append([y, x, txt])
        bullets = newBullets
        if not bullets:
            noBullet = True
        blueMoon()

    if enemyAlive and stoneFree:
        y, x, z = enemyDataLatest
        if 20 > x:
            x = x + 1
            enemyDataLatest = [y, x, z]
            changeInHitArea = True
        else:
            x = x - 1
            enemyDataLatest = [y, x, z]
            changeInHitArea = True
        blueMoon()


gameUpdates()

while True:

    givenIn = stdscr.getch()

    if givenIn == curses.KEY_RIGHT:
        if curses.COLS > x + 3:
            x = x + 2
            blueMoon(heroData=[20, x, "____"])
        else:
            pass

    elif givenIn == curses.KEY_LEFT:
        if x - 2 >= 0:
            x = x - 2
            blueMoon(heroData=[20, x, "____"])

    elif givenIn == curses.KEY_UP:
        bullets.append([19, x, "¤"])
        noBullet = False

    elif givenIn == ord(" "):
        bullets.append([19, x, "¤"])
        noBullet = False

    elif givenIn == ord("q"):
        break
    elif givenIn == curses.KEY_END:
        break

curses.endwin()
print("goodbye jojo")
