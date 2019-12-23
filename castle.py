from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


class Castle(QDialog):

	def __init__(self, parent):
		super(Castle, self).__init__(parent)
		self._dialog = QDialog(self)
		self.setWindowTitle("Zamek")

		self.setStyleSheet("""
				background-image: url(UI/brown_background.jpg);
				background-attachment: scroll;
				border: 2px outset gray;
				border-radius: 10px;
				color: white;
				font-size: 14pt;
				font: Arial;
				min-height: 20px;
			""")

		grid = QGridLayout(self)

		self.level1 = self.parent().in_castle_units['level_1']
		self.level2 = self.parent().in_castle_units['level_2']
		self.level3 = self.parent().in_castle_units['level_3']
		self.level4 = self.parent().in_castle_units['level_4']
		self.level5 = self.parent().in_castle_units['level_5']


		units = QLabel(
			'Dostępne:\nJednostki poziomu 1: %d (%d)\nJednostki poziomu 2: %d (%d)\nJednostki poziomu 3: %d (%d)\nJednostki poziomu 4: %d (%d)\nJednostki poziomu 5: %d (%d)\n'
			% (self.level1, self.parent().available_units['level_1'], 
				self.level2, self.parent().available_units['level_2'], 
				self.level3, self.parent().available_units['level_3'], 
				self.level4, self.parent().available_units['level_4'],
				self.level5, self.parent().available_units['level_5']))# nie wiem do czego odnosi się 0 w nawiasie, więc nic z tym nie robię xd
			#odnosi się do ilości jednostek, które mozna kupić
		
		grid.addWidget(units)
		upgrade = QLabel('Ulepsz zamek za 3000 złota')
		grid.addWidget(upgrade)
		prices = ['60', '100', '400', '1000', '3000']
		available = [True, True, False, False, False]
		for i in range(len(prices)):
			if available[i]:
				grid.addWidget(QPushButton('Kup jednostkę poziomu %s za %s złota' % (str(i + 1), str(prices[i]))), i + 2, 0)
