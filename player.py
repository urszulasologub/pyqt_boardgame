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
		self.dice = 3#DiceRoll(self).roll_dice()
		self.pos_x = 0
		self.pos_y = 0

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
		castle = Castle(self)
		castle_image.clicked.connect(lambda: castle.show_castle())

		self.grid.addWidget(castle_image, 0, 0)

		self.labels = [QLabel(player), QLabel('Poziom zamku: %d' % self.castle_level), QLabel('Złoto: 0'), QLabel('Wyrzucono oczek: %d' % self.dice), QLabel('Tydzień: %d, Dzień: %d' % (self.parent().week, self.parent().day))]

		i = 1
		for label in self.labels:
			self.grid.addWidget(label, i, 0)
			i += 1

		self.setLayout(self.grid)
		self.update_gold_amount(5000)
		#self.update_week_day()

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
				min-height: 70px;
			""")

		self.grid = QGridLayout(self)
		self.labels = ['Zobacz druzynę', 'Zakończ kolejkę', 'Atakuj', 'Bohater1', 'Bohater2', 'Bohater3']
		self.buttons = []

		for i in range(len(self.labels)):
			self.buttons.append(QPushButton(self.labels[i]))
			self.grid.addWidget(self.buttons[i], i, 0)

		dice = DiceRoll(self)
		self.buttons[1].clicked.connect(self.change_turn)
		self.setLayout(self.grid)

	def change_turn(self):
		self.grandpa.turn += 1
		#print(self.grandpa.turn)
		self.grandpa.roll_dice()
		self.grandpa.show_info()


