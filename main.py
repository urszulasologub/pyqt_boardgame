import os, sys

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtPrintSupport import *


class Board(QWidget):
	def __init__(self, parent):
		super(Board, self).__init__(parent)

		width = 12
		height = 10
		self.generate_board(width, height)


		self.setLayout(self.board)
		self.show()


	def generate_board(self, width, height):
		self.buttons = [[0 for x in range(width)] for y in range(height)]
		self.board = QGridLayout()
		for i in range(height):
			for j in range(width):
				self.buttons[i][j] = QPushButton()

		for j in range(width):
			self.set_button_stylesheet(self.buttons[0][j], 'objects/arrow_green_right.png')
			self.set_button_stylesheet(self.buttons[height - 1][j], 'objects/arrow_green_left.png')
			self.board.addWidget(self.buttons[0][j], 0, j)
			self.board.addWidget(self.buttons[height - 1][j], height - 1, j)

		for i in range(height):
			self.set_button_stylesheet(self.buttons[i][0], 'objects/arrow_green_up.png')
			self.set_button_stylesheet(self.buttons[i][width - 1], 'objects/arrow_green_down.png')
			self.board.addWidget(self.buttons[i][0], i, 0)
			self.board.addWidget(self.buttons[i][width - 1], i, width - 1)

		self.set_button_stylesheet(self.buttons[0][0], 'objects/castle1.png')
		
		for i in range(height-2):
			for j in range(width-2):
				self.buttons[i+1][j+1].deleteLater()

		
	def set_button_stylesheet(self, button, image):
		str = 'height: 60px; width: 60px; border-image: url("'
		str += image
		str += '");'
		button.setStyleSheet(str)
		return button
		


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
