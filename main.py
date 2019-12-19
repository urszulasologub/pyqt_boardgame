import os, sys

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtPrintSupport import *
from player import *
from dice import DiceRoll



class Board(QWidget):
	def __init__(self, parent):
		super(Board, self).__init__(parent)

		width = 15
		height = 10
		max_tiles = width * 2 + height * 2 - 4
		self.special_tiles = int(max_tiles / 4)
		self.generate_board(width, height)
		self.player1 = QPushButton()
		self.player2 = QPushButton()
		self.set_hero(0, 0, self.player1)
		self.set_hero(height - 1, width - 1, self.player2)

		label1 = PlayerInfo(self, 'Gracz 1')
		self.board.addWidget(label1, 1, 1, height - 2, width / 2 - 1)
		#only one player, because this widget will be changed depending on whose turn it is

		act = PlayerActions(self, 'Gracz 1')
		place = width / 2
		if width % 2 != 0:
			place = width / 2 + 1
		self.board.addWidget(act, 1, place, height - 2, width / 2 - 1)
		
		self.setLayout(self.board)
		self.show()
		dice = DiceRoll(self)
		dice.roll_dice()


	def generate_board(self, width, height):
		self.board = QGridLayout(self)
		self.buttons = []
		k = 0

		for j in range(width - 1):
			self.buttons.append(QPushButton())
			self.set_button_stylesheet(self.buttons[k], 'objects/arrow_green_right.png')
			self.board.addWidget(self.buttons[k], 0, j)
			self.buttons[k].setText(str(k))
			k += 1

		for i in range(height - 1):
			self.buttons.append(QPushButton())
			self.set_button_stylesheet(self.buttons[k], 'objects/arrow_green_down.png')
			self.board.addWidget(self.buttons[k], i, width - 1)
			self.buttons[k].setText(str(k))
			k += 1

		for j in range(width - 1):
			self.buttons.append(QPushButton())
			self.set_button_stylesheet(self.buttons[k], 'objects/arrow_green_left.png')
			self.board.addWidget(self.buttons[k], height - 1, width - j - 1)
			self.buttons[k].setText(str(k))
			k += 1

		for i in range(height - 1):
			self.buttons.append(QPushButton())
			self.set_button_stylesheet(self.buttons[k], 'objects/arrow_green_up.png')
			self.board.addWidget(self.buttons[k], height - i - 1, 0)
			self.buttons[k].setText(str(k))
			k += 1

		self.set_button_stylesheet(self.buttons[0], 'objects/castle1.png')
		self.set_button_stylesheet(self.buttons[int(k / 2)], 'objects/castle1.png')

		self.generate_special_tiles(width, height)


	def generate_special_tiles(self, width, height):
		print(self.buttons)


	def set_hero(self, x1, y1, which_one):
		if which_one == self.player1:
			self.set_button_stylesheet(which_one, 'sprites/hero1_p.png')
		else:
			self.set_button_stylesheet(which_one, 'sprites/hero2_p.png')
		self.board.addWidget(which_one, x1, y1)

		
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
		#self.showFullScreen()
		self.move(0, 0)


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
