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
		self.buttons = []
		self.board = self.parent().board

		self.player1_button = QPushButton()
		self.player2_button = QPushButton()
		self.player1_button2 = QPushButton()  # jeśli nie są od razu, to przy zakupie przestawiało pierwszy pionek na pozycję startową
		self.player2_button2 = QPushButton()
		self.player1_button3 = QPushButton()
		self.player2_button3 = QPushButton()
		self.player1_button2.hide()  # ukrywa dopóki nie zostaną kupione
		self.player2_button2.hide()
		self.player1_button3.hide()
		self.player2_button3.hide()

		if self.parent().turn is 1:
		#wszystkie rzeczy, kóre muszą się zadziać w pierwszej turze
			self.parent().player2.h1pos_x = self.parent().width - 1
			self.parent().player2.h1pos_y = self.parent().height - 1
			self.parent().player2.h2pos_x = self.parent().width - 1
			self.parent().player2.h2pos_y = self.parent().height - 1
			self.parent().player2.h3pos_x = self.parent().width - 1
			self.parent().player2.h3pos_y = self.parent().height - 1

		self.generate_board(self.parent().width, self.parent().height)
		self.generate_special_tiles()

		act = PlayerActions(self)
		place = self.parent().width / 2
		if self.parent().width % 2 != 0:
			place = self.parent().width / 2 + 1

		self.board.addWidget(act, 1, place, self.parent().height - 2, self.parent().width / 2 - 1)

		self.setLayout(self.board)
		self.show()


	def show_heroes(self):# na razie pokazuje tylko odpowiadających bohaterów
		player1 = self.parent().player1
		player2 = self.parent().player2

		#każdy ma od razu hero1 więc nie sprawdzam
		#a powinnaś, bo hero1 mozna stracić ;)
		if 1 in player1.available_heroes:
			self.h1x1, self.h1y1 = self.parent().player1.h1pos_x, self.parent().player1.h1pos_y
			self.set_hero(self.h1x1, self.h1y1, self.player1_button)
		if 1 in player2.available_heroes:
			self.h1x2, self.h1y2 = self.parent().player2.h1pos_x, self.parent().player2.h1pos_y
			self.set_hero(self.h1x2, self.h1y2, self.player2_button)

		if 2 in player1.available_heroes: #resztę trzeba sprawdzić zanim się ich wyświtli
			self.h2x1, self.h2y1 = self.parent().player1.h2pos_x, self.parent().player1.h2pos_y
			self.set_hero_2(self.h2x1, self.h2y1, self.player1_button2)
		if 2 in player2.available_heroes:
			self.h2x2, self.h2y2 = self.parent().player2.h2pos_x, self.parent().player2.h2pos_y
			self.set_hero_2(self.h2x2, self.h2y2, self.player2_button2)
		if 3 in player1.available_heroes:
			self.h3x1, self.h3y1 = self.parent().player1.h3pos_x, self.parent().player1.h3pos_y
			self.set_hero_3(self.h3x1, self.h3y1, self.player1_button3)
		if 3 in player2.available_heroes:
			self.h3x2, self.h3y2 = self.parent().player2.h3pos_x, self.parent().player2.h3pos_y
			self.set_hero_3(self.h3x2, self.h3y2, self.player2_button3)


	def generate_board(self, width, height):
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

		self.board.addWidget(self.parent().player2, 1, 1, self.parent().height - 2, self.parent().width / 2 - 1)# najpier dodaje oba, a pożniej chowam i pokazuje w zależności od tury
		self.board.addWidget(self.parent().player1, 1, 1, self.parent().height - 2, self.parent().width / 2 - 1)

		if self.parent().update_units:		#We should update units and money at the same moment
			self.parent().update_units = False
			available = self.parent().player1.available_units
			i = 0
			growth = {
				1 : [10, 7, 0, 0, 0],
				2 : [20, 15, 5, 0, 0],
				3 : [25, 20, 10, 3, 0],
				4 : [35, 25, 15, 6, 2]	
			}
			for i in range(5):
				level = 'level_' + str(i + 1)
				if self.parent().player1.castle.available[i]:
					self.parent().player1.available_units[level] += growth[self.parent().player1.castle_level][i]
				if self.parent().player2.castle.available[i]:
					self.parent().player2.available_units[level] += growth[self.parent().player1.castle_level][i]
				self.parent().player1.castle.update_unit_labels()
				self.parent().player2.castle.update_unit_labels()
			
			self.parent().player1.update_gold_amount(self.parent().player1.gold + 2500)
			self.parent().player2.update_gold_amount(self.parent().player2.gold + 2500)
			
			

		if self.parent().turn % 2 is 0:
			self.player_info = self.parent().player2
			self.parent().player1.hide()
			self.player_info.show()
			if not self.parent().changed_day:
				self.parent().changed_day = True
				self.parent().day += 1
				if self.parent().day % 7 is 1:
					self.parent().week += 1
					self.parent().update_units = True
		else:
			self.parent().changed_day = False
			self.player_info = self.parent().player1 #player_info nadal jest potrzebne, bo jest używane w innych miejscach w kodzie
			self.parent().player2.hide()
			self.player_info.show()
		#self.board.addWidget(self.player_info, 1, 1, self.parent().height - 2, self.parent().width / 2 - 1) #tak nie chce dziłać

		self.show_heroes()

		for i in range(self.tiles_amount): #shows special tiles every turn
			if i in self.parent().special_tiles:
				self.set_button_stylesheet(self.buttons[i], 'objects/treasure.png')


	def generate_special_tiles(self):
		self.parent().special_tiles.clear()
		self.parent().special_locations.clear()
		for i in range(1, self.tiles_amount):
			if randrange(2) == 1 and i is not int(self.tiles_amount / 2):
				self.parent().special_tiles.append(i)
				self.set_button_stylesheet(self.buttons[i], 'objects/treasure.png')
				location = self.parent().board.getItemPosition(i)
				self.parent().special_locations.append((location[1], location[0]))


	def set_hero(self, x, y, which_one):
		if which_one == self.player1_button:
			self.player1_button.show()
			self.set_button_stylesheet(which_one, 'sprites/hero1_p.png')
		else:
			self.player2_button.show()
			self.set_button_stylesheet(which_one, 'sprites/hero2_p.png')
		self.board.addWidget(which_one, y, x) #row / column

	def set_hero_2(self, x, y, which_one):
		if which_one == self.player1_button2:
			self.player1_button2.show()
			self.set_button_stylesheet(which_one, 'sprites/hero1_2p.png')
		else:
			self.player2_button2.show()
			self.set_button_stylesheet(which_one, 'sprites/hero2_2p.png')
		self.board.addWidget(which_one, y, x)

	def set_hero_3(self, x, y, which_one):
		if which_one == self.player1_button3:
			self.player1_button3.show()
			self.set_button_stylesheet(which_one, 'sprites/hero1_3p.png')
		else:
			self.player2_button3.show()
			self.set_button_stylesheet(which_one, 'sprites/hero2_3p.png')
		self.board.addWidget(which_one, y, x)

	def set_button_stylesheet(self, button, image):
		str = 'height: 60px; width: 60px; background-image: url(None); border-image: url("'
		str += image
		str += '");'
		button.setStyleSheet(str)
		return button

	def get_opponent_on_tile(self, x, y):
		#1, 2, 3 or castle
		objects = []
		if self.parent().turn % 2 == 1:
			if self.parent().player2.h1pos_x == x and self.parent().player2.h1pos_y == y:
				if 1 in self.parent().player2.available_heroes:
					objects.append('1')
			if self.parent().player2.h2pos_x == x and self.parent().player2.h2pos_y == y:
				if 2 in self.parent().player2.available_heroes:
					objects.append('2')
			if self.parent().player2.h3pos_x == x and self.parent().player2.h3pos_y == y:
				if 3 in self.parent().player2.available_heroes:
					objects.append('3')
			if self.parent().player2.castle_x == x and self.parent().player2.castle_y == y:
				objects.append('castle')
		else:
			if self.parent().player1.h1pos_x == x and self.parent().player1.h1pos_y == y:
				if 1 in self.parent().player1.available_heroes:
					objects.append('1')
			if self.parent().player1.h2pos_x == x and self.parent().player1.h2pos_y == y:
				if 2 in self.parent().player1.available_heroes:
					objects.append('2')
			if self.parent().player1.h3pos_x == x and self.parent().player1.h3pos_y == y:
				if 3 in self.parent().player1.available_heroes:
					objects.append('3')		
			if self.parent().player1.castle_x == x and self.parent().player1.castle_y == y:
				objects.append('castle')	
		return objects


