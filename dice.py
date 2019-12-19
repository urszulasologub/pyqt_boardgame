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
			""")

		dice = randrange(1, 6)
		text = 'Wyrzucono %s oczek' % str(dice)
		message = QLabel(text)

		buttons = QHBoxLayout()
		ok = QPushButton('OK')
		ok.clicked.connect(self.okButton)

		image = QLabel()
		dice_gif = QMovie('UI/dice.gif')
		image.setMovie(dice_gif)

		sound = QSound('audio/dice.wav')
		sound.play()

		layout = QHBoxLayout(self)
		layout.addWidget(image)
		layout.addWidget(message)
		layout.addWidget(ok)

		dice_gif.start()

		self.setLayout(layout)



	def okButton(self):
		self.close()


	def roll_dice(self):
		dialog = DiceRoll(self)
		dialog.show()