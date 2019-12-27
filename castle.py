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

		self.grid = QGridLayout(self)

		self.level1 = self.parent().in_castle_units['level_1']
		self.level2 = self.parent().in_castle_units['level_2']
		self.level3 = self.parent().in_castle_units['level_3']
		self.level4 = self.parent().in_castle_units['level_4']
		self.level5 = self.parent().in_castle_units['level_5']

		self.units = [QLabel('Dostępne:'),
					  QLabel('Jednostki poziomu 1: %d (%d)' % (self.level1, self.parent().available_units['level_1'])),
					  QLabel('Jednostki poziomu 2: %d (%d)' % (self.level2, self.parent().available_units['level_2'])),
					  QLabel('Jednostki poziomu 3: %d (%d)' % (self.level3, self.parent().available_units['level_3'])),
					  QLabel('Jednostki poziomu 4: %d (%d)' % (self.level4, self.parent().available_units['level_4'])),
					  QLabel('Jednostki poziomu 5: %d (%d)' % (self.level5, self.parent().available_units['level_5']))]

		i = 0
		for label in self.units:
			self.grid.addWidget(label, i, 0)
			i += 1
		upgrade = QLabel('Ulepsz zamek za 3000 złota')
		upgrade.setAlignment(Qt.AlignCenter)
		self.grid.addWidget(upgrade, i, 0, 1, 3)
		self.prices = ['60', '100', '400', '1000', '3000']
		available = [True, True, False, False, False]
		button = []
		for i in range(len(self.prices)):
			button.append(QPushButton('Kup jednostkę poziomu %s za %s złota' % (str(i + 1), str(self.prices[i]))))
		button[0].clicked.connect(lambda: self.buy_unit(1))
		button[1].clicked.connect(lambda: self.buy_unit(2))
		button[2].clicked.connect(lambda: self.buy_unit(3))
		button[3].clicked.connect(lambda: self.buy_unit(4))
		button[4].clicked.connect(lambda: self.buy_unit(5))

		for i in range(len(self.prices)):
			if available[i]:
				self.grid.addWidget(button[i], i + 1, 1)
				self.grid.addWidget(QPushButton('Dodaj do drużyny'), i + 1, 2)
			else:
				self.grid.addWidget(QPushButton('Aby odblokować te jednostki musisz ulepszyć zamek'), i + 1, 1, 1, 2)

	def buy_unit(self, level):
		self._dialog = QDialog()
		self._dialog.setStyleSheet("""
									background-image: url(UI/brown_background.jpg);
									background-attachment: scroll;
									border: 2px outset gray;
									border-radius: 10px;
									color: white;
									font-size: 14pt;
									font: Arial;
									min-height: 20px; """)
		self._dialog.setWindowTitle("Kup jednostki")
		self.curr_level = 'level_' + str(level)
		self.lvl = level#potrzebuję ziennej level osobno, i jako self
		print(self.curr_level)

		layout = QVBoxLayout(self._dialog)
		text = QLabel("Ile jednostek chcesz kupić?")

		hlay = QHBoxLayout()
		minus = QPushButton('-')
		minus.setStyleSheet("min-width: 20px; max-width: 20px;")
		minus.clicked.connect(self.substract)
		self.slider = QSlider(Qt.Horizontal)
		self.slider.setValue(1)
		self.max_units = self.parent().available_units[self.curr_level]
		self.slider.setMaximum(self.max_units)
		self.slider.valueChanged[int].connect(self.changeValue)
		plus = QPushButton('+')
		plus.setStyleSheet("min-width: 20px; max-width: 20px;")
		plus.clicked.connect(self.add)
		self.value = QLabel()
		self.value.setAlignment(Qt.AlignCenter)
		self.value.setText(str(1))

		self.full_price = QLabel("Suma do zapłaty: %s" % self.prices[level-1])# taki napis?

		hlay.addWidget(minus)
		hlay.addWidget(self.slider)
		hlay.addWidget(plus)

		buy = QPushButton()
		buy.setText("Kup")
		buy.clicked.connect(self.buy)
		cancel = QPushButton()
		cancel.setText("Anuluj")
		cancel.clicked.connect(self._dialog.close)

		layout.addWidget(text)
		layout.addLayout(hlay)
		layout.addWidget(self.value)
		layout.addWidget(self.full_price)

		layout.addWidget(buy)
		layout.addWidget(cancel)
		self._dialog.setLayout(layout)
		self._dialog.exec_()

	def buy(self):
		print("kupione xD")
		#po kupieniu musi zupdejtować player info, więc zupdejtuje całą planszę xd
		self._dialog.close()

	def substract(self):
		value = self.slider.value()
		if value is not 0:
			self.slider.setValue(value-1)

	def changeValue(self, value):
		#zmiana wartości do zakupu w jakiejś zmiennej, wystarczy tylko tu
		self.value.setText(str(value))
		self.full_price.setText("Suma do zapłaty: %d" % (int(self.prices[self.lvl-1]) * value))

	def add(self):
		value = self.slider.value()
		if value is not self.max_units:
			self.slider.setValue(value+1)
