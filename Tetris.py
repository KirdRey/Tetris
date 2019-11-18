from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys
import random
import sqlite3


class game(QMainWindow):
    def __init__(self):
        super().__init__()
        self.speed = 600
        self.initUI()
        self.pole = []
        self.pole1 = []
        self.figures = [[[4, 0], [5, 0], [4, 1], [5, 1]],
                   [[4, 0], [4, 1], [4, 2], [4, 3]],
                   [[4, 0], [3, 0], [3, 1], [2, 1]],
                   [[4, 0], [5, 0], [5, 1], [6, 1]],
                   [[4, 0], [4, 1], [3, 1], [2, 1]],
                   [[4, 0], [4, 1], [5, 1], [6, 1]],
                   [[4, 0], [3, 1], [5, 1], [4, 1]]]
        self.createpole()
        self.fig = ['o', 'i', 's', 'z', 'l', 'j', 't']
        self.curfig = ''
        self.figpos = []
        self.minx, self.miny, self.maxx, self.maxy = 0, 0, 0, 0
        self.perevorotfig = 0
        self.deletedlines = 0
        self.score = 0
        self.nextfig = random.choice(self.fig)
        self.buttoncolours = ['#FF00FF', '#800080', '#FF0000', '#800000',
                              '#008000', '#808000', '#0000FF']
        self.pausegame = False
        self.board = []

        con = sqlite3.connect('Tetris.db')
        cur = con.cursor()
        result1 = cur.execute("""SELECT score, name FROM Tetris""").fetchall()
        for elem in result1:
            self.board.append(elem)
        self.board = list(reversed(sorted(self.board)))
        for i in range(len(self.board)):
            self.scoreboard.setItem(i, 0, QTableWidgetItem(str(self.board[i][1])))
            self.scoreboard.setItem(i, 1, QTableWidgetItem(str(self.board[i][0])))
        con.commit()
        con.close()

    def initUI(self):
        self.setGeometry(900, 100, 800, 600)
        self.setWindowTitle('GAME')

        self.start = QPushButton(f'Начать новую игру', self)
        self.start.resize(120, 40)
        self.start.move(50, 10)
        self.start.clicked.connect(self.startgame)

        self.pausa = QPushButton(f'Пауза', self)
        self.pausa.resize(120, 40)
        self.pausa.move(50, 90)
        self.pausa.clicked.connect(self.pause)
        self.pausa.setEnabled(False)

        self.save = QPushButton(f'Сохранить игру', self)
        self.save.resize(120, 40)
        self.save.move(520, 10)
        self.save.clicked.connect(self.savegame)

        self.load = QPushButton(f'Загрузить игру', self)
        self.load.resize(120, 40)
        self.load.move(660, 10)
        self.load.clicked.connect(self.loadgame)


        self.rules = QLabel(self)
        self.rules.setText("Правила:\n+1 уровень за 3 убранные линии\n"
                           "ОДНА линия - 100 очков\n"
                           "ДВЕ линии - 300 очков\n"
                           "ТРИ линии - 600 очков\n"
                           "ЧЕТЫРЕ линии - 1000 очков\n"
                           "Проигрыш - фигура на первом ряду\n"
                           "При проигрыше заполните имя\n\n"
                           "Управление:\n"
                           "А - влево, D - вправо\n"
                           "S - вниз,  W - переворот\n\n"
                           "Удачи!")
        self.rules.resize(200, 300)
        self.rules.move(10, 270)

        self.label = QLabel(self)
        self.label.setText("Очки:")
        self.label.move(80, 160)

        self.scoreLCD = QLCDNumber(self)
        self.scoreLCD.move(60, 190)

        self.label1 = QLabel(self)
        self.label1.setText("Уровень:")
        self.label1.move(80, 240)

        self.scoreLCD2 = QLCDNumber(self)
        self.scoreLCD2.move(60, 270)

        self.label2 = QLabel(self)
        self.label2.setText("Следующая фигура:")
        self.label2.resize(130, 30)
        self.label2.move(600, 50)

        self.scoreboard = QTableWidget(self)
        self.scoreboard.move(540, 240)
        self.scoreboard.resize(224, 327)
        self.scoreboard.setRowCount(10)
        self.scoreboard.setColumnCount(2)
        self.scoreboard.setEnabled(False)

    def save_results(self, name):
        con = sqlite3.connect('Tetris.db')
        cur = con.cursor()
        result = cur.execute(f'insert into Tetris(name, score) values("{name}", {self.score})')
        self.board.append((self.score, name))
        self.board = list(reversed(sorted(self.board)))
        for i in range(len(self.board)):
            self.scoreboard.setItem(i, 0, QTableWidgetItem(str(self.board[i][1])))
            self.scoreboard.setItem(i, 1, QTableWidgetItem(str(self.board[i][0])))
        con.commit()
        con.close()

    def savegame(self):
        q = []
        q.append(self.speed)
        q.append(self.pole)
        q.append(self.pole1)
        q.append(self.curfig)
        q.append(self.figpos)
        q.append([self.minx, self.miny, self.maxx, self.maxy])
        q.append(self.perevorotfig)
        q.append(self.deletedlines)
        q.append(self.score)
        q.append(self.nextfig)
        q.append(self.pausegame)
        q.append(self.board)
        q = str(q)
        con = sqlite3.connect('Tetris.db')
        cur = con.cursor()
        result = cur.execute(f'insert into safeload(lastgame) values("{q}")')
        con.commit()
        con.close()

    def loadgame(self):
        q = 0
        con = sqlite3.connect('Tetris.db')
        cur = con.cursor()
        q = cur.execute("""SELECT lastgame FROM safeload""").fetchall()
        con.commit()
        con.close()
        q = eval(q[-1][0])
        self.speed = q[0]
        self.pole = q[1]
        self.pole1 = q[2]
        self.curfig = q[3]
        self.figpos = q[4]
        self.minx, self.miny, self.maxx, self.maxy = q[5][0], q[5][1], q[5][2], q[5][3]
        self.perevorotfig = q[6]
        self.deletedlines = q[7]
        self.score = q[8]
        self.nextfig = q[9]
        self.pausegame = q[10]
        self.board = q[11]
        self.level()
        self.nextfigbuild()

    def startgame(self):
        self.start.setEnabled(False)
        self.pausa.setEnabled(True)
        self.reloadgame()
        self.startigra = True
        self.timer = QTimer()
        self.timer.timeout.connect(self.turn)
        self.speed = 600
        self.deletedlines = 0
        self.score = 0
        self.nextfig = random.choice(self.fig)
        self.timer.start(self.speed)
        self.curfig = ''
        self.figpos = []
        self.pausegame = False

    def reloadgame(self):
        self.pole.clear()
        self.pole1.clear()
        for i in range(10):
            for j in range(20):
                exec(f'self.btn{str(i) + str(0) + str(j)}.setStyleSheet("background-color: #FFFFFF")')
        for i in range(5):
            for j in range(4):
                exec(f'self.btn{str(i) + str(111) + str(j)}.setStyleSheet("background-color: #FFFFFF")')
        for i in range(20):
            pole1 = []
            for j in range(10):
                pole1.append('O')
            self.pole.append(pole1)
        for i in range(3):
            pole1 = []
            for i in range(4):
                pole1.append('O')
            self.pole1.append(pole1)

    def pause(self):
        if not self.pausegame:
            self.timer.stop()
            self.pausegame = True
        else:
            self.timer.start(self.speed)
            self.pausegame = False

    def createpole(self):
        for i in range(10):
            for j in range(20):
                exec(f'self.btn{str(i) + str(0) + str(j)} = QPushButton(self)')
                exec(f'self.btn{str(i) + str(0) + str(j)}.resize(30, 30)')
                exec(f'self.btn{str(i) + str(0) + str(j)}.move({i * 30 + 200}, {j * 30})')
                exec(f'self.btn{str(i) + str(0) + str(j)}.setEnabled(False)')
                exec(f'self.btn{str(i) + str(0) + str(j)}.setStyleSheet("background-color: #FFFFFF")')
                exec(f'self.btn{str(i) + str(0) + str(j)}.show()')
        for i in range(5):
            for j in range(4):
                exec(f'self.btn{str(i) + str(111) + str(j)} = QPushButton(self)')
                exec(f'self.btn{str(i) + str(111) + str(j)}.resize(30, 30)')
                exec(f'self.btn{str(i) + str(111) + str(j)}.move({i * 30 + 580}, {j * 30 + 80})')
                exec(f'self.btn{str(i) + str(111) + str(j)}.setEnabled(False)')
                exec(f'self.btn{str(i) + str(111) + str(j)}.setStyleSheet("background-color: #FFFFFF")')
                exec(f'self.btn{str(i) + str(111) + str(j)}.show()')
        for i in range(20):
            pole1 = []
            for j in range(10):
                pole1.append('O')
            self.pole.append(pole1)
        for i in range(3):
            pole1 = []
            for i in range(4):
                pole1.append('O')
            self.pole1.append(pole1)

    def keyPressEvent(self, event):
        if not self.pausegame:
            if event.key() == Qt.Key_D:
                self.dash('>')
            elif event.key() == Qt.Key_A:
                self.dash('<')
            elif event.key() == Qt.Key_S:
                self.dash('v')
            elif event.key() == Qt.Key_W:
                self.dash('/')

    def createfigure(self, figure):
        if figure == 'o':
            self.figpos = [[4, 0], [5, 0], [4, 1], [5, 1]]
            self.minx, self.miny, self.maxx, self.maxy = 4, 0, 5, 1
        elif figure == 'i':
            self.figpos = [[4, 0], [4, 1], [4, 2], [4, 3]]
            self.minx, self.miny, self.maxx, self.maxy = 4, 0, 4, 3
        elif figure == 's':
            self.figpos = [[4, 0], [3, 0], [3, 1], [2, 1]]
            self.minx, self.miny, self.maxx, self.maxy = 2, 0, 4, 1
        elif figure == 'z':
            self.figpos = [[4, 0], [5, 0], [5, 1], [6, 1]]
            self.minx, self.miny, self.maxx, self.maxy = 4, 0, 6, 1
        elif figure == 'l':
            self.figpos = [[4, 0], [4, 1], [3, 1], [2, 1]]
            self.minx, self.miny, self.maxx, self.maxy = 2, 0, 4, 1
        elif figure == 'j':
            self.figpos = [[4, 0], [4, 1], [5, 1], [6, 1]]
            self.minx, self.miny, self.maxx, self.maxy = 4, 0, 6, 1
        elif figure == 't':
            self.figpos = [[4, 0], [3, 1], [5, 1], [4, 1]]
            self.minx, self.miny, self.maxx, self.maxy = 3, 0, 5, 1
        for i in self.figpos:
            if self.pole[i[1]][i[0]] == 'X':
                self.timer.stop()
                i, okBtnPressed = QInputDialog.getText(self, 'Game over', "Введите имя")
                if okBtnPressed:
                    self.save_results(i)
                    self.start.setEnabled(True)
                    self.pausa.setEnabled(False)
                    break
            else:
                self.pole[i[1]][i[0]] = 'X'

    def repaiting(self):
        for i in range(20):
            for j in range(10):
                if self.pole[i][j] == 'O':
                    exec(f'self.btn{str(j) + str(0) + str(i)}.setStyleSheet("background-color: #FFFFFF")')
                elif self.pole[i][j] == 'X':
                    exec(f'self.btn{str(j) + str(0) + str(i)}.setStyleSheet("background-color:'
                         f' {self.buttoncolours[self.deletedlines // 3 % 7]}")')

    def ischecked(self, minx, miny, maxx, maxy, coords):
        q, q1 = 0, 0
        if self.minx + minx >= 0:
            q += 1
        if self.miny + miny >= 0:
            q += 1
        if self.maxx + maxx < 10:
            q += 1
        if self.maxy + maxy <= 19:
            q += 1
        if q == 4:
            for i in range(4):
                if self.pole[self.figpos[i][1] + coords[i][1]][self.figpos[i][0] + coords[i][0]]\
                        == 'O' or [self.figpos[i][0] + coords[i][0], self.figpos[i][1] + coords[i][1]] in self.figpos:
                    q1 += 1
        if q == 4 and q1 == 4:
            return True
        else:
            return False

    def perevorot(self):
        if self.curfig == 'o':
            pass

        elif self.curfig == 'i':
            if self.perevorotfig == 0 or self.perevorotfig == 2:
                if self.ischecked(-2, 1, 1, -2, [[1, 1], [0, 0], [-1, -1], [-2, -2]]):
                    for i in range(4):
                        self.pole[self.figpos[i][1]][self.figpos[i][0]] = 'O'
                    self.figpos = [[self.figpos[0][0] + 1, self.figpos[0][1] + 1],
                               [self.figpos[1][0], self.figpos[1][1]],
                               [self.figpos[2][0] - 1, self.figpos[2][1] - 1],
                               [self.figpos[3][0] - 2, self.figpos[3][1] - 2]]
                    self.minx, self.miny, self.maxx, self.maxy = self.minx - 2, self.miny + 1, self.maxx + 1, self.maxy - 2
                    for i in range(4):
                        self.pole[self.figpos[i][1]][self.figpos[i][0]] = 'X'
                    self.perevorotfig += 1
            elif self.perevorotfig == 1 or self.perevorotfig == 3:
                if self.ischecked(2, -1, -1, 2, [[-1, -1], [0, 0], [1, 1], [2, 2]]):
                    for i in range(4):
                        self.pole[self.figpos[i][1]][self.figpos[i][0]] = 'O'
                    self.figpos = [[self.figpos[0][0] - 1, self.figpos[0][1] - 1],
                               [self.figpos[1][0], self.figpos[1][1]],
                               [self.figpos[2][0] + 1, self.figpos[2][1] + 1],
                               [self.figpos[3][0] + 2, self.figpos[3][1] + 2]]
                    self.minx, self.miny, self.maxx, self.maxy = self.minx + 2, self.miny - 1, self.maxx - 1, self.maxy + 2
                    for i in range(4):
                        self.pole[self.figpos[i][1]][self.figpos[i][0]] = 'X'
                    if self.perevorotfig == 1:
                        self.perevorotfig += 1
                    else:
                        self.perevorotfig = 0

        elif self.curfig == 's':
            if self.perevorotfig == 0 or self.perevorotfig == 2:
                if self.ischecked(1, 0, 0, 1, [[0, 2], [1, 1], [0, 0], [1, -1]]):
                    for i in range(4):
                        self.pole[self.figpos[i][1]][self.figpos[i][0]] = 'O'
                    self.figpos = [[self.figpos[0][0], self.figpos[0][1] + 2],
                               [self.figpos[1][0] + 1, self.figpos[1][1] + 1],
                               [self.figpos[2][0], self.figpos[2][1]],
                               [self.figpos[3][0] + 1, self.figpos[3][1] - 1]]
                    self.minx, self.miny, self.maxx, self.maxy = self.minx + 1, self.miny, self.maxx, self.maxy + 1
                    for i in range(4):
                        self.pole[self.figpos[i][1]][self.figpos[i][0]] = 'X'
                    self.perevorotfig += 1
            elif self.perevorotfig == 1 or self.perevorotfig == 3:
                if self.ischecked(-1, 0, 0, -1, [[0, -2], [-1, -1], [0, 0], [-1, 1]]):
                    for i in range(4):
                        self.pole[self.figpos[i][1]][self.figpos[i][0]] = 'O'
                    self.figpos = [[self.figpos[0][0], self.figpos[0][1] - 2],
                               [self.figpos[1][0] - 1, self.figpos[1][1] - 1],
                               [self.figpos[2][0], self.figpos[2][1]],
                               [self.figpos[3][0] - 1, self.figpos[3][1] + 1]]
                    self.minx, self.miny, self.maxx, self.maxy = self.minx - 1, self.miny, self.maxx, self.maxy - 1
                    for i in range(4):
                        self.pole[self.figpos[i][1]][self.figpos[i][0]] = 'X'
                    if self.perevorotfig == 1:
                        self.perevorotfig += 1
                    else:
                        self.perevorotfig = 0

        elif self.curfig == 'z':
            if self.perevorotfig == 0 or self.perevorotfig == 2:
                if self.ischecked(1, 0, 0, 1, [[2, 0], [1, 1], [0, 0], [-1, 1]]):
                    for i in range(4):
                        self.pole[self.figpos[i][1]][self.figpos[i][0]] = 'O'
                    self.figpos = [[self.figpos[0][0] + 2, self.figpos[0][1]],
                               [self.figpos[1][0] + 1, self.figpos[1][1] + 1],
                               [self.figpos[2][0], self.figpos[2][1]],
                               [self.figpos[3][0] - 1, self.figpos[3][1] + 1]]
                    self.minx, self.miny, self.maxx, self.maxy = self.minx + 1, self.miny, self.maxx, self.maxy + 1
                    for i in range(4):
                        self.pole[self.figpos[i][1]][self.figpos[i][0]] = 'X'
                    self.perevorotfig += 1
            elif self.perevorotfig == 1 or self.perevorotfig == 3:
                if self.ischecked(-1, 0, 0, -1, [[-2, 0], [-1, -1], [0, 0], [1, -1]]):
                    for i in range(4):
                        self.pole[self.figpos[i][1]][self.figpos[i][0]] = 'O'
                    self.figpos = [[self.figpos[0][0] - 2, self.figpos[0][1]],
                               [self.figpos[1][0] - 1, self.figpos[1][1] - 1],
                               [self.figpos[2][0], self.figpos[2][1]],
                               [self.figpos[3][0] + 1, self.figpos[3][1] - 1]]
                    self.minx, self.miny, self.maxx, self.maxy = self.minx - 1, self.miny, self.maxx, self.maxy - 1
                    for i in range(4):
                        self.pole[self.figpos[i][1]][self.figpos[i][0]] = 'X'
                    if self.perevorotfig == 1:
                        self.perevorotfig += 1
                    else:
                        self.perevorotfig = 0

        elif self.curfig == 'l':
            if self.perevorotfig == 0:
                if self.ischecked(1, 0, 0, 1, [[0, 2], [-1, 1], [0, 0], [1, -1]]):
                    for i in range(4):
                        self.pole[self.figpos[i][1]][self.figpos[i][0]] = 'O'
                    self.figpos = [[self.figpos[0][0], self.figpos[0][1] + 2],
                               [self.figpos[1][0] - 1, self.figpos[1][1] + 1],
                               [self.figpos[2][0], self.figpos[2][1]],
                               [self.figpos[3][0] + 1, self.figpos[3][1] - 1]]
                    self.minx, self.miny, self.maxx, self.maxy = self.minx + 1, self.miny, self.maxx, self.maxy + 1
                    for i in range(4):
                        self.pole[self.figpos[i][1]][self.figpos[i][0]] = 'X'
                    self.perevorotfig += 1
            elif self.perevorotfig == 1:
                if self.ischecked(-1, 1, 0, 0, [[-2, 0], [-1, -1], [0, 0], [1, 1]]):
                    for i in range(4):
                        self.pole[self.figpos[i][1]][self.figpos[i][0]] = 'O'
                    self.figpos = [[self.figpos[0][0] - 2, self.figpos[0][1]],
                               [self.figpos[1][0] - 1, self.figpos[1][1] - 1],
                               [self.figpos[2][0], self.figpos[2][1]],
                               [self.figpos[3][0] + 1, self.figpos[3][1] + 1]]
                    self.minx, self.miny, self.maxx, self.maxy = self.minx - 1, self.miny + 1, self.maxx, self.maxy
                    for i in range(4):
                        self.pole[self.figpos[i][1]][self.figpos[i][0]] = 'X'
                    self.perevorotfig += 1
            elif self.perevorotfig == 2:
                if self.ischecked(0, -1, -1, 0, [[0, -2], [1, -1], [0, 0], [-1, 1]]):
                    for i in range(4):
                        self.pole[self.figpos[i][1]][self.figpos[i][0]] = 'O'
                    self.figpos = [[self.figpos[0][0], self.figpos[0][1] - 2],
                               [self.figpos[1][0] + 1, self.figpos[1][1] - 1],
                               [self.figpos[2][0], self.figpos[2][1]],
                               [self.figpos[3][0] - 1, self.figpos[3][1] + 1]]
                    self.minx, self.miny, self.maxx, self.maxy = self.minx, self.miny - 1, self.maxx - 1, self.maxy
                    for i in range(4):
                        self.pole[self.figpos[i][1]][self.figpos[i][0]] = 'X'
                    self.perevorotfig += 1
            elif self.perevorotfig == 3:
                if self.ischecked(0, 0, 1, -1, [[2, 0], [1, 1], [0, 0], [-1, -1]]):
                    for i in range(4):
                        self.pole[self.figpos[i][1]][self.figpos[i][0]] = 'O'
                    self.figpos = [[self.figpos[0][0] + 2, self.figpos[0][1]],
                               [self.figpos[1][0] + 1, self.figpos[1][1] + 1],
                               [self.figpos[2][0], self.figpos[2][1]],
                               [self.figpos[3][0] - 1, self.figpos[3][1] - 1]]
                    self.minx, self.miny, self.maxx, self.maxy = self.minx, self.miny, self.maxx + 1, self.maxy - 1
                    for i in range(4):
                        self.pole[self.figpos[i][1]][self.figpos[i][0]] = 'X'
                    self.perevorotfig = 0

        elif self.curfig == 'j':
            if self.perevorotfig == 0:
                if self.ischecked(1, 0, 0, 1, [[2, 0], [1, -1], [0, 0], [-1, 1]]):
                    for i in range(4):
                        self.pole[self.figpos[i][1]][self.figpos[i][0]] = 'O'
                    self.figpos = [[self.figpos[0][0] + 2, self.figpos[0][1]],
                               [self.figpos[1][0] + 1, self.figpos[1][1] - 1],
                               [self.figpos[2][0], self.figpos[2][1]],
                               [self.figpos[3][0] - 1, self.figpos[3][1] + 1]]
                    self.minx, self.miny, self.maxx, self.maxy = self.minx + 1, self.miny, self.maxx, self.maxy + 1
                    for i in range(4):
                        self.pole[self.figpos[i][1]][self.figpos[i][0]] = 'X'
                    self.perevorotfig += 1
            elif self.perevorotfig == 1:
                if self.ischecked(-1, 1, 0, 0, [[0, 2], [1, 1], [0, 0], [-1, -1]]):
                    for i in range(4):
                        self.pole[self.figpos[i][1]][self.figpos[i][0]] = 'O'
                    self.figpos = [[self.figpos[0][0], self.figpos[0][1] + 2],
                               [self.figpos[1][0] + 1, self.figpos[1][1] + 1],
                               [self.figpos[2][0], self.figpos[2][1]],
                               [self.figpos[3][0] - 1, self.figpos[3][1] - 1]]
                    self.minx, self.miny, self.maxx, self.maxy = self.minx - 1, self.miny + 1, self.maxx, self.maxy
                    for i in range(4):
                        self.pole[self.figpos[i][1]][self.figpos[i][0]] = 'X'
                    self.perevorotfig += 1
            elif self.perevorotfig == 2:
                if self.ischecked(0, -1, -1, 0, [[-2, 0], [-1, 1], [0, 0], [1, -1]]):
                    for i in range(4):
                        self.pole[self.figpos[i][1]][self.figpos[i][0]] = 'O'
                    self.figpos = [[self.figpos[0][0] - 2, self.figpos[0][1]],
                               [self.figpos[1][0] - 1, self.figpos[1][1] + 1],
                               [self.figpos[2][0], self.figpos[2][1]],
                               [self.figpos[3][0] + 1, self.figpos[3][1] - 1]]
                    self.minx, self.miny, self.maxx, self.maxy = self.minx, self.miny - 1, self.maxx - 1, self.maxy
                    for i in range(4):
                        self.pole[self.figpos[i][1]][self.figpos[i][0]] = 'X'
                    self.perevorotfig += 1
            elif self.perevorotfig == 3:
                if self.ischecked(0, 0, 1, -1, [[0, -2], [-1, -1], [0, 0], [1, 1]]):
                    for i in range(4):
                        self.pole[self.figpos[i][1]][self.figpos[i][0]] = 'O'
                    self.figpos = [[self.figpos[0][0], self.figpos[0][1] - 2],
                               [self.figpos[1][0] - 1, self.figpos[1][1] - 1],
                               [self.figpos[2][0], self.figpos[2][1]],
                               [self.figpos[3][0] + 1, self.figpos[3][1] + 1]]
                    self.minx, self.miny, self.maxx, self.maxy = self.minx, self.miny, self.maxx + 1, self.maxy - 1
                    for i in range(4):
                        self.pole[self.figpos[i][1]][self.figpos[i][0]] = 'X'
                    self.perevorotfig = 0

        elif self.curfig == 't':
            if self.perevorotfig == 0:
                if self.ischecked(1, 0, 0, 1, [[1, 1], [1, -1], [-1, 1], [0, 0]]):
                    for i in range(4):
                        self.pole[self.figpos[i][1]][self.figpos[i][0]] = 'O'
                    self.figpos = [[self.figpos[0][0] + 1, self.figpos[0][1] + 1],
                               [self.figpos[1][0] + 1, self.figpos[1][1] - 1],
                               [self.figpos[2][0] - 1, self.figpos[2][1] + 1],
                               [self.figpos[3][0], self.figpos[3][1]]]
                    self.minx, self.miny, self.maxx, self.maxy = self.minx + 1, self.miny, self.maxx, self.maxy + 1
                    for i in range(4):
                        self.pole[self.figpos[i][1]][self.figpos[i][0]] = 'X'
                    self.perevorotfig += 1
            elif self.perevorotfig == 1:
                if self.ischecked(-1, 1, 0, 0, [[-1, 1], [1, 1], [-1, -1], [0, 0]]):
                    for i in range(4):
                        self.pole[self.figpos[i][1]][self.figpos[i][0]] = 'O'
                    self.figpos = [[self.figpos[0][0] - 1, self.figpos[0][1] + 1],
                               [self.figpos[1][0] + 1, self.figpos[1][1] + 1],
                               [self.figpos[2][0] - 1, self.figpos[2][1] - 1],
                               [self.figpos[3][0], self.figpos[3][1]]]
                    self.minx, self.miny, self.maxx, self.maxy = self.minx - 1, self.miny + 1, self.maxx, self.maxy
                    for i in range(4):
                        self.pole[self.figpos[i][1]][self.figpos[i][0]] = 'X'
                    self.perevorotfig += 1
            elif self.perevorotfig == 2:
                if self.ischecked(0, -1, -1, 0, [[-1, -1], [-1, 1], [1, -1], [0, 0]]):
                    for i in range(4):
                        self.pole[self.figpos[i][1]][self.figpos[i][0]] = 'O'
                    self.figpos = [[self.figpos[0][0] - 1, self.figpos[0][1] - 1],
                               [self.figpos[1][0] - 1, self.figpos[1][1] + 1],
                               [self.figpos[2][0] + 1, self.figpos[2][1] - 1],
                               [self.figpos[3][0], self.figpos[3][1]]]
                    self.minx, self.miny, self.maxx, self.maxy = self.minx, self.miny - 1, self.maxx - 1, self.maxy
                    for i in range(4):
                        self.pole[self.figpos[i][1]][self.figpos[i][0]] = 'X'
                    self.perevorotfig += 1
            elif self.perevorotfig == 3:
                if self.ischecked(0, 0, 1, -1, [[1, -1], [-1, -1], [1, 1], [0, 0]]):
                    for i in range(4):
                        self.pole[self.figpos[i][1]][self.figpos[i][0]] = 'O'
                    self.figpos = [[self.figpos[0][0] + 1, self.figpos[0][1] - 1],
                               [self.figpos[1][0] - 1, self.figpos[1][1] - 1],
                               [self.figpos[2][0] + 1, self.figpos[2][1] + 1],
                               [self.figpos[3][0], self.figpos[3][1]]]
                    self.minx, self.miny, self.maxx, self.maxy = self.minx, self.miny, self.maxx + 1, self.maxy - 1
                    for i in range(4):
                        self.pole[self.figpos[i][1]][self.figpos[i][0]] = 'X'
                    self.perevorotfig = 0
        self.repaiting()

    def deletelines(self):
        q = 0
        for i in range(20):
            if self.pole[i].count('X') == 10:
                self.pole.insert(0, ['O' for _ in range(10)])
                del self.pole[i + 1]
                q += 1
                self.deletedlines += 1
                self.level()
        self.score += q * (100 + (q - 1) * 50)
        self.scoreLCD.display(self.score)

    def level(self):
        self.scoreLCD2.display(self.deletedlines // 3)
        self.speed = 600 - self.deletedlines // 3 * 20
        self.timer.start(self.speed)

    def dash(self, dv):
        if len(self.figpos) != 0:
            if dv == 'v':
                if self.maxy < 19:
                    q = True
                    for i in range(4):
                        if self.pole[self.figpos[i][1] + 1][self.figpos[i][0]] == 'X' and \
                                [self.figpos[i][0], self.figpos[i][1] + 1] not in self.figpos:
                            q = False
                    if q:
                        for i in range(4):
                            self.pole[self.figpos[i][1]][self.figpos[i][0]] = 'O'
                            self.figpos[i][1] = self.figpos[i][1] + 1
                        for i in range(4):
                            self.pole[self.figpos[i][1]][self.figpos[i][0]] = 'X'
                        self.repaiting()
                        self.miny += 1
                        self.maxy += 1
                    else:
                        self.figpos = []
                        self.deletelines()
                else:
                    self.figpos = []
                    self.deletelines()

            elif dv == '<':
                if self.minx > 0:
                    q = True
                    for i in range(4):
                        if self.pole[self.figpos[i][1]][self.figpos[i][0] - 1] == 'X' and \
                                [self.figpos[i][0] - 1, self.figpos[i][1]] not in self.figpos:
                            q = False
                    if q:
                        for i in range(4):
                            self.pole[self.figpos[i][1]][self.figpos[i][0]] = 'O'
                            self.figpos[i][0] = self.figpos[i][0] - 1
                        for i in range(4):
                            self.pole[self.figpos[i][1]][self.figpos[i][0]] = 'X'
                        self.repaiting()
                        self.minx -= 1
                        self.maxx -= 1
            elif dv == '>':
                if self.maxx < 9:
                    q = True
                    for i in range(4):
                        if self.pole[self.figpos[i][1]][self.figpos[i][0] + 1] == 'X' and \
                                [self.figpos[i][0] + 1, self.figpos[i][1]] not in self.figpos:
                            q = False
                    if q:
                        self.repaiting()
                        for i in range(4):
                            self.pole[self.figpos[i][1]][self.figpos[i][0]] = 'O'
                            self.figpos[i][0] = self.figpos[i][0] + 1
                        for i in range(4):
                            self.pole[self.figpos[i][1]][self.figpos[i][0]] = 'X'
                        self.repaiting()
                        self.maxx += 1
                        self.minx += 1
            elif dv == '/':
                self.perevorot()

    def nextfigbuild(self):
        for i in range(5):
            for j in range(4):
                exec(f'self.btn{str(i) + str(111) + str(j)}.setStyleSheet("background-color: #FFFFFF")')
        for i in self.figures[self.fig.index(self.nextfig)]:
            exec(f'self.btn{str(i[0] - 2) + str(111) + str(i[1])}.setStyleSheet("background-color: #000000")')

    def turn(self):
        if self.figpos == []:
            self.perevorotfig = 0
            self.curfig = self.nextfig
            self.nextfig = random.choice(self.fig)
            while self.nextfig == self.curfig:
                self.nextfig = random.choice(self.fig)
            self.createfigure(self.curfig)
            self.nextfigbuild()
            self.repaiting()
        else:
            self.dash('v')


app = QApplication(sys.argv)
ex = game()
ex.show()
sys.exit(app.exec_())
