from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from random import randrange
from PyQt5.QtMultimedia import QSound 


class DiceRoll(QDialog):

	def __init__(self, parent):
		super(DiceRoll, self).__init__(parent)
		self._dialog = QDialog(self)

		self.setStyleSheet("""
				background-image: url(UI/brown_background.jpg);
				background-attachment: scroll;
				border: 2px outset gray;
				border-radius: 10px;
				color: white;
				font-size: 18pt;
				font: Arial;
				min-height: 15px;
			""")

		grid = QGridLayout(self)

		image = QLabel()
		dice_gif = QMovie('UI/dice.gif')
		dice_gif.setScaledSize(QSize(100, 150))
		image.setMovie(dice_gif)
		grid.addWidget(image)

		dice = randrange(1, 6)
		text = 'Wyrzucono %s oczek' % str(dice)
		message = QLabel(text)
		grid.addWidget(message)

		ok = QPushButton('OK')
		ok.clicked.connect(self.okButton)
		grid.addWidget(ok)

		sound = QSound('audio/dice.wav')
		sound.play()

		self.setLayout(grid)
		dice_gif.start()



	def okButton(self):
		self.close()


	def roll_dice(self):
		dialog = DiceRoll(self)
		dialog.exec_()