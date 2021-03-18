# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'form.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from OpenGL.GL import *
from PyQt5 import QtCore, QtGui, QtWidgets


class Triangle:
    a, b, c = (), (), ()

    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c
        self.cm = self.center_of_mass()

    def center_of_mass(self):
        ox = (self.a[0] + self.b[0] + self.c[0]) / 3
        oy = (self.a[1] + self.b[1] + self.c[1]) / 3
        return (ox, oy)

    def divide(self):
        p1 = self.a  # 90 deg
        p2 = self.b  # 60 deg
        p3 = self.c  # 30 deg
        p4 = ((p2[0] + p3[0]) / 2, (p2[1] + p3[1]) / 2)
        p5 = (p1[0] + (p3[0] - p1[0]) / 3, p1[1] + (p3[1] - p1[1]) / 3)
        tr1 = Triangle(p1, p5, p2)
        tr2 = Triangle(p4, p5, p2)
        tr3 = Triangle(p4, p5, p3)
        return [tr1, tr2, tr3]


class Fractal:
    order = 1
    triangles = []
    points = []
    a, b, c = (), (), ()

    def __init__(self, a, b, c, order=1):
        assert order > 0
        self.a = a
        self.b = b
        self.c = c
        self.order = order

    def place_triangles(self):
        self.triangles = [Triangle(self.a, self.b, self.c)]
        for i in range(self.order):
            new_triangles = []
            new_points = []
            for j in range(len(self.triangles)):
                div = self.triangles[j].divide()
                if j % 2 == 0:
                    div.reverse()
                new_points.extend([div[0].cm, div[1].cm, div[2].cm])
                new_triangles.extend(div)
            self.triangles = new_triangles
            self.points = new_points


class GLWidget(QtWidgets.QOpenGLWidget):
    def __init__(self, parent):
        QtWidgets.QOpenGLWidget.__init__(self, parent)
        self.setMinimumSize(100, 100)
        self.order = 1
        self.a, self.b, self.c = (-1, -0.5), (-1, 0.7), (1.07, -0.5)

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        kx, ky = 1, 1
        if self.width() > self.height():
            kx = self.height() / self.width()
        else:
            ky = self.width() / self.height()
        glScale(kx, ky, 1)
        glLineWidth(2.0)
        self.draw_shape()
        glFlush()

    def initializeGL(self):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(0, self.width(), self.height(), 0, 1, 0)

    def draw_shape(self):
        fr = Fractal(self.a, self.b, self.c, self.order)
        fr.place_triangles()
        self.draw_triangles(fr)
        self.draw_line(fr.points)

    def draw_triangles(self, fr):
        for tr in fr.triangles:
            p1 = tr.a
            p2 = tr.b
            p3 = tr.c
            glBegin(GL_LINE_LOOP)
            glColor4d(0, 0, 1, 1)
            glVertex2d(p1[0], p1[1])
            glVertex2d(p2[0], p2[1])
            glVertex2d(p3[0], p3[1])
            glEnd()

    def draw_line(self, points):
        glBegin(GL_LINE_STRIP)
        glColor4d(1, 1, 1, 1)
        for p in points:
            glVertex2d(p[0], p[1])
        glEnd()


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setMaximumSize(QtCore.QSize(16777215, 70))
        self.widget.setObjectName("widget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.order = QtWidgets.QSlider(self.widget)
        self.order.setOrientation(QtCore.Qt.Horizontal)
        self.order.setObjectName("order")
        self.verticalLayout.addWidget(self.order)
        self.verticalLayout_3.addWidget(self.widget)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.canvas = GLWidget(self.centralwidget)
        self.canvas.setObjectName("canvas")
        self.verticalLayout_2.addWidget(self.canvas)
        self.verticalLayout_3.addLayout(self.verticalLayout_2)
        MainWindow.setCentralWidget(self.centralwidget)

        self.order.setMinimum(1)
        self.order.setMaximum(8)
        self.order.setValue(1)
        self.order.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.order.setTickInterval(1)
        self.order.valueChanged.connect(self.order_changed)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Лабораторная 4"))
        self.label.setText(_translate("MainWindow", "Порядок фрактала"))

    def order_changed(self):
        o = self.order.value()
        self.canvas.order = o
        self.canvas.update()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
