import os, sys

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtPrintSupport import *
from dice import DiceRoll
from castle import Castle
import math


class PlayerInfo(QWidget):
	def __init__(self, parent, player):
		self.castle_level = 1
		self.gold = 0
		self.dice = 0
		self.h1pos_x = 0
		self.h1pos_y = 0
		self.h2pos_x = 0
		self.h2pos_y = 0
		self.h3pos_x = 0
		self.h3pos_y = 0
		self.hero = 1# to którym obecnie bohaterem się porusza
		self.available_heroes = [1]
		self.can_move = False

		self.h1units = {
			"level_1": 15,
			"level_2": 10,
			"level_3": 0,
			"level_4": 0,
			"level_5": 0,
		}

		self.h2units = {
			"level_1": 15,
			"level_2": 10,
			"level_3": 0,
			"level_4": 0,
			"level_5": 0
		}

		self.h3units = {
			"level_1": 15,
			"level_2": 10,
			"level_3": 0,
			"level_4": 0,
			"level_5": 0
		}

		self.in_castle_units = {
			"level_1": 10,
			"level_2": 5,
			"level_3": 0,
			"level_4": 0,
			"level_5": 0
		}

		self.available_units = {
			"level_1": 10,
			"level_2": 5,
			"level_3": 0,
			"level_4": 0,
			"level_5": 0
		}		

		super(PlayerInfo, self).__init__(parent)
		color = 'darkblue'
		if player == 'Gracz 1':
			color = 'darkred'
		self.setStyleSheet("""
				background-image: url(UI/brown_background.jpg);
				background-attachment: scroll;
				border: 2px outset %s;
				border-radius: 10px;
				color: white;
				font-size: 18pt;
				font: Arial;
			""" % color)
		self.grid = QGridLayout(self)
		castle_image = QPushButton()
		castle_image.setStyleSheet('border-image: url(UI/castle_inside); min-height: 200px; ')
		castle_image.clicked.connect(self.show_castle)

		self.grid.addWidget(castle_image, 0, 0)

		self.labels = [QLabel(player), QLabel('Poziom zamku: %d' % self.castle_level), QLabel('Złoto: 0'), QLabel('Wyrzucono oczek: %d' % self.dice), QLabel('Tydzień: %d, Dzień: %d' % (self.parent().week, self.parent().day))]

		i = 1
		for label in self.labels:
			self.grid.addWidget(label, i, 0)
			i += 1

		self.setLayout(self.grid)
		self.update_gold_amount(5000)
		#self.update_week_day()


	def show_castle(self):
		castle = Castle(self)
		castle.exec_()


	def update_castle_level(self, level):
		self.castle_level = level
		text = 'Poziom zamku: ' + str(level)
		self.labels[1] = QLabel(text)
		self.grid.addWidget(self.labels[1], 2, 0)


	def update_gold_amount(self, amount):
		self.gold = amount
		text = 'Złoto: ' + str(amount)
		self.labels[2] = QLabel(text)
		self.grid.addWidget(self.labels[2], 3, 0)


	def update_dice_amount(self, amount):
		self.dice = amount
		text = 'Wyrzucono oczek: ' + str(amount)
		self.labels[3] = QLabel(text)
		self.grid.addWidget(self.labels[3], 4, 0)


	def update_week_day(self, week, day): # z jakiegoś powodu, jak się używa parent() to wywala cały program
		text = 'Tydzień: ' + str(week) + ', Dzień: ' + str(day)
		self.labels[4] = QLabel(text)
		self.grid.addWidget(self.labels[4], 5, 0)


	def clear_hero_pos(self, hero_num):
		if hero_num == 1:
			self.h1pos_x = 0
			self.h1pos_y = 0
		elif hero_num == 2:
			self.h2pos_x = 0
			self.h2pos_y = 0
		else:
			self.h3pos_x = 0
			self.h3pos_y = 0

