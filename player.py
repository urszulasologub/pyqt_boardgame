import os, sys

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtPrintSupport import *
from dice import DiceRoll
from castle import Castle

class PlayerInfo(QWidget):
	def __init__(self, parent, player):
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

		self.labels = [QLabel(player), QLabel('Poziom zamku: 1'), QLabel('Złoto: 0'), QLabel('Wyrzucono oczek: 3'), QLabel('Tydzień: 1, Dzień: 1')]

		i = 1
		for label in self.labels:
			self.grid.addWidget(label, i, 0)
			i += 1

		self.setLayout(self.grid)
		self.update_gold_amount(5000)


	def update_castle_level(self, level):
		text = 'Poziom zamku: ' + str(level)
		self.labels[1] = QLabel(text)
		self.grid.addWidget(self.labels[1], 2, 0)
				
	
	def update_gold_amount(self, amount):
		text = 'Złoto: ' + str(amount)
		self.labels[2] = QLabel(text)
		self.grid.addWidget(self.labels[2], 3, 0)


	def update_dice_amount(self, amount):
		text = 'Wyrzucono oczek: ' + str(amount)
		self.labels[3] = QLabel(text)
		self.grid.addWidget(self.labels[3], 4, 0)


class PlayerActions(QWidget):
	def __init__(self, parent, player):
		super(PlayerActions, self).__init__(parent)
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
		self.buttons[1].clicked.connect(lambda: dice.roll_dice())
		self.setLayout(self.grid)


