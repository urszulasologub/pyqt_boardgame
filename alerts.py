import os, sys
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtPrintSupport import *
from player import *


class Alert(QDialog):

	def __init__(self, parent):
		super(Alert, self).__init__(parent)
		self._dialog = QDialog(self)
		self.setStyleSheet("""
			QDialog, QLabel, QPushButton {
			background-image: url(UI/brown_background.jpg);
			background-attachment: scroll;
			border: 2px outset gray;
			border-radius: 10px;
			color: white;
			font-size: 18pt;
			font: Arial;
			min-height: 15px;}
			
			QPushButton:pressed {
			background-image: url(UI/darker_brown_background.jpg);}
			""")

	def get_prize(self, amount):
		self.setWindowTitle('Znalazłeś skarb')
		grid = QGridLayout(self)

		label = QLabel(self)
		pixmap = QPixmap('UI/treasure_icon.png')
		pixmap = pixmap.scaledToHeight(200)
		label.setPixmap(pixmap)
		grid.addWidget(label)

		text = 'Znajdujesz %d sztuk złota!' % amount
		message = QLabel(text)
		grid.addWidget(message)

		ok = QPushButton('OK')
		ok.clicked.connect(lambda: self.close())
		grid.addWidget(ok)

		self.setLayout(grid)
		self.exec_()

	
	def get_battle(self, level, team):
		grid = QGridLayout(self)

		label = QLabel(self)
		if level == 'easy':
			self.setWindowTitle('Łatwa walka')
			pixmap = QPixmap('sprites/skeleton.png')
			text = 'Zaatakował cię mały oddział.\nCzeka cię łatwa walka'
		elif level == 'medium':
			self.setWindowTitle('Średnia walka')
			pixmap = QPixmap('sprites/ghost.png')
			text = 'Na swojej drodze napotkałeś małą brygadę.\nPrzygotuj się na wyrównaną bitwę'			
		else:
			self.setWindowTitle('Trudna walka')
			pixmap = QPixmap('sprites/dragon.png')
			text = 'Trafiłeś na wielką armię.\nPowodzenia w walce'

		pixmap = pixmap.scaledToHeight(200)
		label.setPixmap(pixmap)
		grid.addWidget(label)

		message = QLabel(text)
		grid.addWidget(message)

		opponents = 'Jednostki poziomu 1: %d\nJednostki poziomu 2: %d\nJednostki poziomu 3: %d\nJednostki poziomu 4: %d\nJednostki poziomu 5: %d' % (team['level_1'], team['level_2'], team['level_3'], team['level_4'], team['level_5'])
		opponents_label = QLabel(opponents)
		grid.addWidget(opponents_label)

		ok = QPushButton('OK')
		ok.clicked.connect(lambda: self.close())
		grid.addWidget(ok)

		self.setLayout(grid)
		self.exec_()


	def victory(self, main_window, player):
		self.setWindowTitle('Koniec gry')
		grid = QGridLayout(self)

		label = QLabel(self)
		if player.color == 'darkblue':
			pixmap = QPixmap('UI/blue_victory.png')
			name = 'Gracz 2'
		else:
			pixmap = QPixmap('UI/red_victory.png')
			name = 'Gracz 1'

		pixmap = pixmap.scaledToWidth(400)
		label.setPixmap(pixmap)
		grid.addWidget(label)

		text = 'Zwycięstwo!\nUdało się podbić zamek przeciwnika!\nWygrywa %s' % name
		message = QLabel(text)
		grid.addWidget(message)

		ok = QPushButton('OK')
		ok.clicked.connect(lambda: self.close_all(main_window))
		grid.addWidget(ok)

		self.setLayout(grid)
		self.exec_()

	
	def close_all(self, main_window):
		self.close()
		main_window.close()
		