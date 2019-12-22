import os, sys

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtPrintSupport import *
from player import *
from dice import DiceRoll
from random import randrange


class Board(QWidget):
	def __init__(self, parent):
		super(Board, self).__init__(parent)

		# self.max_tiles = self.width * 2 + self.height * 2 - 4
		# self.parent().special_tiles = int(self.max_tiles / 4)
		self.board = self.parent().board

		self.generate_board(self.parent().width, self.parent().height)

		self.player1_button = QPushButton()
		self.player2_button = QPushButton()

		if self.parent().turn is 1:
		#wszystkie rzeczy, kóre muszą się zadziać w pierwszej turze
			self.parent().player2.h1pos_x = self.parent().width - 1
			self.parent().player2.h1pos_y = self.parent().height - 1
			self.parent().player2.h2pos_x = self.parent().width - 1
			self.parent().player2.h2pos_y = self.parent().height - 1
			self.parent().player2.h3pos_x = self.parent().width - 1
			self.parent().player2.h3pos_y = self.parent().height - 1
		#else:
		#	self.unset_heroes()

		if self.parent().turn % 2 is 0:
			self.player_info = self.parent().player2
			self.parent().day += 1
			if self.parent().day % 7 is 1:
				self.parent().week += 1
		else:
			self.player_info = self.parent().player1

		#self.move_hero(self.player_info, 1)
		self.show_heroes()


		#self.player_info.update_week_day()
		self.board.addWidget(self.player_info, 1, 1, self.parent().height - 2, self.parent().width / 2 - 1)
		#only one player, because this widget will be changed depending on whose turn it is

		act = PlayerActions(self)
		place = self.parent().width / 2
		if self.parent().width % 2 != 0:
			place = self.parent().width / 2 + 1

		self.board.addWidget(act, 1, place, self.parent().height - 2, self.parent().width / 2 - 1)

		self.setLayout(self.board)
		self.show()

	def show_heroes(self): # na razie pokazuje tylko odpowiadających bohaterów
		hero = self.player_info.hero
		if hero is 1:
			self.x1, self.y1 = self.parent().player1.h1pos_x, self.parent().player1.h1pos_y
			self.x2, self.y2 = self.parent().player2.h1pos_x, self.parent().player2.h1pos_y
		elif hero is 2:
			self.x1, self.y1 = self.parent().player1.h2pos_x, self.parent().player1.h2pos_y
			self.x2, self.y2 = self.parent().player2.h2pos_x, self.parent().player2.h2pos_y
		else:
			self.x1, self.y1 = self.parent().player1.h3pos_x, self.parent().player1.h3pos_y
			self.x2, self.y2 = self.parent().player2.h3pos_x, self.parent().player2.h3pos_y
		# jakbyśmy chcialy pokazywać tylko po jednym
		'''if self.player_info.player is "Gracz 1":
			self.x2, self.y2 = self.parent().player2.h1pos_x, self.parent().player2.h1pos_y
			if hero is 1:
				self.x1, self.y1 = self.parent().player1.h1pos_x, self.parent().player1.h1pos_y
			elif hero is 2:
				self.x1, self.y1 = self.parent().player1.h2pos_x, self.parent().player1.h2pos_y
			else:
				self.x1, self.y1 = self.parent().player1.h3pos_x, self.parent().player1.h3pos_y
		else:
			self.x1, self.y1 = self.parent().player1.h1pos_x, self.parent().player1.h1pos_y
			if hero is 1:
				self.x2, self.y2 = self.parent().player2.h1pos_x, self.parent().player2.h1pos_y
			elif hero is 2:
				self.x2, self.y2 = self.parent().player2.h2pos_x, self.parent().player2.h2pos_y
			else:
				self.x2, self.y2 = self.parent().player2.h3pos_x, self.parent().player2.h3pos_y'''

		self.set_hero(self.x1, self.y1, self.player1_button)
		self.set_hero(self.x2, self.y2, self.player2_button)



	def generate_board(self, width, height):
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

		self.tiles_amount = k

		if self.parent().turn is 1:
			self.generate_special_tiles()

		if self.parent().day % 7 is 0 and self.parent().turn % 2 is 1:
			self.parent().special_tiles.clear()
			self.generate_special_tiles()

		for i in range(self.tiles_amount): #shows special tiles every turn
			if i in self.parent().special_tiles:
				self.set_button_stylesheet(self.buttons[i], 'objects/treasure.png')

	def generate_special_tiles(self):
		for i in range(self.tiles_amount):
			if randrange(3) == 1:
				self.parent().special_tiles.append(i)

	def set_hero(self, x, y, which_one):
		if which_one == self.player1_button:
			self.set_button_stylesheet(which_one, 'sprites/hero1_p.png')
		else:
			self.set_button_stylesheet(which_one, 'sprites/hero2_p.png')
		self.board.addWidget(which_one, y, x) #row / column

	def unset_heroes(self):# próba ukrycia pionka postaci, który pojawia się pod strałką, ale nie wyszło
		self.player1_button.hide()# deleteLater też nie diziała
		self.player2_button.hide()

	def set_button_stylesheet(self, button, image):
		str = 'height: 60px; width: 60px; background-image: url(None); border-image: url("'
		str += image
		str += '");'
		button.setStyleSheet(str)
		return button
		

class mainWindow(QMainWindow):

	def __init__(self, parent=None):
		super(mainWindow, self).__init__(parent)

		self.week = 1
		self.day = 1
		self.turn = 1

		self.width = 15
		self.height = 10

		self.board = QGridLayout(self) # nie wiem czemu ale musi być tu inaczej jak 2 raz musi wyświetlić pierwszego gracza to się psuje ;(
		self.player1 = PlayerInfo(self, 'Gracz 1')
		self.player2 = PlayerInfo(self, 'Gracz 2')
		self.roll_dice()

		self.special_tiles = [] #po to by się nie aktualizowało za wcześnie

		self.show_info()
		self.setWindowTitle("Board game")
		#self.showFullScreen()
		self.move(0, 0)

		self.setStyleSheet("""
				background-image: url(./UI/map_visual.png);
				background-attachment: scroll;
			""")

	def show_info(self):
		self.setCentralWidget(Board(self))

	def roll_dice(self):
		dice = DiceRoll(self)
		if self.turn % 2 is 0:
			player = self.player2
		else:
			player = self.player1
		player.update_dice_amount(dice.dice)
		player.update_week_day(self.week, self.day)
		#print("przed %d"%player.hero)
		player.can_move = True
		player.hero = 1 #przywrócić defaultową wartość dla kolejnego gracza
		#print("po %d" % player.hero)
		dice.exec_()


if __name__ == "__main__":
	app = QApplication(sys.argv)
	app.aboutToQuit.connect(app.deleteLater)
	win = mainWindow()
	win.show()
	sys.exit(app.exec_())