class mainWindow(QMainWindow):
	def __init__(self, parent=None):
		super(mainWindow, self).__init__(parent)

		self.week = 1
		self.day = 1
		self.turn = 1
		self.update_units = False
		self.changed_day = False

		self.width = 15
		self.height = 10

		self.board = QGridLayout(self) # nie wiem czemu ale musi być tu inaczej jak 2 raz musi wyświetlić pierwszego gracza to się psuje ;(
		self.player1 = PlayerInfo(self, 'Gracz 1', 0, 0)
		self.player2 = PlayerInfo(self, 'Gracz 2', self.width - 1, self.height - 1)
		self.roll_dice()

		self.special_tiles = [] #po to by się nie aktualizowało za wcześnie
		self.special_locations = []

		self.board_widget = Board(self)
		self.setCentralWidget(self.board_widget)
		self.setWindowTitle('Heroes of Might and Magic: Gra planszowa')
		#self.showFullScreen()
		self.move(0, 0)

		self.setStyleSheet("""
				background-image: url(./UI/map_visual.png);
				background-attachment: scroll;
			""")

	def show_info(self):
		self.board_widget.generate_board(self.width, self.height)


	def roll_dice(self):
		dice = DiceRoll(self)
		if self.turn % 2 is 0:
			player = self.player2
		else:
			player = self.player1
		player.update_dice_amount(dice.dice)
		player.update_week_day(self.week, self.day)
		player.can_move = True
		if not player.available_heroes:
			player.hero = None
		else:
			player.hero = player.available_heroes[0]
		dice.exec_()


if __name__ == "__main__":
	app = QApplication(sys.argv)
	app.aboutToQuit.connect(app.deleteLater)
	win = mainWindow()
	win.show()
	sys.exit(app.exec_())
