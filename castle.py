from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


class Castle(QDialog):

	def __init__(self, parent):
		super(Castle, self).__init__(parent)
		self._dialog = QDialog(self)

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
		
		units = QLabel('Dostępne:\nJednostki poziomu 1: 0\nJednostki poziomu 2: 0\nJednostki poziomu 3: 0\nJednostki poziomu 4: 0\nJednostki poziomu 5: 0\n')
		grid.addWidget(units)
		prices = ['50', '100', '500', '1000', '2500']
		available = [True, True, False, False, False]
		for i in range(len(prices)):
			if available[i]:
				grid.addWidget(QPushButton('Kup jednostkę poziomu %s za %s złota' % (str(i + 1), str(prices[i]))), i + 1, 0)



	def show_castle(self):
		dialog = Castle(self)
		dialog.exec_()