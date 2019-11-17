from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys
import random


class game(QMainWindow):
    def __init__(self):
        super().__init__()
        self.speed = 600
        self.initUI()
        self.pole = []
        self.createpole()
        self.fig = ['o', 'i', 's', 'z', 'l', 'j', 't']
        self.curfig = ''
        self.figpos = []
        self.minx, self.miny, self.maxx, self.maxy = 0, 0, 0, 0
        self.perevorotfig = 0
        self.deletedlines = 0
        self.score = 0
        self.buttoncolours = ['#FF00FF', '#800080', '#FF0000', '#800000',
                              '#008000', '#FFFF00', '#00FF00', '#808000', '#00FFFF', '#0000FF']


    def initUI(self):
        self.setGeometry(900, 100, 800, 800)
        self.setWindowTitle('GAME')

        self.start = QPushButton(f'Начать игру', self)
        self.start.resize(100, 40)
        self.start.move(50, 10)
        self.start.clicked.connect(self.turn)

        self.timer = QTimer()
        self.timer.timeout.connect(self.turn)
        self.timer.start(self.speed)

        self.label = QLabel(self)
        self.label.setText("Очки")
        self.label.move(80, 110)

        self.scoreLCD = QLCDNumber(self)
        self.scoreLCD.move(60, 140)

    def createpole(self):
        for i in range(10):
            for j in range(20):
                exec(f'self.btn{str(i) + str(0) + str(j)} = QPushButton(self)')
                exec(f'self.btn{str(i) + str(0) + str(j)}.resize(40, 40)')
                exec(f'self.btn{str(i) + str(0) + str(j)}.move({i * 40 + 200}, {j * 40})')
                exec(f'self.btn{str(i) + str(0) + str(j)}.setEnabled(False)')
                exec(f'self.btn{str(i) + str(0) + str(j)}.setStyleSheet("background-color: #FFFFFF")')
                exec(f'self.btn{str(i) + str(0) + str(j)}.show()')
        for i in range(20):
            pole1 = []
            for j in range(10):
                pole1.append('O')
            self.pole.append(pole1)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_D:
            self.dash('>')
        elif event.key() == Qt.Key_A:
            self.dash('<')
        elif event.key() == Qt.Key_S:
            self.score += 1
            self.scoreLCD.display(self.score)
            self.dash('v')
        elif event.key() == Qt.Key_W:
            self.dash('/')

    def createfigure(self):
        if self.pole[0][4] == 'X':
            print('lose')
            self.timer.stop()
        else:
            if self.curfig == 'o':
                self.figpos = [[4, 0], [5, 0], [4, 1], [5, 1]]
                self.minx, self.miny, self.maxx, self.maxy = 4, 0, 5, 1
            elif self.curfig == 'i':
                self.figpos = [[4, 0], [4, 1], [4, 2], [4, 3]]
                self.minx, self.miny, self.maxx, self.maxy = 4, 0, 4, 3
            elif self.curfig == 's':
                self.figpos = [[4, 0], [3, 0], [3, 1], [2, 1]]
                self.minx, self.miny, self.maxx, self.maxy = 2, 0, 4, 1
            elif self.curfig == 'z':
                self.figpos = [[4, 0], [5, 0], [5, 1], [6, 1]]
                self.minx, self.miny, self.maxx, self.maxy = 4, 0, 6, 1
            elif self.curfig == 'l':
                self.figpos = [[4, 0], [4, 1], [3, 1], [2, 1]]
                self.minx, self.miny, self.maxx, self.maxy = 2, 0, 4, 1
            elif self.curfig == 'j':
                self.figpos = [[4, 0], [4, 1], [5, 1], [6, 1]]
                self.minx, self.miny, self.maxx, self.maxy = 4, 0, 6, 1
            elif self.curfig == 't':
                self.figpos = [[4, 0], [3, 1], [5, 1], [4, 1]]
                self.minx, self.miny, self.maxx, self.maxy = 3, 0, 5, 1
            for i in self.figpos:
                self.pole[i[1]][i[0]] = 'X'

    def repaiting(self):
        for i in range(20):
            for j in range(10):
                if self.pole[i][j] == 'O':
                    exec(f'self.btn{str(j) + str(0) + str(i)}.setStyleSheet("background-color: #FFFFFF")')
                elif self.pole[i][j] == 'X':
                    exec(f'self.btn{str(j) + str(0) + str(i)}.setStyleSheet("background-color: {self.buttoncolours[self.deletedlines // 3 % 10]}")')

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

    def turn(self):
        if self.figpos == []:
            self.perevorotfig = 0
            self.curfig = random.choice(self.fig)
            self.createfigure()
            self.repaiting()
        else:
            self.dash('v')


app = QApplication(sys.argv)
ex = game()
ex.show()
sys.exit(app.exec_())
