import os, sys

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtPrintSupport import *


class Board(QWidget):
	def __init__(self, parent):
		super(Board, self).__init__(parent)

		board = QGridLayout()

		width = 12
		height = 10

		self.buttons = [[0 for x in range(width)] for y in range(height)]

		arrow = QPixmap('objects/arrow_green.png')
		#arrow = arrow.scaled(50, 50) #nie działa, zmniejsza się, ale w pewnym momencie nie chce się już zwiększyć xd
		rotation = 90
		left = arrow
		up = arrow.transformed(QTransform().rotate(rotation), Qt.SmoothTransformation)
		down = arrow.transformed(QTransform().rotate(-rotation), Qt.SmoothTransformation)
		right = arrow.transformed(QTransform().rotate(2*rotation), Qt.SmoothTransformation)

		for i in range(height):
			for j in range(width):
				self.buttons[i][j] = QPushButton()
				if i is 0 and j is width-1:
					self.buttons[i][j].setStyleSheet('height: 60px; width: 60px; border-image: url("objects/arrow_green_down.png");')
				elif i is height-1 and j is 0:
					self.buttons[i][j].setStyleSheet('height: 60px; width: 60px; border-image: url("objects/arrow_green_up.png");')
				#a to całą resztę
				elif i is 0:
					self.buttons[i][j].setStyleSheet('height: 60px; width: 60px; border-image: url("objects/arrow_green_right.png");')
				elif i is height-1:
					self.buttons[i][j].setStyleSheet('height: 60px; width: 60px; border-image: url("objects/arrow_green_left.png");')
				elif j is 0:
					self.buttons[i][j].setStyleSheet('height: 60px; width: 60px; border-image: url("objects/arrow_green_up.png");')
				elif j is width-1:
					self.buttons[i][j].setStyleSheet('height: 60px; width: 60px; border-image: url("objects/arrow_green_down.png");')
				else:
					self.buttons[i][j].setText("")

				board.addWidget(self.buttons[i][j], i, j)

		for i in range(height-2):
			for j in range(width-2):
				self.buttons[i+1][j+1].deleteLater()

		self.setLayout(board)
		self.show()


class mainWindow(QMainWindow):

	def __init__(self, parent=None):
		super(mainWindow, self).__init__(parent)

		self.board = Board(self)
		self.setCentralWidget(self.board)
		self.setWindowTitle("Board game")
		self.showFullScreen()


if __name__ == "__main__":
	app = QApplication(sys.argv)
	app.aboutToQuit.connect(app.deleteLater)
	win = mainWindow()
	win.show()
	sys.exit(app.exec_())