#akcje zawsze są te same, więc nie potrzeba podawać gracza
class PlayerActions(QWidget):
	def __init__(self, parent):
		super(PlayerActions, self).__init__(parent)
		self.main_window = self.parent().parent()
		self.board = self.parent()
		self.setStyleSheet("""
				background-image: url(UI/brown_background.jpg);
				background-attachment: scroll;
				border: 2px outset gray;
				border-radius: 10px;
				color: white;
				font-size: 18pt;
				font: Arial;
				min-height: 50px;
			""")

		self.grid = QGridLayout(self)
		self.labels = ['Zobacz druzynę', 'Zakończ kolejkę', 'Atakuj', 'Bohater1', 'Bohater2', 'Bohater3', 'Wykonaj ruch']
		self.buttons = []

		for i in range(len(self.labels)):
			self.buttons.append(QPushButton(self.labels[i]))
			self.grid.addWidget(self.buttons[i], i, 0)

		self.buttons[1].clicked.connect(self.change_turn)
		self.buttons[3].clicked.connect(self.set_hero_one)
		self.buttons[4].clicked.connect(self.set_hero_two)
		self.buttons[5].clicked.connect(self.set_hero_three)
		self.buttons[6].clicked.connect(self.move)
		self.setLayout(self.grid)

	def move(self):
		if self.main_window.turn % 2 is 0:
			hero = self.main_window.player2.hero
			player = self.main_window.player2
		else:
			hero = self.main_window.player1.hero
			player = self.main_window.player1

		if player.can_move:
			self.move_hero(player, hero, self.main_window.height, self.main_window.width)
			player.can_move = False
			#Zmienić wartoś nowej zmiennej, że już się ruszył
			self.main_window.show_info()
		else:# zmieni się na jakiś dialog czy coś
			print("Już się ruszyłeś w tej turze")

	def move_hero(self, player, hero, height, width):
		if hero is 1:# muszę w ten sposób, z dodatkowa zmienna na player.h1pos_x itd, nie działa
			#print("=====")
			for i in range(player.dice):  # pętli, żeby nie wyszło za przedział
				if player.h1pos_x in range(width - 1) and player.h1pos_y is 0:
					#print("lewo")
					player.h1pos_x += 1
				elif player.h1pos_x is 0 and player.h1pos_y in range(width - 1):
					#print("gora")
					player.h1pos_y -= 1
				elif player.h1pos_x in range(width) and player.h1pos_y is height - 1:
					#print("prawo")
					player.h1pos_x -= 1
				elif player.h1pos_x is width - 1 and player.h1pos_y in range(height):
					#print("dol")
					player.h1pos_y += 1
		elif hero is 2:
			for i in range(player.dice):
				if player.h2pos_x in range(width - 1) and player.h2pos_y is 0:
					player.h2pos_x += 1
				elif player.h2pos_x is 0 and player.h2pos_y in range(width - 1):
					player.h2pos_y -= 1
				elif player.h2pos_x in range(width) and player.h2pos_y is height - 1:
					player.h2pos_x -= 1
				elif player.h2pos_x is width - 1 and player.h2pos_y in range(height):
					player.h2pos_y += 1
		else:
			for i in range(player.dice):
				if player.h3pos_x in range(width - 1) and player.h3pos_y is 0:
					player.h3pos_x += 1
				elif player.h3pos_x is 0 and player.h3pos_y in range(width - 1):
					player.h3pos_y -= 1
				elif player.h3pos_x in range(width) and player.h3pos_y is height - 1:
					player.h3pos_x -= 1
				elif player.h3pos_x is width - 1 and player.h3pos_y in range(height):
					player.h3pos_y += 1

	def change_turn(self):
		self.main_window.turn += 1
		#print(self.main_window.turn)
		self.main_window.roll_dice()
		self.main_window.show_info()

	def buy_new_hero(self, player, hero):
		self._dialog = QDialog()
		self._dialog.setWindowTitle("Kup bohatera")
		layout = QVBoxLayout(self._dialog)#tymczasowo
		text = QLabel()
		text.setText("Kupić bohatera za 1500 sztuk złota?")
		buy = QPushButton()
		buy.setText("Kup")
		buy.clicked.connect(lambda: self.buy(player, hero))
		cancel = QPushButton()
		cancel.setText("Anuluj")
		cancel.clicked.connect(self._dialog.close)
		layout.addWidget(text)
		layout.addWidget(buy)
		layout.addWidget(cancel)

		self._dialog.setLayout(layout)
		self._dialog.show()

	def buy(self, player, hero):
		if player is 1 and self.main_window.player1.gold >= 1500:
			self.main_window.player1.available_heroes.append(hero)
			self.main_window.player1.hero = hero
			self.main_window.player1.update_gold_amount(self.main_window.player1.gold - 1500)
			if hero is 2:#powinno ci pozwolić od razu kupić bohatera 3, bez konieczności posiadania najpierw 2
				self.board.set_hero_2(0, 0, self.board.player1_button2)
			else:
				self.board.set_hero_3(0, 0, self.board.player1_button3)
		elif player is 2 and self.main_window.player2.gold >= 1500:
			self.main_window.player2.available_heroes.append(hero)
			self.main_window.player2.hero = hero
			self.main_window.player2.update_gold_amount(self.main_window.player2.gold - 1500)
			pos = [self.board.parent().width - 1, self.board.parent().height - 1]
			if hero is 2:
				self.board.set_hero_2(pos[0], pos[1], self.board.player2_button2)
			else:
				self.board.set_hero_3(pos[0], pos[1], self.board.player2_button3)
		self._dialog.close()

	def set_hero_one(self):
		self.main_window.player1.hero = 1
		self.main_window.player2.hero = 1

	def set_hero_two(self):
		if self.main_window.turn % 2 is 0:
			if 2 in self.main_window.player2.available_heroes:
				self.main_window.player2.hero = 2
			else:
				self.buy_new_hero(2, 2)
		else:
			if 2 in self.main_window.player1.available_heroes:
				self.main_window.player1.hero = 2
			else:
				self.buy_new_hero(1, 2)

	def set_hero_three(self):
		if self.main_window.turn % 2 is 0:
			if 3 in self.main_window.player2.available_heroes:
				self.main_window.player2.hero = 3
			else:
				self.buy_new_hero(2, 3)
		else:
			if 3 in self.main_window.player1.available_heroes:
				self.main_window.player1.hero = 3
			else:
				self.buy_new_hero(1, 3)


