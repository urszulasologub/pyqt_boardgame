import os, sys

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtPrintSupport import *


class PlayerInfo(QWidget):
	def __init__(self, parent, player):
		super(PlayerInfo, self).__init__(parent)
		self.setStyleSheet("""
				background-image: url(UI/brown_background.jpg);
				background-attachment: scroll;
				border: 2px solid gray;
				border-radius: 10px;
			""")
		grid = QGridLayout(self)
		castle_image = QPushButton()
		castle_image.setStyleSheet('border-image: url(UI/castle_inside); min-height: 200px;')
		grid.addWidget(castle_image)
		player_label = QLabel(player)
		grid.addWidget(player_label)
		self.setLayout(grid)


class Board(QWidget):
	def __init__(self, parent):
		super(Board, self).__init__(parent)

		width = 15
		height = 10
		max_tiles = width * 2 + height * 2 - 4
		self.special_tiles = int(max_tiles / 4)
		self.generate_board(width, height)
		self.set_hero(0, 0, 1)
		self.set_hero(height - 1, width - 1, 2)

		label1 = PlayerInfo(self, 'Gracz 1')
		self.board.addWidget(label1, 1, 1, height - 2, width / 2 - 1)

		place = width / 2
		if width % 2 != 0:
			place = width / 2 + 1
		label2 = PlayerInfo(self, 'Gracz 2')
		self.board.addWidget(label2, 1, place, height - 2, width / 2 - 1)

		self.setLayout(self.board)
		self.show()


	def generate_board(self, width, height):
		self.buttons = [[0 for x in range(width)] for y in range(height)]
		self.board = QGridLayout(self)
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
		self.set_button_stylesheet(self.buttons[height - 1][width - 1], 'objects/castle1.png')
		
		for i in range(height - 2):
			for j in range(width - 2):
				self.buttons[i + 1][j + 1].deleteLater()


	def set_hero(self, x1, y1, which_one=1):
		#icon1  = QPixmap('sprites/hero1.png')
		#self.buttons[x1][y1].setIcon(QIcon(icon1))
		if which_one == 1:
			self.set_button_stylesheet(self.buttons[x1][y1], 'sprites/castle1_hero1.png')
			self.board.addWidget(self.buttons[x1][y1], x1, y1)
		else:
			self.set_button_stylesheet(self.buttons[x1][y1], 'sprites/castle1_hero2.png')
			self.board.addWidget(self.buttons[x1][y1], x1, y1)

		
	def set_button_stylesheet(self, button, image):
		str = 'height: 60px; width: 60px; background-image: url(None); border-image: url("'
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


		self.setStyleSheet("""
				background-image: url(./UI/map_visual.png);
				background-attachment: scroll;
			""")

if __name__ == "__main__":
	app = QApplication(sys.argv)
	app.aboutToQuit.connect(app.deleteLater)
	win = mainWindow()
	win.show()
	sys.exit(app.exec_())
