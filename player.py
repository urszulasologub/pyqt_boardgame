import os, sys

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtPrintSupport import *
from dice import DiceRoll
from castle import Castle


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
		self.avaliable_heroes = [1]
		self.can_move = False

		self.h1units = {
			"level_1": 0,
			"level_2": 0,
			"level_3": 0,
			"level_4": 0,
			"level_5": 0
		}

		self.h2units = {
			"level_1": 0,
			"level_2": 0,
			"level_3": 0,
			"level_4": 0,
			"level_5": 0
		}

		self.h3units = {
			"level_1": 0,
			"level_2": 0,
			"level_3": 0,
			"level_4": 0,
			"level_5": 0
		}

		self.in_castle_units = {
			"level_1": 10, #do testów losowe wartości
			"level_2": 4,
			"level_3": 1000,
			"level_4": 0,
			"level_5": 0
		}

		self.unit_atk = {
			"level_1": 0,
			"level_2": 0,
			"level_3": 0,
			"level_4": 0,
			"level_5": 0
		}
		self.unit_def = {
			"level_1": 0,
			"level_2": 0,
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

#akcje zawsze są te same, więc nie potrzeba podawać gracza
class PlayerActions(QWidget):
	def __init__(self, parent):
		super(PlayerActions, self).__init__(parent)
		self.grandpa = self.parent().parent()
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

		dice = DiceRoll(self)
		self.buttons[1].clicked.connect(self.change_turn)
		self.buttons[3].clicked.connect(self.set_hero_one)
		self.buttons[4].clicked.connect(self.set_hero_two)
		self.buttons[5].clicked.connect(self.set_hero_three)
		self.buttons[6].clicked.connect(self.move)
		self.setLayout(self.grid)

	def move(self):
		if self.grandpa.turn % 2 is 0:
			hero = self.grandpa.player2.hero
			player = self.grandpa.player2
		else:
			hero = self.grandpa.player1.hero
			player = self.grandpa.player1

		if player.can_move:
			self.move_hero(player, hero, self.grandpa.height, self.grandpa.width)
			player.can_move = False
			#Zmienić wartoś nowej zmiennej, że już się ruszył
			self.grandpa.show_info()
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
		self.grandpa.turn += 1
		#print(self.grandpa.turn)
		self.grandpa.roll_dice()
		self.grandpa.show_info()

	def buy_new_hero(self, player, hero):
		self._dialog = QDialog()
		self._dialog.setWindowTitle("Kup bohatera")
		layout = QVBoxLayout(self._dialog)#tymczasowo
		text = QLabel()
		text.setText("Tu kupisz nowego bohatera.\n Wiem, że wygląda brzydko xD")
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
		if player is 1:
			self.grandpa.player1.avaliable_heroes.append(hero)
			self.grandpa.player1.hero = hero
		else:
			self.grandpa.player2.avaliable_heroes.append(hero)
			self.grandpa.player2.hero = hero
		self._dialog.close()

	def set_hero_one(self):# chciałam zrobić na podstawie tekstu jaki jest na buttonie, ale nie wiem jak go wyciągnąć, więc są 3 funkcje xd
		print("h1") #uważam, że od początku bohater1 powinien być dostępy, więc nie daje opcji kupienia go
		self.grandpa.player1.hero = 1
		self.grandpa.player2.hero = 1

	def set_hero_two(self):
		print("h2")
		if self.grandpa.turn % 2 is 0:
			if 2 in self.grandpa.player2.avaliable_heroes:
				self.grandpa.player2.hero = 2
			else:
				self.buy_new_hero(2, 2)
		else:
			if 2 in self.grandpa.player1.avaliable_heroes:
				print("hello")
				self.grandpa.player1.hero = 2
			else:
				self.buy_new_hero(1, 2)


	def set_hero_three(self):
		print("h3")
		if self.grandpa.turn % 2 is 0:
			if 3 in self.grandpa.player2.avaliable_heroes:
				self.grandpa.player2.hero = 3
			else:
				self.buy_new_hero(2, 3)
		else:
			if 3 in self.grandpa.player1.avaliable_heroes:
				self.grandpa.player1.hero = 3
			else:
				self.buy_new_hero(1, 3)

